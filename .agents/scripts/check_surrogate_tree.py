import os
os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, export_text

def main():
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

    print("K-Means cluster counts:", dict(zip(*np.unique(labels, return_counts=True))))

    for depth in [1, 2, 3, 4]:
        for min_leaf in [1, 5, 8]:
            tree = DecisionTreeClassifier(
                max_depth=depth,
                min_samples_leaf=min_leaf,
                random_state=42,
            ).fit(X_scaled, labels)
            preds = tree.predict(X_scaled)
            pred_classes = np.unique(preds)
            fidelity = tree.score(X_scaled, labels)
            print(f"depth={depth}, min_leaf={min_leaf}: fidelity={fidelity:.1%}, unique predicted classes={pred_classes}, leaf_count={tree.get_n_leaves()}")

    print("\n--- Current surrogate (max_depth=3, min_samples_leaf=8) ---")
    current = DecisionTreeClassifier(
        max_depth=3,
        min_samples_leaf=8,
        random_state=42,
    ).fit(X_scaled, labels)
    print("Classes in tree:", current.classes_)
    print("Tree rules:")
    print(export_text(current, feature_names=features))
    print("Tree leaf values and predictions:")
    # Inspect cluster 1
    c1_countries = data.loc[labels == 1, ["country", "gdpp", "income", "exports", "health", "child_mort"]]
    print("\n--- Paises en Grupo 1 (K-Means) ---")
    print(c1_countries)

    # Exploration of pruning with ccp_alpha and manual pruning
    print("\n--- Pruning exploration ---")
    base_tree = DecisionTreeClassifier(random_state=42).fit(X_scaled, labels)
    path = base_tree.cost_complexity_pruning_path(X_scaled, labels)
    ccp_alphas, impurities = path.ccp_alphas, path.impurities

    print(f"Number of alphas: {len(ccp_alphas)}")
    for alpha in ccp_alphas:
        tree = DecisionTreeClassifier(random_state=42, ccp_alpha=alpha).fit(X_scaled, labels)
        preds = tree.predict(X_scaled)
        fidelity = tree.score(X_scaled, labels)
        leaves = tree.get_n_leaves()
        depth = tree.get_depth()
        classes = np.unique(preds)
        print(f"alpha={alpha:.5f}: depth={depth}, leaves={leaves}, fidelity={fidelity:.1%}, classes={classes}")

    print("\n--- Exploring max_leaf_nodes ---")
    for max_leaves in [3, 4, 5, 6]:
        tree = DecisionTreeClassifier(random_state=42, max_leaf_nodes=max_leaves).fit(X_scaled, labels)
        preds = tree.predict(X_scaled)
        fidelity = tree.score(X_scaled, labels)
        depth = tree.get_depth()
        classes = np.unique(preds)
        print(f"max_leaves={max_leaves}: depth={depth}, fidelity={fidelity:.1%}, classes={classes}")
        if len(classes) == 4:
            print(export_text(tree, feature_names=features))

    print("\n=======================================================")
    print("=== ONE-VERSUS-REST (OvR) TREES FOR EACH CLUSTER ===")
    print("=======================================================")
    for k in range(4):
        y_binary = (labels == k).astype(int)
        # Tree with depth 2 or max 2 leaves
        tree_ovr = DecisionTreeClassifier(max_depth=2, random_state=42).fit(X_scaled, y_binary)
        fidelity_ovr = tree_ovr.score(X_scaled, y_binary)
        print(f"\n--- Clúster {k} vs Resto (N={sum(y_binary)}) ---")
        print(f"Fidelidad binaria: {fidelity_ovr:.1%}")
        print(export_text(tree_ovr, feature_names=features))

if __name__ == "__main__":
    main()





