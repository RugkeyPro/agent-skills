from pathlib import Path
import argparse
import sys

def check_script_text(script_path: str | Path) -> list[str]:
    """Inspects target script text to ensure standard layout formatting."""
    script_path = Path(script_path)
    if not script_path.exists():
        return [f"Script file does not exist: {script_path}"]
        
    text = script_path.read_text(encoding="utf-8", errors="replace")
    issues = []
    
    # Core variables required to be declared near top of script motherboard
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
        "save_outputs"
    ]
    
    for token in required_tokens:
        if token not in text:
            issues.append(f"Missing required block/token: '{token}'")
            
    # Prohibit interactive blockers
    if "plt.show(" in text:
        issues.append("Error: Script contains blocking 'plt.show()'. Use save_outputs() instead.")
        
    # Check for Agg backend setting before importing pyplot
    if "matplotlib.use(" not in text:
        issues.append("Warning: Matplotlib Agg backend not explicitly set with matplotlib.use('Agg').")
        
    return issues

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check generated scientific plotting scripts.")
    parser.add_argument("script", type=Path, help="Script path to check")
    args = parser.parse_args(argv)
    
    issues = check_script_text(args.script)
    if issues:
        print("FAIL: The script has formatting issues:")
        for issue in issues:
            print(f"  - {issue}")
        return 1
        
    print("PASS: The script follows the motherboard specifications.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
