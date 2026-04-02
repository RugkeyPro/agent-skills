---
name: rk_plotter
description: "Scientific plotting skill for marine ecology figures. Use when: creating matplotlib figures, plotting species distribution maps, time series, boxplots, heatmaps, SEM path diagrams, cartopy geographic maps, or any publication-quality scientific plot following GCB journal style. Triggers on: matplotlib, cartopy, seaborn, scientific figure, publication plot, species map, MHW boxplot, time series trend, correlation heatmap, SEM diagram, raster map, coexistence map, divergence map, centroid shift."
argument-hint: "Describe the plot type, data source, and output figure name"
---

# rk_plotter — Marine Ecology Scientific Plotting Skill

## When to Use
- Creating any new `plot_*.py` script in this project
- Generating matplotlib publication figures (maps, time series, boxplots, heatmaps, SEM diagrams)
- Asking how to style axes, save figures, or annotate statistics in this codebase
- Debugging figure layout or color conventions

## Core Rules (Non-Negotiable)

1. **Always** `import matplotlib; matplotlib.use('Agg')` BEFORE any other matplotlib import
2. **Always** `from plot_config import FIG_DIR, SPECIES_COLORS, SPECIES_ORDER, get_base_filename` and apply rcParams via that module (never re-define globally)
3. **Always** end every script with `plt.tight_layout()` → `fig.savefig(...)` → `plt.close(fig)`
4. **Always** save two formats: `.svg` + `.png` (600 dpi, transparent); add `.pdf` for main figures
5. **Never** use red-green color contrast, `jet`, or `rainbow` colormaps

---

## Procedure

### Step 1 — File Setup

```python
import matplotlib
matplotlib.use('Agg')           # MUST be first

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from pathlib import Path
from plot_config import FIG_DIR, SPECIES_COLORS, SPECIES_ORDER, get_base_filename
```

Add optional imports only when needed:
- Maps: `import cartopy.crs as ccrs; import cartopy.feature as cfeature`
- Seaborn: `import seaborn as sns` (trends, boxplots, heatmaps)
- Raster: `import rasterio`
- Stats: `from scipy import stats`
- Smooth: `from scipy.ndimage import gaussian_filter`
- Custom SEM shapes: `import matplotlib.patches as mpatches; import matplotlib.path as mpath`

### Step 2 — Data Loading

Use `pathlib` and `PROJECT_ROOT`-relative paths:
```python
PROJECT_ROOT = Path(__file__).resolve().parents[1]   # preferred
data_path = PROJECT_ROOT / "output" / "subfolder" / "file.csv"
df = pd.read_csv(data_path).dropna()
```

For rasters (GeoTIFF):
```python
import rasterio
with rasterio.open(tif_path) as src:
    arr = src.read(1).astype(np.float32)
    arr[arr == src.nodata] = np.nan
```

For batch files:
```python
import glob
files = glob.glob(str(PROJECT_ROOT / "validation" / "*.csv"))
```

Use `plot_data_helpers` functions when loading species spatial data:
- `load_annual_map(species, year, scope)` → `(array, extent)`
- `load_period_mean_map(species, years, scope)` → mean raster
- `compute_annual_or10_area_change(species, threshold, scope)` → area time series

### Step 3 — Figure Creation

Choose layout pattern:

| Plot type | Code pattern |
|-----------|-------------|
| Single panel | `fig, ax = plt.subplots(figsize=(6, 4))` |
| 1×N stats panels | `fig, axes = plt.subplots(1, N, figsize=(4*N, 4), sharey=False)` |
| Map with ratio | `gs = GridSpec(1, N, width_ratios=[...]); ax = fig.add_subplot(gs[i], projection=proj)` |
| SEM diagram | `fig, ax = plt.subplots(figsize=(6, 7))` |

**GCB column width targets**: single-column 88 mm (3.46"), double-column 183 mm (7.2")

### Step 4 — Axis Styling

rcParams from `plot_config.py` handle most defaults. Per-script overrides:
```python
sns.despine(ax=ax)                          # use in seaborn plots
ax.spines[['top','right']].set_visible(False)  # manual fallback

# Species italic labels
ax.set_xticklabels(
    [f"$\\it{{{sp}}}$" if sp != "Community" else sp for sp in SPECIES_ORDER],
    rotation=30, ha='right'
)

# Rotated region labels
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')
```

**Panel labels** (auto-generate a/b/c/d):
```python
for i, (ax, title) in enumerate(zip(axes, titles)):
    ax.set_title(f'({chr(97+i)}) {title}', loc='left', fontweight='bold')
```

### Step 5 — Statistical Annotations

See [stat-annotations reference](./references/stat-annotations.md) for full patterns.

**Significance stars** (universal mapping):
```python
def sig_label(p):
    if p < 0.001: return '***'
    if p < 0.01:  return '**'
    if p < 0.05:  return '*'
    if p < 0.1:   return '.'
    return 'ns'
```

**Bracket between two bars/boxes**:
```python
ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1, c='k')
ax.text((x1+x2)*0.5, y+h*1.02, sig_label(p), ha='center', va='bottom', fontweight='bold')
```

**Regression annotation box** (time series):
```python
ax.text(0.05, 0.05, f"Slope: {slope:+.2f}%/yr\nP < 0.001",
        transform=ax.transAxes, fontsize=8.5, fontweight='bold',
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))
```

**95% CI shaded band**:
```python
ax.fill_between(x, y_reg - conf, y_reg + conf, color=color, alpha=0.12)
```

### Step 6 — Colors

See [color-palettes reference](./references/color-palettes.md) for full palette tables.

Quick reference:
```python
from plot_config import SPECIES_COLORS   # Acropora red, Lobophora green, Scarus blue, Cephalopholis purple

REGION_COLORS = {
    "Global":         "#2C3E50",
    "Caribbean":      "#E74C3C",
    "GreatBarrierReef": "#27AE60",
    "SoutheastAsia":  "#8E44AD",
}
MHW_COLORS = {"low": "#3498DB", "high": "#E74C3C"}
SSP_COLORS = {"SSP245_lo": "#90CAF9", "SSP245_hi": "#1565C0",
              "SSP585_lo": "#EF9A9A", "SSP585_hi": "#B71C1C"}
```

**Colormaps**:
- Diverging difference maps → `RdBu_r` + `TwoSlopeNorm` or symmetric `vmin/vmax`
- Species richness / coexistence → `RdYlBu_r` (5-level discrete)
- Log-scale intensity → `magma_r` + `LogNorm`
- Sequential data → `viridis`, `cividis`, or `mako`

### Step 7 — Figure Saving

```python
base = get_base_filename(__file__)    # derives name from script filename

out_svg = FIG_DIR / f"{base}.svg"
out_png = FIG_DIR / f"{base}.png"
out_pdf = FIG_DIR / f"{base}.pdf"    # optional, for main figures

plt.tight_layout()
fig.savefig(out_svg, transparent=True)
fig.savefig(out_png, dpi=600, transparent=True, bbox_inches='tight')
fig.savefig(out_pdf, bbox_inches='tight')  # if needed
plt.close(fig)
print(f"Saved {out_png}")
```

For **explicit** naming (skip `get_base_filename`):
```python
fig.savefig(FIG_DIR / "fig4a_mrq_map.svg", transparent=True)
fig.savefig(FIG_DIR / "fig4a_mrq_map.png", dpi=600, transparent=True, bbox_inches='tight')
plt.close(fig)
```

---

## Plot-Type Quick References

| Plot type | Key imports | Reference script |
|-----------|------------|-----------------|
| Global/regional raster map | `cartopy`, `rasterio`, `TwoSlopeNorm` | `plot_fig4a_mrq_map.py` |
| Multi-species time series | `scipy.stats`, `fill_between` | `plot_fig4b_epop_trends.py`, `plot_area_time_series.py` |
| MHW grouped boxplots | `seaborn`, `sig brackets` | `plot_fig4c_mhw_boxplots.py` |
| Correlation heatmap | `seaborn`, `annotate cells` | `plot_fig4d_correlation_heatmap.py` |
| Scatter validation facets | `sns.FacetGrid`, OLS | `plot_fig6d.py` |
| SEM path diagram | `FancyArrowPatch`, `mpath` | `plot_sem_global_path.py` |
| SEM bar/synergy | `bar + yerr=1.96*sd` | `plot_sem_synergy_bars.py` |
| Coexistence raster map | `RdYlBu_r` discrete, `cartopy` | `plot_global_coexistence_map.py` |
| Centroid shift map | `GridSpec` width_ratios, arrows | `plot_centroid_shift_maps.py` |
| Spatial divergence map | `RdBu_r`, `TwoSlopeNorm` | `plot_spatial_divergence_maps.py` |

---

## Checklist Before Finishing

- [ ] `matplotlib.use('Agg')` is the FIRST matplotlib call
- [ ] `from plot_config import ...` brings in rcParams automatically
- [ ] All font sizes use rcParams defaults (no explicit fontsize overrides unless deliberately deviating)
- [ ] Top and right spines are removed
- [ ] Species names are italicized (except "Community")
- [ ] Files saved as SVG + PNG (600 dpi, transparent)
- [ ] `plt.close(fig)` is called at the end
- [ ] No `jet`, `rainbow`, or red-green contrast colormaps used
- [ ] Output path is inside `FIG_DIR`
