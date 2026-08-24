# Proyecto de Aplicación 1: Datos Abiertos

**Asignatura:** Técnicas de Aprendizaje de Máquina  
**Institución:** Pontificia Universidad Javeriana  
**Modalidad:** Trabajo en grupo (4 personas)  

---

## 🎯 Objetivo

Desarrollar una solución a un **problema real de interés público** utilizando datos abiertos colombianos. El Machine Learning es la herramienta, no el fin: el proyecto se evalúa por la capacidad del equipo de entender un problema, investigar su contexto, proponer una solución fundamentada y comunicar sus hallazgos de forma clara.

### 🌐 Fuentes de Información
Se deberá consumir información disponible en el portal de [Datos Abiertos Colombia](https://datos.gov.co/). Los equipos pueden complementar con fuentes externas si lo justifican adecuadamente.

---

## 🧭 Fase 0: Definición del Problema Real

Antes de explorar datos o entrenar modelos, el equipo debe definir con claridad el problema que busca resolver:

- **Problema concreto:** ¿Qué problema público, social o económico están abordando? Describirlo en términos que un no-técnico pueda entender.
- **Stakeholder objetivo:** Identificar un usuario o entidad beneficiaria concreta (ej. un ministerio, una alcaldía, una ONG, una comunidad). ¿Quién usaría esta solución y por qué?
- **Costo de la inacción:** ¿Cuál es el impacto de *no resolver* este problema? ¿Qué se pierde?
- **Hipótesis inicial:** Antes de tocar los datos, ¿qué esperan encontrar? ¿Qué preguntas concretas buscan responder? Formular al menos 3 hipótesis que guíen la exploración.
- **Justificación de ML:** Argumentar explícitamente *por qué* este problema requiere técnicas de Machine Learning y no se resuelve mejor con un análisis estadístico tradicional, un dashboard descriptivo o una regla de negocio simple. ¿Qué valor agregado aporta un modelo predictivo o clasificatorio?

### 🤖 Uso de IA en la Definición del Problema

Se recomienda utilizar un asistente de IA (ChatGPT, Gemini, Copilot, Claude, etc.) como **sparring partner** para afinar el planteamiento. Antes de avanzar a la Fase 1, someter la definición del problema a un *stress-test* con la IA usando prompts como:

> *"Actúa como un director de datos de [entidad stakeholder]. Te presento este proyecto: [descripción]. Dame 5 razones por las que NO financiarías este proyecto y qué le falta para convencerte."*

> *"¿Este problema realmente necesita Machine Learning o se puede resolver con un análisis descriptivo y un buen dashboard? Argumenta en contra del uso de ML."*

> *"¿Qué sesgos podrían tener los datos de datos.gov.co para este problema? ¿Qué datos faltan y dónde los conseguiría?"*

Documentar en el cuaderno: el prompt utilizado, la respuesta de la IA y **cómo el equipo ajustó su planteamiento** a partir de esa retroalimentación. La IA no define el problema — el equipo lo defiende.

---

## 🔍 Uso Transversal de IA como Revisora Crítica

A lo largo de todo el proyecto, se espera que los equipos utilicen la IA como **revisora ácida** de sus decisiones intermedias. El objetivo no es que la IA haga el trabajo, sino que **cuestione la utilidad real** de cada paso. Ejemplos de uso por fase:

| Fase | Prompt sugerido para la IA |
|---|---|
| **EDA** | *"Estoy analizando [dataset]. Estas son mis 5 visualizaciones principales: [lista]. ¿Alguna es redundante? ¿Cuál no aporta nada al problema que intento resolver?"* |
| **Preparación** | *"Decidí imputar los valores nulos con la mediana y eliminar outliers con IQR. ¿Es la mejor estrategia para mi problema o estoy perdiendo información valiosa?"* |
| **Modelado** | *"Entrené 3 modelos y el Random Forest da el mejor F1-Score. ¿Eso es suficiente para elegirlo? ¿Qué otras consideraciones debería tener (interpretabilidad, costo computacional, fairness)?"* |
| **App Web** | *"Mi app solo muestra la predicción. ¿Qué necesitaría un usuario real de [stakeholder] para confiar en este resultado y tomar una decisión?"* |

En cada fase del cuaderno, incluir al menos **una interacción documentada con la IA** donde se evidencie: el prompt, la crítica recibida y la acción tomada por el equipo (aceptar, refutar con argumentos o ajustar el enfoque).

---

## 📋 Fase 1: Análisis y Preparación de Datos

Se espera que el equipo aborde las siguientes actividades y las deje plasmadas y documentadas en un cuaderno de **Google Colab**:

### 1. Exploración de Datos (EDA con Narrativa)
- Realizar una exploración exhaustiva de los datos: medidas de dispersión, tendencia central, sesgos en la distribución, tablas de contingencia y correlaciones.
- **Data Storytelling:** Cada visualización debe responder a una pregunta de negocio concreta, no solo describir distribuciones. Narrar el EDA como una historia: *"Descubrimos que X está correlacionado con Y, lo cual sugiere que..."* en lugar de *"La correlación entre X e Y es 0.73"*.
- **Hallazgos inesperados:** Incluir un apartado explícito de descubrimientos sorpresivos, sesgos detectados o limitaciones encontradas en los datos.

### 2. Preparación de Datos e Ingeniería de Características
- Adecuar y limpiar los datos para el modelado, **justificando cada paso** del preprocesamiento.
- Descripción de transformaciones realizadas (normalización, estandarización, codificación de variables, etc.).
- Proceso de limpieza (imputación de valores faltantes, manejo de outliers).
- Identificación y creación de nuevas variables (ingeniería de características), explicando su relevancia para el problema definido.

---

## ⚙️ Fase 2: Modelado y Evaluación

### 1. Definición y Modelado de Problemas
- A partir de los datos y el problema definido en la Fase 0, plantear y resolver **al menos dos problemas** (clasificación, clusterización o regresión).
- Para cada problema, implementar, evaluar y comparar **como mínimo tres algoritmos** de Machine Learning.

### 2. Selección de Algoritmos
Los algoritmos deben ser seleccionados del listado de temas cubiertos en la Parte 1 del curso:

- **Modelos Lineales:** Regresión lineal, Regresión Logística.
- **Máquinas de Soporte Vectorial:** SVM.
- **Árboles de Decisión:** Decision Trees.
- **Modelos de Ensamble:** Gradient Boosted Trees, Random Forest, Voting, Stacking.
- **Reducción de Dimensionalidad:** PCA.
- **Algoritmos de Clustering:** K-Means, DBSCAN.

### 3. Optimización y Métricas
- Reportar los hiperparámetros finales y el método de optimización empleado (ej. *Grid Search*, *Randomized Search*).
- Presentar una **tabla comparativa de rendimiento** con métricas según el tipo de problema:
  - **Clasificación:** *Accuracy*, *Precision*, *Recall*, *F1-Score*, *AUC*. Acompañar con matrices de confusión y curvas ROC.
  - **Regresión:** *MSE*, *RMSE*, *MAE*, *R²*.
  - **Clusterización:** Método del Codo (*Elbow Method*), Coeficiente de Silueta (*Silhouette Score*), Índice de Davies-Bouldin.

### 4. Iteración y Mejora
- Tras el primer ciclo de modelado, documentar explícitamente:
  - ¿Qué cambiarían en el preprocesamiento a la luz de los primeros resultados?
  - ¿Agregaron o eliminaron features después de ver los resultados iniciales?
  - ¿El EDA inicial les dio pistas que luego validaron o descartaron con el modelo?
- El ML es un proceso cíclico, no un pipeline lineal. Se valora evidencia de iteración.

---

## 🌐 Fase 3: Aplicación Web

Desarrollar una aplicación web desplegada en la nube que resuelva uno de los problemas analizados, diseñada para un **usuario real** (no para un data scientist):

- **Contexto para el usuario:** La app debe explicar *qué hace*, *por qué es útil* y *cómo interpretar los resultados* en lenguaje accesible.
- **Acciones derivadas:** No solo mostrar una predicción, sino sugerir *qué hacer con ella* (ej: "El modelo predice riesgo alto → Acciones recomendadas: ...").
- **Transparencia del modelo:** Incluir algún elemento de explicabilidad (ej: "Las variables más importantes para esta predicción fueron...").

### 🚀 Plataformas Recomendadas de Despliegue

Se recomienda utilizar alguna de las siguientes plataformas, que son gratuitas, fáciles de mantener y están diseñadas para proyectos de ML:

| Plataforma | Ventajas | Enlace |
|---|---|---|
| **Hugging Face Spaces** | Integración nativa con modelos de ML, soporte para Gradio y Streamlit, hosting gratuito, comunidad activa de IA. | [huggingface.co/spaces](https://huggingface.co/spaces) |
| **Streamlit Community Cloud** | Despliegue directo desde un repositorio de GitHub, ideal para prototipos rápidos con Python, widgets interactivos sin frontend. | [streamlit.io/cloud](https://streamlit.io/cloud) |

Ambas plataformas permiten desplegar una app funcional en minutos con solo un archivo `app.py` y un `requirements.txt`, sin necesidad de configurar servidores ni infraestructura.

---

## ⚠️ Fase 4: Ética, Sesgos y Limitaciones

Incluir una reflexión obligatoria sobre:

- **Sesgos identificados en los datos:** ¿Están ciertos departamentos, poblaciones o periodos sobre/sub-representados? ¿Los datos reflejan la realidad o solo lo que se registra?
- **Implicaciones éticas:** Si el modelo se desplegara en producción, ¿podría perjudicar a algún grupo? ¿Las predicciones son justas?
- **Limitaciones reconocidas:** ¿Qué *no puede* hacer su modelo? ¿Bajo qué condiciones fallaría? ¿Qué datos adicionales mejorarían la solución?

---

## 📦 Entregables

La evaluación final consta de un **informe técnico** y una **presentación en vivo**.

### 1. Informe Técnico (Cuaderno de Google Colab)
El cuaderno deberá estar claramente estructurado, siguiendo como mínimo las secciones:

- **Elevator Pitch:**
  - Problema real identificado y stakeholder objetivo.
  - Preguntas de negocio o de análisis planteadas.
  - Justificación de la importancia de resolver dichas preguntas.
  - Justificación de por qué ML es la herramienta adecuada.

- **Diccionario y Justificación de Datos:**
  - Tabla descriptiva para cada campo del conjunto de datos principal (nombre, tipo de dato, descripción de negocio).
  - Justificación para la inclusión de datos complementarios.
  - Estrategia de integración de los datos adicionales con el conjunto original.

- **Análisis Exploratorio de Datos (EDA con narrativa):**
  - Inventario descriptivo de los conjuntos de datos.
  - Análisis estadístico (tendencia central, dispersión, sesgo, correlaciones, contingencia).
  - Narrativa de hallazgos vinculada a las preguntas de negocio.
  - Hallazgos inesperados y sesgos detectados.

- **Preparación de Datos e Ingeniería de Características.**

- **Modelado, Evaluación e Interpretación:**
  - Proceso de entrenamiento y validación.
  - Tabla comparativa de rendimiento con métricas.
  - Evidencia de iteración y mejora.
  - Análisis de resultados y justificación del modelo seleccionado.

- **Ética, Sesgos y Limitaciones.**

- **Conclusiones y trabajo futuro.**

### 2. Aplicación Web
- Prototipo funcional desplegado en la nube con los requisitos de la Fase 3.

---

## 🎤 Presentación Final (20 minutos)

La presentación de cada grupo se estructurará de la siguiente manera:

1. **5 minutos - Elevator Pitch:** Presentación orientada a "vender" el proyecto a una entidad para conseguir financiación. Enfocarse en el problema y su impacto, no en los algoritmos.
2. **10 minutos - Presentación Técnica:** Exposición del proceso, análisis, visualizaciones y material técnico que soporte los resultados.
3. **5 minutos - Preguntas:** Sesión de preguntas por parte del público, los revisores y el profesor.

---

## 👥 Dinámica de Revisión por Pares (Preguntas y Debate)

Para fomentar el análisis crítico durante las presentaciones finales, se implementará un sistema de **revisores cruzados**:

- **Asignación de Roles:** Por cada grupo que expone (ej. Grupo 1), habrá un grupo designado como **Revisor** (ej. Grupo 2).
- **Misión del Grupo Revisor:** Evaluar críticamente la exposición, prestando especial atención a la claridad del análisis técnico, la preparación de datos, la fundamentación de los modelos y la aplicación web desarrollada.
- **Sesión de Preguntas:** Al finalizar la presentación, el grupo revisor liderará la sesión de dudas y deberá realizar **al menos dos (2) preguntas técnicas o analíticas** al grupo expositor.
- **Impacto de la Dinámica:** Esta interacción evaluará tanto la capacidad del grupo expositor para defender y argumentar su proyecto, como la pertinencia y profundidad crítica de las preguntas formuladas por el grupo revisor.

---

## ⚖️ Criterios de Evaluación

| Criterio | Peso |
|---|---|
| **Definición del problema y relevancia** (Fase 0) | 20% |
| **Calidad del EDA y narrativa de datos** (Fase 1) | 15% |
| **Preparación de datos e ingeniería de features** (Fase 1) | 15% |
| **Modelado, comparación, iteración y justificación** (Fase 2) | 20% |
| **Aplicación web y usabilidad** (Fase 3) | 10% |
| **Ética, limitaciones y reflexión crítica** (Fase 4) | 10% |
| **Presentación, defensa y revisión por pares** | 10% |