import subprocess
import sys
from pathlib import Path
import argparse
import shutil

TEMPLATES_LIST = [
    "predicted_vs_real_scatter",
    "density_scatter",
    "dual_panel_scatter_fit",
    "multi_scenario_timeseries",
    "scenario_uncertainty_timeseries",
    "event_period_timeseries",
    "stacked_percent_bar",
    "horizontal_stacked_bar",
    "boxen_plot",
    "violin_boxplot",
    "heatmap_2d",
    "raster_map",
    "choropleth_map",
    "global_regional_sst_map",
    "shap_importance_bar",
    "multipanel_layout"
]

def render_preview(template_id: str, templates_dir: Path, output_dir: Path) -> bool:
    """Runs template script as a subprocess to render and save preview image."""
    script_path = templates_dir / f"{template_id}.py"
    if not script_path.exists():
        print(f"Error: Template script not found: {script_path}")
        return False
        
    print(f"Rendering '{template_id}'...")
    try:
        # Run script. By default, templates save to 'outputs/{template_id}.png'
        res = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Verify and copy PNG preview file
        raw_png = Path("outputs") / f"{template_id}.png"
        if raw_png.exists():
            dest_png = output_dir / f"{template_id}.png"
            shutil.copy2(raw_png, dest_png)
            print(f"  Saved preview to: {dest_png}")
            return True
        else:
            print(f"  Error: Output PNG not found at: {raw_png}")
            print(f"  Subprocess stdout: {res.stdout}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"  Error: Subprocess crashed with code {e.returncode}!")
        print(f"  Stdout: {e.stdout}")
        print(f"  Stderr: {e.stderr}")
        return False

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render previews for rk_plotter templates.")
    parser.add_argument("--template", default="all", help="Template ID to render or 'all'")
    args = parser.parse_args(argv)
    
    skill_root = Path(__file__).resolve().parents[1]
    templates_dir = skill_root / "templates"
    previews_dir = skill_root / "previews"
    previews_dir.mkdir(parents=True, exist_ok=True)
    
    target_ids = TEMPLATES_LIST if args.template == "all" else [args.template]
    
    failed = 0
    passed = 0
    
    for tid in target_ids:
        success = render_preview(tid, templates_dir, previews_dir)
        if success:
            passed += 1
        else:
            failed += 1
            
    print(f"\nRender Summary: {passed} passed, {failed} failed.")
    
    # Remove local temp outputs folder to keep git clean
    shutil.rmtree("outputs", ignore_errors=True)
    
    return 1 if failed > 0 else 0

if __name__ == "__main__":
    sys.exit(main())
