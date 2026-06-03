# Refactoring Existing Plot Code: Integration Guidelines

When refactoring a user's existing plot script, you must never modify variables or parameters in place. Instead, partition the code into distinct logical blocks and rewrite the script with the standard template motherboard as your base structure.

---

## 1. Split the Code into Three Blocks

Inspect the user's legacy script and mentally divide it:

### The DATA Block (RETAIN)
- Package imports (`numpy`, `pandas`, `scipy`, etc.).
- Reading source CSV, Excel, or database files.
- Row filtering, NaN cleanings, and grouping.
- Mathematical operations, stats computations, and data transformations.
- **Action**: Preserve this block intact and place it inside the script's `load_data()` or `prepare_data()` functions.

### The PLOT Block (REPLACE)
- Subplots setups (`plt.subplots()`).
- Data plotting commands (`ax.plot`, `ax.scatter`, etc.).
- Legend boxes, coordinate axes lines, and grids.
- Label annotations, stats boxes, and colorbars.
- **Action**: Completely discard this block. Replace it with the corresponding template's `plot()` function.

### The EXPORT Block (REPLACE)
- Save commands (`plt.savefig()`, `plt.show()`).
- Close commands (`plt.close()`).
- **Action**: Replace this block with the standardized `save_outputs()` template routine.

---

## 2. Standard Script Layout

All refactored scripts must follow the template script layout exactly, retaining the meta header comments to declare the templates ID, source mode, and kept/replaced lines:

```python
# TEMPLATE_ID: [template_name]
# SOURCE_MODE: refactor_existing_script
# OLD_CODE_KEPT: [brief summary of data processing / statistics retained]
# OLD_CODE_REPLACED: [brief summary of plotting and save logic replaced]

from __future__ import annotations
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path

TEMPLATE_ID = "[template_name]"
FIELD_MAP = {
    # Bind template fields to user data column names here
}
TEXT_CONFIG = {
    "title": "...",
    "x_label": "...",
    "y_label": "...",
}
STYLE_CONFIG = {
    "figsize": (3.5, 3.2),
    "font_size": 8.5,
    # Standard styles...
}
EXPORT_CONFIG = {
    "output_dir": "outputs",
    "basename": "...",
    "formats": ["svg", "pdf", "png"],
    "dpi": 600,
}

# --- Legacy DATA BLOCK goes here ---
def load_data(path: str | Path) -> pd.DataFrame:
    # 1. Place the user's original data loading / file path logic here
    return pd.read_csv(path)

def prepare_data(df: pd.DataFrame, field_map: dict) -> pd.DataFrame:
    # 2. Place user's original data cleaning / filtering logic here
    # 3. Standardize columns to template fields based on the field_map
    ...
    return clean_df

# --- Standard Plot & Export goes here ---
def plot(data: pd.DataFrame, text: dict, style: dict):
    # Standardized plotting function from the chosen template motherboard
    ...
    return fig

def save_outputs(fig, export: dict):
    # Standardized file saves
    ...
    return paths

def main():
    df = load_data("user_data.csv")
    data = prepare_data(df, FIELD_MAP)
    fig = plot(data, TEXT_CONFIG, STYLE_CONFIG)
    save_outputs(fig, EXPORT_CONFIG)

if __name__ == "__main__":
    main()
```

---

## 3. Benefits of this Refactoring Approach

1. **Maintains Analytical Integrity**: Retaining the exact data processing block ensures that scientific computations (e.g. data points, standard errors, interpolation curves) remain mathematically identical.
2. **Standardizes Aesthetics**: Discarding legacy plot logic guarantees that the output figures conform to clean, professional layout principles.
3. **No Black-Box Imports**: The user receives a standalone, fully readable, and modifiable python script containing all logic from data loading to file saving.
