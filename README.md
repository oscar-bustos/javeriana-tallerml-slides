# Taller de Machine Learning — Pontificia Universidad Javeriana

Material docente del curso **Técnicas de Aprendizaje de Máquina**: presentaciones
interactivas en Quarto/Reveal.js, talleres y recursos reproducibles en Python.

## Contenido

| Clase | Tema | Fuente | Presentación compilada |
|---:|---|---|---|
| 01 | Introducción a la IA | [`quarto/intro_ia/index.qmd`](quarto/intro_ia/index.qmd) | [`docs/intro_ia.html`](docs/intro_ia.html) |
| 02 | Modelos lineales | [`quarto/modelos_lineales/index.qmd`](quarto/modelos_lineales/index.qmd) | [`docs/modelos_lineales.html`](docs/modelos_lineales.html) |
| 03 | Árboles de decisión | [`quarto/arboles_decision/index.qmd`](quarto/arboles_decision/index.qmd) | [`docs/arboles_decision.html`](docs/arboles_decision.html) |
| 04 | Métodos de ensamble | [`quarto/ensambles/index.qmd`](quarto/ensambles/index.qmd) | [`docs/ensambles.html`](docs/ensambles.html) |
| 05 | Máquinas de soporte vectorial | [`quarto/svm/index.qmd`](quarto/svm/index.qmd) | [`docs/svm.html`](docs/svm.html) |
| 06 | Clustering | [`quarto/clustering/index.qmd`](quarto/clustering/index.qmd) | [`docs/clustering.html`](docs/clustering.html) |
| 07 | Redes neuronales | [`quarto/redes_neuronales/index.qmd`](quarto/redes_neuronales/index.qmd) | [`docs/redes_neuronales.html`](docs/redes_neuronales.html) |
| 08 | Aprendizaje profundo | [`quarto/aprendizaje_profundo/index.qmd`](quarto/aprendizaje_profundo/index.qmd) | [`docs/aprendizaje_profundo.html`](docs/aprendizaje_profundo.html) |
| 09 | Redes convolucionales | [`quarto/cnn/index.qmd`](quarto/cnn/index.qmd) | [`docs/cnn.html`](docs/cnn.html) |
| 10 | Modelos de lenguaje grandes | [`quarto/llms/index.qmd`](quarto/llms/index.qmd) | [`docs/llms.html`](docs/llms.html) |

El índice navegable de las clases compiladas está en [`docs/index.html`](docs/index.html).

## Requisitos

- [Quarto](https://quarto.org/docs/get-started/) disponible en `PATH`.
- Python 3.9 o posterior para los scripts auxiliares.
- Las dependencias de [`quarto/clustering/requirements.txt`](quarto/clustering/requirements.txt)
  solo son necesarias para regenerar las figuras de clustering.

## Inicio rápido

Clona el repositorio y, desde su raíz, compila una presentación:

```bash
python3 .agents/scripts/compile_quarto.py quarto/clustering/index.qmd
```

El script ejecuta Quarto desde el directorio de la fuente, mueve el resultado a
`docs/clustering.html` y elimina el `index.html` temporal. Para compilar todas las
presentaciones:

```bash
python3 .agents/scripts/compile_quarto.py
```

Para reconstruir todas las presentaciones y el índice del portal:

```bash
python3 .agents/scripts/publish_docs.py
```

> `publish_docs.py` invoca internamente el comando `python`. En sistemas que no
> tengan ese alias, usa `compile_quarto.py` con `python3` y conserva el índice
> existente, o configura el alias correspondiente.

## Regenerar las visualizaciones de clustering

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r quarto/clustering/requirements.txt
python3 quarto/clustering/generate_figures.py --all
python3 quarto/clustering/country_narrative.py --all
```

Los resultados reproducibles se guardan en
`quarto/clustering/assets/generated/`.

## Estructura del repositorio

```text
.
├── quarto/                 # Fuentes .qmd, bibliografías y tema compartido
│   └── <tema>/index.qmd
├── docs/                   # HTML autónomo, versionado y listo para publicar
├── homework/               # Talleres, preguntas y notebooks para estudiantes
├── planning/               # Pendientes e ideas todavía no publicables
├── reference/              # Decks y extractos de libros para consulta local
├── course-admin/           # Programa y datos administrativos locales
├── .agents/
│   ├── scripts/            # Compilación, publicación y utilidades reproducibles
│   └── skills/             # Flujos especializados para asistentes compatibles
└── .github/workflows/      # Despliegue automático de docs/
```

`quarto/custom.scss` define el tema compartido. Cada presentación mantiene sus
referencias en un archivo `references.bib` local. Los HTML usan
`embed-resources: true`, por lo que son artefactos autónomos.

## Fuentes, referencias y material local

Hay tres categorías distintas:

- `quarto/<tema>/references.bib` contiene las referencias bibliográficas que se
  citan y publican con cada presentación.
- `reference/slides/` contiene decks externos usados únicamente como inspiración o
  comparación pedagógica.
- `reference/book-excerpts/` contiene copias locales de capítulos para consulta
  privada. No se versionan ni se redistribuyen; las ideas se parafrasean y se cita
  siempre la obra original.

El programa del curso y la lista de clase están separados en `course-admin/`. Esta
última se considera información privada y permanece fuera de Git. Consulta
[`reference/README.md`](reference/README.md) y
[`course-admin/README.md`](course-admin/README.md) para más detalles.

## Flujo de edición

1. Edita la fuente en `quarto/<tema>/index.qmd`; no edites el HTML compilado a mano.
2. Mantén las citas en `quarto/<tema>/references.bib` y usa claves Pandoc como
   `[@autor2024]`.
3. Compila únicamente la presentación modificada durante la iteración.
4. Revisa visualmente la presentación y comprueba que no haya desbordamientos.
5. Incluye en el mismo cambio la fuente y su `docs/<tema>.html` actualizado.

Las convenciones completas de contenido, validación y trabajo asistido están en
[`AGENTS.md`](AGENTS.md). Para proponer cambios, consulta
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## Automatización y despliegue

Cada `push` a `main` ejecuta [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml).
El flujo copia el contenido precompilado de `docs/` al directorio `slides/` del
repositorio `oscar-bustos/javeriana-tallerml`. Por eso el HTML debe compilarse y
versionarse antes de integrar un cambio.

## Instrucciones para asistentes de IA

`AGENTS.md` es la referencia canónica. Los archivos `CLAUDE.md`, `GEMINI.md`,
`.github/copilot-instructions.md` y `.cursor/rules/repository.mdc` son adaptadores
breves para herramientas específicas; `llms.txt` ofrece un índice compacto del
repositorio. Si hay una discrepancia, prevalece `AGENTS.md`.

## Licencia

Este proyecto se distribuye bajo los términos descritos en [`LICENSE`](LICENSE).
