# Preguntas de Selección Múltiple - Ensambles

**1. ¿Cuál es el principal objetivo de utilizar técnicas de ensambles (como Random Forest o Gradient Boosting) en problemas de clasificación o regresión en lugar de un único modelo base (como un solo Árbol de Decisión)?**
a) Disminuir radicalmente el tiempo de entrenamiento, ya que los ensambles entrenan más rápido que un modelo simple al usar menos memoria.
b) Combinar las predicciones de múltiples modelos base para mejorar la robustez, reducir la varianza y, en general, obtener un mejor rendimiento predictivo que un modelo aislado.
c) Asegurar que el modelo final sea completamente interpretable y fácil de visualizar mediante diagramas de flujo simples.
d) Eliminar la necesidad de realizar un preprocesamiento de los datos, ya que los ensambles manejan automáticamente los valores nulos sin ningún tratamiento previo.

**Respuesta Correcta:** b

---

**2. En el Taller 5, se utilizó un `RandomForestClassifier` para la base de datos de Cáncer. ¿De qué manera este algoritmo introduce diversidad entre los distintos árboles de decisión que lo componen para evitar que todos sean idénticos?**
a) Utiliza una única muestra de datos para todos los árboles, pero entrena cada árbol durante un número diferente de iteraciones.
b) Emplea el método de Bagging (Bootstrap Aggregating) extrayendo muestras aleatorias con reemplazo de los datos de entrenamiento y, además, selecciona un subconjunto aleatorio de características (features) en cada división del nodo.
c) Entrena los árboles secuencialmente, donde cada nuevo árbol intenta corregir los errores del árbol anterior.
d) Aplica una función de activación no lineal en las hojas de los árboles, similar a una red neuronal profunda.

**Respuesta Correcta:** b

---

**3. En el ejercicio de la base de datos de Finca Raíz, se evaluó el desempeño de `Random Forest` frente a técnicas de Boosting (`Gradient Boosting`, `XGBoost`, `LightGBM`). ¿Cuál es la principal diferencia conceptual en la forma en que el `Gradient Boosting` construye su ensamble frente al `Random Forest`?**
a) Gradient Boosting construye los árboles de manera secuencial, donde cada nuevo árbol se enfoca en minimizar los errores (residuos) de los árboles previos; mientras que Random Forest los construye de forma independiente y paralela.
b) Gradient Boosting construye árboles de forma independiente y paralela, mientras que Random Forest los construye secuencialmente.
c) Gradient Boosting solo puede utilizarse para problemas de clasificación binaria, mientras que Random Forest solo funciona para regresión.
d) Gradient Boosting utiliza Máquinas de Soporte Vectorial (SVM) como modelos base en lugar de árboles de decisión.

**Respuesta Correcta:** a

---

**4. Durante la tarea se solicitó implementar un `StackingClassifier` utilizando una `LogisticRegression` como estimador final (`final_estimator`). ¿Cuál es la función específica de este estimador final dentro de la arquitectura de Stacking?**
a) Promediar directamente (o usar voto mayoritario en) las predicciones de los modelos base para obtener el resultado final, sin ningún tipo de entrenamiento adicional.
b) Entrenar un meta-modelo que aprende a combinar de manera óptima las predicciones de los modelos de la capa anterior, dándole mayor o menor peso a cada clasificador según sus aciertos en el conjunto de entrenamiento.
c) Escalar y normalizar las características originales antes de pasarlas a los modelos base de la primera capa.
d) Reducir la dimensionalidad del conjunto de datos mediante un análisis de componentes principales (PCA) previo a la clasificación.

**Respuesta Correcta:** b

---

**5. Cuando evaluamos las métricas de un ensamble avanzado como XGBoost o LightGBM, es posible notar que el rendimiento en el conjunto de entrenamiento es casi perfecto, pero en prueba disminuye significativamente. ¿Qué estrategia es útil para mitigar este sobreajuste (overfitting) en modelos de Boosting?**
a) Aumentar la profundidad máxima de los árboles (`max_depth`) para que aprendan relaciones aún más específicas de la muestra de entrenamiento.
b) Disminuir el número de árboles (`n_estimators`) y/o reducir la tasa de aprendizaje (`learning_rate`) e introducir parámetros de regularización para hacer que el modelo aprenda de forma más conservadora.
c) Cambiar el ensamble a un `VotingClassifier` utilizando únicamente múltiples instancias exactas del mismo modelo de Boosting con los mismos hiperparámetros.
d) Eliminar cualquier tipo de regularización para permitir que el modelo crezca sin ningún tipo de restricciones y se adapte al 100% de los datos.

**Respuesta Correcta:** b
