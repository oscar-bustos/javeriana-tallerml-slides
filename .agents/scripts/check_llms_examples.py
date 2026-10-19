#!/usr/bin/env python3
"""Check slide snippets and run the dependency-free part of the LLM lesson.

Run from the repository root with Python 3. This does not load embedding weights,
install packages, request credentials, or call the generation service.
"""

import ast
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "quarto/llms/index.qmd"


def main():
    source = SOURCE.read_text(encoding="utf-8")
    snippets = re.findall(r"^```python\n(.*?)^```", source, re.M | re.S)
    for number, snippet in enumerate(snippets, start=1):
        ast.parse(snippet, filename=f"{SOURCE.name}:snippet-{number}")
    wide = [
        f"snippet {number}, line {line_number}: {len(line)} characters"
        for number, snippet in enumerate(snippets, start=1)
        for line_number, line in enumerate(snippet.splitlines(), start=1)
        if len(line) > 68
    ]
    if wide:
        raise ValueError("Shorten lines for slide readability: " + "; ".join(wide))

    sections = re.split(r"^## (.+)\n", source, flags=re.M)
    by_title = {
        title: re.findall(r"^```python\n(.*?)^```", body, re.M | re.S)
        for title, body in zip(sections[1::2], sections[2::2])
    }
    namespace = {}

    def run(title):
        blocks = by_title[title]
        if len(blocks) != 1:
            raise ValueError(f"Expected one Python block in: {title}")
        with redirect_stdout(StringIO()):
            exec(compile(blocks[0], title, "exec"), namespace)

    for title in [
        "Las palabras pueden cambiar",
        "Normalizar simplifica la comparación",
        "La práctica usa dos páginas",
        "Fragmentar define tamaño y solape",
        "La lista mantiene texto y metadatos",
    ]:
        run(title)

    assert namespace["coincidencias"] == set(), "Unexpected lexical intersection"
    assert namespace["x_unitario"] == [0.6, 0.8], "Unexpected normalization"
    chunks = namespace["chunks"]
    assert len(chunks) == 2, "Initial corpus must produce two chunks"
    assert [c["id"] for c in chunks] == ["v1-p17-w0", "v1-p42-w0"]
    assert "treinta días" in chunks[0]["texto"], "Notice period was lost"
    assert all(c["documento"] == "contrato_demo.pdf" for c in chunks)

    # Exercise provenance formatting without pretending to compute embeddings.
    namespace["hallazgos"] = chunks
    namespace["pregunta"] = "¿Puedo cancelar antes del vencimiento?"
    run("El contexto incluye etiquetas citables")
    run("El prompt delimita la tarea")
    for chunk in chunks:
        label = f"[{chunk['id']}] {chunk['documento']}, p. {chunk['pagina']}"
        assert label in namespace["entrada"], "Source label missing from prompt"
        assert chunk["texto"] in namespace["entrada"], "Evidence missing from prompt"

    print(f"Syntax valid in {len(snippets)} Python snippets.")
    print("Executed lexical comparison, normalization, corpus, chunking and prompt.")
    print("Embedding inference and generation API were not executed.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, SyntaxError, ValueError, KeyError, AssertionError) as error:
        sys.exit(f"LLM example verification failed: {error}")
