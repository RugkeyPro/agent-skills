# Color Palettes — rk_plotter

## Palette Selection Principles

- Use color to encode data meaning, not decoration
- Prefer colorblind-safe palettes for categorical comparisons
- Prefer perceptually uniform sequential palettes for magnitude
- Prefer diverging palettes only when a meaningful midpoint exists
- Confirm grayscale readability when figures may be printed

## Qualitative Palettes

Use for species, treatments, regions, scenarios, categories, or model groups.

| Palette | N | Hex values | Notes |
|---------|---|-----------|-------|
| **Okabe-Ito** | 8 | `#E69F00` `#56B4E9` `#009E73` `#F0E442` `#0072B2` `#D55E00` `#CC79A7` `#000000` | Reliable first choice |
| **Tol Bright** | 6 | `#4477AA` `#EE6677` `#228833` `#CCBB44` `#66CCEE` `#AA3377` | High clarity, publication-safe |
| **Tol Muted** | 10 | `#332288` `#88CCEE` `#44AA99` `#117733` `#999933` `#DDCC77` `#CC6677` `#882255` `#AA4499` `#DDDDDD` | Good larger categorical set |
| **Matplotlib `tab10`** | 10 | built-in | Acceptable, but less refined for dense print figures |
| **Pastel fill set** | 4–6 | `#AEC6CF` `#FFD1DC` `#B5EAD7` `#FFDAC1` `#C7CEEA` | Good for fills beneath darker outlines |

## Sequential Palettes

Use for concentration, abundance, probability, risk, elevation, anomaly magnitude without sign, or uncertainty width.

| Palette | Best for | Notes |
|---------|----------|-------|
| `viridis` | general continuous magnitude | default first choice |
| `cividis` | print-friendly / deuteranopia-safe | slightly lower chroma |
| `mako` | cool-toned scientific maps | elegant seaborn option |
| `plasma` | high dynamic range | more vivid, use carefully |
| `YlOrRd` | heat / hazard / exposure | intuitive warm ramp |
| `Blues`, `Greens` | single-domain spatial maps | simple and readable |

## Diverging Palettes

Use only when values differ around a reference such as zero, baseline, climatology, control, or target.

| Palette | Use case | Notes |
|---------|----------|-------|
| `RdBu_r` | anomaly / difference / residual | strong contrast |
| `coolwarm` | symmetric signed effect | balanced but softer |
| `PuOr` | two-sided comparison | colorblind-friendlier than many red-blue sets |
| `BrBG` | environmental wet/dry or gain/loss | earthy tones |
| `RdYlBu_r` | midpoint-centered gradients | useful but watch yellow in print |

Always pair with explicit normalization:

```python
from matplotlib.colors import TwoSlopeNorm

vmax = np.nanpercentile(np.abs(arr), 95)
norm = TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
```

## Cyclic Palettes

Use for phase, direction, day-of-year on a circular axis, or aspect/orientation.

Recommended:
- `twilight`
- `twilight_shifted`
- `hsv` only if no better cyclic option is available and the use case is explicitly cyclic

## Discrete / Classified Maps

Use `BoundaryNorm` for classed rasters, thresholds, or management categories.

```python
from matplotlib.colors import BoundaryNorm

bounds = [0, 5, 10, 20, 40, 80]
cmap = plt.cm.get_cmap("YlOrRd", len(bounds) - 1)
norm = BoundaryNorm(bounds, cmap.N)
```

## Encoding Advice by Plot Type

- Scatter groups: saturated edge/marker colors; low-alpha points when many observations
- Box/violin: neutral fill + colored points if the distribution shape should not dominate
- Heatmap: keep the scale interpretable and show a labeled colorbar
- Stacked bars: use ordered, distinct categories with enough luminance separation
- Maps: do not overload geography with too many discrete hues

## Grayscale and Accessibility Checks

- Check whether adjacent categories differ in lightness, not only hue
- For >6 categories, combine color with marker or linestyle differences
- Avoid red-green as the sole contrast
- Use dark outlines when light fills abut white backgrounds

## Forbidden or High-Risk Choices

Never use:
- `jet`
- `rainbow`
- `gist_rainbow`
- unlabeled custom gradients with non-monotonic luminance

Use with caution:
- saturated neon palettes for publication
- many-category stacked bars with similar hues
- diverging colormaps when the midpoint has no scientific meaning
