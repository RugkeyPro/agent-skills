# Color Palettes — rk_plotter

## Species Colors (from `plot_config.py`)

```python
from plot_config import SPECIES_COLORS, SPECIES_ORDER

SPECIES_ORDER = ["Acropora", "Lobophora", "Scarus", "Cephalopholis"]
SPECIES_COLORS = {
    "Acropora":      "#E57373",   # coral red
    "Lobophora":     "#81C784",   # leaf green
    "Scarus":        "#64B5F6",   # sky blue
    "Cephalopholis": "#BA68C8",   # soft purple
}
```

## Region Colors

### SEM scripts (primary authoritative set)
```python
REGION_COLORS = {
    "Global":           "#2C3E50",   # dark slate
    "Caribbean":        "#E74C3C",   # red
    "GreatBarrierReef": "#27AE60",   # green
    "SoutheastAsia":    "#8E44AD",   # purple
}
```

### Alternative (used in some trend/time-series scripts)
```python
REGION_COLORS_ALT = {
    "Global":           "#9E9E9E",   # grey
    "Caribbean":        "#26A69A",   # teal
    "GreatBarrierReef": "#FFA726",   # amber
    "SoutheastAsia":    "#AB47BC",   # amethyst
}
```

## Scenario / Projection Colors

```python
SSP_COLORS = {
    "SSP245_shade": "#90CAF9",   # light blue
    "SSP245_line":  "#1565C0",   # dark blue
    "SSP585_shade": "#EF9A9A",   # light red
    "SSP585_line":  "#B71C1C",   # dark red
}
```

## MHW State Colors

```python
MHW_COLORS = {
    "low":  "#3498DB",   # blue
    "high": "#E74C3C",   # red
}
```

## SEM Path Colors

```python
SEM_PATH_COLORS = {
    "positive": "#3498DB",   # blue arrows
    "negative": "#E74C3C",   # red arrows
}
SEM_NODE_COLORS = {
    "mhw":  "#FFD3B6",   # warm orange fill
    "mp":   "#C8E7FA",   # cool blue fill
}
```

## Validation Plot Colors

```python
VAL_COLORS = {
    "model":    "#1f77b4",   # matplotlib default blue
    "observed": "#ff7f0e",   # matplotlib default orange
}
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
