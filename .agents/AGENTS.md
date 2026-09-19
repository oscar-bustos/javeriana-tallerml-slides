# Reglas locales de `.agents/`

Primero aplica el [`AGENTS.md`](../AGENTS.md) de la raíz. Estas reglas adicionales
rigen únicamente los scripts y skills de este directorio.

- Mantén los scripts pequeños, reproducibles y seguros para ejecutar desde la raíz.
- Resuelve rutas desde `__file__`; no dependas del directorio actual salvo que se
  documente explícitamente.
- No uses código Python inline para análisis o transformaciones: crea un script.
- Comprueba códigos de salida de procesos externos y propaga los fallos.
- Evita rutas absolutas específicas de una máquina; si se conserva compatibilidad
  heredada, añade también una ruta portátil mediante `PATH`.
- Una skill debe describir con precisión su disparador, entradas, comandos y manejo
  de errores. No dupliques en ella reglas generales del repositorio.
- Si cambias una automatización de compilación, pruébala con una presentación antes
  de usarla sobre todo el repositorio.
