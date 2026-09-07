"""Genera la visualización del árbol de decisión sustituto para interpretar K-Means."""

import os
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, plot_tree

ROOT = Path(__file__).resolve().parent.parent.parent
DATA_PATH = ROOT / "quarto" / "clustering" / "data" / "Country-data.csv"
OUTPUT = ROOT / "quarto" / "clustering" / "assets" / "generated"

FEATURES = [
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

FEATURE_SPANISH = [
    "Mortalidad inf.",
    "Exportaciones",
    "Gasto salud",
    "Importaciones",
    "Ingreso",
    "Inflación",
    "Esperanza vida",
    "Fertilidad",
    "PIB per cápita",
]


def main():
    data = pd.read_csv(DATA_PATH)
    X = data[FEATURES].to_numpy(dtype=float)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Ajustar K-Means con K=4
    kmeans = KMeans(n_clusters=4, n_init=30, random_state=42).fit(X_scaled)
    labels = kmeans.labels_

    # Ajustar árbol sustituto
    surrogate = DecisionTreeClassifier(
        max_depth=3,
        min_samples_leaf=8,
        random_state=42,
    ).fit(X_scaled, labels)

    fidelity = surrogate.score(X_scaled, labels)
    print(f"Fidelidad: {fidelity:.1%}")

    # Visualización del árbol
    # Palette matching presentation
    class_names = [f"Grupo {k}" for k in range(4)]

    fig, ax = plt.subplots(figsize=(11, 4.4), dpi=200)
    plot_tree(
        surrogate,
        feature_names=FEATURE_SPANISH,
        class_names=class_names,
        filled=True,
        rounded=True,
        precision=1,
        fontsize=8,
        ax=ax,
        impurity=False,
    )

    OUTPUT.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT / "kmeans_surrogate_tree.png"
    fig.savefig(out_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[ok] Guardada imagen del árbol en: {out_path}")


if __name__ == "__main__":
    main()
