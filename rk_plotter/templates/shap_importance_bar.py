# TEMPLATE_ID: shap_importance_bar
# TEMPLATE_VERSION: 1.0
# FIGURE_TYPE: ranked_horizontal_importance_bar
# LOCKED_STRUCTURE:
# - horizontal bars sorted in descending order of feature importance
# - features listed vertically on y-axis
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

TEMPLATE_ID = "shap_importance_bar"

FIELD_MAP = {
    "feature": "Feature_Name",
    "importance": "Mean_SHAP_Value",
}

TEXT_CONFIG = {
    "title": "Mean Feature Impact on Model Prediction",
    "x_label": "Mean(|SHAP value|) (average impact magnitude)",
    "y_label": "Features",
}

STYLE_CONFIG = {
    "figsize": (3.8, 3.1),  # Compact square-like wide size is standard
    "font_family": "sans-serif",
    "font_sans": ["Arial", "DejaVu Sans", "Helvetica", "Microsoft YaHei"],
    "font_size": 8.5,
    "bar_color": "#4C78A8",  # Standard calm blue CUD color
    "bar_height": 0.6,
    "axis_linewidth": 0.8,
}

EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "shap_importance_bar",
    "formats": ["svg", "pdf", "png"],
    "dpi": 600,
}

def load_data(path: str | Path) -> pd.DataFrame:
    """Loads feature dataset. Falls back to generating sample dataset."""
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    
    # Generate mock features and SHAP importances
    features = [
        "Temperature (°C)", "pH level", "Salinity (psu)", "Dissolved Oxygen",
        "Chlorophyll-a", "Nitrate (µmol/L)", "Phosphate (µmol/L)", "Silicate (µmol/L)"
    ]
    importance = [0.48, 0.35, 0.22, 0.18, 0.14, 0.09, 0.05, 0.02]
    return pd.DataFrame({
        "Feature_Name": features,
        "Mean_SHAP_Value": importance
    })

def prepare_data(df: pd.DataFrame, field_map: dict) -> pd.DataFrame:
    """Extracts features and importances, and sorts in descending order."""
    feature = df[field_map["feature"]].astype(str)
    importance = pd.to_numeric(df[field_map["importance"]], errors="coerce")
    
    out = pd.DataFrame({"feature": feature, "importance": importance}).dropna()
    # Sort in descending order of feature importance
    out = out.sort_values(by="importance", ascending=True)  # Ascending True for bottom-to-top rendering in barh
    return out

def apply_style(style: dict) -> None:
    """Applies matplotlib styles."""
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
    """Plots ranked horizontal bars representing feature importances."""
    apply_style(style)
    fig, ax = plt.subplots(figsize=style["figsize"], dpi=300)
    
    features = data["feature"].to_numpy()
    importance = data["importance"].to_numpy()
    
    y = np.arange(len(features))
    
    # Render horizontal bars
    ax.barh(
        y,
        importance,
        height=style["bar_height"],
        color=style["bar_color"],
        edgecolor="none",
        zorder=2
    )
    
    ax.grid(True, color="#F0F0F0", linewidth=0.6, zorder=0)
    ax.xaxis.grid(True, linestyle="-", color="#f0f0f0", linewidth=0.6, zorder=-10)
    ax.set_axisbelow(True)
    
    ax.set_yticks(y)
    ax.set_yticklabels(features)
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
