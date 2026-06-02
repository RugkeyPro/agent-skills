import sys
from pathlib import Path

_skill_root = str(Path(__file__).resolve().parents[2])
if _skill_root not in sys.path:
    sys.path.insert(0, _skill_root)

from rk_plotter.templates.density_colored_scatter import plot, render, make_sample_data, TEMPLATE_ID
