Taller 2: Regresión y Clasificación con Modelos Lineales

Asignatura: Técnicas de Aprendizaje de Máquina

Institución: Pontificia Universidad Javeriana

Sesión: Modelos Lineales

📋 Instrucciones Generales para la Entrega

Esta tarea representa la continuación práctica del Análisis Exploratorio de Datos (EDA) realizado en la Tarea 0. Deberá desarrollar y entregar un único cuaderno de Google Colab que contenga el desarrollo de los dos casos de modelado detallados a continuación.

Entorno y Estructura: Ingrese a Google Colab y cree un Nuevo cuaderno (New notebook). Utilice celdas de texto (Markdown) para separar claramente el documento en "Sección 1" y "Sección 2".

Identificación del Grupo: En la primera celda del cuaderno, incluya los nombres completos de los 2 integrantes que entregan el taller.

⚠️ IMPORTANTE - Reproducibilidad: Para garantizar que sus experimentos sean reproducibles, debe imponer una semilla aleatoria en todas las funciones que involucren un componente estocástico. Utilice random_state=42 de manera consistente en todo su código.

Partición de Datos: Todos los modelos deben entrenarse utilizando una partición de los datos. Importe y utilice la función train_test_split del módulo sklearn.model_selection para dividir su conjunto en datos de entrenamiento (80%) y prueba (20%).

Guardado y Entrega:

Asegúrese de haber ejecutado todas las celdas y que los resultados sean visibles en pantalla.

Guarde el archivo con el formato: Taller2_ModelosLineales_[Apellido1]_[Apellido2].

Cambie los permisos de acceso a "Cualquier persona con el enlace" (Anyone with the link) en modo Lector (Viewer) y pegue el enlace en el cuestionario de entrega.

📊 Sección 1: Regresión Lineal, Regularización y Predicción de Precios

Objetivo: Entrenar modelos de regresión lineal para predecir el valor de viviendas, implementando técnicas de regularización para controlar la complejidad. El estudiante deberá comparar el rendimiento de distintos algoritmos, interpretar la importancia de las variables y traducir las métricas de error al contexto real del negocio.

Preparación de Datos:

Importe fetch_california_housing desde sklearn.datasets.

Extraiga la matriz de características $X$ (con todas sus columnas) y el vector objetivo $y$.

💡 Sugerencia de Pre-procesamiento: Para obtener exactamente el MAE esperado de $\approx 0.5332$ en el conjunto de prueba, no escale ni normalice las variables originales antes de entrenar la Regresión Lineal estándar.

Realice la partición de entrenamiento y pruebas (aplique la semilla aleatoria random_state=42).

Entrenamiento y Comparación de Modelos:

Importe LinearRegression, Lasso y Ridge desde sklearn.linear_model.

Entrene los tres modelos utilizando su conjunto de entrenamiento asignando random_state=42 a Lasso y Ridge.

Análisis de Regularización (Lasso):

Extraiga los coeficientes ($\beta$) generados por el modelo Lasso.

Identifique cuáles son las variables más importantes (los coeficientes con mayor magnitud) y cuáles fueron anuladas (coeficientes iguales a cero).

Escriba una celda de texto analizando: ¿Tiene sentido el peso asignado a estas variables desde una perspectiva lógica/inmobiliaria? ¿Cuál fue el impacto de aplicar la penalización respecto al modelo de regresión lineal estándar?

Interpretación del Error:

Genere predicciones sobre el conjunto de prueba utilizando el modelo LinearRegression.

Calcule el Error Absoluto Medio (MAE) importando mean_absolute_error de sklearn.metrics.

Análisis: Teniendo en cuenta que la variable objetivo del dataset de California está expresada en cientos de miles de dólares, multiplique su MAE por 100,000 para convertirlo a dólares exactos. Responda en una celda de texto: ¿Considera que el modelo es útil y preciso para el negocio inmobiliario considerando esta magnitud de error?

🚢 Sección 2: Clasificación Logística y Detección de Supervivencia (Titanic)

Objetivo: Implementar un modelo de Regresión Logística para resolver un problema de clasificación binaria basado en datos históricos. El estudiante deberá identificar el impacto de los predictores en la probabilidad de la clase y realizar una evaluación exhaustiva del modelo utilizando múltiples métricas de clasificación.

Preparación de Datos:

Descargue y cargue el conjunto de datos clásico del Titanic utilizando el mismo repositorio de la Tarea 1&nbsp;(https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv)). Utilice la librería pandas para leer el archivo CSV.

💡 Sugerencia de Pre-procesamiento: Para asegurar que las métricas cuadren exactamente, aplique los siguientes pasos:

Impute los valores nulos de la variable Age utilizando la media aritmética de dicha columna.

Convierta la variable categórica Sex en numérica, mapeando female como 1 y male como 0.

Defina su matriz predictora $X$ utilizando únicamente estas 6 variables: ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare'].

Defina su vector objetivo $y$ utilizando la columna Survived.

Realice la partición de entrenamiento y pruebas (aplique la semilla aleatoria random_state=42).

Entrenamiento del Modelo:

Importe LogisticRegression de sklearn.linear_model.

Instancie el modelo configurando los parámetros random_state=42 y max_iter=1000 para garantizar la convergencia.

Entrene el modelo utilizando el conjunto de datos de entrenamiento.

Interpretabilidad del Modelo:

Extraiga los coeficientes de la regresión logística.

Determine mediante código cuál es la variable que más peso tiene en el modelo (aquella con el coeficiente de mayor magnitud absoluta).

Explique brevemente en una celda de texto qué significa este resultado en el contexto del hundimiento del Titanic.

Evaluación Integral de Clasificación:

Importe de sklearn.metrics las funciones necesarias para calcular: Accuracy, Precision, Recall, F1-Score y ROC-AUC.

Genere las predicciones sobre el conjunto de prueba y calcule todas las métricas mencionadas.

En una celda de texto, interprete los resultados en conjunto: ¿Qué tan bueno es el modelo? ¿En qué tipo de fallos (falsos positivos o falsos negativos) incurre con mayor frecuencia según lo que indican Precision y Recall?