# TEMPLATE_ID: multi_scenario_timeseries
# TEMPLATE_VERSION: 1.1
# FIGURE_TYPE: multi_scenario_line_plot
#
# CORE_VISUAL_GRAMMAR:
# - calendar time on x-axis
# - multiple scenario/experimental curves represented by distinct lines
# - compact legend positioned at the top of the canvas
#
# COMMON_ADAPTATIONS:
# - add more scenario lines if user data contains more scenarios
# - add uncertainty ribbons if lower/upper or standard deviation columns exist
# - add event windows (shaded vertical bands with axvspan)
# - add horizontal threshold reference lines
# - add minor inset zoom plots
#
# DO_NOT_CHANGE:
# - do not convert trends to bar charts or radar charts
# - do not reverse chronological order
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

TEMPLATE_ID = "multi_scenario_timeseries"

FIELD_MAP = {
    "x": "Year",
    "series": ["SSP126", "SSP245", "SSP585"],
}

TEXT_CONFIG = {
    "title": "Projected Future Trajectories",
    "x_label": "Year",
    "y_label": "Global Indicator Value",
    "legend_title": "Scenarios",
}

STYLE_CONFIG = {
    "figsize": (7.2, 3.8),
    "font_family": "sans-serif",
    "font_sans": ["Arial", "DejaVu Sans", "Helvetica", "Microsoft YaHei"],
    "font_size": 8.5,
    "line_colors": ["#1B9E77", "#D95F02", "#7570B3"],  # Scenario-friendly color scheme
    "line_width": 1.6,
    "marker_size": 4.0,
    "axis_linewidth": 0.8,
}

EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "multi_scenario_timeseries",
    "formats": ["svg", "pdf", "png"],
    "dpi": 600,
}

def load_data(path: str | Path) -> pd.DataFrame:
    """Loads time series from CSV file. Falls back to generating sample data if missing."""
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    
    # Generate realistic scenario trajectories (2020 to 2100)
    years = np.arange(2020, 2101, 5)
    n = len(years)
    rng = np.random.default_rng(42)
    
    ssp126 = 350.0 + np.cumsum(rng.normal(0.8, 1.5, n)) + 0.1 * (years - 2020)
    ssp245 = 350.0 + np.cumsum(rng.normal(1.5, 2.0, n)) + 0.6 * (years - 2020)
    ssp585 = 350.0 + np.cumsum(rng.normal(2.5, 3.5, n)) + 1.8 * (years - 2020)
    
    return pd.DataFrame({
        "Year": years,
        "SSP126": ssp126,
        "SSP245": ssp245,
        "SSP585": ssp585,
    })

def prepare_data(df: pd.DataFrame, field_map: dict) -> pd.DataFrame:
    """Extracts date/time column and value columns."""
    x = pd.to_numeric(df[field_map["x"]], errors="coerce")
    series_cols = {}
    for col in field_map["series"]:
        series_cols[col] = pd.to_numeric(df[col], errors="coerce")
        
    out = pd.DataFrame({"x": x, **series_cols}).dropna()
    return out

def apply_style(style: dict) -> None:
    """Standardizes font selections and spines configurations."""
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
    """Plots lines with markers for multiple scenarios."""
    apply_style(style)
    fig, ax = plt.subplots(figsize=style["figsize"], dpi=300)
    
    x = data["x"].to_numpy()
    series_names = [col for col in data.columns if col != "x"]
    
    # Render line plots
    for i, name in enumerate(series_names):
        y = data[name].to_numpy()
        color = style["line_colors"][i % len(style["line_colors"])]
        ax.plot(
            x,
            y,
            label=name,
            color=color,
            linewidth=style["line_width"],
            marker="o",
            markersize=style["marker_size"],
            markerfacecolor="white",
            markeredgewidth=1.2,
            zorder=3
        )
        
    ax.grid(True, color="#F0F0F0", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    
    # Custom Labels
    ax.set_title(text["title"], loc="left", fontweight="bold", pad=12)
    ax.set_xlabel(text["x_label"])
    ax.set_ylabel(text["y_label"])
    
    # Legend at the top (ncol = number of lines)
    ax.legend(
        loc="upper left",
        bbox_to_anchor=(0.0, 1.08),
        ncol=len(series_names),
        frameon=False,
        title=text.get("legend_title")
    )
    
    return fig

def save_outputs(fig: plt.Figure, export: dict) -> list[Path]:
    """Exports figure outputs."""
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
