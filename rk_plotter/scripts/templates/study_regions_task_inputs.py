from __future__ import annotations

from rk_plotter_core import make_sample_data as _make_sample_data
from rk_plotter_core import plot_template as _plot_template
from rk_plotter_core import render_template as _render_template

TEMPLATE_ID = 'study_regions_task_inputs'
CATEGORY = 'framework'
KIND = 'study_framework'
TITLE = 'Study regions, tasks, and inputs overview'
DESCRIPTION = 'overview figures for regions and inputs'
ORIGINAL_SCRIPT = 'figure-study regions + task + inputs.py'
PREVIEW_BASENAME = 'stimp_overview_framework'
REQUIRES = ()
OPTIONAL_REQUIRES = ()


def make_sample_data(seed: int = 42):
    return _make_sample_data(KIND, seed=seed, title=TITLE)


def plot(data=None, *, ax=None, style=None, config=None):
    return _plot_template(KIND, data or make_sample_data(), ax=ax, title=TITLE, style=style, config=config)


def render(output_dir, basename=None, formats=("png", "pdf", "svg"), seed: int = 42, data=None):
    return _render_template(KIND, output_dir, basename or TEMPLATE_ID, title=TITLE, formats=formats, seed=seed, data=data)
