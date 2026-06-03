# Edit Boundary: Modification Constraints

This document defines what code modifications are permitted and what structures must remain locked when creating, refactoring, or optimizing scientific plots.

---

## Allowed Modifications & Controlled Extensions
The LLM is encouraged to modify parameters and add necessary structural components to adapt templates to the user's scientific query, as long as they stay within the template's style system.

### 1. Style & Config Parameters (`STYLE_CONFIG`, `TEXT_CONFIG`)
- **Data Path & Columns**: Customize `load_data()` path and `FIELD_MAP` variables.
- **Axes Text & Labels**: Titles, coordinate labels, legend texts, and units.
- **Style Customizations**: Figure size (`figsize`), font sizes, marker sizes, line widths, and specific color palette overrides mapping to semantic values.
- **Export Formats**: Basename, formats, and export DPIs.

### 2. Controlled Structure Extensions (受控结构扩展)
**"不改变图形基本形式，不等于不能添加元素。"** If the scientific data demands it, the LLM is explicitly allowed to add the following elements on top of the template motherboard:
- **Secondary Y/X Axes (同类轴)**: Add a secondary axis using `ax.twinx()` or `ax.twiny()` to overlay a second related variable of the same chart type (e.g. secondary line or scatter series).
- **Extra Series (系列)**: Add more lines, bars, or scatter series to display additional comparison groups.
- **Error Indicators (误差线/带)**: Add error bars (`ax.errorbar()`) or semi-transparent uncertainty shading/envelopes (using `ax.fill_between()`).
- **Reference lines (参考线)**: Add horizontal/vertical threshold or mean lines using `ax.axhline()`, `ax.axvline()`, or a diagonal 1:1 guideline.
- **Inset Subplots (局部放大图)**: Add local inset subplots using `ax.inset_axes()` to detail or zoom in on high-density regions.

---

## Forbidden Modifications
Unless the user explicitly requests otherwise, the LLM **must not** modify the following core structural features:

1. **Fundamental Graph Type Conversion**: Do not turn a scatter plot into a line plot, a violin plot into a bar chart, or a stacked bar into a grouped bar.
2. **Axis Meanings**: Do not swap variables across axes (e.g., swapping x and y in a prediction diagnostic plot) or change their physical meaning.
3. **Overall Layout Frame**: Do not change the overall multi-panel grid layout. A dual-panel template must remain a dual-panel layout, though each panel can be expanded with the allowed elements above.
4. **Statistical Methods**: Do not change how regressions, metrics, or distributions are calculated (e.g. do not change a linear regression fit to a polynomial fit unless asked).
5. **Single-Format Export**: Do not omit `svg` or `pdf` outputs. Publication-quality requires vector exports.
