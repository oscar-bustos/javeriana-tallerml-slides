# Taller 8: Perceptrón

**Asignatura:** Técnicas de Aprendizaje de Máquina<br>
**Institución:** Pontificia Universidad Javeriana<br>
**Tema:** Redes neuronales MLP<br>
**Puntaje total:** 50 puntos

---

## Ejercicio 1: Cáncer (25 puntos)

Implemente un modelo de clasificación basado en redes neuronales MLP utilizando la base de datos de cáncer.

1. Cargue la base de datos de cáncer desde [cancer.csv](https://github.com/oscar-bustos/javeriana-analitica/blob/main/taller3/cancer.csv).
2. Consulte la [descripción del conjunto de datos](https://www.kaggle.com/datasets/erdemtaha/cancer-data).
3. Limpie los datos eliminando los valores nulos.
4. Separe los datos en conjuntos de entrenamiento y prueba. La variable objetivo es `Diagnosis`.
5. Entrene un modelo con `sklearn.neural_network.MLPClassifier`.
6. Explore los siguientes hiperparámetros:
   - `learning_rate_init`: tasa de aprendizaje inicial; por ejemplo, `0.001`, `0.01` y `0.1`. Analice su efecto en la convergencia y el rendimiento.
   - `alpha`: regularización L2; por ejemplo, `0.0001`, `0.001` y `0.01`. Observe su efecto en el sobreajuste.
   - `hidden_layer_sizes`: número y tamaño de las capas ocultas; por ejemplo, `(100,)`, `(50, 50)` y `(100, 50, 25)`. Analice el efecto de la arquitectura.
   - `activation`: función de activación; compare `identity`, `logistic`, `tanh` y `relu`.
   - `solver`: algoritmo de optimización; compare `adam`, `lbfgs` y `sgd`.

   Utilice validación cruzada para evaluar diferentes combinaciones. Puede usar `GridSearchCV` o `RandomizedSearchCV` de scikit-learn.
7. Construya una tabla comparativa de los modelos entrenados. Incluya sus hiperparámetros y las métricas *accuracy* y F1 en entrenamiento y prueba.
8. Analice el efecto de cada hiperparámetro en el rendimiento. ¿Qué combinaciones funcionan mejor para este conjunto de datos?
9. Escale las características con `StandardScaler` o `MinMaxScaler`. Compare la convergencia y los resultados del MLP con y sin escalamiento.
10. Grafique la pérdida frente a las iteraciones para los mejores modelos encontrados. Analice la convergencia y la presencia de sobreajuste.
11. Compare en una tabla el desempeño del MLP con los modelos del taller anterior de ensambles.

---

## Ejercicio 2: Finca raíz (25 puntos)

Implemente un modelo de regresión basado en redes neuronales MLP utilizando la base de datos de finca raíz de Ames, Iowa (Estados Unidos).

1. Cargue los datos desde [train.csv](https://github.com/oscar-bustos/javeriana-analitica/blob/main/housing/train.csv).
2. Consulte la [descripción del conjunto de datos](https://www.kaggle.com/competitions/home-data-for-ml-course/overview).
3. Limpie los datos eliminando los valores nulos.
4. Separe los datos en conjuntos de entrenamiento y prueba. La variable objetivo es `SalePrice`.
5. Entrene un modelo con `sklearn.neural_network.MLPRegressor`.
6. Como en el ejercicio 1, explore diferentes valores de `learning_rate_init`, `alpha`, `hidden_layer_sizes`, `activation` y `solver`. Utilice validación cruzada para encontrar la mejor combinación.
7. Para el mejor modelo, calcule `mean_squared_error`, `mean_absolute_error` y `r2_score` en los conjuntos de entrenamiento y prueba.
8. Implemente una interfaz con Gradio para estimar el precio de una vivienda. Permita seleccionar los valores de las variables mediante filtros desplegables, de acuerdo con la [descripción de los datos](https://github.com/oscar-bustos/javeriana-analitica/blob/main/housing/data_description.txt).
9. Escale las características numéricas y la variable objetivo con técnicas apropiadas para regresión. Evalúe el efecto del escalamiento en el rendimiento.
10. Grafique los valores reales frente a los valores predichos por el mejor modelo en el conjunto de prueba.
11. Compare en una tabla el desempeño del MLP con los modelos del taller anterior de ensambles.
