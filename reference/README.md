# Material de referencia local

Esta carpeta contiene insumos de consulta, no fuentes canónicas del curso. Está
separada deliberadamente de `quarto/`, donde viven las presentaciones que se editan
y publican.

## Estructura

```text
reference/
├── slides/
│   └── clustering/     # Decks y material visual recibido como referencia
└── book-excerpts/
    ├── hands-on-machine-learning/
    ├── data-science-for-business/
    └── ensemble-methods-for-machine-learning/
```

### `slides/`

Contiene presentaciones o PDFs externos usados para comparar cobertura, ejemplos y
secuencia pedagógica. No son la fuente de las clases publicadas y no deben editarse
como sustituto de `quarto/<tema>/index.qmd`.

### `book-excerpts/`

Contiene copias locales de texto de libros para consulta privada. Estos archivos:

- no están versionados por Git;
- no deben publicarse, redistribuirse ni copiarse extensamente en las diapositivas;
- deben usarse para comprender y parafrasear conceptos;
- requieren citar la obra original mediante el `references.bib` del tema.

La bibliografía citable no vive aquí: está en
`quarto/<tema>/references.bib`. Antes de usar un extracto, verifica la edición y la
atribución en ese archivo BibTeX.

## Convención para nuevos materiales

- Deck externo: `reference/slides/<tema>/nombre-descriptivo.pptx`.
- Extracto de libro: `reference/book-excerpts/<libro>/chapter-NN.txt`.
- Artículo o enlace citable: agrégalo al `references.bib` de la presentación.
- Recurso que debe publicarse: colócalo junto a la fuente Quarto siguiendo las
  reglas de `AGENTS.md`, no en esta carpeta.
