# Statistical Annotations — rk_plotter

Use annotation only when it improves interpretation. Favor short, consistent callouts over dense narrative text inside the panel.

## 1. Significance Label Mapping

```python
def sig_label(p: float) -> str:
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    if p < 0.1:
        return "."
    return "ns"
```

Use cautiously:
- good for a few preplanned comparisons
- poor substitute for effect size and interval reporting

## 2. Brackets for Boxplots or Bars

```python
def draw_sig_bracket(ax, x1, x2, y_top, h_gap, p):
    y = y_top + h_gap
    h = h_gap * 0.3
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=1, c="k")
    ax.text(
        (x1 + x2) * 0.5,
        y + h * 1.02,
        sig_label(p),
        ha="center",
        va="bottom",
        fontweight="bold",
    )
```

Guidelines:
- leave enough headroom above the tallest element
- avoid stacking many brackets into unreadable ladders
- report adjusted p-values in the caption if multiple comparisons were corrected

## 3. Point Estimate + Interval Labels

Useful for point-range, coefficient, and forest plots.

```python
label = f"{estimate:.2f} [{lower:.2f}, {upper:.2f}]"
ax.text(x_pos, y_pos, label, va="center")
```

Prefer this style when:
- the estimate itself matters more than star labels
- the audience needs exact interval values

## 4. Bar or Point Intervals

Always make the interval meaning explicit in code comments or caption text.

```python
ax.bar(
    x,
    mean_val,
    yerr=ci95,
    capsize=4,
    color=color,
    edgecolor="white",
    linewidth=0.5,
)
```

Common interval types:
- `SD`: variability of observations
- `SE`: precision of mean estimate
- `95% CI`: interval estimate for parameter
- posterior interval: Bayesian uncertainty summary

## 5. Regression Line + Confidence Ribbon

```python
from scipy import stats

slope, intercept, r, p, se = stats.linregress(x, y)
x_fit = np.linspace(x.min(), x.max(), 200)
y_fit = slope * x_fit + intercept
conf_95 = 1.96 * se * np.sqrt(
    1 / len(x) + (x_fit - x.mean()) ** 2 / np.sum((x - x.mean()) ** 2)
)

ax.plot(x_fit, y_fit, color=color, lw=1.2)
ax.fill_between(x_fit, y_fit - conf_95, y_fit + conf_95, color=color, alpha=0.12)
```

Annotate only the essentials:
- slope and units
- `R²` or correlation where relevant
- `P` if inferential emphasis is necessary

## 6. Compact Regression Annotation Box

```python
p_str = f"P = {p:.3f}" if p >= 0.001 else "P < 0.001"
annot = f"Slope = {slope:+.2f} unit/yr\nR² = {r**2:.2f}\n{p_str}"

ax.text(
    0.05,
    0.05,
    annot,
    transform=ax.transAxes,
    fontsize=8,
    bbox=dict(facecolor="white", alpha=0.8, edgecolor="none", pad=2),
)
```

Keep boxes:
- inside unused panel space
- short enough to scan instantly
- consistent across facets or repeated figures

## 7. Sample Size Annotation

Important when group sizes differ strongly or when small `n` affects interpretation.

```python
for xpos, n in zip(x_positions, sample_sizes):
    ax.text(xpos, y_base, f"n={n}", ha="center", va="top", fontsize=7)
```

## 8. Heatmap Annotation

### Numeric cell labels

```python
annot = corr_df.round(2)
sns.heatmap(corr_df, annot=annot, fmt=".2f", cmap="RdBu_r", center=0)
```

### Numeric + significance label

```python
def heatmap_annot(val: float, p: float, fmt: str = ".2f") -> str:
    star = ""
    if p < 0.001:
        star = "***"
    elif p < 0.01:
        star = "**"
    elif p < 0.05:
        star = "*"
    return f"{val:{fmt}}{star}"
```

Use only for small matrices. For larger matrices:
- annotate selected cells only
- mask one triangle
- move significance detail to the caption or supplement

## 9. Reference Lines and Thresholds

```python
ax.axhline(0, color="gray", linewidth=0.7, linestyle="--", zorder=0)
ax.axvline(threshold_x, color="gray", linewidth=0.7, linestyle=":")
```

Good use cases:
- zero-anomaly baseline
- regulatory threshold
- intervention date
- detection limit

## 10. Quantile or Median Labels

```python
median_val = np.median(values)
ax.text(
    0.98,
    0.95,
    f"Median = {median_val:.2f}",
    transform=ax.transAxes,
    ha="right",
    va="top",
)
```

Use for skewed environmental data when mean would mislead.

## 11. Facet-Level Callouts

Useful for grouped scatter or repeated panels.

```python
annot = f"n={n}\nSlope={slope:.2f}\nP={p:.3f}"
ax.text(
    0.03,
    0.97,
    annot,
    transform=ax.transAxes,
    va="top",
    fontsize=7,
    bbox=dict(boxstyle="round,pad=0.25", facecolor="white", alpha=0.8),
)
```

Facet annotations should:
- use identical format across panels
- avoid changing box size drastically panel to panel
- not replace a shared legend when one is clearer

## 12. Map Labels and Spatial Callouts

### White-outline map text

```python
import matplotlib.patheffects as pe

ax.text(
    lon,
    lat,
    "Site A",
    fontsize=7,
    ha="center",
    va="center",
    path_effects=[pe.withStroke(linewidth=1.5, foreground="white")],
)
```

### Arrow or shift annotation

```python
ax.annotate(
    "",
    xy=(lon2, lat2),
    xytext=(lon1, lat1),
    xycoords=ccrs.PlateCarree()._as_mpl_transform(ax),
    textcoords=ccrs.PlateCarree()._as_mpl_transform(ax),
    arrowprops=dict(arrowstyle="->", color=color, lw=1.5),
)
```

## 13. What to Annotate First

Default priority order:
1. axis labels with units
2. legend/colorbar labels
3. uncertainty intervals
4. sample size when necessary
5. effect estimate or slope
6. p-value/significance marker only if still useful

## 14. What to Avoid

- paragraphs of text inside panels
- too many significance brackets
- overlapping labels without collision control
- `P = 0.000`
- unexplained acronyms in annotation boxes
- interval bars without stating what interval they represent
