#!/usr/bin/env python3
"""
Nature-Writer 硬规则机械校验器。

把 SKILL.md 里的 0/1 硬规则交给脚本判定，比模型自检更稳，且每次生成/润色后可复用。
不做风格评判（那是模型的工作），只检查可机械判定的项。

用法:
    python lint.py <文本文件>            # 校验整篇/整段
    python lint.py --section methods <文件>   # 指定章节，启用该节专属检查
    echo "some text" | python lint.py -      # 从 stdin 读取

章节可选: abstract / introduction / methods / results / discussion / main
词数上限按章节+期刊近似设定，可用 --journal 调整 Abstract 上限。

退出码: 0 = 无 ERROR；1 = 存在 ERROR（WARN 不影响退出码）。
"""
import argparse
import re
import sys

# Abstract 词数上限（近似，见 references/journals.md）
ABSTRACT_LIMIT = {"nature": 180, "nc": 250, "ncc": 200, "ns": 200, "nee": 200, "ng": 200, "default": 250}

# Methods 中不应出现的结果性词汇（提示混入了 Results）
RESULTS_WORDS = [
    r"\bwe found\b", r"\bwe find\b", r"\bresults? (?:show|showed|indicate|revealed?)\b",
    r"\bsignificant(?:ly)?\b", r"\bour findings?\b", r"\bdemonstrated that\b",
    r"\bwas higher\b", r"\bwas lower\b", r"\bincreased by\b", r"\bdecreased by\b",
]

# 过度确定的措辞
OVERCERTAIN = [r"\bproves? that\b", r"\bconclusively shows?\b", r"\bconfirms? that\b"]


def find_em_dashes(text):
    # em dash (—, U+2014) 和 horizontal bar (―, U+2015)，禁用
    hits = []
    for m in re.finditer(r"[—―]", text):
        s = max(0, m.start() - 30)
        e = min(len(text), m.end() + 30)
        hits.append(text[s:e].replace("\n", " ").strip())
    return hits


def find_unspaced_hyphen_range(text):
    # 数值范围应使用 en dash（–），若用 ASCII 连字符连接两个数字则提示
    return re.findall(r"\d+\s*-\s*\d+", text)


def check_abbrev_first_use(text):
    """缩写首次出现是否给了全称(缩写)。
    启发式：找到 '(ABC)' 形式定义过的缩写；对未经定义就出现的全大写缩写(2-6字母)给出 WARN。
    会跳过常见单位/通用缩写以降低噪音。
    """
    SKIP = {"AND", "THE", "FOR", "WITH", "DNA", "RNA", "PH", "USA", "UK", "CO2", "AI",
            "CI", "SD", "SE", "GHG", "GDP", "II", "III", "IV", "PFAS"}
    defined = set(re.findall(r"\(([A-Z][A-Za-z0-9]{1,6})\)", text))
    warns = []
    seen = set()
    for m in re.finditer(r"\b([A-Z]{2,6})\b", text):
        ab = m.group(1)
        if ab in SKIP or ab in defined or ab in seen:
            continue
        seen.add(ab)
        s = max(0, m.start() - 25)
        warns.append((ab, text[s:m.end() + 5].replace("\n", " ").strip()))
    return warns


def word_count(text):
    return len(re.findall(r"\b[\w'-]+\b", text))


def lint(text, section=None, journal="default"):
    errors, warns = [], []

    em = find_em_dashes(text)
    for h in em:
        errors.append(f"破折号(em dash): …{h}…  → 改用逗号/冒号/分号/括号")

    for r in find_unspaced_hyphen_range(text):
        warns.append(f"数值范围疑似用了 ASCII '-' 而非 en dash '–': '{r}'")

    for pat in OVERCERTAIN:
        for m in re.finditer(pat, text, re.I):
            warns.append(f"过度确定措辞: '{m.group(0)}' → 改用 suggest/indicate/demonstrate")

    wc = word_count(text)

    if section == "methods":
        for pat in RESULTS_WORDS:
            for m in re.finditer(pat, text, re.I):
                errors.append(f"Methods 混入结果性表述: '{m.group(0)}' → Methods 只描述方法，不展示结果")

    if section == "abstract":
        limit = ABSTRACT_LIMIT.get(journal, ABSTRACT_LIMIT["default"])
        if wc > limit:
            errors.append(f"Abstract {wc} 词，超过 {journal} 上限 ~{limit} 词")
        if not re.search(r"\d", text):
            warns.append("Abstract 未见任何数字，顶刊摘要应含至少 1 个定量发现")
        if re.search(r"\[\s*\d+\s*\]|\(\s*[A-Z][a-z]+ et al", text):
            warns.append("Abstract 疑似含参考文献引用，通常应去除")

    if section in ("introduction", "main"):
        if not re.search(r"\bHere,?\s+we\b|\bIn this study,?\s+we\b", text, re.I):
            warns.append("Introduction/Main 未见 'Here, we...' 类目标句(P5)")
        if not re.search(r"\b(However|Nevertheless|Yet|Despite|remains? (?:unclear|unknown|poorly understood))\b", text, re.I):
            warns.append("Introduction/Main 未见明确的研究缺口转折句(P3)")

    for ab, ctx in check_abbrev_first_use(text):
        warns.append(f"缩写 '{ab}' 首次出现疑未给全称: …{ctx}…")

    return errors, warns, wc


def main():
    p = argparse.ArgumentParser(description="Nature-Writer 硬规则校验")
    p.add_argument("file", help="文本文件路径，'-' 表示 stdin")
    p.add_argument("--section", choices=["abstract", "introduction", "methods", "results", "discussion", "main"])
    p.add_argument("--journal", default="default", help="nature/nc/ncc/ns/nee/ng（影响 Abstract 词数上限）")
    args = p.parse_args()

    text = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8").read()

    errors, warns, wc = lint(text, args.section, args.journal.lower())

    print(f"词数: {wc}" + (f"  | 章节: {args.section}" if args.section else ""))
    if errors:
        print(f"\n❌ ERROR ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
    if warns:
        print(f"\n⚠️  WARN ({len(warns)}):")
        for w in warns:
            print(f"  - {w}")
    if not errors and not warns:
        print("✅ 通过：未发现硬规则问题")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
