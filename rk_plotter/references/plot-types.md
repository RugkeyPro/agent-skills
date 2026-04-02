# Plot Types — rk_plotter

This reference describes how to implement common scientific chart families while preserving a one-script-per-figure workflow.

## 1. Scatter Plots

Use for relationships, calibration, model-vs-observation checks, and environmental gradients.

Best practices:
- alpha-reduce points when dense
- add regression or smoother only when the fit is scientifically meaningful
- annotate `n`, slope, `R²`, or effect estimate only if it helps interpretation
- use hexbin or density contours when overplotting is severe

Useful variants:
- grouped scatter
- faceted scatter
- hexbin
- contour density
- scatter with marginal histograms

## 2. Line and Time-Series Plots

Use for trends, trajectories, seasonal cycles, scenario comparisons, or long-term monitoring.

Best practices:
- keep time continuous and ordered
- show uncertainty as ribbon, band, or interval bars where justified
- mark interventions, regime shifts, or thresholds with subtle reference lines
- facet or directly label lines instead of overcrowding legends

Useful variants:
- multi-line trend
- anomaly plot
- ribbon plot
- rolling mean/median
- seasonal climatology panel

## 3. Boxplots, Violins, and Rainclouds

Use for group-wise distributions, treatment comparisons, site comparisons, and before/after studies.

Best practices:
- overlay raw points when sample size allows
- make sure the interval type is clear if showing mean/CI instead of quartiles
- use horizontal orientation for long category labels
- do not imply symmetry if the distribution is strongly skewed

Useful variants:
- box + strip
- violin + swarm
- raincloud
- paired slope chart for repeated measures

## 4. Bar, Point-Range, and Lollipop Charts

Use for summarized estimates, categorical totals, or ordered comparisons.

Best practices:
- start bars at zero unless explicitly broken and disclosed
- prefer point-range when uncertainty matters more than filled area
- sort categories by scientific or effect-size order, not arbitrary alphabetic order
- use lollipop or dot plots when many categories would create visual bulk

Useful variants:
- grouped bar
- stacked bar
- normalized stacked bar
- point estimate + CI
- lollipop ranking

## 5. Stacked Bar and Composition Charts

Use when the message is composition of a whole across groups, sites, times, or scenarios.

Best practices:
- keep stack order consistent across panels
- use normalized stacked bars for proportion comparison
- show totals separately if both total magnitude and composition matter
- avoid too many categories; aggregate low-frequency classes into `Other` when justified

## 6. Histograms, KDE, ECDF, and Ridgelines

Use for distributions, threshold exceedance, skewness, and site/group distribution comparison.

Best practices:
- choose bins using domain logic or a transparent rule
- use ECDF when exact cumulative comparison matters
- use ridgelines carefully; they look attractive but can distort scale perception
- do not overlay too many KDEs on one axis

## 7. Heatmaps and Correlation Matrices

Use for covariance structure, feature comparison, distance matrices, or cell-wise responses.

Best practices:
- label the scale and midpoint clearly
- cluster only when the ordering itself is not scientifically fixed
- round annotations consistently and avoid annotating every cell in large matrices
- use masking for redundant upper triangles when appropriate

Useful variants:
- correlation heatmap
- clustered heatmap
- response matrix
- confusion matrix

## 8. Maps for Environmental and Spatial Data

Use for gridded data, site observations, regional summaries, anomaly surfaces, and habitat suitability.

Best practices:
- use projection and extent appropriate to the region
- keep coastlines, borders, and land fills subtle
- use a shared scale across comparable maps
- do not mix too many point, polygon, and raster encodings in one panel
- disclose interpolation or smoothing where used

Useful variants:
- raster map
- choropleth
- station/bubble map
- contour/isoline map
- faceted scenario maps
- depth transect / longitude-latitude section

## 9. Uncertainty and Model Summary Plots

Use for regression coefficients, Bayesian intervals, sensitivity analyses, and scenario envelopes.

Best practices:
- emphasize interval width and estimate direction
- keep zero/reference line visible
- sort coefficients by magnitude or conceptual grouping
- annotate units or transformation scale when coefficients are not directly interpretable

Useful variants:
- coefficient plot
- forest plot
- marginal effects plot
- posterior interval plot
- residual diagnostics panel

## 10. Multi-Panel Figure Composition

Use when the scientific story requires linked evidence types.

Best practices:
- align panels to support comparison
- keep each panel’s role distinct: context, distribution, trend, model, map
- share legends/colorbars where possible
- avoid panel overload; four strong panels usually communicate better than eight weak ones
