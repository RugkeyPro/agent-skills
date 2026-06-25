# TEMPLATE_ID: boxen_plot
# TEMPLATE_VERSION: 1.1
# FIGURE_TYPE: boxen_distribution_plot
#
# CORE_VISUAL_GRAMMAR:
# - group categories on x-axis, continuous values on y-axis
# - letter-value boxen representation showing distributions
#
# COMMON_ADAPTATIONS:
# - overlay individual scatter/jitter points to show sample sizes
# - add statistical significance brackets/markers between groups (e.g. *, **)
# - add horizontal mean or baseline guidelines
#
# DO_NOT_CHANGE:
# - do not convert to boxplots or violin plots without permission
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
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
import sys

TEMPLATE_ID = "boxen_plot"

FIELD_MAP = {
    "group": "Treatment",
    "value": "Response",
}

TEXT_CONFIG = {
    "title": "Response Distribution Across Treatments",
    "x_label": "Treatments",
    "y_label": "Response Rate (%)",
}

STYLE_CONFIG = {
    "figsize": (4.2, 5.8),  # Tall format is standard for group comparisons
    "font_family": "sans-serif",
    "font_sans": ["Arial", "DejaVu Sans", "Helvetica", "Microsoft YaHei"],
    "font_size": 8.5,
    "bar_colors": ["#4477AA", "#EE6677", "#228833", "#CCBB44"],  # CUD palette
    "box_alpha": 0.85,
    "axis_linewidth": 0.8,
}

EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "boxen_plot",
    "formats": ["svg", "pdf", "png"],
    "dpi": 600,
}

def load_data(path: str | Path) -> pd.DataFrame:
    """Loads dataset from CSV. Falls back to generating sample data if missing."""
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    
    # Generate realistic response distributions across groups
    rng = np.random.default_rng(42)
    groups = ["Control", "Low Dose", "Medium Dose", "High Dose"]
    df_list = []
    
    # Generate different distributions (normal, lognormal, exponential)
    df_list.append(pd.DataFrame({"Treatment": "Control", "Response": rng.normal(45.0, 8.0, 150)}))
    df_list.append(pd.DataFrame({"Treatment": "Low Dose", "Response": rng.normal(55.0, 12.0, 150)}))
    df_list.append(pd.DataFrame({"Treatment": "Medium Dose", "Response": rng.lognormal(4.1, 0.15, 150)}))
    df_list.append(pd.DataFrame({"Treatment": "High Dose", "Response": rng.exponential(15.0, 150) + 50.0}))
    
    return pd.concat(df_list, ignore_index=True)

def prepare_data(df: pd.DataFrame, field_map: dict) -> pd.DataFrame:
    """Extracts grouping and measurement columns."""
    group = df[field_map["group"]].astype(str)
    value = pd.to_numeric(df[field_map["value"]], errors="coerce")
    return pd.DataFrame({"group": group, "value": value}).dropna()

def apply_style(style: dict) -> None:
    """Applies matplotlib settings."""
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
    """Plots group distribution using Seaborn boxenplot."""
    apply_style(style)
    fig, ax = plt.subplots(figsize=style["figsize"], dpi=300)
    
    # Render boxenplot
    sns.boxenplot(
        data=data,
        x="group",
        y="value",
        ax=ax,
        palette=style["bar_colors"],
        linewidth=0.8,
        linecolor="#333333",
        box_kws={"alpha": style["box_alpha"], "edgecolor": "white"}
    )
    
    # Fine grid lines and axes tweaks
    ax.yaxis.grid(True, linestyle="-", color="#f0f0f0", linewidth=0.6, zorder=-10)
    ax.set_axisbelow(True)
    
    # Titles and labels
    ax.set_title(text["title"], loc="left", fontweight="bold", pad=12)
    ax.set_xlabel(text["x_label"])
    ax.set_ylabel(text["y_label"])
    
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
