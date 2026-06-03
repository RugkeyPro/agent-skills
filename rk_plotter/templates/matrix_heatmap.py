# TEMPLATE_ID: matrix_heatmap
# TEMPLATE_VERSION: 1.0
# FIGURE_TYPE: high_fidelity_correlation_cluster_and_significance_heatmaps
#
# IMAGE-DERIVED MODES:
# - triangular_corr: upper triangular annotated correlation heatmap
# - pair_corr_density: lower density mini-panels plus upper correlation tiles
# - clustered_heatmap: heatmap with row/column dendrograms and side annotations
# - expression_significance: narrow scaled-expression heatmap with significance labels

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle, Patch
import numpy as np
import pandas as pd

try:
    from scipy.cluster.hierarchy import dendrogram, linkage
    from scipy.stats import gaussian_kde
except ImportError:
    dendrogram = linkage = gaussian_kde = None


TEMPLATE_ID = "matrix_heatmap"

FIELD_MAP = {"matrix": "matrix"}

TEXT_CONFIG = {"colorbar_label": "Spearman correlation", "title": ""}

STYLE_CONFIG = {
    "heatmap_mode": "triangular_corr",
    "figsize": (3.5, 3.2),
    "dpi": 300,
    "font_family": "Arial",
    "font_size": 7.0,
    "cmap": "RdBu",
}

EXPORT_CONFIG = {"output_dir": "outputs", "basename": "matrix_heatmap", "formats": ["png", "pdf", "svg"], "dpi": 600}


def apply_style(style):
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": [style.get("font_family", "Arial"), "Arial", "DejaVu Sans"],
        "font.size": style["font_size"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.unicode_minus": False,
    })


def synthetic_corr(n=10):
    rng = np.random.default_rng(42)
    base = rng.normal(size=(180, n))
    base[:, 1:4] += base[:, [0]] * 0.7
    base[:, 5:8] -= base[:, [2]] * 0.6
    corr = np.corrcoef(base, rowvar=False)
    labels = ["carb", "wt", "hp", "cyl", "disp", "qsec", "vs", "mpg", "drat", "am"][:n]
    return corr, labels, base


def load_data(path: str | Path = "data.csv") -> pd.DataFrame:
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    corr, labels, base = synthetic_corr()
    return pd.DataFrame(base, columns=labels)


def prepare_data(df, field_map, style):
    numeric = df.select_dtypes(include=[np.number])
    if numeric.empty:
        corr, labels, base = synthetic_corr()
        return {"corr": corr, "labels": labels, "raw": base}
    return {"corr": numeric.corr(method="spearman").to_numpy(), "labels": list(numeric.columns), "raw": numeric.to_numpy()}


def stars(v):
    a = abs(v)
    return "***" if a > 0.55 else "**" if a > 0.35 else "*" if a > 0.18 else ""


def plot_triangular(data, text, style):
    corr, labels = data["corr"], data["labels"]
    n = len(labels)
    fig, ax = plt.subplots(figsize=style["figsize"], dpi=style["dpi"])
    cmap = mpl.colormaps["RdBu"]
    norm = mpl.colors.Normalize(-1, 1)
    ax.set_xlim(0, n)
    ax.set_ylim(n, 0)
    for i in range(n):
        for j in range(n):
            if j < i:
                continue
            val = corr[i, j]
            ax.add_patch(Rectangle((j, i), 1, 1, facecolor=cmap(norm(val)), edgecolor="white", linewidth=0.7))
            ax.text(j + 0.5, i + 0.5, f"{val:.2g}", ha="center", va="center", fontsize=style["font_size"], fontweight="bold")
    ax.set_xticks(np.arange(n) + 0.5)
    ax.set_xticklabels(labels, rotation=45, ha="left", fontsize=style["font_size"])
    ax.xaxis.tick_top()
    ax.set_yticks(np.arange(n) + 0.5)
    ax.set_yticklabels(labels, fontsize=style["font_size"])
    ax.tick_params(length=0)
    ax.set_frame_on(False)
    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, fraction=0.045, pad=0.02)
    cbar.set_label(text["colorbar_label"])
    return fig


def plot_pair_corr_density(data, text, style):
    corr, labels, raw = data["corr"], data["labels"][:8], data["raw"][:, :8]
    n = len(labels)
    fig = plt.figure(figsize=(3.5, 3.5), dpi=style["dpi"])
    gs = GridSpec(n, n, figure=fig, wspace=0.08, hspace=0.08)
    cmap = mpl.cm.RdYlBu_r
    norm = mpl.colors.Normalize(-0.85, 0.77)
    for i in range(n):
        for j in range(n):
            ax = fig.add_subplot(gs[i, j])
            ax.set_xticks([])
            ax.set_yticks([])
            if i == j:
                ax.text(0.5, 0.5, labels[i][-6:], ha="center", va="center", fontsize=style["font_size"] + 1, fontweight="bold")
                ax.axis("off")
            elif i < j:
                val = corr[i, j]
                ax.imshow([[val]], cmap=cmap, norm=norm, aspect="auto")
                ax.text(0, 0, f"{val:.2f}{stars(val)}", ha="center", va="center", fontsize=style["font_size"] - 1)
                for sp in ax.spines.values():
                    sp.set_color("0.55")
            else:
                x, y = raw[:, j], raw[:, i]
                ax.scatter(x, y, s=1, color="none")
                if gaussian_kde is not None:
                    xx, yy = np.meshgrid(np.linspace(x.min(), x.max(), 30), np.linspace(y.min(), y.max(), 30))
                    zz = gaussian_kde(np.vstack([x, y]))(np.vstack([xx.ravel(), yy.ravel()])).reshape(xx.shape)
                    ax.contourf(xx, yy, zz, levels=8, cmap="RdYlBu_r", alpha=0.85)
                for sp in ax.spines.values():
                    sp.set_linewidth(0.7)
    cax = fig.add_axes([0.90, 0.16, 0.025, 0.68])
    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax, label=text["colorbar_label"])
    return fig


def plot_clustered(data, text, style):
    raw = data["raw"][:20, :6]
    row_labels = [f"MADN{i:04d}" for i in range(1, raw.shape[0] + 1)]
    col_labels = ["B3", "A1", "B2", "A3", "A2", "B1"][:raw.shape[1]]
    if linkage is not None:
        row_link = linkage(raw, method="average")
        col_link = linkage(raw.T, method="average")
        row_order = dendrogram(row_link, no_plot=True)["leaves"]
        col_order = dendrogram(col_link, no_plot=True)["leaves"]
    else:
        row_order = list(range(raw.shape[0]))
        col_order = list(range(raw.shape[1]))
    z = raw[row_order][:, col_order]
    fig = plt.figure(figsize=(3.5, 3.4), dpi=style["dpi"])
    gs = GridSpec(3, 4, width_ratios=[0.55, 0.12, 2.2, 0.9], height_ratios=[0.45, 0.1, 2.6], wspace=0.05, hspace=0.05)
    ax_col = fig.add_subplot(gs[0, 2])
    ax_row = fig.add_subplot(gs[2, 0])
    ax_ann = fig.add_subplot(gs[2, 1])
    ax = fig.add_subplot(gs[2, 2])
    ax_leg = fig.add_subplot(gs[2, 3])
    if dendrogram is not None:
        dendrogram(col_link, ax=ax_col, color_threshold=0, above_threshold_color="0.25", no_labels=True)
        dendrogram(row_link, ax=ax_row, orientation="left", color_threshold=0, above_threshold_color="0.25", no_labels=True)
    ax_col.axis("off")
    ax_row.axis("off")
    im = ax.imshow(z, cmap="RdBu", vmin=-2, vmax=2, aspect="auto")
    for i in range(z.shape[0]):
        for j in range(z.shape[1]):
            ax.text(j, i, f"{z[i, j]:.1f}", ha="center", va="center", fontsize=style["font_size"] - 1, color="0.25")
    ax.set_xticks(range(len(col_order)))
    ax.set_xticklabels([col_labels[i] for i in col_order], rotation=45, ha="right")
    ax.set_yticks(range(len(row_order)))
    ax.set_yticklabels([row_labels[i] for i in row_order], fontsize=style["font_size"] - 1)
    ax.yaxis.tick_right()
    ax.tick_params(length=0)
    groups = np.array(["#e6462e", "#4bbbd0", "#00a77f"])
    ax_ann.imshow(np.arange(z.shape[0])[:, None] % 3, cmap=mpl.colors.ListedColormap(groups), aspect="auto")
    ax_ann.axis("off")
    fig.colorbar(im, ax=ax_leg, fraction=0.25)
    ax_leg.axis("off")
    return fig


def plot_expression(data, text, style):
    genes = ["Ccl2", "Ccl5", "Ccl8", "Cxcl1", "Cxcl15", "Cxcl3", "Cxcl5", "Cxcl9", "Ereg", "Gdf15", "Igfbp6", "Igfbp7", "Il1a", "Il1b", "Il6", "Mmp12", "Mmp2", "Mmp3", "Mmp9", "Spp1", "Tnf"]
    cols = ["10 wk", "48 wk", "72 wk", "72 wk + 3TC", "72 wk + H-151"]
    rng = np.random.default_rng(42)
    z = rng.normal(0, 0.9, (len(genes), len(cols)))
    fig, ax = plt.subplots(figsize=(1.45, 4.0), dpi=style["dpi"])
    im = ax.imshow(z, cmap="RdBu_r", vmin=-2, vmax=2, aspect="auto")
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels(cols, rotation=90, va="bottom")
    ax.xaxis.tick_top()
    ax.set_yticks(range(len(genes)))
    ax.set_yticklabels(genes, fontstyle="italic", fontsize=style["font_size"])
    for i in range(len(genes)):
        for j in range(len(cols)):
            ax.text(j, i, "*" if abs(z[i, j]) > 0.6 else "NS", ha="center", va="center", fontsize=style["font_size"], fontweight="bold")
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_linewidth(0.8)
    cbar = fig.colorbar(im, ax=ax, orientation="horizontal", fraction=0.08, pad=0.05)
    cbar.set_label("Scaled expression")
    return fig


def plot(data, text, style):
    apply_style(style)
    mode = style["heatmap_mode"]
    if mode == "pair_corr_density":
        return plot_pair_corr_density(data, text, style)
    if mode == "clustered_heatmap":
        return plot_clustered(data, text, style)
    if mode == "expression_significance":
        return plot_expression(data, text, style)
    return plot_triangular(data, text, style)


def save_outputs(fig, export):
    out = Path(export["output_dir"])
    out.mkdir(parents=True, exist_ok=True)
    paths = []
    for fmt in export["formats"]:
        path = out / f"{export['basename']}.{fmt}"
        kwargs = {"bbox_inches": "tight", "pad_inches": 0.04}
        if fmt == "png":
            kwargs["dpi"] = export["dpi"]
        fig.savefig(path, **kwargs)
        paths.append(path)
    plt.close(fig)
    return paths


def main():
    df = load_data(sys.argv[1] if len(sys.argv) > 1 else "data.csv")
    data = prepare_data(df, FIELD_MAP, STYLE_CONFIG)
    fig = plot(data, TEXT_CONFIG, STYLE_CONFIG)
    print("Generated:", [str(p) for p in save_outputs(fig, EXPORT_CONFIG)])


if __name__ == "__main__":
    main()
