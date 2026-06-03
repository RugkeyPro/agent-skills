import pandas as pd
from pathlib import Path
import json
import argparse
import sys

def inspect_data(path: str | Path) -> dict:
    """Helper function to return detailed statistics of a dataset."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Source file not found at: '{path}'")
        
    # Attempt reading using pandas
    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    elif path.suffix.lower() in {".xls", ".xlsx"}:
        df = pd.read_excel(path)
    else:
        # Fallback raw text loading
        df = pd.read_csv(path, sep=None, engine="python")
        
    summary = {
        "file": path.name,
        "shape": list(df.shape),
        "columns": list(df.columns),
        "dtypes": {str(c): str(t) for c, t in df.dtypes.items()},
        "missing_counts": df.isna().sum().to_dict(),
        "numeric_columns": list(df.select_dtypes(include="number").columns),
        "non_numeric_columns": list(df.select_dtypes(exclude="number").columns),
        "preview_head": df.head(5).to_dict(orient="records")
    }
    return summary

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect user data files and print schema.")
    parser.add_argument("data_file", type=Path, help="Data file path (.csv, .xlsx)")
    args = parser.parse_args(argv)
    
    try:
        summary = inspect_data(args.data_file)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0
    except Exception as e:
        print(f"Error inspecting data: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
