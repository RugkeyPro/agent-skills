from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping, Sequence
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl

DEFAULT_FORMATS = ("png", "pdf", "svg")

# Standardized publication figure sizes (in inches) based on journal column layouts
FIG_SIZES = {
    "single": (3.46, 3.0),
    "square": (3.46, 3.46),
    "wide": (7.2, 3.8),
    "map": (7.2, 4.0),
    "tall": (3.46, 4.8),
    "framework": (7.2, 4.8)
}

# Scientific color palettes (Color Universal Design / Okabe-Ito recommended values)
PALETTES = {
    "categorical": ["#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377", "#BBBBBB", "#000000"],
    "scenario": ["#1B9E77", "#D95F02", "#7570B3", "#E7298A", "#66A61E", "#E6AB02"],
    "model": ["#4C78A8", "#F58518", "#54A24B", "#B279A2", "#E45756"],
    "sequential": "viridis",
    "diverging": "RdBu_r",
    "log": "magma_r",
    "density": "mako"
}

# Publication-grade rcParams configuration preset
STYLE_RC = {
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans", "Helvetica", "Microsoft YaHei"],
    "font.size": 8.5,
    "axes.titlesize": 9.5,
    "axes.labelsize": 8.5,
    "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5,
    "legend.fontsize": 7.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "savefig.transparent": True,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
}

def apply_style(style_config: Mapping | None = None) -> None:
    """Applies standardized publication styles to matplotlib's rcParams."""
    mpl.rcParams.update(STYLE_RC)
    if style_config:
        mpl.rcParams.update(style_config)

def save_figure(
    fig,
    output_dir: str | Path,
    basename: str,
    formats: Iterable[str] = DEFAULT_FORMATS,
    dpi: int = 600
) -> list[Path]:
    """
    Saves a Matplotlib figure in high resolution in multiple formats
    and properly releases figure resources afterwards.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    paths: list[Path] = []
    for fmt in formats:
        fmt = fmt.lower().lstrip(".")
        filename = output_dir / f"{basename}.{fmt}"
        kwargs = {"bbox_inches": "tight", "transparent": True}
        if fmt in {"png", "jpg", "jpeg", "tif", "tiff"}:
            kwargs["dpi"] = dpi
        fig.savefig(filename, **kwargs)
        paths.append(filename)
        
    plt.close(fig)
    return paths
