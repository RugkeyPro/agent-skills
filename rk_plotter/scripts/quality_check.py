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
    parser = argparse.ArgumentParser(description="Check rk_plotter generated scripts and outputs.")
    parser.add_argument("--script", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--formats", nargs="+", default=["png", "pdf", "svg"])
    args = parser.parse_args(argv)
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
