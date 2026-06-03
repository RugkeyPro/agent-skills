# Style Contract: Aesthetic & Layout Specifications

This document defines the core aesthetic specifications that all generated scientific plots must conform to.

---

## 1. Typography & Fonts

### Matplotlib Configurations
All scripts must explicitly configure `rcParams` to ensure cross-platform compatibility and vector font preservation:

```python
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans", "Helvetica", "Microsoft YaHei"],
    "svg.fonttype": "none",   # CRITICAL: Ensures text is stored as editable vector font, not path outlines
    "pdf.fonttype": 42,       # CRITICAL: Embeds TrueType fonts in PDF files
    "ps.fonttype": 42,
    "axes.spines.top": False,  # Hide top spine for clean look
    "axes.spines.right": False # Hide right spine
})
```

### Multilingual Support (Chinese Fonts)
For plots containing Chinese text, modify the font parameters to prioritize Microsoft YaHei and ensure minus signs render correctly:
```python
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False  # Avoid box characters for negative numbers
```

### Font Size Scales
Relative font sizes should be configured as follows:
- **Global / Tick labels**: 7.5 pt - 8.5 pt.
- **Axes Labels / Legends**: 8.5 pt - 9.0 pt.
- **Titles / Panel Labels**: 9.5 pt - 10.5 pt (bold).

---

## 2. Canvas Dimensions

Scientific figures must fit standard journal page columns. Ensure the `figsize` is specified in **inches**:

| Figure Layout | Target Width | Typical Height | Recommended Figsize |
|---|---|---|---|
| Single-column | 3.5 inches | 3.0 - 3.5 inches | `(3.5, 3.2)` |
| Dual-column | 7.2 inches | 4.0 - 4.5 inches | `(7.2, 4.0)` |
| Multi-panel grid | 7.2 - 8.5 inches| 5.0 - 6.5 inches | `(7.2, 5.5)` |
| Square panels | - | - | `(3.7, 3.7)` |

---

## 3. Color Palettes

Do not use high-saturation raw primary colors (e.g. pure red `#FF0000` or pure green `#00FF00`). Colors must serve scientific and semantic purposes:

1. **Standard Color Cycle (Okabe-Ito Color Universal Design)**:
   Use colorblind-safe, high-contrast colors for categorical variables:
   `["#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377", "#BBBBBB"]`
2. **Time Series Scenarios**:
   Use distinct scenario colors (e.g., SSP/RCP pathways):
   `["#1B9E77", "#D95F02", "#7570B3", "#E7298A", "#66A61E", "#E6AB02"]`
3. **Semantic Meanings**:
   - **Baseline / Historical**: Slate grey (`#888888` or `#bbbbbb`).
   - **Positive Change / Gains**: Forest green or deep blue (`#228833` or `#4477AA`).
   - **Negative Change / Loss**: Crimson or reddish orange (`#EE6677` or `#D95F02`).
   - **Confidence Intervals**: Semi-transparent versions of line colors (e.g. `alpha=0.15`).

---

## 4. Layout & Details

- **Margins**: Use `bbox_inches="tight"` during export to automatically remove unnecessary white space.
- **Grid Lines**: Use light grid lines behind data points:
  `ax.grid(True, color="#F0F0F0", linestyle="-", linewidth=0.6, zorder=0)`
  `ax.set_axisbelow(True)`
- **Colorbars**: Place on the right of maps or raster plots, matching panel heights:
  `fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)`

---

## 5. Output Specifications

All plotting scripts must save outputs in three standard formats:
1. **SVG**: For vector graphics scaling and vector editing (illustrator, Inkscape).
2. **PDF**: For vector embedding in document editors.
3. **PNG**: High-resolution raster preview (DPI **600** required).
