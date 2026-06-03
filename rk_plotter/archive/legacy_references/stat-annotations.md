# Statistical Annotations

```python
def sig_label(p):
    if p < 0.001: return "***"
    if p < 0.01: return "**"
    if p < 0.05: return "*"
    if p < 0.1: return "."
    return "ns"
```

Use brackets only for pre-planned comparisons. For model diagnostics, show the one-to-one line and only the metrics needed for interpretation. Label uncertainty bands as confidence intervals, prediction intervals, credible intervals, or scenario envelopes.
