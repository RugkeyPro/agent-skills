# TEMPLATE_ID: violin_boxplot
# TEMPLATE_VERSION: 2.0
# FIGURE_TYPE: high_fidelity_environmental_distribution_plots
#
# HIGH_FIDELITY_SOURCES:
# - assets/original-scripts/figure-boxen_plot.py
# - assets/original-scripts/figure-grouped violin plot with boxplot overlay.py
# - assets/new-scripts/Raincloud plot.py
# - assets/original-scripts/figure-faceted grouped boxplot.py
#
# USER_DECISION_POINTS_BEFORE_USE:
# - distribution_mode: boxen_letter_value, violin_box, raincloud, faceted_boxplot
# - palette: threat_yellow_orange_red, chemical_multicolor, lcc_regions, regional_blue_magenta
# - overlays: raw jitter, mean diamond/dot, outliers, panel labels, significance brackets

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd

try:
    from scipy.stats import gaussian_kde
except ImportError:
    gaussian_kde = None


TEMPLATE_ID = "violin_boxplot"

FIELD_MAP = {
    "group": "group",
    "value": "value",
    "facet": "facet",
}

TEXT_CONFIG = {
    "title": "Amphibian",
    "x_label": "",
    "y_label": "log[Area of native\nhabitat (km$^2$)]",
}

STYLE_CONFIG = {
    "distribution_mode": "boxen_letter_value",
    "figsize": (3.5, 4.8),
    "dpi": 300,
    "font_family": "Arial",
    "font_size": 7.0,
    "axis_linewidth": 0.9,
    "panel_label": None,
    "show_grid": False,
}

EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "violin_boxplot",
    "formats": ["png", "pdf", "svg"],
    "dpi": 600,
}


PALETTES = {
    "threat_yellow_orange_red": ["#d8df27", "#d99036", "#c7191c"],
    "chemical_multicolor": [
        "#b5b6e6", "#d6c253", "#7eb6b4", "#f1b4bd", "#e6a2a9", "#c99b3f",
        "#e6c674", "#d1b064", "#d6a8c4", "#c5a6db", "#b5a1e6", "#dba9be",
    ],
    "lcc_regions": ["#75c8b4", "#ff9b72", "#9fb2d6", "#e89aca", "#a7d45a", "#a91d1d"],
    "regional_blue_magenta": ["#a23b92", "#1f77d0", "#a23b92", "#1f77d0", "#1f77d0", "#1f77d0"],
}


def apply_style(style: dict) -> None:
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": [style.get("font_family", "Arial"), "Arial", "DejaVu Sans"],
        "font.size": style["font_size"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.unicode_minus": False,
    })


def load_data(path: str | Path = "data.csv") -> pd.DataFrame:
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    rng = np.random.default_rng(42)
    mode = STYLE_CONFIG["distribution_mode"]
    rows = []
    if mode == "faceted_boxplot":
        panels = {
            "Latin America and the Caribbean": (["BRA", "MEX", "ARG"], [(1.4, 0.32), (0.75, 0.22), (0.35, 0.10)]),
            "Sub-Saharan Africa": (["NGA", "COD", "TZA"], [(3.4, 0.55), (0.95, 0.22), (0.75, 0.18)]),
            "Western Asia": (["IRQ", "TUR", "SYR"], [(0.78, 0.22), (0.45, 0.12), (0.32, 0.10)]),
            "Southern Asia": (["IND", "PAK", "BGD"], [(9.0, 1.6), (2.5, 0.45), (1.7, 0.30)]),
            "South-eastern Asia": (["IDN", "THA", "PHL"], [(3.4, 0.55), (1.0, 0.22), (0.75, 0.22)]),
            "Oceania": (["PNG", "SLB", "VUT"], [(0.12, 0.035), (0.012, 0.004), (0.008, 0.003)]),
        }
        for facet, (groups, params) in panels.items():
            for group, (mu, sd) in zip(groups, params):
                vals = np.clip(rng.normal(mu, sd, 180), 0, None)
                vals = np.concatenate([vals, np.clip(rng.normal(mu + 2.8 * sd, 0.5 * sd, 8), 0, None)])
                rows.extend({"facet": facet, "group": group, "value": v} for v in vals)
        return pd.DataFrame(rows)
    if mode == "violin_box":
        groups = [f"Class {i}" for i in range(1, 13)]
        means = np.linspace(2.6, 4.0, len(groups))
        for i, (group, mu) in enumerate(zip(groups, means)):
            vals = np.clip(rng.normal(mu, rng.uniform(0.25, 0.55), rng.integers(35, 80)), 1.6, 8.7)
            if i in [4, 7, 10]:
                vals = np.concatenate([vals, rng.normal(mu + 1.2, 0.45, 8)])
            rows.extend({"group": group, "value": v} for v in vals)
        return pd.DataFrame(rows)
    if mode == "raincloud":
        groups = ["TP", "NEP", "EP", "IMXJ", "YGP", "China"]
        params = [(1.0, 0.45), (0.55, 0.20), (0.45, 0.25), (0.75, 0.25), (2.1, 0.65), (0.8, 0.35)]
        for group, (mu, sd) in zip(groups, params):
            vals = np.clip(rng.normal(mu, sd, 80), 0, 5)
            vals = np.concatenate([vals, np.clip(rng.normal(mu + 1.4, sd, 12), 0, 5)])
            rows.extend({"group": group, "value": v} for v in vals)
        return pd.DataFrame(rows)
    groups = ["VU", "EN", "CR"]
    params = [(11.1, 0.85), (10.7, 0.80), (10.5, 0.90)]
    for group, (mu, sd) in zip(groups, params):
        vals = np.clip(rng.normal(mu, sd, 420), 6.2, 15.0)
        rows.extend({"group": group, "value": v} for v in vals)
    return pd.DataFrame(rows)


def prepare_data(df: pd.DataFrame, field_map: dict, style: dict) -> pd.DataFrame:
    cols = {
        "group": df[field_map["group"]].astype(str),
        "value": pd.to_numeric(df[field_map["value"]], errors="coerce"),
    }
    if field_map["facet"] in df.columns:
        cols["facet"] = df[field_map["facet"]].astype(str)
    return pd.DataFrame(cols).dropna()


def draw_boxen(ax, values, x, color, width=0.82):
    values = np.asarray(values)
    jitter = np.random.default_rng(42).normal(0, 0.035, size=len(values))
    ax.scatter(np.full_like(values, x) + jitter, values, s=7, color="0.60", alpha=0.18, zorder=1)
    q_low, q_high = np.quantile(values, [0.025, 0.975])
    ax.plot([x, x], [q_low, q_high], color="0.35", linewidth=1.0, alpha=0.65, zorder=2)
    for q1, q2, w_scale in [(0.025, 0.050, 0.18), (0.050, 0.100, 0.28), (0.100, 0.200, 0.42), (0.200, 0.350, 0.58), (0.350, 0.650, 1.00), (0.650, 0.800, 0.58), (0.800, 0.900, 0.42), (0.900, 0.950, 0.28), (0.950, 0.975, 0.18)]:
        y1, y2 = np.quantile(values, [q1, q2])
        rect_width = width * w_scale
        ax.add_patch(Rectangle((x - rect_width / 2, y1), rect_width, y2 - y1, facecolor=color, edgecolor="0.35", linewidth=0.65, alpha=0.82, zorder=3))
    ax.plot([x - width * 0.48, x + width * 0.48], [np.median(values), np.median(values)], color="0.25", linewidth=1.0, zorder=4)
    ax.scatter(x, np.mean(values), marker="D", s=20, color="black", edgecolor="none", zorder=5)


def draw_half_violin(ax, values, x, color, width=0.33, y_min=0, y_max=5.0):
    if gaussian_kde is None or len(values) < 3:
        return
    y_grid = np.linspace(y_min, y_max, 240)
    density = gaussian_kde(values, bw_method=0.30)(y_grid)
    density = density / density.max() * width
    ax.fill_betweenx(y_grid, np.full_like(y_grid, x), x + density, facecolor=color, edgecolor="none", alpha=0.78, zorder=1)


def plot_boxen(data, text, style):
    colors = PALETTES["threat_yellow_orange_red"]
    groups = list(dict.fromkeys(data["group"]))
    fig, ax = plt.subplots(figsize=style["figsize"], dpi=style["dpi"])
    for i, group in enumerate(groups, start=1):
        draw_boxen(ax, data.loc[data["group"] == group, "value"], i, colors[(i - 1) % len(colors)])
    ax.set_xlim(0.48, len(groups) + 0.52)
    ax.set_ylim(6, 15.1)
    ax.set_xticks(range(1, len(groups) + 1))
    ax.set_xticklabels(groups, fontsize=style["font_size"] + 5)
    ax.set_yticks([6, 9, 11, 13, 15])
    ax.set_title(text["title"], fontsize=style["font_size"] + 6, pad=10)
    ax.set_ylabel(text["y_label"], fontsize=style["font_size"] + 5, labelpad=12)
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_linewidth(1.0)
    return fig


def plot_violin_box(data, text, style):
    groups = list(dict.fromkeys(data["group"]))
    values = [data.loc[data["group"] == g, "value"].to_numpy() for g in groups]
    colors = (PALETTES["chemical_multicolor"] * 4)[:len(groups)]
    fig, ax = plt.subplots(figsize=(3.5, 3.2), dpi=style["dpi"])
    positions = np.arange(1, len(groups) + 1)
    violins = ax.violinplot(values, positions=positions, widths=0.75, showmeans=False, showmedians=False, showextrema=False)
    for body, color in zip(violins["bodies"], colors):
        body.set_facecolor(color)
        body.set_edgecolor("none")
        body.set_alpha(0.75)
    box = ax.boxplot(values, positions=positions, widths=0.42, patch_artist=True, showfliers=False,
                     medianprops=dict(color="black", linewidth=1.1),
                     boxprops=dict(facecolor="white", edgecolor="black", linewidth=0.8, alpha=0.75),
                     whiskerprops=dict(color="black", linewidth=0.8), capprops=dict(color="black", linewidth=0.8))
    for patch, color in zip(box["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.45)
    rng = np.random.default_rng(42)
    for x, vals in zip(positions, values):
        outliers = np.sort(vals)[-3:]
        ax.scatter(np.full(len(outliers), x) + rng.normal(0, 0.035, len(outliers)), outliers, s=8, color="black", edgecolor="none", zorder=5)
    ax.set_xticks(positions)
    ax.set_xticklabels(groups, rotation=90, fontsize=style["font_size"] - 0.5)
    ax.set_ylabel("uncertainty (95% CI width)", fontsize=style["font_size"] + 1)
    ax.grid(axis="y", color="0.82", linewidth=0.6, alpha=0.9)
    ax.grid(axis="x", color="0.90", linewidth=0.45, alpha=0.5)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_linewidth(0.8)
        spine.set_color("0.25")
    return fig


def plot_raincloud(data, text, style):
    groups = list(dict.fromkeys(data["group"]))
    colors = PALETTES["lcc_regions"]
    fig, ax = plt.subplots(figsize=(3.5, 2.15), dpi=style["dpi"])
    positions = np.arange(1, len(groups) + 1)
    rng = np.random.default_rng(42)
    for x, group, color in zip(positions, groups, colors):
        values = data.loc[data["group"] == group, "value"].to_numpy()
        draw_half_violin(ax, values, x + 0.08, color, y_min=0, y_max=5.0)
        ax.scatter(np.full_like(values, x) + rng.normal(-0.05, 0.045, len(values)), values, s=10, color=color, alpha=0.42, edgecolor="white", linewidth=0.25, zorder=3)
        ax.boxplot(values, positions=[x], widths=0.18, patch_artist=True, showfliers=False,
                   medianprops=dict(color="black", linewidth=1.1),
                   boxprops=dict(facecolor="white", edgecolor="black", linewidth=0.9, alpha=0.78),
                   whiskerprops=dict(color="black", linewidth=0.8), capprops=dict(color="black", linewidth=0.8))
        ax.scatter(x, np.mean(values), s=16, color=color, edgecolor="black", linewidth=0.35, zorder=5)
    ax.set_xlim(0.4, len(groups) + 0.7)
    ax.set_ylim(-0.25, 5.25)
    ax.set_xticks(positions)
    ax.set_xticklabels(groups, fontsize=style["font_size"])
    ax.set_ylabel("LCC magnitude(C)", fontsize=style["font_size"] + 1, fontweight="bold")
    ax.grid(True, axis="both", color="0.88", linewidth=0.8, alpha=0.85)
    ax.set_axisbelow(True)
    ax.text(0.01, 0.98, "(a)", transform=ax.transAxes, ha="left", va="top", fontsize=style["font_size"] + 4, fontweight="bold")
    for spine in ax.spines.values():
        spine.set_linewidth(0.9)
    return fig


def plot_faceted_boxplot(data, text, style):
    facets = list(dict.fromkeys(data["facet"]))
    colors = PALETTES["regional_blue_magenta"]
    fig, axes = plt.subplots(1, len(facets), figsize=(3.5, 1.35), dpi=style["dpi"], sharey=False)
    if len(facets) == 1:
        axes = [axes]
    plt.subplots_adjust(left=0.05, right=0.995, top=0.78, bottom=0.25, wspace=0.38)
    for ax, facet, color in zip(axes, facets, colors):
        sub = data[data["facet"] == facet]
        groups = list(dict.fromkeys(sub["group"]))
        values = [sub.loc[sub["group"] == g, "value"].to_numpy() for g in groups]
        ax.boxplot(values, positions=np.arange(1, len(groups) + 1), widths=0.58, patch_artist=True, showfliers=True,
                   medianprops=dict(color=color, linewidth=1.0),
                   boxprops=dict(facecolor="white", edgecolor=color, linewidth=0.8),
                   whiskerprops=dict(color=color, linewidth=0.8),
                   capprops=dict(color=color, linewidth=0.8),
                   flierprops=dict(marker="o", markerfacecolor=color, markeredgecolor=color, markersize=1.2, alpha=0.75))
        ax.set_title(facet, fontsize=style["font_size"] - 1, pad=5)
        ax.set_xticks(np.arange(1, len(groups) + 1))
        ax.set_xticklabels(groups, fontsize=style["font_size"] - 1)
        ax.tick_params(axis="both", direction="out", length=2.5, width=0.7, labelsize=style["font_size"] - 1, pad=2)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_linewidth(0.7)
        ax.spines["bottom"].set_linewidth(0.7)
    return fig


def plot(data: pd.DataFrame, text: dict, style: dict) -> plt.Figure:
    apply_style(style)
    mode = style["distribution_mode"]
    if mode == "violin_box":
        return plot_violin_box(data, text, style)
    if mode == "raincloud":
        return plot_raincloud(data, text, style)
    if mode == "faceted_boxplot":
        return plot_faceted_boxplot(data, text, style)
    return plot_boxen(data, text, style)


def save_outputs(fig: plt.Figure, export: dict) -> list[Path]:
    output_dir = Path(export["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for fmt in export["formats"]:
        path = output_dir / f"{export['basename']}.{fmt}"
        kwargs = {"bbox_inches": "tight", "pad_inches": 0.04}
        if fmt.lower() == "png":
            kwargs["dpi"] = export["dpi"]
        fig.savefig(path, **kwargs)
        paths.append(path)
    plt.close(fig)
    return paths


def main() -> None:
    df = load_data(sys.argv[1] if len(sys.argv) > 1 else "data.csv")
    data = prepare_data(df, FIELD_MAP, STYLE_CONFIG)
    fig = plot(data, TEXT_CONFIG, STYLE_CONFIG)
    print("Generated:", [str(p) for p in save_outputs(fig, EXPORT_CONFIG)])


if __name__ == "__main__":
    main()
