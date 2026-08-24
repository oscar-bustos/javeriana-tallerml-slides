# Tarea 0: Análisis Exploratorio de Datos (EDA) Asistido por IA en Google Colab

**Asignatura:** Técnicas de Aprendizaje de Máquina  
**Institución:** Pontificia Universidad Javeriana  
**Sesión:** Introducción a la IA y Entornos de Desarrollo  

---

## 🎯 Objetivo

El objetivo de esta tarea inicial es familiarizarse con el entorno de **Google Colab** y su integración con asistentes de Inteligencia Artificial (Google Gemini / Colab AI), ejecutando un *prompt* de generación de código para realizar un Análisis Exploratorio de Datos (EDA) automático sobre un conjunto de datos clásico.

---

## 📋 Descripción de la Actividad

Basado en lo presentado en la sesión introductoria (`intro_ia`), deberá utilizar el asistente de IA integrado en Google Colab para generar y ejecutar el código necesario para realizar un EDA mediante la librería `ydata-profiling`.

### Pasos a seguir:

1. **Acceso a Google Colab:**
   - Ingrese a [Google Colab](https://colab.research.google.com/) con su cuenta institucional o personal de Google.
   - Cree un **Nuevo cuaderno** (*New notebook*).

2. **Identificación del Grupo:**
   - En la primera celda del cuaderno, cree una **celda de texto (Markdown)** e incluya los **nombres completos de los 2 integrantes** que entregan el taller.

3. **Generación mediante Prompt con IA:**
   - Active el chat o la función de generación de código con IA dentro de Colab.
   - Ingrese el siguiente **prompt exacto** (o variante adecuada):

   > *"Haz un analisis exploratorio de datos del archivo de github datasciencedojo titanic.csv usando la librería ydata-profiling. Instala la ultima version disponible de la libreria."*

4. **Ejecución y Verificación:**
   - Asegúrese de que el código generado contenga:
     - Instalación de la última versión de `ydata-profiling` (`pip install -U ydata-profiling`).
     - Carga del dataset Titanic desde el repositorio de GitHub (`https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv`).
     - Generación y visualización del reporte exploratorio completo (`ProfileReport`).
   - Ejecute todas las celdas del cuaderno y verifique que el reporte interactivo de EDA se renderice correctamente en la salida de Colab.

5. **Guardado y Compartición del Cuaderno:**
   - ⚠️ **¡Importante! (Ejecución y Guardado):** Asegúrese de haber ejecutado **todas las celdas** y que los resultados y gráficos del EDA sean visibles en pantalla. **Únicamente después de haber ejecutado todo el cuaderno**, proceda a guardarlo (`Archivo -> Guardar` o `Ctrl+S`). Esto garantiza que el progreso y las salidas generadas queden grabadas en el archivo.
   - Renombre el cuaderno con el formato: `Tarea0_EDA_[Apellido1]_[Apellido2]`.
   - Haga clic en el botón **Compartir** (*Share*) en la esquina superior derecha de Google Colab.
   - Cambie los permisos de acceso a **"Cualquier persona con el enlace"** (*Anyone with the link*) en modo Lector (*Viewer*).
   - Copie el enlace público de su cuaderno.

6. **Entrega:**
   - Ingrese al cuestionario de la tarea y pegue el enlace público del cuaderno de Colab ya compartido.
