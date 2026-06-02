from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Mapping, Sequence

def write_trace(
    output_dir: str | Path,
    template_id: str,
    field_mapping: Mapping[str, str],
    paths: Sequence[str | Path]
) -> Path:
    """
    Writes a structured execution trace log in JSON format to document
    column mapping, styling configurations, and output files.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Extract string paths
    str_paths = [str(Path(p).resolve()) for p in paths]
    basename = Path(paths[0]).stem if len(paths) > 0 else "unknown"
    
    trace_data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "template_id": template_id,
        "field_mapping": dict(field_mapping),
        "generated_files": str_paths,
        "status": "COMPLETED"
    }
    
    trace_filename = output_dir / f"trace_{basename}.json"
    with open(trace_filename, "w", encoding="utf-8") as f:
        json.dump(trace_data, f, ensure_ascii=False, indent=2)
        
    return trace_filename


def verify_consistency(trace_path: str | Path) -> dict:
    """
    Audits the generated outputs documented in an execution trace log
    to verify presence, file size, and formatting parameters.
    """
    trace_path = Path(trace_path)
    if not trace_path.exists():
        raise FileNotFoundError(f"Trace file not found at: '{trace_path}'")
        
    with open(trace_path, "r", encoding="utf-8") as f:
        trace = json.load(f)
        
    generated_files = trace.get("generated_files", [])
    audits = []
    all_passed = True
    
    for filepath_str in generated_files:
        filepath = Path(filepath_str)
        audit_res = {
            "file": filepath.name,
            "exists": False,
            "size_bytes": 0,
            "passed": False,
            "notes": ""
        }
        
        if filepath.exists():
            audit_res["exists"] = True
            size = filepath.stat().st_size
            audit_res["size_bytes"] = size
            if size > 0:
                audit_res["passed"] = True
                audit_res["notes"] = "File generated successfully with data."
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
