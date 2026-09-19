# Instrucciones de Copilot para este repositorio

La guía canónica está en `/AGENTS.md`; léela antes de proponer o aplicar cambios.

- Edita `quarto/<tema>/index.qmd`, nunca `docs/<tema>.html` a mano.
- Mantén el contenido docente en español y sigue las reglas de densidad de slides.
- Conserva citas en el `references.bib` local y usa sintaxis Pandoc.
- Reutiliza los scripts de `.agents/scripts/`; no escribas análisis Python inline.
- Preserva cambios preexistentes y evita refactors ajenos al objetivo.
- Compila la presentación afectada y revisa visualmente el HTML resultante.
- Incluye la fuente y el artefacto de `docs/` correspondiente en el mismo cambio.
- Si no hay Quarto, informa la validación pendiente; no fabriques el HTML.
