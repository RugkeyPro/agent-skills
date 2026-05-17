from __future__ import annotations

from rk_plotter_core import make_sample_data as _make_sample_data
from rk_plotter_core import plot_template as _plot_template
from rk_plotter_core import render_template as _render_template

TEMPLATE_ID = 'loglog_model_observation_scatter'
CATEGORY = 'scatter_model'
KIND = 'loglog_scatter'
TITLE = 'Log-log model-observation scatter'
DESCRIPTION = 'comparisons spanning orders of magnitude'
ORIGINAL_SCRIPT = 'figure-log-log model–observation comparison scatter plot.py'
PREVIEW_BASENAME = 'model_observation_loglog_scatter'
REQUIRES = ()
OPTIONAL_REQUIRES = ()


def make_sample_data(seed: int = 42):
    return _make_sample_data(KIND, seed=seed, title=TITLE)


def plot(data=None, *, ax=None, style=None, config=None):
    return _plot_template(KIND, data or make_sample_data(), ax=ax, title=TITLE, style=style, config=config)


def render(output_dir, basename=None, formats=("png", "pdf", "svg"), seed: int = 42, data=None):
    return _render_template(KIND, output_dir, basename or TEMPLATE_ID, title=TITLE, formats=formats, seed=seed, data=data)
