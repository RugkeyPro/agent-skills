from __future__ import annotations

from rk_plotter_core import make_sample_data as _make_sample_data
from rk_plotter_core import plot_template as _plot_template
from rk_plotter_core import render_template as _render_template

TEMPLATE_ID = 'horizontal_stacked_bar_zoom'
CATEGORY = 'bar_composition'
KIND = 'horizontal_stacked_zoom'
TITLE = 'Horizontal stacked bar with zoomed inset'
DESCRIPTION = 'small categories needing an inset'
ORIGINAL_SCRIPT = 'figure-horizontal stacked bar chart with zoomed inset panel.py'
PREVIEW_BASENAME = 'regional_plastic_emissions_stacked_bar_zoom'
REQUIRES = ()
OPTIONAL_REQUIRES = ()


def make_sample_data(seed: int = 42):
    return _make_sample_data(KIND, seed=seed, title=TITLE)


def plot(data=None, *, ax=None, style=None, config=None):
    return _plot_template(KIND, data or make_sample_data(), ax=ax, title=TITLE, style=style, config=config)


def render(output_dir, basename=None, formats=("png", "pdf", "svg"), seed: int = 42, data=None):
    return _render_template(KIND, output_dir, basename or TEMPLATE_ID, title=TITLE, formats=formats, seed=seed, data=data)
