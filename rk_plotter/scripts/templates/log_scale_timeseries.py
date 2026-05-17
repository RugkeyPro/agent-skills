from __future__ import annotations

from rk_plotter_core import make_sample_data as _make_sample_data
from rk_plotter_core import plot_template as _plot_template
from rk_plotter_core import render_template as _render_template

TEMPLATE_ID = 'log_scale_timeseries'
CATEGORY = 'time_series'
KIND = 'log_timeseries'
TITLE = 'Log-scale time-series plot'
DESCRIPTION = 'series spanning orders of magnitude'
ORIGINAL_SCRIPT = 'figure-log-scale time series plot.py'
PREVIEW_BASENAME = 'cumulative_yield_fate_log_timeseries'
REQUIRES = ()
OPTIONAL_REQUIRES = ()


def make_sample_data(seed: int = 42):
    return _make_sample_data(KIND, seed=seed, title=TITLE)


def plot(data=None, *, ax=None, style=None, config=None):
    return _plot_template(KIND, data or make_sample_data(), ax=ax, title=TITLE, style=style, config=config)


def render(output_dir, basename=None, formats=("png", "pdf", "svg"), seed: int = 42, data=None):
    return _render_template(KIND, output_dir, basename or TEMPLATE_ID, title=TITLE, formats=formats, seed=seed, data=data)
