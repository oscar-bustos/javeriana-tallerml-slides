"""
generate_ensambles_assets.py
Genera todas las imágenes educativas faltantes para la presentación de Ensambles.

Requiere: pip install matplotlib numpy scikit-learn seaborn
Uso: python generate_ensambles_assets.py
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

# ─── Directorio de salida ───────────────────────────────────────────────────
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "quarto", "ensambles", "assets")
os.makedirs(OUT, exist_ok=True)

BLUE  = "#003576"
LIGHT = "#e8eef7"
RED   = "#c0392b"
GREEN = "#27ae60"
GRAY  = "#7f8c8d"
ORANGE= "#e67e22"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

def savefig(name, fig):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  [OK] {name}")


# ══════════════════════════════════════════════════════════════════════════════
# 1. Alta Varianza del Árbol Individual (recap)
# ══════════════════════════════════════════════════════════════════════════════
def tree_variance():
    np.random.seed(42)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

    for ax, seed, title in zip(axes, [0, 7],
                                ["Entrenamiento A", "Entrenamiento B\n(quitando 5% de datos)"]):
        rng = np.random.default_rng(seed)
        X = rng.uniform(0, 1, (80, 2))
        y = (X[:, 0] + X[:, 1] > 1.0).astype(int)
        if seed == 7:
            idx = rng.choice(len(y), size=int(0.05 * len(y)), replace=False)
            X = np.delete(X, idx, axis=0); y = np.delete(y, idx)

        from sklearn.tree import DecisionTreeClassifier
        clf = DecisionTreeClassifier(max_depth=4, random_state=seed)
        clf.fit(X, y)

        xx, yy = np.meshgrid(np.linspace(0, 1, 200), np.linspace(0, 1, 200))
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        ax.contourf(xx, yy, Z, alpha=0.25, cmap="coolwarm")
        ax.scatter(*X[y==0].T, c=BLUE,  s=40, label="Clase 0", zorder=3, edgecolors="white")
        ax.scatter(*X[y==1].T, c=RED,   s=40, label="Clase 1", zorder=3, edgecolors="white")
        ax.set_title(title, fontsize=13, fontweight="bold", color=BLUE)
        ax.set_xticks([]); ax.set_yticks([])

    axes[0].legend(loc="upper left", fontsize=10)
    fig.suptitle("Alta Varianza: Cambios mínimos en los datos alteran el árbol radicalmente",
                 fontsize=12, color=BLUE, y=1.02)
    savefig("tree_alta_varianza.png", fig)


# ══════════════════════════════════════════════════════════════════════════════
# 2. Bootstrap — Muestreo con reemplazo ilustrado
# ══════════════════════════════════════════════════════════════════════════════
def bootstrap_illustration():
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.axis("off")

    orig = list("ABCDEFGHIJ")
    bags = [
        ["A","C","C","E","G","G","H","J","J","A"],
        ["B","B","D","F","F","A","I","C","G","E"],
        ["A","D","H","H","J","B","F","E","A","C"],
    ]

    # Dataset original
    for i, c in enumerate(orig):
        box = FancyBboxPatch((0.02 + i*0.08, 0.62), 0.065, 0.28,
                             boxstyle="round,pad=0.01", fc=LIGHT, ec=BLUE, lw=1.5)
        ax.add_patch(box)
        ax.text(0.055 + i*0.08, 0.755, c, ha="center", va="center",
                fontsize=14, fontweight="bold", color=BLUE)

    ax.text(0.5, 0.97, "Dataset Original (N=10)", ha="center", va="center",
            fontsize=13, fontweight="bold", color=BLUE)

    colors = [BLUE, GREEN, ORANGE]
    for j, (bag, col) in enumerate(zip(bags, colors)):
        y0 = 0.35 - j * 0.18
        ax.text(-0.01, y0 + 0.10, f"Bootstrap\nSample {j+1}", ha="center",
                fontsize=10, color=col, fontweight="bold")
        for i, c in enumerate(bag):
            box = FancyBboxPatch((0.12 + i*0.08, y0), 0.065, 0.17,
                                 boxstyle="round,pad=0.01", fc=LIGHT, ec=col, lw=1.5)
            ax.add_patch(box)
            ax.text(0.155 + i*0.08, y0 + 0.085, c, ha="center", va="center",
                    fontsize=12, color=col, fontweight="bold")

        ax.annotate("", xy=(0.115, y0 + 0.085), xytext=(0.86, 0.755),
                    arrowprops=dict(arrowstyle="->", color=col, lw=1.5,
                                   connectionstyle="arc3,rad=0.3"))

    ax.text(0.5, -0.05, "[*] Algunos elementos aparecen mas de una vez  |  [*] Otros no aparecen (Out-of-Bag)",
            ha="center", fontsize=10, color=GRAY, style="italic")
    ax.set_xlim(-0.05, 1.0); ax.set_ylim(-0.12, 1.05)
    savefig("bootstrap_sampling.png", fig)


# ══════════════════════════════════════════════════════════════════════════════
# 3. OOB Evaluation — muestras fuera de la bolsa como validation set automático
# ══════════════════════════════════════════════════════════════════════════════
def oob_evaluation():
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.axis("off")

    N = 10
    labels = [f"x{i+1}" for i in range(N)]

    rows = [
        ([0,2,2,4,5,7,8,8,9,9], BLUE,  "Árbol 1"),
        ([1,1,3,3,6,7,7,9,9,0], GREEN, "Árbol 2"),
        ([0,2,4,4,5,5,8,9,9,1], ORANGE,"Árbol 3"),
    ]

    y_tops = [0.80, 0.52, 0.24]
    for (bag_idx, col, name), y0 in zip(rows, y_tops):
        in_bag  = set(bag_idx)
        out_bag = set(range(N)) - in_bag
        ax.text(-0.02, y0 + 0.12, name, fontsize=11, fontweight="bold", color=col, va="center")
        for i in range(N):
            if i in in_bag:
                fc, ec, txt = LIGHT, col, "✓"
            else:
                fc, ec, txt = "#fdecea", RED, "OOB"
            box = FancyBboxPatch((0.07 + i*0.088, y0), 0.075, 0.22,
                                 boxstyle="round,pad=0.01", fc=fc, ec=ec, lw=1.5)
            ax.add_patch(box)
            ax.text(0.107 + i*0.088, y0 + 0.11, labels[i], ha="center",
                    fontsize=9, color=BLUE)
            ax.text(0.107 + i*0.088, y0 + 0.05, txt, ha="center",
                    fontsize=7, color=ec, fontweight="bold")

    legend_in  = mpatches.Patch(fc=LIGHT,    ec=BLUE,  label="En la muestra (Training)")
    legend_oob = mpatches.Patch(fc="#fdecea", ec=RED,   label="Out-of-Bag → Evaluación automática")
    ax.legend(handles=[legend_in, legend_oob], loc="lower center",
              bbox_to_anchor=(0.5, -0.1), ncol=2, fontsize=10)

    ax.text(0.5, 1.03,
            "OOB Evaluation: las muestras no usadas en cada árbol actúan como validation set gratuito",
            ha="center", fontsize=12, fontweight="bold", color=BLUE)
    ax.set_xlim(-0.05, 1.0); ax.set_ylim(-0.15, 1.10)
    savefig("oob_evaluation.png", fig)


# ══════════════════════════════════════════════════════════════════════════════
# 4. Hard Voting vs Soft Voting
# ══════════════════════════════════════════════════════════════════════════════
def hard_vs_soft_voting():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Datos de ejemplo
    models = ["Reg. Log.", "SVM", "RF"]
    preds  = ["Clase 1", "Clase 1", "Clase 0"]
    probas = [[0.30, 0.70], [0.45, 0.55], [0.62, 0.38]]

    # ── Hard Voting ──────────────────────────────────────────────────────────
    ax = axes[0]
    ax.set_xlim(0, 6); ax.set_ylim(0, 5); ax.axis("off")
    ax.set_title("Hard Voting  (Mayoría simple)", fontsize=13, fontweight="bold", color=BLUE)

    colors = [BLUE, GREEN, ORANGE]
    for i, (m, p, c) in enumerate(zip(models, preds, colors)):
        y = 3.8 - i * 1.2
        box = FancyBboxPatch((0.3, y), 2.4, 0.8,
                             boxstyle="round,pad=0.05", fc=LIGHT, ec=c, lw=2)
        ax.add_patch(box)
        ax.text(1.5, y + 0.55, m, ha="center", fontsize=11, color=c, fontweight="bold")
        ax.text(1.5, y + 0.2,  f"→ {p}", ha="center", fontsize=11, color=BLUE)

    ax.annotate("", xy=(4.8, 2.2), xytext=(2.8, 2.2),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2))
    box = FancyBboxPatch((4.8, 1.7), 1.0, 1.0,
                         boxstyle="round,pad=0.05", fc=BLUE, ec=BLUE, lw=2)
    ax.add_patch(box)
    ax.text(5.3, 2.2, "Clase 1", ha="center", va="center",
            fontsize=12, color="white", fontweight="bold")
    ax.text(3.5, 1.0, "2 votos Clase 1  vs  1 voto Clase 0\n→ Gana Clase 1",
            ha="center", fontsize=10, color=GRAY, style="italic")

    # ── Soft Voting ──────────────────────────────────────────────────────────
    ax = axes[1]
    ax.set_xlim(0, 7); ax.set_ylim(0, 5); ax.axis("off")
    ax.set_title("Soft Voting  (Promedio de probabilidades)", fontsize=13, fontweight="bold", color=BLUE)

    for i, (m, pr, c) in enumerate(zip(models, probas, colors)):
        y = 3.8 - i * 1.2
        box = FancyBboxPatch((0.3, y), 2.4, 0.8,
                             boxstyle="round,pad=0.05", fc=LIGHT, ec=c, lw=2)
        ax.add_patch(box)
        ax.text(1.5, y + 0.55, m, ha="center", fontsize=11, color=c, fontweight="bold")
        ax.text(1.5, y + 0.2, f"P(0)={pr[0]:.2f}  P(1)={pr[1]:.2f}",
                ha="center", fontsize=10, color=BLUE)

    ax.annotate("", xy=(5.0, 2.2), xytext=(2.8, 2.2),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2))

    avg0 = np.mean([p[0] for p in probas])
    avg1 = np.mean([p[1] for p in probas])
    box = FancyBboxPatch((5.0, 1.6), 1.7, 1.2,
                         boxstyle="round,pad=0.05", fc=BLUE, ec=BLUE, lw=2)
    ax.add_patch(box)
    ax.text(5.85, 2.3, "Clase 1", ha="center", va="center",
            fontsize=12, color="white", fontweight="bold")

    ax.text(3.5, 0.9,
            f"Avg P(Clase 0) = {avg0:.2f}  |  Avg P(Clase 1) = {avg1:.2f}\n"
            f"→ Mayor probabilidad: Clase 1  (más información que la mayoría simple)",
            ha="center", fontsize=10, color=GRAY, style="italic")

    fig.tight_layout(pad=2)
    savefig("hard_vs_soft_voting.png", fig)


# ══════════════════════════════════════════════════════════════════════════════
# 5. Stacking — blender entrenado con predicciones fuera de muestra
# ══════════════════════════════════════════════════════════════════════════════
def stacking_diagram():
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.set_xlim(0, 11); ax.set_ylim(0, 6); ax.axis("off")

    # Datos
    box = FancyBboxPatch((0.2, 1.8), 1.4, 2.4,
                         boxstyle="round,pad=0.08", fc="#eaf4fb", ec=BLUE, lw=2)
    ax.add_patch(box)
    ax.text(0.9, 3.4, "Dataset", ha="center", fontsize=11, fontweight="bold", color=BLUE)
    ax.text(0.9, 3.0, "de", ha="center", fontsize=10, color=BLUE)
    ax.text(0.9, 2.6, "entrenamiento", ha="center", fontsize=10, color=BLUE)
    ax.text(0.9, 2.1, "(X_train)", ha="center", fontsize=10, color=GRAY, style="italic")

    # Modelos base
    base_models = [("Reg. Logística", BLUE), ("SVM", GREEN), ("Random Forest", ORANGE)]
    for i, (name, col) in enumerate(base_models):
        y0 = 3.8 - i * 1.4
        box = FancyBboxPatch((2.5, y0), 2.0, 1.0,
                             boxstyle="round,pad=0.06", fc=LIGHT, ec=col, lw=2)
        ax.add_patch(box)
        ax.text(3.5, y0 + 0.5, name, ha="center", fontsize=10, color=col, fontweight="bold")
        ax.annotate("", xy=(2.5, y0 + 0.5), xytext=(1.7, 3.0),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.5,
                                   connectionstyle="arc3,rad=0.0"))
        # predicciones
        ax.annotate("", xy=(5.8, y0 + 0.5), xytext=(4.5, y0 + 0.5),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.5))
        ax.text(6.1, y0 + 0.5, f"ŷ{i+1}\n(cross_val\n_predict)", ha="center",
                fontsize=8.5, color=col, va="center")

    # Meta-dataset
    box = FancyBboxPatch((7.3, 1.8), 1.5, 2.4,
                         boxstyle="round,pad=0.08", fc="#f0f9f4", ec=GREEN, lw=2)
    ax.add_patch(box)
    ax.text(8.05, 3.4, "Meta-", ha="center", fontsize=11, fontweight="bold", color=GREEN)
    ax.text(8.05, 3.0, "dataset", ha="center", fontsize=11, fontweight="bold", color=GREEN)
    ax.text(8.05, 2.5, "[ŷ1, ŷ2, ŷ3]", ha="center", fontsize=10, color=GREEN, style="italic")
    ax.text(8.05, 2.1, "+ y_train", ha="center", fontsize=10, color=GRAY, style="italic")

    for i in range(3):
        y0 = 3.8 - i * 1.4
        ax.annotate("", xy=(7.3, 2.8 + 0.3*(1-i)), xytext=(6.7, y0 + 0.5),
                    arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.2))

    # Blender
    ax.annotate("", xy=(9.7, 3.0), xytext=(8.9, 3.0),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2))
    box = FancyBboxPatch((9.7, 2.4), 1.1, 1.2,
                         boxstyle="round,pad=0.06", fc=GREEN, ec=GREEN, lw=2)
    ax.add_patch(box)
    ax.text(10.25, 3.0, "Blender\n(Meta-\nmodelo)", ha="center", va="center",
            fontsize=10, color="white", fontweight="bold")

    ax.text(5.5, 5.5,
            "Stacking: El blender aprende a combinar predicciones de modelos base",
            ha="center", fontsize=13, fontweight="bold", color=BLUE)
    ax.text(5.5, 5.0,
            "Clave: el blender se entrena con predicciones fuera de muestra (cross_val_predict)\n"
            "para evitar data leakage",
            ha="center", fontsize=10, color=GRAY, style="italic")

    savefig("stacking_blender.png", fig)


# ══════════════════════════════════════════════════════════════════════════════
# 6. AdaBoost — Actualización de pesos
# ══════════════════════════════════════════════════════════════════════════════
def adaboost_weights():
    np.random.seed(42)
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.5))

    np.random.seed(0)
    X = np.random.randn(20, 2)
    y = (X[:, 0] > 0).astype(int)

    # puntos "difíciles" artificiales
    X[3] = [-0.3, 1.5];  y[3]  = 1
    X[8] = [0.4, -0.8];  y[8]  = 0
    X[15] = [-0.2, 0.9]; y[15] = 1

    from sklearn.tree import DecisionTreeClassifier
    weights = np.ones(len(y)) / len(y)

    for step, ax in enumerate(axes):
        clf = DecisionTreeClassifier(max_depth=1, random_state=42)
        clf.fit(X, y, sample_weight=weights)
        preds = clf.predict(X)
        wrong = preds != y

        sizes = (weights / weights.max()) * 500 + 50
        scatter_colors = np.where(y == 0, BLUE, RED)
        ax.scatter(X[~wrong, 0], X[~wrong, 1], c=np.array(scatter_colors)[~wrong],
                   s=sizes[~wrong], alpha=0.7, edgecolors="white", lw=0.5, zorder=3)
        ax.scatter(X[wrong, 0],  X[wrong, 1],  c=np.array(scatter_colors)[wrong],
                   s=sizes[wrong], alpha=1.0, edgecolors="black", lw=2.5, zorder=4,
                   marker="*")

        # decision boundary
        xx = np.linspace(-3, 3, 200)
        threshold = clf.tree_.threshold[0]
        feat = clf.tree_.feature[0]
        if feat == 0:
            ax.axvline(threshold, color=ORANGE, lw=2, ls="--")
        else:
            ax.axhline(threshold, color=ORANGE, lw=2, ls="--")

        err = np.sum(weights[wrong]) / np.sum(weights)
        alpha = 0.5 * np.log((1 - err) / (err + 1e-10))
        ax.set_title(f"Iteración {step+1}\nError={err:.2f}  α={alpha:.2f}",
                     fontsize=11, fontweight="bold", color=BLUE)
        ax.set_xticks([]); ax.set_yticks([])

        # Actualizar pesos
        weights[wrong]  *= np.exp(alpha)
        weights[~wrong] *= np.exp(-alpha)
        weights /= weights.sum()

    c0 = mpatches.Patch(color=BLUE, label="Clase 0")
    c1 = mpatches.Patch(color=RED,  label="Clase 1")
    axes[2].legend(handles=[c0, c1], fontsize=9, loc="lower right")

    fig.suptitle("AdaBoost: las instancias mal clasificadas reciben mayor peso en la siguiente iteración\n"
                 "★ = mal clasificado (peso aumentado)",
                 fontsize=11, color=BLUE, y=1.03)
    fig.tight_layout()
    savefig("adaboost_pesos.png", fig)


# ══════════════════════════════════════════════════════════════════════════════
# 7. Early Stopping en GBT
# ══════════════════════════════════════════════════════════════════════════════
def early_stopping_gbt():
    np.random.seed(42)
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import log_loss

    X, y = make_classification(n_samples=500, n_features=10, random_state=42)
    Xtr, Xval, ytr, yval = train_test_split(X, y, test_size=0.3, random_state=42)

    n_trees = 200
    clf = GradientBoostingClassifier(n_estimators=n_trees, max_depth=3,
                                     learning_rate=0.1, random_state=42)
    clf.fit(Xtr, ytr)

    train_losses = [log_loss(ytr,  pred) for pred in clf.staged_predict_proba(Xtr)]
    val_losses   = [log_loss(yval, pred) for pred in clf.staged_predict_proba(Xval)]
    best = int(np.argmin(val_losses)) + 1

    fig, ax = plt.subplots(figsize=(9, 4.5))
    xs = range(1, n_trees + 1)
    ax.plot(xs, train_losses, color=BLUE,  lw=2, label="Pérdida entrenamiento")
    ax.plot(xs, val_losses,   color=RED,   lw=2, label="Pérdida validación")
    ax.axvline(best, color=GREEN, lw=2, ls="--",
               label=f"Óptimo: árbol {best}\n(Early Stopping)")
    ax.fill_betweenx([min(val_losses)*0.98, max(val_losses)*1.02],
                     best, n_trees, alpha=0.08, color=RED, label="Zona de sobreajuste")

    ax.annotate(f"Mejor árbol\n#{best}", xy=(best, val_losses[best-1]),
                xytext=(best + 25, val_losses[best-1] + 0.05),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5),
                fontsize=10, color=GREEN, fontweight="bold")

    ax.set_xlabel("Número de árboles", fontsize=11)
    ax.set_ylabel("Log-Loss", fontsize=11)
    ax.set_title("Early Stopping en Gradient Boosting\n"
                 "Detener antes de que la pérdida de validación suba", fontsize=12,
                 fontweight="bold", color=BLUE)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    savefig("early_stopping_gbt.png", fig)


# ══════════════════════════════════════════════════════════════════════════════
# 8. Bias-Variance Trade-off en Bagging
# ══════════════════════════════════════════════════════════════════════════════
def bias_variance_bagging():
    np.random.seed(42)
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import BaggingClassifier
    from sklearn.datasets import make_moons

    X, y = make_moons(n_samples=300, noise=0.35, random_state=42)
    Xgrid = np.linspace(-1.5, 2.5, 300)
    Ygrid = np.linspace(-1.2, 1.5, 300)
    xx, yy = np.meshgrid(Xgrid, Ygrid)
    grid = np.c_[xx.ravel(), yy.ravel()]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    models = [
        (DecisionTreeClassifier(max_depth=None, random_state=42),
         "Árbol de Decisión (sin límite)\nAlta varianza — sobreajuste"),
        (BaggingClassifier(DecisionTreeClassifier(max_depth=None),
                           n_estimators=200, random_state=42),
         "Bagging (200 árboles)\nVarianza reducida — mejor generalización"),
    ]

    for ax, (clf, title) in zip(axes, models):
        clf.fit(X, y)
        Z = clf.predict(grid).reshape(xx.shape)
        ax.contourf(xx, yy, Z, alpha=0.25, cmap="coolwarm")
        ax.contour(xx, yy, Z, levels=[0.5], colors=[BLUE], lw=1)
        ax.scatter(*X[y==0].T, c=BLUE, s=35, edgecolors="white", lw=0.5, zorder=3)
        ax.scatter(*X[y==1].T, c=RED,  s=35, edgecolors="white", lw=0.5, zorder=3)
        ax.set_title(title, fontsize=11, fontweight="bold", color=BLUE)
        ax.set_xticks([]); ax.set_yticks([])

    fig.suptitle("Bagging reduce la varianza promediando múltiples árboles inestables",
                 fontsize=12, color=BLUE, y=1.02)
    fig.tight_layout()
    savefig("bagging_variance_reduction.png", fig)


# ══════════════════════════════════════════════════════════════════════════════
# 9. HistGradientBoosting — Discretización en bins
# ══════════════════════════════════════════════════════════════════════════════
def hist_gradient_boosting():
    np.random.seed(42)
    x = np.sort(np.random.uniform(0, 10, 60))
    y_cont = np.sin(x) + np.random.randn(60) * 0.15

    bins = np.linspace(0, 10, 9)
    bin_idx = np.digitize(x, bins) - 1
    bin_means_x = [(bins[i] + bins[i+1]) / 2 for i in range(len(bins)-1)]
    bin_means_y = [y_cont[bin_idx == i].mean() if np.any(bin_idx == i) else 0
                   for i in range(len(bins)-1)]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # Panel 1 — datos continuos (GBT clásico busca en ∞ puntos)
    ax = axes[0]
    ax.scatter(x, y_cont, c=BLUE, s=30, alpha=0.7, zorder=3)
    for xi in x[::4]:
        ax.axvline(xi, color=RED, lw=0.7, alpha=0.4, ls="--")
    ax.set_title("GBT clásico: evalúa O(N × M × log M) umbrales\n"
                 "— cada punto rojo es un umbral candidato",
                 fontsize=10, fontweight="bold", color=BLUE)
    ax.set_xlabel("Feature continua X"); ax.set_ylabel("Target")
    ax.grid(alpha=0.3)

    # Panel 2 — histograma discretizado
    ax = axes[1]
    ax.scatter(x, y_cont, c=LIGHT, s=30, alpha=0.5, edgecolors=BLUE, lw=0.5, zorder=3)
    for b in bins:
        ax.axvline(b, color=GREEN, lw=2, alpha=0.7)
    ax.step(bins[:-1], bin_means_y, where="post", color=ORANGE, lw=2.5,
            label="Valor del bin")
    for i, (bx, by) in enumerate(zip(bin_means_x, bin_means_y)):
        ax.text(bx, by + 0.12, f"B{i+1}", ha="center", fontsize=8, color=ORANGE,
                fontweight="bold")

    ax.set_title("HistGBT: discretiza en K bins → O(K × M) umbrales\n"
                 "— mucho más rápido, soporta nulos y categóricas nativamente",
                 fontsize=10, fontweight="bold", color=BLUE)
    ax.set_xlabel("Feature discreta (bin)"); ax.set_ylabel("Target")
    ax.legend(fontsize=10); ax.grid(alpha=0.3)

    fig.suptitle("HistGradientBoosting: acelerar GBT mediante discretización de características",
                 fontsize=12, color=BLUE, y=1.02)
    fig.tight_layout()
    savefig("hist_gradient_boosting.png", fig)


# ══════════════════════════════════════════════════════════════════════════════
# 10. Extra-Trees vs Random Forest
# ══════════════════════════════════════════════════════════════════════════════
def extra_trees_comparison():
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
    from sklearn.datasets import make_moons

    X, y = make_moons(n_samples=300, noise=0.30, random_state=42)
    xx, yy = np.meshgrid(np.linspace(-1.5, 2.5, 300),
                         np.linspace(-1.2, 1.5, 300))
    grid = np.c_[xx.ravel(), yy.ravel()]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    models = [
        (RandomForestClassifier(n_estimators=100, random_state=42),
         "Random Forest\nUmbral óptimo en cada nodo"),
        (ExtraTreesClassifier(n_estimators=100, random_state=42),
         "Extra-Trees\nUmbral aleatorio → más rápido, mayor variación"),
    ]
    for ax, (clf, title) in zip(axes, models):
        clf.fit(X, y)
        Z = clf.predict(grid).reshape(xx.shape)
        ax.contourf(xx, yy, Z, alpha=0.25, cmap="coolwarm")
        ax.contour(xx, yy, Z, levels=[0.5], colors=[BLUE], lw=1.5)
        ax.scatter(*X[y==0].T, c=BLUE, s=35, edgecolors="white", lw=0.5, zorder=3)
        ax.scatter(*X[y==1].T, c=RED,  s=35, edgecolors="white", lw=0.5, zorder=3)
        ax.set_title(title, fontsize=11, fontweight="bold", color=BLUE)
        ax.set_xticks([]); ax.set_yticks([])

    fig.suptitle("Extra-Trees: mayor aleatoriedad → frontera más suave y entrenamiento más veloz",
                 fontsize=12, color=BLUE, y=1.02)
    fig.tight_layout()
    savefig("extra_trees_comparison.png", fig)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"\nGenerando imágenes en: {OUT}\n")
    tree_variance()
    bootstrap_illustration()
    oob_evaluation()
    hard_vs_soft_voting()
    stacking_diagram()
    adaboost_weights()
    early_stopping_gbt()
    bias_variance_bagging()
    hist_gradient_boosting()
    extra_trees_comparison()
    print("\n[DONE] Todas las imagenes generadas correctamente.\n")
