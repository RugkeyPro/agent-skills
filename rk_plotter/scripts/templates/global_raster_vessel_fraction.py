from __future__ import annotations

from rk_plotter_core import make_sample_data as _make_sample_data
from rk_plotter_core import plot_template as _plot_template
from rk_plotter_core import render_template as _render_template

TEMPLATE_ID = 'global_raster_vessel_fraction'
CATEGORY = 'maps'
KIND = 'raster_map'
TITLE = 'Global raster map of publicly tracked vessel fraction'
DESCRIPTION = 'global gridded fractions or exposure'
ORIGINAL_SCRIPT = 'figure-global raster map of publicly tracked vessel fraction.py'
PREVIEW_BASENAME = 'global_publicly_tracked_fishing_vessels'
REQUIRES = ()
OPTIONAL_REQUIRES = ('cartopy',)


def make_sample_data(seed: int = 42):
    return _make_sample_data(KIND, seed=seed, title=TITLE)


def plot(data=None, *, ax=None, style=None, config=None):
    return _plot_template(KIND, data or make_sample_data(), ax=ax, title=TITLE, style=style, config=config)


def render(output_dir, basename=None, formats=("png", "pdf", "svg"), seed: int = 42, data=None):
    return _render_template(KIND, output_dir, basename or TEMPLATE_ID, title=TITLE, formats=formats, seed=seed, data=data)
