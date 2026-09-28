"""Generate the reproducible plots used by the neural networks class.

The mls3_* book figures remain local, are ignored by Git, and are credited in
slide captions. Quarto embeds them in the compiled HTML when they are present.

Decision-boundary figures adapt these BSD-3-Clause scikit-learn examples:
https://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html
https://scikit-learn.org/stable/auto_examples/neural_networks/plot_mlp_alpha.html

Run from the repository root:
    python3 quarto/redes_neuronales/generate_figures.py --all

The Fashion MNIST snapshot is versioned. Refresh it only when needed:
    python3 quarto/redes_neuronales/generate_figures.py --fetch-sample
"""

import argparse
import gzip
import json
import struct
import sys
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "fashion_sample.json"
FIGURES = ROOT / "figures"
FASHION_BASE = (
    "https://raw.githubusercontent.com/zalandoresearch/fashion-mnist/"
    "master/data/fashion/"
)


def read_idx_prefix(filename, byte_count):
    request = urllib.request.Request(
        FASHION_BASE + filename,
        headers={"User-Agent": "javeriana-tallerml-slides/figure-generator"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        with gzip.GzipFile(fileobj=response) as stream:
            return stream.read(byte_count)


def fetch_sample():
    try:
        raw_image = read_idx_prefix("train-images-idx3-ubyte.gz", 16 + 28 * 28)
        raw_label = read_idx_prefix("train-labels-idx1-ubyte.gz", 9)
    except Exception as exc:
        raise RuntimeError(f"No se pudo descargar Fashion MNIST: {exc}") from exc

    if len(raw_image) != 800 or len(raw_label) != 9:
        raise RuntimeError("La descarga de Fashion MNIST terminó antes de la primera muestra")
    magic, count, rows, cols = struct.unpack(">IIII", raw_image[:16])
    label_magic, label_count = struct.unpack(">II", raw_label[:8])
    if (magic, rows, cols, label_magic) != (2051, 28, 28, 2049):
        raise RuntimeError("Fashion MNIST no tiene el formato IDX esperado")
    if count != label_count or count < 1:
        raise RuntimeError("Las imágenes y etiquetas de Fashion MNIST no coinciden")

    values = list(raw_image[16:])
    sample = {
        "source": "https://github.com/zalandoresearch/fashion-mnist",
        "license": "MIT; © 2017 Zalando SE",
        "split": "train",
        "index": 0,
        "label": raw_label[8],
        "pixels": [values[row * 28 : (row + 1) * 28] for row in range(28)],
    }
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(sample, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Muestra guardada en {DATA.relative_to(ROOT)} (etiqueta {sample['label']})")


def load_sample():
    if not DATA.is_file():
        raise RuntimeError(
            f"Falta {DATA}. Ejecuta este script con --fetch-sample antes de --all."
        )
    sample = json.loads(DATA.read_text(encoding="utf-8"))
    pixels = sample.get("pixels", [])
    if len(pixels) != 28 or any(len(row) != 28 for row in pixels):
        raise RuntimeError("La muestra Fashion MNIST debe contener 28 × 28 píxeles")
    if any(not isinstance(v, int) or not 0 <= v <= 255 for row in pixels for v in row):
        raise RuntimeError("Los píxeles Fashion MNIST deben ser enteros entre 0 y 255")
    return sample


def generate_figures():
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.colors import ListedColormap
        from sklearn.datasets import make_circles, make_moons
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.inspection import DecisionBoundaryDisplay
        from sklearn.model_selection import train_test_split
        from sklearn.neural_network import MLPClassifier
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
        from sklearn.svm import SVC
    except ImportError as exc:
        raise RuntimeError(
            "Faltan dependencias. Instala quarto/redes_neuronales/requirements.txt"
        ) from exc

    sample = load_sample()
    FIGURES.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 12, "axes.titlesize": 15})
    point_colors = ListedColormap(["#c64141", "#174ea6"])

    def draw_boundary(ax, estimator, x, x_train, y_train, x_test, y_test):
        estimator.fit(x_train, y_train)
        DecisionBoundaryDisplay.from_estimator(
            estimator, x, ax=ax, cmap=plt.cm.RdBu, alpha=0.75, eps=0.5
        )
        ax.scatter(x_train[:, 0], x_train[:, 1], c=y_train, cmap=point_colors,
                   edgecolors="black", s=24, linewidths=0.5)
        ax.scatter(x_test[:, 0], x_test[:, 1], c=y_test, cmap=point_colors,
                   edgecolors="black", s=24, linewidths=0.5, alpha=0.55)
        ax.set_xticks([])
        ax.set_yticks([])
        return estimator.score(x_test, y_test)

    for dataset_name, (x, y) in {
        "moons": make_moons(noise=0.3, random_state=0),
        "circles": make_circles(noise=0.2, factor=0.5, random_state=1),
    }.items():
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.4, random_state=42
        )
        models = [
            ("SVM lineal", SVC(kernel="linear", C=0.025, random_state=42)),
            ("SVM RBF", SVC(gamma=2, C=1, random_state=42)),
            ("Bosque aleatorio", RandomForestClassifier(
                max_depth=5, n_estimators=10, max_features=1, random_state=42
            )),
            ("Red neuronal", MLPClassifier(alpha=1, max_iter=1000, random_state=42)),
        ]
        fig, axes = plt.subplots(2, 2, figsize=(10.8, 6.2), constrained_layout=True)
        for ax, (name, model) in zip(axes.flat, models):
            score = draw_boundary(
                ax, make_pipeline(StandardScaler(), model),
                x, x_train, y_train, x_test, y_test
            )
            ax.set_title(f"{name} · prueba {score:.2f}")
        path = FIGURES / f"comparison_{dataset_name}.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        print(f"Generada {path.relative_to(ROOT)}")

    x, y = make_moons(noise=0.3, random_state=0)
    x_train, x_holdout, y_train, y_holdout = train_test_split(
        x, y, test_size=0.4, random_state=42
    )
    x_valid, _, y_valid, _ = train_test_split(
        x_holdout, y_holdout, test_size=0.5, random_state=42
    )
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.6), constrained_layout=True)
    for ax, alpha in zip(axes, [0.1, 1.0, 10.0]):
        model = make_pipeline(
            StandardScaler(),
            MLPClassifier(
                solver="lbfgs", alpha=alpha, hidden_layer_sizes=(10, 10),
                random_state=1, max_iter=2000
            ),
        )
        score = draw_boundary(ax, model, x, x_train, y_train, x_valid, y_valid)
        ax.set_title(f"α = {alpha:g} · validación {score:.2f}")
    path = FIGURES / "alpha_moons.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Generada {path.relative_to(ROOT)}")

    pixels = np.asarray(sample["pixels"], dtype=np.uint8)
    patch = pixels[12:20, 10:18]
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.6), constrained_layout=True)
    axes[0].imshow(pixels, cmap="gray", vmin=0, vmax=255, interpolation="nearest")
    axes[0].set_title("Imagen completa: 28 × 28")
    axes[0].axis("off")
    axes[1].imshow(patch, cmap="gray", vmin=0, vmax=255, interpolation="nearest")
    axes[1].set_title("Ampliación: intensidad de cada píxel")
    for row in range(8):
        for col in range(8):
            value = int(patch[row, col])
            axes[1].text(col, row, str(value), ha="center", va="center",
                         fontsize=8, color="white" if value < 125 else "black")
    axes[1].set_xticks(np.arange(-0.5, 8, 1), minor=True)
    axes[1].set_yticks(np.arange(-0.5, 8, 1), minor=True)
    axes[1].grid(which="minor", color="#64748b", linewidth=0.5)
    axes[1].tick_params(which="both", bottom=False, left=False,
                        labelbottom=False, labelleft=False)
    path = FIGURES / "fashion_pixels.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    print(f"Generada {path.relative_to(ROOT)}")

    fig, ax = plt.subplots(figsize=(7.6, 4.4), constrained_layout=True)
    for x1, x2, result in [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)]:
        ax.scatter(x1, x2, s=750, c="#174ea6" if result else "#c64141",
                   edgecolors="black", linewidths=1.5, zorder=3)
        ax.text(x1, x2, str(result), ha="center", va="center", color="white",
                weight="bold", fontsize=18, zorder=4)
    ax.set(xlim=(-0.35, 1.35), ylim=(-0.35, 1.35), xticks=[0, 1], yticks=[0, 1],
           xlabel="$x_1$", ylabel="$x_2$")
    ax.grid(alpha=0.25)
    ax.set_aspect("equal")
    path = FIGURES / "xor_pattern.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Generada {path.relative_to(ROOT)}")

    epochs = np.arange(1, 17)
    train_loss = 0.18 + 0.9 * np.exp(-epochs / 3.2)
    valid_loss = 0.32 + 0.75 * np.exp(-epochs / 2.5) + 0.009 * np.maximum(epochs - 7, 0) ** 1.7
    fig, ax = plt.subplots(figsize=(8.8, 4.4), constrained_layout=True)
    ax.plot(epochs, train_loss, color="#174ea6", linewidth=3, label="Entrenamiento")
    ax.plot(epochs, valid_loss, color="#c64141", linewidth=3, label="Validación")
    ax.axvline(8, color="#64748b", linestyle="--", linewidth=1.5)
    ax.text(8.3, 0.85, "Revisar aquí", color="#475569", fontsize=12)
    ax.set(xlim=(1, 16), ylim=(0.1, 1.15), xlabel="Época", ylabel="Pérdida")
    ax.legend(frameon=False)
    ax.grid(alpha=0.2)
    path = FIGURES / "learning_curves_schematic.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Generada {path.relative_to(ROOT)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch-sample", action="store_true",
                        help="descarga la primera muestra oficial de Fashion MNIST")
    parser.add_argument("--all", action="store_true", help="genera todas las figuras")
    args = parser.parse_args()
    try:
        if args.fetch_sample:
            fetch_sample()
        if args.all:
            generate_figures()
        if not args.fetch_sample and not args.all:
            parser.print_help()
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
