# 期刊维度参考：各刊结构规格与叙事风格

> 这是"按期刊"组织的唯一权威来源。判断目标刊后，只读本文件中对应一节即可。章节内部写法见 `sections.md`，句子层规则见 `style-rules.md`。

---

## 速查对比表

| 特征 | Nature 正刊 | Nature Communications (NC) | NCC / NS / NEE / NG |
|------|------------|---------------------------|---------------------|
| Introduction 标题 | 无（"Main"替代） | 无，或"Introduction" | 通常有"Introduction" |
| Results / Discussion | 合并于"Main" | 灵活（可分可合，"Results and Discussion"常见） | 通常分开 |
| Abstract 长度 | ~150 词，叙事性强 | ~200 词，指标密集 | ~180 词，情景导向 |
| Methods | 精简，置于文末 | 独立、可详实 | 独立、中等长度 |
| 正文字数 | 3000–4000 | 5000–8000 | 5000–8000 |
| 参考文献量 | ~30–50 | ~50–80 | ~40–70 |

判断目标刊后，先定结构骨架（本表），再按章节填充（`sections.md` + `templates.md`）。

---

## Nature 正刊（Article）

结构特征：
- **无独立 Introduction 标题**：正文以 "Main" 为整体标题，引言自然嵌入开头。
- **Results 与 Discussion 不分开**：融合在 "Main" 的连续叙事中，按逻辑推进而非小节划分。
- **极简 Methods 在文末**：详细方法放入 Extended Data / Supplementary Information。
- **Abstract 极短（约 150 词）**：强调"一个核心发现"的叙事弧线，可不堆数字，但需 1–2 个核心定量结果。
- 正文高度精炼。

正刊 Main 的过渡与结论句法（从真实论文提取）：
- `We begin by describing [X], and then go on to show [Y].`
- `Having established [X], we next asked whether [Y].`
- `Our results support the first part of this expectation ([A]) while challenging the expectation that [B].`
- `Nevertheless, we believe our [model/study] is an important step towards [broader goal].`
- `There is a need for more extensive monitoring of [X] with [specific recommendation].`

Main 结构骨架见 `templates.md` 的"正刊 Main 结构模板"。

---

## Nature Communications (NC)

结构特征：
- 首段直接充当引言（多无 "Introduction" 标题）。
- "Results and Discussion" 合并形式常见且可接受。
- 有独立、可详实的 Methods 节。
- Abstract 较长（180–250 词），指标密集，可含具体数字甚至公式/算法概述。
- 图表标题可更详细，含方法关键参数。

NC 的 Abstract 走"五句式"（背景+数据 → 缺口/挑战 → Here we → 2–3 句定量结果 → 意义+应用），模板见 `templates.md`。

---

## Nature Climate Change (NCC)

风格特征：
- **"因果链"叙事**：气候变化 → 气候变量变化 → 生态响应 → 生态系统服务影响。Introduction 与 Discussion 都应让这条链清晰可见。
- **情景对比驱动**：贯穿全文使用多种 SSP/RCP 情景对比。
- **缩放逻辑**：全球平均 → 按生物群系(biome)分区 → 按纬度/区域分解。
- 关键术语：projected shifts, ensemble mean, trophic amplification, under climate change, SSP scenarios。

因果链与情景句式见 `phrase-bank.md` 的 NCC 节。

---

## Nature Sustainability (NS)

风格特征：
- **"科学发现 → 管理建议"桥梁**：Results 后须有专门的 policy / management implications 部分。
- **政策导向句式**：`We advocate / We suggest / We urge / Our results can provide guidance for...`
- **不确定性透明化**：先坦诚局限，再给政策建议。
- 关键术语：sustainability perspective, mitigation measures, actionable insights, long-term resilience, biodiversity targets。

---

## Nature Ecology & Evolution (NEE)

风格特征：
- **Research article**：强调进化/生态机制，区别于 NCC 的"环境驱动"叙事。
- **Perspective / Commentary 特殊结构**：让步开头（`[Established method] is a powerful tool for...`）→ 转折（`However, [misapplication] will lead to...`）→ 分层论证（每个论点都有引用）→ 强结语（带警示或建议）。
- **高密度引用**：观点文章几乎每句都有引用支撑。

---

## Nature Geoscience (NG)

风格特征：
- **"突破性发现"驱动**：Abstract 开篇即点出颠覆性结果。
- **量化对比强化**：`threefold greater than`, `only 0.2% of X but receive 27% of Y`。
- **多数据源交叉验证**：强调方法严谨性。
- 局限性可坦诚，但要把工作定位为"提供突破性观测证据"。
- 关键术语：observation-constrained, mechanistic model, uncertainty bracketing。

NG 突破性证据句式见 `phrase-bank.md` 的 NG 节。

---

## Science / Science Advances（如目标刊为此）

### Science（与 Nature 正刊的差异）
- **新闻价值优先**：Abstract 第一句必须抓住非专业读者。
- **更短正文**：8–12 段，约 2000–3000 词。
- **Methods 在补充材料**：正文不设 Methods。
- **无独立 Introduction 标题**：首段直接作引言。
- **更强故事性**：善用引文、隐喻、文化参照。
- 用 `Here we show/report/document`（而非 Nature 的 `Here we present/use`）。

### Science Advances（与 NC 的差异）
- 有明确 Introduction 标题（不同于 Science）。
- 有独立 Methods 节在正文（类似 NC）。
- Abstract 略长（150–200 词）。
- 在 Science 的"新闻价值"与 NC 的"技术完整性"之间取平衡。
