# TEMPLATE_ID: heatmap_2d
# TEMPLATE_VERSION: 1.1
# FIGURE_TYPE: heatmap_matrix_plot
#
# CORE_VISUAL_GRAMMAR:
# - 2D grid matrix colored by cell values
# - numerical cell values annotated inside each cell
# - vertical colorbar on the right side
#
# COMMON_ADAPTATIONS:
# - add statistical significance markers (e.g., *, **) next to cell numbers
# - overlay contour lines to represent response surfaces
# - change color maps (e.g., diverging vs. sequential)
#
# DO_NOT_CHANGE:
# - do not convert to 3D surface plot
# - do not remove colorbar or annotations
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
import sys

TEMPLATE_ID = "heatmap_2d"

FIELD_MAP = {
    "x_group": "Variable_X",
    "y_group": "Variable_Y",
    "value": "Correlation",
}

TEXT_CONFIG = {
    "title": "Parameter Correlation Matrix",
    "colorbar_label": "Pearson Correlation Coefficient (r)",
}

STYLE_CONFIG = {
    "figsize": (5.0, 4.2),
    "font_family": "sans-serif",
    "font_sans": ["Arial", "DejaVu Sans", "Helvetica", "Microsoft YaHei"],
    "font_size": 8.5,
    "cmap": "RdBu_r",  # Standard diverging palette for positive/negative values
    "text_colors": ("black", "white"),  # Contrast colors for annotations
    "text_threshold": 0.65,             # Absolute value threshold for changing text color
    "axis_linewidth": 0.8,
}

EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "heatmap_2d",
    "formats": ["svg", "pdf", "png"],
    "dpi": 600,
}

def load_data(path: str | Path) -> pd.DataFrame:
    """Loads dataset from CSV file. Falls back to generating sample data if missing."""
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    
    # Generate pairwise correlation structure for 5 parameters
    params = ["Temp", "pH", "Salinity", "DO", "Chl-a"]
    n = len(params)
    data = []
    
    # Realistic mock correlation coefficients (symmetric with 1.0 on diagonal)
    matrix = [
        [1.00, -0.42, 0.65, -0.78, 0.52],
        [-0.42, 1.00, -0.15, 0.35, -0.28],
        [0.65, -0.15, 1.00, -0.58, 0.73],
        [-0.78, 0.35, -0.58, 1.00, -0.62],
        [0.52, -0.28, 0.73, -0.62, 1.00]
    ]
    
    for i in range(n):
        for j in range(n):
            data.append({
                "Variable_X": params[i],
                "Variable_Y": params[j],
                "Correlation": matrix[i][j]
            })
            
    return pd.DataFrame(data)

def prepare_data(df: pd.DataFrame, field_map: dict) -> pd.DataFrame:
    """Pivots 3-column long dataframe into a 2D matrix structure."""
    x = df[field_map["x_group"]].astype(str)
    y = df[field_map["y_group"]].astype(str)
    val = pd.to_numeric(df[field_map["value"]], errors="coerce")
    
    pivoted_df = pd.DataFrame({"x": x, "y": y, "value": val}).pivot(index="y", columns="x", values="value")
    return pivoted_df

def apply_style(style: dict) -> None:
    """Configures scientific styles."""
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
    """Plots 2D annotated heatmap grid."""
    apply_style(style)
    fig, ax = plt.subplots(figsize=style["figsize"], dpi=300)
    
    x_labels = data.columns.values
    y_labels = data.index.values
    matrix_vals = data.to_numpy()
    
    # Render heatmap image
    im = ax.imshow(
        matrix_vals,
        cmap=style["cmap"],
        aspect="auto",
        vmin=-1.0,  # Bounded for correlation coefficients
        vmax=1.0,
        origin="upper"
    )
    
    # Overlay cell annotations
    for i in range(len(y_labels)):
        for j in range(len(x_labels)):
            val = matrix_vals[i, j]
            # Select contrasting text color based on cell background intensity
            text_color = style["text_colors"][1] if abs(val) > style["text_threshold"] else style["text_colors"][0]
            ax.text(
                j,
                i,
                f"{val:.2f}",
                ha="center",
                va="center",
                color=text_color,
                fontsize=style["font_size"] - 1,
                fontweight="semibold"
            )
            
    # Configure axes tick ticks and limits
    ax.set_xticks(np.arange(len(x_labels)))
    ax.set_yticks(np.arange(len(y_labels)))
    ax.set_xticklabels(x_labels)
    ax.set_yticklabels(y_labels)
    
    # Hide axis spines for cleanliness
    for spine in ax.spines.values():
        spine.set_visible(False)
        
    ax.tick_params(top=False, bottom=False, left=False, right=False)
    ax.set_title(text["title"], loc="left", fontweight="bold", pad=14)
    
    # Add vertical colorbar track
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
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
    path = sys.argv[1] if len(sys.argv) > 1 else "data.csv"
    if not Path(path).exists():
        print(f"WARNING: '{path}' not found; rendering synthetic preview data (NOT real data).", file=sys.stderr)
    df = load_data(path)
    data = prepare_data(df, FIELD_MAP)
    fig = plot(data, TEXT_CONFIG, STYLE_CONFIG)
    paths = save_outputs(fig, EXPORT_CONFIG)
    print(f"Generated: {[str(p) for p in paths]}")

if __name__ == "__main__":
    main()
