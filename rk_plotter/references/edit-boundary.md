# Edit Boundary: Modification Constraints

This document defines what code modifications are permitted and what structures must remain locked when creating, refactoring, or optimizing scientific plots.

---

## Allowed Modifications
The LLM is encouraged to modify the following parameters to adapt templates to the user's data and requirements:

1. **Data loading path**: Change the path in `load_data()` or `main()` to point to the user's actual data files.
2. **Field mapping (`FIELD_MAP`)**: Bind template variable keys to the user's actual DataFrame column names.
3. **Axes Labels & Text (`TEXT_CONFIG`)**:
   - Title, subtitle, and coordinates labels.
   - Units (e.g. converting `y_label: "value"` to `y_label: "Concentration (mg/L)"`).
   - Legend titles and label overrides.
   - Text boxes, mathematical annotations, and statistics text.
4. **Style Parameters (`STYLE_CONFIG`)**:
   - Canvas size (`figsize`) to fit single-column (3.5 in) or double-column (7.2 in) page constraints.
   - Global font size (must keep labels, ticks, and titles scaled proportionally).
   - Marker size, line thickness, alpha transparency, and spine visibilities.
   - Color palettes: Modify color hex codes to match specific semantic colors (e.g. assigning red to "high emissions" and blue to "low emissions").
5. **Export Configs (`EXPORT_CONFIG`)**: Output path, file naming stems, formats (`png`, `pdf`, `svg`), and PNG DPI limits.

---

## Forbidden Modifications
Unless the user explicitly requests otherwise, the LLM **must not** modify the following core features:

1. **Graph Type Conversion**: Do not turn a scatter plot into a line plot, a violin plot into a bar chart, or a stacked bar into a grouped bar.
2. **Axis Meanings**: Do not swap variables across axes (e.g., swapping x and y in a prediction diagnostic plot).
3. **Panel Count & Layout**: Do not add or remove panels in multi-panel figures. A dual-panel template must remain dual-panel.
4. **Statistical Methods**: Do not change how regressions, metrics, or distributions are calculated (e.g. do not change a linear regression fit to a polynomial fit unless asked).
5. **Deletions of Essential Visual Elements**:
   - Do not remove legend boxes or colorbar tracks.
   - Do not remove 1:1 reference lines or regression bands.
   - Do not remove statistical text boxes or error intervals.
6. **Hardcoded guess rules**: Do not bypass `FIELD_MAP` and guess columns by integer index (e.g., `df.iloc[:, 0]`) unless the data has no column headers. Always use `FIELD_MAP` for explicit variable binding.
7. **Single-Format Export**: Do not omit `svg` or `pdf` outputs. Publication-quality requires vector exports.
