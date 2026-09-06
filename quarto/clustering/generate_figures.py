"""Genera las figuras reproducibles de la presentacion de clustering.

Dependencias: numpy, pandas, matplotlib, scipy y scikit-learn. La captura de
interactividades requiere además Playwright y Google Chrome o Microsoft Edge.

Uso desde ``quarto/clustering``::

    python generate_figures.py --all
    python generate_figures.py --figure k_selection
    python generate_figures.py --figure colombia_similarity

Las figuras se guardan en ``assets/generated``. Todas las simulaciones usan
``random_state=42``. El caso de paises usa una copia local en ``data/`` cuando
esta disponible; de lo contrario descarga el CSV oficial y lo deja en cache.
"""

from __future__ import annotations

import argparse
import os
import shutil
import warnings
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlretrieve

import matplotlib

matplotlib.use("Agg")
os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
from matplotlib.patches import Circle, Ellipse
from scipy.spatial.distance import pdist
from sklearn.cluster import DBSCAN, KMeans, MiniBatchKMeans
from sklearn.datasets import load_digits, load_sample_image, make_blobs, make_moons
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.metrics import pairwise_distances, silhouette_samples, silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SEED = 42
ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "assets" / "generated"
DATA_DIR = ROOT / "data"
COUNTRY_URL = (
    "https://raw.githubusercontent.com/oscar-bustos/"
    "javeriana-analitica/main/countrydata/Country-data.csv"
)
INTERACTIVE_URLS = {
    "interactive_pca": (
        "https://oscar-bustos.github.io/javeriana-tallerml/"
        "reduccion_dimension/pca.html"
    ),
    "interactive_kmeans": (
        "https://oscar-bustos.github.io/javeriana-tallerml/"
        "clustering/kmeans.html"
    ),
}
BLUE = "#003576"
TEAL = "#00A6A6"
ORANGE = "#F28E2B"
RED = "#D1495B"
PURPLE = "#7B2CBF"
COLORS = [BLUE, ORANGE, TEAL, RED, PURPLE, "#59A14F", "#EDC948"]


def _style() -> None:
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


def _save(fig: plt.Figure, name: str) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT / f"{name}.png", dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[ok] {name}.png")


def distance_concentration() -> None:
    """Muestra como las distancias pierden contraste al crecer la dimension."""
    rng = np.random.default_rng(SEED)
    dimensions = np.array([2, 5, 10, 20, 50, 100, 200])
    cv, contrast = [], []
    distributions = {}
    for dimension in dimensions:
        x = rng.uniform(size=(500, dimension))
        distances = pdist(x)
        cv.append(distances.std() / distances.mean())
        contrast.append((np.percentile(distances, 95) - np.percentile(distances, 5)) / distances.mean())
        if dimension in (2, 20, 200):
            distributions[dimension] = distances / distances.mean()

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.8))
    axes[0].plot(dimensions, cv, "o-", color=BLUE, lw=2.5, label="Variacion relativa")
    axes[0].plot(dimensions, contrast, "s--", color=ORANGE, lw=2, label="Contraste P95-P05")
    axes[0].set(xlabel="Numero de dimensiones", ylabel="Contraste normalizado", xscale="log")
    axes[0].set_title("Las distancias se concentran")
    axes[0].grid(True)
    axes[0].legend(frameon=False)
    for dimension, color in zip((2, 20, 200), (BLUE, ORANGE, TEAL)):
        axes[1].hist(
            distributions[dimension], bins=35, density=True, alpha=0.42,
            label=f"d={dimension}", color=color,
        )
    axes[1].axvline(1, color="#475569", ls=":")
    axes[1].set(xlabel="Distancia / distancia media", ylabel="Densidad")
    axes[1].set_title("En alta dimension, casi todo queda igual de lejos")
    axes[1].legend(frameon=False)
    _save(fig, "distance_concentration")


def pca_digits() -> None:
    """Combina varianza explicada y reconstruccion de digitos con PCA."""
    digits = load_digits()
    x = digits.data
    full = PCA(random_state=SEED).fit(x)
    cumulative = np.cumsum(full.explained_variance_ratio_)
    choices = [5, 15, 30]
    sample_idx = 42

    fig = plt.figure(figsize=(11, 4.3))
    grid = fig.add_gridspec(2, 4, width_ratios=[1.5, 1, 1, 1])
    ax = fig.add_subplot(grid[:, 0])
    ax.plot(np.arange(1, len(cumulative) + 1), cumulative, color=BLUE, lw=2.5)
    ax.axhline(0.95, color=RED, ls="--", label="95%")
    d95 = int(np.argmax(cumulative >= 0.95) + 1)
    ax.axvline(d95, color=RED, ls=":")
    ax.annotate(f"{d95} componentes", (d95, 0.95), xytext=(d95 + 7, 0.78),
                arrowprops={"arrowstyle": "->", "color": RED})
    ax.set(xlabel="Componentes", ylabel="Varianza explicada acumulada", ylim=(0, 1.02))
    ax.set_title("PCA conserva informacion, no etiquetas")
    ax.grid(True)

    images = [("Original (64D)", x[sample_idx].reshape(8, 8))]
    for n_components in choices:
        model = PCA(n_components=n_components, random_state=SEED)
        reconstructed = model.inverse_transform(model.fit_transform(x[[sample_idx]] if False else x))[sample_idx]
        images.append((f"{n_components}D", reconstructed.reshape(8, 8)))
    sub = grid[:, 1:].subgridspec(1, 4, wspace=0.08)
    for col, (title, image) in enumerate(images):
        image_ax = fig.add_subplot(sub[0, col])
        image_ax.imshow(image, cmap="gray_r", vmin=0, vmax=16)
        image_ax.set_title(title, fontsize=10)
        image_ax.axis("off")
    _save(fig, "pca_digits")


def scaling_effect() -> None:
    """Ilustra que una variable de gran magnitud domina la distancia euclidiana."""
    rng = np.random.default_rng(SEED)
    age = np.r_[rng.normal(28, 4, 70), rng.normal(51, 5, 70)]
    income = np.r_[rng.normal(45_000, 18_000, 70), rng.normal(62_000, 18_000, 70)]
    x = np.column_stack([age, income])
    raw = KMeans(n_clusters=2, n_init=20, random_state=SEED).fit_predict(x)
    scaled_x = StandardScaler().fit_transform(x)
    scaled = KMeans(n_clusters=2, n_init=20, random_state=SEED).fit_predict(scaled_x)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].scatter(age, income / 1000, c=raw, cmap=ListedColormap(COLORS[:2]), s=26)
    axes[0].set_title("Sin escalar: ingreso decide casi todo")
    axes[0].set(xlabel="Edad", ylabel="Ingreso (miles)")
    axes[1].scatter(scaled_x[:, 0], scaled_x[:, 1], c=scaled,
                    cmap=ListedColormap(COLORS[:2]), s=26)
    axes[1].set_title("Estandarizado: ambas variables cuentan")
    axes[1].set(xlabel="Edad estandarizada", ylabel="Ingreso estandarizado")
    for ax in axes:
        ax.grid(True)
    _save(fig, "scaling_effect")


def kmeans_iterations() -> None:
    """Implementa cuatro pasos de Lloyd para mostrar asignacion y actualizacion."""
    x, _ = make_blobs(n_samples=360, centers=[(-4, -1), (0, 3), (4, -0.5)],
                      cluster_std=[1.0, 0.9, 1.1], random_state=SEED)
    centroids = np.array([[-1.0, -2.8], [0.8, -1.8], [2.8, 3.8]])
    states = []
    for _ in range(4):
        distances = ((x[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)
        labels = distances.argmin(axis=1)
        states.append((centroids.copy(), labels.copy()))
        centroids = np.vstack([x[labels == j].mean(axis=0) for j in range(3)])

    fig, axes = plt.subplots(1, 4, figsize=(12, 3.2), sharex=True, sharey=True)
    for idx, (ax, (centers, labels)) in enumerate(zip(axes, states)):
        ax.scatter(x[:, 0], x[:, 1], c=labels, cmap=ListedColormap(COLORS[:3]), s=9, alpha=0.65)
        ax.scatter(centers[:, 0], centers[:, 1], marker="X", s=160, c="white",
                   edgecolor="#111827", linewidth=1.5)
        ax.set_title("Inicio" if idx == 0 else f"Iteracion {idx}")
        ax.grid(True)
    fig.suptitle("K-Means alterna asignar puntos y mover centroides", color=BLUE,
                 fontsize=15, fontweight="bold")
    _save(fig, "kmeans_iterations")


def k_selection() -> None:
    """Genera curvas de codo, silueta media y diagrama de silueta."""
    x, _ = make_blobs(n_samples=700, centers=4, cluster_std=[0.8, 1.0, 0.65, 0.9],
                      random_state=SEED)
    ks = range(2, 9)
    inertias, scores, models = [], [], {}
    for k in ks:
        model = KMeans(n_clusters=k, n_init=20, random_state=SEED).fit(x)
        models[k] = model
        inertias.append(model.inertia_)
        scores.append(silhouette_score(x, model.labels_))
    best_k = list(ks)[int(np.argmax(scores))]
    model = models[best_k]
    values = silhouette_samples(x, model.labels_)

    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))
    axes[0].plot(list(ks), inertias, "o-", color=BLUE, lw=2.5)
    axes[0].set(title="Codo", xlabel="k", ylabel="Inercia")
    axes[1].plot(list(ks), scores, "o-", color=ORANGE, lw=2.5)
    axes[1].axvline(best_k, color=RED, ls="--")
    axes[1].set(title=f"Silueta media: k={best_k}", xlabel="k", ylabel="Silueta media", ylim=(0, 1))
    y_lower = 10
    for cluster in range(best_k):
        cluster_values = np.sort(values[model.labels_ == cluster])
        y_upper = y_lower + len(cluster_values)
        axes[2].fill_betweenx(np.arange(y_lower, y_upper), 0, cluster_values,
                              color=COLORS[cluster], alpha=0.8)
        y_lower = y_upper + 10
    axes[2].axvline(scores[best_k - 2], color=RED, ls="--")
    axes[2].set(title="Distribución por clúster", xlabel="Coeficiente de silueta",
                ylabel="Instancias ordenadas", xlim=(-0.2, 1), yticks=[])
    for ax in axes[:2]:
        ax.grid(True)
    _save(fig, "k_selection")


def algorithm_comparison() -> None:
    """Compara K-Means, DBSCAN y GMM en cuatro geometrías."""
    rng = np.random.default_rng(SEED)
    blobs, _ = make_blobs(n_samples=450, centers=3, cluster_std=0.7, random_state=SEED)
    varied, _ = make_blobs(n_samples=450, centers=3, cluster_std=[0.35, 1.4, 0.6], random_state=SEED)
    anisotropic, _ = make_blobs(n_samples=450, centers=3, random_state=SEED)
    anisotropic = anisotropic @ np.array([[0.65, -0.65], [-0.25, 0.85]])
    moons, _ = make_moons(n_samples=450, noise=0.055, random_state=SEED)
    datasets = [("Esfericos", blobs), ("Densidad variable", varied),
                ("Anisotropicos", anisotropic), ("Lunas", moons)]
    algorithms = [
        ("K-Means", lambda x: KMeans(3, n_init=20, random_state=SEED).fit_predict(x)),
        ("DBSCAN", lambda x: DBSCAN(eps=0.28, min_samples=8).fit_predict(StandardScaler().fit_transform(x))),
        ("GMM", lambda x: GaussianMixture(3, n_init=10, random_state=SEED).fit_predict(x)),
    ]
    fig, axes = plt.subplots(4, 4, figsize=(10.5, 9.2))
    for row, (dataset_name, x) in enumerate(datasets):
        axes[row, 0].scatter(x[:, 0], x[:, 1], s=7, color="#64748B")
        axes[row, 0].set_ylabel(dataset_name, fontweight="bold")
        for col, (_, fit_predict) in enumerate(algorithms, start=1):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                labels = fit_predict(x)
            axes[row, col].scatter(x[:, 0], x[:, 1], s=7, c=labels,
                                   cmap=ListedColormap(COLORS), vmin=-1, vmax=5)
        for ax in axes[row]:
            ax.set(xticks=[], yticks=[])
    for col, title in enumerate(["Datos", "K-Means", "DBSCAN", "GMM"]):
        axes[0, col].set_title(title)
    fig.suptitle("La geometria de los datos determina el algoritmo", color=BLUE,
                 fontsize=15, fontweight="bold")
    _save(fig, "algorithm_comparison")


def dbscan_roles() -> None:
    """Distingue puntos núcleo, frontera y ruido en DBSCAN."""
    x, _ = make_moons(n_samples=420, noise=0.075, random_state=SEED)
    x = StandardScaler().fit_transform(x)
    eps, min_samples = 0.22, 8
    model = DBSCAN(eps=eps, min_samples=min_samples).fit(x)
    core = np.zeros(len(x), dtype=bool)
    core[model.core_sample_indices_] = True
    noise = model.labels_ == -1
    border = ~core & ~noise

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].scatter(x[core, 0], x[core, 1], c=BLUE, s=28, label="Nucleo")
    axes[0].scatter(x[border, 0], x[border, 1], c=ORANGE, s=28, label="Frontera")
    axes[0].scatter(x[noise, 0], x[noise, 1], c=RED, marker="x", s=38, label="Ruido")
    chosen = model.core_sample_indices_[len(model.core_sample_indices_) // 2]
    axes[0].add_patch(Circle(x[chosen], eps, fill=False, lw=2, ls="--", color=RED))
    axes[0].set_title(r"$eps$ define la vecindad local")
    axes[0].legend(frameon=False)
    axes[1].scatter(x[:, 0], x[:, 1], c=model.labels_, cmap=ListedColormap(COLORS), s=24)
    axes[1].scatter(x[noise, 0], x[noise, 1], c=RED, marker="x", s=38)
    axes[1].set_title("La conectividad forma clústeres no convexos")
    for ax in axes:
        ax.set(xticks=[], yticks=[])
    _save(fig, "dbscan_roles")


def _draw_gmm_ellipses(ax: plt.Axes, model: GaussianMixture) -> None:
    for mean, covariance, weight, color in zip(model.means_, model.covariances_, model.weights_, COLORS):
        values, vectors = np.linalg.eigh(covariance)
        order = values.argsort()[::-1]
        values, vectors = values[order], vectors[:, order]
        angle = np.degrees(np.arctan2(vectors[1, 0], vectors[0, 0]))
        for scale in (1, 2):
            width, height = 2 * scale * np.sqrt(values)
            ax.add_patch(Ellipse(mean, width, height, angle=angle, fill=False,
                                 color=color, lw=1.5, alpha=0.85 * weight + 0.15))


def gmm_density() -> None:
    """Visualiza responsabilidades, densidad, anomalías y selección AIC/BIC."""
    x, _ = make_blobs(n_samples=750, centers=3, cluster_std=[0.7, 1.0, 0.55], random_state=SEED)
    transform = np.array([[0.75, -0.55], [0.35, 1.15]])
    x = x @ transform
    model = GaussianMixture(3, covariance_type="full", n_init=10, random_state=SEED).fit(x)
    responsibilities = model.predict_proba(x)
    density = model.score_samples(x)
    threshold = np.percentile(density, 2)
    anomalies = density < threshold
    ks = range(1, 8)
    models = [GaussianMixture(k, n_init=5, random_state=SEED).fit(x) for k in ks]

    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))
    rgb = responsibilities @ np.array([matplotlib.colors.to_rgb(c) for c in COLORS[:3]])
    axes[0].scatter(x[:, 0], x[:, 1], c=rgb, s=12)
    _draw_gmm_ellipses(axes[0], model)
    axes[0].set_title("Responsabilidades suaves", fontsize=11)
    scatter = axes[1].scatter(x[:, 0], x[:, 1], c=density, cmap="viridis", s=12)
    axes[1].scatter(x[anomalies, 0], x[anomalies, 1], facecolors="none", edgecolors=RED, s=60, lw=1.5)
    axes[1].set_title("Baja densidad = posible anomalía", fontsize=11)
    fig.colorbar(scatter, ax=axes[1], fraction=0.046, label="log densidad")
    axes[2].plot(list(ks), [m.bic(x) for m in models], "o-", color=BLUE, label="BIC")
    axes[2].plot(list(ks), [m.aic(x) for m in models], "s--", color=ORANGE, label="AIC")
    axes[2].set_title("AIC/BIC penalizan complejidad", fontsize=11)
    axes[2].set(xlabel="Componentes", ylabel="Criterio")
    axes[2].grid(True)
    axes[2].legend(frameon=False)
    for ax in axes[:2]:
        ax.set(xticks=[], yticks=[])
    _save(fig, "gmm_density")


def minibatch_tradeoff() -> None:
    """Compara inercia y un proxy reproducible del trabajo computacional."""
    x, _ = make_blobs(n_samples=30_000, centers=8, n_features=12, random_state=SEED)
    ks = [4, 6, 8, 10, 12]
    results = {"K-Means": ([], []), "MiniBatch": ([], [])}
    for k in ks:
        for name, estimator in (
            ("K-Means", KMeans(k, n_init=5, random_state=SEED)),
            ("MiniBatch", MiniBatchKMeans(k, n_init=5, batch_size=1024, random_state=SEED)),
        ):
            estimator.fit(x)
            results[name][0].append(estimator.inertia_)
            if name == "K-Means":
                work = len(x) * k * estimator.n_iter_
            else:
                work = estimator.batch_size * k * estimator.n_steps_
            results[name][1].append(work)
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.6))
    for name, color in (("K-Means", BLUE), ("MiniBatch", ORANGE)):
        axes[0].plot(ks, results[name][0], "o-", color=color, label=name)
        axes[1].plot(ks, results[name][1], "o-", color=color, label=name)
    axes[0].set(title="Calidad: inercia", xlabel="k", ylabel="Inercia")
    axes[1].set(title="Costo: trabajo aproximado", xlabel="k",
                ylabel="Distancias evaluadas (proxy)", yscale="log")
    for ax in axes:
        ax.grid(True)
        ax.legend(frameon=False)
    _save(fig, "minibatch_tradeoff")


def image_segmentation() -> None:
    """Cuantiza los colores de una imagen mediante K-Means."""
    image = load_sample_image("china.jpg")
    pixels = image.reshape(-1, 3) / 255.0
    rng = np.random.default_rng(SEED)
    sample = pixels[rng.choice(len(pixels), 15_000, replace=False)]
    outputs = [("Original", image)]
    for k in (8, 3):
        model = MiniBatchKMeans(k, random_state=SEED, n_init=5, batch_size=2048).fit(sample)
        quantized = model.cluster_centers_[model.predict(pixels)].reshape(image.shape)
        outputs.append((f"{k} colores", quantized))
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.5))
    for ax, (title, output) in zip(axes, outputs):
        ax.imshow(output)
        ax.set_title(title)
        ax.axis("off")
    fig.suptitle("Clustering de píxeles comprime la paleta", color=BLUE,
                 fontsize=15, fontweight="bold")
    _save(fig, "image_segmentation")


def _load_countries() -> pd.DataFrame:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    cache = DATA_DIR / "Country-data.csv"
    if not cache.exists():
        print(f"[info] Descargando datos de paises en {cache}")
        try:
            urlretrieve(COUNTRY_URL, cache)
        except (URLError, OSError) as exc:
            raise RuntimeError(
                "No fue posible descargar Country-data.csv. Verifique la conexion "
                f"o copie el archivo manualmente en {cache}."
            ) from exc
    return pd.read_csv(cache)


def countries() -> None:
    """Genera selección de k, proyección PCA y perfiles del caso de países."""
    data = _load_countries()
    country_col = "country"
    features = [column for column in data.columns if column != country_col]
    pipeline = make_pipeline(SimpleImputer(strategy="median"), StandardScaler())
    x_scaled = pipeline.fit_transform(data[features])
    ks = range(2, 9)
    scores, models = [], {}
    for k in ks:
        model = KMeans(k, n_init=30, random_state=SEED).fit(x_scaled)
        models[k] = model
        scores.append(silhouette_score(x_scaled, model.labels_))
    best_k = list(ks)[int(np.argmax(scores))]
    model = models[best_k]
    projection = PCA(n_components=2, random_state=SEED).fit_transform(x_scaled)

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.2))
    axes[0].plot(list(ks), scores, "o-", color=BLUE, lw=2.5)
    axes[0].axvline(best_k, color=RED, ls="--")
    axes[0].set(title=f"Silueta favorece k={best_k}", xlabel="k", ylabel="Silueta media", ylim=(0, 1))
    axes[0].grid(True)
    axes[1].scatter(projection[:, 0], projection[:, 1], c=model.labels_,
                    cmap=ListedColormap(COLORS), s=30, alpha=0.8)
    colombia = data[country_col].astype(str).str.strip().str.casefold() == "colombia"
    if colombia.any():
        point = projection[np.flatnonzero(colombia)[0]]
        axes[1].scatter(*point, marker="*", s=260, c=RED, edgecolor="white", lw=1.2)
        axes[1].annotate("Colombia", point, xytext=(8, 10), textcoords="offset points", fontweight="bold")
    axes[1].set(title="PCA permite ver; K-Means usa todas las variables", xlabel="PC1", ylabel="PC2")
    axes[1].grid(True)
    _save(fig, "countries_pca")

    profiles = pd.DataFrame(model.cluster_centers_, columns=features)
    fig, ax = plt.subplots(figsize=(11, 4.3))
    x_axis = np.arange(len(features))
    for cluster, row in profiles.iterrows():
        ax.plot(x_axis, row, marker="o", lw=2.2, color=COLORS[cluster], label=f"Cluster {cluster}")
    ax.axhline(0, color="#64748B", lw=1)
    ax.set_xticks(x_axis, features, rotation=32, ha="right")
    ax.set_ylabel("Centroide estandarizado")
    ax.set_title("Los centroides convierten grupos en perfiles comparables")
    ax.grid(True, axis="y")
    ax.legend(frameon=False, ncol=min(best_k, 4))
    _save(fig, "countries_profiles")


def colombia_similarity() -> None:
    """Compara los vecinos de Colombia bajo distintas representaciones."""
    data = _load_countries()
    country_col = "country"
    all_features = [column for column in data.columns if column != country_col]
    health_features = ["child_mort", "health", "life_expec", "total_fer"]
    macro_features = ["exports", "imports", "income", "inflation", "gdpp"]
    country_names = data[country_col].astype(str).str.strip()
    colombia_matches = country_names.str.casefold() == "colombia"
    if colombia_matches.sum() != 1:
        raise ValueError("El dataset debe contener exactamente una fila para Colombia.")
    colombia_idx = int(np.flatnonzero(colombia_matches)[0])

    def nearest(features: list[str], standardize: bool = True) -> list[tuple[str, float]]:
        values = SimpleImputer(strategy="median").fit_transform(data[features])
        if standardize:
            values = StandardScaler().fit_transform(values)
        distances = pairwise_distances(values[[colombia_idx]], values)[0]
        order = np.argsort(distances)
        return [
            (country_names.iloc[index], float(distances[index]))
            for index in order
            if index != colombia_idx
        ]

    raw = nearest(all_features, standardize=False)
    standardized = nearest(all_features)
    health = nearest(health_features)
    macro = nearest(macro_features)

    values = SimpleImputer(strategy="median").fit_transform(data[all_features])
    scaled = StandardScaler().fit_transform(values)
    pca = PCA(n_components=2, random_state=SEED)
    projection = pca.fit_transform(scaled)
    pca_distances = pairwise_distances(projection[[colombia_idx]], projection)[0]
    pca_order = [index for index in np.argsort(pca_distances) if index != colombia_idx]
    pca_neighbor = country_names.iloc[pca_order[0]]
    explained = float(pca.explained_variance_ratio_.sum())

    expected = {
        "sin escalar": (raw[0][0], "Dominican Republic"),
        "estandarizado": (standardized[0][0], "Turkey"),
        "salud y demografia": (health[0][0], "Barbados"),
        "macroeconomia y comercio": (macro[0][0], "China"),
        "PCA 2D": (pca_neighbor, "Argentina"),
    }
    mismatches = [
        f"{label}: se obtuvo {actual!r}, se esperaba {wanted!r}"
        for label, (actual, wanted) in expected.items()
        if actual != wanted
    ]
    if mismatches:
        raise AssertionError("Cambió el dataset o el pipeline:\n" + "\n".join(mismatches))

    display_names = {
        "Dominican Republic": "República Dominicana",
        "Maldives": "Maldivas",
        "St. Vincent and the Grenadines": "San Vicente y las Granadinas",
        "Turkey": "Turquía",
    }

    fig, axes = plt.subplots(1, 3, figsize=(12, 4.25))

    def ranking_panel(ax: plt.Axes, title: str, groups: list[tuple[str, list[tuple[str, float]], str]]) -> None:
        ax.axis("off")
        ax.set_title(title, pad=12)
        y = 0.88
        for group_name, ranking, color in groups:
            ax.text(0.02, y, group_name, color=color, fontweight="bold", transform=ax.transAxes)
            y -= 0.10
            for rank, (name, _) in enumerate(ranking[:3], start=1):
                weight = "bold" if rank == 1 else "normal"
                shown_name = display_names.get(name, name)
                ax.text(0.07, y, f"{rank}. {shown_name}", fontweight=weight,
                        color="#0F172A", transform=ax.transAxes)
                y -= 0.085
            y -= 0.055

    ranking_panel(
        axes[0],
        "La escala cambia el vecino",
        [("Sin escalar", raw, RED), ("9 variables estandarizadas", standardized, BLUE)],
    )
    ranking_panel(
        axes[1],
        "El propósito cambia el vecino",
        [("Salud y demografía", health, TEAL), ("Macro y comercio", macro, ORANGE)],
    )

    axes[2].axis("off")
    axes[2].set_title("La proyección cambia la vista", pad=12)
    axes[2].text(0.5, 0.79, "Distancia completa · 9D", ha="center", color=BLUE,
                 fontweight="bold", transform=axes[2].transAxes)
    axes[2].text(0.5, 0.67, "Colombia  →  Turquía", ha="center", fontsize=14,
                 fontweight="bold", transform=axes[2].transAxes)
    axes[2].annotate("", xy=(0.5, 0.49), xytext=(0.5, 0.59), xycoords="axes fraction",
                     arrowprops={"arrowstyle": "->", "color": "#64748B", "lw": 1.8})
    axes[2].text(0.5, 0.39, "PCA · 2D", ha="center", color=PURPLE,
                 fontweight="bold", transform=axes[2].transAxes)
    axes[2].text(0.5, 0.27, "Colombia  →  Argentina", ha="center", fontsize=14,
                 fontweight="bold", transform=axes[2].transAxes)
    axes[2].text(0.5, 0.10, f"Varianza visible: {explained:.1%}", ha="center",
                 color="#475569", transform=axes[2].transAxes)

    fig.suptitle("¿Qué país se parece más a Colombia? Depende de la representación",
                 color=BLUE, fontsize=15, fontweight="bold", y=1.02)
    fig.tight_layout()
    _save(fig, "colombia_similarity")


def _find_browser() -> str:
    """Localiza un navegador Chromium para capturas reproducibles."""
    candidates = [
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        shutil.which("msedge"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)
    raise RuntimeError(
        "No se encontró Chrome/Chromium/Edge. Instale un navegador Chromium "
        "para regenerar las capturas de las interactividades."
    )


def interactive_previews() -> None:
    """Captura las interactividades públicas de PCA y K-Means."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError(
            "Instale Playwright con 'pip install playwright' para regenerar "
            "las capturas interactivas."
        ) from exc

    OUTPUT.mkdir(parents=True, exist_ok=True)
    browser_path = _find_browser()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=browser_path,
            headless=True,
            args=["--allow-file-access-from-files"],
        )
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        for name, url in INTERACTIVE_URLS.items():
            try:
                page.goto(url, wait_until="load", timeout=30_000)
                page.wait_for_timeout(1_500)
                page.screenshot(path=str(OUTPUT / f"{name}.png"), full_page=False)
            except Exception as exc:
                raise RuntimeError(
                    f"No se pudo capturar {url}. Verifique la conexión a internet."
                ) from exc
            print(f"[ok] {name}.png")
        browser.close()


FIGURES = {
    "distance_concentration": distance_concentration,
    "pca_digits": pca_digits,
    "scaling_effect": scaling_effect,
    "kmeans_iterations": kmeans_iterations,
    "k_selection": k_selection,
    "algorithm_comparison": algorithm_comparison,
    "dbscan_roles": dbscan_roles,
    "gmm_density": gmm_density,
    "minibatch_tradeoff": minibatch_tradeoff,
    "image_segmentation": image_segmentation,
    "countries": countries,
    "colombia_similarity": colombia_similarity,
    "interactive_previews": interactive_previews,
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Genera todas las figuras.")
    group.add_argument("--figure", choices=sorted(FIGURES), help="Genera una figura o grupo.")
    args = parser.parse_args()
    _style()
    selected = FIGURES.values() if args.all else [FIGURES[args.figure]]
    for function in selected:
        function()


if __name__ == "__main__":
    main()
