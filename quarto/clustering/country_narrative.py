"""Reproduce el hilo narrativo de Colombia para la presentación de clustering.

El script usa exclusivamente ``data/Country-data.csv`` para los resultados de
países. Los ejemplos geométricos de GMM y DBSCAN son simulaciones deterministas.

Uso, desde la raíz del repositorio::

    python quarto/clustering/country_narrative.py --all
    python quarto/clustering/country_narrative.py --figure pca
    python quarto/clustering/country_narrative.py --metrics

Las figuras y ``country_narrative_metrics.csv`` se escriben en
``quarto/clustering/assets/generated``. Todos los modelos usan semilla 42.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
from matplotlib.patches import Ellipse
from sklearn.cluster import DBSCAN, KMeans
from sklearn.datasets import make_moons
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances, silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

SEED = 42
ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "Country-data.csv"
OUTPUT = ROOT / "assets" / "generated"

BLUE = "#003576"
TEAL = "#00A6A6"
ORANGE = "#F28E2B"
RED = "#D1495B"
PURPLE = "#7B2CBF"
GREEN = "#59A14F"
GRAY = "#94A3B8"
DARK = "#0F172A"
COLORS = [BLUE, ORANGE, TEAL, RED, PURPLE, GREEN, "#EDC948"]

COUNTRY_COL = "country"
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
TWO_FEATURES = ["gdpp", "child_mort"]
HEALTH_FEATURES = ["child_mort", "health", "life_expec", "total_fer"]
MACRO_FEATURES = ["exports", "imports", "income", "inflation", "gdpp"]

DISPLAY_NAMES = {
    "St. Vincent and the Grenadines": "San Vicente y las Granadinas",
    "Dominican Republic": "Rep. Dominicana",
    "Cape Verde": "Cabo Verde",
    "Iran": "Irán",
    "Slovenia": "Eslovenia",
    "Turkey": "Turquía",
    "Ukraine": "Ucrania",
}


def style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#CBD5E1",
            "axes.labelcolor": "#1E293B",
            "axes.titlecolor": BLUE,
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "grid.color": "#E2E8F0",
            "grid.alpha": 0.8,
        }
    )


def load_countries() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"No existe {DATA_PATH}. El dataset debe permanecer versionado con el script."
        )
    data = pd.read_csv(DATA_PATH)
    expected = [COUNTRY_COL, *FEATURES]
    if list(data.columns) != expected:
        raise ValueError(f"Columnas inesperadas: {list(data.columns)}; se esperaba {expected}")
    if data[COUNTRY_COL].duplicated().any() or data[FEATURES].isna().any().any():
        raise ValueError("El dataset cambió: hay países duplicados o datos faltantes.")
    if (data[COUNTRY_COL].str.casefold() == "colombia").sum() != 1:
        raise ValueError("Debe existir exactamente una fila para Colombia.")
    return data


def colombia_index(data: pd.DataFrame) -> int:
    return int(np.flatnonzero(data[COUNTRY_COL].str.casefold() == "colombia")[0])


def shown(name: str) -> str:
    return DISPLAY_NAMES.get(name, name)


def matrix(data: pd.DataFrame, features: list[str], scale: bool = True) -> np.ndarray:
    values = data[features].to_numpy(dtype=float)
    return StandardScaler().fit_transform(values) if scale else values


def log_standardized_matrix(data: pd.DataFrame, features: list[str]) -> np.ndarray:
    """Aplica log10 y luego estandariza variables estrictamente positivas."""
    values = data[features].to_numpy(dtype=float)
    if np.any(values <= 0):
        raise ValueError(f"La transformación log requiere valores positivos: {features}")
    return StandardScaler().fit_transform(np.log10(values))


def nearest_from_matrix(
    data: pd.DataFrame, values: np.ndarray, *, n: int = 5
) -> list[tuple[str, float]]:
    ci = colombia_index(data)
    distances = pairwise_distances(values[[ci]], values)[0]
    order = [index for index in np.argsort(distances) if index != ci]
    return [(str(data.loc[index, COUNTRY_COL]), float(distances[index])) for index in order[:n]]


def nearest(
    data: pd.DataFrame, features: list[str], *, scale: bool = True, n: int = 5
) -> list[tuple[str, float]]:
    return nearest_from_matrix(data, matrix(data, features, scale), n=n)


def country_models(data: pd.DataFrame) -> dict[str, object]:
    x = matrix(data, FEATURES)
    pca = PCA(n_components=2, random_state=SEED).fit(x)
    z = pca.transform(x)
    kmeans = KMeans(n_clusters=4, n_init=30, random_state=SEED).fit(x)
    gmm = GaussianMixture(
        n_components=4,
        covariance_type="full",
        n_init=20,
        reg_covar=1e-4,
        random_state=SEED,
    ).fit(x)
    return {"x": x, "pca": pca, "z": z, "kmeans": kmeans, "gmm": gmm}


def save(fig: plt.Figure, name: str) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT / f"{name}.png", dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[ok] {name}.png")


def annotate_neighbors(
    ax: plt.Axes,
    coordinates: np.ndarray,
    data: pd.DataFrame,
    neighbor_names: list[str],
) -> None:
    ci = colombia_index(data)
    ax.scatter(*coordinates[ci], s=260, marker="*", c=RED, edgecolor="white", lw=1.2, zorder=5)
    ax.annotate("Colombia", coordinates[ci], xytext=(8, 9), textcoords="offset points", weight="bold")
    for rank, name in enumerate(neighbor_names, start=1):
        idx = int(data.index[data[COUNTRY_COL] == name][0])
        ax.plot(
            [coordinates[ci, 0], coordinates[idx, 0]],
            [coordinates[ci, 1], coordinates[idx, 1]],
            color=RED if rank == 1 else "#CBD5E1",
            lw=1.8 if rank == 1 else 0.9,
            zorder=1,
        )
        ax.scatter(*coordinates[idx], s=52, c=ORANGE if rank == 1 else BLUE, zorder=4)
    ranking = "Vecinos de Colombia\n" + "\n".join(
        f"{rank}. {shown(name)}" for rank, name in enumerate(neighbor_names, start=1)
    )
    ax.text(
        0.98,
        0.96,
        ranking,
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=8.5,
        linespacing=1.35,
        bbox={"boxstyle": "round,pad=0.45", "facecolor": "white", "edgecolor": "#CBD5E1", "alpha": 0.94},
    )


def two_variables() -> None:
    data = load_countries()
    raw = matrix(data, TWO_FEATURES, scale=False)
    transformed = log_standardized_matrix(data, TWO_FEATURES)
    raw_neighbors = [name for name, _ in nearest(data, TWO_FEATURES, scale=False)]
    transformed_neighbors = [name for name, _ in nearest_from_matrix(data, transformed)]

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4))
    for ax, values in zip(axes, (raw, transformed)):
        ax.scatter(values[:, 0], values[:, 1], s=24, c=GRAY, alpha=0.58)
        ax.grid(True)
    annotate_neighbors(axes[0], raw, data, raw_neighbors[:3])
    annotate_neighbors(axes[1], transformed, data, transformed_neighbors[:5])
    axes[0].set(
        xlabel="PIB per cápita (USD)",
        ylabel="Mortalidad infantil por 1.000",
    )
    axes[1].set(
        xlabel="log10(PIB per cápita), estandarizado",
        ylabel="log10(mortalidad infantil), estandarizado",
    )
    axes[1].axhline(0, color="#CBD5E1", lw=1)
    axes[1].axvline(0, color="#CBD5E1", lw=1)
    fig.tight_layout()
    save(fig, "countries_two_variables")


def pca_story() -> None:
    data = load_countries()
    models = country_models(data)
    pca = models["pca"]
    z = models["z"]
    ci = colombia_index(data)
    distances = pairwise_distances(z[[ci]], z)[0]
    order = [index for index in np.argsort(distances) if index != ci]
    neighbors = [str(data.loc[index, COUNTRY_COL]) for index in order[:6]]

    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    ax.scatter(z[:, 0], z[:, 1], s=26, c=GRAY, alpha=0.62)
    annotate_neighbors(ax, z, data, neighbors)
    ax.set(
        xlabel=f"PC1 ({pca.explained_variance_ratio_[0]:.1%})",
        ylabel=f"PC2 ({pca.explained_variance_ratio_[1]:.1%})",
    )
    ax.grid(True)
    fig.tight_layout()
    save(fig, "countries_pca_neighborhood")

    loadings = pd.DataFrame(pca.components_, index=["PC1", "PC2"], columns=FEATURES)
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.1), gridspec_kw={"width_ratios": [1, 2.4]})
    explained = [*pca.explained_variance_ratio_, 1 - pca.explained_variance_ratio_.sum()]
    axes[0].bar(["PC1", "PC2", "No visible"], explained, color=[BLUE, PURPLE, GRAY])
    axes[0].set(ylabel="Proporción", ylim=(0, 0.7))
    axes[0].grid(True, axis="y")
    for index, value in enumerate(explained):
        axes[0].text(index, value + 0.025, f"{value:.1%}", ha="center", weight="bold")
    image = axes[1].imshow(loadings, cmap="RdBu_r", vmin=-0.7, vmax=0.7, aspect="auto")
    axes[1].set_xticks(range(len(FEATURES)), FEATURES, rotation=32, ha="right")
    axes[1].set_yticks([0, 1], ["PC1", "PC2"])
    for row in range(2):
        for column in range(len(FEATURES)):
            value = loadings.iloc[row, column]
            axes[1].text(column, row, f"{value:.2f}", ha="center", va="center", fontsize=8)
    fig.colorbar(image, ax=axes[1], shrink=0.75, label="Carga")
    fig.tight_layout()
    save(fig, "countries_pca_loadings")


def kmeans_story() -> None:
    data = load_countries()
    models = country_models(data)
    x, z, pca = models["x"], models["z"], models["pca"]
    kmeans = models["kmeans"]
    ci = colombia_index(data)

    ks = list(range(2, 9))
    fitted = [KMeans(k, n_init=30, random_state=SEED).fit(x) for k in ks]
    inertia = [model.inertia_ for model in fitted]
    silhouette = [silhouette_score(x, model.labels_) for model in fitted]
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.8))
    axes[0].plot(ks, inertia, "o-", color=BLUE, lw=2.5)
    axes[0].set(xlabel="Número de grupos (K)", ylabel="Inercia")
    axes[1].plot(ks, silhouette, "o-", color=TEAL, lw=2.5)
    axes[1].axvline(4, color=RED, ls="--", label=f"K=4 · {silhouette[2]:.3f}")
    axes[1].set(xlabel="Número de grupos (K)", ylabel="Silueta")
    axes[1].legend(frameon=False)
    for ax in axes:
        ax.grid(True)
    fig.tight_layout()
    save(fig, "countries_k_selection")

    projected_centers = pca.transform(kmeans.cluster_centers_)
    fig, ax = plt.subplots(figsize=(9.2, 5.1))
    ax.scatter(z[:, 0], z[:, 1], c=kmeans.labels_, cmap=ListedColormap(COLORS[:4]), s=30, alpha=0.72)
    ax.scatter(projected_centers[:, 0], projected_centers[:, 1], marker="X", c=COLORS[:4], s=230, edgecolor="white", lw=1.3)
    ax.scatter(*z[ci], marker="*", s=300, c=RED, edgecolor="white", lw=1.4, zorder=6)
    label = int(kmeans.labels_[ci])
    size = int(np.sum(kmeans.labels_ == label))
    ax.annotate(f"Colombia · grupo de {size}", z[ci], xytext=(9, 11), textcoords="offset points", weight="bold")
    ax.set(
        xlabel="PC1",
        ylabel="PC2",
    )
    ax.grid(True)
    fig.tight_layout()
    save(fig, "countries_kmeans_pca")


def draw_covariance(ax: plt.Axes, mean: np.ndarray, covariance: np.ndarray, color: str) -> None:
    values, vectors = np.linalg.eigh(covariance)
    order = values.argsort()[::-1]
    values, vectors = values[order], vectors[:, order]
    angle = np.degrees(np.arctan2(*vectors[:, 0][::-1]))
    for scale, alpha in ((2, 0.18), (4, 0.08)):
        width, height = scale * np.sqrt(values)
        ax.add_patch(Ellipse(mean, width, height, angle=angle, color=color, alpha=alpha))


def gmm_story() -> None:
    data = load_countries()
    models = country_models(data)
    probabilities = models["gmm"].predict_proba(models["x"])
    uncertainty = 1 - probabilities.max(axis=1)
    ci = colombia_index(data)
    selected = list(np.argsort(uncertainty)[-6:][::-1]) + [ci]
    shown_probs = probabilities[selected]
    labels = [shown(str(data.loc[index, COUNTRY_COL])) for index in selected]

    fig, ax = plt.subplots(figsize=(9.6, 4.7))
    left = np.zeros(len(selected))
    for component in range(4):
        ax.barh(labels, shown_probs[:, component], left=left, color=COLORS[component], label=f"Componente {component + 1}")
        left += shown_probs[:, component]
    ax.invert_yaxis()
    ax.set(xlabel="Responsabilidad posterior", xlim=(0, 1))
    ax.legend(frameon=False, ncol=4, loc="lower center", bbox_to_anchor=(0.5, -0.30))
    ax.grid(True, axis="x")
    fig.tight_layout()
    save(fig, "countries_gmm_uncertainty")

    rng = np.random.default_rng(SEED)
    anisotropic = np.vstack(
        [
            rng.multivariate_normal([-1.4, -0.2], [[1.05, 0.82], [0.82, 0.78]], 190),
            rng.multivariate_normal([1.3, -0.1], [[1.00, -0.76], [-0.76, 0.72]], 190),
            rng.multivariate_normal([0.0, 2.0], [[0.22, 0.02], [0.02, 0.62]], 120),
        ]
    )
    km = KMeans(3, n_init=30, random_state=SEED).fit(anisotropic)
    gm = GaussianMixture(3, covariance_type="full", n_init=20, random_state=SEED).fit(anisotropic)
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.2))
    axes[0].scatter(anisotropic[:, 0], anisotropic[:, 1], c=km.labels_, cmap=ListedColormap(COLORS[:3]), s=20, alpha=0.68)
    axes[0].scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], c=COLORS[:3], marker="X", s=190, edgecolor="white")
    gm_labels = gm.predict(anisotropic)
    axes[1].scatter(anisotropic[:, 0], anisotropic[:, 1], c=gm_labels, cmap=ListedColormap(COLORS[:3]), s=20, alpha=0.68)
    for component in range(3):
        draw_covariance(axes[1], gm.means_[component], gm.covariances_[component], COLORS[component])
    for ax in axes:
        ax.grid(True)
        ax.set(xticks=[], yticks=[])
    fig.tight_layout()
    save(fig, "kmeans_vs_gmm_anisotropy")


def dbscan_story() -> None:
    x, _ = make_moons(n_samples=520, noise=0.075, random_state=SEED)
    rng = np.random.default_rng(SEED)
    noise = rng.uniform(low=[-1.3, -0.7], high=[2.3, 1.3], size=(35, 2))
    x = np.vstack([x, noise])
    gmm = GaussianMixture(2, covariance_type="full", n_init=20, random_state=SEED).fit(x)
    dbscan = DBSCAN(eps=0.16, min_samples=8).fit(x)

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.2))
    axes[0].scatter(x[:, 0], x[:, 1], c=gmm.predict(x), cmap=ListedColormap(COLORS[:2]), s=21, alpha=0.75)
    for component in range(2):
        draw_covariance(axes[0], gmm.means_[component], gmm.covariances_[component], COLORS[component])
    labels = dbscan.labels_
    clustered = labels >= 0
    axes[1].scatter(x[clustered, 0], x[clustered, 1], c=labels[clustered], cmap=ListedColormap(COLORS[:4]), s=21, alpha=0.75)
    axes[1].scatter(x[~clustered, 0], x[~clustered, 1], c="#475569", marker="x", s=30, label="Ruido")
    axes[1].legend(frameon=False)
    for ax in axes:
        ax.grid(True)
        ax.set(xticks=[], yticks=[])
    fig.tight_layout()
    save(fig, "gmm_vs_dbscan_shapes")


def metrics() -> pd.DataFrame:
    data = load_countries()
    models = country_models(data)
    ci = colombia_index(data)
    z = models["z"]
    pca_distances = pairwise_distances(z[[ci]], z)[0]
    pca_order = [index for index in np.argsort(pca_distances) if index != ci]
    kmeans = models["kmeans"]
    gmm_probs = models["gmm"].predict_proba(models["x"])[ci]

    records = []
    definitions = [
        ("PIB y mortalidad sin escalar", TWO_FEATURES, False),
        ("Salud y demografía", HEALTH_FEATURES, True),
        ("Macroeconomía y comercio", MACRO_FEATURES, True),
        ("Nueve variables estandarizadas", FEATURES, True),
    ]
    for question, features, scaled in definitions:
        name, distance = nearest(data, features, scale=scaled, n=1)[0]
        records.append(
            {
                "pregunta": question,
                "respuesta": shown(name),
                "distancia": distance,
                "detalle": ", ".join(features),
            }
        )
    log_name, log_distance = nearest_from_matrix(
        data, log_standardized_matrix(data, TWO_FEATURES), n=1
    )[0]
    records.insert(
        1,
        {
            "pregunta": "PIB y mortalidad con log + estándar",
            "respuesta": shown(log_name),
            "distancia": log_distance,
            "detalle": "StandardScaler(log10(gdpp), log10(child_mort))",
        },
    )
    pca = models["pca"]
    records.append(
        {
            "pregunta": "PCA 2D de nueve variables",
            "respuesta": shown(str(data.loc[pca_order[0], COUNTRY_COL])),
            "distancia": float(pca_distances[pca_order[0]]),
            "detalle": f"varianza explicada={pca.explained_variance_ratio_.sum():.6f}",
        }
    )
    records.append(
        {
            "pregunta": "K-Means K=4",
            "respuesta": f"Grupo de {int(np.sum(kmeans.labels_ == kmeans.labels_[ci]))} países",
            "distancia": float(np.min(kmeans.transform(models["x"][[ci]]))),
            "detalle": "ajustado en las nueve variables; PCA solo visualiza",
        }
    )
    records.append(
        {
            "pregunta": "GMM K=4",
            "respuesta": f"responsabilidad máxima={gmm_probs.max():.6f}",
            "distancia": float(1 - gmm_probs.max()),
            "detalle": "covarianza full; ajustado en las nueve variables",
        }
    )
    result = pd.DataFrame(records)

    expected = {
        "PIB y mortalidad sin escalar": "San Vicente y las Granadinas",
        "PIB y mortalidad con log + estándar": "Irán",
        "Salud y demografía": "Barbados",
        "Macroeconomía y comercio": "China",
        "Nueve variables estandarizadas": "Turquía",
        "PCA 2D de nueve variables": "Argentina",
        "K-Means K=4": "Grupo de 88 países",
    }
    actual = result.set_index("pregunta")["respuesta"].to_dict()
    mismatches = [f"{key}: {actual.get(key)!r} != {value!r}" for key, value in expected.items() if actual.get(key) != value]
    if mismatches:
        raise AssertionError("Cambió el dataset o el pipeline:\n" + "\n".join(mismatches))
    return result


def write_metrics() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    path = OUTPUT / "country_narrative_metrics.csv"
    metrics().to_csv(path, index=False)
    print(f"[ok] {path.name}")


FIGURES = {
    "two_variables": two_variables,
    "pca": pca_story,
    "kmeans": kmeans_story,
    "gmm": gmm_story,
    "dbscan": dbscan_story,
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Genera figuras y métricas.")
    group.add_argument("--metrics", action="store_true", help="Valida y guarda resultados numéricos.")
    group.add_argument("--figure", choices=sorted(FIGURES), help="Genera una sección de figuras.")
    args = parser.parse_args()
    style()
    if args.metrics:
        write_metrics()
        return
    selected = FIGURES.values() if args.all else [FIGURES[args.figure]]
    for function in selected:
        function()
    write_metrics()


if __name__ == "__main__":
    main()
