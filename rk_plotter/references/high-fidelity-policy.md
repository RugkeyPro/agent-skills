# High-Fidelity Template Policy

`templates/` are high-fidelity visual masters derived from
`assets/original-scripts/` and `assets/new-scripts/`, not generic plotting recipes.
Both asset folders have equal priority. If a template and a source asset disagree,
preserve the source asset's visual grammar unless the user explicitly chooses another
option.

## Required pre-plot questions

Before generating a figure, ask the user to choose from concrete candidates based on the
nearest template. Do not silently decide these visual details:

- Figure type: bar, stacked bar, raster map, choropleth map, proportional-symbol map,
  box/violin/raincloud, time series, model diagnostic scatter, KDE/histogram, SHAP/PCA,
  profile/response curve, framework diagram, or multipanel figure.
- Source template: list the closest `templates/*.py` file and the asset script(s) it
  inherits from.
- Color plan: offer the original palette from the source asset plus scientifically
  appropriate alternatives such as sequential blue, green-yellow-red hotspot, diverging
  blue-red, categorical colorblind-safe, and log-scale risk palettes.
- Legend/colorbar plan: offer patch legend, symbol-size legend, categorical legend,
  horizontal colorbar, vertical colorbar, inset colorbar, and combined legends when the
  template supports them.
- Map-specific choices: projection, central longitude, lon/lat extent, land/ocean
  colors, layer order, coastlines/borders/province boundaries, gridline/tick labels,
  inset map, contour overlay, quiver arrows, and significant/hotspot mask overlays.
- Statistical/display choices: significance symbols, confidence intervals, error bars,
  fitted lines, reference lines, panel labels, and whether values should be annotated.

The user may combine compatible choices, for example using the default log-raster map
projection with the hotspot color palette and a horizontal colorbar. Reject combinations
only when they would break the source template's scientific meaning or visual grammar.

## Fixed output contract

All templates must use a single-column canvas by default, usually near `(3.5, 2.0)` to
`(3.5, 3.3)` inches depending on the original aspect ratio. All templates must export
`png`, `pdf`, and `svg`. Text must remain editable in Adobe Illustrator:

```python
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})
```

Use Arial as the default font even when the source asset used another family. Replace
asset demo data with clearer synthetic demo data, but keep the source asset's projection,
layer order, colorbar/legend structure, line weights, alpha values, and map extent unless
the user chooses an alternative.
