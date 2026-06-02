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


def select_template(
    user_request: str,
    columns: Sequence[str] | None = None,
    data_shape: tuple[int, ...] | None = None
) -> TemplateMatch:
    """
    Programmatically selects the optimal plotting template matching the user request
    and structural column constraints.
    """
    query_tags = set(infer_tags_from_query(user_request))
    
    results: list[TemplateMatch] = []
    for template_id, meta in TEMPLATES.items():
        score = score_candidate(template_id, meta, query_tags)
        
        # Hard limits on shape/columns compatibility (custom checks)
        # e.g., mapping templates need at least 2 columns, spatial grid needs 2D or long/lat
        if columns is not None:
            required_fields_count = len(meta.get("data_profile", {}).get("required_fields", ("x", "y")))
            if len(columns) < required_fields_count:
                # Incompatible columns size - penalize heavily
                score -= 10.0
                
        matched_tags = sorted(list(query_tags & {normalize_token(tag) for tag in meta.get("tags", ())}))
        results.append(TemplateMatch(template_id, score, matched_tags))
        
    # Sort results in descending order of score
    results.sort(key=lambda match: -match.score)
    
    if len(results) > 0 and results[0].score > 0:
        return results[0]
        
    # Fallback to general scatter/boxen defaults
    default_id = "predicted_vs_real_scatter" if "预测" in user_request or "ML" in user_request else "boxen_plot"
    return TemplateMatch(default_id, 0.0, [])
