# Guía canónica para agentes

Este archivo aplica a todo el repositorio. Un `AGENTS.md` más profundo puede añadir
reglas para su subárbol, pero no debe contradecir estas instrucciones. `README.md`
explica el uso humano del proyecto; este archivo define cómo modificarlo con
seguridad.

## Objetivo y fuentes de verdad

- El repositorio contiene material docente en español para el curso **Técnicas de
  Aprendizaje de Máquina**.
- `quarto/<tema>/index.qmd` es la fuente de cada presentación.
- `quarto/<tema>/references.bib` es la bibliografía local de esa presentación.
- `quarto/custom.scss` es el tema compartido.
- `docs/<tema>.html` es un artefacto generado, autónomo y versionado.
- `homework/` contiene material entregable para estudiantes.
- `reference/slides/` contiene decks externos de consulta, no fuentes editables.
- `reference/book-excerpts/` contiene texto local de libros y nunca se publica.
- `course-admin/private/` puede contener datos personales y está fuera de Git.
- `planning/` contiene ideas y estados de trabajo todavía no publicables.
- `.agents/scripts/` contiene automatización; evita comandos ad hoc si ya existe
  un script reproducible.

No edites manualmente un archivo de `docs/` para cambiar una clase. Modifica la
fuente y recompílala. La única excepción habitual es `docs/index.html`, generado
por `.agents/scripts/publish_docs.py`.

## Antes de modificar

1. Lee `README.md` y este archivo completo.
2. Ejecuta `git status --short` y conserva todos los cambios ajenos a la tarea.
3. Localiza la fuente, sus referencias y los recursos que utiliza.
4. Limita el cambio al tema solicitado; no reformatees presentaciones completas.
5. No uses acceso de red ni agregues dependencias salvo que la tarea lo requiera.

El `.gitignore` usa una lista permitida estricta. Antes de crear un archivo,
comprueba que `git status --short --untracked-files=all` lo muestre. Los recursos
locales de muchas clases están ignorados deliberadamente; no introduzcas una nueva
referencia a un recurso que no pueda versionarse.

## Presentaciones Quarto / Reveal.js

### Narrativa y lenguaje

- Redacta el contenido docente en español claro y conserva los términos técnicos
  aceptados en inglés cuando sean útiles.
- Prefiere títulos de afirmación-evidencia: breves, directos y con una conclusión,
  no encabezados temáticos genéricos.
- Mantén los títulos por debajo de unas 45 letras siempre que sea posible para que
  no ocupen dos líneas.
- Conserva el arco pedagógico, la notación y la dificultad de las clases vecinas.

### Densidad y diseño

- Usa como máximo 11–12 líneas visibles de texto por diapositiva.
- Si hay un `callout`, `div` destacado o alerta, reduce el máximo a 7–8 líneas.
- Cada viñeta debe ser una frase corta, no un párrafo.
- Evita combinar varios subtítulos, listas y bloques de texto en una sola pantalla.
  Divide el contenido o usa columnas.
- Deja siempre una línea en blanco antes de listas; Pandoc puede tratarlas como
  texto continuo de otro modo.
- Los fragmentos siguen ocupando espacio en la misma diapositiva. Si el estado
  final no cabe, usa dos diapositivas.
- En imágenes verticales fija `height` (por ejemplo,
  `{height="350px" fig-align="center"}`) en vez de depender solo de `width`.
- Envuelve tablas grandes en un `div` con fuente reducida, normalmente entre
  `0.7em` y `0.75em`.
- Mantén el formato Reveal.js, el tema `../custom.scss`, la numeración y
  `embed-resources: true`, salvo que la tarea pida explícitamente otra cosa.

### Citas y recursos

- Añade las referencias nuevas al `references.bib` del mismo tema.
- Usa la sintaxis de citas de Pandoc y verifica que no queden claves sin resolver.
- Da atribución a imágenes, datos y afirmaciones externas.
- No confundas `references.bib` con `reference/`: el primero es bibliografía
  publicable; el segundo contiene insumos locales de consulta.
- Usa los extractos de libros solo para comprender y parafrasear. No reproduzcas
  pasajes extensos, no los redistribuyas y cita siempre la obra original.
- Trata los decks de `reference/slides/` como fuentes externas: no los modifiques ni
  copies su contenido sin atribución.
- No leas, expongas ni versionees datos de `course-admin/private/` salvo petición
  explícita del usuario y necesidad directa para la tarea.
- No edites a mano archivos bajo `quarto/clustering/assets/generated/`: modifica el
  generador correspondiente y vuelve a producirlos.
- No agregues archivos binarios grandes ni fuentes de datos nuevas sin necesidad.

## Scripts y reproducibilidad

- Usa Python 3 y rutas relativas a la raíz del repositorio en la documentación.
- No ejecutes análisis como `python -c` ni mediante heredocs. Crea o reutiliza un
  script en `.agents/scripts/` o en el directorio del tema para que el proceso sea
  auditable.
- Los scripts deben resolver rutas a partir de `__file__`, ser ejecutables desde la
  raíz y fallar con mensajes claros.
- Conserva la compatibilidad con Windows, macOS y Linux cuando el cambio lo permita.
- Si cambias una figura reproducible, versiona juntos el script, los datos fuente
  permitidos y la salida generada.

## Comandos habituales

Desde la raíz del repositorio:

```bash
# Compilar una clase a docs/<tema>.html
python3 .agents/scripts/compile_quarto.py quarto/<tema>/index.qmd

# Compilar todas las clases
python3 .agents/scripts/compile_quarto.py

# Generar las figuras reproducibles de clustering
python3 quarto/clustering/generate_figures.py --all
python3 quarto/clustering/country_narrative.py --all

# Comprobar sintaxis de los scripts versionados
python3 -m compileall -q .agents/scripts quarto/clustering

# Revisar problemas de espacios y el alcance final
git diff --check
git status --short
```

Quarto debe estar instalado para compilar. Si no está disponible, no fabriques ni
edites el HTML: informa qué validación quedó pendiente y proporciona el comando
exacto que debe ejecutarse.

## Validación proporcional al cambio

- Cambio de texto: compila la presentación afectada y revísala visualmente.
- Cambio de diseño: además prueba varias relaciones de aspecto o tamaños de ventana
  y busca desbordamientos, texto cortado y tablas ilegibles.
- Cambio de bibliografía: confirma que la compilación no emita citas sin resolver.
- Cambio de Python o datos: ejecuta el script afectado y verifica sus salidas.
- Cambio transversal: compila todas las presentaciones.
- Todo cambio: ejecuta `git diff --check` y confirma que no se incluyan archivos
  temporales, secretos, cachés ni modificaciones ajenas.

No existe una suite de pruebas automatizada general. El render de Quarto y la
inspección visual son las validaciones principales.

## Git y artefactos generados

- No reviertas cambios preexistentes del usuario.
- No uses operaciones destructivas de Git ni reescribas historia sin autorización.
- Mantén cada cambio enfocado y no mezcles limpieza incidental.
- Cuando cambie un `.qmd`, actualiza el HTML correspondiente en el mismo cambio si
  Quarto está disponible.
- Un `push` a `main` publica `docs/`; trata ese directorio como salida de producción.
- No incluyas `.quarto/`, `*_files/`, `__pycache__/`, entornos virtuales ni secretos.
- No incluyas extractos de libros, decks externos ni archivos administrativos
  privados; `.gitignore` los mantiene locales deliberadamente.

## Definición de terminado

Un cambio está terminado cuando la fuente correcta fue modificada, las referencias
y recursos son reproducibles, el artefacto compilado está actualizado cuando sea
posible, no hay desbordamientos visibles y las comprobaciones pertinentes pasan.
La entrega debe indicar de forma breve qué cambió, qué se validó y cualquier
validación pendiente.
