from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, export_text

DATA_PATH = Path("quarto/clustering/data/Country-data.csv")
data = pd.read_csv(DATA_PATH)

features = [
    "child_mort",
    "exports",
    "health",
    "imports",
    "income",
    "inflation",
    "life_expec",
    "total_fer",
    "gdpp",
]

X = data[features].to_numpy(dtype=float)
X_scaled = StandardScaler().fit_transform(X)

kmeans = KMeans(n_clusters=4, n_init=30, random_state=42).fit(X_scaled)
labels = kmeans.labels_

surrogate = DecisionTreeClassifier(
    max_depth=3,
    min_samples_leaf=8,
    random_state=42,
).fit(X_scaled, labels)

fidelity = surrogate.score(X_scaled, labels)
print(f"Fidelidad del árbol sustituto frente a K-Means: {fidelity:.1%}")

rules = export_text(surrogate, feature_names=features)
print("\nReglas del árbol sustituto:")
print(rules)
