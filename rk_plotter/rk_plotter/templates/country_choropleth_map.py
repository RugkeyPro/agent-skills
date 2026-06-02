from __future__ import annotations

import os
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader

# Core template metadata
TEMPLATE_ID = 'country_choropleth_map'
CATEGORY = 'maps'
KIND = 'country_choropleth'
TITLE = 'Country-level choropleth map'
DESCRIPTION = 'country or administrative-unit maps'
TAGS = ('maps', 'country_choropleth', 'spatial', 'map', 'choropleth', 'country', 'administrative_units', 'binned', 'regional')
STYLE_PROFILE = {
    'figsize': (12.5, 5.4),
    'palette': 'binned_choropleth',
    'aspect': 'wide',
    'layout': ('map_projection', 'discrete_colorbar'),
    'plot_primitives': ('choropleth',)
}

STYLE_RC = {
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans", "Helvetica", "Microsoft YaHei"],
    "font.size": 9.0,
    "axes.titlesize": 10.5,
    "axes.labelsize": 9.0,
    "legend.fontsize": 8.0,
    "savefig.transparent": True,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
}

def make_sample_data(seed: int = 42) -> dict:
    """Generates sample country-level plastic emission index data."""
    countries_data = {
        "CHN": 95.5, "USA": 82.3, "IND": 78.4, "BRA": 65.2, "IDN": 72.1,
        "RUS": 58.0, "ZAF": 49.6, "DEU": 42.1, "GBR": 39.8, "FRA": 41.2,
        "AUS": 35.5, "CAN": 38.0, "JPN": 45.4, "MEX": 59.3, "NGA": 61.2,
        "EGY": 52.8, "SAU": 48.0, "TUR": 51.5, "ESP": 38.5, "ITA": 39.2,
        "KOR": 44.1, "ARG": 47.3, "COL": 49.5, "THA": 58.7, "VNM": 63.4
    }
    return {
        "countries": countries_data,
        "metric": "Emissions Index",
        "title": "Global Plastic Emissions Index by Country"
    }

def plot(data=None, *, ax=None, country_col=None, value_col=None, title=None, cmap="YlOrRd", config=None):
    """
    Plots a genuine publication-quality Global Country-level Choropleth map
    using Cartopy Robinson projection and Natural Earth shapefiles.
    """
    matplotlib.rcParams.update(STYLE_RC)
    
    if data is None:
        data = make_sample_data()
        
    fig = None
    figsize = (config or {}).get("figsize", STYLE_PROFILE["figsize"])
    
    proj = ccrs.Robinson(central_longitude=0)
    
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, subplot_kw={'projection': proj}, dpi=300)
    else:
        fig = ax.figure
        if not hasattr(ax, 'projection'):
            raise ValueError("Provided 'ax' must be initialized with a Cartopy projection")
            
    # Standardize input variables
    mapping_dict = {}
    metric_name = "Value"
    plot_title = title or TITLE
    
    if isinstance(data, dict):
        if "countries" in data and isinstance(data["countries"], dict):
            mapping_dict = data["countries"]
            metric_name = data.get("metric", "Value")
            plot_title = title or data.get("title", TITLE)
        else:
            mapping_dict = data
    elif isinstance(data, pd.DataFrame):
        c_col = country_col or data.columns[0]
        v_col = value_col or data.columns[1]
        mapping_dict = dict(zip(data[c_col].astype(str).str.upper(), data[v_col].astype(float)))
        metric_name = v_col
        plot_title = title or TITLE
    else:
        raise TypeError("Data must be either a dict or a pandas DataFrame")

    mapping_dict = {str(k).strip().upper(): v for k, v in mapping_dict.items()}

    vals = list(mapping_dict.values())
    if len(vals) > 0:
        vmin = min(vals)
        vmax = max(vals)
    else:
        vmin, vmax = 0, 100
        
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    colormap = plt.get_cmap(cmap)
    
    ax.set_global()
    ax.add_feature(cfeature.OCEAN, facecolor="#F4F8FA", zorder=0)
    ax.add_feature(cfeature.LAKES, facecolor="#F4F8FA", edgecolor="none", zorder=0)
    
    try:
        shpfilename = shpreader.natural_earth(resolution='110m', category='cultural', name='admin_0_countries')
        reader = shpreader.Reader(shpfilename)
        
        for record in reader.records():
            geom = record.geometry
            attrs = record.attributes
            
            iso3 = str(attrs.get('ISO_A3', '')).upper()
            adm0 = str(attrs.get('ADM0_A3', '')).upper()
            name = str(attrs.get('NAME', '')).upper()
            
            val = None
            for key in [iso3, adm0, name]:
                if key in mapping_dict:
                    val = mapping_dict[key]
                    break
                    
            if val is not None:
                color = colormap(norm(val))
                edgecolor = "#555555"
                linewidth = 0.25
                zorder = 2
            else:
                color = "#E5E5E5"
                edgecolor = "#bbbbbb"
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
        print(f"Warning: Cartopy shapefile loading failed: {e}. Drawing fallback regional indicator...")
        ax.text(
            0.5, 0.5,
            "Geographical Map Download Failed\n(Cartopy Shapefile Fetch Error)",
            transform=ax.transAxes,
            ha="center", va="center",
            color="#888888", fontsize=12
        )
        
    ax.gridlines(draw_labels=False, dms=True, xlocs=None, ylocs=None, color="#e0e0e0", linestyle=":", linewidth=0.5, zorder=3)
    ax.set_title(plot_title, loc="left", fontweight="bold", pad=14)
    
    # Professional bottom colorbar
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
    cbar.set_label(metric_name, fontsize=8.0)
    cbar.ax.tick_params(labelsize=7.5)
    cbar.outline.set_visible(False)
    
    # Apply user-customized config title/labels if provided
    if config:
        if "y_label" in config:  # map metric label override
            cbar.set_label(config["y_label"], fontsize=8.0)
        if "title" in config:
            ax.set_title(config["title"], loc="left", fontweight="bold", pad=14)
            
    return fig, ax

def render(output_dir, basename=None, formats=("png", "pdf", "svg"), seed: int = 42, data=None, config=None):
    """Renders and saves the figure in high resolution in multiple formats."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    fig, ax = plot(data=data, config=config)
    basename = basename or TEMPLATE_ID
    
    paths = []
    for fmt in formats:
        fmt = fmt.lower().lstrip(".")
        filename = out_dir / f"{basename}.{fmt}"
        kwargs = {"bbox_inches": "tight", "transparent": True}
        if fmt in {"png", "jpg", "jpeg", "tif", "tiff"}:
            kwargs["dpi"] = 600
        fig.savefig(filename, **kwargs)
        paths.append(filename)
        
    plt.close(fig)
    return paths

if __name__ == "__main__":
    outputs = render("outputs", basename="country_choropleth_demo")
    print(f"Done! Outputs saved to: {[str(p) for p in outputs]}")
