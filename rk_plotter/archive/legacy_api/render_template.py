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
    
    # 1. Try importing from upgraded package templates
    try:
        import importlib
        return importlib.import_module(f"rk_plotter.templates.{template_id}")
    except ModuleNotFoundError:
        pass
        
    # 2. Try importing from scripts templates module
    try:
        import importlib
        return importlib.import_module(f"scripts.templates.{template_id}")
    except ModuleNotFoundError:
        pass
        
    # 3. Fallback to raw file loading as legacy
    path = TEMPLATE_DIR / f"{template_id}.py"
    if not path.exists():
        raise SystemExit(f"Template script file not found: {path}")
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
    
    failed = False
    for tid in ids:
        try:
            module = load_template(tid)
            paths = module.render(Path(args.output_dir), formats=formats, seed=args.seed)
            print(f"{tid}: " + ", ".join(str(p) for p in paths))
            
            # Incorporate trace quality / consistency validation
            try:
                from rk_plotter.quality import write_trace, verify_consistency
                trace_path = write_trace(
                    output_dir=args.output_dir,
                    template_id=tid,
                    field_mapping={"x": "dummy_x", "y": "dummy_y"},
                    paths=paths
                )
                audit = verify_consistency(trace_path)
                if not audit["all_passed"]:
                    print(f"  [ERROR] Quality consistency audit failed for template '{tid}'!")
                    for item in audit["audits"]:
                        if not item["passed"]:
                            print(f"    - {item['file']}: {item['notes']}")
                    failed = True
            except Exception as e:
                # Basic fallback checks if rk_plotter package isn't importable
                for p in paths:
                    p = Path(p)
                    if not p.exists() or p.stat().st_size == 0:
                        print(f"  [ERROR] Output file '{p.name}' is missing or empty!")
                        failed = True
        except Exception as e:
            print(f"  [CRASH] Failed to render template '{tid}': {e}")
            failed = True
            
    if failed:
        print("\n[FAIL] Smoke test finished with errors.")
        return 1
    print("\n[SUCCESS] All templates successfully rendered and verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
