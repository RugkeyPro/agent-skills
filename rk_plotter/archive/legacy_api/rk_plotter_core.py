from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping, Sequence

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "none"

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import FancyArrowPatch, Rectangle
import numpy as np

DEFAULT_FORMATS = ("png", "pdf", "svg")
FIG_SIZES = {"single": (3.46, 3.0), "square": (3.46, 3.46), "wide": (7.2, 3.8), "map": (7.2, 4.0), "tall": (3.46, 4.8), "framework": (7.2, 4.8)}
PALETTES = {
    "categorical": ["#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377", "#BBBBBB", "#000000"],
    "scenario": ["#1B9E77", "#D95F02", "#7570B3", "#E7298A", "#66A61E", "#E6AB02"],
    "model": ["#4C78A8", "#F58518", "#54A24B", "#B279A2", "#E45756"],
    "sequential": "viridis",
    "diverging": "RdBu_r",
    "log": "magma_r",
}


def apply_style(style: Mapping | None = None) -> None:
    style = dict(style or {})
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans", "Microsoft YaHei"],
        "font.size": style.get("font.size", 8.5),
        "axes.titlesize": style.get("axes.titlesize", 9.5),
        "axes.labelsize": style.get("axes.labelsize", 8.5),
        "xtick.labelsize": style.get("xtick.labelsize", 7.5),
        "ytick.labelsize": style.get("ytick.labelsize", 7.5),
        "legend.fontsize": style.get("legend.fontsize", 7.5),
        "axes.spines.top": False,
        "axes.spines.right": False,
        "savefig.transparent": True,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    })


def create_axes(kind: str, figsize: tuple[float, float] | None = None):
    if kind == "radar":
        fig = plt.figure(figsize=figsize or FIG_SIZES["square"], dpi=300)
        return fig, fig.add_subplot(111, projection="polar")
    if kind in {"framework", "study_framework"}:
        fig, ax = plt.subplots(figsize=figsize or FIG_SIZES["framework"], dpi=300)
        ax.set_axis_off()
        return fig, ax
    if "map" in kind or "raster" in kind or "choropleth" in kind:
        return plt.subplots(figsize=figsize or FIG_SIZES["map"], dpi=300)
    if "horizontal" in kind or kind in {"stacked_area", "scenario_uncertainty", "multi_line_time", "event_period", "log_timeseries"}:
        return plt.subplots(figsize=figsize or FIG_SIZES["wide"], dpi=300)
    if kind in {"boxen", "model_boxplot", "violin_box", "faceted_boxplot"}:
        return plt.subplots(figsize=figsize or FIG_SIZES["tall"], dpi=300)
    return plt.subplots(figsize=figsize or FIG_SIZES["single"], dpi=300)


def save_figure(fig, output_dir: str | Path, basename: str, formats: Iterable[str] = DEFAULT_FORMATS, dpi: int = 600) -> list[Path]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for fmt in formats:
        fmt = fmt.lower().lstrip(".")
        out = output_dir / f"{basename}.{fmt}"
        kwargs = {"bbox_inches": "tight", "transparent": True}
        if fmt in {"png", "jpg", "jpeg", "tif", "tiff"}:
            kwargs["dpi"] = dpi
        fig.savefig(out, **kwargs)
        paths.append(out)
    plt.close(fig)
    return paths


def make_sample_data(kind: str, seed: int = 42, title: str | None = None) -> dict:
    rng = np.random.default_rng(seed)
    groups = np.array(["A", "B", "C", "D"])
    comps = np.array(["Type 1", "Type 2", "Type 3", "Type 4"])
    years = np.arange(2000, 2025)
    x = np.linspace(0, 1, 160)
    lon = np.linspace(-180, 180, 240)
    lat = np.linspace(-60, 80, 120)
    lon2, lat2 = np.meshgrid(lon, lat)
    raster = 1.8 * np.exp(-((lon2 + 70) ** 2 / 1800 + (lat2 - 5) ** 2 / 450)) + 1.2 * np.exp(-((lon2 - 105) ** 2 / 2200 + (lat2 - 12) ** 2 / 550)) + 0.35 * rng.random(lon2.shape)
    common = {"title": title or kind.replace("_", " ").title()}
    if kind in {"boxen", "model_boxplot", "faceted_boxplot", "violin_box"}:
        return common | {"groups": groups, "values": [rng.normal(0.6 + i * 0.35, 0.25 + 0.05 * i, 90) for i in range(4)], "ylabel": "Value"}
    if kind in {"stacked_percent", "stacked_bar_time", "horizontal_stacked", "horizontal_stacked_zoom", "stacked_percent_line"}:
        raw = rng.gamma(1.5, 1.0, (len(groups), len(comps)))
        return common | {"groups": groups, "components": comps, "values": raw / raw.sum(axis=1, keepdims=True), "ylabel": "Percent"}
    if kind in {"grouped_bar", "horizontal_dual_axis", "binary_bar"}:
        return common | {"groups": groups, "series": np.array(["S1", "S2", "S3"]), "values": np.abs(rng.normal(1, 0.35, (4, 3))), "ylabel": "Index"}
    if kind == "diverging_bar":
        return common | {"groups": groups, "components": comps, "values": rng.normal(0, 0.35, (4, 4)), "xlabel": "Contribution"}
    if kind in {"stacked_area", "multi_line_time", "observed_simulated", "scenario_uncertainty", "event_period", "log_timeseries"}:
        series = np.vstack([np.cumsum(rng.normal(0.04 + i * 0.02, 0.08, len(years))) + i + 1 for i in range(3)])
        return common | {"x": years, "series": series, "labels": np.array(["Baseline", "Scenario A", "Scenario B"]), "ylabel": "Value"}
    if kind in {"response_curve", "latitudinal_profile", "depth_profile"}:
        return common | {"x": x, "y": 1 / (1 + np.exp(-8 * (x - 0.5))), "ylabel": "Response"}
    if kind in {"density_scatter", "pca", "loglog_scatter", "predicted_real", "parity"}:
        xs = rng.normal(0, 1, 450)
        return common | {"x": xs, "y": xs * 0.75 + rng.normal(0, 0.65, 450), "xlabel": "Observed", "ylabel": "Predicted"}
    if kind in {"hist_kde", "hist_ecdf", "overlap_kde", "joint_kde"}:
        return common | {"values": [rng.lognormal(i * 0.2, 0.35, 300) for i in range(3)], "labels": np.array(["A", "B", "C"]), "xlabel": "Value"}
    if kind in {"shap_bar", "shap_beeswarm"}:
        return common | {"features": np.array([f"Feature {i}" for i in range(1, 9)]), "importance": np.sort(rng.random(8))[::-1], "effects": rng.normal(0, 1, (300, 8))}
    if kind == "radar":
        return common | {"labels": np.array(["Accuracy", "Robust", "Speed", "Stable", "Cost"]), "values": np.clip(rng.normal(0.65, 0.18, 5), 0.05, 1)}
    if kind == "nested_donut":
        return common | {"outer": np.array([40, 30, 20, 10]), "inner": np.array([25, 15, 18, 12, 14, 6, 7, 3])}
    if kind in {"framework", "study_framework"}:
        return common
    return common | {"lon": lon, "lat": lat, "raster": raster, "xlabel": "Longitude", "ylabel": "Latitude"}


def _clean(ax, xlabel=None, ylabel=None):
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.grid(True, color="0.90", linewidth=0.6, zorder=0)


def _raster(ax, data, kind):
    arr = data["raster"]
    extent = [float(data["lon"][0]), float(data["lon"][-1]), float(data["lat"][0]), float(data["lat"][-1])]
    norm = mpl.colors.LogNorm(vmin=max(float(np.nanmin(arr)), 1e-3), vmax=float(np.nanmax(arr))) if kind == "log_raster" else None
    im = ax.imshow(arr, extent=extent, origin="lower", aspect="auto", cmap=PALETTES["log"] if kind == "log_raster" else PALETTES["sequential"], norm=norm)
    if kind == "raster_quiver":
        qlon, qlat = np.meshgrid(np.linspace(extent[0], extent[1], 18), np.linspace(extent[2], extent[3], 10))
        ax.quiver(qlon, qlat, np.cos(np.deg2rad(qlat)), np.sin(np.deg2rad(qlon)), color="white", alpha=0.65, scale=35)
    if kind == "raster_contour":
        ax.contour(data["lon"], data["lat"], arr, colors="black", linewidths=0.5, alpha=0.45)
    plt.colorbar(im, ax=ax, fraction=0.036, pad=0.03, label="Intensity")
    _clean(ax, data.get("xlabel"), data.get("ylabel"))


def plot_template(kind: str, data: Mapping | None = None, *, ax=None, title: str | None = None, style: Mapping | None = None, config: Mapping | None = None):
    apply_style(style)
    data = dict(data or make_sample_data(kind, title=title))
    fig = None
    if ax is None:
        fig, ax = create_axes(kind, tuple(config["figsize"]) if config and "figsize" in config else None)
    else:
        fig = ax.figure
    colors = PALETTES["categorical"]
    ax.set_title(data.get("title", title or kind.replace("_", " ").title()), loc="left", fontweight="bold")

    if "map" in kind or "raster" in kind or "choropleth" in kind:
        _raster(ax, data, kind)
    elif kind in {"boxen", "model_boxplot", "faceted_boxplot", "violin_box"}:
        if kind == "violin_box":
            parts = ax.violinplot(data["values"], showmeans=False, showmedians=False, widths=0.72)
            for body, color in zip(parts["bodies"], colors):
                body.set_facecolor(color); body.set_edgecolor("black"); body.set_alpha(0.35)
        bp = ax.boxplot(data["values"], patch_artist=True, labels=data["groups"], widths=0.48)
        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color); patch.set_alpha(0.55)
        _clean(ax, None, data.get("ylabel"))
    elif kind in {"stacked_percent", "stacked_bar_time"}:
        bottom = np.zeros(len(data["groups"]))
        for i, comp in enumerate(data["components"]):
            vals = data["values"][:, i] * 100
            ax.bar(data["groups"], vals, bottom=bottom, color=colors[i], label=comp, edgecolor="white", linewidth=0.4)
            bottom += vals
        ax.set_ylim(0, 100); ax.legend(frameon=False, ncol=2); _clean(ax, None, data.get("ylabel"))
    elif kind in {"horizontal_stacked", "horizontal_stacked_zoom"}:
        left = np.zeros(len(data["groups"])); y = np.arange(len(data["groups"]))
        for i, comp in enumerate(data["components"]):
            vals = data["values"][:, i] * 100
            ax.barh(y, vals, left=left, color=colors[i], label=comp, edgecolor="white", linewidth=0.4)
            left += vals
        ax.set_yticks(y, data["groups"]); ax.legend(frameon=False, ncol=2); _clean(ax, "Percent", None)
    elif kind in {"grouped_bar", "horizontal_dual_axis", "binary_bar"}:
        vals = data["values"]; x = np.arange(vals.shape[0]); width = 0.23
        for i in range(vals.shape[1]):
            ax.bar(x + (i - 1) * width, vals[:, i], width=width, color=colors[i], label=data["series"][i])
        ax.set_xticks(x, data["groups"]); ax.legend(frameon=False); _clean(ax, None, data.get("ylabel"))
    elif kind == "diverging_bar":
        vals = data["values"]; y = np.arange(vals.shape[0])
        for i in range(vals.shape[1]):
            ax.barh(y, vals[:, i], color=colors[i], alpha=0.8, label=data["components"][i])
        ax.axvline(0, color="black", linewidth=0.8); ax.set_yticks(y, data["groups"]); ax.legend(frameon=False); _clean(ax, data.get("xlabel"), None)
    elif kind == "stacked_area":
        ax.stackplot(data["x"], data["series"], labels=data["labels"], colors=colors[:len(data["labels"])], alpha=0.85); ax.legend(frameon=False); _clean(ax, "Year", data.get("ylabel"))
    elif kind in {"multi_line_time", "observed_simulated", "scenario_uncertainty", "event_period", "log_timeseries"}:
        for i, y in enumerate(data["series"]):
            ax.plot(data["x"], y, color=colors[i], linewidth=1.8, label=data["labels"][i])
            if kind == "scenario_uncertainty":
                ax.fill_between(data["x"], y - 0.25, y + 0.25, color=colors[i], alpha=0.14, linewidth=0)
        if kind == "event_period":
            ax.axvspan(data["x"][8], data["x"][13], color="#F2C14E", alpha=0.22, linewidth=0)
        if kind == "log_timeseries":
            ax.set_yscale("log")
        ax.legend(frameon=False, ncol=3); _clean(ax, "Year", data.get("ylabel"))
    elif kind in {"response_curve", "latitudinal_profile", "depth_profile"}:
        ax.plot(data["x"], data["y"], color=colors[0], linewidth=2.0); ax.fill_between(data["x"], data["y"] - 0.08, data["y"] + 0.08, color=colors[0], alpha=0.16)
        if kind == "depth_profile":
            ax.invert_yaxis(); _clean(ax, "Cumulative value", "Depth")
        else:
            _clean(ax, "Gradient", data.get("ylabel"))
    elif kind in {"density_scatter", "pca", "loglog_scatter", "predicted_real", "parity"}:
        x = np.abs(data["x"]) + 0.05 if kind == "loglog_scatter" else data["x"]; y = np.abs(data["y"]) + 0.05 if kind == "loglog_scatter" else data["y"]
        ax.scatter(x, y, c=np.hypot(x - np.mean(x), y - np.mean(y)), cmap="viridis", s=12, alpha=0.72, edgecolor="none")
        if kind in {"predicted_real", "parity", "loglog_scatter"}:
            lo = min(np.nanmin(x), np.nanmin(y)); hi = max(np.nanmax(x), np.nanmax(y)); ax.plot([lo, hi], [lo, hi], color="black", linestyle="--", linewidth=1)
        if kind == "loglog_scatter":
            ax.set_xscale("log"); ax.set_yscale("log")
        if kind == "pca":
            for angle, label in zip(np.linspace(0, 2*np.pi, 5, endpoint=False), ["V1", "V2", "V3", "V4", "V5"]):
                ax.arrow(0, 0, np.cos(angle) * 1.2, np.sin(angle) * 1.2, width=0.006, color="#D95F02", length_includes_head=True); ax.text(np.cos(angle) * 1.32, np.sin(angle) * 1.32, label, color="#D95F02")
            ax.axhline(0, color="0.75", linewidth=0.8); ax.axvline(0, color="0.75", linewidth=0.8)
        _clean(ax, data.get("xlabel"), data.get("ylabel"))
    elif kind in {"hist_kde", "hist_ecdf", "overlap_kde", "joint_kde"}:
        for values, label, color in zip(data["values"], data["labels"], colors):
            ax.hist(values, bins=28, density=True, alpha=0.25, color=color, label=label)
            hist, edges = np.histogram(values, bins=40, density=True); centers = 0.5 * (edges[:-1] + edges[1:])
            xs = np.linspace(np.min(values), np.max(values), 160); ax.plot(xs, np.interp(xs, centers, hist), color=color, linewidth=1.8)
            if kind == "hist_ecdf":
                ax2 = ax.twinx(); sorted_v = np.sort(values); ax2.plot(sorted_v, np.linspace(0, 1, len(sorted_v)), color=color, linestyle="--", alpha=0.65); ax2.set_ylabel("ECDF")
        ax.legend(frameon=False); _clean(ax, data.get("xlabel"), "Density")
    elif kind == "shap_bar":
        order = np.arange(len(data["features"])); ax.barh(order, data["importance"], color=colors[0]); ax.set_yticks(order, data["features"]); ax.invert_yaxis(); _clean(ax, "Mean |effect|", None)
    elif kind == "shap_beeswarm":
        effects = data["effects"]
        for i in range(effects.shape[1]):
            jitter = np.random.default_rng(i).normal(0, 0.07, effects.shape[0]); ax.scatter(effects[:, i], np.full(effects.shape[0], i) + jitter, c=effects[:, i], cmap="coolwarm", s=7, alpha=0.55, edgecolor="none")
        ax.set_yticks(np.arange(len(data["features"])), data["features"]); ax.axvline(0, color="0.35", linewidth=0.8); _clean(ax, "Effect value", None)
    elif kind == "radar":
        labels = data["labels"]; values = np.r_[data["values"], data["values"][0]]; angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False); angles = np.r_[angles, angles[0]]
        ax.plot(angles, values, color=colors[0], linewidth=1.8); ax.fill(angles, values, color=colors[0], alpha=0.18); ax.set_xticks(angles[:-1], labels); ax.set_ylim(0, 1)
    elif kind == "nested_donut":
        ax.set_aspect("equal"); ax.pie(data["outer"], radius=1, colors=colors[:4], wedgeprops=dict(width=0.26, edgecolor="white")); ax.pie(data["inner"], radius=0.70, colors=(colors * 2)[:len(data["inner"])], wedgeprops=dict(width=0.24, edgecolor="white"))
    elif kind in {"framework", "study_framework"}:
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        boxes = [(0.06, 0.58, "Data"), (0.36, 0.58, "Model"), (0.66, 0.58, "Outputs"), (0.36, 0.22, "Validation")]
        for x0, y0, text in boxes:
            ax.add_patch(Rectangle((x0, y0), 0.22, 0.15, facecolor="#E8F1F2", edgecolor="0.25", linewidth=0.9)); ax.text(x0 + 0.11, y0 + 0.075, text, ha="center", va="center", fontweight="bold")
        for start, end in [((0.28, 0.655), (0.36, 0.655)), ((0.58, 0.655), (0.66, 0.655)), ((0.47, 0.58), (0.47, 0.37))]:
            ax.add_patch(FancyArrowPatch(start, end, arrowstyle="->", mutation_scale=12, linewidth=1, color="0.25"))
    return fig, ax


def render_template(kind: str, output_dir: str | Path, basename: str, *, title: str | None = None, formats: Sequence[str] = DEFAULT_FORMATS, seed: int = 42, data: Mapping | None = None, style: Mapping | None = None, config: Mapping | None = None) -> list[Path]:
    fig, _ = plot_template(kind, data or make_sample_data(kind, seed=seed, title=title), title=title, style=style, config=config)
    return save_figure(fig, output_dir, basename, formats=formats)
