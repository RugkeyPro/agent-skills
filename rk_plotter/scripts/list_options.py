from __future__ import annotations

import argparse
import json
from pathlib import Path


PALETTES = [
    {
        "id": "original_template",
        "name": "Original template palette",
        "best_for": "Preserving the selected template's high-fidelity visual identity.",
        "colors": "Defined inside the selected template.",
    },
    {
        "id": "okabe_ito",
        "name": "Okabe-Ito colorblind-safe categorical",
        "best_for": "Groups, classes, scenarios, and legends with distinct categories.",
        "colors": ["#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377", "#BBBBBB"],
    },
    {
        "id": "scenario",
        "name": "Scenario time-series categorical",
        "best_for": "SSP/RCP/pathway or multi-scenario line charts.",
        "colors": ["#1B9E77", "#D95F02", "#7570B3", "#E7298A", "#66A61E", "#E6AB02"],
    },
    {
        "id": "sequential_blue",
        "name": "Sequential blue",
        "best_for": "Ordered intensity, concentration, load, or risk values.",
        "colors": ["#F7FBFF", "#C6DBEF", "#6BAED6", "#2171B5", "#08306B"],
    },
    {
        "id": "hotspot_green_yellow_red",
        "name": "Green-yellow-red hotspot",
        "best_for": "Hotspot, risk, exceedance, and priority-area maps.",
        "colors": ["#1A9850", "#91CF60", "#FFFFBF", "#FC8D59", "#D73027"],
    },
    {
        "id": "diverging_blue_red",
        "name": "Diverging blue-red",
        "best_for": "Anomalies, differences, positive/negative change, and residuals.",
        "colors": ["#2166AC", "#67A9CF", "#F7F7F7", "#EF8A62", "#B2182B"],
    },
    {
        "id": "log_risk",
        "name": "Log-scale risk/load",
        "best_for": "Log-normal loads, exposure, concentration, or skewed raster fields.",
        "colors": ["#2C7BB6", "#00A6CA", "#FFFF8C", "#FDAE61", "#D7191C", "#7B3294"],
    },
    {
        "id": "density_mako",
        "name": "Seaborn mako density",
        "best_for": "High-density scatter and KDE-like point clouds.",
        "colors": "mako colormap",
    },
]

LEGEND_COLORBAR_PLANS = [
    "patch legend",
    "symbol-size legend",
    "categorical legend",
    "top compact legend",
    "bottom multi-column legend",
    "horizontal colorbar",
    "vertical colorbar",
    "inset colorbar",
    "combined legend and colorbar",
]

STATISTICAL_DISPLAY_PLANS = [
    "none",
    "confidence interval band",
    "error bars",
    "fitted regression line",
    "1:1 reference line",
    "threshold/reference line",
    "significance marks",
    "panel labels",
    "metric annotation box",
    "value annotations",
]

MAP_PLANS = [
    "PlateCarree projection",
    "Robinson projection",
    "custom lon/lat extent",
    "central longitude",
    "land/ocean color choices",
    "coastlines and borders",
    "province/administrative boundaries",
    "gridline/tick labels",
    "inset map",
    "contour overlay",
    "quiver arrows",
    "significant/hotspot mask overlay",
]


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_manifest() -> dict:
    manifest_path = skill_root() / "templates" / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(
            f"templates/manifest.json not found at {manifest_path}. "
            "It is the single source of truth for templates."
        )
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def collect_options() -> dict[str, object]:
    manifest = load_manifest()
    templates = manifest.get("templates", [])
    return {
        "templates": templates,
        "families": manifest.get("families", {}),
        "template_ids": [t["id"] for t in templates],
        "palettes": PALETTES,
        "legend_colorbar_plans": LEGEND_COLORBAR_PLANS,
        "statistical_display_plans": STATISTICAL_DISPLAY_PLANS,
        "map_plans": MAP_PLANS,
    }


def as_markdown(options: dict[str, object], sections: set[str]) -> str:
    lines: list[str] = []

    if "templates" in sections:
        families = options["families"]
        assert isinstance(families, dict)
        templates = options["templates"]
        assert isinstance(templates, list)
        lines.append("## Templates and Modes (grouped by family)")
        by_family: dict[str, list[dict]] = {}
        for tpl in templates:
            by_family.setdefault(tpl["family"], []).append(tpl)
        for family_id, label in families.items():
            members = by_family.get(family_id, [])
            if not members:
                continue
            lines.append(f"\n### {family_id} — {label}")
            for tpl in members:
                modes = tpl.get("modes", ["default"])
                modes_str = ", ".join(modes)
                req = ", ".join(tpl.get("required_fields", []))
                deps = tpl.get("deps", [])
                deps_str = f" [deps: {', '.join(deps)}]" if deps else ""
                alias = f" (alias → {tpl['alias_of']})" if tpl.get("alias_of") else ""
                preview = f" [preview: {tpl['preview']}]" if tpl.get("preview") else ""
                lines.append(
                    f"- `{tpl['id']}`{alias} | modes: {modes_str} | required: {req}{deps_str}{preview}"
                )
        lines.append("")

    if "palettes" in sections:
        lines.append("## Palette and Color-Scheme Options")
        for palette in options["palettes"]:
            assert isinstance(palette, dict)
            lines.append(f"- `{palette['id']}`: {palette['name']} - {palette['best_for']} Colors: {palette['colors']}")
        lines.append("")

    if "legend" in sections:
        lines.append("## Legend and Colorbar Options")
        for plan in options["legend_colorbar_plans"]:
            lines.append(f"- {plan}")
        lines.append("")

    if "statistics" in sections:
        lines.append("## Statistical Display Options")
        for plan in options["statistical_display_plans"]:
            lines.append(f"- {plan}")
        lines.append("")

    if "maps" in sections:
        lines.append("## Map Options")
        for plan in options["map_plans"]:
            lines.append(f"- {plan}")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="List rk_plotter template and style choices (manifest-driven).")
    parser.add_argument(
        "--section",
        action="append",
        choices=["templates", "palettes", "legend", "statistics", "maps"],
        help="Section to print. Repeatable. Defaults to all sections.",
    )
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)

    sections = set(args.section or ["templates", "palettes", "legend", "statistics", "maps"])
    options = collect_options()

    if args.format == "json":
        key_map = {
            "templates": ["templates", "families", "template_ids"],
            "palettes": ["palettes"],
            "legend": ["legend_colorbar_plans"],
            "statistics": ["statistical_display_plans"],
            "maps": ["map_plans"],
        }
        wanted: set[str] = set()
        for section in sections:
            wanted.update(key_map[section])
        filtered = {key: value for key, value in options.items() if key in wanted}
        print(json.dumps(filtered, indent=2, ensure_ascii=False))
    else:
        print(as_markdown(options, sections), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
