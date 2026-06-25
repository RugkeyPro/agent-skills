# TEMPLATE_ID: horizontal_stacked_bar
# TEMPLATE_VERSION: 1.1
# FIGURE_TYPE: horizontal_stacked_bar_chart
#
# CORE_VISUAL_GRAMMAR:
# - horizontal 100% stacked bar chart (great for long categorical labels)
# - component segments sum up to 100%
#
# COMMON_ADAPTATIONS:
# - add extra categorical groups or component columns
# - sort bars in ascending/descending order of a specific component
# - add vertical threshold/reference lines
#
# DO_NOT_CHANGE:
# - do not convert to vertical bars unless requested
# - do not remove category labels on the y-axis
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

TEMPLATE_ID = "horizontal_stacked_bar"

FIELD_MAP = {
    "group": "Category",
    "components": ["Sector_Commercial", "Sector_Industrial", "Sector_Residential"],
}

TEXT_CONFIG = {
    "title": "Energy Consumption Share by Region",
    "x_label": "Share of Consumption (%)",
    "y_label": "Regions",
    "legend_title": "Sectors",
}

STYLE_CONFIG = {
    "figsize": (6.4, 3.2),
    "font_family": "sans-serif",
    "font_sans": ["Arial", "DejaVu Sans", "Helvetica", "Microsoft YaHei"],
    "font_size": 8.5,
    "bar_colors": ["#66CCEE", "#AA3377", "#BBBBBB"],
    "bar_height": 0.55,
    "axis_linewidth": 0.8,
}

EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "horizontal_stacked_bar",
    "formats": ["svg", "pdf", "png"],
    "dpi": 600,
}

def load_data(path: str | Path) -> pd.DataFrame:
    """Loads source CSV. Falls back to generating sample data if missing."""
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    
    # Generate realistic composition splits
    categories = [
        "East Asia & Pacific Region",
        "Europe & Central Asia Region",
        "Latin America & Caribbean",
        "Middle East & North Africa",
        "North America Region",
        "Sub-Saharan Africa Region"
    ]
    commercial = [20.0, 25.0, 30.0, 15.0, 35.0, 10.0]
    industrial = [55.0, 45.0, 35.0, 60.0, 40.0, 30.0]
    residential = [25.0, 30.0, 35.0, 25.0, 25.0, 60.0]
    
    return pd.DataFrame({
        "Category": categories,
        "Sector_Commercial": commercial,
        "Sector_Industrial": industrial,
        "Sector_Residential": residential,
    })

def prepare_data(df: pd.DataFrame, field_map: dict) -> pd.DataFrame:
    """Standardizes composition fractions to sum to exactly 100%."""
    group_col = df[field_map["group"]].astype(str)
    comp_dfs = []
    for col in field_map["components"]:
        comp_dfs.append(pd.to_numeric(df[col], errors="coerce"))
        
    comp_df = pd.concat(comp_dfs, axis=1)
    row_sums = comp_df.sum(axis=1)
    normalized = comp_df.div(row_sums, axis=0) * 100.0
    
    out = pd.concat([group_col, normalized], axis=1).dropna()
    return out

def apply_style(style: dict) -> None:
    """Applies clean spines and fonts."""
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
    """Plots horizontal 100% stacked bar chart."""
    apply_style(style)
    fig, ax = plt.subplots(figsize=style["figsize"], dpi=300)
    
    groups = data.iloc[:, 0].to_numpy()
    components = data.columns[1:]
    values = data.iloc[:, 1:].to_numpy()
    
    y = np.arange(len(groups))
    
    # Initialize lefts accumulation array
    left = np.zeros(len(groups))
    
    for i, comp_name in enumerate(components):
        vals = values[:, i]
        ax.barh(
            y,
            vals,
            left=left,
            height=style["bar_height"],
            color=style["bar_colors"][i % len(style["bar_colors"])],
            label=comp_name,
            edgecolor="white",
            linewidth=0.5,
            zorder=2
        )
        left += vals
        
    ax.grid(True, color="#F0F0F0", linewidth=0.6, zorder=0)
    ax.xaxis.grid(True, linestyle="-", color="#f0f0f0", linewidth=0.6, zorder=-10)
    ax.set_axisbelow(True)
    
    # Custom labels and limit bounds
    ax.set_xlim(0, 100)
    ax.set_yticks(y)
    ax.set_yticklabels(groups)
    ax.set_title(text["title"], loc="left", fontweight="bold", pad=14)
    ax.set_xlabel(text["x_label"])
    ax.set_ylabel(text["y_label"])
    
    # Legend at the top (ncol = number of columns)
    ax.legend(
        loc="upper left",
        bbox_to_anchor=(0.0, 1.12),
        ncol=len(components),
        frameon=False,
        title=text.get("legend_title")
    )
    
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
