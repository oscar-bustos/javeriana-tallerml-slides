#!/usr/bin/env python3
"""Inspect a local Reveal deck and save screenshots outside the repository.

Run from any directory; paths to the HTML resolve from the repository root.
Requires the locally installed Playwright browser and Pillow for contact sheets.
"""

import argparse
import ast
import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]


def inspect(html, output, width, height):
    output.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height})
        page.route("**/*", lambda route: (
            route.abort() if route.request.url.startswith(("http:", "https:"))
            else route.continue_()
        ))
        page.goto(html.as_uri())
        page.wait_for_function("window.Reveal && Reveal.isReady()")
        page.evaluate("document.fonts.ready")
        page.evaluate("Reveal.configure({transition: 'none'})")
        slides = page.evaluate("""Reveal.getSlides().map(slide => ({
            ...Reveal.getIndices(slide),
            title: slide.querySelector('h1,h2')?.textContent || slide.id
        }))""")
        results = []
        for index, slide in enumerate(slides):
            page.evaluate("({h,v}) => Reveal.slide(h, v, -1)", slide)
            if page.locator("section.present .fragment").count():
                page.screenshot(path=str(output / f"{index + 1:02d}-question.png"))
            page.evaluate("""({h,v}) => {
                Reveal.slide(h, v, 999);
                Reveal.getCurrentSlide().querySelectorAll('.fragment')
                    .forEach(el => el.classList.add('visible'));
            }""", slide)
            page.wait_for_timeout(80)
            problems = page.evaluate("""() => {
                const slide = Reveal.getCurrentSlide();
                const bounds = {left: 0, right: innerWidth, bottom: innerHeight - 12};
                if (slide.classList.contains('scrollable')) return [];
                return [...slide.querySelectorAll('h1,h2,p,li,table,pre,img,mjx-container')]
                    .filter(el => !el.closest('aside') && el.getBoundingClientRect().height)
                    .flatMap(el => {
                        const r = el.getBoundingClientRect();
                        const outside = r.bottom > bounds.bottom + 3 ||
                            r.right > bounds.right + 3 || r.left < bounds.left - 3 ||
                            r.top < -3;
                        const clippedCode = el.tagName === 'PRE' &&
                            (el.scrollWidth > el.clientWidth + 2 ||
                             el.scrollHeight > el.clientHeight + 2);
                        return outside || clippedCode ? [{
                            tag: el.tagName, text: el.textContent.slice(0,100),
                            outside, clippedCode
                        }] : [];
                    });
            }""")
            page.screenshot(path=str(output / f"{index + 1:02d}.png"))
            results.append({"slide": index + 1, **slide, "problems": problems})
        resources = page.evaluate("""() => ({
            brokenImages: [...document.images].filter(img => !img.naturalWidth).length,
            unrenderedMath: document.querySelectorAll('.math:not(:has(math)):not(:has(.katex))').length,
            unresolvedCitations: document.querySelectorAll('.citation .citeproc-not-found').length
        })""")
        browser.close()
    (output / "layout.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    from PIL import Image, ImageDraw

    thumb_width = 420
    thumb_height = round(height * thumb_width / width)
    for start in range(0, len(results), 12):
        sheet = Image.new("RGB", (thumb_width * 3, (thumb_height + 24) * 4), "#dddddd")
        draw = ImageDraw.Draw(sheet)
        for offset, result in enumerate(results[start:start + 12]):
            x = (offset % 3) * thumb_width
            y = (offset // 3) * (thumb_height + 24)
            with Image.open(output / f"{result['slide']:02d}.png") as shot:
                sheet.paste(shot.resize((thumb_width, thumb_height)), (x, y))
            draw.text((x + 8, y + thumb_height + 4), str(result["slide"]), fill="black")
        sheet.save(output / f"contact-{start // 12 + 1}.png")
    flagged = [result for result in results if result["problems"]]
    print(json.dumps({"slides": len(results), "resources": resources,
                      "flagged": flagged}, ensure_ascii=False))
    return bool(flagged) or any(resources.values())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, default=1440)
    parser.add_argument("--height", type=int, default=960)
    parser.add_argument("--source", type=Path, help="Also check Python snippet syntax in this QMD")
    args = parser.parse_args()
    html = (ROOT / args.html).resolve()
    if not html.is_file():
        parser.error(f"HTML file not found: {html}")
    try:
        if args.source:
            source = (ROOT / args.source).read_text(encoding="utf-8")
            snippets = re.findall(r"^```python\n(.*?)^```", source, re.M | re.S)
            for index, snippet in enumerate(snippets, 1):
                ast.parse(snippet, filename=f"{args.source}:snippet-{index}")
            print(f"Python syntax valid in {len(snippets)} snippets (not executed).")
        failed = inspect(html, args.output.resolve(), args.width, args.height)
    except Exception as error:
        parser.exit(1, f"Reveal inspection failed: {error}\n")
    if failed:
        parser.exit(1, "Review the flagged slides or resources.\n")


if __name__ == "__main__":
    main()
