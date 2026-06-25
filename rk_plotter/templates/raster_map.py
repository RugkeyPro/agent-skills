# TEMPLATE_ID: raster_map
# TEMPLATE_VERSION: 2.0
# FIGURE_TYPE: high_fidelity_environmental_raster_contour_quiver_hotspot_maps
#
# HIGH_FIDELITY_SOURCES:
# - assets/original-scripts/figure-log-scale raster map.py
# - assets/original-scripts/figure-raster map with contour lines.py
# - assets/original-scripts/figure-raster map+quiver map+log colorbar.py
# - assets/original-scripts/figure-hotspot_map.py
# - assets/original-scripts/figure-global raster map of publicly tracked vessel fraction.py (palette reference only)
#
# USER_DECISION_POINTS_BEFORE_USE:
# - map_mode: log_raster, contour_robinson, quiver_log, hotspot
# - projection/extent: PlateCarree global, Robinson global, or regional PlateCarree
# - colorbar: horizontal log, horizontal discrete, vertical log, or inset vertical hotspot bar
# - overlays: contour lines, quiver arrows, land mask, ocean mask, ticks, panel label

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    from scipy.ndimage import gaussian_filter
except ImportError:
    def gaussian_filter(a, sigma=1):
        return a

try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
except ImportError as exc:
    raise ImportError("This high-fidelity map template requires cartopy. Install with: pip install cartopy") from exc


TEMPLATE_ID = "raster_map"

FIELD_MAP = {
    "lon": "lon",
    "lat": "lat",
    "value": "value",
    "u": "u",
    "v": "v",
}

TEXT_CONFIG = {
    "title": "",
    "colorbar_label": "Ingestion risk (mol C m$^{-3}$ kg m$^{-3}$)",
    "side_label": "PFOS",
    "quiver_label": "0.3 m s$^{-1}$",
    "hotspot_side_label": "Terrestrial vertebrates",
    "hotspot_colorbar_label": "Hotspot\nvalue",
}

STYLE_CONFIG = {
    "map_mode": "log_raster",
    "figsize": (3.5, 2.0),
    "dpi": 300,
    "font_family": "Arial",
    "font_size": 6.8,
    "projection": "platecarree",
    "extent": [-180, 180, -75, 85],
    "show_ticks": False,
    "panel_label": None,
    "axis_facecolor": "white",
    "land_color": "white",
    "land_edgecolor": "black",
    "land_linewidth": 0.45,
    "coastline_linewidth": 0.45,
    "border_linewidth": 0.20,
    "spine_linewidth": 0.8,
    "log_vmin": 1e-14,
    "log_vmax": 1e-10,
    "contour_levels": list(np.arange(1, 11, 1)),
    "discrete_levels": list(np.arange(0, 11, 1)),
    "quiver_scale": 28,
    "quiver_step": 15,
    "hotspot_vmax": 282.17,
}

EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "raster_map",
    "formats": ["png", "pdf", "svg"],
    "dpi": 600,
}


PALETTES = {
    "log_raster": ["#2b008f", "#0047ff", "#00c7ff", "#ffff66", "#ffb000", "#ff0000", "#8e008e"],
    "contour_robinson": ["#4b1d7a", "#40327f", "#31507f", "#22728a", "#1d8d8d", "#209c84", "#2da56d", "#62b955", "#a9d63a", "#f4e51c"],
    "quiver_log": ["#3d46b5", "#6c83d7", "#b9d4f2", "#fff2bf", "#f7c66a", "#f98f52", "#e34a33"],
    "hotspot": ["#2b8c5a", "#6fb96f", "#d9ef8b", "#fee08b", "#f46d43", "#a50026"],
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


def synthetic_grid(mode: str) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(42)
    if mode == "quiver_log":
        lon = np.linspace(-180, 180, 361)
        lat = np.linspace(-75, 75, 151)
    elif mode == "contour_robinson":
        lon = np.linspace(-180, 180, 361)
        lat = np.linspace(-89.5, 89.5, 180)
    else:
        lon = np.linspace(-180, 180, 360)
        lat = np.linspace(-80, 85, 180)
    lon2, lat2 = np.meshgrid(lon, lat)

    def hotspot(lon0, lat0, amp, sx=18, sy=10):
        return amp * np.exp(-(((lon2 - lon0) ** 2) / (2 * sx ** 2) + ((lat2 - lat0) ** 2) / (2 * sy ** 2)))

    field = 0.45 * gaussian_filter(rng.random(lon2.shape), sigma=5)
    field += 0.55 + 0.35 * np.exp(-(lat2 / 35) ** 2)
    for args in [(-145, 30, 1.2, 24, 11), (-40, 35, 1.0, 22, 10), (70, 15, 0.9, 24, 12), (115, -15, 0.9, 28, 12), (-15, -25, 0.7, 25, 12)]:
        field += hotspot(*args)
    field = gaussian_filter(field, sigma=1.5)
    field = (field - field.min()) / (field.max() - field.min())

    if mode == "contour_robinson":
        value = np.clip(field * 10, 0, 10)
    elif mode == "hotspot":
        value = np.power(field, 1.05) * 282.17
    elif mode == "quiver_log":
        value = 10 ** (-6 + field * 5)
    else:
        value = 10 ** (-14 + field * 4)

    qlon = np.arange(-170, 171, 15)
    qlat = np.arange(-60, 61, 15)
    qlon2, qlat2 = np.meshgrid(qlon, qlat)
    u = 0.8 * np.cos(np.deg2rad(qlat2)) * np.sin(np.deg2rad(qlon2 / 1.4)) + 0.7 * np.exp(-(qlat2 / 18) ** 2)
    v = 0.45 * np.sin(np.deg2rad(qlat2 * 1.7)) + 0.22 * np.cos(np.deg2rad(qlon2 * 1.3))
    speed = np.sqrt(u**2 + v**2)
    return {"lon": lon, "lat": lat, "value": value, "qlon": qlon2, "qlat": qlat2, "u": u / (speed + 1e-6), "v": v / (speed + 1e-6)}


def load_data(path: str | Path = "data.csv") -> pd.DataFrame:
    p = Path(path)
    if p.exists():
        df = pd.read_csv(p)
        df.attrs["synthetic"] = False
        return df
    print(f"WARNING: '{p}' not found; using synthetic preview data (NOT real data).", file=sys.stderr)
    grid = synthetic_grid(STYLE_CONFIG["map_mode"])
    lon2, lat2 = np.meshgrid(grid["lon"], grid["lat"])
    df = pd.DataFrame({"lon": lon2.ravel(), "lat": lat2.ravel(), "value": grid["value"].ravel()})
    df.attrs["synthetic"] = True
    return df


def prepare_data(df: pd.DataFrame, field_map: dict, style: dict) -> dict[str, np.ndarray]:
    # Use the DataFrame actually loaded (any filename), not a hardcoded data.csv probe,
    # so real user data is never silently replaced by synthetic preview data.
    if df.attrs.get("synthetic", False):
        return synthetic_grid(style["map_mode"])
    clean = pd.DataFrame({
        "lon": pd.to_numeric(df[field_map["lon"]], errors="coerce"),
        "lat": pd.to_numeric(df[field_map["lat"]], errors="coerce"),
        "value": pd.to_numeric(df[field_map["value"]], errors="coerce"),
    }).dropna()
    pivot = clean.pivot(index="lat", columns="lon", values="value")
    out = {"lon": pivot.columns.to_numpy(), "lat": pivot.index.to_numpy(), "value": pivot.to_numpy()}
    if field_map["u"] in df.columns and field_map["v"] in df.columns:
        out.update(synthetic_grid("quiver_log"))
    return out


def projection_for(mode: str):
    if mode == "contour_robinson":
        return ccrs.Robinson()
    return ccrs.PlateCarree()


def add_land(ax, style: dict, ocean_mask: bool = False) -> None:
    ax.add_feature(cfeature.LAND, facecolor=style["land_color"], edgecolor=style["land_edgecolor"], linewidth=style["land_linewidth"], zorder=4)
    ax.add_feature(cfeature.COASTLINE, edgecolor=style["land_edgecolor"], linewidth=style["coastline_linewidth"], zorder=5)
    if style.get("border_linewidth", 0) > 0:
        ax.add_feature(cfeature.BORDERS, edgecolor=style["land_edgecolor"], linewidth=style["border_linewidth"], alpha=0.55, zorder=5)
    if ocean_mask:
        ax.add_feature(cfeature.OCEAN, facecolor="white", edgecolor="none", zorder=3)
        ax.add_feature(cfeature.COASTLINE, edgecolor="0.45", linewidth=0.25, zorder=5)


def format_axes(ax, style: dict, mode: str) -> None:
    ax.set_extent(style["extent"], crs=ccrs.PlateCarree())
    ax.set_facecolor(style["axis_facecolor"])
    if style["show_ticks"] or mode == "quiver_log":
        ax.set_xticks(np.arange(-150, 181, 60), crs=ccrs.PlateCarree())
        ax.set_yticks(np.arange(-60, 61, 30), crs=ccrs.PlateCarree())
        if mode == "quiver_log":
            ax.set_xticklabels([])
            ax.set_yticklabels(["60 S", "30 S", "0", "30 N", "60 N"], fontsize=style["font_size"])
        ax.tick_params(axis="both", direction="out", length=3, width=0.8)
    else:
        ax.set_xticks([])
        ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_linewidth(style["spine_linewidth"])
        spine.set_edgecolor("black")


def plot(data: dict[str, np.ndarray], text: dict, style: dict) -> plt.Figure:
    apply_style(style)
    mode = style["map_mode"]
    fig = plt.figure(figsize=style["figsize"], dpi=style["dpi"])
    ax = plt.axes(projection=projection_for(mode))
    if mode == "contour_robinson":
        ax.set_global()
    else:
        format_axes(ax, style, mode)

    lon, lat, value = data["lon"], data["lat"], data["value"]

    if mode == "contour_robinson":
        cmap = mpl.colors.ListedColormap(PALETTES["contour_robinson"])
        levels = np.asarray(style["discrete_levels"])
        norm = mpl.colors.BoundaryNorm(levels, cmap.N)
        im = ax.pcolormesh(lon, lat, value, cmap=cmap, norm=norm, shading="auto", transform=ccrs.PlateCarree(), zorder=1)
        ax.contour(lon, lat, value, levels=style["contour_levels"], colors="black", linewidths=0.45, alpha=0.9, transform=ccrs.PlateCarree(), zorder=3)
        add_land(ax, {**style, "land_color": "#f2f2f2", "land_linewidth": 0.45, "border_linewidth": 0})
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines["geo"].set_linewidth(0.7)
        ax.spines["geo"].set_edgecolor("0.5")
        cbar = plt.colorbar(im, ax=ax, orientation="horizontal", fraction=0.065, pad=0.08, shrink=0.83, ticks=levels, boundaries=levels, spacing="proportional", drawedges=True)
        cbar.ax.tick_params(labelsize=style["font_size"], length=0, width=0.7)
        if cbar.solids is not None:
            cbar.solids.set_edgecolor("black")
            cbar.solids.set_linewidth(0.3)
        cbar.set_ticklabels([str(int(i)) for i in levels])
    elif mode == "quiver_log":
        cmap = mpl.colors.LinearSegmentedColormap.from_list("contaminant_load", PALETTES["quiver_log"], N=256)
        norm = mpl.colors.LogNorm(vmin=1e-6, vmax=2e-1)
        ax.gridlines(draw_labels=False, linewidth=0.45, color="0.75", alpha=0.7, linestyle="-")
        im = ax.pcolormesh(lon, lat, value, cmap=cmap, norm=norm, shading="auto", transform=ccrs.PlateCarree(), zorder=1)
        ax.quiver(data["qlon"], data["qlat"], data["u"], data["v"], transform=ccrs.PlateCarree(), color="black", scale=style["quiver_scale"], width=0.0026, headwidth=3.2, headlength=4.2, headaxislength=3.6, alpha=0.9, zorder=3)
        add_land(ax, {**style, "land_color": "#d9d9d9", "land_linewidth": 0.5})
        ax.text(-0.09, 0.50, text["side_label"], transform=ax.transAxes, fontsize=style["font_size"] + 1, ha="right", va="center")
        ax.annotate("", xy=(0.86, 0.95), xytext=(0.77, 0.95), xycoords="axes fraction", arrowprops=dict(arrowstyle="->", color="red", lw=0.9))
        ax.text(0.865, 0.95, text["quiver_label"], transform=ax.transAxes, fontsize=style["font_size"], va="center", ha="left")
        cbar = plt.colorbar(im, ax=ax, orientation="vertical", fraction=0.05, pad=0.02, extend="both")
        cbar.set_ticks([1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1])
        cbar.set_ticklabels([r"$10^{-6}$", r"$10^{-5}$", r"$10^{-4}$", r"$10^{-3}$", r"$10^{-2}$", r"$10^{-1}$"])
        cbar.ax.tick_params(labelsize=style["font_size"], length=3, width=0.7)
        cbar.outline.set_linewidth(0.7)
    elif mode == "hotspot":
        cmap = mpl.colors.LinearSegmentedColormap.from_list("habitat_hotspot", PALETTES["hotspot"], N=256)
        norm = mpl.colors.Normalize(vmin=0, vmax=style["hotspot_vmax"])
        ax.add_feature(cfeature.LAND, facecolor="#e9e9e9", edgecolor="none", zorder=1)
        ax.add_feature(cfeature.COASTLINE, linewidth=0.25, edgecolor="0.45", zorder=4)
        im = ax.imshow(value, extent=[lon.min(), lon.max(), lat.min(), lat.max()], origin="lower", transform=ccrs.PlateCarree(), cmap=cmap, norm=norm, alpha=0.88, zorder=2)
        add_land(ax, {**style, "land_color": "#e9e9e9", "land_linewidth": 0.25, "border_linewidth": 0}, ocean_mask=True)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines["geo"].set_visible(False)
        fig.text(0.065, 0.50, text["hotspot_side_label"], rotation=90, fontsize=style["font_size"] + 2, ha="center", va="center")
        cax = fig.add_axes([0.105, 0.20, 0.026, 0.20])
        cb = plt.colorbar(im, cax=cax, orientation="vertical")
        cb.set_ticks([0, style["hotspot_vmax"]])
        cb.set_ticklabels(["0", f"{style['hotspot_vmax']:.2f}"])
        cb.outline.set_visible(False)
        cb.ax.tick_params(labelsize=style["font_size"], length=0, pad=3)
        fig.text(0.145, 0.30, text["hotspot_colorbar_label"], rotation=270, fontsize=style["font_size"] + 1, ha="center", va="center")
    else:
        cmap = mpl.colors.LinearSegmentedColormap.from_list("plastic_ingestion_risk", PALETTES["log_raster"], N=256)
        norm = mpl.colors.LogNorm(vmin=style["log_vmin"], vmax=style["log_vmax"])
        im = ax.pcolormesh(lon, lat, value, cmap=cmap, norm=norm, shading="auto", transform=ccrs.PlateCarree(), zorder=1)
        add_land(ax, style)
        cbar = plt.colorbar(im, ax=ax, orientation="horizontal", fraction=0.09, pad=0.10, shrink=0.94, extend="both")
        cbar.set_label(text["colorbar_label"], fontsize=style["font_size"] + 0.5, labelpad=4)
        cbar.set_ticks([1e-14, 1e-13, 1e-12, 1e-11, 1e-10])
        cbar.set_ticklabels([r"$10^{-14}$", r"$10^{-13}$", r"$10^{-12}$", r"$10^{-11}$", r"$10^{-10}$"])
        cbar.ax.tick_params(labelsize=style["font_size"], length=3, width=0.7)
        cbar.outline.set_linewidth(0.7)

    if text.get("title"):
        ax.set_title(text["title"], fontsize=style["font_size"] + 1, pad=5)
    if style.get("panel_label"):
        fig.text(0.055, 0.88, style["panel_label"], fontsize=style["font_size"] + 2, fontweight="bold", ha="left", va="center")
    return fig


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
