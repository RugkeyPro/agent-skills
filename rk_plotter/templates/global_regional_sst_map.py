# TEMPLATE_ID: global_regional_sst_map
# TEMPLATE_VERSION: 1.1
# FIGURE_TYPE: global_regional_sst_contourf_map
#
# CORE_VISUAL_GRAMMAR:
# - PlateCarree projection map with central_longitude=180
# - coastline features, land polygons, and specific gridlines
# - horizontal colorbar on bottom
#
# COMMON_ADAPTATIONS:
# - add region outline boxes (axvspan/rectangle)
# - add scatter markers for observation stations
# - overlay isotherm contour lines with labels
# - add zoomed regional inset maps
#
# DO_NOT_CHANGE:
# - do not degrade or fallback to non-geographical plots
# - do not change central projection meridian
#
# EDITABLE:
# - FIELD_MAP
# - TEXT_CONFIG
# - STYLE_CONFIG
# - EXPORT_CONFIG
# - data loading and preparation logic

from __future__ import annotations
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np
from pathlib import Path

import sys
import subprocess

# Cartopy imports are auto-installed if missing to prevent layout degradation
try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
except ImportError:
    print("Required package 'cartopy' is missing. Attempting automatic installation...", file=sys.stderr)
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "cartopy"], check=True)
        import cartopy.crs as ccrs
        import cartopy.feature as cfeature
    except Exception as e:
        raise ImportError(
            "Failed to automatically install 'cartopy'. Please install it manually "
            "using 'pip install cartopy' to run this template."
        ) from e

TEMPLATE_ID = "global_regional_sst_map"

FIELD_MAP = {
    "lon": "lon",
    "lat": "lat",
    "value": "delta_sst",
}

TEXT_CONFIG = {
    "title": "A. ΔSST (CMIP6)",
    "colorbar_label": "ΔSST (°C)",
}

STYLE_CONFIG = {
    "figsize": (10.0, 6.0),
    "font_family": "sans-serif",
    "font_sans": ["Arial", "DejaVu Sans", "Helvetica", "Microsoft YaHei"],
    "font_size": 8.5,
    "cmap": "RdYlBu_r",     # Diverging warm/cold color palette
    "axis_linewidth": 1.0,
    "land_color": "#d3d3d3",
    "coastline_color": "#000000",
    "gridline_color": "#808080",
    "levels": np.arange(0, 6.1, 0.5),
}

EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "global_regional_sst_map",
    "formats": ["svg", "pdf", "png"],
    "dpi": 600,
}

def load_data(path: str | Path) -> pd.DataFrame:
    """Loads dataset from CSV file. Falls back to generating sample data if missing."""
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    
    # Generate virtual SST change data
    rng = np.random.default_rng(42)
    lons = np.linspace(0, 360, 180)
    lats = np.linspace(-60, 60, 90)
    lon_grid, lat_grid = np.meshgrid(lons, lats)

    # Base meridional warming: higher at low latitudes
    base = 2.5 + 2.0 * np.cos(np.deg2rad(lat_grid))

    # Zonal wave pattern (ocean basins differences)
    basin_pattern = (
        0.35 * np.sin(np.deg2rad(lon_grid * 1.4))
        + 0.25 * np.cos(np.deg2rad(lon_grid * 2.2 + lat_grid))
    )

    # Localized anomalies simulating ocean warm pools
    warm_pool = (
        0.65 * np.exp(-((lon_grid - 150) ** 2 / (2 * 35 ** 2) + (lat_grid - 5) ** 2 / (2 * 18 ** 2)))
        + 0.45 * np.exp(-((lon_grid - 220) ** 2 / (2 * 42 ** 2) + (lat_grid + 10) ** 2 / (2 * 20 ** 2)))
    )

    noise = rng.normal(0, 0.18, size=lon_grid.shape)
    data = base + basin_pattern + warm_pool + noise
    data = np.clip(data, 0, 6)

    df = pd.DataFrame({
        "lon": lon_grid.ravel(),
        "lat": lat_grid.ravel(),
        "delta_sst": data.ravel()
    })
    return df

def prepare_data(df: pd.DataFrame, field_map: dict) -> dict[str, np.ndarray]:
    """Pivots tabular coordinate columns into 2D meshes."""
    lon_col = pd.to_numeric(df[field_map["lon"]], errors="coerce")
    lat_col = pd.to_numeric(df[field_map["lat"]], errors="coerce")
    val_col = pd.to_numeric(df[field_map["value"]], errors="coerce")
    
    clean_df = pd.DataFrame({"lon": lon_col, "lat": lat_col, "value": val_col}).dropna()
    
    # Pivot to mesh grid matrices
    pivoted = clean_df.pivot(index="lat", columns="lon", values="value")
    
    return {
        "lon": pivoted.columns.to_numpy(),
        "lat": pivoted.index.to_numpy(),
        "raster": pivoted.to_numpy()
    }

def apply_style(style: dict) -> None:
    """Applies standard matplotlib properties."""
    plt.rcParams.update({
        "font.family": style["font_family"],
        "font.sans-serif": style["font_sans"],
        "font.size": style["font_size"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.linewidth": style["axis_linewidth"],
        "xtick.direction": "out",
        "ytick.direction": "out",
    })

def plot(data: dict[str, np.ndarray], text: dict, style: dict) -> plt.Figure:
    """Plots global/regional SST map with central_longitude=180."""
    apply_style(style)
    
    proj = ccrs.PlateCarree(central_longitude=180)
    fig, ax = plt.subplots(figsize=style["figsize"], subplot_kw={"projection": proj}, dpi=300)
    
    lon = data["lon"]
    lat = data["lat"]
    raster = data["raster"]
    
    # Draw contourf representation of Delta SST anomalies
    cf = ax.contourf(
        lon,
        lat,
        raster,
        levels=style["levels"],
        transform=ccrs.PlateCarree(),
        cmap=style["cmap"],
        extend="both",
        zorder=0
    )
    
    # Overlay land features
    ax.add_feature(
        cfeature.LAND,
        facecolor=style["land_color"],
        edgecolor="none",
        zorder=2
    )
    
    # Overlay coastline boundaries
    ax.coastlines(
        resolution="110m",
        color=style["coastline_color"],
        linewidth=0.8,
        zorder=3
    )
    
    # Define extent limits
    ax.set_extent(
        [30, 330, -60, 60],
        crs=ccrs.PlateCarree()
    )
    
    # Add geographical ticks and grid lines
    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        draw_labels=True,
        linewidth=0.7,
        linestyle="--",
        color=style["gridline_color"],
        alpha=0.5,
        zorder=4
    )
    gl.top_labels = False
    gl.right_labels = False
    
    gl.xlocator = mticker.FixedLocator([40, 100, 160, 220, 280, 340])
    gl.ylocator = mticker.FixedLocator([-60, -30, 0, 30, 60])
    
    gl.xlabel_style = {"size": style["font_size"], "color": "#000000"}
    gl.ylabel_style = {"size": style["font_size"], "color": "#000000"}
    
    gl.xformatter = mticker.FixedFormatter(["40°E", "100°E", "160°E", "140°W", "80°W", "20°W"])
    gl.yformatter = mticker.FixedFormatter(["60°S", "30°S", "0°", "30°N", "60°N"])
    
    # Title
    ax.set_title(text["title"], loc="left", fontweight="bold", pad=10)
    
    # Bottom Horizontal Colorbar
    cb = fig.colorbar(
        cf,
        ax=ax,
        orientation="horizontal",
        pad=0.10,
        shrink=0.62,
        aspect=24
    )
    cb.set_ticks([0, 2, 4, 6])
    cb.ax.tick_params(labelsize=style["font_size"], length=4, width=0.8, direction="out")
    cb.set_label(text["colorbar_label"], fontsize=style["font_size"] + 0.5, labelpad=6)
    cb.outline.set_linewidth(0.8)
    
    return fig

def save_outputs(fig: plt.Figure, export: dict) -> list[Path]:
    """Saves figure in high-res vector and raster formats."""
    output_dir = Path(export["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for fmt in export["formats"]:
        basename = export["basename"]
        path = output_dir / f"{basename}.{fmt}"
        kwargs: dict = {"bbox_inches": "tight"}
        if fmt.lower() in {"png", "jpg", "jpeg", "tif", "tiff"}:
            kwargs["dpi"] = export["dpi"]
        fig.savefig(path, **kwargs)
        paths.append(path)
    plt.close(fig)
    return paths

def main() -> None:
    df = load_data("data.csv")
    data = prepare_data(df, FIELD_MAP)
    fig = plot(data, TEXT_CONFIG, STYLE_CONFIG)
    paths = save_outputs(fig, EXPORT_CONFIG)
    print(f"Generated: {[str(p) for p in paths]}")

if __name__ == "__main__":
    main()
