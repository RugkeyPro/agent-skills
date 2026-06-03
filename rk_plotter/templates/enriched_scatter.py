# TEMPLATE_ID: enriched_scatter
# TEMPLATE_VERSION: 1.0
# FIGURE_TYPE: high_fidelity_enriched_scatter_and_model_diagnostic_plots
#
# IMAGE-DERIVED MODES:
# - enrichment_bubble: fold-enrichment bubble scatter with colorbar and count legend
# - marginal_true_pred: true-vs-predicted scatter with top/right KDE marginals
# - joint_kde_hist: overlaid 2D KDE fields plus marginal histograms and colorbars
# - grouped_regression: grouped scatter, dashed fits, translucent confidence bands
# - residual_diagnostic: true-vs-predicted panel plus residual panel and marginals
# - shap_dependence: SHAP dependence scatter with smooth partial curve
#
# USER_DECISION_POINTS_BEFORE_USE:
# - scatter_mode, color palette, size legend levels, marginal distributions, fitted lines,
#   confidence bands, metric annotations, highlighted labels, panel labels.

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

try:
    from scipy.stats import gaussian_kde
    from scipy.ndimage import gaussian_filter1d
except ImportError:
    gaussian_kde = None
    gaussian_filter1d = None


TEMPLATE_ID = "enriched_scatter"

FIELD_MAP = {
    "x": "x",
    "y": "y",
    "group": "group",
    "size": "size",
    "color": "color",
    "label": "label",
}

TEXT_CONFIG = {
    "x_label": "Fold enrichment",
    "y_label": r"-log$_{10}$(FDR)",
    "colorbar_label": r"-log$_{10}$(FDR)",
    "size_legend_title": "Count",
    "title": "",
    "metric_text": "Train RMSE: 1.02\nTest RMSE: 2.56",
}

STYLE_CONFIG = {
    "scatter_mode": "enrichment_bubble",
    "figsize": (3.5, 3.0),
    "dpi": 300,
    "font_family": "Arial",
    "font_size": 7.2,
    "axis_linewidth": 0.9,
    "panel_label": None,
    "palette": ["#7fcdbb", "#2c7fb8", "#fdae61", "#f03b20"],
}

EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "enriched_scatter",
    "formats": ["png", "pdf", "svg"],
    "dpi": 600,
}


def apply_style(style: dict) -> None:
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": [style.get("font_family", "Arial"), "Arial", "DejaVu Sans"],
        "font.size": style["font_size"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.unicode_minus": False,
    })


def load_data(path: str | Path = "data.csv") -> pd.DataFrame:
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    rng = np.random.default_rng(42)
    mode = STYLE_CONFIG["scatter_mode"]
    if mode == "enrichment_bubble":
        x = 1.04 + rng.gamma(2.0, 0.045, 90)
        y = 0.8 + (x - 1.03) * 13 + rng.normal(0, 0.35, len(x))
        y = np.clip(y, 0.9, 5.6)
        size = np.clip(rng.gamma(2.2, 18, len(x)), 5, 80)
        labels = [""] * len(x)
        top = np.argsort(y + x * 4)[-10:]
        names = ["AP1", "ATF", "CREB", "XBP1", "CREBP1", "SP1", "PAX5", "HTF", "NMYC", "MAX"]
        for i, name in zip(top, names):
            labels[i] = name
        return pd.DataFrame({"x": x, "y": y, "size": size, "color": y, "label": labels})
    if mode in {"marginal_true_pred", "residual_diagnostic"}:
        true = np.linspace(12, 60, 95) + rng.normal(0, 3, 95)
        pred = true * 0.96 + 2.0 + rng.normal(0, 2.3, 95)
        group = np.where(rng.random(len(true)) > 0.45, "Train", "Test")
        return pd.DataFrame({"x": true, "y": pred, "group": group})
    if mode == "joint_kde_hist":
        a = rng.multivariate_normal([47, 48], [[8, 5], [5, 16]], 500)
        b = rng.multivariate_normal([54, 55], [[9, 4], [4, 15]], 500)
        return pd.DataFrame({"x": np.r_[a[:, 0], b[:, 0]], "y": np.r_[a[:, 1], b[:, 1]], "group": ["X"] * len(a) + ["Y"] * len(b)})
    if mode == "shap_dependence":
        x = rng.uniform(0.05, 1.0, 1200)
        y = 0.155 - 0.028 / (1 + np.exp(-(x - 0.50) * 28)) + rng.normal(0, 0.006, len(x))
        return pd.DataFrame({"x": x, "y": y})
    groups = ["Group 1", "Group 2", "Group 3"]
    rows = []
    params = [(5, 1.35, "#6a9f50"), (9, 1.05, "#4e6fae"), (14, 0.45, "#46a7a3")]
    for group, (offset, slope, color) in zip(groups, params):
        x = rng.uniform(5, 25, 35)
        y = offset + slope * x + rng.normal(0, 1.3, len(x))
        rows.extend({"x": xi, "y": yi, "group": group, "color": color} for xi, yi in zip(x, y))
    return pd.DataFrame(rows)


def prepare_data(df: pd.DataFrame, field_map: dict) -> pd.DataFrame:
    out = pd.DataFrame({
        "x": pd.to_numeric(df[field_map["x"]], errors="coerce"),
        "y": pd.to_numeric(df[field_map["y"]], errors="coerce"),
    })
    for key in ["group", "label"]:
        col = field_map[key]
        if col in df.columns:
            out[key] = df[col].astype(str)
    for key in ["size", "color"]:
        col = field_map[key]
        if col in df.columns:
            out[key] = pd.to_numeric(df[col], errors="coerce")
    return out.dropna(subset=["x", "y"])


def style_axes(ax, style):
    for spine in ax.spines.values():
        spine.set_linewidth(style["axis_linewidth"])
    ax.tick_params(direction="out", length=3.5, width=0.8)


def kde_fill(ax, values, orient, color, alpha=0.22):
    if gaussian_kde is None:
        hist, edges = np.histogram(values, bins=25, density=True)
        grid = (edges[:-1] + edges[1:]) / 2
        dens = hist
    else:
        grid = np.linspace(values.min(), values.max(), 200)
        dens = gaussian_kde(values)(grid)
    if orient == "x":
        ax.fill_between(grid, 0, dens, color=color, alpha=alpha)
        ax.plot(grid, dens, color=color, linewidth=0.8)
    else:
        ax.fill_betweenx(grid, 0, dens, color=color, alpha=alpha)
        ax.plot(dens, grid, color=color, linewidth=0.8)


def plot_enrichment(data, text, style):
    fig, ax = plt.subplots(figsize=style["figsize"], dpi=style["dpi"])
    cmap = mpl.colors.LinearSegmentedColormap.from_list("fdr", ["#3aa7e8", "#f7f48b", "#f03b20"])
    sizes = np.interp(data.get("size", pd.Series(np.ones(len(data)) * 25)), [5, 80], [8, 420])
    sc = ax.scatter(data["x"], data["y"], s=sizes, c=data.get("color", data["y"]), cmap=cmap, edgecolor="black", linewidth=0.55, alpha=0.9)
    ax.set_xlim(1.0, 1.6)
    ax.set_ylim(0, 6)
    ax.set_xticks([1.0, 1.2, 1.4, 1.6])
    ax.set_yticks([0, 2, 4, 6])
    ax.grid(True, color="0.75", linewidth=0.7)
    ax.set_xlabel(text["x_label"], fontsize=style["font_size"] + 1.2, fontweight="bold")
    ax.set_ylabel(text["y_label"], fontsize=style["font_size"] + 1.2, fontweight="bold")
    for _, row in data[data.get("label", "") != ""].iterrows():
        ax.text(row["x"] + 0.015, row["y"], row["label"], fontsize=style["font_size"] + 0.5, va="center")
    cbar = fig.colorbar(sc, ax=ax, fraction=0.045, pad=0.04)
    cbar.ax.set_title(text["colorbar_label"], fontsize=style["font_size"], pad=7)
    legend_sizes = [8.56, 25.13, 73.80]
    handles = [Line2D([0], [0], marker="o", linestyle="", markerfacecolor="black", markeredgecolor="black", markersize=np.sqrt(np.interp(v, [5, 80], [8, 420])), label=f"{v:.2f}") for v in legend_sizes]
    ax.legend(handles=handles, title=text["size_legend_title"], loc="lower left", bbox_to_anchor=(1.02, 0.02), frameon=False, labelspacing=1.1)
    style_axes(ax, style)
    return fig


def plot_marginal_true_pred(data, text, style):
    fig = plt.figure(figsize=(3.2, 3.2), dpi=style["dpi"])
    gs = GridSpec(2, 2, height_ratios=[0.38, 2.6], width_ratios=[2.6, 0.38], hspace=0, wspace=0)
    ax_top = fig.add_subplot(gs[0, 0])
    ax = fig.add_subplot(gs[1, 0])
    ax_right = fig.add_subplot(gs[1, 1])
    colors = {"Train": "#a8d5a2", "Test": "#2c7fb8"}
    for group, sub in data.groupby("group"):
        ax.scatter(sub["x"], sub["y"], s=24, color=colors.get(group, "#777777"), edgecolor="0.35", alpha=0.85, label=f"{group}: RMSE: {np.sqrt(np.mean((sub['y']-sub['x'])**2)):.2f}")
        kde_fill(ax_top, sub["x"].to_numpy(), "x", colors.get(group, "#777777"))
        kde_fill(ax_right, sub["y"].to_numpy(), "y", colors.get(group, "#777777"))
    lo, hi = 10, 65
    ax.plot([lo, hi], [lo, hi], "--", color="0.35", linewidth=0.8, label="Ideal fit")
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_xlabel("True", fontweight="bold")
    ax.set_ylabel("Predicted", fontweight="bold")
    ax.legend(loc="upper left", frameon=False, fontsize=style["font_size"] - 0.4)
    ax_top.axis("off")
    ax_right.axis("off")
    style_axes(ax, style)
    return fig


def plot_joint_kde_hist(data, text, style):
    fig = plt.figure(figsize=(3.5, 3.15), dpi=style["dpi"])
    gs = GridSpec(2, 3, height_ratios=[0.65, 2.7], width_ratios=[2.7, 0.65, 0.18], hspace=0.12, wspace=0.15)
    ax_top = fig.add_subplot(gs[0, 0])
    ax = fig.add_subplot(gs[1, 0])
    ax_right = fig.add_subplot(gs[1, 1])
    cax = fig.add_subplot(gs[1, 2])
    colors = {"X": "#9bd7e3", "Y": "#f3a0a0"}
    cmaps = {"X": "Blues", "Y": "Reds"}
    for group, sub in data.groupby("group"):
        ax_top.hist(sub["x"], bins=45, density=True, color=colors[group], alpha=0.45, edgecolor="0.3", linewidth=0.45, label=group)
        ax_right.hist(sub["y"], bins=45, density=True, orientation="horizontal", color=colors[group], alpha=0.45, edgecolor="0.3", linewidth=0.45)
        if gaussian_kde is not None:
            xgrid = np.linspace(30, 70, 100)
            ygrid = np.linspace(30, 70, 100)
            xx, yy = np.meshgrid(xgrid, ygrid)
            zz = gaussian_kde(np.vstack([sub["x"], sub["y"]]))(np.vstack([xx.ravel(), yy.ravel()])).reshape(xx.shape)
            zz = zz / zz.max()
            ax.contourf(xx, yy, zz, levels=np.linspace(0.08, 1, 12), cmap=cmaps[group], alpha=0.34)
            ax.contour(xx, yy, zz, levels=np.linspace(0.2, 0.9, 5), cmap=cmaps[group], linewidths=0.45, alpha=0.5)
    sm = mpl.cm.ScalarMappable(cmap="Blues", norm=mpl.colors.Normalize(0, 1))
    fig.colorbar(sm, cax=cax)
    ax.set_xlim(30, 70)
    ax.set_ylim(30, 70)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax_top.legend(frameon=False, loc="upper right")
    ax_right.set_xlabel("Frequency")
    style_axes(ax, style)
    return fig


def plot_grouped_regression(data, text, style):
    fig, ax = plt.subplots(figsize=(3.0, 3.0), dpi=style["dpi"])
    colors = ["#6a9f50", "#4e6fae", "#46a7a3", "#f28e6b"]
    for i, (group, sub) in enumerate(data.groupby("group")):
        color = colors[i % len(colors)]
        ax.scatter(sub["x"], sub["y"], s=18, color=color, edgecolor="0.25", linewidth=0.3, alpha=0.85)
        coef = np.polyfit(sub["x"], sub["y"], 1)
        xs = np.linspace(sub["x"].min(), sub["x"].max(), 80)
        ys = np.polyval(coef, xs)
        ax.plot(xs, ys, "--", color=color, linewidth=1.0)
        ax.fill_between(xs, ys - 1.0, ys + 1.0, color=color, alpha=0.14, linewidth=0)
        r2 = np.corrcoef(sub["x"], sub["y"])[0, 1] ** 2
        ax.text(0.06, 0.93 - i * 0.07, f"{group}: $R^2$={r2:.3f}", color=color, transform=ax.transAxes, fontweight="bold")
    ax.set_xlabel("X Value (units)", fontweight="bold")
    ax.set_ylabel("Y Value (units)", fontweight="bold")
    ax.set_xlim(4, 25.5)
    ax.set_ylim(7, 30)
    ax.minorticks_on()
    style_axes(ax, style)
    return fig


def plot_residual_diagnostic(data, text, style):
    fig = plt.figure(figsize=(3.5, 3.9), dpi=style["dpi"])
    gs = GridSpec(4, 3, height_ratios=[0.55, 2.0, 0.25, 1.25], width_ratios=[2.6, 0.12, 0.45], hspace=0.15, wspace=0.05)
    ax_top = fig.add_subplot(gs[0, 0])
    ax = fig.add_subplot(gs[1, 0])
    ax_right = fig.add_subplot(gs[1, 2])
    ax_res = fig.add_subplot(gs[3, 0], sharex=ax)
    colors = {"Train": "#8c8c8c", "Test": "#ff8c1a"}
    for group, sub in data.groupby("group"):
        c = colors.get(group, "#777")
        ax.scatter(sub["x"], sub["y"], s=18, color=c, alpha=0.75, label=f"{group} data")
        ax_res.scatter(sub["x"], sub["y"] - sub["x"], s=16, color=c, alpha=0.75)
        ax_top.hist(sub["x"], bins=25, density=True, histtype="step", color=c, linewidth=1.0)
        kde_fill(ax_top, sub["x"].to_numpy(), "x", c, alpha=0.18)
        ax_right.hist(sub["y"], bins=25, density=True, orientation="horizontal", histtype="step", color=c, linewidth=1.0)
        kde_fill(ax_right, sub["y"].to_numpy(), "y", c, alpha=0.18)
    xs = np.linspace(5, 52, 100)
    ax.plot(xs, xs, color="black", linewidth=1.1, label="Fitted line")
    ax.plot(xs, xs * 0.96 + 2, color="black", linewidth=0.8)
    ax.text(0.5, 0.93, "SVR", transform=ax.transAxes, ha="center", fontsize=style["font_size"] + 4)
    ax.text(0.05, 0.78, "$R^2_{test}$=0.93\nRMSE$_{test}$=2.24", transform=ax.transAxes, color="#d7191c", fontsize=style["font_size"] + 1.5)
    ax.legend(loc="lower right", frameon=True, fontsize=style["font_size"])
    ax_res.axhline(0, color="black", linewidth=0.9)
    ax_res.text(0.64, 0.65, "MAE (Train) = 0.610\nMAE (Test) = 1.692", transform=ax_res.transAxes, fontsize=style["font_size"] + 1)
    ax_res.set_ylabel("Residuals")
    ax_res.set_xlabel("Experimental Yield", fontsize=style["font_size"] + 2)
    ax.set_ylabel("Predicted Yield", fontsize=style["font_size"] + 2)
    ax_top.axis("off")
    ax_right.axis("off")
    for a in [ax, ax_res]:
        a.grid(True, color="0.85", linewidth=0.6)
        style_axes(a, style)
    return fig


def plot_shap_dependence(data, text, style):
    fig, ax = plt.subplots(figsize=(2.1, 1.75), dpi=style["dpi"])
    ax.scatter(data["x"], data["y"], s=4, color="#9bd7e3", alpha=0.55, edgecolor="none")
    order = np.argsort(data["x"].to_numpy())
    xs = data["x"].to_numpy()[order]
    ys = data["y"].to_numpy()[order]
    if gaussian_filter1d is not None:
        smooth = gaussian_filter1d(ys, 45)
    else:
        smooth = pd.Series(ys).rolling(80, center=True, min_periods=5).mean().bfill().ffill().to_numpy()
    ax.plot(xs, smooth, color="#b85c5c", linewidth=1.1)
    ax.set_xlabel("NDVI")
    ax.set_ylabel("SHAP main effect value for NDVI", fontsize=style["font_size"] - 1)
    ax.text(0.05, 0.92, "(h)", transform=ax.transAxes, fontsize=style["font_size"], fontweight="bold")
    style_axes(ax, style)
    return fig


def plot(data: pd.DataFrame, text: dict, style: dict) -> plt.Figure:
    apply_style(style)
    mode = style["scatter_mode"]
    if mode == "marginal_true_pred":
        return plot_marginal_true_pred(data, text, style)
    if mode == "joint_kde_hist":
        return plot_joint_kde_hist(data, text, style)
    if mode == "grouped_regression":
        return plot_grouped_regression(data, text, style)
    if mode == "residual_diagnostic":
        return plot_residual_diagnostic(data, text, style)
    if mode == "shap_dependence":
        return plot_shap_dependence(data, text, style)
    return plot_enrichment(data, text, style)


def save_outputs(fig: plt.Figure, export: dict) -> list[Path]:
    output_dir = Path(export["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for fmt in export["formats"]:
        path = output_dir / f"{export['basename']}.{fmt}"
        kwargs = {"bbox_inches": "tight", "pad_inches": 0.04}
        if fmt == "png":
            kwargs["dpi"] = export["dpi"]
        fig.savefig(path, **kwargs)
        paths.append(path)
    plt.close(fig)
    return paths


def main() -> None:
    df = load_data(sys.argv[1] if len(sys.argv) > 1 else "data.csv")
    data = prepare_data(df, FIELD_MAP)
    fig = plot(data, TEXT_CONFIG, STYLE_CONFIG)
    print("Generated:", [str(p) for p in save_outputs(fig, EXPORT_CONFIG)])


if __name__ == "__main__":
    main()
