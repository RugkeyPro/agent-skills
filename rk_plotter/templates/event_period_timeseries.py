# TEMPLATE_ID: event_period_timeseries
# TEMPLATE_VERSION: 1.1
# FIGURE_TYPE: event_period_timeseries_plot
#
# CORE_VISUAL_GRAMMAR:
# - continuous line plot displaying time series data
# - vertical highlighted shaded window (axvspan) marking a specific event period
#
# COMMON_ADAPTATIONS:
# - add multiple event windows with different colors
# - add multiple line series for comparison
# - add annotations pointing to specific event dates
#
# DO_NOT_CHANGE:
# - do not remove the vertical event highlight window
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

TEMPLATE_ID = "event_period_timeseries"

FIELD_MAP = {
    "x": "Year",
    "y": "Value",
}

TEXT_CONFIG = {
    "title": "Carbon Emission Trajectory and Policy Intervention",
    "x_label": "Year",
    "y_label": "Emission Index (tonnes/capita)",
    "legend_label": "Emissions Index",
    "event_label": "Policy Implementation Phase",
}

STYLE_CONFIG = {
    "figsize": (7.2, 3.8),
    "font_family": "sans-serif",
    "font_sans": ["Arial", "DejaVu Sans", "Helvetica", "Microsoft YaHei"],
    "font_size": 8.5,
    "line_color": "#228833",
    "event_range": (2025, 2035),  # Years to highlight
    "event_color": "#EE6677",
    "event_alpha": 0.12,
    "line_width": 1.8,
    "axis_linewidth": 0.8,
}

EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "event_period_timeseries",
    "formats": ["svg", "pdf", "png"],
    "dpi": 600,
}

def load_data(path: str | Path) -> pd.DataFrame:
    """Loads time series CSV. Falls back to generating sample data if missing."""
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    
    # Generate realistic historical trajectory with policy drop
    years = np.arange(2010, 2046)
    n = len(years)
    rng = np.random.default_rng(42)
    
    values = []
    current_val = 8.5
    for year in years:
        if year < 2025:
            # Steady growth phase
            current_val += rng.uniform(0.05, 0.25)
        elif 2025 <= year <= 2035:
            # Sharp drop during policy phase
            current_val -= rng.uniform(0.15, 0.45)
        else:
            # Post-policy stabilization
            current_val += rng.uniform(-0.08, 0.08)
        values.append(current_val)
        
    return pd.DataFrame({
        "Year": years,
        "Value": values
    })

def prepare_data(df: pd.DataFrame, field_map: dict) -> pd.DataFrame:
    """Standardizes columns and drops null entries."""
    x = pd.to_numeric(df[field_map["x"]], errors="coerce")
    y = pd.to_numeric(df[field_map["y"]], errors="coerce")
    return pd.DataFrame({"x": x, "y": y}).dropna()

def apply_style(style: dict) -> None:
    """Applies clean scientific spines and fonts."""
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
    """Plots data lines and overlays vertical span segment."""
    apply_style(style)
    fig, ax = plt.subplots(figsize=style["figsize"], dpi=300)
    
    x = data["x"].to_numpy()
    y = data["y"].to_numpy()
    
    # Plot central trajectory line
    ax.plot(
        x,
        y,
        color=style["line_color"],
        linewidth=style["line_width"],
        label=text["legend_label"],
        zorder=3
    )
    
    # Highlight event period window (axvspan)
    start_y, end_y = style["event_range"]
    ax.axvspan(
        start_y,
        end_y,
        color=style["event_color"],
        alpha=style["event_alpha"],
        label=text["event_label"],
        zorder=1
    )
    
    # Add subtle vertical boundary lines
    ax.axvline(start_y, color=style["event_color"], linestyle=":", linewidth=0.8, alpha=0.5, zorder=2)
    ax.axvline(end_y, color=style["event_color"], linestyle=":", linewidth=0.8, alpha=0.5, zorder=2)
    
    ax.grid(True, color="#F0F0F0", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    
    ax.set_title(text["title"], loc="left", fontweight="bold")
    ax.set_xlabel(text["x_label"])
    ax.set_ylabel(text["y_label"])
    ax.legend(frameon=False, loc="upper right")
    
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
