# Statistical Annotations — rk_plotter

## Significance Level Mapping

```python
def sig_label(p: float) -> str:
    """Map p-value to significance marker string."""
    if p < 0.001: return '***'
    if p < 0.01:  return '**'
    if p < 0.05:  return '*'
    if p < 0.1:   return '.'
    return 'ns'
```

## Significance Bracket (Boxplot / Bar)

Draws a horizontal bracket with a significance label between two positions:

```python
def draw_sig_bracket(ax, x1, x2, y_top, h_gap, p):
    """
    x1, x2   : x-positions of the two groups
    y_top    : top of the taller box/bar
    h_gap    : extra vertical gap above y_top for the bracket
    p        : p-value
    """
    y  = y_top + h_gap
    h  = h_gap * 0.3
    ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1, c='k')
    ax.text((x1+x2)*0.5, y+h*1.02,
            sig_label(p), ha='center', va='bottom', fontweight='bold', fontsize=8)
```

## Error Bars (95% CI = 1.96 × SD)

```python
ax.bar(x, mean_val, yerr=1.96 * sd_val, capsize=4,
       color=color, edgecolor='white', linewidth=0.5)
```

## OLS Regression Line + Confidence Interval

```python
from scipy import stats

slope, intercept, r, p, se = stats.linregress(x, y)
x_fit   = np.linspace(x.min(), x.max(), 200)
y_fit   = slope * x_fit + intercept
conf_95 = 1.96 * se * np.sqrt(1/len(x) + (x_fit - x.mean())**2 / np.sum((x - x.mean())**2))

ax.plot(x_fit, y_fit, color=color, lw=1.2)
ax.fill_between(x_fit, y_fit - conf_95, y_fit + conf_95, color=color, alpha=0.12)
```

## Regression Annotation Box (Time Series)

```python
p_str = f"P = {p:.3f}" if p >= 0.001 else "P < 0.001"
ax.text(0.05, 0.05,
        f"Slope: {slope:+.2f}%/yr\n{p_str}",
        transform=ax.transAxes, fontsize=8.5, fontweight='bold',
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))
```

## Inline Facet Annotation Box (Scatter / Validation)

```python
r2   = r**2
annot = f"R²={r2:.2f}\nSlope={slope:.2f}\n{p_str}"
ax.text(0.05, 0.95, annot,
        transform=ax.transAxes, va='top', fontsize=7,
        bbox=dict(boxstyle='round,pad=0.3', edgecolor='gray',
                  facecolor='white', alpha=0.8))
```

## Heatmap Cell Significance Star

Append a star to the cell text based on p-value:

```python
def heatmap_annot(val: float, p: float, fmt: str = ".2f") -> str:
    star = '' if p >= 0.05 else ('*' if p < 0.05 else '')
    if p < 0.001: star = '***'
    elif p < 0.01:  star = '**'
    elif p < 0.05:  star = '*'
    return f"{val:{fmt}}{star}"
```

Example usage in seaborn heatmap:
```python
annot_df = pd.DataFrame(
    [[heatmap_annot(corr_df.loc[r,c], pval_df.loc[r,c])
      for c in corr_df.columns] for r in corr_df.index],
    index=corr_df.index, columns=corr_df.columns
)
sns.heatmap(corr_df, annot=annot_df, fmt='', ...)
```

## Horizontal Reference Line

```python
ax.axhline(0, color='gray', linewidth=0.7, linestyle='--', zorder=0)
```

## Map Centroid Shift Arrow

```python
ax.annotate('', xy=(lon2, lat2), xytext=(lon1, lat1),
            xycoords=ccrs.PlateCarree()._as_mpl_transform(ax),
            textcoords=ccrs.PlateCarree()._as_mpl_transform(ax),
            arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
```
