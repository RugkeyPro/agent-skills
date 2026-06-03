# TEMPLATE_ID: ordination_embedding
# TEMPLATE_VERSION: 1.0
# FIGURE_TYPE: high_fidelity_pca_pcoa_rda_embedding_plots
#
# IMAGE-DERIVED MODES:
# - pca_biplot_marginal: PCA biplot with arrows, ellipses, and marginal densities
# - pcoa_ellipse: PCoA points with group ellipses and PERMANOVA annotation
# - rda_biplot: RDA/CCA-style axes with environmental arrows
# - embedding_colorbar: MDS/t-SNE/UMAP-like colored embedding with colorbar

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Ellipse
import numpy as np
import pandas as pd


TEMPLATE_ID = "ordination_embedding"
FIELD_MAP = {"x": "x", "y": "y", "group": "group", "color": "color"}
TEXT_CONFIG = {"x_label": "PCA1 54.26%", "y_label": "PCA2 19.67%", "title": ""}
STYLE_CONFIG = {"ordination_mode": "pcoa_ellipse", "figsize": (2.7, 2.7), "dpi": 300, "font_family": "Arial", "font_size": 7.0}
EXPORT_CONFIG = {"output_dir": "outputs", "basename": "ordination_embedding", "formats": ["png", "pdf", "svg"], "dpi": 600}


def apply_style(style):
    mpl.rcParams.update({"font.family": "sans-serif", "font.sans-serif": [style.get("font_family", "Arial"), "Arial", "DejaVu Sans"], "font.size": style["font_size"], "svg.fonttype": "none", "pdf.fonttype": 42, "ps.fonttype": 42, "axes.unicode_minus": False})


def load_data(path: str | Path = "data.csv"):
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    rng = np.random.default_rng(42)
    mode = STYLE_CONFIG["ordination_mode"]
    if mode == "embedding_colorbar":
        centers = rng.normal(0, 25, (10, 2))
        rows = []
        for i, c in enumerate(centers):
            pts = rng.normal(c, 6, (130, 2))
            rows.extend({"x": x, "y": y, "group": str(i), "color": i} for x, y in pts)
        return pd.DataFrame(rows)
    centers = [(-0.22, -0.08), (0.02, 0.08), (0.30, -0.03)]
    rows = []
    for i, (cx, cy) in enumerate(centers):
        pts = rng.multivariate_normal([cx, cy], [[0.008, 0.002], [0.002, 0.018]], 14)
        rows.extend({"x": x, "y": y, "group": f"G{i+1}", "color": i} for x, y in pts)
    return pd.DataFrame(rows)


def prepare_data(df, field_map, style):
    out = pd.DataFrame({"x": pd.to_numeric(df[field_map["x"]], errors="coerce"), "y": pd.to_numeric(df[field_map["y"]], errors="coerce")})
    if field_map["group"] in df.columns:
        out["group"] = df[field_map["group"]].astype(str)
    if field_map["color"] in df.columns:
        out["color"] = pd.to_numeric(df[field_map["color"]], errors="coerce")
    return out.dropna(subset=["x", "y"])


def add_ellipse(ax, x, y, color):
    cov = np.cov(x, y)
    vals, vecs = np.linalg.eigh(cov)
    angle = np.degrees(np.arctan2(*vecs[:, 1][::-1]))
    ell = Ellipse((np.mean(x), np.mean(y)), width=2.6 * np.sqrt(vals[1]), height=2.6 * np.sqrt(vals[0]), angle=angle, facecolor=color, edgecolor="none", alpha=0.15)
    ax.add_patch(ell)


def plot_pcoa(data, text, style):
    fig, ax = plt.subplots(figsize=style["figsize"], dpi=style["dpi"])
    colors = ["#00a78d", "#39b6d3", "#e54b32"]
    for i, (group, sub) in enumerate(data.groupby("group")):
        c = colors[i % len(colors)]
        ax.scatter(sub["x"], sub["y"], color=c, s=18, edgecolor="white", linewidth=0.3)
        add_ellipse(ax, sub["x"], sub["y"], c)
    ax.axhline(0, color="0.85", lw=0.8)
    ax.axvline(0, color="0.85", lw=0.8)
    ax.text(0.56, 0.13, "PERMANOVA\nF = 8.944, P = 0.0001", transform=ax.transAxes, fontsize=style["font_size"])
    ax.set_xlabel("PCoA1: 31.32 %", fontsize=style["font_size"] + 2)
    ax.set_ylabel("PCoA2: 10.3 %", fontsize=style["font_size"] + 2)
    for sp in ax.spines.values():
        sp.set_linewidth(0.8)
    return fig


def plot_rda(data, text, style):
    fig, ax = plt.subplots(figsize=(2.7, 2.45), dpi=style["dpi"])
    ax.axhline(0, color="0.75", lw=0.8)
    ax.axvline(0, color="0.75", lw=0.8)
    rng = np.random.default_rng(1)
    ax.scatter(rng.uniform(-0.8, 0.8, 20), rng.uniform(-0.7, 0.7, 20), marker="^", color="#14a6c8", s=12)
    arrows = {"WT": (0.78, -0.32), "Turbidity": (0.60, 0.04), "Cond": (-0.20, -0.68), "NH3-N": (-0.40, 0.55)}
    for lab, (x, y) in arrows.items():
        ax.arrow(0, 0, x, y, color="#ff5a1f", head_width=0.045, length_includes_head=True, lw=1.0)
        ax.text(x, y, lab, color="#ff5a1f", fontsize=style["font_size"], ha="center")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-0.9, 0.8)
    ax.set_xlabel("RDA1(69.03%)")
    ax.set_ylabel("RDA2(1.68%)")
    for sp in ax.spines.values():
        sp.set_linewidth(0.8)
    return fig


def plot_pca_biplot(data, text, style):
    fig = plt.figure(figsize=(3.3, 3.0), dpi=style["dpi"])
    gs = GridSpec(2, 2, height_ratios=[0.35, 2.4], width_ratios=[2.4, 0.35], hspace=0, wspace=0)
    ax_top = fig.add_subplot(gs[0, 0])
    ax = fig.add_subplot(gs[1, 0])
    ax_right = fig.add_subplot(gs[1, 1])
    colors = ["#83c7db", "#f0c39a", "#7fb9a8"]
    for i, (g, sub) in enumerate(data.groupby("group")):
        c = colors[i % len(colors)]
        ax.scatter(sub["x"], sub["y"], color=c, s=20, alpha=0.7)
        add_ellipse(ax, sub["x"], sub["y"], c)
        ax_top.hist(sub["x"], bins=20, density=True, histtype="stepfilled", color=c, alpha=0.25)
        ax_right.hist(sub["y"], bins=20, density=True, orientation="horizontal", histtype="stepfilled", color=c, alpha=0.25)
    ax.axhline(0, color="0.2", ls=(0, (1, 3)))
    ax.axvline(0, color="0.2", ls=(0, (1, 3)))
    for lab, x, y in [("oxy", -0.35, 0.25), ("ele", -0.30, -0.35), ("dis", 0.36, 0.32), ("nit", 0.40, 0.0), ("amm", 0.32, -0.36), ("pH", 0.02, 0.24)]:
        ax.arrow(0, 0, x, y, color="#b52b2b", head_width=0.018, length_includes_head=True, lw=0.8)
        ax.text(x, y, lab, fontsize=style["font_size"])
    ax.set_xlabel(text["x_label"])
    ax.set_ylabel(text["y_label"])
    ax_top.axis("off")
    ax_right.axis("off")
    return fig


def plot_embedding(data, text, style):
    fig, ax = plt.subplots(figsize=(3.0, 2.7), dpi=style["dpi"])
    sc = ax.scatter(data["x"], data["y"], c=data.get("color", 0), cmap="Spectral", s=15, alpha=0.55)
    ax.set_title("MDS on the Digits Dataset")
    fig.colorbar(sc, ax=ax, fraction=0.045, pad=0.04)
    for sp in ax.spines.values():
        sp.set_linewidth(0.8)
    return fig


def plot(data, text, style):
    apply_style(style)
    mode = style["ordination_mode"]
    if mode == "pca_biplot_marginal":
        return plot_pca_biplot(data, text, style)
    if mode == "rda_biplot":
        return plot_rda(data, text, style)
    if mode == "embedding_colorbar":
        return plot_embedding(data, text, style)
    return plot_pcoa(data, text, style)


def save_outputs(fig, export):
    out = Path(export["output_dir"]); out.mkdir(parents=True, exist_ok=True)
    paths = []
    for fmt in export["formats"]:
        path = out / f"{export['basename']}.{fmt}"
        kwargs = {"bbox_inches": "tight", "pad_inches": 0.04}
        if fmt == "png": kwargs["dpi"] = export["dpi"]
        fig.savefig(path, **kwargs); paths.append(path)
    plt.close(fig); return paths


def main():
    df = load_data(sys.argv[1] if len(sys.argv) > 1 else "data.csv")
    data = prepare_data(df, FIELD_MAP, STYLE_CONFIG)
    fig = plot(data, TEXT_CONFIG, STYLE_CONFIG)
    print("Generated:", [str(p) for p in save_outputs(fig, EXPORT_CONFIG)])


if __name__ == "__main__":
    main()
