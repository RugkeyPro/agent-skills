# TEMPLATE_ID: raster_map
# TEMPLATE_VERSION: 1.0
# FIGURE_TYPE: geographical_spatial_raster_map
# LOCKED_STRUCTURE:
# - Cartopy map projection subplot (Robinson projection by default)
# - spatial gridline overlays
# - ocean and land boundary backdrops
# - colorbar matching map height
# EDITABLE:
# - FIELD_MAP
# - TEXT_CONFIG
# - STYLE_CONFIG
# - EXPORT_CONFIG
# - data loading path

from __future__ import annotations
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path

# Cartopy imports must be wrapped or handled gracefully
try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    HAS_CARTOPY = True
except ImportError:
    HAS_CARTOPY = False

TEMPLATE_ID = "raster_map"

FIELD_MAP = {
    "lon": "Longitude",
    "lat": "Latitude",
    "value": "Anomalies",
}

TEXT_CONFIG = {
    "title": "Global Sea Surface Temperature Anomalies",
    "colorbar_label": "Temperature Anomaly (°C)",
}

STYLE_CONFIG = {
    "figsize": (7.2, 4.0),
    "font_family": "sans-serif",
    "font_sans": ["Arial", "DejaVu Sans", "Helvetica", "Microsoft YaHei"],
    "font_size": 8.5,
    "cmap": "coolwarm",     # Diverging warm/cold color palette
    "axis_linewidth": 0.8,
}

EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "raster_map",
    "formats": ["svg", "pdf", "png"],
    "dpi": 600,
}

def load_data(path: str | Path) -> pd.DataFrame:
    """Loads dataset from CSV file. Falls back to generating sample data if missing."""
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    
    # Generate 1-degree global grid data
    lons = np.linspace(-180, 180, 180)
    lats = np.linspace(-90, 90, 90)
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    
    # Generate realistic looking temperature anomaly fields using sinusoidal gradients
    anomalies = 2.5 * np.sin(np.deg2rad(lon_grid)) * np.cos(np.deg2rad(lat_grid))
    rng = np.random.default_rng(42)
    anomalies += rng.normal(0, 0.25, anomalies.shape)
    
    # Flatten grid to 3-column long dataframe format
    data = pd.DataFrame({
        "Longitude": lon_grid.flatten(),
        "Latitude": lat_grid.flatten(),
        "Anomalies": anomalies.flatten()
    })
    return data

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
    """Applies matplotlib text parameters."""
    plt.rcParams.update({
        "font.family": style["font_family"],
        "font.sans-serif": style["font_sans"],
        "font.size": style["font_size"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.linewidth": style["axis_linewidth"]
    })

def plot(data: dict[str, np.ndarray], text: dict, style: dict) -> plt.Figure:
    """Plots Cartopy Robinson projected spatial grid map."""
    apply_style(style)
    
    # Check cartopy presence
    if not HAS_CARTOPY:
        # Fallback to standard matplotlib subplots if Cartopy not installed
        fig, ax = plt.subplots(figsize=style["figsize"], dpi=300)
        im = ax.imshow(data["raster"], extent=[-180, 180, -90, 90], origin="lower", cmap=style["cmap"], aspect="auto")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_title(text["title"] + " (Cartopy Fallback)", loc="left", fontweight="bold")
        cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label(text["colorbar_label"])
        cbar.outline.set_visible(False)
        return fig
        
    proj = ccrs.Robinson(central_longitude=0)
    fig, ax = plt.subplots(figsize=style["figsize"], subplot_kw={"projection": proj}, dpi=300)
    
    # Map layers configurations
    ax.set_global()
    ax.add_feature(cfeature.OCEAN, facecolor="#F5F8FA", zorder=0)
    ax.add_feature(cfeature.LAND, facecolor="#E5E5E5", edgecolor="none", zorder=1)
    
    lon = data["lon"]
    lat = data["lat"]
    raster = data["raster"]
    
    # Plot spatial mesh colored surface
    im = ax.pcolormesh(
        lon,
        lat,
        raster,
        transform=ccrs.PlateCarree(),
        cmap=style["cmap"],
        shading="auto",
        zorder=2
    )
    
    # Add borders and coastlines above data raster
    ax.add_feature(cfeature.COASTLINE, linewidth=0.4, edgecolor="#555555", zorder=3)
    ax.add_feature(cfeature.BORDERS, linewidth=0.25, edgecolor="#888888", zorder=3)
    
    # Display gridline tracks
    ax.gridlines(draw_labels=False, dms=True, color="#d3d3d3", linestyle=":", linewidth=0.5, zorder=4)
    
    ax.set_title(text["title"], loc="left", fontweight="bold", pad=12)
    
    # Standard colorbar right layout
    cbar = fig.colorbar(im, ax=ax, orientation="horizontal", fraction=0.045, pad=0.06, aspect=45)
    cbar.set_label(text["colorbar_label"], fontsize=style["font_size"] - 1)
    cbar.ax.tick_params(labelsize=style["font_size"] - 2)
    cbar.outline.set_visible(False)
    
    return fig

def save_outputs(fig: plt.Figure, export: dict) -> list[Path]:
    """Exports files."""
    output_dir = Path(export["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for fmt in export["formats"]:
        path = output_dir / f"{export['basename']}.{fmt}"
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
