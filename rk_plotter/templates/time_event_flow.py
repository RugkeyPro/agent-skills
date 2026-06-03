# TEMPLATE_ID: time_event_flow
# TEMPLATE_VERSION: 1.0
# FIGURE_TYPE: high_fidelity_timeseries_timeline_and_flow_diagrams
#
# IMAGE-DERIVED MODES:
# - ensemble_timeseries: multi-model thin lines with thick ensemble line
# - event_timeline: horizontal discovery timeline with alternating labels/arrows
# - paired_slope: paired before-after slope plot
# - sankey_multistage: pastel multi-stage sankey
# - alluvial_survival: two-color survival-style alluvial
# - ternary_bubble: ternary bubble plot with size and color legends

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.path import Path as MplPath
from matplotlib.patches import PathPatch, Rectangle, FancyArrowPatch
import numpy as np
import pandas as pd


TEMPLATE_ID = "time_event_flow"
FIELD_MAP = {"x": "x", "y": "y", "group": "group"}
TEXT_CONFIG = {"x_label": "", "y_label": "W m$^{-2}$", "title": ""}
STYLE_CONFIG = {"mode": "ensemble_timeseries", "figsize": (3.5, 1.25), "dpi": 300, "font_family": "Arial", "font_size": 7.0}
EXPORT_CONFIG = {"output_dir": "outputs", "basename": "time_event_flow", "formats": ["png", "pdf", "svg"], "dpi": 600}


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


def load_data(path: str | Path = "data.csv"):
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    return pd.DataFrame()


def prepare_data(df, field_map, style):
    return df


def style_axes(ax):
    for sp in ax.spines.values():
        sp.set_linewidth(0.8)
    ax.tick_params(direction="out", length=3, width=0.7)


def plot_ensemble(style, text):
    rng = np.random.default_rng(42)
    fig, ax = plt.subplots(figsize=style["figsize"], dpi=style["dpi"])
    years = np.linspace(2000, 2017, 160)
    colors = ["#356b45", "#4cb3c7", "#7868a6", "#8ea448", "#2f4b6e", "#5b559e", "#7eb8b2"]
    models = ["CanESM5", "CESM2", "EC-Earth3-Veg", "ECHAM6.3", "GFDL-AM4", "HadGEM3", "IPSL-CM6A"]
    all_y = []
    for i, (color, name) in enumerate(zip(colors, models)):
        noise = np.cumsum(rng.normal(0, 0.06, len(years)))
        y = 0.25 * np.sin(years * 1.6 + i) + 0.25 * np.cos(years * 0.7) + noise
        y = y - y.mean()
        all_y.append(y)
        ax.plot(years, y, color=color, linewidth=0.9, alpha=0.85, label=name)
    ens = np.mean(all_y, axis=0)
    ax.plot(years, ens, color="black", linewidth=2.2)
    ax.plot(years, ens * 0.75, color="#b00000", linewidth=2.0)
    ax.axhline(0, color="0.45", linewidth=0.8)
    ax.set_xlim(2000, 2018)
    ax.set_ylim(-1.25, 1.25)
    ax.set_ylabel(text["y_label"])
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.18), frameon=False, fontsize=style["font_size"] - 0.5)
    style_axes(ax)
    return fig


def plot_timeline(style):
    fig, ax = plt.subplots(figsize=(3.5, 1.1), dpi=style["dpi"])
    ax.set_xlim(2012.8, 2018.8)
    ax.set_ylim(-1.1, 1.1)
    ax.axis("off")
    ax.annotate("", xy=(2018.75, 0), xytext=(2013, 0), arrowprops=dict(arrowstyle="->", lw=1.6, color="black"))
    years = np.arange(2013, 2019)
    labels = ["DetectorNet\n(Szegedy et al.)", "RCNN\n(Girshick et al.)", "Fast RCNN\n(Girshick)", "ResNet\n(He et al.)", "YOLO9000\n(Redmon and Farhadi)", "CornerNet\n(Law and Deng)"]
    for i, yr in enumerate(years):
        ax.scatter([yr], [0], s=18, color="red", zorder=5)
        ax.text(yr - 0.05, 0.22, str(yr), rotation=35, color="red", fontsize=style["font_size"], fontweight="bold")
    events = np.linspace(2013.4, 2018.2, len(labels))
    for i, (x, lab) in enumerate(zip(events, labels)):
        y = 0.72 if i % 2 else -0.72
        ax.plot([x, x], [0, y * 0.72], color="#2d5c9b", linewidth=1.7)
        ax.scatter([x], [0], s=20, color="#2d5c9b")
        ax.text(x, y, lab, ha="center", va="center", fontsize=style["font_size"], fontstyle="italic")
    return fig


def plot_paired(style):
    rng = np.random.default_rng(42)
    fig, ax = plt.subplots(figsize=(1.65, 2.65), dpi=style["dpi"])
    pre = np.sort(rng.uniform(0.0, 0.7, 12))
    post = np.clip(pre + rng.normal(0.35, 0.25, 12), 0, 1)
    for a, b in zip(pre, post):
        ax.plot([0, 1], [a, b], color="0.45", linewidth=1.0, zorder=1)
    ax.scatter(np.zeros_like(pre), pre, color="#1f78b4", s=28, zorder=3)
    ax.scatter(np.ones_like(post), post, color="#f21a12", s=28, zorder=3)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["GBM", "PDGC"], fontsize=style["font_size"] + 5)
    ax.set_ylabel("MYC pathway score", fontsize=style["font_size"] + 4)
    ax.set_ylim(-0.05, 1.05)
    ax.text(0.05, 0.96, "In-house data\n$p$ = 0.012", transform=ax.transAxes, va="top", fontsize=style["font_size"] + 3)
    style_axes(ax)
    return fig


def ribbon(ax, x0, y0, x1, y1, width, color, alpha=0.35):
    verts = [
        (x0, y0 - width / 2), ((x0 + x1) / 2, y0 - width / 2), ((x0 + x1) / 2, y1 - width / 2), (x1, y1 - width / 2),
        (x1, y1 + width / 2), ((x0 + x1) / 2, y1 + width / 2), ((x0 + x1) / 2, y0 + width / 2), (x0, y0 + width / 2),
        (x0, y0 - width / 2),
    ]
    codes = [MplPath.MOVETO, MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4, MplPath.LINETO, MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4, MplPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MplPath(verts, codes), facecolor=color, edgecolor="none", alpha=alpha))


def plot_sankey(style, survival=False):
    fig, ax = plt.subplots(figsize=(3.5, 2.1), dpi=style["dpi"])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    rng = np.random.default_rng(42)
    columns = [["Glycolysis", "TCA Cycle", "Lipid Metabolism", "Amino Acid"], ["Adenocarcinoma", "Small Cell", "Squamous Cell", "Large Cell"], ["Asia", "Europe", "North America"]]
    if survival:
        columns = [["First", "Second", "Third", "Crew"], ["Female", "Male"], ["Adult", "Child"], ["Alive", "Dead"]]
    xs = np.linspace(0.04, 0.94, len(columns))
    colors = ["#e41a1c", "#377eb8"] if survival else ["#d8c84e", "#6c67aa", "#b15e9f", "#8fc05a", "#e44d45", "#e96a3d", "#71b59b", "#eaa33f"]
    node_pos = []
    for ci, labels in enumerate(columns):
        ys = np.linspace(0.86, 0.14, len(labels))
        node_pos.append(dict(zip(labels, ys)))
        for li, (lab, y) in enumerate(zip(labels, ys)):
            c = colors[li % len(colors)] if not survival else colors[li % 2]
            ax.add_patch(Rectangle((xs[ci] - 0.012, y - 0.035), 0.024, 0.07, facecolor=c, edgecolor="0.45", lw=0.35, alpha=0.9))
            ax.text(xs[ci] + (0.018 if ci == 0 else -0.018 if ci == len(columns) - 1 else 0.018), y, lab, va="center", ha="left" if ci < len(columns) - 1 else "right", fontsize=style["font_size"] - 0.5)
    for ci in range(len(columns) - 1):
        for src in columns[ci]:
            for dst in columns[ci + 1]:
                if rng.random() < (0.55 if not survival else 0.75):
                    c = colors[0 if (survival and dst in {"Alive", "Female"}) else rng.integers(0, len(colors))]
                    ribbon(ax, xs[ci] + 0.012, node_pos[ci][src], xs[ci + 1] - 0.012, node_pos[ci + 1][dst], rng.uniform(0.006, 0.025), c, alpha=0.25 if not survival else 0.22)
    if survival:
        ax.legend(handles=[Patch(color="#e41a1c", label="Alive"), Patch(color="#377eb8", label="Dead")], loc="upper right", frameon=False, ncol=2)
    return fig


def ternary_to_xy(a, b, c):
    s = a + b + c
    a, b, c = a / s, b / s, c / s
    x = b + 0.5 * c
    y = np.sqrt(3) / 2 * c
    return x, y


def plot_ternary(style):
    rng = np.random.default_rng(42)
    fig, ax = plt.subplots(figsize=(3.5, 2.8), dpi=style["dpi"])
    ax.axis("off")
    tri = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3) / 2], [0, 0]])
    ax.plot(tri[:, 0], tri[:, 1], color="0.45", lw=1.0)
    for t in np.linspace(0.2, 0.8, 4):
        ax.plot([t, 0.5 + t / 2], [0, np.sqrt(3) / 2 * (1 - t)], "--", color="0.85", lw=0.6)
        ax.plot([1 - t, (1 - t) / 2], [0, np.sqrt(3) / 2 * (1 - t)], "--", color="0.85", lw=0.6)
        ax.plot([t / 2, 1 - t / 2], [np.sqrt(3) / 2 * t, np.sqrt(3) / 2 * t], "--", color="0.85", lw=0.6)
    vals = rng.dirichlet([5, 4, 3], 120)
    x, y = ternary_to_xy(vals[:, 0], vals[:, 1], vals[:, 2])
    score = rng.uniform(15, 85, len(x))
    sizes = rng.uniform(40, 150, len(x))
    sc = ax.scatter(x, y, s=sizes, c=score, cmap="RdBu_r", edgecolor="0.4", linewidth=0.4, alpha=0.85)
    ax.text(0.5, -0.08, "Stromal fraction", ha="center", va="top", color="#496a9f")
    ax.text(-0.06, 0.46, "Immune fraction", rotation=58, ha="center", color="#11a889")
    ax.text(1.05, 0.46, "Metabolic fraction", rotation=-58, ha="center", color="#e45b47")
    cbar = fig.colorbar(sc, ax=ax, fraction=0.03, pad=0.05)
    cbar.set_label("Pathway score")
    return fig


def plot(data, text, style):
    apply_style(style)
    mode = style["mode"]
    if mode == "event_timeline":
        return plot_timeline(style)
    if mode == "paired_slope":
        return plot_paired(style)
    if mode == "sankey_multistage":
        return plot_sankey(style, False)
    if mode == "alluvial_survival":
        return plot_sankey(style, True)
    if mode == "ternary_bubble":
        return plot_ternary(style)
    return plot_ensemble(style, text)


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
