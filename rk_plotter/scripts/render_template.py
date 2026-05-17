from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = SCRIPT_DIR / "templates"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from template_registry import CATEGORIES, TEMPLATES


def load_template(template_id: str):
    if template_id not in TEMPLATES:
        known = ", ".join(sorted(TEMPLATES))
        raise SystemExit(f"Unknown template '{template_id}'. Known templates: {known}")
    path = TEMPLATE_DIR / f"{template_id}.py"
    spec = importlib.util.spec_from_file_location(template_id, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Cannot load template module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render an rk_plotter template sample figure.")
    parser.add_argument("--template", required=True, help="Template id, or 'all'.")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--formats", default="png,pdf,svg")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args(argv)
    if args.list:
        for category in CATEGORIES:
            print(f"[{category}]")
            for tid, meta in sorted(TEMPLATES.items()):
                if meta["category"] == category:
                    print(f"  {tid}: {meta['title']}")
        return 0
    formats = tuple(fmt.strip().lstrip(".") for fmt in args.formats.split(",") if fmt.strip())
    ids = sorted(TEMPLATES) if args.template == "all" else [args.template]
    for tid in ids:
        module = load_template(tid)
        paths = module.render(Path(args.output_dir), formats=formats, seed=args.seed)
        print(f"{tid}: " + ", ".join(str(p) for p in paths))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
