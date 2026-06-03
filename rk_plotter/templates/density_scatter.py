# TEMPLATE_ID: density_scatter
# TEMPLATE_VERSION: 1.1
# FIGURE_TYPE: density_colored_scatter
#
# CORE_VISUAL_GRAMMAR:
# - scatter plot colored by local Gaussian KDE density
# - uses Seaborn 'mako' colormap by default
# - vertical colorbar on the right side
#
# COMMON_ADAPTATIONS:
# - add horizontal/vertical threshold lines
# - add target guidelines or regression lines
# - add local inset zoom plot for dense region
# - change colormap to match specific journal theme
#
# DO_NOT_CHANGE:
# - do not convert to 2D heatmap or contour plot
# - do not remove colorbar
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
import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import gaussian_kde
import seaborn as sns

TEMPLATE_ID = "density_scatter"

FIELD_MAP = {
    "x": "X_Values",
    "y": "Y_Values",
}

TEXT_CONFIG = {
    "title": "Density-Colored Scatter Plot",
    "x_label": "X variable",
    "y_label": "Y variable",
}

STYLE_CONFIG = {
    "figsize": (4.2, 3.3),
    "font_family": "sans-serif",
    "font_sans": ["Arial", "DejaVu Sans", "Helvetica", "Microsoft YaHei"],
    "font_size": 8.5,
    "cmap": "mako",  # Seaborn mako is standard for high-density plots
    "point_size": 10,
    "axis_linewidth": 0.8,
}

EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "density_scatter",
    "formats": ["svg", "pdf", "png"],
    "dpi": 600,
}

def load_data(path: str | Path) -> pd.DataFrame:
    """Loads dataset from CSV file. Falls back to generating sample data if missing."""
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    
    # Generate realistic sample data (high density normal distribution)
    rng = np.random.default_rng(42)
    mean = [2.0, 2.5]
    cov = [[1.2, 0.8], [0.8, 1.5]]
    x, y = rng.multivariate_normal(mean, cov, 1000).T
    # Add some exponential noise to introduce asymmetry
    x += rng.exponential(0.4, 1000)
    y += rng.exponential(0.4, 1000)
    return pd.DataFrame({
        "X_Values": x,
        "Y_Values": y
    })

def prepare_data(df: pd.DataFrame, field_map: dict) -> pd.DataFrame:
    """Extracts columns and cleans NaNs."""
    x = pd.to_numeric(df[field_map["x"]], errors="coerce")
    y = pd.to_numeric(df[field_map["y"]], errors="coerce")
    return pd.DataFrame({"x": x, "y": y}).dropna()

def apply_style(style: dict) -> None:
    """Applies clean matplotlib typography settings."""
    plt.rcParams.update({
        "font.family": style["font_family"],
        "font.sans-serif": style["font_sans"],
        "font.size": style["font_size"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": style["axis_linewidth"]
    })

def plot(data: pd.DataFrame, text: dict, style: dict) -> plt.Figure:
    """Plots scatter points colored by density calculation."""
    apply_style(style)
    fig, ax = plt.subplots(figsize=style["figsize"], dpi=300)
    
    x = data["x"].to_numpy()
    y = data["y"].to_numpy()
    
    # Calculate local density using kernel density estimation
    xy = np.vstack([x, y])
    kde = gaussian_kde(xy)
    density = kde(xy)
    
    # Sort points by density so high-density points plot on top
    sort_idx = density.argsort()
    x, y, density = x[sort_idx], y[sort_idx], density[sort_idx]
    
    # Plot scatter
    scatter = ax.scatter(
        x,
        y,
        c=density,
        s=style["point_size"],
        cmap=style["cmap"],
        edgecolors="none",
        alpha=0.85,
        zorder=2
    )
    
    # Customize grid and spines
    ax.grid(True, color="#F0F0F0", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    
    # Add titles and labels
    ax.set_title(text["title"], loc="left", fontweight="bold")
    ax.set_xlabel(text["x_label"])
    ax.set_ylabel(text["y_label"])
    
    # Standard colorbar right layout
    cbar = fig.colorbar(scatter, ax=ax, fraction=0.035, pad=0.04)
    cbar.set_label("Relative Density", fontsize=style["font_size"] - 1)
    cbar.ax.tick_params(labelsize=style["font_size"] - 2)
    cbar.outline.set_visible(False)
    
    return fig

def save_outputs(fig: plt.Figure, export: dict) -> list[Path]:
    """Saves figure in high-res formats."""
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
