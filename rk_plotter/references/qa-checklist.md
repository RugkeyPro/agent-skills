# QA Checklist: Verification Specifications

Before completing a plotting task or delivering a script, verify every item on this checklist.

---

## 1. Script Architecture & Formatting

- [ ] **TEMPLATE_ID**: The script declares a clear `TEMPLATE_ID` matching one of the official templates.
- [ ] **Standard Blocks**: The script defines `FIELD_MAP`, `TEXT_CONFIG`, `STYLE_CONFIG`, and `EXPORT_CONFIG` near the top.
- [ ] **No Black-Box Imports**: The script is complete and standalone, containing `load_data()`, `prepare_data()`, `plot()`, `save_outputs()`, and `main()`. It does **not** import `rk_plotter` packages or helper functions.
- [ ] **No Interactive Functions**: There is no `plt.show()` inside the script (interactive rendering blocks execution during script runs).
- [ ] **Memory Management**: Every plotting script includes `plt.close(fig)` inside `save_outputs()` to release backend memory.

---

## 2. Scientific Data & Columns

- [ ] **No Guessing**: Columns are bound via `FIELD_MAP` and matched in `prepare_data()`. There is no guessing by raw integer index unless the dataset lacks headers.
- [ ] **Units & Labels**: All units are preserved and explicitly appended to axes labels (e.g. `Time (s)`, `Concentration (mg/L)`).
- [ ] **NaN Handling**: Data filtering and sorting handle null values (`.dropna()`) before calling plot commands to prevent NaN errors.
- [ ] **Chronological / Sequence Order**: Sorted coordinates, dates, times, or custom labels preserve logical ordering (e.g. SSP126 -> SSP245 -> SSP585).

---

## 3. Publication Layout & Spacing

- [ ] **Font Family**: Standardizes matplotlib typography to use Arial/DejaVu Sans.
- [ ] **Font Sizes**: Axes labels, ticks, and legends are scaled proportionally.
- [ ] **Vector Fonts**: The script sets `plt.rcParams["svg.fonttype"] = "none"` to preserve editable fonts in SVG.
- [ ] **Vector File Embedding**: The script sets `plt.rcParams["pdf.fonttype"] = 42` to ensure TrueType font embedding in PDFs.
- [ ] **White Space**: `bbox_inches="tight"` is passed to `fig.savefig()` to crop out margins.
- [ ] **Grid Lines & Spines**: Spines (`top`/`right`) are hidden. Grid lines are placed behind elements (`zorder=0`).
- [ ] **No Text Clutter**: Custom annotations inside the plot coordinates are kept minimal (e.g. limited to significance asterisks, regression stats like slope/p-value/R², or panel labels). No long explanatory sentences or redundant data values on bars/points are present.
- [ ] **Extension Styling**: If structural extensions were added (twin axes, extra series, error bands, reference lines, zoom insets), they are styled consistently with standard widths, colors, transparency, and markers.

---

## 4. Multi-Panel & Layouts

- [ ] **Shared Limits**: Shared panels (e.g. dual-panel scatter plots) share y-axis or x-axis ranges where comparable.
- [ ] **A/B Labeling**: Multi-panel figures include bold labels (`A`, `B`, etc.) in the top-left of each axis coordinate.
- [ ] **Legend Positioning**: Legends are positioned inside panels or at the top of the canvas to avoid overlapping with data points.
- [ ] **Colorbars**: Right-hand colorbars match panel heights and do not distort the aspect ratio of the plot panels.
