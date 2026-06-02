from __future__ import annotations

import os
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns  # Registers seaborn colormaps like 'mako'
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde

# Core template metadata
TEMPLATE_ID = 'density_colored_scatter'
CATEGORY = 'scatter_model'
KIND = 'density_scatter'
TITLE = 'Density colored scatter plot'
DESCRIPTION = 'dense point clouds with density color'
TAGS = ('scatter_model', 'density_scatter', 'scatter', 'dense_points', 'density', 'continuous_color', 'relationship', 'overplotting')
STYLE_PROFILE = {
    'figsize': (4.2, 3.3),
    'palette': 'continuous_density',
    'aspect': 'standard',
    'layout': ('single_panel', 'inset_colorbar'),
    'plot_primitives': ('scatter', 'density_color', 'one_to_one_line')
}

STYLE_RC = {
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans", "Helvetica", "Microsoft YaHei"],
    "font.size": 8.5,
    "axes.titlesize": 9.5,
    "axes.labelsize": 8.5,
    "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5,
    "legend.fontsize": 7.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "savefig.transparent": True,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
}

def make_sample_data(seed: int = 42) -> dict:
    """Generates a dense point cloud with correlation and skewness."""
    rng = np.random.default_rng(seed)
    mean = [2.0, 2.2]
    cov = [[0.8, 0.6], [0.6, 0.8]]
    x, y = rng.multivariate_normal(mean, cov, 1000).T
    x += rng.exponential(0.3, 1000)
    y += rng.exponential(0.3, 1000)
    return {
        "x": x,
        "y": y,
        "xlabel": "Observed Value",
        "ylabel": "Simulated Value",
        "title": "Density Colored Scatter Plot"
    }

def plot(data=None, *, ax=None, x=None, y=None, xlabel=None, ylabel=None, title=None, config=None):
    """
    Plots a high-quality scatter plot where points are colored by local kernel density.
    """
    matplotlib.rcParams.update(STYLE_RC)
    
    if data is None:
        data = make_sample_data()
        
    fig = None
    figsize = (config or {}).get("figsize", STYLE_PROFILE["figsize"])
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, dpi=300)
    else:
        fig = ax.figure
        
    # Standardize input variables
    if isinstance(data, dict):
        plot_x = data["x"]
        plot_y = data["y"]
        plot_xlabel = xlabel or data.get("xlabel", "X Axis")
        plot_ylabel = ylabel or data.get("ylabel", "Y Axis")
        plot_title = title or data.get("title", TITLE)
    elif isinstance(data, pd.DataFrame):
        plot_x_col = x or data.columns[0]
        plot_y_col = y or data.columns[1]
        plot_x = data[plot_x_col].values
        plot_y = data[plot_y_col].values
        plot_xlabel = xlabel or plot_x_col
        plot_ylabel = ylabel or plot_y_col
        plot_title = title or TITLE
    else:
        raise TypeError("Data must be either a dict or a pandas DataFrame")
        
    # Remove NaNs
    mask = ~np.isnan(plot_x) & ~np.isnan(plot_y)
    plot_x = plot_x[mask]
    plot_y = plot_y[mask]
    
    if len(plot_x) == 0:
        raise ValueError("Input data contains no valid, non-NaN coordinates")

    # Perform Gaussian KDE
    xy = np.vstack([plot_x, plot_y])
    kde = gaussian_kde(xy)
    z = kde(xy)
    
    # Sort points by density
    idx = z.argsort()
    plot_x, plot_y, z = plot_x[idx], plot_y[idx], z[idx]
    
    scatter = ax.scatter(
        plot_x,
        plot_y,
        c=z,
        cmap="mako",
        s=8,
        alpha=0.8,
        edgecolors="none",
        zorder=2
    )
    
    # Diagonal 1:1 reference line
    lim_min = min(ax.get_xlim()[0], ax.get_ylim()[0])
    lim_max = max(ax.get_xlim()[1], ax.get_ylim()[1])
    ax.plot([lim_min, lim_max], [lim_min, lim_max], color="#888888", linestyle="--", linewidth=1.0, zorder=1, alpha=0.7)
    
    # Grid lines and spines
    ax.grid(True, linestyle="-", color="#f0f0f0", linewidth=0.6, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    
    # Titles and Labels
    ax.set_title(plot_title, loc="left", fontweight="bold", pad=12)
    ax.set_xlabel(plot_xlabel)
    ax.set_ylabel(plot_ylabel)
    
    # Colorbar
    cbar = fig.colorbar(scatter, ax=ax, fraction=0.035, pad=0.04)
    cbar.set_label("Relative Density", fontsize=7.5)
    cbar.ax.tick_params(labelsize=6.5)
    cbar.outline.set_visible(False)
    
    # Apply user-customized config title/labels if provided
    if config:
        if "x_label" in config:
            ax.set_xlabel(config["x_label"])
        if "y_label" in config:
            ax.set_ylabel(config["y_label"])
        if "title" in config:
            ax.set_title(config["title"], loc="left", fontweight="bold", pad=12)
            
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
    outputs = render("outputs", basename="density_scatter_demo")
    print(f"Done! Outputs saved to: {[str(p) for p in outputs]}")
