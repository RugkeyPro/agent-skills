# Style Guide — rk_plotter

## Core Visual Principles

- Prioritize interpretation speed over ornament
- Keep visual hierarchy obvious: data first, guides second, annotations third
- Use the minimum number of encodings needed to communicate the result
- Prefer small multiples over overcrowded single panels
- Match the figure style to the output context: publication, report, slide, or supplementary material

## Recommended rcParams Baseline

Use as a default starting point when the repository does not already define plotting defaults.

| Property | Recommended value |
|----------|-------------------|
| Backend | `Agg` for scripts |
| Font family | `Arial`, `Helvetica`, `DejaVu Sans` fallback |
| `font.size` | 8–9 pt publication; 10–12 pt slides |
| `axes.labelsize` | 9–10 pt publication |
| `axes.titlesize` | 9–10 pt publication |
| `xtick.labelsize` | 7–8 pt publication |
| `ytick.labelsize` | 7–8 pt publication |
| `legend.fontsize` | 7–8 pt publication |
| `legend.frameon` | `False` unless legend overlaps complex data |
| `axes.spines.right` | `False` |
| `axes.spines.top` | `False` |
| `axes.linewidth` | `0.5`–`0.8` pt |
| `figure.dpi` | `300` |
| `savefig.dpi` | `600` |
| `savefig.transparent` | `True` for manuscript figures when acceptable |
| `pdf.fonttype` | `42` |
| `svg.fonttype` | `'none'` |

## Figure Size Presets

| Context | Recommended figsize |
|---------|----------------------|
| Single-panel publication | `(5, 4)` or `(6, 4)` |
| Wide comparison panel | `(7.2, 4)` |
| 2×2 multi-panel | `(7.2, 6.2)` |
| 1×4 strip of panels | `(12, 3.2)` to `(14, 3.8)` |
| Global map | `(8, 4.5)` to `(10, 5.5)` |
| Poster/presentation | scale up 1.3×–1.8× from publication default |

Journal heuristics:
- single-column width: ~85–90 mm
- double-column width: ~175–185 mm

## Typography Rules

- Use bold sparingly: panel labels, compact callouts, or short section titles
- Use italics only when scientifically required, such as Latin names or mathematical notation
- Keep axis labels descriptive and unit-bearing, e.g. `Concentration (mg L$^{-1}$)`
- Use sentence case for titles unless a journal style explicitly prefers title case

## Axes and Gridlines

- Remove top/right spines unless enclosing panels improves comparison
- Use light horizontal gridlines only when they aid reading precise values
- Start bars at zero unless a justified broken-axis pattern is clearly disclosed
- For log scales, label the base or communicate that the axis is logarithmic
- For temporal axes, avoid overcrowded tick labels; aggregate or rotate if needed

## Legends

- Prefer direct labeling when only 2–3 lines are present
- Use a shared legend for faceted or multi-panel plots when categories are consistent
- Keep legend order aligned with plotting order and scientific logic
- Avoid duplicating information already encoded in panel titles or axis labels

## Colorbars

```python
cbar = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
cbar.ax.tick_params(labelsize=7)
cbar.set_label("Label (unit)")
cbar.outline.set_linewidth(0.5)
```

Rules:
- Use one shared colorbar for comparable map panels
- Fix limits across comparable panels
- Label the physical meaning and units, not just the variable name

## Layout and Multi-Panel Figures

- Use aligned axes whenever direct comparison matters
- Reserve whitespace for legends, colorbars, and annotations rather than letting them overlap data
- Keep panel labels consistent: `(a)`, `(b)`, `(c)` at upper-left
- Use `GridSpec` when maps, marginal plots, or unequal panel widths are needed
- Prefer shared x/y limits when the purpose is comparison across panels

## Annotation Style

- Annotations should clarify a result, not restate the whole caption
- Keep annotation boxes compact and positioned away from dense data regions
- Use white backing or stroke effects only when text overlays complex raster or point clouds
- Report sample sizes when omission could mislead interpretation

## Export Rules

- Save vector output (`.svg`, optionally `.pdf`) for publication and editing
- Save `.png` at 600 dpi for quick sharing or manuscript upload systems
- Check for clipped labels, missing fonts, oversized file output, and rasterization artifacts
- Always close figures after export in script workflows
