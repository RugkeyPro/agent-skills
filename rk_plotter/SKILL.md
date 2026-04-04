---
name: rk_plotter
description: "General-purpose scientific plotting skill for Python. Use when creating or refactoring publication-quality figures with matplotlib, seaborn, pandas plotting, cartopy, scipy, statsmodels, or numpy-based visualization workflows. Triggers on: scientific plotting, publication figure, matplotlib script, seaborn chart, environmental map, time series, scatter plot, boxplot, stacked bar chart, heatmap, uncertainty plot, statistical annotation, figure styling, color palette selection, journal-ready visualization, or requests for choosing the right chart."
argument-hint: "Describe the scientific question, plot type or comparison goal, input data structure, grouping variables, optional statistical needs, target style/journal, and expected output files"
---

# rk_plotter — General Scientific Plotting Skill

## When to Use
- Creating or modifying any Python plotting script, especially `plot_*.py`
- Turning tabular, matrix, raster, or geospatial data into publication-quality figures
- Choosing an appropriate chart type for a scientific question before implementation
- Standardizing figure style, layout, annotation, legends, colorbars, or export settings
- Adding statistical summaries, uncertainty bands, significance markers, or model-fit annotations
- Producing figures for papers, reports, supplementary material, posters, or presentations

## What This Skill Optimizes For
- Clear scientific communication over decoration
- Reproducible one-script-per-figure workflows
- Consistent configuration, typography, palette, and export conventions
- Sensible defaults for matplotlib and seaborn, with cartopy/raster support when needed
- Honest statistical communication, including uncertainty and method boundaries

## Input Contract

Collect or infer the following before writing code. If key details are missing, ask concise follow-up questions.

### 1. Scientific intent
- What question should the figure answer?
- Is the goal comparison, trend, relationship, composition, distribution, uncertainty, or spatial pattern?
- What is the expected reader action: identify a difference, compare scenarios, inspect variability, or localize hotspots?

### 2. Data contract
- Source type: `DataFrame`, CSV, Excel, matrix, NetCDF, GeoTIFF, shapefile, GeoJSON, model output, or aggregated summary table
- Variable roles: `x`, `y`, `hue`, `size`, `style`, `facet`, `label`, `weight`
- Units, transformations, missing-value rules, detection limits, and time/spatial resolution
- Whether data are raw observations, summaries, model predictions, or uncertainty intervals

### 3. Statistical contract
- Whether to show raw points, mean ± SD, mean ± SE, 95% CI, quantiles, fitted trend, or posterior interval
- Whether hypothesis testing is needed, and if so which family: parametric, nonparametric, regression, correlation, contingency, or permutation
- Whether multiple-comparison correction, effect sizes, or sample sizes must be shown
- Whether the user wants significance marks, model coefficients, or only descriptive uncertainty

### 4. Output contract
- Output filename stem and directory
- Required formats: usually `.svg` + `.png`, optional `.pdf`
- Intended use: journal, slide deck, report, dashboard snapshot, or exploratory notebook export
- Preferred style constraints: journal template, grayscale-safe, colorblind-safe, dark/light background, bilingual labels, aspect ratio limits

## Core Rules

1. Prefer **one figure script per output figure**. Keep data loading, transformation, plotting, and export in the same script unless the repository already uses shared helpers.
2. Use a **configuration module** if the repository already has one. Reuse rcParams, output directories, palette constants, and naming helpers instead of redefining them in every script.
3. If using matplotlib scripts, place `import matplotlib; matplotlib.use('Agg')` **before other matplotlib imports** unless the repository clearly uses a different backend pattern.
4. Save publication outputs as **SVG + PNG** by default; add **PDF** when editable vector output or journal submission requires it.
5. Favor **colorblind-safe palettes**, perceptually uniform sequential maps, and explicit uncertainty displays.
6. Avoid misleading defaults: 3D charts without a strong reason, dual y-axes for unrelated quantities, truncated axes without disclosure, and rainbow/jet-style colormaps.
7. Match annotation intensity to evidence. Do not overload figures with p-values, stars, and text boxes when the core pattern is already clear.

## Implementation Framework

### Step 1 — Confirm the request with the input contract
- Identify the scientific question and audience
- Confirm data shape and variable mapping
- Decide whether the figure is exploratory, report-grade, or publication-grade
- Determine whether statistics are descriptive, inferential, or model-based

### Step 2 — Choose the figure family
- Read `references/plot-selection.md` when the user is unsure what to draw
- Map the task to one of these families:
  - Comparison: bar, box, violin, strip, swarm, raincloud, lollipop
  - Trend: line, rolling trend, ribbon plot, seasonal facets
  - Relationship: scatter, hexbin, density contour, regression panel
  - Composition: stacked bar, area chart, mosaic plot, alluvial
  - Distribution: histogram, KDE, ECDF, ridgeline
  - Matrix/structure: heatmap, clustered heatmap, correlation matrix
  - Space/environment: raster map, choropleth, station map, transect section
  - Model/statistical summary: coefficient plot, effect plot, forest plot, residual plot

### Step 3 — Keep the script structure simple

Use this script order unless the repository has a stronger local convention:

1. Imports
2. Configuration/constants
3. Data loading and validation
4. Data transformation for plotting
5. Figure and axes creation
6. Plot layers
7. Labels, legends, annotations, colorbars
8. Statistical overlays if needed
9. Export and cleanup

### Step 4 — Use robust Python plotting foundations

Typical packages:
- Core: `matplotlib`, `numpy`, `pandas`, `pathlib`
- Statistical plotting: `seaborn`, `scipy`, `statsmodels`
- Matrix/scientific helpers: `matplotlib.colors`, `matplotlib.gridspec`
- Geospatial/environmental: `cartopy`, `geopandas`, `rasterio`, `xarray`

When building scripts:
- Prefer explicit axes objects (`fig, ax = plt.subplots(...)`) over stateful plotting
- Use `constrained_layout=True` or `plt.tight_layout()` carefully; confirm labels are not clipped
- Use shared legends/colorbars for multi-panel figures whenever possible
- Close figures explicitly after saving

### Step 5 — Separate config from figure logic

Keep these items centralized when possible:
- rcParams and font defaults
- output directory and naming helpers
- canonical palette lists
- journal/report size presets
- reusable annotation helpers

If the repo has no plotting config yet, create a light `plot_config.py` or equivalent only when the task actually needs reusable settings. Do not add scaffolding unnecessarily.

### Step 6 — Match the plot type to the message

Before coding, answer all of the following:
- What is the primary comparison unit?
- What should the reader compare first?
- What must remain visible: raw data, distribution shape, central tendency, trend, or geography?
- Which uncertainty measure is scientifically defensible here?
- Which visual encodings are redundant or distracting?

Read `references/plot-types.md` for concrete implementation patterns by chart family.

### Step 7 — Handle statistics responsibly

Read `references/statistical-boundaries.md` whenever the figure includes inferential claims.

Default principles:
- Prefer showing the underlying data distribution when sample sizes are moderate
- Prefer confidence/credible intervals over stars when the figure is about estimation
- Show effect size, slope, odds ratio, or coefficient magnitude when that is more informative than a p-value
- Use multiple-comparison correction when many pairwise tests or matrix cells are annotated
- Avoid implying causality from observational scatter plots without strong design support

### Step 8 — Export cleanly

Default export sequence:
1. finalize layout
2. save SVG
3. save PNG at high resolution
4. optionally save PDF
5. close figure

## Recommended Default Pattern

```python
import matplotlib
matplotlib.use("Agg")

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# optional: seaborn, scipy, statsmodels, cartopy, geopandas, rasterio, xarray

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(6, 4))

# plot layers here

fig.savefig(OUTPUT_DIR / "figure_name.svg", transparent=True, bbox_inches="tight")
fig.savefig(OUTPUT_DIR / "figure_name.png", dpi=600, transparent=True, bbox_inches="tight")
plt.close(fig)
```

## Reference Map

Read only the files relevant to the current task:

- `references/style-guide.md` — typography, figure sizes, layout, legends, colorbars, export
- `references/color-palettes.md` — qualitative, sequential, diverging, cyclic, and grayscale-safe palette guidance
- `references/stat-annotations.md` — significance labels, regression annotations, intervals, model callouts
- `references/plot-selection.md` — choosing the right chart for the scientific question
- `references/plot-types.md` — implementation guidance for common scientific chart families
- `references/statistical-boundaries.md` — when common plotting + testing combinations are appropriate or misleading
- `references/quality-checklist.md` — final quality-control checklist before finishing a figure

## Quick Plot-Type Guide

| Goal | Best starting point | Better alternatives when needed |
|------|---------------------|---------------------------------|
| Compare 2–8 groups | boxplot / violin + points | raincloud, estimation plot |
| Show group means only | point-range / bar with intervals | dot plot, lollipop |
| Show temporal trend | line + interval ribbon | seasonal facets, rolling median |
| Show bivariate relationship | scatter + fit | hexbin, density contour |
| Show composition across groups | stacked bar | normalized stacked bar, small multiples |
| Show matrix structure | heatmap | clustered heatmap, pair plot |
| Show spatial pattern | raster map / choropleth | contours, station map, faceted maps |
| Show model results | coefficient/effect plot | forest plot, marginal means |

## Before Finishing

- Confirm the figure answers the user’s scientific question directly
- Verify that chart type, scales, uncertainty, and annotations are defensible
- Use `references/quality-checklist.md` as the final gate
