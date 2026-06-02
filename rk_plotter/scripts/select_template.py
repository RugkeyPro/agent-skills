from __future__ import annotations

import argparse
import json
import re
from typing import Any, Iterable

import sys
from pathlib import Path
_scripts_dir = str(Path(__file__).resolve().parent)
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

from template_registry import CATEGORIES, TEMPLATES

TOKEN_SPLIT_RE = re.compile(r"[^a-z0-9_]+")
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
QUERY_RULES = (
    (("地图", "经纬度", "栅格", "热点", "风险", "暴露", "map", "raster", "spatial"), ("spatial", "lon_lat_grid", "continuous_field")),
    (("国家", "行政区", "choropleth", "country"), ("spatial", "choropleth", "country")),
    (("对数", "数量级", "log"), ("log_scale",)),
    (("方向", "流场", "风场", "quiver", "vector"), ("vector_field", "quiver")),
    (("分布", "两组", "多组", "distribution", "box", "violin"), ("distribution", "grouped_samples", "category_comparison")),
    (("联合密度", "joint", "bivariate"), ("distribution", "paired_samples", "joint_density")),
    (("kde", "核密度"), ("distribution", "kde", "density")),
    (("预测", "实测", "观测", "predicted", "observed", "parity"), ("prediction", "observed", "predicted", "one_to_one", "model_diagnostic")),
    (("情景", "scenario", "ssp", "rcp"), ("scenario", "time_series", "multi_line")),
    (("不确定", "置信", "区间", "uncertainty", "confidence"), ("uncertainty_band",)),
    (("组成", "比例", "百分比", "composition", "percent", "stacked"), ("composition", "percent", "groups")),
    (("正负", "贡献", "diverging"), ("composition", "diverging", "signed")),
    (("shap", "特征效应"), ("shap", "features", "effects")),
    (("重要性", "importance"), ("shap", "features", "importance")),
    (("框架", "流程", "概念", "framework", "workflow"), ("framework", "conceptual", "workflow")),
)


def normalize_token(value: Any) -> str:
    token = str(value).strip().lower().replace("-", "_").replace(" ", "_")
    token = TOKEN_SPLIT_RE.sub("_", token)
    return re.sub(r"_+", "_", token).strip("_")


def parse_tags(raw: str | None) -> tuple[str, ...]:
    if not raw:
        return ()
    parts: list[str] = []
    for chunk in raw.split(","):
        parts.extend(chunk.strip().split())
    return tuple(token for token in (normalize_token(part) for part in parts) if token)


def expand_tags(tags: Iterable[str]) -> tuple[str, ...]:
    expanded: list[str] = []
    for tag in tags:
        token = normalize_token(tag)
        if not token:
            continue
        expanded.append(token)
        expanded.extend(TAG_ALIASES.get(token, ()))
    return tuple(dict.fromkeys(expanded))


def infer_tags(query: str | None) -> tuple[str, ...]:
    if not query:
        return ()
    text = query.lower()
    tags: list[str] = []
    for keywords, inferred in QUERY_RULES:
        if any(keyword.lower() in text for keyword in keywords):
            tags.extend(inferred)
    return tuple(dict.fromkeys(normalize_token(tag) for tag in tags if normalize_token(tag)))


def flatten_tokens(value: Any) -> set[str]:
    tokens: set[str] = set()
    if value is None:
        return tokens
    if isinstance(value, dict):
        for key, item in value.items():
            tokens.add(normalize_token(key))
            tokens.update(flatten_tokens(item))
        return tokens
    if isinstance(value, (list, tuple, set)):
        for item in value:
            tokens.update(flatten_tokens(item))
        return tokens
    text = str(value)
    tokens.add(normalize_token(text))
    for part in re.split(r"[,;/\s]+", text):
        token = normalize_token(part)
        if token:
            tokens.add(token)
    return tokens


def score_template(template_id: str, meta: dict[str, Any], query_tags: Iterable[str]) -> dict[str, Any]:
    query = set(query_tags)
    explicit_tags = {normalize_token(tag) for tag in meta.get("tags", ())}
    data_tokens = flatten_tokens(meta.get("data_profile", {}))
    style_tokens = flatten_tokens(meta.get("style_profile", {}))
    text_tokens = flatten_tokens((meta.get("title"), meta.get("use"), meta.get("best_for"), meta.get("avoid_when")))
    category_tokens = {normalize_token(meta.get("category", "")), normalize_token(meta.get("kind", ""))}

    matched_tags = sorted(query & explicit_tags)
    data_matches = sorted((query - set(matched_tags)) & data_tokens)
    style_matches = sorted((query - set(matched_tags) - set(data_matches)) & style_tokens)
    category_matches = sorted((query - set(matched_tags) - set(data_matches) - set(style_matches)) & category_tokens)
    text_matches = sorted(
        (query - set(matched_tags) - set(data_matches) - set(style_matches) - set(category_matches)) & text_tokens
    )

    score = 0.0
    score += 4.0 * len(matched_tags)
    score += 3.0 * len(data_matches)
    score += 2.0 * len(style_matches)
    score += 2.0 * len(category_matches)
    score += 1.0 * len(text_matches)

    all_matches = sorted(set(matched_tags + data_matches + style_matches + category_matches + text_matches))
    return {
        "id": meta.get("id", template_id),
        "template_id": template_id,
        "score": score,
        "matched": all_matches,
        "missing": sorted(query - set(all_matches)),
        "title": meta["title"],
        "category": meta["category"],
        "kind": meta["kind"],
        "use": meta["use"],
        "best_for": meta["best_for"],
        "avoid_when": meta["avoid_when"],
        "data_shape": meta.get("data_shape", meta["data_profile"].get("shape")),
        "coordinates": meta.get("coordinates", "cartesian"),
        "data_profile": meta["data_profile"],
        "style_profile": meta["style_profile"],
        "source_file": meta.get("source_file", meta["original"]),
        "original": meta["original"],
        "preview": meta["preview"],
        "optional_requires": meta.get("optional_requires", ()),
    }


def recommend(tags: Iterable[str], category: str | None = None, top: int = 5) -> list[dict[str, Any]]:
    category_norm = normalize_token(category) if category else None
    query_tags = expand_tags(tags)
    results: list[dict[str, Any]] = []
    for template_id, meta in TEMPLATES.items():
        if category_norm and normalize_token(meta["category"]) != category_norm:
            continue
        result = score_template(template_id, meta, query_tags)
        if query_tags and result["score"] <= 0:
            continue
        if category_norm:
            result["score"] += 1.5
            result["matched"] = sorted(set(result["matched"] + [category_norm]))
        results.append(result)
    results.sort(key=lambda item: (-item["score"], item["category"], item["template_id"]))
    return results[: max(top, 1)]


def format_result(item: dict[str, Any], index: int, explain: bool = False) -> str:
    style = item["style_profile"]
    data = item["data_profile"]
    line = f"{index}. {item['template_id']} | score={item['score']:.1f} | {item['title']} [{item['category']}/{item['kind']}]"
    if not explain:
        return line
    matched = ", ".join(item["matched"]) or "-"
    missing = ", ".join(item["missing"]) or "-"
    optional = ", ".join(item["optional_requires"]) or "-"
    return "\n".join(
        [
            line,
            f"   matched: {matched}; missing: {missing}",
            f"   use: {item['use']}",
            f"   data: {item.get('data_shape') or data.get('shape')} | coordinates: {item.get('coordinates')} | fields: {', '.join(data.get('required_fields', ())) or '-'}",
            f"   style: figsize={tuple(style.get('figsize', ()))}, aspect={style.get('aspect')}, palette={style.get('palette')}, cmap={style.get('cmap') or '-'}, scale={', '.join(style.get('scale', ())) or '-'}",
            f"   primitives: {', '.join(style.get('plot_primitives', ())) or '-'} | layout: {', '.join(style.get('layout', ())) or '-'}",
            f"   best_for: {item['best_for']}",
            f"   avoid_when: {item['avoid_when']}",
            f"   source: {item.get('source_file', item['original'])} | preview: {item['preview']} | optional deps: {optional}",
        ]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Recommend rk_plotter templates from data/style tags.")
    parser.add_argument("--tags", default="", help="Comma- or space-separated tags, e.g. spatial,lon_lat_grid,log_scale")
    parser.add_argument("--query", default="", help="Free-text plotting need; common Chinese/English phrases are mapped to tags.")
    parser.add_argument("--category", choices=CATEGORIES, help="Restrict recommendations to one category.")
    parser.add_argument("--top", type=int, default=5, help="Number of recommendations to show.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument("--explain", action="store_true", help="Show matching rationale and style/data profile.")
    args = parser.parse_args(argv)

    query_tags = tuple(dict.fromkeys((*parse_tags(args.tags), *infer_tags(args.query))))
    results = recommend(query_tags, category=args.category, top=args.top)
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for index, item in enumerate(results, start=1):
            print(format_result(item, index, explain=args.explain))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
