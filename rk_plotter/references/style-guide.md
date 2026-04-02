# Style Guide — rk_plotter

## Global rcParams (set by `plot_config.py`)

| Property | Value |
|----------|-------|
| Backend | `Agg` (headless) |
| Font family | `Arial`, `Helvetica` (sans-serif) |
| `font.size` | 8 pt |
| `axes.labelsize` | 9 pt |
| `xtick.labelsize` | 7 pt |
| `ytick.labelsize` | 7 pt |
| `legend.fontsize` | 7 pt |
| `legend.frameon` | False |
| `axes.spines.right` | False |
| `axes.spines.top` | False |
| `axes.linewidth` | 0.5 pt |
| `figure.dpi` | 300 |
| `savefig.dpi` | 600 |
| `savefig.transparent` | True |
| `pdf.fonttype` | 42 (embedded, Illustrator-editable) |
| `svg.fonttype` | `'none'` (text as text, not paths) |

## Typical Figure Sizes

| Category | figsize (inches) |
|----------|-----------------|
| Single-panel stats | `(5, 4)`, `(6, 4)`, `(6, 4.5)`, `(6, 5)`, `(6.5, 4.5)` |
| Multi-panel 1×4 stats | `(15, 3.5)`, `(16, 4.5)` |
| Multi-panel 1×5 stats | `(20, 4)`, `(20, 5)` |
| Global map | `(12, 7)`, `(10, 5)` |
| SEM path diagram | `(6, 7)` |
| GCB single-column | 88 mm ≈ 3.46" |
| GCB double-column | 183 mm ≈ 7.2" |

## Line and Marker Widths

| Element | Width |
|---------|-------|
| Axis spines | 0.5 pt |
| Data lines (time series) | 1.0–1.5 pt |
| Error/grid lines | 0.6–0.8 pt |
| Significance bracket | 1 pt, black |
| SEM arrow | 2–4 pt (varies by coefficient magnitude) |
| Map coastline | 0.5–0.8 pt |

## Font Rules

All text uses **Arial** (fallback: Helvetica). Three weights/styles only:

| Style | When to use | matplotlib parameter |
|-------|-------------|---------------------|
| **Bold** | Panel labels `(a) Title`; key stats in annotation boxes; figure titles | `fontweight='bold'` |
| Regular | Axis labels, tick labels, legend entries, colorbar labels, body annotations | *(default)* |
| *Italic* | Genus/species Latin names in any label or title | `fontstyle='italic'` or `$\it{Name}$` |

Rules:
- **Bold**: panel labels, significance stars inside brackets, dominant numbers in callouts
- **Regular**: all axes labels (`ax.set_xlabel/ylabel`), tick labels, legend text, colorbar label, general annotation text
- **Italic**: Latin binomials only (e.g. *Acropora*, *Symbiodinium*); common names and non-Latin terms stay roman
- Avoid mixing bold + italic unless a species name appears inside a bold panel label

```python
# Panel label (bold)
ax.set_title(f'({chr(97+i)}) Title', loc='left', fontweight='bold')

# Species name italic in tick label
ax.set_xticklabels([f'$\\it{{{sp}}}$' for sp in species_list])

# Annotation box (regular text, bold value)
ax.text(0.05, 0.05, f"Slope: {slope:+.2f}%/yr",
        transform=ax.transAxes, fontsize=8.5, fontweight='bold',
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))
```

## Spines Convention

```python
# Inherited from rcParams (preferred):
# axes.spines.right: False
# axes.spines.top: False

# Manual override when needed:
ax.spines[['top', 'right']].set_visible(False)

# Seaborn plots:
sns.despine(ax=ax)
```

## Colorbar Style

```python
cbar = fig.colorbar(im, ax=ax, shrink=0.7, pad=0.02)
cbar.ax.tick_params(labelsize=7)
cbar.set_label("Label (unit)", fontsize=8)
cbar.outline.set_linewidth(0.5)
```

## Map Style (Cartopy)

```python
import cartopy.crs as ccrs
import cartopy.feature as cfeature

proj = ccrs.PlateCarree()
ax = fig.add_subplot(gs[i], projection=proj)
ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND, facecolor='#f0f0f0', zorder=1)
ax.add_feature(cfeature.COASTLINE, linewidth=0.5, zorder=2)
ax.add_feature(cfeature.BORDERS, linewidth=0.3, linestyle=':', zorder=2)
ax.gridlines(draw_labels=True, linewidth=0.3, color='gray', alpha=0.5,
             xlocs=range(-180, 181, 30), ylocs=range(-90, 91, 15))
```

For width-ratio multi-panel maps:
```python
from matplotlib.gridspec import GridSpec
ratios = [(lon_max-lon_min) for lon_min, lon_max in extents]
gs = GridSpec(1, N, width_ratios=ratios, wspace=0.05)
```

## White-outline Map Text

```python
import matplotlib.patheffects as pe
ax.text(lon, lat, "Label",
        fontsize=7, ha='center', va='center',
        path_effects=[pe.withStroke(linewidth=1.5, foreground='white')])
```
