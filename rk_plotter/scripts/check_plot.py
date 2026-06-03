from pathlib import Path
import argparse
import sys
import py_compile


def check_script_text(script_path: str | Path) -> list[str]:
    script_path = Path(script_path)
    if not script_path.exists():
        return [f"Script file does not exist: {script_path}"]

    issues = []

    try:
        py_compile.compile(str(script_path), doraise=True)
    except py_compile.PyCompileError as e:
        issues.append(f"Syntax error: {e.msg}")

    text = script_path.read_text(encoding="utf-8", errors="replace")

    required_tokens = [
        "TEMPLATE_ID",
        "FIELD_MAP",
        "STYLE_CONFIG",
        "EXPORT_CONFIG",
        "svg.fonttype",
        "savefig",
        "plt.close",
        "load_data",
        "prepare_data",
        "plot",
        "save_outputs",
    ]

    for token in required_tokens:
        if token not in text:
            issues.append(f"Missing required block/token: '{token}'")

    if "plt.show(" in text:
        issues.append("Error: Script contains blocking 'plt.show()'. Use save_outputs() instead.")

    if "matplotlib.use(" not in text:
        issues.append("Warning: Matplotlib Agg backend not explicitly set with matplotlib.use('Agg').")

    if "import rk_plotter" in text or "from rk_plotter" in text:
        issues.append("Warning: Final scripts should usually be standalone and should not rely on rk_plotter black-box imports.")

    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check generated scientific plotting scripts.")
    parser.add_argument("script", type=Path, help="Script path to check")
    args = parser.parse_args(argv)

    issues = check_script_text(args.script)
    if issues:
        print("FAIL: The script has issues:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print("PASS: The script follows the template motherboard specifications.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
