# Tarea 6: Clustering de Países con K-Means

**Asignatura:** Técnicas de Aprendizaje de Máquina  
**Institución:** Pontificia Universidad Javeriana  
**Sesión:** Aprendizaje no supervisado y clustering  
**Puntaje total:** 50 puntos

---

## 🎯 Objetivo

Construir, evaluar e interpretar una segmentación de países mediante K-Means. El ejercicio debe mostrar cómo las decisiones de preparación, escalamiento y selección de $K$ afectan los grupos obtenidos, y debe comunicar sus resultados sin tratar los clústeres como categorías naturales o definitivas.

---

## 📋 Instrucciones Generales

Desarrolle y entregue un único cuaderno de Google Colab con todas las celdas ejecutadas y sus resultados visibles.

1. **Identificación:** incluya los nombres completos de los integrantes en la primera celda Markdown.
2. **Estructura:** separe el cuaderno usando los mismos títulos de las seis secciones de esta guía.
3. **Reproducibilidad:** utilice `random_state=42` en PCA, K-Means, particiones y árboles. Use un valor entero explícito para `n_init`.
4. **Evidencia:** toda gráfica debe tener título, ejes, leyenda cuando aplique y una interpretación escrita.
5. **Entrega:** guarde el cuaderno como `Tarea6_KMeans_[Apellido1]_[Apellido2]`.
6. **Acceso:** comparta el Colab como **“Cualquier persona con el enlace”** en modo Lector y entregue ese enlace.

### Fuentes de datos

- [Diccionario de datos](https://github.com/oscar-bustos/javeriana-analitica/blob/main/countrydata/data-dictionary.csv)
- [Datos de países](https://github.com/oscar-bustos/javeriana-analitica/blob/main/countrydata/Country-data.csv)

Para leer los archivos directamente con pandas use:

```python
DATA_URL = "https://raw.githubusercontent.com/oscar-bustos/javeriana-analitica/main/countrydata/Country-data.csv"
DICTIONARY_URL = "https://raw.githubusercontent.com/oscar-bustos/javeriana-analitica/main/countrydata/data-dictionary.csv"
```

---

## 🔎 Sección 1: Auditoría y Comprensión — 5 puntos

1. Lea primero el diccionario y explique con sus palabras el significado de las variables.
2. Cargue `Country-data.csv` y reporte:
   - Número de países y variables.
   - Tipos de datos.
   - Valores faltantes y duplicados.
   - Estadísticas descriptivas de las variables numéricas.
3. Identifique variables con escalas muy diferentes, asimetrías u observaciones extremas.
4. Explique por qué esas propiedades afectan un algoritmo basado en distancia euclidiana.

**Producto esperado:** una tabla de auditoría y una conclusión breve sobre la calidad de los datos.

---

## ⚙️ Sección 2: Preparación y Escalamiento — 10 puntos

1. Separe la columna `country`; no debe entrar como característica de K-Means.
2. Construya una matriz $X$ con todas las variables numéricas justificadas.
3. Impute valores faltantes con la mediana, incluso si el dataset actual no contiene faltantes.
4. Estandarice las variables con `StandardScaler`.
5. Use `Pipeline` o una secuencia equivalente que evite mezclar datos transformados y originales.
6. Compare la dispersión de al menos dos variables antes y después del escalamiento.
7. Explique qué significa una distancia en el espacio estandarizado.

**Producto esperado:** pipeline reproducible, comprobación de faltantes y evidencia visual del escalamiento.

---

## 🧭 Sección 3: Modelos K-Means — 10 puntos

Entrene modelos para cada valor de $K$ entre 2 y 8.

1. Use `init="k-means++"`, `n_init=30` y `random_state=42`.
2. Para cada $K$, registre:
   - Inercia (`inertia_`).
   - Número de iteraciones (`n_iter_`).
   - Tamaño de cada clúster.
   - Centroides en el espacio estandarizado.
3. Presente una tabla comparativa para $K=2,\ldots,8$.
4. Compruebe si aparecen clústeres excesivamente pequeños.

**Producto esperado:** siete modelos comparables y una tabla resumen completa.

---

## 📏 Sección 4: Selección de K — 10 puntos

1. Grafique número de clústeres frente a inercia e identifique el posible codo.
2. Calcule y grafique la silueta promedio para cada $K$.
3. Construya diagramas de silueta para los dos valores de $K$ más prometedores.
4. Compare cohesión, separación y equilibrio de tamaños.
5. Seleccione un $K$ final y defiéndalo usando ambas métricas y la utilidad interpretativa.

**Importante:** no es suficiente escoger automáticamente el máximo de silueta. Discuta si la solución también produce perfiles útiles y estables.

**Producto esperado:** tres visualizaciones y una decisión argumentada.

---

## 🌎 Sección 5: Visualización e Interpretación — 10 puntos

1. Ajuste el modelo final usando todas las características estandarizadas.
2. Aplique `PCA(n_components=2, random_state=42)` para visualizar los países en dos dimensiones.
3. Coloree la proyección con los clústeres e identifique a Colombia.
4. Reporte la varianza explicada por PC1 y PC2. Aclare que PCA solo se usa para visualizar.
5. Transforme los centroides nuevamente a las unidades originales usando `inverse_transform()`.
6. Construya una tabla de perfiles con:
   - Centroides originales.
   - Tamaño del clúster.
   - Tres países más cercanos a cada centroide.
7. Identifique el clúster de Colombia y las variables que más influyen en su cercanía.
8. Compare su distancia al centroide asignado con la distancia al segundo centroide más cercano.
9. Encuentre el país más cercano a Colombia usando las nueve variables estandarizadas.
10. Defina un subconjunto de variables para una pregunta concreta —por ejemplo, salud y demografía o macroeconomía y comercio— y repita la búsqueda. Justifique las variables y explique por qué puede cambiar el vecino.

Responda: ¿la agrupación de Colombia tiene sentido según las variables utilizadas? ¿Existe un país “más parecido” sin especificar el propósito? ¿Qué información relevante no está representada?

**Producto esperado:** proyección PCA, tabla de perfiles, comparación de vecinos y análisis de Colombia.

---

## 🌳 Sección 6: Árbol Sustituto — 5 puntos

El árbol de esta sección no predice una categoría real: aproxima las fronteras producidas por K-Means.

1. Use las etiquetas del modelo final como objetivo temporal.
2. Divida las observaciones en entrenamiento (80%) y prueba (20%), estratificando por clúster cuando sea posible.
3. Entrene `DecisionTreeClassifier` con:
   - `max_depth=3`.
   - `min_samples_leaf=5` o un valor mayor justificado.
   - `random_state=42`.
4. Reporte la fidelidad del árbol frente a K-Means en entrenamiento y prueba.
5. Visualice el árbol e interprete al menos tres reglas en unidades comprensibles.
6. Explique por qué fidelidad alta no demuestra que los clústeres sean verdaderos.

**Producto esperado:** árbol legible, fidelidad en train/test e interpretación de reglas.

---

## ✅ Reflexión Final Obligatoria

Concluya el cuaderno respondiendo brevemente:

1. ¿Qué tan estable parece la solución si cambia la semilla o se usa un $K$ vecino?
2. ¿Qué limitaciones de K-Means son relevantes para este dataset?
3. ¿Qué decisiones reales no deberían tomarse únicamente con estos clústeres?
4. ¿Cómo evitaría nombres o interpretaciones que estigmaticen países?

---

## Rúbrica Resumida

| Componente | Puntos |
|---|---:|
| Auditoría y comprensión | 5 |
| Preparación y escalamiento | 10 |
| Modelos K-Means | 10 |
| Selección de $K$ | 10 |
| PCA, perfiles y Colombia | 10 |
| Árbol sustituto | 5 |
| **Total** | **50** |

La calificación considera tanto la corrección del código como la claridad de las explicaciones, la reproducibilidad y la calidad de la argumentación.
