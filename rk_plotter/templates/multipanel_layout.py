# TEMPLATE_ID: multipanel_layout
# TEMPLATE_VERSION: 1.0
# FIGURE_TYPE: multipanel_layout_gridspec
# LOCKED_STRUCTURE:
# - GridSpec 2x2 grid layout (4 panels)
# - bold panel labels (A, B, C, D) in top-left of each panel
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

TEMPLATE_ID = "multipanel_layout"

# Field map represents variables for multiple sub-panels
FIELD_MAP = {
    "x1": "X_Values",
    "y1": "Y1_Values",
    "y2": "Y2_Values",
    "y3": "Y3_Values",
    "y4": "Y4_Values",
}

TEXT_CONFIG = {
    "title_fig": "Integrated Environmental Parameter Analysis",
    "labels_y": ["Temp (°C)", "pH level", "Salinity (psu)", "Oxygen (mg/L)"],
    "label_x": "Station ID",
}

STYLE_CONFIG = {
    "figsize": (7.2, 5.5),  # Standard double-column layout tall height
    "font_family": "sans-serif",
    "font_sans": ["Arial", "DejaVu Sans", "Helvetica", "Microsoft YaHei"],
    "font_size": 8.5,
    "panel_colors": ["#4477AA", "#EE6677", "#228833", "#CCBB44"],
    "axis_linewidth": 0.8,
}

EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "multipanel_layout",
    "formats": ["svg", "pdf", "png"],
    "dpi": 600,
}

def load_data(path: str | Path) -> pd.DataFrame:
    """Loads source CSV. Falls back to generating sample dataset."""
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    
    # Generate mock parameters across 10 stations
    stations = [f"Stn {i}" for i in range(1, 11)]
    rng = np.random.default_rng(42)
    return pd.DataFrame({
        "X_Values": stations,
        "Y1_Values": rng.normal(20.0, 2.0, 10),
        "Y2_Values": rng.normal(8.1, 0.15, 10),
        "Y3_Values": rng.normal(32.0, 1.5, 10),
        "Y4_Values": rng.normal(6.5, 0.8, 10),
    })

def prepare_data(df: pd.DataFrame, field_map: dict) -> pd.DataFrame:
    """Extracts station IDs and multi-panel parameter columns."""
    x = df[field_map["x1"]].astype(str)
    y1 = pd.to_numeric(df[field_map["y1"]], errors="coerce")
    y2 = pd.to_numeric(df[field_map["y2"]], errors="coerce")
    y3 = pd.to_numeric(df[field_map["y3"]], errors="coerce")
    y4 = pd.to_numeric(df[field_map["y4"]], errors="coerce")
    return pd.DataFrame({"x": x, "y1": y1, "y2": y2, "y3": y3, "y4": y4}).dropna()

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
    """Draws 2x2 multi-panel layout with custom plots and markers."""
    apply_style(style)
    fig, axs = plt.subplots(2, 2, figsize=style["figsize"], dpi=300, sharex=True)
    
    x = data["x"].to_numpy()
    y_cols = ["y1", "y2", "y3", "y4"]
    panel_markers = ["A", "B", "C", "D"]
    
    flat_axs = axs.flatten()
    
    for i, ax in enumerate(flat_axs):
        y = data[y_cols[i]].to_numpy()
        color = style["panel_colors"][i % len(style["panel_colors"])]
        
        # Plot data points as connected lines
        ax.plot(x, y, color=color, linewidth=1.4, marker="o", markersize=4.0, zorder=2)
        
        # Grid layout
        ax.grid(True, color="#F0F0F0", linewidth=0.6, zorder=0)
        ax.set_axisbelow(True)
        
        # Subplot labels and indicators
        ax.set_ylabel(text["labels_y"][i])
        ax.text(-0.15, 1.05, panel_markers[i], transform=ax.transAxes, fontsize=style["font_size"] + 2, fontweight="bold", va="bottom", ha="left")
        
        # Set x label for bottom row panels
        if i >= 2:
            ax.set_xlabel(text["label_x"])
            
    fig.suptitle(text["title_fig"], fontweight="bold", fontsize=style["font_size"] + 2, y=0.98, x=0.08, ha="left")
    fig.tight_layout()
    
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
