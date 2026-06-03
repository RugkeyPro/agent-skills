# Color Palettes

## Core Palettes

```python
CATEGORICAL = ["#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377", "#BBBBBB", "#000000"]
SCENARIO = ["#1B9E77", "#D95F02", "#7570B3", "#E7298A", "#66A61E", "#E6AB02"]
MODEL = ["#4C78A8", "#F58518", "#54A24B", "#B279A2", "#E45756"]
```

## Sequential, Diverging, and Log Data

Use `viridis`, `cividis`, `mako`, or `YlGnBu` for ordered values. Use `magma_r` with `LogNorm` for log-scale intensity. Use `RdBu_r`, `BrBG`, or `PuOr` with a meaningful center for differences.

## Rules

Do not use `jet` or `rainbow`. Do not encode critical groups with red vs green only. Keep alpha high enough for print.
