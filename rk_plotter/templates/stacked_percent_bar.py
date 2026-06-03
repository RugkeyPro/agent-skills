# TEMPLATE_ID: stacked_percent_bar
# TEMPLATE_VERSION: 2.0
# FIGURE_TYPE: high_fidelity_environmental_composition_bar_charts
#
# HIGH_FIDELITY_SOURCES:
# - assets/original-scripts/figure-100%_stacked_bar_chart.py
# - assets/new-scripts/horizontal 100% stacked bar chart.py
# - assets/original-scripts/figure-diverging stacked bar chart.py
# - assets/original-scripts/figure-stacked percentage bar + multi-line chart with secondary y-axis.py
#
# USER_DECISION_POINTS_BEFORE_USE:
# - bar_mode: vertical_percent, horizontal_percent, diverging_total, stacked_line
# - palette: hfi_green_blue_black, observation_blue_red, carbon_blue_orange, plastic_pastels
# - legend: bottom multi-column, top compact, split positive/negative, or split bar/line
# - annotations: country/group labels above bars, panel label, reference line, secondary-axis lines

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import numpy as np
import pandas as pd


TEMPLATE_ID = "stacked_percent_bar"

FIELD_MAP = {
    "group": "group",
    "components": ["A", "B", "C", "D", "E"],
    "line_series": ["line_1", "line_2", "line_3"],
}

TEXT_CONFIG = {
    "title": "Native habitats",
    "x_label": "Hotspot value quantile (%)",
    "y_label": "Proportion (%)",
    "legend_title": "HFI Levels",
    "secondary_y_label": "Ingestion risk index",
}

STYLE_CONFIG = {
    "bar_mode": "vertical_percent",
    "figsize": (3.5, 2.7),
    "dpi": 300,
    "font_family": "Arial",
    "font_size": 6.8,
    "bar_width": 0.62,
    "bar_height": 0.55,
    "axis_linewidth": 0.8,
    "grid_color": "0.88",
    "palette": "hfi_green_blue_black",
    "panel_label": None,
}

EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "stacked_percent_bar",
    "formats": ["png", "pdf", "svg"],
    "dpi": 600,
}


PALETTES = {
    "hfi_green_blue_black": {
        "labels": ["0 (No pressure)", "1-2 (Low pressure)", "3-5 (Moderate pressure)", "6-11 (High pressure)", "12-50 (Very high pressure)"],
        "colors": ["#d9f2e3", "#45bfa9", "#2f7fa3", "#46366f", "#0b0303"],
    },
    "observation_blue_red": {
        "labels": ["Low value", "<10", "10-20", "20-40", "40-80", ">80"],
        "colors": ["#d9d9d9", "#4f7fb9", "#8fa9b8", "#f4f3b5", "#f4a36e", "#df3b2f"],
    },
    "carbon_blue_orange": {
        "labels": ["Buried carbon from beached plastic", "Buried carbon from sedimented plastic", "Sedimented plastic", "Beached plastic"],
        "colors": ["#b8d2ec", "#4f94cf", "#f07f2f", "#f6c6a6"],
    },
    "plastic_pastels": {
        "labels": ["PP", "PE", "PVC", "PS", "ABS"],
        "colors": ["#e8d790", "#cfd6dc", "#9fd9df", "#d9cbd4", "#8b89aa"],
    },
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
    mode = STYLE_CONFIG["bar_mode"]
    rng = np.random.default_rng(42)
    if mode == "horizontal_percent":
        groups = ["India", "Venezuela", "Thailand", "Viet Nam", "Pakistan", "Myanmar", "Indonesia", "Iran", "Japan", "Colombia", "Turkey", "Chile"]
        raw = rng.uniform(2, 40, (len(groups), 6))
        avg = np.linspace(39.0, 23.0, len(groups))
        df = pd.DataFrame(raw, columns=["A", "B", "C", "D", "E", "F"])
        df.insert(0, "avg_label", avg)
        df.insert(0, "group", groups)
        return df
    if mode == "stacked_line":
        body = [1, 2, 3, 4, 6, 9, 13, 18, 27, 39, 58, 84, 123, 180, 263, 385]
        x = np.arange(len(body))
        raw = np.vstack([
            np.interp(x, [0, 8, 15], [0, 5, 30]),
            np.interp(x, [0, 8, 15], [5, 3, 18]),
            np.interp(x, [0, 8, 15], [45, 42, 28]),
            np.interp(x, [0, 8, 15], [35, 36, 20]),
            np.interp(x, [0, 8, 15], [15, 14, 7]),
        ]) + rng.normal(0, 1.2, (5, len(body)))
        raw = np.clip(raw, 0.2, None)
        pct = raw / raw.sum(axis=0) * 100
        df = pd.DataFrame(pct.T, columns=["A", "B", "C", "D", "E"])
        df.insert(0, "group", [str(v) for v in body])
        df["line_1"] = 6 + 2 * np.sin(x / 2)
        df["line_2"] = 3 + 1.1 * np.cos(x / 3)
        df["line_3"] = 9 + 4 * np.exp(-x / 9)
        return df
    if mode == "diverging_total":
        groups = ["ABS", "PS", "PVC", "PP", "PE"]
        return pd.DataFrame({
            "group": groups,
            "positive_1": [3, 10, 6, 7, 10],
            "positive_2": [4, 8, 5, 20, 25],
            "negative_1": [3, 9, 15, 7, 10],
            "negative_2": [4, 7, 8, 18, 22],
        })
    quantiles = np.arange(0, 101, 10)
    raw = np.array([
        [48, 22, 17, 16, 24, 22, 14, 8, 19, 15, 8],
        [18, 12, 20, 18, 17, 16, 17, 15, 16, 21, 7],
        [14, 20, 29, 26, 21, 27, 30, 29, 28, 22, 21],
        [12, 24, 25, 22, 21, 22, 23, 27, 30, 23, 29],
        [8, 22, 9, 18, 17, 13, 16, 21, 7, 19, 35],
    ]).T
    df = pd.DataFrame(raw, columns=["A", "B", "C", "D", "E"])
    df.insert(0, "group", quantiles)
    return df


def prepare_data(df: pd.DataFrame, field_map: dict, style: dict) -> pd.DataFrame:
    out = df.copy()
    comps = [c for c in field_map["components"] if c in out.columns]
    if style["bar_mode"] in {"vertical_percent", "horizontal_percent", "stacked_line"}:
        row_sums = out[comps].sum(axis=1).replace(0, np.nan)
        out[comps] = out[comps].div(row_sums, axis=0) * 100
    return out


def current_palette(style: dict) -> dict:
    if style["bar_mode"] == "horizontal_percent":
        return PALETTES["observation_blue_red"]
    if style["bar_mode"] == "diverging_total":
        return PALETTES["carbon_blue_orange"]
    if style["bar_mode"] == "stacked_line":
        return PALETTES["plastic_pastels"]
    return PALETTES[style["palette"]]


def add_panel_label(fig, style: dict) -> None:
    if style.get("panel_label"):
        fig.text(0.02, 0.96, style["panel_label"], fontsize=style["font_size"] + 2, fontweight="bold", ha="left", va="top")


def plot_vertical_percent(data: pd.DataFrame, text: dict, style: dict) -> plt.Figure:
    pal = current_palette(style)
    comps = [c for c in FIELD_MAP["components"] if c in data.columns]
    colors = pal["colors"][:len(comps)]
    labels = pal["labels"][:len(comps)]
    fig, ax = plt.subplots(figsize=style["figsize"], dpi=style["dpi"])
    x_numeric = pd.to_numeric(data["group"], errors="coerce")
    x = np.where(x_numeric.notna(), x_numeric.to_numpy(), np.arange(len(data)))
    bottom = np.zeros(len(data))
    order = list(range(len(comps) - 1, -1, -1))
    for i in order:
        ax.bar(x, data[comps[i]], bottom=bottom, width=8.8 if len(x) > 6 else style["bar_width"],
               color=colors[i], edgecolor="white", linewidth=0.8, align="center", label=labels[i])
        bottom += data[comps[i]].to_numpy()
    ax.set_xlim(x.min() - 2, x.max() + 2)
    ax.set_ylim(0, 105)
    ax.set_xticks(x)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_title(text["title"], fontsize=style["font_size"] + 2, pad=6)
    ax.set_xlabel(text["x_label"], fontsize=style["font_size"] + 1)
    ax.set_ylabel(text["y_label"], fontsize=style["font_size"] + 1)
    ax.grid(axis="y", color=style["grid_color"], linewidth=0.55)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_linewidth(style["axis_linewidth"])
    handles = [Patch(facecolor=c, edgecolor="none", label=l) for c, l in zip(colors, labels)]
    leg = ax.legend(handles=handles, title=text["legend_title"], ncol=2, frameon=False, fontsize=style["font_size"],
                    title_fontsize=style["font_size"] + 0.5, loc="upper center", bbox_to_anchor=(0.5, -0.26),
                    handlelength=0.9, handleheight=0.8, columnspacing=1.0, handletextpad=0.35)
    leg._legend_box.align = "left"
    add_panel_label(fig, style)
    return fig


def plot_horizontal_percent(data: pd.DataFrame, text: dict, style: dict) -> plt.Figure:
    pal = current_palette(style)
    comps = [c for c in ["A", "B", "C", "D", "E", "F"] if c in data.columns]
    colors = pal["colors"][:len(comps)]
    labels = pal["labels"][:len(comps)]
    fig, ax = plt.subplots(figsize=(3.5, 5.2), dpi=style["dpi"])
    y = np.arange(len(data))[::-1] * 1.18
    left = np.zeros(len(data))
    for comp, color in zip(comps, colors):
        ax.barh(y, data[comp], left=left, height=style["bar_height"], color=color, edgecolor="black", linewidth=0.55, zorder=3)
        left += data[comp].to_numpy()
    for yi, group, avg in zip(y, data["group"], data.get("avg_label", pd.Series([np.nan] * len(data)))):
        label = f"{group}: {avg:.2f}%" if np.isfinite(avg) else str(group)
        ax.text(1.0, yi + 0.40, label, ha="left", va="center", fontsize=style["font_size"], fontweight="bold")
    ax.set_xlim(0, 100)
    ax.set_yticks([])
    ax.set_xlabel("Percentage (%)", fontsize=style["font_size"] + 1, fontweight="bold")
    ax.set_ylabel("Countries", fontsize=style["font_size"] + 2, fontweight="bold", labelpad=8)
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    for spine in ax.spines.values():
        spine.set_linewidth(0.8)
    handles = [Patch(facecolor=c, edgecolor="black", linewidth=0.55, label=l) for c, l in zip(colors, labels)]
    leg = ax.legend(handles=handles, title="SWOT observation times per year", loc="upper center",
                    bbox_to_anchor=(0.50, 1.065), ncol=3, frameon=False, fontsize=style["font_size"],
                    title_fontsize=style["font_size"] + 0.8, handlelength=1.1, handleheight=0.8,
                    handletextpad=0.35, columnspacing=0.55, borderpad=0.1)
    leg.get_title().set_fontweight("bold")
    return fig


def plot_diverging_total(data: pd.DataFrame, text: dict, style: dict) -> plt.Figure:
    pal = current_palette(style)
    colors = dict(zip(["positive_2", "positive_1", "negative_1", "negative_2"], pal["colors"]))
    fig = plt.figure(figsize=(3.5, 1.65), dpi=style["dpi"])
    gs = GridSpec(1, 2, width_ratios=[5.3, 1.45], wspace=0.07)
    ax = fig.add_subplot(gs[0, 0])
    ax_total = fig.add_subplot(gs[0, 1])
    x = np.arange(len(data))
    for target_ax, subset, width in [(ax, data, 0.34), (ax_total, data.mean(numeric_only=True).to_frame().T, 0.36)]:
        xpos = x if target_ax is ax else [0]
        target_ax.bar(xpos, subset["positive_1"], width=width, color=colors["positive_1"], edgecolor="black", linewidth=0.35, zorder=3)
        target_ax.bar(xpos, subset["positive_2"], bottom=subset["positive_1"], width=width, color=colors["positive_2"], edgecolor="black", linewidth=0.35, zorder=3)
        target_ax.bar(xpos, -subset["negative_1"], width=width, color=colors["negative_1"], edgecolor="black", linewidth=0.35, zorder=3)
        target_ax.bar(xpos, -subset["negative_2"], bottom=-subset["negative_1"], width=width, color=colors["negative_2"], edgecolor="black", linewidth=0.35, zorder=3)
        target_ax.axhline(0, color="black", linewidth=0.8, zorder=2)
        for spine in target_ax.spines.values():
            spine.set_linewidth(0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(data["group"], fontsize=style["font_size"])
    ax.set_ylabel("Proportion (%)", fontsize=style["font_size"] + 0.5)
    ax.set_yticks([-40, -20, 0, 20, 40])
    ax.set_yticklabels(["40", "20", "0", "20", "40"], fontsize=style["font_size"])
    ax_total.set_xticks([0])
    ax_total.set_xticklabels(["Total"], fontsize=style["font_size"])
    ax_total.yaxis.tick_right()
    handles_top = [Patch(facecolor=colors["positive_2"], edgecolor="black", linewidth=0.35, label=pal["labels"][0]),
                   Patch(facecolor=colors["positive_1"], edgecolor="black", linewidth=0.35, label=pal["labels"][1])]
    handles_bottom = [Patch(facecolor=colors["negative_1"], edgecolor="black", linewidth=0.35, label=pal["labels"][2]),
                      Patch(facecolor=colors["negative_2"], edgecolor="black", linewidth=0.35, label=pal["labels"][3])]
    leg1 = ax.legend(handles=handles_top, loc="upper left", bbox_to_anchor=(0.0, 1.03), frameon=False, fontsize=style["font_size"], handlelength=1.0)
    ax.legend(handles=handles_bottom, loc="lower left", bbox_to_anchor=(0.0, -0.02), frameon=False, fontsize=style["font_size"], handlelength=1.0)
    ax.add_artist(leg1)
    return fig


def plot_stacked_line(data: pd.DataFrame, text: dict, style: dict) -> plt.Figure:
    pal = current_palette(style)
    comps = [c for c in FIELD_MAP["components"] if c in data.columns]
    fig, ax1 = plt.subplots(figsize=(3.5, 2.25), dpi=style["dpi"])
    x = np.arange(len(data))
    bottom = np.zeros(len(data))
    for comp, color in zip(comps, pal["colors"]):
        ax1.bar(x, data[comp], bottom=bottom, width=0.66, color=color, edgecolor="white", linewidth=0.45, zorder=2)
        bottom += data[comp].to_numpy()
    ax1.set_ylim(0, 110)
    ax1.set_ylabel("Contribution ratio (%)", fontsize=style["font_size"])
    ax1.set_xlabel("Body size (mm)", fontsize=style["font_size"])
    ax1.set_xticks(x[::2])
    ax1.set_xticklabels(data["group"].iloc[::2], fontsize=style["font_size"] - 0.5)
    ax2 = ax1.twinx()
    line_specs = [("#ff7f00", "o", "Epipelagic index"), ("#d9481d", "^", "Migratory index"), ("#2f5da8", "s", "Mesopelagic index")]
    for col, (color, marker, label) in zip(FIELD_MAP["line_series"], line_specs):
        ax2.plot(x, data[col], color=color, marker=marker, markersize=3, linewidth=1.4, label=label, zorder=5)
    ax2.set_ylabel(text["secondary_y_label"], fontsize=style["font_size"], rotation=270, labelpad=11)
    for ax in [ax1, ax2]:
        for spine in ax.spines.values():
            spine.set_linewidth(0.8)
        ax.spines["top"].set_visible(False)
    plastic_handles = [Patch(facecolor=c, edgecolor="none", label=l) for c, l in zip(pal["colors"], pal["labels"])]
    line_handles = [Line2D([0], [0], color=c, marker=m, markersize=3, linewidth=1.2, label=l) for c, m, l in line_specs]
    leg1 = ax1.legend(handles=plastic_handles, loc="upper center", bbox_to_anchor=(0.50, -0.19), ncol=5, frameon=False, fontsize=style["font_size"] - 0.2, handlelength=0.8)
    ax1.legend(handles=line_handles, loc="upper center", bbox_to_anchor=(0.50, -0.30), ncol=2, frameon=False, fontsize=style["font_size"] - 0.2, handlelength=0.9)
    ax1.add_artist(leg1)
    return fig


def plot(data: pd.DataFrame, text: dict, style: dict) -> plt.Figure:
    apply_style(style)
    mode = style["bar_mode"]
    if mode == "horizontal_percent":
        return plot_horizontal_percent(data, text, style)
    if mode == "diverging_total":
        return plot_diverging_total(data, text, style)
    if mode == "stacked_line":
        return plot_stacked_line(data, text, style)
    return plot_vertical_percent(data, text, style)


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
