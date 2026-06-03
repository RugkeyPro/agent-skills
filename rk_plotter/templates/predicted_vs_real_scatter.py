# TEMPLATE_ID: predicted_vs_real_scatter
# TEMPLATE_VERSION: 1.0
# FIGURE_TYPE: prediction_diagnostic_scatter
# LOCKED_STRUCTURE:
# - single square scatter panel
# - observed on x-axis
# - predicted on y-axis
# - 1:1 reference line
# - fitted regression line
# - metric textbox
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

TEMPLATE_ID = "predicted_vs_real_scatter"

FIELD_MAP = {
    "observed": "Observed",
    "predicted": "Predicted",
}

TEXT_CONFIG = {
    "title": "Observed vs. Predicted Diagnostic",
    "x_label": "Measured value",
    "y_label": "Predicted value",
}

STYLE_CONFIG = {
    "figsize": (3.7, 3.7),
    "font_family": "sans-serif",
    "font_sans": ["Arial", "DejaVu Sans", "Helvetica", "Microsoft YaHei"],
    "font_size": 8.5,
    "point_color": "#4C78A8",
    "fit_color": "#E15759",
    "reference_color": "#333333",
    "axis_linewidth": 0.8,
}

EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "predicted_vs_real_scatter",
    "formats": ["svg", "pdf", "png"],
    "dpi": 600,
}

def load_data(path: str | Path) -> pd.DataFrame:
    """Loads source data from CSV file. Falls back to generating sample data if file missing."""
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    
    # Generate realistic sample data if file not found
    rng = np.random.default_rng(42)
    obs = rng.uniform(10, 100, 200)
    pred = 0.92 * obs + 4.0 + rng.normal(0, 6.0, 200)
    return pd.DataFrame({
        "Observed": obs,
        "Predicted": pred
    })

def prepare_data(df: pd.DataFrame, field_map: dict) -> pd.DataFrame:
    """Cleans data and maps columns to template keys."""
    obs = pd.to_numeric(df[field_map["observed"]], errors="coerce")
    pred = pd.to_numeric(df[field_map["predicted"]], errors="coerce")
    out = pd.DataFrame({
        "observed": obs,
        "predicted": pred,
    }).dropna()
    return out

def apply_style(style: dict) -> None:
    """Sets standard matplotlib typography and canvas features."""
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

def compute_metrics(data: pd.DataFrame) -> dict:
    """Computes basic model prediction validation statistics."""
    obs = data["observed"].to_numpy()
    pred = data["predicted"].to_numpy()
    ss_res = np.sum((obs - pred) ** 2)
    ss_tot = np.sum((obs - np.mean(obs)) ** 2)
    return {
        "r2": 1 - ss_res / ss_tot if ss_tot else np.nan,
        "rmse": np.sqrt(np.mean((obs - pred) ** 2)),
        "mae": np.mean(np.abs(obs - pred)),
        "n": len(obs),
    }

def plot(data: pd.DataFrame, text: dict, style: dict) -> plt.Figure:
    """Draws observed vs. predicted diagnostics figure."""
    apply_style(style)
    fig, ax = plt.subplots(figsize=style["figsize"], dpi=300)
    
    obs = data["observed"].to_numpy()
    pred = data["predicted"].to_numpy()
    
    # Scatter plot of raw data points
    ax.scatter(
        obs,
        pred,
        s=14,
        color=style["point_color"],
        alpha=0.6,
        edgecolors="none",
        zorder=2,
    )
    
    # Square axis scaling limits
    lim_min = min(np.nanmin(obs), np.nanmin(pred))
    lim_max = max(np.nanmax(obs), np.nanmax(pred))
    pad = 0.05 * (lim_max - lim_min) if lim_max > lim_min else 1.0
    lim_min -= pad
    lim_max += pad
    
    # 1:1 reference line
    ax.plot(
        [lim_min, lim_max],
        [lim_min, lim_max],
        color=style["reference_color"],
        linewidth=0.9,
        linestyle="-",
        zorder=1,
    )
    
    # Regression linear fit
    slope, intercept = np.polyfit(obs, pred, 1)
    fit_x = np.array([lim_min, lim_max])
    fit_y = slope * fit_x + intercept
    ax.plot(
        fit_x,
        fit_y,
        color=style["fit_color"],
        linewidth=1.2,
        linestyle="--",
        zorder=3,
    )
    
    # Metrics Textbox overlay
    metrics = compute_metrics(data)
    metric_text = (
        f"$R^2$ = {metrics['r2']:.3f}\n"
        f"RMSE = {metrics['rmse']:.2f}\n"
        f"MAE = {metrics['mae']:.2f}\n"
        f"N = {metrics['n']}"
    )
    ax.text(
        0.05,
        0.95,
        metric_text,
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=style["font_size"] - 1,
        bbox=dict(
            boxstyle="round,pad=0.35",
            facecolor="white",
            edgecolor="#CCCCCC",
            linewidth=0.5,
            alpha=0.95,
        ),
    )
    
    ax.set_xlim(lim_min, lim_max)
    ax.set_ylim(lim_min, lim_max)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title(text["title"], loc="left", fontweight="bold")
    ax.set_xlabel(text["x_label"])
    ax.set_ylabel(text["y_label"])
    ax.grid(True, color="#F0F0F0", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    
    return fig

def save_outputs(fig: plt.Figure, export: dict) -> list[Path]:
    """Saves figure in high-res vector and raster formats."""
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
