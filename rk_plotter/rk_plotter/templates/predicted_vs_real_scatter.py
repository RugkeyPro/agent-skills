from __future__ import annotations

import os
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Core template metadata
TEMPLATE_ID = 'predicted_vs_real_scatter'
CATEGORY = 'scatter_model'
KIND = 'predicted_real'
TITLE = 'Predicted vs real scatter plot'
DESCRIPTION = 'prediction diagnostics with one-to-one lines'
TAGS = ('scatter_model', 'predicted_real', 'scatter', 'prediction', 'observed', 'predicted', 'one_to_one', 'model_validation', 'model_diagnostic', 'square')
STYLE_PROFILE = {
    'figsize': (3.7, 3.7),
    'palette': 'prediction_scatter',
    'aspect': 'square',
    'layout': ('square_panel', 'one_to_one_line'),
    'plot_primitives': ('scatter', 'line', 'text')
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
    """Generates synthetic ML prediction data (Observed vs Predicted)."""
    rng = np.random.default_rng(seed)
    real = rng.uniform(10, 100, 200)
    predicted = 0.92 * real + 5.0 + rng.normal(0, 6.5, 200)
    return {
        "x": real,
        "y": predicted,
        "xlabel": "Measured Values",
        "ylabel": "Predicted Values",
        "title": "Observed vs. Predicted Diagnostic"
    }

def plot(data=None, *, ax=None, x=None, y=None, xlabel=None, ylabel=None, title=None, config=None):
    """
    Plots a professional ML model Observed vs. Predicted scatter plot with 1:1 line,
    regression fit, and performance metrics (R2, RMSE, MAE).
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
        real = data.get("x", data.get("real", data.get("observed")))
        pred = data.get("y", data.get("predicted", data.get("modeled")))
        if real is None or pred is None:
            dict_vals = list(data.values())
            real, pred = dict_vals[0], dict_vals[1]
        plot_xlabel = xlabel or data.get("xlabel", "Observed Values")
        plot_ylabel = ylabel or data.get("ylabel", "Predicted Values")
        plot_title = title or data.get("title", TITLE)
    elif isinstance(data, pd.DataFrame):
        plot_x_col = x or data.columns[0]
        plot_y_col = y or data.columns[1]
        real = data[plot_x_col].values
        pred = data[plot_y_col].values
        plot_xlabel = xlabel or plot_x_col
        plot_ylabel = ylabel or plot_y_col
        plot_title = title or TITLE
    else:
        raise TypeError("Data must be either a dict or a pandas DataFrame")
        
    # Filter out NaNs
    mask = ~np.isnan(real) & ~np.isnan(pred)
    real = real[mask]
    pred = pred[mask]
    
    if len(real) == 0:
        raise ValueError("Input data contains no valid coordinates")

    # Calculate model metrics
    slope, intercept = np.polyfit(real, pred, 1)
    y_mean = np.mean(real)
    ss_tot = np.sum((real - y_mean) ** 2)
    ss_res = np.sum((real - pred) ** 2)
    r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    rmse = np.sqrt(np.mean((real - pred) ** 2))
    mae = np.mean(np.abs(real - pred))
    
    # Plot scatter points
    ax.scatter(
        real,
        pred,
        color="#4C78A8",
        s=12,
        alpha=0.6,
        edgecolors="#2b5078",
        linewidths=0.5,
        label="Data Points",
        zorder=2
    )
    
    # Square aspect ratio scaling
    xmin, xmax = real.min(), real.max()
    ymin, ymax = pred.min(), pred.max()
    lim_min = min(xmin, ymin) - 0.05 * abs(xmin)
    lim_max = max(xmax, ymax) + 0.05 * abs(xmax)
    
    ax.set_xlim(lim_min, lim_max)
    ax.set_ylim(lim_min, lim_max)
    ax.set_aspect("equal", adjustable="box")
    
    # Draw 1:1 Reference Line
    ax.plot(
        [lim_min, lim_max],
        [lim_min, lim_max],
        color="#333333",
        linestyle="-",
        linewidth=0.8,
        label="1:1 Reference",
        zorder=1
    )
    
    # Draw fitted regression line
    fit_x = np.array([lim_min, lim_max])
    fit_y = slope * fit_x + intercept
    ax.plot(
        fit_x,
        fit_y,
        color="#E15759",
        linestyle="--",
        linewidth=1.2,
        label="Linear Fit",
        zorder=3
    )
    
    # Grids and spines styling
    ax.grid(True, linestyle="-", color="#f2f2f2", linewidth=0.6, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    
    # Text box metrics
    stats_text = (
        f"$R^2$ = {r2:.3f}\n"
        f"RMSE = {rmse:.2f}\n"
        f"MAE = {mae:.2f}\n"
        f"N = {len(real)}"
    )
    ax.text(
        0.05, 0.95,
        stats_text,
        transform=ax.transAxes,
        fontsize=7.5,
        verticalalignment='top',
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="#cccccc", alpha=0.9, linewidth=0.5)
    )
    
    # Labels and legend
    ax.set_title(plot_title, loc="left", fontweight="bold", pad=12)
    ax.set_xlabel(plot_xlabel)
    ax.set_ylabel(plot_ylabel)
    ax.legend(frameon=False, loc="lower right")
    
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
    outputs = render("outputs", basename="predicted_vs_real_demo")
    print(f"Done! Outputs saved to: {[str(p) for p in outputs]}")
