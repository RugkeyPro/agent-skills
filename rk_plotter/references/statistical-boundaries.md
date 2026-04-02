# Statistical Boundaries — rk_plotter

Use this reference when a figure makes inferential claims or overlays fitted statistics.

## General Principles

- A plot can be descriptive without hypothesis testing
- Prefer estimation and uncertainty intervals when the goal is magnitude, not thresholding by p-value
- Align the figure annotation with the actual analysis level: observation, group, model, or posterior summary
- Avoid displaying more statistical precision than the design supports

## Common Pairings and Their Boundaries

### Scatter Plot + Regression Line

Reasonable when:
- the relationship is approximately monotonic or linear
- the fit is part of the scientific question
- residual structure is not grossly misleading

Be careful when:
- there are clear nonlinearities
- the x-axis has strong measurement error
- points are repeated by subject/site and independence is violated
- a few leverage points drive the slope

Prefer alternatives:
- GAM / smoother
- robust regression
- mixed-effects model summaries
- grouped/faceted fits

### Boxplot / Violin + Significance Brackets

Reasonable when:
- a small number of preplanned comparisons exist
- the test aligns with the data structure
- sample size and variance structure justify the chosen test

Be careful when:
- there are many pairwise tests without correction
- users want stars but the effect size is tiny
- data are paired or nested but the test assumes independence
- outliers or ties dominate nonparametric rank tests

Prefer showing:
- raw points
- sample sizes
- effect size with interval
- adjusted p-values if multiple comparisons are made

### Bar Chart + Error Bars

Reasonable when:
- bars encode totals or proportions
- zero is the meaningful baseline
- summary estimates are truly the focus

Be careful when:
- the bars hide highly skewed or multimodal raw data
- the interval type is ambiguous (`SD`, `SE`, or `CI`)
- viewers may infer the wrong uncertainty meaning

Prefer:
- point-range
- box/violin + points
- paired plots for repeated measures

### Time Series + Trend Line

Reasonable when:
- time ordering matters
- the trend estimate is interpretable
- the autocorrelation structure is acknowledged if inferential claims are made

Be careful when:
- seasonality is present but ignored
- smoothing windows are arbitrary
- missing periods create false continuity

Prefer adding:
- uncertainty ribbon
- seasonal decomposition panel
- breakpoint markers if supported by analysis

### Heatmap + Cell-Wise Significance

Reasonable when:
- the matrix is small and the annotation density remains readable
- multiple testing is handled appropriately

Be careful when:
- hundreds of cells are each tested and starred
- effect size magnitude is overshadowed by binary significance

Prefer:
- masking non-significant cells
- annotating only key regions
- combining effect magnitude and interval summaries elsewhere

## Effect Size and Uncertainty

Whenever possible, show at least one of:
- mean difference
- median difference
- standardized effect size
- slope / coefficient
- odds ratio / hazard ratio
- confidence or credible interval

## Multiple Comparisons

If many hypotheses are displayed in one figure, consider:
- Holm correction
- Benjamini-Hochberg false discovery rate
- model-based simultaneous intervals

Do not annotate many pairwise tests as if each were independent one-off analyses.

## Environmental Science Notes

- Spatial data often violate independence; avoid naive pixel-wise or site-wise p-value overlays
- Repeated monitoring data often require mixed or hierarchical models
- Detection limits and censored values should be disclosed before plotting means and fits
- Units, transformations, and baseline/reference periods should always be explicit

## What to Annotate by Default

Default annotation priority:
1. unit-bearing axis labels
2. sample size or observation count when important
3. uncertainty intervals
4. effect estimate or slope
5. p-value or significance marker only if it materially helps interpretation
