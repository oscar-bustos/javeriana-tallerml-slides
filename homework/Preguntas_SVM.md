# Preguntas de Selección Múltiple - SVM y Dataset Titanic

**1. Antes de entrenar el modelo SVM con el dataset del Titanic, ¿por qué es indispensable aplicar un preprocesamiento como `StandardScaler` a características con escalas muy distintas (ej. `Age` entre 0-80 y `Fare` entre 0-500)?**
a) Porque la librería Scikit-Learn arrojará un error de compilación si detecta variables numéricas no normalizadas en la función `fit()`.
b) Porque SVM basa la construcción del margen en el cálculo de distancias; sin escalar, la variable con el rango más amplio (como Tarifa) dominará la distancia y distorsionará la frontera de decisión.
c) Porque ayuda a rellenar automáticamente los valores nulos (NaN) presentes en el conjunto de entrenamiento.
d) Porque permite que el modelo SVM funcione sin necesidad de usar validación cruzada.

**Respuesta Correcta:** b

---

**2. Durante la sección "El Impacto de la Regularización", se entrenó un Modelo A con $C=0.01$ y un Modelo B con $C=1000$. Si al evaluar el Modelo B en el dataset del Titanic observa un `Accuracy` del 98% en entrenamiento pero cae bruscamente a 65% en la prueba, ¿qué fenómeno evidencia este resultado?**
a) Underfitting: El modelo $C=1000$ es demasiado simple, asumiendo márgenes muy amplios, y no logró capturar ninguna relación entre las variables.
b) Overfitting: El modelo memorizó los datos de entrenamiento debido a una alta penalización de error (margen muy ajustado), perdiendo capacidad para generalizar si un nuevo pasajero sobrevive o no.
c) Balanceo de clases: Significa que la variable de supervivencia tiene exactamente 50% de sobrevivientes en el conjunto de prueba.
d) Optimización de Kernel: El modelo ha decidido cambiar automáticamente de un kernel lineal a un kernel polinomial de alto grado.

**Respuesta Correcta:** b

---

**3. En el taller se utilizó `GridSearchCV` para buscar la mejor combinación de parámetros probando los kernels `linear`, `poly` y `rbf` para clasificar a los pasajeros del Titanic. ¿Por qué el uso del "Truco del Kernel" (ej. RBF) suele entregar mejores resultados que el modelo lineal básico en este dataset?**
a) Porque el kernel lineal solo es válido para predecir variables continuas (regresión), no para clasificación binaria como la supervivencia.
b) Porque el kernel RBF elimina automáticamente la influencia de pasajeros atípicos (como aquellos con tarifas excesivamente altas).
c) Porque los factores de supervivencia (edad, tarifa, sexo, etc.) rara vez se pueden separar perfectamente con una sola línea recta; los kernels no lineales mapean los datos a más dimensiones permitiendo encontrar separaciones complejas.
d) Porque el kernel RBF no requiere de una limpieza de datos previa y puede procesar valores nulos directamente en la columna de Edad.

**Respuesta Correcta:** c

---

**4. ¿Cuál es la principal ventaja de utilizar un modelo de "Margen Suave" (Soft Margin) en lugar de un "Margen Duro" (Hard Margin) al clasificar datos ruidosos o del mundo real como los del Titanic?**
a) El margen suave fuerza a que absolutamente todos los puntos caigan fuera del margen, garantizando cero errores en el conjunto de entrenamiento.
b) El margen suave tolera ciertas violaciones (errores) mediante variables de holgura ($\zeta$), lo que lo hace mucho más robusto y generalizable frente a datos atípicos (outliers) o ruido.
c) El margen suave descarta automáticamente características irrelevantes del dataset, reduciendo el sobreajuste.
d) El margen suave solo es aplicable cuando usamos regresión logística, no funciona matemáticamente para SVM.

**Respuesta Correcta:** b

---

**5. Si en lugar de usar `GridSearchCV` para optimizar hiperparámetros (evaluando todas las combinaciones posibles) decidiéramos utilizar `RandomizedSearchCV`, ¿cuál sería el beneficio principal de este cambio?**
a) `RandomizedSearchCV` siempre garantiza encontrar matemáticamente los hiperparámetros óptimos globales, algo que `GridSearchCV` no puede asegurar.
b) `RandomizedSearchCV` explora una muestra aleatoria de combinaciones limitada por el parámetro `n_iter`, reduciendo drásticamente el costo y tiempo computacional frente a espacios de búsqueda muy grandes.
c) `RandomizedSearchCV` evita la necesidad de dividir los datos en particiones de entrenamiento y prueba (Cross-Validation).
d) `RandomizedSearchCV` es la única estructura en Python capaz de optimizar redes neuronales profundas junto a un modelo SVM.

**Respuesta Correcta:** b
