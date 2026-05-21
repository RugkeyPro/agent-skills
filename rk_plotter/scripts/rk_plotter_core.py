from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "none"

import matplotlib as mpl
import matplotlib.pyplot as plt

DEFAULT_FORMATS = ("png", "pdf", "svg")


def apply_style(style: Mapping | None = None) -> None:
    """Apply the shared rk_plotter publication style."""
    style = dict(style or {})
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans", "Microsoft YaHei"],
        "font.size": style.get("font.size", 8.5),
        "axes.titlesize": style.get("axes.titlesize", 9.5),
        "axes.labelsize": style.get("axes.labelsize", 8.5),
        "xtick.labelsize": style.get("xtick.labelsize", 7.5),
        "ytick.labelsize": style.get("ytick.labelsize", 7.5),
        "legend.fontsize": style.get("legend.fontsize", 7.5),
        "axes.spines.top": False,
        "axes.spines.right": False,
        "savefig.transparent": True,
        "savefig.bbox": "tight",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    })


def save_figure(
    fig,
    output_dir: str | Path,
    basename: str,
    formats: Iterable[str] = DEFAULT_FORMATS,
    dpi: int = 600,
    transparent: bool = True,
) -> list[Path]:
    """Save a figure as png/pdf/svg and close it after export."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for fmt in formats:
        fmt = fmt.lower().lstrip(".")
        path = output_dir / f"{basename}.{fmt}"
        kwargs = {"bbox_inches": "tight", "transparent": transparent}
        if fmt in {"png", "jpg", "jpeg", "tif", "tiff"}:
            kwargs["dpi"] = dpi
        fig.savefig(path, **kwargs)
        paths.append(path)
    plt.close(fig)
    return paths
