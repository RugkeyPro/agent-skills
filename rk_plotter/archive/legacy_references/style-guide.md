# Style Guide

## Configuration Header

```python
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "none"

import matplotlib.pyplot as plt
from scripts.rk_plotter_core import apply_style, save_figure

apply_style()
```

## Figure Sizes

- Single-column panel: `3.46 x 3.0 in`
- Square panel: `3.46 x 3.46 in`
- Wide time series or map: `7.2 x 3.8-4.0 in`
- Tall distribution panel: `3.46 x 4.8 in`
- Conceptual framework: `7.2 x 4.8 in`

## Typography and Layout

Use sans-serif fonts with editable SVG text. Remove top and right spines unless the plot needs a boxed frame. Put units in axis labels and keep legends outside dense data regions when possible.

## Export

Use `save_figure(fig, output_dir, basename, formats=("png", "pdf", "svg"))`. This keeps PNG high resolution, SVG text editable, PDF vector-friendly, and closes figures after saving.
