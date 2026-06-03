# Template Index: Scientific Plotting Catalog

Use this table to match user requests and datasets to the appropriate scientific plotting template.

| Template ID | Chart Category | Primary Use Case | Required Fields | Locked Structures (Do Not Change) |
|---|---|---|---|---|
| `predicted_vs_real_scatter` | Regression / ML | Model prediction diagnostics (Measured vs. Predicted). | `observed`, `predicted` | Single square panel, 1:1 diagonal line, linear fit dashed line, performance metrics box. |
| `density_scatter` | Scatter Plot | Visualizing high-density paired numeric observations. | `x`, `y` | Points colored by local Gaussian KDE density using Seaborn 'mako' colormap, colorbar on right. |
| `dual_panel_scatter_fit` | Multi-panel | Comparing relationships of two groups or datasets side-by-side. | `x1`, `y1`, `x2`, `y2` | Left-right double panels, shared y-axis limits, linear fit regression curves. |
| `multi_scenario_timeseries` | Time Series | Projecting multiple model/experimental curves over time. | `x` (Time), `series` (List of scenario columns) | X-axis calendar time, color-differentiated scenario lines, publication-friendly top legend. |
| `scenario_uncertainty_timeseries` | Time Series | Trends over time with uncertainty/confidence envelopes. | `x` (Time), `y` (Mean), `lower`, `upper` | Center line trend plus transparent alpha band indicating standard deviation or IQR. |
| `event_period_timeseries` | Time Series | Analyzing trajectories before, during, and after an event. | `x`, `y` | Line series plus vertical highlighted shaded window (`axvspan`) representing target event. |
| `stacked_percent_bar` | Composition | Component shares or relative abundance across groups (sum=100%).| `group`, `components` (columns) | Vertical 100% stacked bar chart, clean top legend. |
| `horizontal_stacked_bar` | Composition | Part-of-whole composition with long categorical group labels. | `group`, `components` (columns) | Horizontal 100% stacked bar chart, clean top legend. |
| `boxen_plot` | Distribution | Analyzing detailed distribution shapes across groups. | `group`, `value` | Letter-value boxen plot using Seaborn, quantile-based color bands. |
| `violin_boxplot` | Distribution | Showing probability density and IQR statistics simultaneously. | `group`, `value` | Violin plot with internal box-and-whisker overlay. |
| `heatmap_2d` | Correlation / Grid | Displaying matrices, correlation coefficients, or grid values. | `x` (Categories), `y` (Categories), `value` | 2D color-coded grid with annotated cells and right-hand colorbar. |
| `raster_map` | Spatial Map | Gridded spatial fields (e.g., global anomalies or exposures). | `lon`, `lat`, `raster` (2D array) | Geographic projection (Cartopy PlateCarree/Robinson), spatial grid overlay, colorbar. |
| `choropleth_map` | Spatial Map | Country-level or administrative regional indicators. | `region` (ISO codes), `value` | Robinson projection global country outlines colored by quantitative values. |
| `shap_importance_bar` | ML Explainability | Ranking feature importances or summary metrics. | `feature`, `importance` | Ranked horizontal bar chart sorted in descending order of feature impact. |
| `multipanel_layout` | Layout Frame | Combining different chart types into a single figure. | Custom per panel | GridSpec multi-panel layout canvas (e.g. 2x2 grids) with explicit panel markers (A, B, C, D). |

---

## Data Structure Compatibility Guide

- **Time Series**: If the dataset contains a column like `Year`, `Date`, or `Month` and multiple scenario columns, use `multi_scenario_timeseries` or `scenario_uncertainty_timeseries`.
- **Spatial Grids**: If data contains coordinates like `longitude/latitude` or `x/y` grids with a 2D matrix of values, use `raster_map`.
- **Compositions**: If data represents percentage splits (relative abundance, mass fractions, cost shares) that add up to 100% for each category, use `stacked_percent_bar` or `horizontal_stacked_bar`.
- **Distributions**: If data contains a categorical grouping column and continuous measurement values (e.g. experimental treatments vs. values), use `boxen_plot` or `violin_boxplot`.
- **Predictions**: If data contains target observations (observed) and corresponding model outputs (predicted), use `predicted_vs_real_scatter`.
