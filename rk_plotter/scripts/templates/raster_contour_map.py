from __future__ import annotations

from rk_plotter_core import make_sample_data as _make_sample_data
from rk_plotter_core import plot_template as _plot_template
from rk_plotter_core import render_template as _render_template
from template_registry import TEMPLATES

TEMPLATE_ID = 'raster_contour_map'
_META = TEMPLATES[TEMPLATE_ID]
CATEGORY = _META["category"]
KIND = _META["kind"]
TITLE = _META["title"]
DESCRIPTION = _META["use"]
ORIGINAL_SCRIPT = _META["original"]
PREVIEW_BASENAME = _META["preview"]
TAGS = tuple(_META["tags"])
DATA_PROFILE = dict(_META["data_profile"])
STYLE_PROFILE = dict(_META["style_profile"])
BEST_FOR = _META["best_for"]
AVOID_WHEN = _META["avoid_when"]
REQUIRES = tuple(_META.get("requires", ()))
OPTIONAL_REQUIRES = tuple(_META.get("optional_requires", ()))


def _merged_config(config=None):
    merged = {"figsize": STYLE_PROFILE["figsize"]}
    if config:
        merged.update(config)
    return merged


def make_sample_data(seed: int = 42):
    return _make_sample_data(KIND, seed=seed, title=TITLE)


def plot(data=None, *, ax=None, style=None, config=None):
    return _plot_template(KIND, data or make_sample_data(), ax=ax, title=TITLE, style=style, config=_merged_config(config))


def render(output_dir, basename=None, formats=("png", "pdf", "svg"), seed: int = 42, data=None, config=None):
    return _render_template(
        KIND,
        output_dir,
        basename or TEMPLATE_ID,
        title=TITLE,
        formats=formats,
        seed=seed,
        data=data,
        config=_merged_config(config),
    )
