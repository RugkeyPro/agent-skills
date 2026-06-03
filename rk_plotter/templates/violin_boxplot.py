# TEMPLATE_ID: violin_boxplot
# TEMPLATE_VERSION: 1.1
# FIGURE_TYPE: violin_boxplot_distribution_plot
#
# CORE_VISUAL_GRAMMAR:
# - violin density outlines representing distributions per group
# - overlay of a standard narrow box-and-whisker plot inside each violin
#
# COMMON_ADAPTATIONS:
# - add significance asterisks above violins
# - overlay raw jittered scatter points for small sample sizes
# - adjust violin bandwidth or boxplot width
#
# DO_NOT_CHANGE:
# - do not remove the internal boxplot overlay
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

TEMPLATE_ID = "violin_boxplot"

FIELD_MAP = {
    "group": "Treatment",
    "value": "Response",
}

TEXT_CONFIG = {
    "title": "Bio-Response Distribution",
    "x_label": "Study Groups",
    "y_label": "Concentration (µg/L)",
}

STYLE_CONFIG = {
    "figsize": (5.2, 4.5),
    "font_family": "sans-serif",
    "font_sans": ["Arial", "DejaVu Sans", "Helvetica", "Microsoft YaHei"],
    "font_size": 8.5,
    "colors": ["#66CCEE", "#EE6677", "#228833", "#BBBBBB"],
    "violin_alpha": 0.4,
    "box_width": 0.16,
    "axis_linewidth": 0.8,
}

EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "violin_boxplot",
    "formats": ["svg", "pdf", "png"],
    "dpi": 600,
}

def load_data(path: str | Path) -> pd.DataFrame:
    """Loads dataset from CSV. Falls back to generating sample data if missing."""
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    
    # Generate realistic distribution values
    rng = np.random.default_rng(42)
    groups = ["Baseline", "Intervention A", "Intervention B", "Control"]
    df_list = []
    
    df_list.append(pd.DataFrame({"Treatment": "Baseline", "Response": rng.normal(30.0, 5.0, 100)}))
    df_list.append(pd.DataFrame({"Treatment": "Intervention A", "Response": rng.normal(45.0, 8.0, 100)}))
    df_list.append(pd.DataFrame({"Treatment": "Intervention B", "Response": rng.normal(55.0, 10.0, 100)}))
    df_list.append(pd.DataFrame({"Treatment": "Control", "Response": rng.normal(32.0, 4.5, 100)}))
    
    return pd.concat(df_list, ignore_index=True)

def prepare_data(df: pd.DataFrame, field_map: dict) -> pd.DataFrame:
    """Extracts grouping and response variables."""
    group = df[field_map["group"]].astype(str)
    value = pd.to_numeric(df[field_map["value"]], errors="coerce")
    return pd.DataFrame({"group": group, "value": value}).dropna()

def apply_style(style: dict) -> None:
    """Configures scientific typography and grids."""
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
    """Plots group distributions with violin and box overlays."""
    apply_style(style)
    fig, ax = plt.subplots(figsize=style["figsize"], dpi=300)
    
    # 1. Plot Violin distributions
    sns.violinplot(
        data=data,
        x="group",
        y="value",
        ax=ax,
        palette=style["colors"],
        inner=None,          # Hide inner lines to avoid overlay clutter
        linewidth=0.8,
        cut=0                # Bounded at min/max values
    )
    
    # Apply alpha transparency to violin bodies
    for collection in ax.collections:
        collection.set_alpha(style["violin_alpha"])
        collection.set_edgecolor("#555555")
        
    # 2. Overlay clean boxplot
    sns.boxplot(
        data=data,
        x="group",
        y="value",
        ax=ax,
        width=style["box_width"],
        palette=style["colors"],
        showfliers=False,    # Fliers are redundant here
        boxprops=dict(zorder=10, edgecolor="#333333", alpha=0.9),
        whiskerprops=dict(zorder=10, color="#333333", linewidth=1.0),
        capprops=dict(zorder=10, color="#333333", linewidth=1.0),
        medianprops=dict(zorder=11, color="black", linewidth=1.2)
    )
    
    ax.yaxis.grid(True, linestyle="-", color="#f0f0f0", linewidth=0.6, zorder=-10)
    ax.set_axisbelow(True)
    
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
    df = load_data("data.csv")
    data = prepare_data(df, FIELD_MAP)
    fig = plot(data, TEXT_CONFIG, STYLE_CONFIG)
    paths = save_outputs(fig, EXPORT_CONFIG)
    print(f"Generated: {[str(p) for p in paths]}")

if __name__ == "__main__":
    main()
