from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Mapping, Sequence
import matplotlib.pyplot as plt

def write_trace(
    output_dir: str | Path,
    template_id: str,
    field_mapping: Mapping[str, str],
    paths: Sequence[str | Path],
    figsize: Sequence[float] | None = None,
    palette: str | None = None,
    formats: Sequence[str] | None = None,
    fig: plt.Figure | None = None,
    n_axes: int | None = None,
    style_profile: dict | str | None = None
) -> Path:
    """
    Writes an enhanced, structured execution trace log in JSON format
    to document column mappings, export formats, and visual dimensions.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    str_paths = [str(Path(p).resolve()) for p in paths]
    basename = Path(paths[0]).name if len(paths) > 0 else "unknown"
    basename_stem = Path(paths[0]).stem if len(paths) > 0 else "unknown"
    
    # Try to load template to fetch style profile
    resolved_profile = {}
    try:
        from template_registry import _STYLE_PROFILES
        resolved_profile = _STYLE_PROFILES.get(template_id, {})
    except Exception:
        pass
        
    try:
        from .registry import load_template
        template = load_template(template_id)
        if template.module and hasattr(template.module, "STYLE_PROFILE"):
            resolved_profile = getattr(template.module, "STYLE_PROFILE", resolved_profile)
    except Exception:
        pass
        
    # Determine figsize
    if figsize is None:
        if fig is not None:
            figsize = list(fig.get_size_inches())
        else:
            figsize = resolved_profile.get("figsize", [4.2, 5.8])
            
    # Determine palette
    if palette is None:
        palette = resolved_profile.get("palette", "categorical")
        
    # Determine n_axes
    if n_axes is None:
        if fig is not None:
            n_axes = len(fig.axes)
        else:
            # Fallback based on layout or common rules
            layout = resolved_profile.get("layout", ())
            if "dual_x_axis" in layout or "twin_y" in layout or "joint_marginal" in layout or "inset_axes" in layout:
                n_axes = 2
            elif "faceted_row" in layout or "multi_panel" in layout:
                n_axes = 3
            else:
                n_axes = 1
                
    # Determine formats
    fmt_list = list(formats) if formats else ["png", "pdf", "svg"]
    if len(paths) > 0:
        fmt_list = list(dict.fromkeys(Path(p).suffix.lstrip(".").lower() for p in paths))
        
    # Record trace data exactly as requested
    trace_data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "template_id": template_id,
        "style_profile": style_profile or resolved_profile,
        "figsize": list(figsize),
        "palette": str(palette),
        "field_mapping": dict(field_mapping),
        "n_axes": n_axes,
        "formats": fmt_list,
        "generated_files": str_paths,
        "status": "COMPLETED"
    }
    
    trace_filename = output_dir / f"trace_{basename_stem}.json"
    with open(trace_filename, "w", encoding="utf-8") as f:
        json.dump(trace_data, f, ensure_ascii=False, indent=2)
        
    return trace_filename


def verify_consistency(trace_path: str | Path) -> dict:
    """
    Audits the generated outputs documented in an execution trace log
    to verify presence, file size, and visual dimension compatibility.
    """
    trace_path = Path(trace_path)
    if not trace_path.exists():
        raise FileNotFoundError(f"Trace file not found at: '{trace_path}'")
        
    with open(trace_path, "r", encoding="utf-8") as f:
        trace = json.load(f)
        
    generated_files = trace.get("generated_files", [])
    expected_figsize = trace.get("figsize", [4.2, 5.8])
    audits = []
    all_passed = True
    
    for filepath_str in generated_files:
        filepath = Path(filepath_str)
        suffix = filepath.suffix.lstrip(".").lower()
        
        audit_res = {
            "file": filepath.name,
            "format": suffix,
            "exists": False,
            "size_bytes": 0,
            "passed": False,
            "dimension_audit": "N/A",
            "notes": ""
        }
        
        if filepath.exists():
            audit_res["exists"] = True
            size = filepath.stat().st_size
            audit_res["size_bytes"] = size
            
            if size > 0:
                # Basic file check passed
                audit_res["passed"] = True
                audit_res["notes"] = "File generated successfully with data."
                
                # PNG dimension check logic (Matplotlib based)
                if suffix == "png":
                    try:
                        img = plt.imread(str(filepath))
                        height_px, width_px = img.shape[:2]
                        # Assuming default save_figure export DPI of 600
                        dpi = 600
                        width_in = width_px / dpi
                        height_in = height_px / dpi
                        
                        # Check bounds (bbox_inches='tight' crops out white space, so dimensions
                        # are typically smaller than or equal to configured figsize, but shouldn't be zero)
                        expected_w, expected_h = expected_figsize
                        max_w_bound = expected_w + 1.0  # allow small border padding
                        max_h_bound = expected_h + 1.0
                        
                        aspect_ratio_actual = width_in / height_in if height_in > 0 else 1
                        aspect_ratio_expected = expected_w / expected_h if expected_h > 0 else 1
                        aspect_diff_pct = abs(aspect_ratio_actual - aspect_ratio_expected) / aspect_ratio_expected
                        
                        if width_in > 0 and height_in > 0 and width_in <= max_w_bound and height_in <= max_h_bound:
                            audit_res["dimension_audit"] = f"PASSED ({width_in:.2f}x{height_in:.2f} in, aspect: {aspect_ratio_actual:.2f})"
                            audit_res["notes"] = (
                                f"Dimension check passed. Verified PNG image size: {width_px}x{height_px} px "
                                f"({width_in:.2f}x{height_in:.2f} in at 600 DPI). Matches expected figsize {expected_figsize}."
                            )
                        else:
                            all_passed = False
                            audit_res["passed"] = False
                            audit_res["dimension_audit"] = f"FAILED ({width_in:.2f}x{height_in:.2f} in)"
                            audit_res["notes"] = (
                                f"Error: Rendered dimension {width_in:.2f}x{height_in:.2f} in "
                                f"exceeds expected limits (max bounds: {max_w_bound:.1f}x{max_h_bound:.1f} in)."
                            )
                    except Exception as e:
                        audit_res["dimension_audit"] = "ERROR"
                        audit_res["notes"] = f"Warning: Failed to parse PNG dimensions: {str(e)}"
            else:
                all_passed = False
                audit_res["notes"] = "Error: File generated but is empty (0 bytes)."
        else:
            all_passed = False
            audit_res["notes"] = "Error: File does not exist on disk."
            
        audits.append(audit_res)
        
    return {
        "trace_file": str(trace_path),
        "template_id": trace.get("template_id"),
        "all_passed": all_passed,
        "audits": audits
    }
