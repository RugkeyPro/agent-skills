# TEMPLATE_ID: stacked_percent_bar
# TEMPLATE_VERSION: 1.0
# FIGURE_TYPE: vertical_stacked_percent_bar
# LOCKED_STRUCTURE:
# - vertical bars representing groups
# - y-axis scaled explicitly from 0 to 100%
# - component values stacked to sum to 100%
# - legend positioned on top
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

TEMPLATE_ID = "stacked_percent_bar"

FIELD_MAP = {
    "group": "Group",
    "components": ["Component_A", "Component_B", "Component_C"],
}

TEXT_CONFIG = {
    "title": "Composition Share Across Treatments",
    "x_label": "Treatment Groups",
    "y_label": "Relative Abundance (%)",
    "legend_title": "Fractions",
}

STYLE_CONFIG = {
    "figsize": (6.2, 4.8),
    "font_family": "sans-serif",
    "font_sans": ["Arial", "DejaVu Sans", "Helvetica", "Microsoft YaHei"],
    "font_size": 8.5,
    "bar_colors": ["#4477AA", "#CCBB44", "#EE6677"],  # High contrast CUD colors
    "bar_width": 0.55,
    "axis_linewidth": 0.8,
}

EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "stacked_percent_bar",
    "formats": ["svg", "pdf", "png"],
    "dpi": 600,
}

def load_data(path: str | Path) -> pd.DataFrame:
    """Loads dataset from CSV. Falls back to generating sample data if missing."""
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    
    # Generate realistic composition splits
    groups = ["Control", "Treatment Low", "Treatment Mid", "Treatment High"]
    a_vals = [45.0, 32.0, 20.0, 10.0]
    b_vals = [35.0, 48.0, 50.0, 40.0]
    c_vals = [20.0, 20.0, 30.0, 50.0]
    
    return pd.DataFrame({
        "Group": groups,
        "Component_A": a_vals,
        "Component_B": b_vals,
        "Component_C": c_vals,
    })

def prepare_data(df: pd.DataFrame, field_map: dict) -> pd.DataFrame:
    """Standardizes composition fractions to sum to exactly 100%."""
    group_col = df[field_map["group"]].astype(str)
    comp_dfs = []
    for col in field_map["components"]:
        comp_dfs.append(pd.to_numeric(df[col], errors="coerce"))
        
    comp_df = pd.concat(comp_dfs, axis=1)
    # Row normalization to sum up to 100
    row_sums = comp_df.sum(axis=1)
    normalized = comp_df.div(row_sums, axis=0) * 100.0
    
    out = pd.concat([group_col, normalized], axis=1).dropna()
    return out

def apply_style(style: dict) -> None:
    """Applies matplotlib publication style parameters."""
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
    """Plots vertical 100% stacked bar chart."""
    apply_style(style)
    fig, ax = plt.subplots(figsize=style["figsize"], dpi=300)
    
    groups = data.iloc[:, 0].to_numpy()
    components = data.columns[1:]
    values = data.iloc[:, 1:].to_numpy()
    
    # Initialize bottoms accumulation array
    bottom = np.zeros(len(groups))
    
    for i, comp_name in enumerate(components):
        vals = values[:, i]
        ax.bar(
            groups,
            vals,
            bottom=bottom,
            width=style["bar_width"],
            color=style["bar_colors"][i % len(style["bar_colors"])],
            label=comp_name,
            edgecolor="white",
            linewidth=0.5,
            zorder=2
        )
        bottom += vals
        
    ax.grid(True, color="#F0F0F0", linewidth=0.6, zorder=0)
    ax.yaxis.grid(True, linestyle="-", color="#f0f0f0", linewidth=0.6, zorder=-10)
    ax.set_axisbelow(True)
    
    # Custom labels and limit bounds
    ax.set_ylim(0, 100)
    ax.set_title(text["title"], loc="left", fontweight="bold", pad=14)
    ax.set_xlabel(text["x_label"])
    ax.set_ylabel(text["y_label"])
    
    # Legend at the top (ncol = number of columns)
    ax.legend(
        loc="upper left",
        bbox_to_anchor=(0.0, 1.08),
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
        path = output_dir / f"{export["basename"]}.{fmt}"
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
