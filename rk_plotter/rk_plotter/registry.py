from __future__ import annotations

import sys
import importlib
from pathlib import Path
import pandas as pd
import numpy as np

# Dynamically append scripts and root directories to sys.path to load template_registry and scripts
_scripts_dir = str(Path(__file__).resolve().parents[1] / "scripts")
_root_dir = str(Path(__file__).resolve().parents[1])
for path_dir in [_scripts_dir, _root_dir]:
    if path_dir not in sys.path:
        sys.path.insert(0, path_dir)

try:
    from template_registry import TEMPLATES
except ImportError:
    TEMPLATES = {}

class Template:
    """Represents a specific research plotting template with visual mapping and rendering logic."""
    def __init__(self, template_id: str, metadata: dict):
        self.template_id = template_id
        self.metadata = metadata
        self.title = metadata.get("title", template_id.replace("_", " ").title())
        self.category = metadata.get("category", "")
        self.use = metadata.get("use", "")
        self.kind = metadata.get("kind", "")
        
        # Load the module dynamically to inspect required fields and custom aliases
        self.module = self._load_module()
        
        # Determine REQUIRED_FIELDS (look for module-level attribute, then metadata, then default)
        self.required_fields = getattr(self.module, "REQUIRED_FIELDS", metadata.get("data_profile", {}).get("required_fields", ("x", "y")))
        
        # Determine FIELD_ALIASES
        self.field_aliases = getattr(self.module, "FIELD_ALIASES", {})
        
    def _load_module(self):
        """Attempts to dynamically import the template module from the package or legacy folder."""
        # 1. Try importing from the upgraded package directory
        try:
            return importlib.import_module(f"rk_plotter.templates.{self.template_id}")
        except ModuleNotFoundError:
            # 2. Try importing from the legacy scripts directory
            try:
                return importlib.import_module(f"scripts.templates.{self.template_id}")
            except ModuleNotFoundError:
                # 3. If both fail, return None (metadata-only template)
                return None
                
    def infer_fields(self, df: pd.DataFrame) -> dict[str, str]:
        """
        Dynamically infers field mappings between template required fields
        and DataFrame column names using semantic keyword matching and positional fallbacks.
        """
        columns = [str(c) for c in df.columns]
        mapping: dict[str, str] = {}
        
        # Default global rule sets for semantic matching
        default_rules = {
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
            
            # Use template-specific aliases if defined, otherwise fallback to defaults
            keywords = self.field_aliases.get(field, default_rules.get(field_lower, [field_lower]))
            
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
                if columns:
                    mapping[field] = columns[-1]
                    
        return mapping
        
    def plot(self, df: pd.DataFrame, field_mapping: dict[str, str], config: dict | None = None):
        """
        Plots the user's DataFrame by dynamically converting it using our visual adapters
        and invoking the loaded template module.
        """
        if self.module is None:
            # Re-attempt loading in case package was updated
            self.module = self._load_module()
            if self.module is None:
                raise NotImplementedError(
                    f"Template '{self.template_id}' is not physically present on disk in templates or scripts."
                )
                
        # 1. Check if the template module defines an explicit adapter
        if hasattr(self.module, "adapt_dataframe"):
            df_adapted = self.module.adapt_dataframe(df, field_mapping)
            
            fig, ax = self.module.plot(
                data=df_adapted,
                config=config
            )
            return fig
            
        # 2. Fallback to Smart Programmatic DataFrame Adapter for legacy templates
        # We translate the DataFrame into the exact dictionary schema required by scripts/templates/
        kind = self.kind or self.metadata.get("kind", "")
        data_dict = {"title": self.title}
        
        try:
            if kind in {"boxen", "model_boxplot", "faceted_boxplot", "violin_box"}:
                grp_col = field_mapping.get("groups") or field_mapping.get("x") or df.columns[0]
                val_col = field_mapping.get("values") or field_mapping.get("y") or df.columns[1]
                grps = df[grp_col].unique()
                data_dict.update({
                    "groups": np.array(grps),
                    "values": [df[df[grp_col] == g][val_col].values for g in grps],
                    "ylabel": str(val_col)
                })
                
            elif kind in {"stacked_percent", "stacked_bar_time", "horizontal_stacked", "horizontal_stacked_zoom", "stacked_percent_line", "diverging_bar"}:
                grp_col = field_mapping.get("groups") or df.columns[0]
                other_cols = [c for c in df.columns if c != grp_col]
                
                # Check for Long format: grp_col, comp_col, val_col
                if len(other_cols) == 2 and not pd.api.types.is_numeric_dtype(df[other_cols[0]]):
                    comp_col, val_col = other_cols[0], other_cols[1]
                    pivoted = df.pivot(index=grp_col, columns=comp_col, values=val_col)
                    groups = pivoted.index.values
                    components = pivoted.columns.values
                    values = pivoted.values
                    ylabel_str = str(val_col)
                else:
                    # Wide format
                    groups = df[grp_col].unique()
                    components = np.array(other_cols)
                    values = df[other_cols].values
                    ylabel_str = "Percent" if "percent" in kind else "Value"
                    
                data_dict.update({
                    "groups": groups,
                    "components": components,
                    "values": values,
                    "ylabel": ylabel_str
                })
                
            elif kind in {"grouped_bar", "horizontal_dual_axis", "binary_bar"}:
                grp_col = field_mapping.get("groups") or df.columns[0]
                other_cols = [c for c in df.columns if c != grp_col]
                
                if len(other_cols) == 2 and not pd.api.types.is_numeric_dtype(df[other_cols[0]]):
                    ser_col, val_col = other_cols[0], other_cols[1]
                    pivoted = df.pivot(index=grp_col, columns=ser_col, values=val_col)
                    groups = pivoted.index.values
                    series = pivoted.columns.values
                    values = pivoted.values
                    ylabel_str = str(val_col)
                else:
                    groups = df[grp_col].unique()
                    series = np.array(other_cols)
                    values = df[other_cols].values
                    ylabel_str = "Value"
                    
                data_dict.update({
                    "groups": groups,
                    "series": series,
                    "values": values,
                    "ylabel": ylabel_str
                })
                
            elif kind in {"stacked_area", "multi_line_time", "observed_simulated", "scenario_uncertainty", "event_period", "log_timeseries"}:
                x_col = field_mapping.get("x") or field_mapping.get("time") or df.columns[0]
                other_cols = [c for c in df.columns if c != x_col]
                
                if len(other_cols) == 2 and not pd.api.types.is_numeric_dtype(df[other_cols[0]]):
                    # Long format: [Time, Scenario, Value]
                    lbl_col, val_col = other_cols[0], other_cols[1]
                    pivoted = df.pivot(index=x_col, columns=lbl_col, values=val_col)
                    x_vals = pivoted.index.values
                    labels = pivoted.columns.values
                    series = pivoted.values.T  # shape (num_series, len_x)
                    ylabel_str = str(val_col)
                else:
                    # Wide format: [Time, ScenarioA, ScenarioB]
                    x_vals = df[x_col].values
                    labels = np.array(other_cols)
                    series = df[other_cols].values.T
                    ylabel_str = "Value"
                    
                data_dict.update({
                    "x": x_vals,
                    "series": series,
                    "labels": labels,
                    "ylabel": ylabel_str
                })
                
            elif kind in {"response_curve", "latitudinal_profile", "depth_profile"}:
                x_col = field_mapping.get("x") or df.columns[0]
                y_col = field_mapping.get("y") or df.columns[1]
                data_dict.update({
                    "x": df[x_col].values,
                    "y": df[y_col].values,
                    "xlabel": str(x_col),
                    "ylabel": str(y_col)
                })
                
            elif kind in {"density_scatter", "pca", "loglog_scatter", "predicted_real", "parity"}:
                x_col = field_mapping.get("real") or field_mapping.get("x") or df.columns[0]
                y_col = field_mapping.get("predicted") or field_mapping.get("y") or df.columns[1]
                data_dict.update({
                    "x": df[x_col].values,
                    "y": df[y_col].values,
                    "xlabel": str(x_col),
                    "ylabel": str(y_col)
                })
                
            elif kind in {"country_choropleth", "choropleth_symbol"}:
                reg_col = field_mapping.get("region") or df.columns[0]
                val_col = field_mapping.get("value") or df.columns[1]
                data_dict.update({
                    "countries": dict(zip(df[reg_col].astype(str), df[val_col].astype(float))),
                    "metric": str(val_col)
                })
                
            elif kind in {"hist_kde", "hist_ecdf", "overlap_kde", "joint_kde"}:
                lbl_col = field_mapping.get("labels") or [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])][0] or df.columns[0]
                val_col = [c for c in df.columns if c != lbl_col][0]
                labels = df[lbl_col].unique()
                values = [df[df[lbl_col] == l][val_col].values for l in labels]
                data_dict.update({
                    "values": values,
                    "labels": np.array(labels),
                    "xlabel": str(val_col)
                })
                
            elif kind in {"shap_bar", "shap_beeswarm"}:
                feat_col = field_mapping.get("features") or df.columns[0]
                imp_col = field_mapping.get("importance") or df.columns[1]
                data_dict.update({
                    "features": df[feat_col].values,
                    "importance": df[imp_col].values,
                    "effects": df.select_dtypes(include=[np.number]).values
                })
                
            elif kind == "radar":
                lbl_col = df.columns[0]
                val_col = df.columns[1]
                data_dict.update({
                    "labels": df[lbl_col].values,
                    "values": df[val_col].values
                })
                
            elif kind == "nested_donut":
                data_dict.update({
                    "outer": df.iloc[:, 0].values,
                    "inner": df.iloc[:, 1].values if len(df.columns) > 1 else df.iloc[:, 0].values
                })
                
            elif "raster" in kind or "quiver" in kind or "contour" in kind or kind in {"hotspot_map", "log_scale_raster_map", "global_raster_vessel_fraction"}:
                lon_col = [c for c in df.columns if "lon" in str(c).lower() or "x" in str(c).lower()]
                lon_col = lon_col[0] if lon_col else df.columns[0]
                lat_col = [c for c in df.columns if "lat" in str(c).lower() or "y" in str(c).lower()]
                lat_col = lat_col[0] if lat_col else df.columns[1]
                val_col = [c for c in df.columns if c not in {lon_col, lat_col}]
                val_col = val_col[0] if val_col else df.columns[-1]
                
                if len(df.columns) >= 3:
                    try:
                        pivoted = df.pivot(index=lat_col, columns=lon_col, values=val_col)
                        lon_vals = pivoted.columns.values
                        lat_vals = pivoted.index.values
                        raster_vals = pivoted.values
                    except Exception:
                        lon_vals = df[lon_col].unique()
                        lat_vals = df[lat_col].unique()
                        raster_vals = df[val_col].values.reshape((len(lat_vals), len(lon_vals)))
                else:
                    lon_vals = df.columns.values
                    lat_vals = df.index.values
                    raster_vals = df.values
                    
                data_dict.update({
                    "lon": lon_vals,
                    "lat": lat_vals,
                    "raster": raster_vals,
                    "xlabel": str(lon_col),
                    "ylabel": str(lat_col)
                })
                
            else:
                # Generic fallback dictionary mapping first 2 columns
                c1, c2 = df.columns[0], df.columns[1]
                data_dict.update({
                    "x": df[c1].values,
                    "y": df[c2].values,
                    "xlabel": str(c1),
                    "ylabel": str(c2)
                })
        except Exception as e:
            # If mapping fails, pass raw DataFrame directly
            data_dict = df
            
        fig, ax = self.module.plot(
            data=data_dict,
            config=config
        )
        return fig


def load_template(template_id: str) -> Template:
    """Loads a specific template object from its ID, supporting legacy fallbacks."""
    if template_id not in TEMPLATES:
        raise ValueError(f"Unknown template ID: '{template_id}'. Available: {list(TEMPLATES.keys())}")
    return Template(template_id, TEMPLATES[template_id])
