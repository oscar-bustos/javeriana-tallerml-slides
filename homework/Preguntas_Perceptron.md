# Preguntas de Selección Múltiple - Perceptrón Multicapa (MLP)

**1. En el ejercicio de Cáncer, las características numéricas presentan rangos y unidades dispares (por ejemplo, `mean area` frente a `mean smoothness`). Si se evalúa un `MLPClassifier` mediante `GridSearchCV`, ¿cuál es la manera metodológicamente correcta de integrar `StandardScaler` para evitar la fuga de información (*data leakage*) entre particiones?**
a) Ajustar (`fit`) el escalador sobre todo el conjunto de datos antes de realizar cualquier división, ya que la media y la desviación estándar deben reflejar la distribución global de la población.
b) Ajustar el escalador únicamente con el conjunto de prueba y aplicar dicha transformación al conjunto de entrenamiento para garantizar una evaluación imparcial.
c) Encapsular el escalador y el `MLPClassifier` dentro de un `Pipeline` de scikit-learn y suministrarlo a `GridSearchCV`, de modo que el escalador se ajuste exclusivamente con la porción de entrenamiento de cada pliegue (*fold*) de validación cruzada.
d) Omitir el escalamiento de características, debido a que optimizadores basados en gradiente como `adam` normalizan internamente las entradas sin verse afectados por diferencias de magnitud.

**Respuesta Correcta:** c

---

**2. Al entrenar un `MLPClassifier` para la clasificación de tumores, se obtiene un F1-score de 0.99 en el conjunto de entrenamiento pero cae a 0.81 en el conjunto de prueba, indicando sobreajuste (*overfitting*). ¿De qué forma el hiperparámetro `alpha` contribuye a mitigar este problema?**
a) Funciona como la tasa de aprendizaje inicial (`learning_rate_init`); disminuir su valor hacia cero acelera la convergencia y evita que la red memorice ruido.
b) Representa el término de penalización de regularización L2 (*weight decay*); incrementar su valor penaliza magnitudes excesivas en los pesos de las conexiones, reduciendo la complejidad del modelo y favoreciendo la generalización.
c) Define la tolerancia del criterio de parada temprana (*early stopping*); reducirlo fuerza a la red a continuar el entrenamiento durante más épocas hasta encontrar un mínimo global.
d) Controla la probabilidad de desactivación de neuronas en capas de Dropout intermedias; fijar un valor negativo desactiva selectivamente las neuronas menos informativas.

**Respuesta Correcta:** b

---

**3. En el taller se comparan arquitecturas como `(100,)` o `(50, 50)` frente a diversas funciones de activación (`relu`, `tanh`, `logistic`, `identity`). Desde el punto de vista matemático y de capacidad de representación, ¿qué sucede si se configuran todas las capas ocultas de un MLP con `activation='identity'`?**
a) La composición de sucesivas transformaciones lineales (afines) colapsa matemáticamente en una única transformación afín equivalente ($W_{\text{total}} x + b_{\text{total}}$), por lo que la red profunda no puede trazar fronteras de decisión no lineales y se reduce a un modelo lineal estándar.
b) La red conserva su capacidad de aproximación universal, pero el cálculo del gradiente se simplifica, lo que agiliza el entrenamiento sin sacrificar la no linealidad.
c) Se genera una saturación inmediata en las derivadas de retropropagación (*vanishing gradient*), impidiendo por completo la actualización de los pesos sinápticos desde la primera época.
d) La red se convierte conceptualmente en un clasificador de vectores de soporte (SVC) con margen duro y sin necesidad de regularización.

**Respuesta Correcta:** a

---

**4. Al optimizar los hiperparámetros del `MLPClassifier` en el ejercicio de Cáncer (`learning_rate_init`, `hidden_layer_sizes`, `activation`, `solver`), ¿cuál es el procedimiento riguroso para seleccionar el mejor modelo y estimar de forma no sesgada su rendimiento en datos no observados?**
a) Evaluar cada combinación de hiperparámetros directamente sobre el conjunto de prueba (*test set*), seleccionar la que maximice el F1 en dicha partición y reportar esa métrica como la evaluación final del modelo.
b) Entrenar cada arquitectura con la totalidad de los datos sin particionar y seleccionar la combinación que minimice la función de pérdida en la última época.
c) Seleccionar la mejor combinación observando únicamente el desempeño en el conjunto de entrenamiento, puesto que un F1 cercano a 1.0 garantiza que el modelo capturó la relación subyacente.
d) Realizar la búsqueda y validación cruzada (`GridSearchCV` o `RandomizedSearchCV`) exclusivamente sobre el conjunto de entrenamiento, y utilizar el conjunto de prueba reservado (*hold-out*) una sola vez al final para evaluar el modelo definitivo.

**Respuesta Correcta:** d

---

**5. En el ejercicio de Finca Raíz, la variable objetivo continua `SalePrice` se escala (por ejemplo, con `StandardScaler` o transformación logarítmica) antes de entrenar el `MLPRegressor`. ¿Qué paso es indispensable antes de calcular el error absoluto medio (`mean_absolute_error`) para reportarlo en unidades monetarias y compararlo con los modelos de ensambles del taller anterior?**
a) Calcular el MAE directamente entre el precio original en dólares y las predicciones escaladas arrojadas por la red, pues la métrica se ajusta automáticamente a la escala.
b) Aplicar la transformación inversa (`inverse_transform` o la función exponencial) a las predicciones generadas por el modelo para devolverlas a la escala monetaria original y luego calcular el error frente a los precios reales del conjunto de prueba.
c) Sustituir el cálculo de `mean_absolute_error` por la métrica de exactitud (*accuracy*), ya que al normalizar la variable objetivo el problema se transforma en uno de clasificación binaria.
d) Reajustar (`fit`) nuevamente el escalador de la variable objetivo usando las predicciones del conjunto de prueba antes de calcular cualquier métrica de regresión.

**Respuesta Correcta:** b
