# Preguntas de Selección Múltiple - Árboles de Decisión

**1. Al entrenar un modelo `DecisionTreeClassifier` o `DecisionTreeRegressor`, ¿qué ocurre generalmente si dejamos el hiperparámetro `max_depth=None` y no ajustamos otros parámetros de parada?**
a) El modelo creará un árbol perfectamente balanceado, asegurando la mejor generalización posible sin necesidad de regularización.
b) El árbol se expandirá hasta que todas las hojas sean puras o contengan menos muestras que `min_samples_split`, lo que típicamente conduce a un severo sobreajuste (overfitting).
c) El modelo detendrá su crecimiento automáticamente al encontrar la profundidad óptima calculada mediante validación cruzada interna.
d) El modelo experimentará subajuste (underfitting), ya que será incapaz de capturar relaciones complejas en los datos.

**Respuesta Correcta:** b

---

**2. En los árboles de clasificación, los hiperparámetros `criterion='gini'` y `criterion='entropy'` definen:**
a) La métrica utilizada para evaluar la calidad de una división (split) en cada nodo, buscando siempre maximizar la ganancia de información o pureza.
b) El algoritmo de optimización para encontrar los pesos globales de las variables de forma similar al descenso del gradiente.
c) La función matemática que proyecta los datos a espacios de mayor dimensión para separar clases no lineales.
d) La técnica de preprocesamiento automático que transforma las variables categóricas en valores numéricos.

**Respuesta Correcta:** a

---

**3. Si observamos que un modelo de árbol de decisión tiene un excelente rendimiento en los datos de entrenamiento pero un desempeño muy pobre en los datos de prueba, ¿qué ajuste de hiperparámetros ayudaría más a mitigar este problema?**
a) Disminuir `min_samples_leaf` a 1 y cambiar el criterio de Gini a Entropía.
b) Aumentar la profundidad máxima (`max_depth`) y permitir un crecimiento ilimitado de nodos.
c) Aumentar `min_samples_split` y `min_samples_leaf`, así como limitar la profundidad máxima (`max_depth`) para forzar la poda del árbol.
d) Escalar todas las características usando `StandardScaler` y ajustar el parámetro $C$.

**Respuesta Correcta:** c

---

**4. A diferencia de modelos como SVM o Regresión Logística, los Árboles de Decisión tienen una ventaja particular al manejar los datos. ¿Cuál es esta ventaja?**
a) No requieren la definición de hiperparámetros, ya que el algoritmo siempre encuentra la estructura óptima de forma analítica.
b) Son inmunes al sobreajuste, por lo que nunca memorizan el ruido en el conjunto de entrenamiento.
c) No requieren escalar o normalizar las variables numéricas, ya que las divisiones en los nodos se basan en umbrales de valor absoluto y no en distancias.
d) Son los únicos algoritmos capaces de procesar imágenes y texto plano sin ningún tipo de vectorización previa.

**Respuesta Correcta:** c

---

**5. ¿Cuál es el propósito principal del hiperparámetro `min_impurity_decrease` en la implementación de Scikit-Learn?**
a) Garantizar que el modelo siempre converja a una solución convexa.
b) Definir un umbral mínimo: un nodo solo se dividirá si dicha división reduce la impureza (como Gini o MSE) en un valor mayor o igual a este umbral, actuando como un mecanismo de prepoda.
c) Calcular la reducción del error absoluto medio (MAE) exclusivamente en los problemas de regresión.
d) Asignar un peso menor a las clases minoritarias para resolver problemas de conjuntos de datos desbalanceados.

**Respuesta Correcta:** b
