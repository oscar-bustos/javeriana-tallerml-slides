# Tarea 9: Redes Neuronales Convolucionales (CNN)

**Asignatura:** Técnicas de Aprendizaje de Máquina<br>
**Institución:** Pontificia Universidad Javeriana<br>
**Tema:** Clasificación de imágenes con CNN y modelos clásicos<br>
**Calificación:** automática mediante el quiz de Brightspace

---

## 🎯 Objetivo

Comparar modelos clásicos y CNN sobre Fashion-MNIST, analizar qué cambia al utilizar uno, dos o tres bloques convolucionales y justificar las conclusiones con métricas, curvas de aprendizaje y costo computacional. Una red más profunda no tiene que obtener mejores resultados.

---

## 📋 Instrucciones Generales para la Entrega

Desarrolle y entregue un único cuaderno de Google Colab que contenga el código, los resultados y el análisis de las cinco secciones de esta guía.

1. **Identificación:** incluya los nombres completos de los integrantes en la primera celda Markdown.
2. **Estructura:** utilice los mismos títulos de las cinco secciones y acompañe las tablas y gráficas con una interpretación escrita.
3. **Reproducibilidad:** use `random_state=42` en los muestreos, particiones y modelos de scikit-learn que acepten ese argumento. Antes de construir cada CNN, ejecute `tf.keras.backend.clear_session()` y `tf.keras.utils.set_random_seed(42)`. Registre las versiones de Python, scikit-learn y TensorFlow, y el dispositivo utilizado (CPU o GPU). Una semilla no garantiza resultados idénticos entre dispositivos.
4. **Evidencia:** ejecute todas las celdas y deje visibles sus salidas. Cada gráfica debe tener título, ejes y leyenda cuando corresponda. El cuaderno debe poder ejecutarse en orden desde una sesión nueva.
5. **Guardado:** use el nombre `Tarea9_CNN_[Apellido1]_[Apellido2]`.
6. **Acceso y entrega:** comparta el Colab como **“Cualquier persona con el enlace”** en modo Lector y entregue el enlace en el quiz de Brightspace. Incluya el análisis de los resultados en el mismo cuaderno.
7. **Calificación:** responda el quiz de Brightspace después de desarrollar la actividad. La calificación se obtiene automáticamente a partir de las respuestas al quiz.

### Recursos de apoyo

- [Fashion-MNIST: descripción y carga con Keras](https://keras.io/api/datasets/fashion_mnist/).
- [Presentación del curso sobre CNN](https://oscar-bustos.github.io/javeriana-tallerml/slides/cnn.html).
- [Cuaderno de modelos clásicos del taller original](https://colab.research.google.com/drive/1TVnEgPdRth-PCfNszxev96rNl8WQKE8W?usp=sharing).
- [Cuaderno de CNN del taller original](https://colab.research.google.com/drive/1QpTnWj3LQwNu1BuZVzxL-ouvGaVbYQy5?usp=sharing).
- [Documentación de Dropout](https://keras.io/api/layers/regularization_layers/dropout/).

Los dos cuadernos son apoyos opcionales. Si los utiliza, incorpore el código necesario en su entrega, cite la fuente y adáptelo al protocolo de esta guía. No copie métricas obtenidas con otras particiones.

---

## 🔎 Sección 1: Datos y Protocolo Común

1. Cargue los datos con `tf.keras.datasets.fashion_mnist.load_data()`. El conjunto contiene imágenes de 28 × 28 píxeles en escala de grises y diez clases de prendas. Conserve las 10 000 imágenes de prueba oficiales para la evaluación final.
2. Para acotar el costo computacional, seleccione una muestra estratificada de **12 000 imágenes del conjunto de entrenamiento oficial**, usando `train_test_split` con `train_size=12000`, `stratify=y` y `random_state=42`. Descarte el resto para esta actividad.
3. Divida esa muestra en **80% entrenamiento y 20% validación**, estratificando por clase y usando `random_state=42`. Obtendrá 9600 imágenes de entrenamiento y 2400 de validación. Genere las particiones una sola vez y reutilice exactamente las mismas imágenes y etiquetas en todos los modelos.
4. Reporte tamaños, distribución de clases, tipo de dato y rango de intensidades. Muestre una imagen de entrenamiento por clase con su etiqueta.
5. Convierta las imágenes a `float32` y divida las intensidades por `255.0` en las tres particiones. Esta transformación usa una constante conocida; si añade una transformación que aprende estadísticas, ajústela únicamente con entrenamiento.
6. Prepare dos representaciones a partir de esas mismas particiones:
   - Modelos clásicos: `X.reshape(len(X), -1)`, con forma `(N, 784)`.
   - CNN: `X[..., tf.newaxis]`, con forma `(N, 28, 28, 1)`.
7. Explique qué significa cada eje y verifique que cambiar la forma no altera los valores de los píxeles ni el orden de las etiquetas.

**Regla de evaluación:** use entrenamiento para ajustar pesos y validación para comparar modelos. No consulte métricas de prueba hasta la sección 4. En esta guía, *accuracy* significa **exactitud**; no es la métrica *precision*. Calcule F1 multiclase con `average="macro"`.

**Producto esperado:** particiones comunes, tabla de auditoría, ejemplos por clase y formas de entrada verificadas.

---

## 🌳 Sección 2: Línea Base con Modelos Clásicos

1. Entrene los siguientes modelos sobre los píxeles aplanados y normalizados:
   - `DecisionTreeClassifier(max_depth=20, random_state=42)`.
   - `RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=42)`.
   - `SVC(kernel="rbf", C=1.0, gamma="scale")`.
2. Mida el tiempo de entrenamiento de cada modelo con `time.perf_counter()` alrededor de `fit`. Excluya la carga de datos y la evaluación.
3. Construya una tabla con el modelo, los hiperparámetros, el tiempo de entrenamiento y las métricas **accuracy y F1 macro en entrenamiento y validación**.
4. Seleccione el mejor modelo clásico por **accuracy de validación**. En caso de empate, use F1 macro y luego el menor tiempo de entrenamiento. Mantenga este criterio durante toda la tarea.
5. Interprete las diferencias entre entrenamiento y validación y contraste el orden de desempeño de los modelos en ambas particiones.

Use las configuraciones indicadas; no se exige una búsqueda exhaustiva de hiperparámetros. Esta comparación evalúa esas configuraciones, no demuestra que una familia de modelos sea siempre superior.

**Producto esperado:** tres modelos entrenados, tabla comparativa y selección argumentada de la línea base.

---

## 🧠 Sección 3: CNN con Uno, Dos y Tres Bloques

Construya tres modelos nuevos con `tf.keras.Sequential`. En esta tarea, cada **bloque convolucional** contiene una capa `Conv2D` seguida de una capa `MaxPooling2D`; el número de bloques no cuenta las capas densas.

### Arquitecturas

| Elemento | Configuración |
|---|---|
| Entrada | `Input(shape=(28, 28, 1))` |
| Bloque 1 | `Conv2D(32, 3, padding="same", activation="relu")` + `MaxPooling2D(2)` |
| Bloque 2 | `Conv2D(64, 3, padding="same", activation="relu")` + `MaxPooling2D(2)` |
| Bloque 3 | `Conv2D(128, 3, padding="same", activation="relu")` + `MaxPooling2D(2)` |
| Cabezal común | `Flatten()` → `Dense(64, activation="relu")` → `Dropout(0.25)` → `Dense(10, activation="softmax")` |

- **CNN-1:** bloque 1 y cabezal.
- **CNN-2:** bloques 1 y 2, y cabezal.
- **CNN-3:** bloques 1, 2 y 3, y cabezal.

Mantenga los valores predeterminados de stride en estas capas: 1 en `Conv2D` y 2 en `MaxPooling2D(2)`, con padding `valid` en pooling. Esta especificación permite desarrollar la tarea sin los cuadernos de apoyo.

### Entrenamiento y comparación

1. Muestre `model.summary()` para cada CNN. Registre las formas de salida después de cada bloque, el tamaño del vector producido por `Flatten` y el número total de parámetros entrenables.
2. Entrene cada CNN **desde cero**, con un optimizador nuevo `Adam(learning_rate=0.001)`, pérdida `sparse_categorical_crossentropy`, métrica `accuracy`, **10 épocas** y `batch_size=64`. Use las etiquetas enteras originales y suministre explícitamente `validation_data`.
3. Mantenga el mismo presupuesto y use los pesos de la **última época** en las tres CNN. No use parada temprana, aumento de datos ni ajuste adicional de hiperparámetros en esta comparación.
4. Guarde el historial de cada entrenamiento. Grafique pérdida y accuracy de entrenamiento y validación frente a las épocas. Identifique evidencia de sobreajuste, subajuste o aprendizaje aún en progreso, sin asumir que necesariamente aparecen.
5. Mida el tiempo total de `fit` y calcule el tiempo promedio por época como `tiempo_total / 10`. Este tiempo incluye la validación y los costos iniciales de ejecución; indique el dispositivo empleado y manténgalo igual para las tres CNN.
6. Evalúe cada CNN en entrenamiento y validación con `evaluate` y `predict`, en modo inferencia. Construya una tabla con bloques, parámetros, tiempo total, tiempo promedio por época, accuracy y F1 macro de ambas particiones. No mezcle el accuracy del historial con la evaluación final: Dropout está activo durante el entrenamiento.
7. Seleccione la CNN con el criterio definido en la sección 2. Explique si el cambio de desempeño justifica el costo observado.

**Importante:** se mantiene la misma tasa de Dropout para evitar cambiar simultáneamente esa decisión. Aun así, añadir bloques cambia filtros, resolución espacial y tamaño de entrada a la capa densa. Es una comparación de arquitecturas: no permite atribuir todo cambio únicamente a la profundidad ni asumir que más bloques implican más parámetros.

**Producto esperado:** tres CNN, sus resúmenes y curvas, tabla de resultados y selección basada en validación.

---

## 📊 Sección 4: Evaluación Final y Análisis de Errores

1. Antes de usar prueba, deje por escrito cuáles son el modelo clásico y la CNN seleccionados y por qué. Conserve los modelos ya entrenados; no los reajuste en esta sección.
2. Obtenga una vez las predicciones sobre las **10 000 imágenes de prueba oficiales** para esos dos modelos. Presente una tabla final con accuracy y F1 macro en prueba, junto con sus métricas de validación y tiempos de entrenamiento.
3. Construya una matriz de confusión para cada modelo, con nombres de clases y ejes identificados. Señale dos pares de prendas que se confundan y compare los errores de ambos modelos.
4. Muestre seis imágenes mal clasificadas por la CNN, o todas si hay menos de seis. Indique etiqueta real y predicha y describa patrones visibles, sin elegir únicamente ejemplos que favorezcan su conclusión.
5. Compare desempeño y costo. Si scikit-learn se ejecutó en CPU y las CNN en GPU, presente los tiempos como resultados de esos entornos, no como una comparación del costo intrínseco de los algoritmos.

No use los errores ni las métricas de prueba para cambiar la arquitectura o escoger otra configuración. Si el orden de los modelos cambia frente a validación, repórtelo y discuta la diferencia.

**Producto esperado:** tabla final de los dos modelos seleccionados, matrices de confusión y análisis visual de errores.

---

## 💬 Sección 5: Conclusiones

Concluya el cuaderno con una síntesis de los experimentos realizados:

1. Resuma los cambios observados en accuracy de validación, parámetros y tiempo por época entre CNN-1, CNN-2 y CNN-3.
2. Sustente la comparación final entre el modelo clásico y la CNN seleccionados con las métricas y los errores observados.
3. Delimite las conclusiones al tamaño de muestra, la semilla, las configuraciones y el entorno de cómputo utilizados.

**Producto esperado:** una conclusión breve respaldada por los resultados del cuaderno.
