from __future__ import annotations

import argparse
from pathlib import Path


def _position(text: str, needle: str) -> int:
    idx = text.find(needle)
    return idx if idx >= 0 else 10**12


def check_script(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    issues: list[str] = []
    pyplot_pos = min(_position(text, "import matplotlib.pyplot"), _position(text, "from matplotlib import pyplot"))
    use_pos = _position(text, "matplotlib.use(")
    if pyplot_pos < 10**12 and not (use_pos < pyplot_pos):
        issues.append('matplotlib.use("Agg") must appear before importing matplotlib.pyplot')
    if '"Agg"' not in text and "'Agg'" not in text:
        issues.append("Agg backend is not set explicitly")
    if "svg.fonttype" not in text and "rk_plotter_core" not in text:
        issues.append('svg.fonttype = "none" is not set or inherited from rk_plotter_core')
    if "plt.show(" in text:
        issues.append("plt.show() is not allowed in export scripts")
    if "save_figure(" not in text and "plt.close(" not in text:
        issues.append("figure is not closed via save_figure() or plt.close(fig)")
    return issues


def check_outputs(output_dir: Path, formats: list[str]) -> list[str]:
    issues: list[str] = []
    if not output_dir.exists():
        return [f"output directory does not exist: {output_dir}"]
    for fmt in formats:
        suffix = fmt.lower().lstrip(".")
        matches = list(output_dir.glob(f"*.{suffix}"))
        if not matches:
            issues.append(f"missing .{suffix} output in {output_dir}")
            continue
        empty = [path.name for path in matches if path.stat().st_size == 0]
        if empty:
            issues.append(f"empty .{suffix} outputs: {', '.join(empty)}")
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check rk_plotter generated scripts, outputs, and quality traces.")
    parser.add_argument("--script", type=Path, help="Script path to check.")
    parser.add_argument("--trace", type=Path, help="JSON Trace file path to verify (runs advanced visual audits).")
    parser.add_argument("--output-dir", type=Path, help="Output directory containing files.")
    parser.add_argument("--formats", nargs="+", default=["png", "pdf", "svg"])
    args = parser.parse_args(argv)
    
    # Check if neither is specified
    if args.script is None and args.trace is None:
        print("FAIL: You must specify either --script or --trace to execute check.")
        return 1
        
    issues = []
    
    # 1. Run advanced trace-based visual consistency check if --trace is specified
    if args.trace is not None:
        print(f"Executing advanced trace visual audit on '{args.trace}'...")
        try:
            import sys
            _skill_root = str(Path(__file__).resolve().parents[1])
            if _skill_root not in sys.path:
                sys.path.insert(0, _skill_root)
                
            from rk_plotter.quality import verify_consistency
            audit = verify_consistency(args.trace)
            
            if audit["all_passed"]:
                print(f"PASS: Advanced quality check passed successfully for template '{audit['template_id']}'!")
                for a in audit["audits"]:
                    print(f"  - {a['file']}: {a['notes']}")
                return 0
            else:
                print("FAIL: Trace quality check failed!")
                for a in audit["audits"]:
                    status = "OK" if a["passed"] else "FAIL"
                    print(f"  - [{status}] {a['file']}: {a['notes']}")
                return 1
        except Exception as e:
            print(f"FAIL: Error during trace consistency audit: {e}")
            return 1
            
    # 2. Legacy checks
    if args.script is not None:
        issues = check_script(args.script)
        if args.output_dir is not None:
            issues.extend(check_outputs(args.output_dir, args.formats))
            
    if issues:
        print("FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1
        
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
