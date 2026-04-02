# Color Palettes — rk_plotter

## Recommended Qualitative Palettes (Categorical Groups)

Use for distinguishing N discrete categories (species, regions, treatments, scenarios, etc.).

| Palette | N | Hex values | Notes |
|---------|---|-----------|-------|
| **Tol Bright** | 6 | `#4477AA` `#EE6677` `#228833` `#CCBB44` `#66CCEE` `#AA3377` | Paul Tol's colorblind-safe set; recommended first choice |
| **Tol Muted** | 10 | `#332288` `#88CCEE` `#44AA99` `#117733` `#999933` `#DDCC77` `#CC6677` `#882255` `#AA4499` `#DDDDDD` | Larger categorical set, still colorblind-safe |
| **Okabe-Ito** | 8 | `#E69F00` `#56B4E9` `#009E73` `#F0E442` `#0072B2` `#D55E00` `#CC79A7` `#000000` | ISO/IEEE recommended; excellent for print & screen |
| **D3 Category10** | 10 | matplotlib `tab10` | Familiar default; avoid for >6 groups |
| **Pastel accents** | 4–6 | `#AEC6CF` `#FFD1DC` `#B5EAD7` `#FFDAC1` | Low-saturation; good for filled areas / node backgrounds |

```python
# Example: pick N colors from Tol Bright
TOL_BRIGHT = ["#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377"]
colors = TOL_BRIGHT[:N]
```

## Recommended Diverging Palettes

Use when data spans a meaningful midpoint (0, baseline, reference year).

| Palette | Use case | Notes |
|---------|----------|-------|
| `RdBu_r` | Change / anomaly / difference | Classic, high contrast |
| `RdYlBu_r` | Graded divergence with neutral mid | Softer; good for richness or gradient |
| `coolwarm` | Symmetric positive/negative | Perceptually uniform diverging |
| `PuOr` | Two-categorical contrast | Purple–orange, colorblind-safe |
| `BrBG` | Environmental index (wet/dry, warm/cold) | Earthy tones |

Always pair with `TwoSlopeNorm` or symmetric `vmin=-vmax`:
```python
from matplotlib.colors import TwoSlopeNorm
vmax = np.nanpercentile(np.abs(arr), 95)
norm = TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
im = ax.imshow(arr, cmap='RdBu_r', norm=norm)
```

## Recommended Sequential Palettes

Use for single-direction continuous data (density, probability, intensity).

| Palette | Best for | Notes |
|---------|----------|-------|
| `viridis` | General-purpose sequential | Perceptually uniform, colorblind-safe |
| `plasma` | High-dynamic-range data | More vibrant than viridis |
| `mako` | Cool-toned density/probability | From seaborn; elegant for scientific use |
| `cividis` | Print-safe sequential | Optimized for deuteranopia |
| `YlOrRd` | Heat / risk / intensity | Intuitive warm ramp |
| `Blues` / `Greens` | Single-variable spatial | Clean, minimal |

```python
# Log-scale intensity
from matplotlib.colors import LogNorm
norm = LogNorm(vmin=np.nanpercentile(arr[arr>0], 5),
               vmax=np.nanpercentile(arr[arr>0], 95))
im = ax.imshow(arr, cmap='mako', norm=norm)
```

## Discrete / Classified Maps

Use `BoundaryNorm` + a diverging or qualitative colormap for N-class rasters:
```python
from matplotlib.colors import BoundaryNorm
bounds = list(range(N + 1))           # e.g. [0, 1, 2, 3, 4, 5]
cmap   = plt.cm.get_cmap('RdYlBu_r', N)
norm   = BoundaryNorm(bounds, cmap.N)
im = ax.imshow(class_arr, cmap=cmap, norm=norm)
```

## Colormaps

| Use case | Colormap | Notes |
|----------|----------|-------|
| Diverging difference (SSP/trend) | `RdBu_r` | Pair with `TwoSlopeNorm` or symmetric `vmin=-vmax` |
| Species richness / coexistence | `RdYlBu_r` | 5-level discrete: `BoundaryNorm([0,1,2,3,4,5], 5)` |
| Log-scale intensity (mRQ, density) | `magma_r` | Pair with `LogNorm(vmin=..., vmax=...)` |
| Sequential continuous | `viridis`, `cividis`, `mako` | Safe for colorblind |

### Diverging map with `TwoSlopeNorm`
```python
from matplotlib.colors import TwoSlopeNorm
vmax = np.nanpercentile(np.abs(diff_arr), 95)
norm  = TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
im = ax.imshow(diff_arr, cmap='RdBu_r', norm=norm, ...)
```

### 5-level discrete coexistence map
```python
from matplotlib.colors import BoundaryNorm
bounds = [0, 1, 2, 3, 4, 5]
cmap   = plt.cm.get_cmap('RdYlBu_r', 5)
norm   = BoundaryNorm(bounds, cmap.N)
im = ax.imshow(richness_arr, cmap=cmap, norm=norm, ...)
```

### Log-scale raster
```python
from matplotlib.colors import LogNorm
norm = LogNorm(vmin=np.nanpercentile(arr[arr > 0], 5),
               vmax=np.nanpercentile(arr[arr > 0], 95))
im = ax.imshow(arr, cmap='magma_r', norm=norm, ...)
```

## Forbidden Colormaps

`jet`, `rainbow`, `hsv`, `gist_rainbow` — never use these.
Avoid explicit red-green pairings (colorblind inaccessible).
