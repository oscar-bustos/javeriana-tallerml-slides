# Tarea 3: Máquinas de Soporte Vectorial (SVM)

**Asignatura:** Técnicas de Aprendizaje de Máquina  
**Institución:** Pontificia Universidad Javeriana  
**Sesión:** SVM  

---

## 🎯 Objetivo

Implementar y comprender a profundidad un modelo de clasificación SVM utilizando la base de datos Titanic. A diferencia de otros modelos, aquí exploraremos visual y métricamente cómo la dureza del margen ($C$) y la flexibilidad del Kernel afectan el sobreajuste (overfitting) y la capacidad de generalización.

---

## 📋 Descripción de la Actividad

Esta tarea representa la evaluación práctica del uso de Máquinas de Soporte Vectorial (SVM). Deberá desarrollar y entregar un único cuaderno de Google Colab que contenga el desarrollo del caso de modelado detallado a continuación.

### Instrucciones Generales para la Entrega:

1. **Entorno y Estructura:**
   - Ingrese a [Google Colab](https://colab.research.google.com/) y cree un **Nuevo cuaderno** (*New notebook*).
   - Utilice celdas de texto (Markdown) para separar claramente el documento según los puntos solicitados.

2. **Identificación del Grupo:**
   - En la primera celda del cuaderno, cree una **celda de texto (Markdown)** e incluya los **nombres completos de los integrantes** que entregan el taller.

3. **⚠️ IMPORTANTE - Reproducibilidad:**
   - Para garantizar que sus experimentos sean reproducibles, debe imponer una semilla aleatoria en todas las funciones que involucren un componente estocástico.
   - Utilice `random_state=42` de manera consistente en todo su código.

4. **Partición de Datos:**
   - Todos los modelos deben entrenarse utilizando una partición de los datos.
   - Importe y utilice la función `train_test_split` del módulo `sklearn.model_selection` para dividir su conjunto en datos de entrenamiento (80%) y prueba (20%).

5. **Guardado y Entrega:**
   - Asegúrese de haber ejecutado **todas las celdas** y que los resultados sean visibles en pantalla.
   - Guarde el archivo con el formato: `Taller3_SVM_[Apellido1]_[Apellido2]`.
   - Cambie los permisos de acceso a **"Cualquier persona con el enlace"** (*Anyone with the link*) en modo Lector (*Viewer*) y pegue el enlace en el cuestionario de entrega.

---

## 🚢 Ejercicio Práctico SVM - Titanic

### Pasos a seguir:

1. **Preparación de Datos:**
   - Cargue la base de datos Titanic en Google Colab.
   - Realice la limpieza de datos: elimine valores nulos y deje únicamente las variables de tipo numérico (ej. `Age`, `Fare`, `Pclass`, `SibSp`, `Parch`) para predecir la variable `Survived`.
   - Separe los datos en conjuntos de entrenamiento (80%) y prueba (20%).

2. **Intuición Visual: El Hiperplano y el Margen:**
   - Para entender qué está haciendo el SVM, primero trabajaremos en 2 dimensiones.
   - Cree un subconjunto de datos temporal que contenga solo dos variables predictoras (ej. `Age` y `Fare`) y la etiqueta `Survived`.
   - Entrene un modelo SVC con `kernel='linear'` sobre estos datos reducidos.
   - Genere un gráfico de dispersión (*scatter plot*) de los datos y dibuje el hiperplano separador (la línea recta) y, si es posible, los márgenes.
   - *Nota:* Observe cómo el algoritmo intenta separar las clases con una línea recta.

3. **El Impacto de la Regularización $C$:**
   - El parámetro $C$ controla el equilibrio entre maximizar el margen y minimizar el error de clasificación. Vamos a comprobar la teoría: "C pequeño prioriza márgenes amplios; C grande prioriza clasificar bien cada punto".
   - Usando todas las variables numéricas limpias del punto 1, entrene dos modelos SVM con kernel lineal:
     - **Modelo A (Rígido):** $C=0.01$ (Baja penalización por error, margen más amplio).
     - **Modelo B (Duro):** $C=1000$ (Alta penalización por error, margen ajustado).
   - Calcule y reporte el Accuracy tanto en Entrenamiento como en Prueba para ambos modelos.
   - **Análisis (Importante):** Responda en una celda de texto: ¿Cuál modelo generaliza mejor? ¿Observa overfitting en el modelo con $C=1000$? (Pista: Mire si la diferencia entre accuracy de train y test es grande).

4. **El "Truco del Kernel" y Optimización:**
   - Dado que los datos del Titanic difícilmente son separables linealmente, utilizaremos Kernels para proyectar los datos a dimensiones superiores.
   - Utilice `GridSearchCV` para encontrar la mejor combinación de hiperparámetros. Debe incluir en su grilla de búsqueda:
     - Kernels: `'linear'`, `'poly'`, `'rbf'`.
     - C: Valores logarítmicos (ej. `0.1`, `1`, `10`, `100`).
     - Gamma: (Solo para rbf/poly) Valores como `'scale'`, `'auto'`, `0.1`, `1`.
   - Reporte los `best_params_` encontrados y el `best_score_`.
   - **Discusión:** ¿El mejor modelo fue lineal o no lineal? ¿Qué nos dice esto sobre la estructura de los datos de supervivencia?

5. **Comparación y Despliegue:**
   - Finalmente, pondremos el modelo en producción y lo compararemos con sus intentos anteriores.
   - **Tabla Comparativa:** Compare (usando Accuracy o F1) el mejor modelo SVM obtenido en el paso anterior contra los mejores modelos de Regresión Logística del Taller 2. Seleccione el ganador absoluto.
   - **Interfaz Gráfica:** Implemente una interfaz simple con Gradio.
     - Debe permitir ingresar los datos numéricos de un pasajero (Edad, Tarifa, etc.).
     - Debe mostrar la predicción: "¿Sobrevive o No?".