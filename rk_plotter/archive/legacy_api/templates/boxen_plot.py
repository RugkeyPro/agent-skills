import sys
from pathlib import Path

# Set up path resolution to find the new rk_plotter package
_skill_root = str(Path(__file__).resolve().parents[2])
if _skill_root not in sys.path:
    sys.path.insert(0, _skill_root)

# Delegate all calls programmatically to the upgraded package template
from rk_plotter.templates.boxen_plot import plot, render, make_sample_data, TEMPLATE_ID
