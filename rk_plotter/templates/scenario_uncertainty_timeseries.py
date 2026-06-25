# TEMPLATE_ID: scenario_uncertainty_timeseries
# TEMPLATE_VERSION: 1.1
# FIGURE_TYPE: scenario_uncertainty_timeseries_plot
#
# CORE_VISUAL_GRAMMAR:
# - continuous trend line representing mean/median over time
# - semi-transparent shaded envelope representing uncertainty (standard deviation, min-max, or IQR)
#
# COMMON_ADAPTATIONS:
# - add multiple trend lines with corresponding shaded envelopes
# - add vertical event bands or horizontal thresholds
# - customize alpha transparency of shaded region
#
# DO_NOT_CHANGE:
# - do not remove the shaded uncertainty ribbon
# - do not convert to bar charts
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

TEMPLATE_ID = "scenario_uncertainty_timeseries"

FIELD_MAP = {
    "x": "Year",
    "y": "Mean",
    "lower": "Lower_CI",
    "upper": "Upper_CI",
}

TEXT_CONFIG = {
    "title": "Historical and Projected Growth with 95% CI",
    "x_label": "Year",
    "y_label": "Measurement Value",
    "legend_label": "Mean projection",
    "fill_label": "95% confidence interval",
}

STYLE_CONFIG = {
    "figsize": (7.0, 3.8),
    "font_family": "sans-serif",
    "font_sans": ["Arial", "DejaVu Sans", "Helvetica", "Microsoft YaHei"],
    "font_size": 8.5,
    "line_color": "#228833",
    "fill_color": "#228833",
    "fill_alpha": 0.15,
    "line_width": 1.8,
    "axis_linewidth": 0.8,
}

EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "scenario_uncertainty_timeseries",
    "formats": ["svg", "pdf", "png"],
    "dpi": 600,
}

def load_data(path: str | Path) -> pd.DataFrame:
    """Loads time series dataset. Falls back to generating sample dataset."""
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    
    # Generate realistic values with expanding uncertainty
    years = np.arange(2000, 2051)
    n = len(years)
    rng = np.random.default_rng(42)
    
    base = 12.0 + 0.35 * (years - 2000)
    fluctuations = rng.normal(0, 0.4, n)
    mean_val = base + fluctuations
    
    # Uncertainty expands in future years
    std_dev = 0.5 + 0.08 * (years - 2000)
    lower_val = mean_val - 1.96 * std_dev
    upper_val = mean_val + 1.96 * std_dev
    
    return pd.DataFrame({
        "Year": years,
        "Mean": mean_val,
        "Lower_CI": lower_val,
        "Upper_CI": upper_val,
    })

def prepare_data(df: pd.DataFrame, field_map: dict) -> pd.DataFrame:
    """Extracts column headers and handles NaNs."""
    x = pd.to_numeric(df[field_map["x"]], errors="coerce")
    y = pd.to_numeric(df[field_map["y"]], errors="coerce")
    lower = pd.to_numeric(df[field_map["lower"]], errors="coerce")
    upper = pd.to_numeric(df[field_map["upper"]], errors="coerce")
    return pd.DataFrame({"x": x, "y": y, "lower": lower, "upper": upper}).dropna()

def apply_style(style: dict) -> None:
    """Sets standard matplotlib typography and lines."""
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
    """Plots central line and translucent fill envelope."""
    apply_style(style)
    fig, ax = plt.subplots(figsize=style["figsize"], dpi=300)
    
    x = data["x"].to_numpy()
    y = data["y"].to_numpy()
    lower = data["lower"].to_numpy()
    upper = data["upper"].to_numpy()
    
    # Shaded uncertainty band
    ax.fill_between(
        x,
        lower,
        upper,
        color=style["fill_color"],
        alpha=style["fill_alpha"],
        label=text["fill_label"],
        zorder=1
    )
    
    # Central trend line
    ax.plot(
        x,
        y,
        color=style["line_color"],
        linewidth=style["line_width"],
        label=text["legend_label"],
        zorder=2
    )
    
    ax.grid(True, color="#F0F0F0", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    
    ax.set_title(text["title"], loc="left", fontweight="bold")
    ax.set_xlabel(text["x_label"])
    ax.set_ylabel(text["y_label"])
    ax.legend(frameon=False, loc="upper left")
    
    return fig

def save_outputs(fig: plt.Figure, export: dict) -> list[Path]:
    """Exports files to output formats."""
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
