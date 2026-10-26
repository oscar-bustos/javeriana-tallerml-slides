#!/usr/bin/env python3
"""Build the time-series deck with the shared compiler and normalize its HTML.

Run: python3 .agents/scripts/compile_series_tiempo.py

Quarto's embedded CSS/JS templates contain trailing spaces. This wrapper removes
only line-end whitespace from the generated artifact so new files pass Git's
whitespace checks. It does not modify sources or any other presentation.
"""

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "quarto" / "series_tiempo" / "index.qmd"
OUTPUT = ROOT / "docs" / "series_tiempo.html"


def main():
    compiler = ROOT / ".agents" / "scripts" / "compile_quarto.py"
    try:
        subprocess.run([sys.executable, str(compiler), str(SOURCE)], cwd=ROOT, check=True)
        html = OUTPUT.read_text(encoding="utf-8")
        # splitlines() also splits Unicode separators inside embedded JavaScript
        # strings/regexes. Only ASCII newlines and trailing spaces are safe here.
        normalized = "\n".join(line.rstrip(" \t\r") for line in html.split("\n"))
        if not normalized.endswith("\n"):
            normalized += "\n"
        if normalized != html:
            with OUTPUT.open("w", encoding="utf-8", newline="\n") as stream:
                stream.write(normalized)
        print("Time-series HTML built and line-end whitespace normalized.")
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"Time-series build failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
