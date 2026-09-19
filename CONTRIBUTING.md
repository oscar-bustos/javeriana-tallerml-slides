# Contribuir

Gracias por mejorar el material del curso. Las fuentes están en `quarto/`, los
ejercicios en `homework/` y las presentaciones listas para publicar en `docs/`.

## Preparación

1. Instala Python 3.9 o posterior y [Quarto](https://quarto.org/docs/get-started/).
2. Crea una rama de trabajo a partir de `main`.
3. Lee [`AGENTS.md`](AGENTS.md), incluso si el cambio se realiza manualmente.
4. Revisa `git status --short` antes de empezar.

Para regenerar las visualizaciones de clustering, instala sus dependencias en un
entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r quarto/clustering/requirements.txt
```

En PowerShell, activa el entorno con `.venv\Scripts\Activate.ps1`.

## Cambiar una presentación

1. Edita `quarto/<tema>/index.qmd`.
2. Actualiza `quarto/<tema>/references.bib` si agregas citas.
3. Compila solo esa presentación mientras iteras:

   ```bash
   python3 .agents/scripts/compile_quarto.py quarto/<tema>/index.qmd
   ```

4. Abre `docs/<tema>.html` y revisa cada diapositiva afectada.
5. Versiona juntos el `.qmd`, la bibliografía o recursos necesarios y el HTML.

No cambies directamente `docs/<tema>.html`: Quarto sobrescribirá la edición.

## Usar material de referencia

`reference/slides/` contiene decks externos y `reference/book-excerpts/` contiene
copias locales de texto. Ninguno es fuente publicable ni debe agregarse a Git.
Parafrasea las ideas necesarias y registra la obra original en el `references.bib`
de la presentación. Los archivos de `course-admin/private/` contienen información
administrativa y no deben utilizarse en contribuciones.

## Cambiar figuras o datos reproducibles

Las figuras de clustering se regeneran así:

```bash
python3 quarto/clustering/generate_figures.py --all
python3 quarto/clustering/country_narrative.py --all
```

Incluye tanto el generador como las salidas modificadas. No edites manualmente los
PNG o CSV de `quarto/clustering/assets/generated/`.

## Comprobaciones antes de entregar

```bash
python3 -m compileall -q .agents/scripts quarto/clustering
git diff --check
git status --short
```

Además, compila y revisa visualmente todas las presentaciones afectadas. Si no fue
posible instalar Quarto o alguna dependencia, anota claramente la validación
pendiente y el comando para reproducirla.

## Lista de revisión

- [ ] El cambio está limitado al objetivo propuesto.
- [ ] Las diapositivas respetan las reglas de densidad y no se desbordan.
- [ ] Las citas, enlaces e imágenes se resuelven.
- [ ] Los archivos generados corresponden a sus fuentes.
- [ ] No se incluyen secretos, cachés, entornos virtuales ni cambios ajenos.
- [ ] La descripción explica qué cambió y cómo se validó.
