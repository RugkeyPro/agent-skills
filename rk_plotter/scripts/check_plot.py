"""Structural validator for rk_plotter-generated scripts and templates.

Goes beyond substring checks: parses the script with `ast` so a token appearing
in a comment or string can't fake a passing grade, and confirms the actual
template-motherboard contract (config dicts, the load/prepare/plot/save pipeline,
3-format export, no blocking plt.show, no silent synthetic-data fallback).

Usage:
    python scripts/check_plot.py path/to/script.py
    python scripts/check_plot.py --all          # scan every templates/*.py
"""
from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path


REQUIRED_CONFIG_DICTS = ["FIELD_MAP", "STYLE_CONFIG", "EXPORT_CONFIG"]
REQUIRED_FUNCTIONS = ["load_data", "prepare_data", "plot", "save_outputs", "main"]


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _module_assignments(tree: ast.Module) -> dict[str, ast.expr]:
    """Map top-level assigned names to their value node."""
    out: dict[str, ast.expr] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    out[target.id] = node.value
    return out


def _function_names(tree: ast.Module) -> set[str]:
    return {n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}


def _calls_plt_show(tree: ast.Module) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "show":
                val = node.func.value
                if isinstance(val, ast.Name) and val.id in {"plt", "pyplot"}:
                    return True
    return False


def check_script_text(script_path: str | Path) -> list[str]:
    script_path = Path(script_path)
    if not script_path.exists():
        return [f"Script file does not exist: {script_path}"]

    issues: list[str] = []
    text = script_path.read_text(encoding="utf-8", errors="replace")

    try:
        tree = ast.parse(text, filename=str(script_path))
    except SyntaxError as e:
        return [f"Syntax error: {e}"]

    assignments = _module_assignments(tree)
    functions = _function_names(tree)

    # Config dictionaries must exist AND actually be dicts (not just a token match).
    for name in REQUIRED_CONFIG_DICTS:
        if name not in assignments:
            issues.append(f"Missing required config: '{name}' is not defined at module level.")
        elif not isinstance(assignments[name], ast.Dict):
            issues.append(f"'{name}' must be a dict literal.")

    # TEMPLATE_ID is expected but a warning rather than hard failure for ad-hoc scripts.
    if "TEMPLATE_ID" not in assignments:
        issues.append("Warning: 'TEMPLATE_ID' not defined; generated scripts should declare it.")

    # The load -> prepare -> plot -> save pipeline must be present as real functions.
    for fn in REQUIRED_FUNCTIONS:
        if fn not in functions:
            issues.append(f"Missing required function: '{fn}()'.")

    # EXPORT_CONFIG.formats should request the three vector/raster formats.
    export = assignments.get("EXPORT_CONFIG")
    if isinstance(export, ast.Dict):
        formats = _dict_get_literal(export, "formats")
        if isinstance(formats, list):
            lowered = {str(f).lower() for f in formats}
            for fmt in ("svg", "pdf", "png"):
                if fmt not in lowered:
                    issues.append(f"EXPORT_CONFIG.formats is missing '{fmt}' (need png+pdf+svg).")
        else:
            issues.append("EXPORT_CONFIG.formats should be a list literal of formats.")

    # Editable-text font preservation for Illustrator.
    if "svg.fonttype" not in text:
        issues.append("Missing 'svg.fonttype' rcParam (needed for editable SVG text).")

    # Export hygiene.
    if "savefig" not in text:
        issues.append("No savefig call found; script must write output files.")
    if "plt.close" not in text:
        issues.append("Missing 'plt.close(fig)'; figures should be closed after saving.")
    if _calls_plt_show(tree):
        issues.append("Script calls plt.show(); use save_outputs() instead of a blocking window.")

    # Backend.
    if "matplotlib.use(" not in text:
        issues.append("Warning: Agg backend not set via matplotlib.use('Agg').")

    # Black-box import of the skill itself defeats the standalone-script contract.
    if "import rk_plotter" in text or "from rk_plotter" in text:
        issues.append("Warning: final scripts should be standalone, not import rk_plotter.")

    # Silent synthetic-data fallback: hardcoded data.csv probe ignores the real path.
    if 'Path("data.csv").exists' in text or "Path('data.csv').exists" in text:
        issues.append(
            "Hardcoded Path(\"data.csv\").exists() probe: real user data with another "
            "filename would be silently replaced by synthetic data. Key off the loaded "
            "DataFrame (e.g. df.attrs['synthetic']) instead."
        )

    return issues


def _dict_get_literal(d: ast.Dict, key: str):
    for k, v in zip(d.keys, d.values):
        if isinstance(k, ast.Constant) and k.value == key:
            try:
                return ast.literal_eval(v)
            except Exception:
                return v
    return None


def check_one(path: Path) -> int:
    issues = check_script_text(path)
    errors = [i for i in issues if not i.startswith("Warning")]
    warnings = [i for i in issues if i.startswith("Warning")]
    if errors:
        print(f"FAIL {path.name}")
        for issue in errors:
            print(f"  - {issue}")
        for w in warnings:
            print(f"  ~ {w}")
        return 1
    print(f"PASS {path.name}" + (f"  ({len(warnings)} warning(s))" if warnings else ""))
    for w in warnings:
        print(f"  ~ {w}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Structurally check rk_plotter scripts/templates.")
    parser.add_argument("script", nargs="?", type=Path, help="Script path to check")
    parser.add_argument("--all", action="store_true", help="Check every templates/*.py")
    args = parser.parse_args(argv)

    if args.all:
        templates = sorted((skill_root() / "templates").glob("*.py"))
        rc = 0
        for tpl in templates:
            rc |= check_one(tpl)
        print(f"\nChecked {len(templates)} template(s).")
        return rc

    if not args.script:
        parser.error("provide a script path or --all")
    return check_one(args.script)


if __name__ == "__main__":
    sys.exit(main())
