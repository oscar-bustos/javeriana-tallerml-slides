# Preguntas de Selección Múltiple - Redes Neuronales Convolucionales (CNN)

Preguntas para el quiz de Brightspace sobre la [Tarea 9: CNN](Tarea9_CNN.md), con calificación automática. Seleccione una única respuesta por pregunta. Esta versión incluye la clave para configurar el quiz.

**1. En Fashion-MNIST, las mismas imágenes se representan como `(N, 784)` para SVM y Random Forest y como `(N, 28, 28, 1)` para la CNN. ¿Cuál explica correctamente la diferencia?**

a) Aplanar elimina parte de los píxeles, mientras que añadir el eje de canal reconstruye los valores perdidos.

b) Ambas representaciones conservan los valores; `Conv2D` utiliza explícitamente vecindarios espaciales y comparte filtros entre posiciones, mientras que los estimadores clásicos utilizados reciben características en columnas.

c) El último eje de tamaño 1 indica que cada imagen puede pertenecer únicamente a la clase 1.

d) `reshape` normaliza automáticamente los píxeles y `tf.newaxis` aprende una representación de las diez clases.

**Respuesta Correcta:** b

---

**2. La CNN recibe imágenes de `28 × 28 × 1`. Se aplica `Conv2D(32, 3, strides=1, padding="same", use_bias=True)` y luego `MaxPooling2D(pool_size=2, strides=2, padding="valid")`. Sin contar el eje del lote, ¿cuál es la forma final y cuántos parámetros entrenables tienen esas dos capas en conjunto?**

a) `14 × 14 × 1` y 320 parámetros, porque pooling reduce los 32 mapas a un solo canal.

b) `28 × 28 × 32` y 320 parámetros, porque `padding="same"` también impide la reducción del pooling posterior.

c) `14 × 14 × 32` y 288 parámetros, porque la capa convolucional no incluye sesgos aunque `use_bias=True`.

d) `14 × 14 × 32` y 320 parámetros: `(3 × 3 × 1 + 1) × 32`; el pooling no añade parámetros entrenables.

**Respuesta Correcta:** d

---

**3. Al entrenar una CNN, la pérdida de entrenamiento disminuye durante diez épocas, pero la pérdida de validación alcanza su mínimo en la cuarta época y luego aumenta de forma sostenida. ¿Qué interpretación está mejor respaldada por estas curvas?**

a) Hay indicios de sobreajuste después de la cuarta época: el modelo sigue mejorando su ajuste a entrenamiento mientras empeora su pérdida en datos de validación.

b) Hay indicios de subajuste después de la cuarta época: la disminución de la pérdida de entrenamiento demuestra que el modelo no logra aprender los patrones de esos datos.

c) La generalización mejora durante las diez épocas, porque la pérdida de entrenamiento es suficiente para evaluar el desempeño en imágenes no vistas.

d) Las curvas demuestran que la CNN necesita más bloques convolucionales y que aumentar su profundidad reducirá la pérdida de validación.

**Respuesta Correcta:** a

---

**4. Un estudiante propone cambiar `Dropout(0.25)` por `Dropout(0.5)` porque la CNN tiene más bloques. ¿Cuál es la interpretación más adecuada?**

a) Usar 0.5 elimina permanentemente la mitad de los pesos y reduce a la mitad los parámetros mostrados por `model.summary()`.

b) Toda CNN de tres bloques necesita una tasa de 0.5 para evitar sobreajuste, independientemente de los datos y del resto de la arquitectura.

c) Una tasa mayor anula una mayor proporción de activaciones durante el entrenamiento y puede regularizar más, pero también perjudicar el aprendizaje; debe compararse con arquitectura fija usando validación, y Dropout se desactiva en la inferencia habitual.

d) Dropout anula activaciones durante la evaluación en prueba, pero no interviene mientras se ejecuta `fit`.

**Respuesta Correcta:** c

---

**5. En una ejecución hipotética, CNN-3 obtiene menor accuracy de validación que CNN-1, tarda más por época y tiene menos parámetros totales. Ambas usan el mismo presupuesto. ¿Qué conclusión está respaldada por estos resultados?**

a) Hay necesariamente un error en `model.summary()`: añadir capas convolucionales siempre aumenta el número total de parámetros.

b) En esta ejecución, CNN-1 ofrece mejor accuracy de validación y menor tiempo por época; el pooling adicional de CNN-3 puede reducir la entrada a la capa densa y sus parámetros. El resultado no demuestra que toda CNN profunda sea inferior.

c) CNN-3 debe seleccionarse porque un menor número de parámetros garantiza mejor generalización en prueba.

d) CNN-3 debe seleccionarse porque su mayor profundidad implica que acabará superando a CNN-1 en cualquier conjunto de datos.

**Respuesta Correcta:** b

---

**6. En la clasificación de prendas de Fashion-MNIST, ¿por qué una CNN puede generalizar mejor que un Random Forest entrenado directamente sobre los píxeles aplanados?**

a) Porque aplanar las imágenes elimina las relaciones entre los valores de los píxeles e impide que Random Forest combine varias características en sus decisiones.

b) Porque la convolución garantiza que cualquier desplazamiento o rotación de una prenda produzca exactamente la misma predicción, sin importar el entrenamiento.

c) Porque una CNN aprende patrones locales, reutiliza los mismos filtros en distintas posiciones y combina patrones en capas sucesivas; Random Forest sobre píxeles aplanados no incorpora explícitamente esa estructura espacial. Esta ventaja debe comprobarse con datos no vistos.

d) Porque las CNN siempre tienen menos parámetros y requieren menos imágenes de entrenamiento que Random Forest para alcanzar el mismo desempeño.

**Respuesta Correcta:** c
