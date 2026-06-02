from __future__ import annotations

import os
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Core template metadata (for rk_plotter registry compatibility)
TEMPLATE_ID = 'boxen_plot'
CATEGORY = 'distributions'
KIND = 'boxen'
TITLE = 'Boxen style group distribution'
DESCRIPTION = 'group distributions with quantile bands'
TAGS = ('distributions', 'boxen', 'distribution', 'grouped_samples', 'quantiles', 'small_multiples_not_needed', 'tall', 'category_comparison')
STYLE_PROFILE = {
    'figsize': (4.2, 5.8),
    'palette': 'ordered_categorical',
    'aspect': 'tall',
    'layout': ('single_panel',),
    'plot_primitives': ('quantile_bands', 'scatter')
}

# Scientific Publication Styling constants
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

# Ordered Categorical Palette (Okabe-Ito / Color Universal Design recommended colors)
PALETTE_COLORS = ["#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377", "#BBBBBB"]

def make_sample_data(seed: int = 42) -> dict:
    """Generates synthetic high-quality distribution data for demonstration."""
    rng = np.random.default_rng(seed)
    groups = ["Group A", "Group B", "Group C", "Group D"]
    # Generate skewed and normal distributions to highlight letter-value boxen structure
    values = [
        rng.normal(0.6, 0.2, 200),
        rng.lognormal(0.1, 0.25, 200) - 0.5,
        rng.normal(1.2, 0.35, 200),
        rng.exponential(0.4, 200) + 0.2
    ]
    return {
        "groups": np.array(groups),
        "values": values,
        "ylabel": "Measurement Value",
        "title": "Boxen Style Group Distribution"
    }

def plot(data=None, *, ax=None, x=None, y=None, ylabel=None, title=None, config=None):
    """
    Plots a high-quality letter-value boxen plot.
    """
    # Apply publication style rcParams
    matplotlib.rcParams.update(STYLE_RC)
    
    if data is None:
        data = make_sample_data()
        
    fig = None
    figsize = (config or {}).get("figsize", STYLE_PROFILE["figsize"])
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, dpi=300)
    else:
        fig = ax.figure
        
    # Convert input data to standard long-format DataFrame if it is a dictionary
    if isinstance(data, dict):
        df_list = []
        for grp, vals in zip(data["groups"], data["values"]):
            df_list.append(pd.DataFrame({
                "Group": grp,
                "Value": vals
            }))
        df = pd.concat(df_list, ignore_index=True)
        plot_x, plot_y = "Group", "Value"
        plot_title = title or data.get("title", TITLE)
        plot_ylabel = ylabel or data.get("ylabel", "Value")
    elif isinstance(data, pd.DataFrame):
        df = data
        plot_x = x or df.columns[0]
        plot_y = y or df.columns[1]
        plot_title = title or TITLE
        plot_ylabel = ylabel or plot_y
    else:
        raise TypeError("Data must be either a dict or a pandas DataFrame")

    # Render actual Letter-Value (Boxen) plot using seaborn
    sns.boxenplot(
        data=df,
        x=plot_x,
        y=plot_y,
        ax=ax,
        palette=PALETTE_COLORS,
        linewidth=0.8,
        linecolor="#333333",
        box_kws={"alpha": 0.85, "edgecolor": "white"}
    )
    
    # Strip spines for clean look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    
    # Enable grid lines
    ax.yaxis.grid(True, linestyle="-", color="#f0f0f0", linewidth=0.6, zorder=-10)
    ax.set_axisbelow(True)
    
    # Customize labels and titles
    ax.set_title(plot_title, loc="left", fontweight="bold", pad=12)
    ax.set_xlabel("")
    ax.set_ylabel(plot_ylabel)
    
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
    outputs = render("outputs", basename="boxen_plot_demo")
    print(f"Done! Outputs saved to: {[str(p) for p in outputs]}")
