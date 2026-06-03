# TEMPLATE_ID: inference_distribution
# TEMPLATE_VERSION: 1.0
# FIGURE_TYPE: high_fidelity_inference_distribution_and_effect_plots
#
# IMAGE-DERIVED MODES:
# - significance_box: colored boxplots with raw points and compact letters
# - taxonomic_stacked_bar: compact 100% stacked composition with legend
# - ridgeline_density: stacked density ridgelines
# - forest_ridgeline: meta-analysis ridgeline forest plot
# - posterior_distribution: posterior ridgelines with side heatmap
# - dumbbell_caterpillar: ordered expected/observed transition dumbbell plot
# - roc_curve: ROC curve with sensitivity/specificity axes and AUC labels

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

try:
    from scipy.stats import gaussian_kde
except ImportError:
    gaussian_kde = None


TEMPLATE_ID = "inference_distribution"
FIELD_MAP = {"group": "group", "value": "value"}
TEXT_CONFIG = {"x_label": "Sample", "y_label": "Index", "title": ""}
STYLE_CONFIG = {"mode": "significance_box", "figsize": (3.2, 2.7), "dpi": 300, "font_family": "Arial", "font_size": 7.0}
EXPORT_CONFIG = {"output_dir": "outputs", "basename": "inference_distribution", "formats": ["png", "pdf", "svg"], "dpi": 600}


def apply_style(style):
    mpl.rcParams.update({"font.family": "sans-serif", "font.sans-serif": [style.get("font_family", "Arial"), "Arial", "DejaVu Sans"], "font.size": style["font_size"], "svg.fonttype": "none", "pdf.fonttype": 42, "ps.fonttype": 42, "axes.unicode_minus": False})


def load_data(path: str | Path = "data.csv"):
    p = Path(path)
    if p.exists(): return pd.read_csv(p)
    return pd.DataFrame()


def prepare_data(df, field_map, style):
    return df


def kde_curve(vals, grid):
    if gaussian_kde is None or len(vals) < 3:
        hist, edges = np.histogram(vals, bins=25, range=(grid.min(), grid.max()), density=True)
        return np.interp(grid, (edges[:-1] + edges[1:]) / 2, hist)
    return gaussian_kde(vals)(grid)


def plot_significance_box(style, text):
    rng = np.random.default_rng(42)
    fig, ax = plt.subplots(figsize=style["figsize"], dpi=style["dpi"])
    colors = ["#53305a", "#fff59d", "#cbd8b8", "#e9a09a", "#c35a3c", "#e7b780", "#42a6c6"]
    letters = ["b", "ab", "b", "a", "ab", "c", "c"]
    data = [rng.normal(mu, 0.55, 6) for mu in [3.0, 4.2, 3.3, 4.7, 3.5, 2.0, 2.2]]
    bp = ax.boxplot(data, patch_artist=True, widths=0.55, showfliers=False, medianprops=dict(color="black", lw=1.2), whiskerprops=dict(color="black", lw=1.0), capprops=dict(color="black", lw=1.0))
    for patch, c in zip(bp["boxes"], colors):
        patch.set_facecolor(c); patch.set_alpha(0.78); patch.set_edgecolor("none")
    for i, vals in enumerate(data, start=1):
        ax.scatter(np.full(len(vals), i) + rng.normal(0, 0.055, len(vals)), vals, color="black", s=16, zorder=3)
        ax.text(i, max(vals) + 0.25, letters[i - 1], ha="center", fontsize=style["font_size"] + 7)
    ax.set_xticks([])
    ax.set_xlabel(text["x_label"], fontsize=style["font_size"] + 8)
    ax.set_ylabel(text["y_label"], fontsize=style["font_size"] + 8)
    ax.set_yticks([])
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(1.2); ax.spines["bottom"].set_linewidth(1.2)
    return fig


def plot_taxonomic_stacked(style):
    rng = np.random.default_rng(42)
    cohorts = ["NOC", "NOM", "POT", "OM", "PT"]
    colors = ["#8db6c2", "#668b97", "#e6c7cd", "#bf7791", "#7fac73"]
    groups = ["NFs", "iCAFs", "apCAFs", "myCAFs_ACTA2", "myCAFs_FAP", "myCAFs_ESR1"]
    raw = rng.uniform(0.01, 1, (len(groups), len(cohorts)))
    raw[:, 3] += np.linspace(0.2, 1.4, len(groups))
    pct = raw / raw.sum(axis=1, keepdims=True) * 100
    fig, ax = plt.subplots(figsize=(2.0, 1.65), dpi=style["dpi"])
    bottom = np.zeros(len(groups))
    x = np.arange(len(groups))
    for i, (cohort, color) in enumerate(zip(cohorts, colors)):
        ax.bar(x, pct[:, i], bottom=bottom, color=color, edgecolor="white", width=0.72, label=cohort)
        bottom += pct[:, i]
    ax.set_ylim(0, 100); ax.set_ylabel("Cell proportion (%)")
    ax.set_xticks(x); ax.set_xticklabels(groups, rotation=55, ha="right")
    ax.legend(title="Cohort", loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False)
    for sp in ax.spines.values(): sp.set_linewidth(0.8)
    return fig


def plot_ridgeline(style):
    rng = np.random.default_rng(42)
    groups = ["Ideal", "Premium", "Very Good", "Good", "Fair"]
    colors = ["#b9df72", "#e99acb", "#a8b5d5", "#f4a07a", "#8bd0bd"]
    fig, ax = plt.subplots(figsize=(2.5, 1.9), dpi=style["dpi"])
    grid = np.linspace(-0.2, 2.8, 300)
    for i, (g, c) in enumerate(zip(groups, colors)):
        vals = np.r_[rng.normal(0.4 + i * 0.13, 0.18, 80), rng.normal(1.0 + i * 0.06, 0.22, 60), rng.exponential(0.45, 30) + 1.3]
        dens = kde_curve(vals, grid); dens = dens / dens.max() * 0.55
        y0 = len(groups) - i
        ax.fill_between(grid, y0, y0 + dens, color=c, alpha=0.85)
        ax.plot(grid, y0 + dens, color="black", lw=0.8)
    ax.set_yticks(range(1, len(groups) + 1)); ax.set_yticklabels(groups[::-1])
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    return fig


def plot_forest_ridgeline(style):
    rng = np.random.default_rng(42)
    outcomes = ["VO2max", "Maximum power", "Peak power", "Mean power", "Strength", "Thickness", "Endurance", "Time trial", "Time to fatigue", "Peak speed", "Sprint time", "Repeat sprint ability"]
    fig, ax = plt.subplots(figsize=(3.3, 3.4), dpi=style["dpi"])
    grid = np.linspace(-2.5, 3, 300)
    cmap = mpl.cm.get_cmap("GnBu")
    effects = rng.normal(0.35, 0.65, len(outcomes))
    for yi, (out, eff) in enumerate(zip(outcomes[::-1], effects[::-1]), start=1):
        vals = rng.normal(eff, 0.35, 150)
        dens = kde_curve(vals, grid); dens = dens / dens.max() * 0.45
        color = cmap((eff + 2) / 4)
        ax.fill_between(grid, yi, yi + dens, color=color, alpha=0.9)
        ax.hlines(yi, -2.3, 2.8, color=color, lw=0.5, alpha=0.5)
        ax.plot([eff - 0.45, eff + 0.45], [yi + 0.04, yi + 0.04], color="black", lw=0.9)
        ax.scatter([eff], [yi + 0.07], marker="s", color="#0086c7", s=14, zorder=3)
        ax.scatter(rng.normal(eff, 0.35, 5), np.full(5, yi + 0.17), color="black", s=5)
    ax.axvline(0, color="#0086c7", lw=1.0, ls="--")
    ax.set_yticks(range(1, len(outcomes) + 1)); ax.set_yticklabels(outcomes[::-1], fontsize=style["font_size"] - 1)
    ax.set_xlabel("Hedges' g (95% CI)")
    ax.set_ylabel("Outcome")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    return fig


def plot_posterior_distribution(style):
    rng = np.random.default_rng(42)
    labels = ["TP", "TN", "SR", "PB", "pH", "MAT", "MAP", "AI", "Clay", "Silt", "C/P", "C/N", "BD", "AP"]
    fig = plt.figure(figsize=(3.4, 3.4), dpi=style["dpi"])
    ax = fig.add_axes([0.16, 0.12, 0.60, 0.78])
    axh = fig.add_axes([0.80, 0.12, 0.09, 0.78])
    grid = np.linspace(-0.8, 0.9, 240)
    for i, lab in enumerate(labels):
        y = len(labels) - i
        mu = rng.normal(0, 0.28)
        vals = rng.normal(mu, 0.12, 200)
        dens = kde_curve(vals, grid); dens = dens / dens.max() * 0.42
        color = "#ef604d" if mu > 0 else "#5cc3d7"
        ax.fill_between(grid, y, y + dens, color=color, alpha=0.9)
        ax.text(0.62 if mu > 0 else -0.62, y + 0.05, f"{rng.uniform(50, 100):.1f}%", color=color, fontsize=style["font_size"] - 1)
    ax.axvline(0, color="0.55", ls="--", lw=0.8)
    ax.set_yticks(range(1, len(labels) + 1)); ax.set_yticklabels(labels[::-1], fontweight="bold")
    ax.set_xlabel("Posterior Distributions", fontweight="bold")
    heat = rng.normal(0, 0.5, (len(labels), 1))
    axh.imshow(heat, cmap="RdBu_r", vmin=-0.5, vmax=0.5, aspect="auto")
    axh.set_yticks(range(len(labels))); axh.set_yticklabels(labels, fontweight="bold")
    axh.yaxis.tick_right(); axh.set_xticks([])
    return fig


def plot_dumbbell(style):
    rng = np.random.default_rng(42)
    cats = ["Serranidae", "Zoarcidae", "Myctophidae", "Sebastidae", "Liparidae", "Carangidae", "Scombridae", "Macrouridae", "Soleidae", "Ophidiidae", "Labridae", "Gobiidae", "Apogonidae", "Haemulidae", "Blenniidae", "Pomacentridae", "Sciaenidae"]
    y = np.arange(len(cats))[::-1]
    exp = rng.uniform(0, 30, len(cats))
    obs = np.clip(exp + rng.normal(5, 10, len(cats)), 0, 75)
    fig, ax = plt.subplots(figsize=(2.75, 4.0), dpi=style["dpi"])
    for yi, e, o in zip(y, exp, obs):
        ax.hlines(yi, e, o, color="0.75", lw=3, alpha=0.5)
        ax.scatter(e, yi, facecolor="white", edgecolor="0.4", s=20, zorder=3)
        color = "#0aa38f" if o > e + 7 else "#f0b000" if o < e - 7 else "0.35"
        ax.scatter(o, yi, color=color, s=20, zorder=4)
    ax.set_yticks(y); ax.set_yticklabels(cats, fontsize=style["font_size"] - 1)
    ax.set_xlabel("Number of Transitions")
    ax.grid(axis="y", color="0.92")
    ax.legend(handles=[Line2D([0], [0], marker="o", color="w", markerfacecolor="#0aa38f", label="Above expectation"), Line2D([0], [0], marker="o", color="w", markerfacecolor="0.35", label="Within expectation"), Line2D([0], [0], marker="o", color="w", markerfacecolor="#f0b000", label="Below expectation")], loc="lower right", fontsize=style["font_size"] - 1, frameon=True)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    return fig


def plot_roc(style):
    fig, ax = plt.subplots(figsize=(2.1, 2.1), dpi=style["dpi"])
    specs = [("#229a95", "Train AUC = 0.914\nAccuracy = 0.912"), ("#c51ba9", "Test AUC = 0.971\nAccuracy = 0.980"), ("#f28e1c", "Validation AUC = 0.966\nAccuracy = 0.920")]
    rng = np.random.default_rng(42)
    for color, label in specs:
        fpr = np.r_[0, np.sort(rng.beta(0.7, 4, 14)), 1]
        tpr = np.r_[0, np.sort(rng.beta(4, 0.9, 14)), 1]
        ax.plot(1 - fpr, tpr, color=color, lw=1.4)
    ax.set_xlim(1.05, -0.05); ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel("Specificity", fontsize=style["font_size"] + 2)
    ax.set_ylabel("Sensitivity", fontsize=style["font_size"] + 2)
    ax.grid(True, color="0.92", lw=0.5)
    ax.text(0.32, 0.45, specs[0][1], color=specs[0][0], transform=ax.transAxes, fontsize=style["font_size"] + 1)
    ax.text(0.35, 0.28, specs[1][1], color=specs[1][0], transform=ax.transAxes, fontsize=style["font_size"] + 1)
    ax.text(0.15, 0.13, specs[2][1], color=specs[2][0], transform=ax.transAxes, fontsize=style["font_size"] + 1)
    for sp in ax.spines.values(): sp.set_linewidth(1.0)
    return fig


def plot(data, text, style):
    apply_style(style)
    mode = style["mode"]
    return {
        "taxonomic_stacked_bar": plot_taxonomic_stacked,
        "ridgeline_density": plot_ridgeline,
        "forest_ridgeline": plot_forest_ridgeline,
        "posterior_distribution": plot_posterior_distribution,
        "dumbbell_caterpillar": plot_dumbbell,
        "roc_curve": plot_roc,
    }.get(mode, plot_significance_box)(style, text) if mode == "significance_box" else {
        "taxonomic_stacked_bar": plot_taxonomic_stacked,
        "ridgeline_density": plot_ridgeline,
        "forest_ridgeline": plot_forest_ridgeline,
        "posterior_distribution": plot_posterior_distribution,
        "dumbbell_caterpillar": plot_dumbbell,
        "roc_curve": plot_roc,
    }[mode](style)


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
