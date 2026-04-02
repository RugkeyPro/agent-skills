# Plot Selection Guide — rk_plotter

Choose the figure from the scientific question, not from habit.

## Start with the Question Type

| Scientific question | Recommended plots | Avoid when possible |
|---------------------|------------------|---------------------|
| Are groups different? | boxplot, violin, raincloud, point-range | bar-only summaries hiding distribution |
| Is there a temporal trend? | line, ribbon, seasonal facets | disconnected bars for continuous time |
| Are two variables related? | scatter, hexbin, density contour, regression panel | raw scatter when severe overplotting hides structure |
| What is the composition of a whole? | stacked bar, normalized stacked bar, area chart | pie charts for many groups |
| What is the distribution shape? | histogram, KDE, ECDF, ridgeline | bar charts of binned values without labeling |
| What is the spatial pattern? | raster map, choropleth, station map, contours | 3D surfaces unless analytically necessary |
| What are model coefficients/effects? | coefficient plot, marginal effect plot, forest plot | tables only when comparison is visual |
| How do many variables covary? | heatmap, clustered heatmap, pair plot | giant unreadable scatter matrices |

## Fast Decision Heuristics

### If you need to compare groups
- Use **boxplot + strip/swarm** when sample sizes are moderate and raw spread matters
- Use **violin + points** when shape matters and `n` is not tiny
- Use **point-range** when only summary estimates and intervals should be emphasized
- Use **stacked bar** only when the message is composition, not group mean difference

### If you need to show trends
- Use **line + confidence ribbon** for continuous time or ordered sequences
- Use **small multiples** when many groups would otherwise crowd one axis
- Use **rolling summaries** only if smoothing is scientifically justified and disclosed

### If you need to show relationships
- Use **scatter + fit** for moderate sample sizes
- Use **hexbin** or **2D density** for thousands of points
- Use **faceting** when subgroup differences matter more than pooled fit

### If you need to show space/environment
- Use **raster maps** for gridded surfaces
- Use **choropleths** for polygon-aggregated statistics
- Use **station maps** or **bubble maps** for point observations
- Use **transect/depth section plots** for oceanographic or atmospheric gradients

## Environmental Science-Specific Guidance

Common tasks and good defaults:

| Task | Good default |
|------|--------------|
| Pollutant concentration across sites | boxplot/violin + points |
| Time trend of climate or water-quality index | line + uncertainty ribbon |
| Land-use composition by watershed | stacked bar or normalized stacked bar |
| Correlation among environmental drivers | clustered heatmap |
| Species-environment relationship | scatter + fit / GAM smooth |
| Spatial anomaly relative to baseline | diverging raster map |
| Monitoring station comparison over time | faceted line plots |
| Model coefficient comparison | coefficient plot |

## When to Replace a Bar Chart

Replace bars with another plot when:
- raw observations matter
- the distribution is skewed
- zero is not a meaningful anchor
- uncertainty is more important than central value
- there are few observations and each point should be visible

Better replacements:
- boxplot
- violin
- strip/swarm
- point-range
- estimation plot

## Anti-Patterns

- Pie charts with many slices
- 3D bars or 3D surfaces for 2D data
- Dual y-axes for unrelated variables
- Stacked area charts when exact comparisons are the goal
- Maps with many unrelated encodings at once
- Correlation heatmaps annotated so densely they become unreadable
