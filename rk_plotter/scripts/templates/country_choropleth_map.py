from __future__ import annotations

from rk_plotter_core import make_sample_data as _make_sample_data
from rk_plotter_core import plot_template as _plot_template
from rk_plotter_core import render_template as _render_template

TEMPLATE_ID = 'country_choropleth_map'
CATEGORY = 'maps'
KIND = 'country_choropleth'
TITLE = 'Country-level choropleth map'
DESCRIPTION = 'country or administrative-unit maps'
ORIGINAL_SCRIPT = 'figure-country-level choropleth map.py'
PREVIEW_BASENAME = 'global_country_plastic_emissions_choropleth'
REQUIRES = ()
OPTIONAL_REQUIRES = ('cartopy',)


def make_sample_data(seed: int = 42):
    return _make_sample_data(KIND, seed=seed, title=TITLE)


def plot(data=None, *, ax=None, style=None, config=None):
    return _plot_template(KIND, data or make_sample_data(), ax=ax, title=TITLE, style=style, config=config)


def render(output_dir, basename=None, formats=("png", "pdf", "svg"), seed: int = 42, data=None):
    return _render_template(KIND, output_dir, basename or TEMPLATE_ID, title=TITLE, formats=formats, seed=seed, data=data)
