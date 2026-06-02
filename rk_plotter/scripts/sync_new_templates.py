from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from pathlib import Path

REQUIRED_FIELDS = (
    "rk_plotter_template", "id", "title", "category", "trigger_phrases", "tags",
    "data_profile", "style_profile", "dependencies", "best_for", "avoid_when",
)


@dataclass
class TemplateDoc:
    path: Path
    meta: dict[str, object]
    missing: list[str]


def parse_frontmatter(path: Path) -> TemplateDoc:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return TemplateDoc(path, {}, list(REQUIRED_FIELDS))
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return TemplateDoc(path, {}, list(REQUIRED_FIELDS))
    meta: dict[str, object] = {}
    current_key: str | None = None
    section_key: str | None = None
    for line in parts[1].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" ") and ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            section_key = None
            if value:
                meta[key] = True if value.lower() == "true" else False if value.lower() == "false" else value
            else:
                meta[key] = [] if key in {"trigger_phrases", "tags"} else {}
        elif line.startswith("  - ") and current_key:
            meta.setdefault(current_key, [])
            if isinstance(meta[current_key], list):
                meta[current_key].append(line.strip()[2:].strip())
        elif line.startswith("  ") and not line.startswith("    ") and ":" in line and current_key:
            subkey, value = line.strip().split(":", 1)
            if isinstance(meta.get(current_key), dict):
                section_key = subkey.strip()
                meta[current_key][section_key] = value.strip() or []
        elif line.startswith("    - ") and current_key and section_key:
            section = meta.get(current_key)
            if isinstance(section, dict):
                section.setdefault(section_key, [])
                if isinstance(section[section_key], list):
                    section[section_key].append(line.strip()[2:].strip())
    missing = [field for field in REQUIRED_FIELDS if field not in meta or meta[field] in (None, "", [], {})]
    if meta.get("rk_plotter_template") is not True and "rk_plotter_template" not in missing:
        missing.append("rk_plotter_template")
    return TemplateDoc(path, meta, missing)


def render_index(target: Path) -> str:
    docs = [parse_frontmatter(path) for path in sorted(target.glob("*.md"))]
    docs = [doc for doc in docs if not doc.missing]
    lines = [
        "# rk_plotter 模板索引",
        "",
        "正式模板只来自 `templates/*.md`；`new_templates/` 是上传暂存区，未同步前不参与绘图匹配。",
        "",
        "| ID | 类别 | 标题 | 触发词 | 标签 | 数据结构 | 布局/比例 | 模板文件 |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for doc in docs:
        meta = doc.meta
        triggers = "; ".join(meta.get("trigger_phrases", [])[:4]) if isinstance(meta.get("trigger_phrases"), list) else ""
        tags = ", ".join(meta.get("tags", [])[:8]) if isinstance(meta.get("tags"), list) else ""
        data_profile = meta.get("data_profile", {})
        style_profile = meta.get("style_profile", {})
        structure = data_profile.get("structure", "") if isinstance(data_profile, dict) else ""
        layout = ""
        if isinstance(style_profile, dict):
            layout = f"{style_profile.get('layout', '')} / {style_profile.get('aspect', '')}"
        template_path = meta.get("template_path") or f"templates/{doc.path.name}"
        lines.append(f"| `{meta.get('id')}` | {meta.get('category')} | {meta.get('title')} | {triggers} | `{tags}` | {structure} | {layout} | `{template_path}` |")
    lines.extend([
        "",
        "## 使用规则",
        "",
        "1. 先根据用户数据和绘图任务在本表中匹配触发词、标签和数据结构。",
        "2. 命中后再读取对应 `templates/*.md` 全文，保留原模板构图、配色、比例和特殊 artist 逻辑。",
        "3. 多个候选接近时，同时读取候选模板全文，对比 `best_for` 与 `avoid_when` 后择优或组合。",
        "4. 不读取 `new_templates/` 作为绘图入口；只有用户要求同步时才处理暂存模板。",
        "",
    ])
    return "\n".join(lines)


def sync(source: Path, target: Path, index: Path, *, dry_run: bool, move: bool) -> int:
    source.mkdir(parents=True, exist_ok=True)
    target.mkdir(parents=True, exist_ok=True)
    docs = [parse_frontmatter(path) for path in sorted(source.glob("*.md"))]
    if not docs:
        print(f"No markdown templates found in {source}")
        return 0
    existing_ids: dict[str, Path] = {}
    for path in sorted(target.glob("*.md")):
        doc = parse_frontmatter(path)
        tid = doc.meta.get("id")
        if isinstance(tid, str):
            existing_ids[tid] = path
    blocked = False
    for doc in docs:
        print(f"Template: {doc.path.name}")
        if doc.missing:
            blocked = True
            print("  status: missing required metadata")
            print("  missing: " + ", ".join(doc.missing))
            continue
        tid = doc.meta.get("id")
        dest = target / doc.path.name
        if isinstance(tid, str) and tid in existing_ids:
            blocked = True
            print(f"  status: id conflict with {existing_ids[tid]}")
            continue
        if dest.exists():
            blocked = True
            print(f"  status: filename conflict with {dest}")
            continue
        print(f"  status: ready -> {dest}")
    if blocked:
        print("Sync blocked. Fix missing metadata or conflicts first.")
        return 1
    if dry_run:
        print("Dry run only; no files copied.")
        return 0
    for doc in docs:
        dest = target / doc.path.name
        if move:
            shutil.move(str(doc.path), str(dest))
        else:
            shutil.copy2(doc.path, dest)
    index.parent.mkdir(parents=True, exist_ok=True)
    index.write_text(render_index(target), encoding="utf-8", newline="\n")
    print(f"Updated index: {index}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sync staged Markdown templates into rk_plotter/templates.")
    parser.add_argument("--source", type=Path, default=Path("new_templates"))
    parser.add_argument("--target", type=Path, default=Path("templates"))
    parser.add_argument("--index", type=Path, default=Path("references/template-index.md"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--move", action="store_true", help="Move staged templates instead of copying them.")
    args = parser.parse_args(argv)
    return sync(args.source, args.target, args.index, dry_run=args.dry_run, move=args.move)


if __name__ == "__main__":
    raise SystemExit(main())
