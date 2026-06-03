# TEMPLATE_ID: dual_panel_scatter_fit
# TEMPLATE_VERSION: 1.0
# FIGURE_TYPE: multi_panel_regression_scatter
# LOCKED_STRUCTURE:
# - dual side-by-side panels (1 row, 2 columns)
# - panel label indicators (A, B) in top-left
# - linear regression dashed fit on both panels
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

TEMPLATE_ID = "dual_panel_scatter_fit"

FIELD_MAP = {
    "x1": "X1_Values",
    "y1": "Y1_Values",
    "x2": "X2_Values",
    "y2": "Y2_Values",
}

TEXT_CONFIG = {
    "title_left": "Dataset Alpha Relationship",
    "title_right": "Dataset Beta Relationship",
    "x_label_left": "Variable X1 (units)",
    "y_label_left": "Variable Y1 (units)",
    "x_label_right": "Variable X2 (units)",
    "y_label_right": "Variable Y2 (units)",
}

STYLE_CONFIG = {
    "figsize": (7.2, 3.4),  # Standard double-column layout size
    "font_family": "sans-serif",
    "font_sans": ["Arial", "DejaVu Sans", "Helvetica", "Microsoft YaHei"],
    "font_size": 8.5,
    "point_color_left": "#4477AA",
    "point_color_right": "#EE6677",
    "fit_color": "#333333",
    "point_size": 15,
    "axis_linewidth": 0.8,
}

EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "dual_panel_scatter_fit",
    "formats": ["svg", "pdf", "png"],
    "dpi": 600,
}

def load_data(path: str | Path) -> pd.DataFrame:
    """Loads source dataset from CSV. Falls back to generating sample data if missing."""
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    
    # Generate realistic sample data for two datasets
    rng = np.random.default_rng(42)
    x1 = rng.uniform(5, 50, 100)
    y1 = 1.35 * x1 + 10.0 + rng.normal(0, 8.0, 100)
    
    x2 = rng.uniform(5, 50, 100)
    y2 = 0.85 * x2 + 25.0 + rng.normal(0, 6.0, 100)
    
    return pd.DataFrame({
        "X1_Values": x1,
        "Y1_Values": y1,
        "X2_Values": x2,
        "Y2_Values": y2,
    })

def prepare_data(df: pd.DataFrame, field_map: dict) -> dict[str, pd.DataFrame]:
    """Cleans columns and structures variables into left/right dataframes."""
    df_left = pd.DataFrame({
        "x": pd.to_numeric(df[field_map["x1"]], errors="coerce"),
        "y": pd.to_numeric(df[field_map["y1"]], errors="coerce")
    }).dropna()
    
    df_right = pd.DataFrame({
        "x": pd.to_numeric(df[field_map["x2"]], errors="coerce"),
        "y": pd.to_numeric(df[field_map["y2"]], errors="coerce")
    }).dropna()
    
    return {"left": df_left, "right": df_right}

def apply_style(style: dict) -> None:
    """Applies matplotlib rendering properties."""
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

def plot(data: dict[str, pd.DataFrame], text: dict, style: dict) -> plt.Figure:
    """Plots side-by-side scatter plots with fit overlays."""
    apply_style(style)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=style["figsize"], dpi=300)
    
    # 1. Left Panel (Panel A)
    dl = data["left"]
    xl, yl = dl["x"].to_numpy(), dl["y"].to_numpy()
    ax1.scatter(xl, yl, s=style["point_size"], color=style["point_color_left"], alpha=0.7, edgecolors="none", zorder=2)
    
    # Fit Left
    slope_l, intercept_l = np.polyfit(xl, yl, 1)
    fit_xl = np.array([xl.min(), xl.max()])
    fit_yl = slope_l * fit_xl + intercept_l
    ax1.plot(fit_xl, fit_yl, color=style["fit_color"], linestyle="--", linewidth=1.1, zorder=3)
    
    ax1.grid(True, color="#F0F0F0", linewidth=0.6, zorder=0)
    ax1.set_axisbelow(True)
    ax1.set_title(text["title_left"], loc="left", fontweight="bold")
    ax1.set_xlabel(text["x_label_left"])
    ax1.set_ylabel(text["y_label_left"])
    ax1.text(-0.15, 1.05, "A", transform=ax1.transAxes, fontsize=style["font_size"] + 2, fontweight="bold", va="bottom", ha="left")
    
    # 2. Right Panel (Panel B)
    dr = data["right"]
    xr, yr = dr["x"].to_numpy(), dr["y"].to_numpy()
    ax2.scatter(xr, yr, s=style["point_size"], color=style["point_color_right"], alpha=0.7, edgecolors="none", zorder=2)
    
    # Fit Right
    slope_r, intercept_r = np.polyfit(xr, yr, 1)
    fit_xr = np.array([xr.min(), xr.max()])
    fit_yr = slope_r * fit_xr + intercept_r
    ax2.plot(fit_xr, fit_yr, color=style["fit_color"], linestyle="--", linewidth=1.1, zorder=3)
    
    ax2.grid(True, color="#F0F0F0", linewidth=0.6, zorder=0)
    ax2.set_axisbelow(True)
    ax2.set_title(text["title_right"], loc="left", fontweight="bold")
    ax2.set_xlabel(text["x_label_right"])
    ax2.set_ylabel(text["y_label_right"])
    ax2.text(-0.15, 1.05, "B", transform=ax2.transAxes, fontsize=style["font_size"] + 2, fontweight="bold", va="bottom", ha="left")
    
    # Align y limits for visual comparison
    ymin = min(ax1.get_ylim()[0], ax2.get_ylim()[0])
    ymax = max(ax1.get_ylim()[1], ax2.get_ylim()[1])
    ax1.set_ylim(ymin, ymax)
    ax2.set_ylim(ymin, ymax)
    
    fig.tight_layout()
    return fig

def save_outputs(fig: plt.Figure, export: dict) -> list[Path]:
    """Saves final figure files."""
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
