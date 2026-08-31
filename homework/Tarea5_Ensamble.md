# Tarea 5: Ensambles

**Asignatura:** Técnicas de Aprendizaje de Máquina  
**Institución:** Pontificia Universidad Javeriana  
**Sesión:** Ensambles  

---

## 🎯 Objetivo

Implementar un modelo de clasificación y regresión basado en ensambles utilizando la base de datos de Cáncer y la base de datos de Finca Raíz, evaluando el rendimiento de diferentes métodos como Random Forest, Gradient Boosting, Voting y Stacking.

---

## 📋 Descripción de la Actividad

Esta tarea representa la evaluación práctica del uso de modelos basados en Ensambles. Deberá desarrollar y entregar un único cuaderno de Google Colab que contenga el desarrollo de los casos detallados a continuación.

### Instrucciones Generales para la Entrega:

1. **Entorno y Estructura:**
   - Ingrese a [Google Colab](https://colab.research.google.com/) y cree un **Nuevo cuaderno** (*New notebook*).
   - Utilice celdas de texto (Markdown) para separar claramente el documento según los puntos solicitados.

2. **Identificación del Grupo:**
   - En la primera celda del cuaderno, cree una **celda de texto (Markdown)** e incluya los **nombres completos de los integrantes** que entregan el taller.

3. **⚠️ IMPORTANTE - Reproducibilidad:**
   - Para garantizar que sus experimentos sean reproducibles, debe imponer una semilla aleatoria en todas las funciones que involucren un componente estocástico.
   - Utilice `random_state=42` de manera consistente en todo su código.

4. **Guardado y Entrega:**
   - Asegúrese de haber ejecutado **todas las celdas** y que los resultados sean visibles en pantalla.
   - Guarde el archivo con el formato: `Taller5_Ensambles_[Apellido1]_[Apellido2]`.
   - Cambie los permisos de acceso a **"Cualquier persona con el enlace"** (*Anyone with the link*) en modo Lector (*Viewer*) y pegue el enlace en el cuestionario de entrega.

---

## 🏥 Ejercicio 1 – Cáncer (25pts)

Implemente un modelo de clasificación basado en ensambles utilizando la base de datos de Cancer.

1. Cargue la base de datos de Cancer, presente en la siguiente URL: [cancer.csv](https://github.com/oscar-bustos/javeriana-analitica/blob/main/taller3/cancer.csv)
2. Lea sobre la metadata de este conjunto de datos:
   - [Metadata de Kaggle](https://www.kaggle.com/datasets/erdemtaha/cancer-data)
3. Realice la limpieza de datos eliminando valores nulos.
4. Separe los datos en conjuntos de entrenamiento y prueba.
5. Entrene un ensamble de clasificadores con las siguientes librerías de Sklearn:
   - `sklearn.ensemble.RandomForestClassifier`
   - `sklearn.ensemble.GradientBoostingClassifier`
   - `sklearn.ensemble.VotingClassifier` que utilice los siguientes clasificadores:
     - `sklearn.linear_model.LogisticRegression`
     - `sklearn.svm.SVC` Kernel lineal
     - `sklearn.svm.SVC` Kernel polinómico
     - `sklearn.svm.SVC` Kernel radial
     - `sklearn.tree.DecisionTreeClassifier`
   - `sklearn.ensemble.StackingClassifier` que utilice los siguientes clasificadores. Use como parámetro de `final_estimator` a `LogisticRegression()`:
     - `sklearn.tree.DecisionTreeClassifier`
     - `sklearn.svm.SVC` Kernel lineal
     - `sklearn.svm.SVC` Kernel polinómico
     - `sklearn.svm.SVC` Kernel radial
6. Haz una tabla comparativa de los cuatro anteriores ensambles, que reporte el Accuracy y F1 en datos de entrenamiento y en pruebas. 

---

## 🏠 Ejercicio 2 – Finca Raíz (25pts)

Implemente un modelo de regresión basado en ensambles utilizando la base de datos Finca Raiz de Boston.

1. Cargue la base de datos de finca raíz en Ames, Iowa (Estados Unidos), presente en la siguiente URL: [housing.csv](https://github.com/oscar-bustos/javeriana-analitica/blob/main/housing/housing.csv)
2. Lea sobre la metadata de este conjunto de datos:
   - [Overview de Kaggle](https://www.kaggle.com/competitions/home-data-for-ml-course/overview)
3. Realice la limpieza de datos eliminando valores nulos.
4. Separe los datos en conjuntos de entrenamiento y prueba.
5. Entrene un ensamble de regresores con las siguientes librerías:
   - `sklearn.ensemble.RandomForestRegressor`
   - `sklearn.ensemble.GradientBoostingRegressor`
   - `Lightgbm`
   - `Xgboost`
6. Para cada uno de los modelos, calcule las siguientes métricas tanto en desarrollo como en prueba: `mean_squared_error`, `mean_absolute_error`, `r2_score` y encuentre el mejor modelo.
7. Implemente una interfaz gráfica con Gradio para hacer predicciones sobre el valor estimado de la finca raíz dependiendo el modelo seleccionado. Permita que el usuario seleccione las variables desde filtros desplegables, con los valores opcionales mostrados en la siguiente metadata:
   - [data_description.txt](https://github.com/oscar-bustos/javeriana-analitica/blob/main/housing/data_description.txt)
