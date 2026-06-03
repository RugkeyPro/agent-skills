# TEMPLATE_ID: choropleth_map
# TEMPLATE_VERSION: 1.0
# FIGURE_TYPE: geographical_country_choropleth_map
# LOCKED_STRUCTURE:
# - Cartopy map projection (Robinson)
# - country geometry boundaries colored by metric value
# - ocean backdrop features
# - horizontal colorbar on bottom
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
import matplotlib.colors as mcolors
import pandas as pd
import numpy as np
from pathlib import Path

import sys
import subprocess

# Cartopy imports are auto-installed if missing to prevent layout degradation
try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    import cartopy.io.shapereader as shpreader
except ImportError:
    print("Required package 'cartopy' is missing. Attempting automatic installation...", file=sys.stderr)
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "cartopy"], check=True)
        import cartopy.crs as ccrs
        import cartopy.feature as cfeature
        import cartopy.io.shapereader as shpreader
    except Exception as e:
        raise ImportError(
            "Failed to automatically install 'cartopy'. Please install it manually "
            "using 'pip install cartopy' to run this template."
        ) from e

TEMPLATE_ID = "choropleth_map"

FIELD_MAP = {
    "region": "ISO_Country",
    "value": "Emission_Index",
}

TEXT_CONFIG = {
    "title": "Country-level CO2 Emission Index",
    "metric_label": "Emission Index (tonnes/capita)",
}

STYLE_CONFIG = {
    "figsize": (12.5, 5.4),
    "font_family": "sans-serif",
    "font_sans": ["Arial", "DejaVu Sans", "Helvetica", "Microsoft YaHei"],
    "font_size": 8.5,
    "cmap": "YlOrRd",
    "missing_facecolor": "#E5E5E5",
    "missing_edgecolor": "#BBBBBB",
    "boundary_edgecolor": "#555555",
    "axis_linewidth": 0.8,
}

EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "choropleth_map",
    "formats": ["svg", "pdf", "png"],
    "dpi": 600,
}

def load_data(path: str | Path) -> pd.DataFrame:
    """Loads country index CSV. Falls back to generating sample data if missing."""
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    
    # Generate mock country-level indices
    countries = {
        "CHN": 92.5, "USA": 88.0, "IND": 74.2, "BRA": 65.8, "RUS": 70.1,
        "CAN": 78.4, "DEU": 68.2, "GBR": 62.5, "FRA": 64.1, "JPN": 72.8,
        "AUS": 79.6, "ZAF": 55.4, "NGA": 48.2, "IDN": 66.5, "MEX": 61.2,
        "TUR": 58.6, "ESP": 60.1, "ITA": 59.8, "KOR": 75.3, "SAU": 63.8
    }
    return pd.DataFrame({
        "ISO_Country": list(countries.keys()),
        "Emission_Index": list(countries.values())
    })

def prepare_data(df: pd.DataFrame, field_map: dict) -> dict[str, float]:
    """Standardizes ISO codes and metric values into mapping dictionary."""
    regions = df[field_map["region"]].astype(str).str.strip().str.upper()
    values = pd.to_numeric(df[field_map["value"]], errors="coerce")
    
    clean_df = pd.DataFrame({"region": regions, "value": values}).dropna()
    return dict(zip(clean_df["region"], clean_df["value"]))

def apply_style(style: dict) -> None:
    """Applies clean matplotlib typography settings."""
    plt.rcParams.update({
        "font.family": style["font_family"],
        "font.sans-serif": style["font_sans"],
        "font.size": style["font_size"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.linewidth": style["axis_linewidth"]
    })

def plot(data: dict[str, float], text: dict, style: dict) -> plt.Figure:
    """Plots global country-level choropleth map."""
    apply_style(style)
    
    proj = ccrs.Robinson(central_longitude=0)
    fig, ax = plt.subplots(figsize=style["figsize"], subplot_kw={"projection": proj}, dpi=300)
    
    vals = list(data.values())
    vmin = min(vals) if vals else 0.0
    vmax = max(vals) if vals else 100.0
    
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    colormap = plt.get_cmap(style["cmap"])
    
    ax.set_global()
    ax.add_feature(cfeature.OCEAN, facecolor="#F4F8FA", zorder=0)
    ax.add_feature(cfeature.LAKES, facecolor="#F4F8FA", edgecolor="none", zorder=0)
    
    # Render country outlines using Natural Earth shapefile geometry
    try:
        shpfilename = shpreader.natural_earth(resolution="110m", category="cultural", name="admin_0_countries")
        reader = shpreader.Reader(shpfilename)
        
        for record in reader.records():
            geom = record.geometry
            attrs = record.attributes
            
            # Match geometries by checking common ISO identifier matches
            iso3 = str(attrs.get("ISO_A3", "")).upper()
            adm0 = str(attrs.get("ADM0_A3", "")).upper()
            name = str(attrs.get("NAME", "")).upper()
            
            match_val = None
            for k in [iso3, adm0, name]:
                if k in data:
                    match_val = data[k]
                    break
                    
            if match_val is not None:
                color = colormap(norm(match_val))
                edgecolor = style["boundary_edgecolor"]
                linewidth = 0.25
                zorder = 2
            else:
                color = style["missing_facecolor"]
                edgecolor = style["missing_edgecolor"]
                linewidth = 0.15
                zorder = 1
                
            ax.add_geometries(
                [geom],
                ccrs.PlateCarree(),
                facecolor=color,
                edgecolor=edgecolor,
                linewidth=linewidth,
                zorder=zorder
            )
            
    except Exception as e:
        print(f"Warning: Cartopy shapefile load failed: {e}")
        ax.text(0.5, 0.5, "Geographical Map Download Failed\n(Cartopy Shapefile Fetch Error)", transform=ax.transAxes, ha="center", va="center", color="#888888")
        
    ax.gridlines(draw_labels=False, color="#E0E0E0", linestyle=":", linewidth=0.5, zorder=3)
    ax.set_title(text["title"], loc="left", fontweight="bold", pad=14)
    
    # Colorbar at the bottom
    sm = plt.cm.ScalarMappable(cmap=colormap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(
        sm,
        ax=ax,
        orientation="horizontal",
        fraction=0.045,
        pad=0.06,
        aspect=45
    )
    cbar.set_label(text["metric_label"], fontsize=style["font_size"] - 1)
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
