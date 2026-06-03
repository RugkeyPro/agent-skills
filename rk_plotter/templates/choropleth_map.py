# TEMPLATE_ID: choropleth_map
# TEMPLATE_VERSION: 2.0
# FIGURE_TYPE: high_fidelity_environmental_choropleth_and_symbol_maps
#
# HIGH_FIDELITY_SOURCES:
# - assets/original-scripts/figure-country-level choropleth map.py
# - assets/original-scripts/figure-choropleth + proportional symbol map.py
# - assets/new-scripts/proportional symbol map + continuous color map.py
# - assets/new-scripts/proportional symbol map + categorical color map.py
#
# CORE_VISUAL_GRAMMAR:
# - Single-column map canvas with PlateCarree projection.
# - White ocean/background, pale land, thin gray/black administrative boundaries.
# - Choropleth legend or proportional-symbol legends placed inside the map.
# - Optional bottom horizontal colorbar for continuous choropleth/symbol color.
# - Text remains editable in Illustrator through svg.fonttype="none" and pdf.fonttype=42.
#
# USER_DECISION_POINTS_BEFORE_USE:
# - map_mode: country_choropleth, choropleth_symbols, proportional_continuous, proportional_categorical
# - palette: original_purple_green_yellow, blues_log, hotspot_green_red, categorical_blue_yellow_red
# - extent/projection: global PlateCarree or a regional PlateCarree extent
# - boundary source: Natural Earth countries, provinces, ocean regions, or user shapefile
# - legend/colorbar: binned patch legend, size legend, horizontal colorbar, categorical legend
# - point encoding: size field, continuous color field, categorical color field, alpha, edge color

from __future__ import annotations

from pathlib import Path
import math
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import numpy as np
import pandas as pd

try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    import cartopy.io.shapereader as shpreader
except ImportError as exc:
    raise ImportError("This high-fidelity map template requires cartopy. Install with: pip install cartopy") from exc


TEMPLATE_ID = "choropleth_map"

FIELD_MAP = {
    "region": "region",
    "polygon_value": "polygon_value",
    "lon": "lon",
    "lat": "lat",
    "point_size": "point_size",
    "point_color": "point_color",
    "point_category": "point_category",
}

TEXT_CONFIG = {
    "title": "",
    "choropleth_legend_title": "Plastic emissions\n(Mt year$^{-1}$)",
    "size_legend_title": "Yield\n(ng m$^{-2}$ yr$^{-1}$)",
    "colorbar_label": "MeHg export (kg yr$^{-1}$)",
    "category_legend_title": "Drawdown area ratio (%)",
}

STYLE_CONFIG = {
    "map_mode": "country_choropleth",
    "figsize": (3.5, 1.65),
    "dpi": 300,
    "font_family": "Arial",
    "font_size": 6.8,
    "projection": "platecarree",
    "extent": [-180, 180, -60, 85],
    "show_ticks": False,
    "panel_label": None,
    "background_color": "white",
    "land_color": "#f2f2f2",
    "ocean_color": "white",
    "boundary_color": "0.35",
    "coastline_color": "0.35",
    "boundary_linewidth": 0.28,
    "coastline_linewidth": 0.30,
    "spine_visible": False,
    "spine_linewidth": 0.6,
    "palette": "original_purple_green_yellow",
    "bins": [0, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 2.0, 5.0, 10.0],
    "bin_labels": ["0-0.1", "0.1-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0", "1.0-2.0", "2.0-5.0", "5.0-10.0"],
    "point_facecolor": "#f4a3a0",
    "point_edgecolor": "#e77d79",
    "point_alpha": 0.95,
    "point_linewidth": 0.35,
    "continuous_point_cmap": ["#f3f5b0", "#d8efaa", "#aee0b1", "#74c6b8", "#39a6bf", "#2073b2", "#24368f"],
    "continuous_vmin": 0.0,
    "continuous_vmax": 2.0,
    "categorical_bins": [0, 5, 10, 20, 50, 100],
    "categorical_labels": ["<5", "5-10", "10-20", "20-50", "50-100"],
    "categorical_colors": ["#4f7fb9", "#a9c3d0", "#f3f1b2", "#f4a56d", "#df3f2f"],
    "size_values": [75, 225, 375, 525, 675],
    "size_labels": ["0-150", "150-300", "300-450", "450-600", ">600"],
    "colorbar_ticks": [0.01, 0.1, 1, 10, 100, 1000],
    "colorbar_ticklabels": ["0.01", "0.1", "1", "10", "100", "1,000"],
    "add_china_inset": False,
}

EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "choropleth_map",
    "formats": ["png", "pdf", "svg"],
    "dpi": 600,
}


PALETTES = {
    "original_purple_green_yellow": [
        "#a56ab3", "#8d83b6", "#8fa5bd", "#80bec5", "#73c4c0",
        "#7ecbb8", "#9cdda4", "#d7ef82", "#fff07a",
    ],
    "blues_log": [mpl.cm.Blues(i) for i in np.linspace(0.22, 0.95, 9)],
    "hotspot_green_red": ["#2b8c5a", "#6fb96f", "#d9ef8b", "#fee08b", "#f46d43", "#a50026"],
    "categorical_blue_yellow_red": ["#4f7fb9", "#a9c3d0", "#f3f1b2", "#f4a56d", "#df3f2f"],
}


def apply_style(style: dict) -> None:
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": [style.get("font_family", "Arial"), "Arial", "DejaVu Sans"],
        "font.size": style["font_size"],
        "axes.unicode_minus": False,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


def country_records() -> list:
    shp_path = shpreader.natural_earth(resolution="110m", category="cultural", name="admin_0_countries")
    return list(shpreader.Reader(shp_path).records())


def load_data(path: str | Path = "data.csv") -> pd.DataFrame:
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)

    rng = np.random.default_rng(42)
    records = country_records()
    rows = []
    manual = {
        "China": 4.0, "India": 6.5, "Indonesia": 2.8, "Brazil": 1.6,
        "Russia": 1.4, "United States of America": 0.8, "Pakistan": 2.5,
        "Bangladesh": 1.8, "Nigeria": 0.9, "Philippines": 0.9,
    }
    for rec in records:
        name = rec.attributes.get("ADMIN", rec.attributes.get("NAME_LONG", ""))
        if name == "Antarctica":
            continue
        rows.append({
            "region": name,
            "polygon_value": manual.get(name, float(np.clip(rng.lognormal(-1.2, 0.9), 0.02, 8.5))),
        })

    clusters = [(-60, -5, 12), (-90, 15, 8), (10, 50, 16), (78, 22, 10), (105, 15, 18), (120, -5, 12)]
    for lon0, lat0, n in clusters:
        lons = rng.normal(lon0, 8, n)
        lats = rng.normal(lat0, 5, n)
        for lon, lat in zip(lons, lats):
            rows.append({
                "region": np.nan,
                "polygon_value": np.nan,
                "lon": lon,
                "lat": lat,
                "point_size": float(np.clip(rng.gamma(2.3, 160), 20, 760)),
                "point_color": float(rng.uniform(0.0, 2.0)),
                "point_category": float(rng.uniform(0, 100)),
            })
    return pd.DataFrame(rows)


def prepare_data(df: pd.DataFrame, field_map: dict) -> dict:
    polygon = df[[field_map["region"], field_map["polygon_value"]]].dropna()
    polygon_values = dict(zip(polygon[field_map["region"]].astype(str), pd.to_numeric(polygon[field_map["polygon_value"]], errors="coerce")))

    point_cols = [field_map["lon"], field_map["lat"], field_map["point_size"], field_map["point_color"], field_map["point_category"]]
    existing = [c for c in point_cols if c in df.columns]
    points = df[existing].copy() if existing else pd.DataFrame()
    for c in existing:
        points[c] = pd.to_numeric(points[c], errors="coerce")
    if existing:
        points = points.dropna(subset=[field_map["lon"], field_map["lat"]])
    return {"polygon_values": polygon_values, "points": points, "records": country_records()}


def palette(style: dict) -> list:
    return PALETTES.get(style["palette"], PALETTES["original_purple_green_yellow"])


def get_projection(style: dict):
    if style.get("projection") == "robinson":
        return ccrs.Robinson()
    return ccrs.PlateCarree()


def size_map(values):
    values = np.asarray(values, dtype=float)
    return np.interp(values, [0, 700], [12, 260])


def draw_base(ax, style: dict) -> None:
    ax.set_facecolor(style["background_color"])
    ax.set_extent(style["extent"], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.OCEAN, facecolor=style["ocean_color"], edgecolor="none", zorder=0)
    ax.add_feature(cfeature.LAND, facecolor=style["land_color"], edgecolor="none", zorder=1)
    ax.add_feature(cfeature.COASTLINE, edgecolor=style["coastline_color"], linewidth=style["coastline_linewidth"], zorder=5)
    ax.add_feature(cfeature.BORDERS, edgecolor=style["boundary_color"], linewidth=style["boundary_linewidth"], zorder=5)
    if style["show_ticks"]:
        ax.set_xticks([-120, -60, 0, 60, 120, 180], crs=ccrs.PlateCarree())
        ax.set_yticks([-60, -30, 0, 30, 60], crs=ccrs.PlateCarree())
        ax.set_xticklabels(["120 W", "60 W", "0", "60 E", "120 E", "180"], fontsize=style["font_size"])
        ax.set_yticklabels(["60 S", "30 S", "0", "30 N", "60 N"], fontsize=style["font_size"])
    else:
        ax.set_xticks([])
        ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(style["spine_visible"])
        spine.set_linewidth(style["spine_linewidth"])


def draw_choropleth(ax, data: dict, style: dict, use_log: bool = False):
    colors = palette(style)
    if use_log:
        cmap = mpl.cm.Blues
        norm = mpl.colors.LogNorm(vmin=0.01, vmax=3000)
    else:
        cmap = mpl.colors.ListedColormap(colors)
        norm = mpl.colors.BoundaryNorm(style["bins"], cmap.N)

    values = data["polygon_values"]
    for rec in data["records"]:
        name = rec.attributes.get("ADMIN", rec.attributes.get("NAME_LONG", ""))
        if name == "Antarctica":
            continue
        value = values.get(name, np.nan)
        facecolor = style["land_color"] if not np.isfinite(value) else cmap(norm(value))
        ax.add_geometries(
            [rec.geometry],
            crs=ccrs.PlateCarree(),
            facecolor=facecolor,
            edgecolor=style["boundary_color"] if not use_log else "white",
            linewidth=style["boundary_linewidth"] if not use_log else 0.35,
            zorder=3,
        )
    return cmap, norm


def add_choropleth_legend(ax, text: dict, style: dict) -> None:
    handles = [
        Patch(facecolor=c, edgecolor=style["boundary_color"], linewidth=0.35, label=lab)
        for c, lab in zip(palette(style), style["bin_labels"])
    ]
    legend = ax.legend(
        handles=handles,
        title=text["choropleth_legend_title"],
        loc="lower left",
        bbox_to_anchor=(0.01, 0.04),
        frameon=False,
        fontsize=style["font_size"],
        title_fontsize=style["font_size"] + 0.5,
        handlelength=1.0,
        handleheight=0.7,
        handletextpad=0.35,
        labelspacing=0.28,
        borderpad=0.1,
    )
    legend._legend_box.align = "left"


def add_size_legend(ax, text: dict, style: dict, loc="lower left", anchor=(0.01, 0.02), ncol=1) -> None:
    handles = [
        Line2D([0], [0], marker="o", linestyle="", markerfacecolor="white", markeredgecolor="black",
               markeredgewidth=0.6, markersize=math.sqrt(size_map(v)), color="black", label=lab)
        for v, lab in zip(style["size_values"], style["size_labels"])
    ]
    legend = ax.legend(
        handles=handles,
        title=text["size_legend_title"],
        loc=loc,
        bbox_to_anchor=anchor,
        ncol=ncol,
        frameon=False,
        fontsize=style["font_size"],
        title_fontsize=style["font_size"] + 0.5,
        handlelength=0.8,
        handletextpad=0.45,
        labelspacing=0.35,
        borderpad=0.1,
    )
    ax.add_artist(legend)


def add_horizontal_colorbar(fig, ax, cmap, norm, text: dict, style: dict) -> None:
    sm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation="horizontal", fraction=0.055, pad=0.12, shrink=0.72)
    cbar.set_label(text["colorbar_label"], fontsize=style["font_size"] + 0.5, labelpad=4)
    cbar.set_ticks(style["colorbar_ticks"])
    cbar.set_ticklabels(style["colorbar_ticklabels"])
    cbar.ax.tick_params(labelsize=style["font_size"], length=0)
    cbar.outline.set_linewidth(0.6)


def draw_points(ax, points: pd.DataFrame, field_map: dict, style: dict, mode: str):
    if points.empty:
        return None, None
    lon = points[field_map["lon"]]
    lat = points[field_map["lat"]]
    sizes = size_map(points.get(field_map["point_size"], pd.Series(np.full(len(points), 200))))

    if mode == "proportional_continuous":
        cmap = mpl.colors.LinearSegmentedColormap.from_list("continuous_symbol", style["continuous_point_cmap"], N=256)
        norm = mpl.colors.Normalize(vmin=style["continuous_vmin"], vmax=style["continuous_vmax"])
        sc = ax.scatter(lon, lat, s=sizes, c=points[field_map["point_color"]], cmap=cmap, norm=norm,
                        edgecolor="black", linewidth=0.45, alpha=0.92, transform=ccrs.PlateCarree(), zorder=6)
        return sc, (cmap, norm)

    if mode == "proportional_categorical":
        bins = style["categorical_bins"]
        labels = style["categorical_labels"]
        colors = dict(zip(labels, style["categorical_colors"]))
        cats = pd.cut(points[field_map["point_category"]], bins=bins, labels=labels, include_lowest=True)
        for label in labels:
            sub = points[cats == label]
            if sub.empty:
                continue
            ax.scatter(sub[field_map["lon"]], sub[field_map["lat"]], s=size_map(sub[field_map["point_size"]]),
                       facecolor=colors[label], edgecolor=colors[label], linewidth=0.55, alpha=0.35,
                       transform=ccrs.PlateCarree(), zorder=6)
        return None, None

    ax.scatter(lon, lat, s=sizes, transform=ccrs.PlateCarree(), facecolor=style["point_facecolor"],
               edgecolor=style["point_edgecolor"], linewidth=style["point_linewidth"],
               alpha=style["point_alpha"], zorder=6)
    return None, None


def add_categorical_legend(ax, text: dict, style: dict) -> None:
    handles = [
        Patch(facecolor=c, edgecolor="black", linewidth=0.35, label=l)
        for l, c in zip(style["categorical_labels"], style["categorical_colors"])
    ]
    legend = ax.legend(
        handles=handles,
        title=text["category_legend_title"],
        loc="lower center",
        bbox_to_anchor=(0.53, 0.005),
        ncol=len(handles),
        frameon=False,
        fontsize=style["font_size"],
        title_fontsize=style["font_size"],
        handlelength=1.0,
        handleheight=0.6,
        handletextpad=0.35,
        columnspacing=0.55,
        borderpad=0.1,
    )
    legend.get_title().set_fontweight("bold")


def plot(data: dict, text: dict, style: dict) -> plt.Figure:
    apply_style(style)
    fig = plt.figure(figsize=style["figsize"], dpi=style["dpi"])
    ax = plt.axes(projection=get_projection(style))
    draw_base(ax, style)

    mode = style["map_mode"]
    cmap = norm = None
    if mode in {"country_choropleth", "choropleth_symbols"}:
        cmap, norm = draw_choropleth(ax, data, style, use_log=(mode == "choropleth_symbols"))
    if mode == "country_choropleth":
        add_choropleth_legend(ax, text, style)
    elif mode == "choropleth_symbols":
        draw_points(ax, data["points"], FIELD_MAP, style, "simple")
        add_size_legend(ax, text, style)
        add_horizontal_colorbar(fig, ax, cmap, norm, text, style)
    elif mode in {"proportional_continuous", "proportional_categorical"}:
        draw_base(ax, {**style, "land_color": "#f1f1f1", "spine_visible": True, "show_ticks": True})
        _, color_scale = draw_points(ax, data["points"], FIELD_MAP, style, mode)
        add_size_legend(ax, text, style, loc="lower center", anchor=(0.52, 0.08), ncol=4)
        if mode == "proportional_continuous" and color_scale:
            cmap, norm = color_scale
            cbar = fig.colorbar(mpl.cm.ScalarMappable(cmap=cmap, norm=norm), ax=ax, orientation="vertical", fraction=0.045, pad=0.03)
            cbar.set_label(text["colorbar_label"], fontsize=style["font_size"] + 0.5, rotation=90, labelpad=7)
            cbar.ax.tick_params(labelsize=style["font_size"], length=3, width=0.6)
            cbar.outline.set_linewidth(0.7)
        if mode == "proportional_categorical":
            add_categorical_legend(ax, text, style)

    if text.get("title"):
        ax.set_title(text["title"], fontsize=style["font_size"] + 1.0, pad=5)
    if style.get("panel_label"):
        fig.text(0.055, 0.91, style["panel_label"], fontsize=style["font_size"] + 2, fontweight="bold", ha="left", va="center")
    return fig


def save_outputs(fig: plt.Figure, export: dict) -> list[Path]:
    output_dir = Path(export["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for fmt in export["formats"]:
        path = output_dir / f"{export['basename']}.{fmt}"
        kwargs = {"bbox_inches": "tight", "pad_inches": 0.03}
        if fmt.lower() == "png":
            kwargs["dpi"] = export["dpi"]
        fig.savefig(path, **kwargs)
        paths.append(path)
    plt.close(fig)
    return paths


def main() -> None:
    data = prepare_data(load_data(sys.argv[1] if len(sys.argv) > 1 else "data.csv"), FIELD_MAP)
    fig = plot(data, TEXT_CONFIG, STYLE_CONFIG)
    print("Generated:", [str(p) for p in save_outputs(fig, EXPORT_CONFIG)])


if __name__ == "__main__":
    main()
