from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def manifest_template_ids() -> list[str]:
    """Single source of truth: read ids from templates/manifest.json.

    Falls back to globbing templates/*.py if the manifest is missing, so the
    renderer never silently drifts out of sync with the template directory.
    """
    root = skill_root()
    manifest_path = root / "templates" / "manifest.json"
    if manifest_path.exists():
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        return [t["id"] for t in data.get("templates", [])]
    return sorted(p.stem for p in (root / "templates").glob("*.py"))


def render_preview(template_id: str, templates_dir: Path, output_dir: Path) -> bool:
    """Run a template script as a subprocess and copy its PNG into previews/."""
    script_path = templates_dir / f"{template_id}.py"
    if not script_path.exists():
        print(f"Error: Template script not found: {script_path}")
        return False

    print(f"Rendering '{template_id}'...")
    try:
        res = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            check=True,
        )
        raw_png = Path("outputs") / f"{template_id}.png"
        if raw_png.exists():
            dest_png = output_dir / f"{template_id}.png"
            shutil.copy2(raw_png, dest_png)
            print(f"  Saved preview to: {dest_png}")
            return True
        print(f"  Error: Output PNG not found at: {raw_png}")
        print(f"  Subprocess stdout: {res.stdout}")
        return False
    except subprocess.CalledProcessError as e:
        # Missing optional deps (cartopy, seaborn, scipy) surface here; report and skip.
        print(f"  Error: Subprocess crashed with code {e.returncode}!")
        print(f"  Stdout: {e.stdout}")
        print(f"  Stderr: {e.stderr}")
        return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render previews for rk_plotter templates (manifest-driven).")
    parser.add_argument("--template", default="all", help="Template ID to render or 'all'")
    args = parser.parse_args(argv)

    root = skill_root()
    templates_dir = root / "templates"
    previews_dir = root / "previews"
    previews_dir.mkdir(parents=True, exist_ok=True)

    target_ids = manifest_template_ids() if args.template == "all" else [args.template]

    failed = 0
    passed = 0
    for tid in target_ids:
        if render_preview(tid, templates_dir, previews_dir):
            passed += 1
        else:
            failed += 1

    print(f"\nRender Summary: {passed} passed, {failed} failed.")
    shutil.rmtree("outputs", ignore_errors=True)
    return 1 if failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
