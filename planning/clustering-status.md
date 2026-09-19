# Pendientes — presentación de clustering

## Estado actual

- Está implementado el hilo conductor “¿Qué país se parece más a Colombia?”.
- El ejemplo de Carlos III y Ozzy Osbourne fue reemplazado por dos estudiantes ficticios de Bogotá.
- Se incorporaron los casos de negocio y las ideas de
  `reference/book-excerpts/data-science-for-business/chapter-06.txt`.
- La Tarea 6 conserva 50 puntos e incluye la comparación de vecinos de Colombia.
- `generate_figures.py` incluye `--figure colombia_similarity` y valida los resultados esperados.
- `python generate_figures.py --all` terminó correctamente, incluidas las capturas de PCA y K-Means.
- La figura de MiniBatch usa un proxy determinista; dos ejecuciones produjeron el mismo hash.
- Se añadió `provost2013data` a `quarto/clustering/references.bib`.
- La presentación fue recompilada y `docs/clustering.html` corresponde al estado final de `index.qmd`.

## Verificación final completada

- Compilación completa sin advertencias bibliográficas.
- Inspección a 1280×720 de las 73 pantallas, con todos los fragmentos visibles.
- `overflow_count = 0`.
- Revisión visual satisfactoria de las nueve diapositivas señaladas.
- NotebookLM, PCA, K-Means, datos y diccionario responden con HTTP 200.
- Rúbrica de la Tarea 6: 50 puntos.
- No hay menciones a Carlos III, Prince Charles, Ozzy Osbourne ni “príncipe de las tinieblas”.
- Existen los 18 recursos locales referenciados por la presentación.
- `git diff --check` sin errores.

## Pendiente opcional

1. Revisar el `git diff` con el usuario.
2. Hacer commit y push únicamente si el usuario lo solicita.

## Archivos con cambios pendientes

- `quarto/clustering/index.qmd`
- `quarto/clustering/generate_figures.py`
- `quarto/clustering/references.bib`
- `quarto/clustering/assets/generated/colombia_similarity.png`
- `quarto/clustering/assets/generated/interactive_pca.png`
- `quarto/clustering/assets/generated/interactive_kmeans.png`
- `quarto/clustering/assets/generated/minibatch_tradeoff.png`
- `homework/Tarea6_KMeans.md`
- `docs/clustering.html`
