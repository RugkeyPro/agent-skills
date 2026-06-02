from __future__ import annotations

import sys
import importlib
from pathlib import Path
import pandas as pd
import numpy as np

# Dynamically append scripts directory to sys.path to load template_registry
_scripts_dir = str(Path(__file__).resolve().parents[1] / "scripts")
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

try:
    from template_registry import TEMPLATES
except ImportError:
    # Failback dictionary in case of path resolution issues during tests
    TEMPLATES = {}

class Template:
    """Represents a specific research plotting template with visual mapping and rendering logic."""
    def __init__(self, template_id: str, metadata: dict):
        self.template_id = template_id
        self.metadata = metadata
        self.required_fields = metadata.get("data_profile", {}).get("required_fields", ("x", "y"))
        self.title = metadata.get("title", template_id.replace("_", " ").title())
        self.category = metadata.get("category", "")
        self.use = metadata.get("use", "")
        
    def infer_fields(self, df: pd.DataFrame) -> dict[str, str]:
        """
        Dynamically infers field mappings between template required fields
        and DataFrame column names using semantic keyword matching and positional fallbacks.
        """
        columns = [str(c) for c in df.columns]
        mapping: dict[str, str] = {}
        
        # Rule sets for semantic matching (lowercase, sub-string matching)
        rules = {
            "real": ["observed", "obs", "real", "measured", "true", "actual", "y_true", "measured_values"],
            "observed": ["observed", "obs", "real", "measured", "true", "actual", "y_true"],
            "predicted": ["predicted", "pred", "simulated", "sim", "model", "forecast", "y_pred", "predicted_values"],
            "simulated": ["predicted", "pred", "simulated", "sim", "model", "forecast", "y_pred"],
            "groups": ["group", "class", "label", "category", "cat", "type", "treatment", "groups"],
            "region": ["country", "iso", "region", "nation", "state", "province", "geo"],
            "value": ["value", "val", "index", "metric", "score", "rate", "emission"],
            "values": ["value", "val", "index", "metric", "score", "rate", "emission"],
            "x": ["x", "lon", "longitude", "observed"],
            "y": ["y", "lat", "latitude", "predicted"]
        }
        
        assigned = set()
        
        # 1. Primary pass: Semantic rule-based matching
        for field in self.required_fields:
            field_lower = field.lower()
            matched_col = None
            
            # Check keywords associated with this field
            keywords = rules.get(field_lower, [field_lower])
            for col in columns:
                if col in assigned:
                    continue
                col_lower = col.lower()
                if any(kw in col_lower for kw in keywords):
                    matched_col = col
                    break
                    
            if matched_col:
                mapping[field] = matched_col
                assigned.add(matched_col)
                
        # 2. Secondary pass: Positional fallback for unassigned fields
        for field in self.required_fields:
            if field in mapping:
                continue
            # Find the first column that hasn't been assigned yet
            for col in columns:
                if col not in assigned:
                    mapping[field] = col
                    assigned.add(col)
                    break
            else:
                # If no columns are left, fall back to the last column
                if columns:
                    mapping[field] = columns[-1]
                    
        return mapping
        
    def plot(self, df: pd.DataFrame, field_mapping: dict[str, str], config: dict | None = None):
        """
        Dynamically imports the specific template script and plots the user's data.
        """
        try:
            module = importlib.import_module(f"rk_plotter.templates.{self.template_id}")
        except ModuleNotFoundError as e:
            raise NotImplementedError(
                f"Template '{self.template_id}' is not yet migrated to the new package structure. "
                f"Error: {str(e)}"
            )
            
        # Standardize keyword mappings based on the specific template expected signatures
        kwargs = {}
        if self.template_id == "boxen_plot":
            kwargs["x"] = field_mapping.get("groups")
            kwargs["y"] = field_mapping.get("values")
        elif self.template_id == "density_colored_scatter":
            kwargs["x"] = field_mapping.get("x")
            kwargs["y"] = field_mapping.get("y")
        elif self.template_id == "predicted_vs_real_scatter":
            kwargs["x"] = field_mapping.get("real")
            kwargs["y"] = field_mapping.get("predicted")
        elif self.template_id == "country_choropleth_map":
            kwargs["country_col"] = field_mapping.get("region")
            kwargs["value_col"] = field_mapping.get("value")
            
        fig, ax = module.plot(
            data=df,
            config=config,
            **kwargs
        )
        return fig


def load_template(template_id: str) -> Template:
    """Loads a specific template object from its ID."""
    if template_id not in TEMPLATES:
        raise ValueError(f"Unknown template ID: '{template_id}'. Available: {list(TEMPLATES.keys())}")
    return Template(template_id, TEMPLATES[template_id])
