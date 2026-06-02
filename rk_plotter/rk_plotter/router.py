from __future__ import annotations

import re
from typing import Any, Iterable, Sequence
from .registry import TEMPLATES

TOKEN_SPLIT_RE = re.compile(r"[^a-z0-9_]+")

# Tags expansion aliases mapping
TAG_ALIASES = {
    "model_diagnostic": ("prediction", "model_validation", "one_to_one"),
    "parity": ("prediction", "observed", "predicted", "one_to_one", "parity"),
    "prediction_pairs": ("prediction", "observed", "predicted", "one_to_one"),
    "loglog": ("prediction", "observed", "predicted", "one_to_one", "log_scale"),
    "scenario_timeseries": ("scenario", "time_series", "multi_line"),
    "categorical_field": ("spatial", "choropleth", "categorical_field"),
    "feature_importance": ("shap", "features", "importance"),
    "ml_explain": ("shap", "features"),
}

# Semantic mapping from user natural language requests to tags
QUERY_RULES = (
    (("地图", "经纬度", "栅格", "热点", "风险", "暴露", "map", "raster", "spatial"), ("spatial", "lon_lat_grid", "continuous_field")),
    (("国家", "行政区", "choropleth", "country", "边界"), ("spatial", "choropleth", "country")),
    (("对数", "数量级", "log"), ("log_scale",)),
    (("方向", "流场", "风场", "quiver", "vector"), ("vector_field", "quiver")),
    (("分布", "两组", "多组", "distribution", "box", "violin", "箱线", "分布图"), ("distribution", "grouped_samples", "category_comparison")),
    (("联合密度", "joint", "bivariate"), ("distribution", "paired_samples", "joint_density")),
    (("kde", "核密度"), ("distribution", "kde", "density")),
    (("预测", "实测", "观测", "predicted", "observed", "parity", "对照", "ML", "回归"), ("prediction", "observed", "predicted", "one_to_one", "model_diagnostic")),
    (("情景", "scenario", "ssp", "rcp", "时间序列"), ("scenario", "time_series", "multi_line")),
    (("不确定", "置信", "区间", "uncertainty", "confidence"), ("uncertainty_band",)),
    (("组成", "比例", "百分比", "composition", "percent", "stacked", "堆叠"), ("composition", "percent", "groups")),
    (("正负", "贡献", "diverging"), ("composition", "diverging", "signed")),
    (("shap", "特征效应", "解释"), ("shap", "features", "effects")),
    (("重要性", "importance"), ("shap", "features", "importance")),
    (("框架", "流程", "概念", "framework", "workflow"), ("framework", "conceptual", "workflow")),
)

class TemplateMatch:
    """Encapsulates the result of a programmatic template routing recommendation."""
    def __init__(self, template_id: str, score: float, matched_tags: list[str]):
        self.template_id = template_id
        self.score = score
        self.matched_tags = matched_tags
        
    def __repr__(self) -> str:
        return f"TemplateMatch(template_id='{self.template_id}', score={self.score:.1f}, matched_tags={self.matched_tags})"


def normalize_token(value: Any) -> str:
    """Normalizes visual strings to unified lower-case snake-case tokens."""
    token = str(value).strip().lower().replace("-", "_").replace(" ", "_")
    token = TOKEN_SPLIT_RE.sub("_", token)
    return re.sub(r"_+", "_", token).strip("_")


def infer_tags_from_query(query: str) -> tuple[str, ...]:
    """Infers standard registry tags from a natural language request query."""
    text = query.lower()
    tags: list[str] = []
    for keywords, inferred in QUERY_RULES:
        if any(keyword.lower() in text for keyword in keywords):
            tags.extend(inferred)
    return tuple(dict.fromkeys(normalize_token(tag) for tag in tags if normalize_token(tag)))


def score_candidate(template_id: str, meta: dict, query_tags: set[str]) -> float:
    """Calculates matching similarity scores between a query and template registry profiles."""
    explicit_tags = {normalize_token(tag) for tag in meta.get("tags", ())}
    
    # Matched tags score
    matched = query_tags & explicit_tags
    score = 4.0 * len(matched)
    
    # Category and title checks
    title_text = meta.get("title", "").lower()
    for tag in query_tags:
        if tag in title_text:
            score += 1.5
            
    return score


def inspect_data_structure(
    columns: Sequence[str] | None = None,
    data_shape: tuple[int, ...] | None = None,
    df: Any | None = None
) -> dict[str, Any]:
    """
    Inspects columns, data shape, and types to infer semantic patterns:
    - has_time: time-like columns (Year, Date, Time, etc.)
    - has_country: geographic country name or ISO columns
    - has_coordinates: coordinate column keywords (lat, lon, x, y)
    - num_numeric: count of numeric columns
    - num_categorical: count of string/categorical columns
    """
    stats = {
        "has_time": False,
        "has_country": False,
        "has_coordinates": False,
        "num_numeric": 0,
        "num_categorical": 0,
        "cols_count": 0,
        "rows_count": 0
    }
    
    # Check if df is a real pandas DataFrame
    is_df = False
    try:
        import pandas as pd
        if isinstance(df, pd.DataFrame):
            is_df = True
    except ImportError:
        pass
        
    if is_df and df is not None:
        columns = list(df.columns)
        data_shape = df.shape
        
        # Analyze pandas columns directly
        for col in columns:
            col_lower = str(col).lower()
            # 1. Date/Time checks
            if any(k in col_lower for k in ["year", "date", "time", "month", "day", "timestamp", "epoch"]):
                stats["has_time"] = True
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                stats["has_time"] = True
                
            # 2. Coordinates checks
            if any(k == col_lower or k in col_lower for k in ["lat", "lon", "latitude", "longitude"]):
                stats["has_coordinates"] = True
                
            # 3. Country checks
            if any(k in col_lower for k in ["country", "iso", "nation", "region", "geo"]):
                stats["has_country"] = True
            else:
                # Check sample values for country codes/names
                sample_vals = df[col].dropna().head(10).astype(str).str.upper().str.strip()
                common_isos = {"USA", "CHN", "IND", "BRA", "RUS", "CAN", "DEU", "GBR", "FRA", "JPN", "AUS"}
                if any(val in common_isos for val in sample_vals):
                    stats["has_country"] = True
                    
            # 4. Numeric vs Categorical
            if pd.api.types.is_numeric_dtype(df[col]):
                stats["num_numeric"] += 1
            else:
                stats["num_categorical"] += 1
    else:
        # Fallback to column-name keywords
        if columns is not None:
            for col in columns:
                col_lower = str(col).lower()
                if any(k in col_lower for k in ["year", "date", "time", "month", "day"]):
                    stats["has_time"] = True
                if any(k in col_lower for k in ["lat", "lon", "latitude", "longitude"]):
                    stats["has_coordinates"] = True
                if any(k in col_lower for k in ["country", "iso", "nation", "region", "geo"]):
                    stats["has_country"] = True
                    
            # Guess types from names
            for col in columns:
                col_lower = str(col).lower()
                if any(k in col_lower for k in ["id", "name", "group", "class", "label", "category", "cat", "type", "country", "region"]):
                    stats["num_categorical"] += 1
                else:
                    stats["num_numeric"] += 1
                    
    if columns is not None:
        stats["cols_count"] = len(columns)
    if data_shape is not None:
        stats["rows_count"] = data_shape[0] if len(data_shape) > 0 else 0
        
    return stats


def select_template(
    user_request: str,
    columns: Sequence[str] | None = None,
    data_shape: tuple[int, ...] | None = None,
    df: Any | None = None
) -> TemplateMatch:
    """
    Programmatically selects the optimal plotting template matching the user request
    and structural column constraints.
    """
    query_tags = set(infer_tags_from_query(user_request))
    
    # Deeply inspect DataFrame structure and metadata
    stats = inspect_data_structure(columns, data_shape, df)
    
    results: list[TemplateMatch] = []
    for template_id, meta in TEMPLATES.items():
        score = score_candidate(template_id, meta, query_tags)
        
        # Determine expected fields from details or style profile
        required_fields_count = 2
        try:
            from template_registry import _DETAILS
            if template_id in _DETAILS:
                required_fields_count = len(_DETAILS[template_id][2])
        except Exception:
            pass
            
        # 1. Size match constraints (penalize if columns are insufficient)
        if stats["cols_count"] > 0 and stats["cols_count"] < required_fields_count:
            score -= 15.0
            
        # 2. Advanced structural affinity checks based on template metadata
        kind = meta.get("kind", "")
        category = meta.get("category", "")
        
        # Time Series matching
        if "time_series" in category or "time" in kind or "timeseries" in template_id:
            if stats["has_time"]:
                score += 8.0  # Time series pattern match!
            else:
                score -= 3.0  # Penalize if time column missing
                
        # Spatial Grid / Raster matching
        if "maps" in category and ("raster" in kind or "contour" in kind or "quiver" in kind or "hotspot" in template_id):
            if stats["has_coordinates"]:
                score += 10.0  # Perfect coordinates match!
            if stats["num_numeric"] >= 3:
                score += 4.0   # Matches lat, lon, raster values structure
                
        # Choropleth / Country matching
        if "maps" in category and ("choropleth" in kind or "country" in kind or "choropleth" in template_id):
            if stats["has_country"]:
                score += 10.0  # Perfect country identification match!
                
        # Category Group Distributions matching
        if "distributions" in category or kind in {"boxen", "model_boxplot", "violin_box", "faceted_boxplot"}:
            if stats["num_categorical"] >= 1 and stats["num_numeric"] >= 1:
                score += 6.0   # Matches category column + numeric values
                
        # Scatter/Regression matching
        if "scatter" in kind or "predicted_real" in kind or "parity" in kind:
            if stats["num_numeric"] >= 2:
                score += 5.0   # Matches paired quantitative variables
                
        # SHAP / ML Explainability matching
        if "shap" in kind or "ml_explainability" in category:
            if any(k in user_request.lower() for k in ["shap", "feature", "importance"]):
                score += 10.0
                
        matched_tags = sorted(list(query_tags & {normalize_token(tag) for tag in meta.get("tags", ())}))
        results.append(TemplateMatch(template_id, score, matched_tags))
        
    # Sort results in descending order of score
    results.sort(key=lambda match: -match.score)
    
    if len(results) > 0 and results[0].score > 0:
        return results[0]
        
    # Fallback to general scatter/boxen defaults
    default_id = "predicted_vs_real_scatter" if "预测" in user_request or "ML" in user_request else "boxen_plot"
    return TemplateMatch(default_id, 0.0, [])
