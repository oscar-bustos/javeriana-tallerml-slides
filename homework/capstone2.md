# Proyecto de Aplicación 2: Hugging Face

**Asignatura:** Técnicas de Aprendizaje de Máquina\
**Institución:** Pontificia Universidad Javeriana\
**Modalidad:** Trabajo en grupo (4 personas)

---

## 🎯 Objetivo

Desarrollar una solución a un problema real mediante el análisis de **texto, imágenes, audio o video** con técnicas de **aprendizaje profundo**. El equipo deberá comprender el contenido, preparar una representación adecuada para los modelos, comparar arquitecturas y poner la solución seleccionada a disposición de un usuario mediante una aplicación web.

### 🌐 Fuente de información

Seleccionar un conjunto de datos disponible en [Hugging Face Datasets](https://huggingface.co/datasets). La información que el modelo debe analizar es **contenido no estructurado**. Las etiquetas, transcripciones, identificadores y otros metadatos pueden acompañarlo para entrenar, evaluar y organizar el proyecto. Justificar el uso de fuentes complementarias y explicar su integración con el contenido principal.

---

## 🧭 Fase 0: Definición del problema

Plantear **al menos un problema** de clasificación, regresión o clusterización sobre el contenido seleccionado. Por ejemplo: clasificar la intención de un mensaje o un evento sonoro, estimar una puntuación de calidad de imagen o agrupar documentos por similitud semántica.

- **Preguntas de análisis o de negocio:** ¿Qué quiere resolver el equipo y por qué importa?
- **Entrada y salida:** ¿El modelo recibe un documento, una imagen, una grabación o un clip? ¿Devuelve una clase, un valor numérico o un grupo? Definir la unidad que se analizará y evaluará.
- **Datos y referencias de evaluación:** ¿Qué contenido se utilizará? En tareas supervisadas, ¿cómo se obtuvieron las etiquetas o los valores objetivo y qué tan confiables son? En clustering, ¿cómo se comprobará que los grupos sean útiles?
- **Propuesta de valor:** ¿A quién le servirían los resultados y cómo se usarían?
- **Justificación del enfoque:** ¿Por qué se necesita aprendizaje profundo en lugar de una regla, una búsqueda o un análisis descriptivo? Si un modelo preentrenado ya resuelve la tarea, ¿qué aporta adaptarlo o compararlo con otras arquitecturas?

### 🤖 Uso de IA en la Definición del Problema

Se recomienda usar un asistente de IA como **interlocutor crítico** antes de avanzar a la Fase 1. Presentarle el problema, el usuario objetivo, la modalidad y el conjunto de datos, y pedirle que cuestione la propuesta. Por ejemplo:

> *"Actúa como [usuario o entidad]. Queremos resolver [problema] con [texto, imágenes o audio]. ¿Qué cinco razones tendrías para no usar esta solución y qué evidencia te haría cambiar de opinión?"*

> *"Argumenta en contra de entrenar o ajustar modelos para [problema]. ¿Bastaría una regla, una búsqueda o usar directamente un modelo preentrenado? ¿Qué tendría que demostrar nuestro proyecto para justificar el enfoque?"*

> *"Con esta descripción de [dataset], su origen, anotaciones y condiciones de captura, plantea posibles diferencias frente al uso real: idioma o dominio del texto, iluminación de las imágenes, ruido o acentos del audio. Distingue lo que la descripción permite concluir de las hipótesis que debemos comprobar con muestras."*

Documentar en el cuaderno el prompt, la crítica recibida y **cómo el equipo ajustó o defendió su planteamiento** con argumentos. El equipo conserva la responsabilidad de definir el problema y comprobar las afirmaciones de la IA.

---

## 🔍 Uso Transversal de IA como Revisora Crítica

Usar la IA para **cuestionar decisiones sobre el contenido, su representación y la evaluación**. Proporcionarle evidencia concreta: muestras, pares antes/después del preprocesamiento, código, curvas de entrenamiento o errores observados. Elegir los ejemplos que correspondan a la modalidad del proyecto.

Comprobar qué entradas admite el asistente. Una transcripción permite revisar el contenido verbal, pero deja fuera el tono, los silencios y el ruido de la grabación. Si el asistente solo recibe una descripción o un gráfico, pedirle hipótesis y pruebas que el equipo pueda realizar; documentar qué información pudo examinar realmente.

| Etapa | Prompt sugerido para la IA |
|---|---|
| **EDA de texto** | *"Estos fragmentos, longitudes e idiomas corresponden a [tarea]. ¿Qué ambigüedades, negaciones, textos repetidos o diferencias de dominio conviene investigar? Propón cómo comprobar si aparecen en el resto del corpus."* |
| **Preparación de texto** | *"Compara estos textos originales con su versión limpia y tokenizada. ¿La eliminación de stopwords o el truncamiento cambia información necesaria para [tarea]? Considera el tokenizador de [modelo] y propón una comparación con y sin esa transformación."* |
| **EDA de imágenes** | *"Examina este conjunto de imágenes y sus anotaciones para [tarea]. ¿El fondo, las marcas de agua, la iluminación o el origen de captura podrían explicar el resultado en lugar del contenido que nos interesa? Sugiere comprobaciones sobre más muestras."* |
| **Preparación de imágenes** | *"Estos pares muestran las imágenes antes y después del recorte, cambio de color, filtro o aumento. ¿Se pierde el objeto o se altera la etiqueta? ¿Cómo evaluarías esa decisión manteniendo la misma partición de datos?"* |
| **EDA de audio o voz** | *"Con estas muestras o mediciones de [grabaciones], ¿qué diferencias de ruido, duración, hablante o dispositivo debemos investigar para [tarea]? Indica qué conclusiones requieren escuchar o medir el audio original."* |
| **Preparación de audio o voz** | *"Este es nuestro proceso de remuestreo, segmentación y extracción de [onda, espectrograma o MFCC]. ¿Podría eliminar pausas, entonación o frecuencias relevantes para [tarea]? Revisa su compatibilidad con [modelo] y propón cómo probarlo."* |
| **Video, si aplica** | *"Mostramos los fotogramas seleccionados y la regla de muestreo de estos clips. ¿Se conserva la acción y su orden temporal? ¿Cómo comprobarías si basta una imagen o si el modelo necesita la secuencia?"* |
| **Modelado y evaluación** | *"Estas son las arquitecturas, representaciones, particiones, métricas, tiempos y costos de [tarea], junto con las curvas si hubo entrenamiento y los resultados de una línea base sin ajuste. ¿La comparación permite elegir un modelo? Busca posibles fugas, diferencias de preentrenamiento, costos omitidos y condiciones en las que empeora. Indica qué evidencia falta para sostener cada crítica."* |
| **Aplicación web** | *"La app acepta [modalidad], aplica [preprocesamiento] y devuelve [salida] para [usuario]. Con estos resultados, propón pruebas con entradas reales que difieran de las de entrenamiento: textos largos, imágenes mal iluminadas o grabaciones ruidosas, según corresponda. ¿Cómo debería comunicar sus límites?"* |

Registrar **al menos una interacción en EDA, preparación, modelado y aplicación web**, además de la revisión de la Fase 0. Basta desarrollar la modalidad utilizada; las filas de la tabla son ejemplos. Incluir el prompt, la evidencia que recibió el asistente, la crítica y la decisión del equipo, respaldada por una inspección o un experimento. Las observaciones de la IA deben verificarse antes de presentarlas como hallazgos.

---

## 📋 Fase 1: Análisis y Preparación de Datos

Documentar esta fase en un cuaderno de **Google Colab**. Desarrollar los apartados de las modalidades que use el proyecto y justificar las decisiones según la tarea y el modelo elegido.

### 1. Exploración de datos no estructurados

- **Para cualquier modalidad:** inventariar origen, cantidad de ejemplos, formatos y condiciones de recolección. Revisar contenido vacío o dañado, duplicados exactos y casi duplicados. Mostrar muestras representativas, ambiguas y difíciles, y explicar qué implican para el problema.
- **Anotaciones, cuando existan:** comprobar su significado y revisar posibles errores. En clasificación, analizar el balance de clases; en regresión, la distribución de los valores objetivo. En clustering, inspeccionar la diversidad del contenido sin suponer que existen clases conocidas.
- **Texto:** examinar idiomas, longitud en palabras y en tokens del modelo, términos frecuentes, negaciones y diferencias entre fuentes o dominios. Identificar documentos que excedan la longitud admitida.
- **Imágenes:** inspeccionar resolución, proporción, canales, desenfoque, iluminación, fondos y distribución de colores. Mostrar ejemplos de distintas fuentes y clases, si las hay.
- **Audio o voz:** escuchar muestras y visualizar ondas o espectrogramas; analizar duración, frecuencia de muestreo, canales, saturación, silencios y ruido. Revisar diversidad de hablantes, acentos, dispositivos o ambientes cuando esa información esté disponible.
- **Video, si aplica:** examinar duración, tasa de fotogramas, cambios de escena y sincronización con el audio. Comprobar si la información necesaria depende del movimiento o del orden de los eventos.

Las estadísticas deben describir propiedades relevantes del contenido, como longitud, duración o resolución. Usar correlaciones o tablas de contingencia solo cuando respondan una pregunta concreta sobre esas propiedades, las anotaciones o las condiciones de captura.

### 2. Preparación común

- Definir la unidad de partición según el uso esperado. Mantener juntas las copias de un documento, variantes de una imagen y segmentos de una misma grabación o video. Si se busca generalizar a personas nuevas, separar también por persona; justificar la decisión según la tarea.
- En tareas supervisadas, separar entrenamiento, validación y prueba **antes de ajustar** vocabularios, estadísticas u otras transformaciones aprendidas. Ajustarlas con entrenamiento y elegir las decisiones con validación. En clustering, definir un protocolo de estabilidad y validación de los grupos; indicar si se espera asignar nuevas muestras.
- Registrar las transformaciones y mostrar ejemplos antes/después. Generar aumentos o contenido sintético solo para entrenamiento, conservar su procedencia y comprobar la validez de sus anotaciones. Las versiones derivadas deben permanecer en la misma partición que su original.
- Usar el tokenizador o procesador asociado al modelo preentrenado y evitar normalizar o redimensionar dos veces. Consultar sus requisitos de entrada en la [guía de preprocesamiento de Hugging Face](https://huggingface.co/docs/transformers/v4.44.0/en/preprocessing).

### 3. Preparación según la modalidad

**Texto**

- Justificar la limpieza de HTML, caracteres extraños, mayúsculas, puntuación, tildes o emojis según la tarea. Mostrar si el cambio conserva el significado; una negación puede determinar la clase de sentimiento.
- Indicar si se eliminan *stopwords*, con qué lista y para qué idioma. En representaciones por conteos puede evaluarse esa opción; con modelos preentrenados, partir de su preprocesamiento esperado y conservar las palabras salvo que la validación justifique un cambio. Documentar también la lematización o el uso de diccionarios de normalización, si se aplican.
- Explicar cómo se tokeniza. Usar el tokenizador y vocabulario asociados al modelo preentrenado; si se construye uno propio, aprenderlo solo con entrenamiento. Documentar longitud máxima, truncamiento, división de documentos y relleno (*padding*), y medir cuántos textos pierden contenido.

**Imágenes**

- Indicar la resolución final, el método de redimensionamiento y cómo se maneja la proporción: recorte, relleno o deformación justificada. Comprobar si se conservan los detalles relevantes.
- Justificar el uso de color, escala de grises o binarización, y especificar el rango y la normalización de los píxeles. Adaptar el número de canales a la entrada del modelo; una conversión a gris puede eliminar información útil de color.
- Si se usan máscaras, filtros o segmentación como preprocesamiento, mostrar su efecto y explicar cómo se obtienen también para imágenes nuevas, sin utilizar la etiqueta que se intenta predecir.
- Distinguir aumentos de imágenes existentes de imágenes generadas por un modelo. Documentar operaciones o generador, revisar calidad y anotaciones, y comprobar que recortes, rotaciones o cambios de color preserven el objetivo de la tarea.

**Audio o voz**

- Definir frecuencia de muestreo, conversión a mono o conservación de canales, duración de segmentos y manejo de longitudes variables. Si cambia la frecuencia de muestreo, remuestrear la señal; cambiar solo el valor declarado altera su interpretación.
- Justificar la normalización de amplitud, reducción de ruido y eliminación de silencios: las pausas, la intensidad o el ambiente pueden ser señales relevantes. Escuchar ejemplos antes y después.
- Elegir una representación compatible con el modelo: **onda temporal**, **espectro de frecuencias**, **espectrograma tiempo-frecuencia** o **espectrograma Mel**. Si se extraen [MFCC](https://librosa.org/doc/main/api/generated/librosa.feature.mfcc.html), describirlos como coeficientes cepstrales derivados del espectrograma Mel logarítmico. Reportar ventana, salto, bandas o coeficientes según corresponda y qué información se descarta.
- Si se trabaja con voz, justificar si interesa el contenido lingüístico o también las características acústicas. Si se utiliza una transcripción automática, analizar sus errores y la pérdida de información como entonación o pausas.
- Para aumentos o audio sintético, documentar el método y comprobar que ruido, cambios de velocidad o de tono preserven el objetivo y la anotación. Aplicarlos solo al entrenamiento.

**Video, si aplica**

- Describir duración de clips, selección y frecuencia de fotogramas, tratamiento del audio y sincronización. Justificar si se analizan cuadros aislados o una secuencia temporal.
- Mantener coherencia entre fotogramas al aplicar aumentos y evitar que clips del mismo video queden en entrenamiento y prueba.

Para cualquier modalidad, explicar cómo se obtiene la representación numérica final: tokens, tensores, descriptores o vectores aprendidos (*embeddings*). Justificar las características adicionales que se construyan.

---

## ⚙️ Fase 2: Modelado y Evaluación

### 1. Comparación de arquitecturas

Para cada problema planteado, implementar, evaluar y comparar **como mínimo tres arquitecturas adecuadas para la misma tarea**. Seleccionarlas entre los temas de la segunda parte del curso:

- Redes con capas densas sobre una representación de tamaño fijo.
- Redes convolucionales para imágenes, secuencias o representaciones de audio, según la tarea.
- Redes recurrentes (RNN, LSTM o GRU) para información secuencial.
- **Opciones avanzadas:** Transformers y autoencoders.

Explicar qué recibe cada arquitectura y cómo produce la salida requerida. En clustering, indicar cómo se obtienen los *embeddings* y qué algoritmo los agrupa. Cambiar solo la tasa de aprendizaje o el número de épocas cuenta como ajuste de una arquitectura.

Para **cualquier modalidad utilizada**, se recomienda partir de **modelos preentrenados** adecuados al contenido y al dominio, como base de aprendizaje y comparación. Pueden usarse como extractores congelados de características o ajustarse mediante *fine-tuning*. El *transfer learning* es una estrategia aplicable a distintas arquitecturas.

Reportar el identificador y la versión de los pesos, sus datos de preentrenamiento conocidos, el procesador asociado y qué componentes se entrenan o congelan. Comparar sobre las mismas muestras de evaluación, con el preprocesamiento requerido por cada modelo, y declarar cualquier solapamiento conocido con los datos de preentrenamiento.

### 2. Entrenamiento, optimización y métricas

- Describir la estrategia de entrenamiento y validación, las semillas y los recursos usados. Si hay entrenamiento, mostrar curvas de pérdida y métricas para examinar sobreajuste.
- Reportar los hiperparámetros relevantes: tasa de aprendizaje, optimizador, tamaño de lote, épocas, regularización y capas entrenables. Explicar cómo se eligieron; una búsqueda acotada sobre validación puede ser suficiente para el presupuesto disponible.
- En aprendizaje supervisado, reservar el conjunto de prueba para la evaluación final, después de elegir el preprocesamiento, el modelo y sus parámetros.

Presentar una **tabla comparativa de rendimiento**. Las [métricas se eligen según la salida de la tarea](https://scikit-learn.org/stable/modules/model_evaluation.html), aunque la entrada sea texto, imagen o audio:

- **Clasificación:** reportar *Accuracy*, *Precision*, *Recall* y *F1*, con resultados por clase y el tipo de promedio usado. Distinguir entre clasificación binaria, multiclase o multietiqueta. Añadir matrices de confusión adecuadas al caso; incluir ROC-AUC cuando existan puntuaciones por clase y explicar su cálculo. Con clases desbalanceadas, complementar con curvas precisión-recall.
- **Regresión:** reportar *MSE*, *RMSE*, *MAE* y *R²* para la variable numérica definida. Expresar los errores en relación con sus unidades y mostrar ejemplos de las mayores discrepancias entre predicción y referencia.
- **Clusterización:** justificar representación, distancia y algoritmo. Usar silueta o Davies-Bouldin cuando sean compatibles con esa geometría; el codo de inercia aplica a métodos como K-Means. Interpretar los índices dentro de cada espacio de representación y acompañarlos con estabilidad y ejemplos del contenido de los grupos. Consultar las [condiciones de uso de las métricas de clustering](https://scikit-learn.org/stable/modules/clustering.html#clustering-performance-evaluation).

### 3. Análisis de errores e iteración

- Mostrar resultados correctos y fallidos sobre textos, imágenes o fragmentos de audio/video originales. En clustering, mostrar ejemplos representativos y ambiguos de cada grupo.
- Analizar cuándo empeora la solución: textos largos o de otro dominio, imágenes con poca luz, grabaciones ruidosas u otras condiciones pertinentes. Las diferencias entre grupos deben sustentarse con suficientes muestras.
- Documentar una decisión de mejora a partir de la validación y comprobar su efecto, por ejemplo, conservar negaciones, cambiar un recorte o revisar la segmentación de audio. Mantener fijo el conjunto de prueba.
- Justificar la selección final con desempeño, utilidad de las salidas, tiempo de inferencia y memoria necesaria. Explicar las limitaciones observadas.

### 4. Recursos de cómputo y comparación con una línea base

Incluir una **ficha técnica reproducible** del experimento y comparar la solución seleccionada con una opción que se use sin ajuste adicional para la tarea:

- **Máquina utilizada:** indicar si el entrenamiento se hizo en un equipo local o en un servicio en la nube, y registrar CPU, GPU o TPU (modelo y memoria disponible), RAM y entorno de ejecución. Indicar la cantidad de ejemplos, épocas, tamaño de lote y componentes entrenables para dar contexto a los tiempos.
- **Tiempo de desarrollo del modelo:** medir el tiempo transcurrido de entrenamiento por ejecución y el tiempo total de las pruebas de ajuste. Informar por separado el tiempo de preprocesamiento o extracción de *embeddings* cuando sea significativo. Si se usa un extractor congelado, distinguir su costo del entrenamiento de la capa final.
- **Línea base sin ajuste:** elegir una opción que acepte la misma modalidad y produzca una salida comparable. Puede ser un modelo preentrenado usado directamente o, si la tarea lo permite, un LLM con un prompt *one-shot*. En este último caso, mostrar el prompt y su único ejemplo, tomado de entrenamiento; el LLM ya fue preentrenado y *one-shot* significa que no se ajustan sus pesos para este proyecto.
- **Comparación justa:** evaluar ambas soluciones con las mismas entradas de prueba y las métricas pertinentes. Registrar la latencia por solicitud, el tamaño de entrada y los recursos de inferencia. Para modelos locales, indicar la máquina de medición; para una API, registrar proveedor, versión del modelo, consumo por solicitud y tarifa con su fecha, aunque no se conozca el hardware del proveedor.
- **Decisión técnica:** explicar en qué condiciones conviene cada opción. Para un volumen de uso declarado, separar la inversión inicial de entrenamiento del costo recurrente por solicitud y calcular el costo total estimado de cada solución. La elección puede justificarse por calidad, rapidez, privacidad o costo operativo. Si la línea base resulta preferible, reportarlo y explicar la conclusión.

Mantener la comparación exigida de tres arquitecturas además de esta línea base. La tabla de resultados debe permitir ver tanto la calidad como el tiempo y el costo de cada opción.

---

## 🌐 Fase 3: Aplicación Web

Desarrollar una aplicación web **disponible en la nube** que resuelva uno de los problemas analizados:

- Integrar el preprocesamiento de evaluación, el modelo seleccionado y la interpretación de sus salidas. Comprobar que un mismo ejemplo produzca resultados consistentes en el cuaderno y en la app.
- Proporcionar una entrada adecuada: campo de texto, carga de imagen, carga o grabación de audio, o carga de video. Informar los idiomas, formatos, tamaños o duraciones admitidos.
- Mostrar la entrada y un resultado comprensible: clase, valor con sus unidades o agrupación con ejemplos representativos. Para clustering, explicar si la app explora una colección o permite asignar contenido nuevo y cómo lo hace.
- Probar ejemplos habituales y difíciles, incluidos archivos vacíos o no admitidos. Comunicar al usuario las limitaciones observadas y cómo interpretar la salida en el contexto del problema.

---

## 📦 Entregables

La evaluación final consta de un **informe técnico** y una **presentación en vivo**. La aplicación web también debe estar disponible para su demostración.

### 1. Informe Técnico (Cuaderno de Google Colab)

El cuaderno deberá estar claramente estructurado e incluir, como mínimo:

- **Elevator Pitch:**
  - Preguntas de negocio o de análisis planteadas.
  - Importancia de resolverlas y argumentos clave para presentar el proyecto.
  - Justificación del enfoque y síntesis de la revisión crítica de la definición del problema.
- **Descripción y Justificación del Corpus:**
  - Fuente, versión, cantidad de ejemplos, modalidad, formatos y unidad de análisis.
  - Tabla de los campos disponibles: nombre, tipo y función como contenido, anotación, identificador o metadato.
  - Significado de las anotaciones y los metadatos que acompañan al contenido, su origen y su función en el proyecto.
  - Justificación de las fuentes complementarias y forma de vincularlas con cada documento, imagen, grabación o clip.
- **Análisis Exploratorio de Datos (EDA):**
  - Muestras de contenido, visualizaciones o audios reproducibles, según la modalidad.
  - Calidad, diversidad, anotaciones y hallazgos que afecten el planteamiento o el modelado.
- **Preparación y Representación de los Datos:**
  - Transformaciones específicas de la modalidad, parámetros y ejemplos antes/después.
  - Partición de datos o protocolo de validación de clustering, prevención de fugas y aumentos sintéticos, si se utilizan.
  - Representación que recibe cada arquitectura y su relación con el procesador del modelo preentrenado.
- **Modelado, Evaluación e Interpretación:**
  - Arquitecturas, pesos preentrenados y estrategia de entrenamiento o extracción de características.
  - Hiperparámetros, procedimiento de selección y tabla comparativa de métricas adecuadas a la tarea.
  - Ejemplos de resultados, análisis de errores, evidencia de iteración y justificación de la solución seleccionada.
  - Limitaciones, condiciones de uso y posibles mejoras futuras.
- **Recursos y comparación con una línea base:** ficha de la máquina, tiempos de entrenamiento y preparación, prompt o configuración de la línea base, resultados sobre las mismas muestras y estimación de latencia y costo para un volumen de uso declarado.
- **Registro de revisión con IA:** prompt, evidencia accesible al asistente, crítica y comprobación realizada por el equipo en la definición del problema, EDA, preparación, modelado y aplicación web.

### 2. Aplicación Web

- Enlace a la aplicación desplegada y demostración de la interacción con el modelo seleccionado.

---

## 🎤 Presentación Final (20 minutos)

La presentación de cada grupo se estructurará así:

1. **5 minutos - Elevator Pitch:** Presentación orientada a explicar el valor del proyecto ante una entidad que podría financiarlo.
2. **10 minutos - Presentación Técnica:** Proceso, análisis, comparación con la línea base, recursos y tiempos utilizados, y resultados que sustentan la solución.
3. **5 minutos - Preguntas:** Sesión de preguntas del público y del profesor.
