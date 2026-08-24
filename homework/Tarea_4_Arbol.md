# Tarea 4: Árboles de Decisión para Regresión y Clasificación

**Asignatura:** Técnicas de Aprendizaje de Máquina  
**Institución:** Pontificia Universidad Javeriana  
**Sesión:** Árboles de Decisión  

---

## 🎯 Objetivo

Implementar y evaluar modelos basados en Árboles de Decisión tanto para problemas de regresión (predicción de rendimientos financieros) como de clasificación (supervivencia en el Titanic). El estudiante deberá explorar cómo los distintos hiperparámetros de los árboles afectan el rendimiento y la complejidad del modelo.

---

## 📋 Instrucciones Generales para la Entrega

Deberá desarrollar y entregar un único cuaderno de Google Colab que contenga el desarrollo de los dos casos de modelado detallados a continuación. Todos los resultados de experimentación deben quedar plasmados en secciones de texto dentro del cuaderno.

1. **Entorno y Estructura:**
   - Ingrese a [Google Colab](https://colab.research.google.com/) y cree un **Nuevo cuaderno** (*New notebook*).
   - Utilice celdas de texto (Markdown) para separar claramente el documento en "Sección 1" y "Sección 2".

2. **Identificación del Grupo:**
   - En la primera celda del cuaderno, cree una **celda de texto (Markdown)** e incluya los **nombres completos de los integrantes** que entregan el taller.

3. **⚠️ IMPORTANTE - Reproducibilidad:**
   - Para garantizar que sus experimentos sean reproducibles, utilice `random_state=42` de manera consistente en todas las funciones que involucren un componente estocástico (como partición de datos o entrenamiento de modelos).

4. **Guardado y Entrega:**
   - Asegúrese de haber ejecutado **todas las celdas** y que los resultados sean visibles en pantalla.
   - Guarde el archivo con el formato: `Tarea4_Arboles_[Apellido1]_[Apellido2]`.
   - Cambie los permisos de acceso a **"Cualquier persona con el enlace"** (*Anyone with the link*) en modo Lector (*Viewer*) y pegue el enlace del cuaderno en el cuestionario de entrega, **junto con el enlace a su interfaz desplegada en Hugging Face Spaces**.

---

## 📈 Sección 1: Regresión de Precios de Viviendas (California Housing)

**Objetivo:** Retomar el conjunto de datos de precios de viviendas de California (utilizado en el Taller 2) para predecir su valor, esta vez utilizando árboles de decisión para regresión. Se explorará el impacto de múltiples hiperparámetros y se comparará el rendimiento contra los modelos lineales anteriores.

### Pasos a seguir:

1. **Carga y Preparación de Datos:**
   - Importe `fetch_california_housing` desde `sklearn.datasets`.
   - Extraiga la matriz de características $X$ (con **todas** sus columnas) y el vector objetivo $y$.
   - *Nota:* Recuerde que los árboles de decisión son insensibles a la escala de los datos, por lo que no es estrictamente necesario normalizar o estandarizar las variables, a diferencia de los modelos lineales.

2. **Partición de Datos:**
   - Utilice `train_test_split` de `sklearn.model_selection` para dividir los datos en entrenamiento (80%) y prueba (20%), manteniendo el `random_state=42`.

3. **Entrenamiento y Exploración de Hiperparámetros:**
   - Importe `DecisionTreeRegressor` de `sklearn.tree` y `GridSearchCV` (o `RandomizedSearchCV`) de `sklearn.model_selection`.
   - Utilice búsqueda en grilla o aleatoria (con validación cruzada `cv=5`) para encontrar la mejor combinación de hiperparámetros. Asegúrese de incluir `random_state=42` en la instanciación del regresor base.
   - Explore variaciones en: `criterion`, `max_depth`, `max_features`, `max_leaf_nodes`, `min_impurity_decrease`, `min_samples_leaf`, `min_samples_split`.
   - Imprima los mejores parámetros encontrados (`best_params_`) y analice en una celda de texto el impacto que tienen estos valores óptimos en la prevención del sobreajuste.

4. **Evaluación y Comparación:**
   - Para cada uno de los modelos entrenados, calcule las siguientes métricas tanto en el conjunto de desarrollo (entrenamiento) como en el de prueba:
     - `mean_squared_error`
     - `mean_absolute_error`
     - `r2_score`
   - **Análisis Comparativo:** En una celda de texto, compare el `mean_absolute_error` (MAE) del mejor árbol de decisión con el obtenido por la regresión lineal del Taller 2. ¿Qué modelo logró capturar mejor los patrones de los precios de las viviendas?

---

## 🚢 Sección 2: Clasificación de Supervivencia - Titanic

**Objetivo:** Implementar un modelo de clasificación basado en árboles de decisión para el clásico problema del Titanic y desplegar el mejor modelo mediante una interfaz gráfica.

### Pasos a seguir:

1. **Carga y Preparación de Datos:**
   - Cargue la base de datos Titanic en Google Colab.
   - **⚠️ IMPORTANTE - Estandarización:** Para garantizar que el modelo sea comparable con el del Taller 2, debe aplicar *exactamente* el mismo preprocesamiento: impute los valores nulos de `Age` con la media aritmética, mapee la variable `Sex` (female=1, male=0), y defina su matriz $X$ utilizando únicamente las columnas `['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare']`.

2. **Partición de Datos:**
   - Separe los datos en conjuntos de entrenamiento y prueba utilizando `train_test_split`.

3. **Entrenamiento y Exploración de Hiperparámetros:**
   - Importe `DecisionTreeClassifier` de `sklearn.tree` y `GridSearchCV` (o `RandomizedSearchCV`) de `sklearn.model_selection`.
   - Utilice búsqueda en grilla o aleatoria (con validación cruzada `cv=5`) para optimizar el árbol, recordando fijar `random_state=42`. Explore hiperparámetros como: `criterion`, `max_depth`, `max_features`, `max_leaf_nodes`, `min_impurity_decrease`, `min_samples_leaf`, `min_samples_split`.
   - Entrene el grid y reporte los `best_params_`. Analice en una celda de texto cómo esta combinación de hiperparámetros ayuda a mejorar la capacidad de generalización del modelo.

4. **Evaluación de Clasificación:**
   - Genere predicciones y calcule la matriz de confusión.
   - Evalúe el modelo utilizando las siguientes métricas:
     - `Accuracy`
     - `Precision`
     - `Recall`
     - `F1`

5. **Comparación y Despliegue:**
   - **Tabla Comparativa Final:** Cree un DataFrame en Pandas que compare el rendimiento (midiendo al menos `Accuracy` y `F1-Score` en el conjunto de prueba) de su mejor Árbol de Decisión contra el modelo de **Regresión Logística (Taller 2)** y el modelo **SVC (Taller 3)**. Discuta en una celda de texto qué modelo resultó ser el mejor y por qué.
   - **Interfaz Gráfica:** Implemente una interfaz gráfica con Gradio para hacer predicciones en tiempo real. La interfaz debe permitir ingresar características relevantes de un pasajero y devolver la probabilidad (o predicción) de supervivencia.
   - **Despliegue en Hugging Face:** Publique su interfaz gráfica como un *Space* público en [Hugging Face Spaces](https://huggingface.co/spaces). Su código debe contener todo lo necesario (ej. archivo `app.py`, y `requirements.txt` con los paquetes necesarios) para que el entorno levante el modelo correctamente. Incluya el enlace a su Space en las entregas.
