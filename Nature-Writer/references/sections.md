# 章节维度参考：各章节写法 + CEI 段落模型

> 这是"按章节"组织的唯一权威来源。CEI 论证模型在本文件定义一次，其他文件只引用。填空式整段骨架见 `templates.md`，可套用句式见 `phrase-bank.md`，句子层规则（时态/标点/语态）见 `style-rules.md`。

---

## 段落黄金模型：Claim–Evidence–Interpretation (CEI)

无论 Introduction、Results 还是 Discussion，每一段都应尽量遵循此模型：

- **第一句 — Claim（主张）**：本段核心论点，一句话概括，即 topic sentence。
- **中间句 — Evidence（证据）**：支撑论点的数据、引用、统计或逻辑推理。
- **末句 — Interpretation/Significance（解释/意义）**：说明这个发现意味着什么。

Results 中的 CEI 示例：
> **Claim:** Global zooplankton biomass declined by 7–16% from 1980 to 2100.
> **Evidence:** Omnivorous zooplankton biomass exhibited the greatest decline of 8–18%, whereas filter feeders experienced a more modest decline of up to 6%.
> **Interpretation:** These declines are primarily caused by projected declines in phytoplankton biomass, with warming acting as a secondary driver.

Introduction 中的 CEI 示例：
> **Claim:** Zooplankton community structure determines energy transfer efficiency.
> **Evidence:** Communities dominated by carnivorous copepods (PPMR < 100) transfer less energy than those dominated by filter feeders (PPMR > 6 million).
> **Interpretation:** Better accounting for zooplankton functional traits will therefore improve understanding of energy flow.

注意区分两种 Interpretation 的深度：Results 里限于"结果内部的解释"（数据模式的成因）；机制层面的深入讨论属于 Discussion。

---

## Abstract（摘要）

按"四句式"结构压缩，词数随刊（正刊 ~150、NC 180–250、其他子刊 ~180，详见 `journals.md`）：

1. **背景/重要性**：1 句锚定问题意义。避免空洞的 "The world is facing..."，用具体事实。正刊更宏大叙事，子刊更技术性。
2. **核心缺口**：1–2 句指出现有不足（remains unclear / poorly understood / has not been established）。这是 Abstract 的张力点。
3. **本方法与核心发现**：2–3 句给方法概述和最重要的量化发现。子刊须含具体数字（百分比、范围、置信区间），正刊至少 1–2 个核心定量结果。
4. **意义与影响**：1 句收尾，说明对管理/政策/科学认知的价值。

三种刊型的句法骨架：

> **A — 正刊（叙事优先）**：`[Topic] poses a critical challenge to [system]. Despite [existing knowledge], [key gap] remains largely unknown. Here we [develop/present] [method] to [objective]. We estimate that [quantitative finding]. Our results suggest that [broader implication], highlighting [significance].`

> **B — NC（指标密集）**：`[Topic] plays a fundamental role in [process]. Yet, current approaches remain inadequate for [goal], limited by [challenge]. Here we [develop] [method], achieving [key metric]. We find that [result 1] and [result 2]. Our results enable [application], providing [insight].`

> **C — NS（政策导向）**：`[Topic] is of growing concern due to [impact]. However, the extent of [X] remains unclear, hindering [policy]. Here we quantify [X] using [method]. We find that [finding with policy relevance]. These results underscore the need for [action].`

真实正刊范例（河流塑料，Nature）：
> *"Plastics in the marine environment have become a major concern because of their persistence at sea... Here we present a global model of plastic inputs from rivers into oceans based on waste management, population density and hydrological information. We estimate that between 1.15 and 2.41 million tonnes of plastic waste currently enters the ocean every year from rivers, with over 74% of emissions occurring between May and October."*

填空模板见 `templates.md` 的 Abstract 模板 A–D。

---

## Introduction（引言）

"漏斗式"结构：宏观 → 领域 → 具体问题 → 本研究。通常 4–6 段，严格按序不可跳跃：

- **P1（全球/学科背景）**：1–2 个具体事实锚定领域重要性，句末出现一个量化数据。
- **P2（已知知识）**：综述已有框架，引用经典文献，建立读者共识。
- **P3（研究缺口 — 张力核心）**：以 However / Nevertheless / Yet / Despite 明确转折，指出具体缺口。**全文最重要的一段**，张力越具体，研究必要性越强。从此段起每段至少 2–3 篇文献支撑。
- **P4（聚焦对象，可选）**：介绍研究物种/区域/系统的特殊性与重要性。
- **P5（本研究方案）**：清晰阐明目的、方法、核心贡献，**必须出现 `Here, we...` 或 `In this study, we...`**。
- **P6（意义预告，可选）**：简述更广泛的影响。

**五种"缺口建立"句法**（P3 选用）：
1. 知识缺口：`Despite [prior work], [aspect] remains poorly understood / unexplored.`
2. 方法缺口：`Current approaches cannot distinguish / fail to capture [critical aspect].`
3. 数据缺口：`[X] data are available for only ~[N] sites globally, insufficient for [assessment].`
4. 尺度缺口：`[X] has been studied at [local] scale; a [global/systematic] assessment is lacking.`
5. 悖论/争议缺口：`Whether [X] enhances or suppresses [Y] remains controversial.`

风格要求：每段首句是 topic sentence；段内走 CEI；缩写首次出现写全称(缩写)，后文统一用缩写；适当嵌入量化信息（含单位）。

---

## Methods / Materials and Methods（方法）

- 用**名词短语**而非 "Step 1/2/3" 命名小节。
- 优先**被动语态**：`Modeling was performed using...`，`Data were obtained from...`。
- 提供足以复现的细节：软件版本、参数、数据来源、分辨率。
- 引用已验证方法用 `following [ref]` / `as described in [ref]`。

硬性规则：
- 只介绍方法，**不展示结果、结论或对应图号**（Methods 出现 found/showed/significant 等结果性词是常见错误，参见 `style-rules.md` 的检查清单与 `lint.py`）。
- 重要参数与超参数必须完整：分辨率、时间窗、过滤阈值、交叉验证折数等。
- 明确运行环境（R/Python）、版本、关键依赖包及版本。
- 参数取值须有依据（文献、经验规则、预实验/敏感性分析）。
- 统计方法须明确：检验类型、效应量、置信区间计算、多重比较校正。
- 模型评估须说明指标（AUC、RMSE、r²、TSS 等）及阈值。
- 公式排版：变量/参数用斜体；上下标用 HTML 标签 `<sup></sup>`/`<sub></sub>`，而非 Unicode 特殊字符。
- 专有名称（方法名、模型名、数据集名）首字母大写。

填空模板见 `templates.md` 的 Methods 小节模板。

---

## Results（结果）

- **纯陈述**，不解释机制（机制留给 Discussion）。
- 每段以主题句开头，直接给核心发现，段内走 CEI（此处 Interpretation 限于结果内部）。
- 图表引用：`(Fig. X)`、`as shown in Extended Data Fig. X`，图号放句末括号内。

数据呈现原则：不逐条罗列原始数据，精选趋势、对比与异常值；正文呈现模式（趋势方向、差异幅度、变化范围、组间对比），不重复图表里已有的全部数值。

常用句型：
- `We found that [X] was [Y] ([value, unit, CI]).`
- `[Variable A] showed the greatest [trend].`
- `Our results indicate that [X] accounts for [X%] of [total Y].`
- `[X] varied substantially across [regions/scenarios], ranging from [A] to [B].`

---

## Discussion（讨论）

段落逻辑：
1. **核心发现重申**：不重复结果数字，用更高层次语言提炼科学意义。
2. **与前人对比**：`Our findings are consistent with / in contrast to [ref].` 可支持某"预期"并挑战另一"预期"。差异恰是创新性的体现，从数据来源、方法、尺度、时段解释不一致，并引文献佐证。
3. **机制解释**：解释"为什么"而非重复"是什么"，对每个核心结果追问机制，需文献支撑。
4. **局限性**：必须有，且具体。这是顶刊 Discussion 的标志（结构见下）。
5. **更广泛意义**：对领域、政策、管理的影响。
6. **未来方向**：`Future studies should consider...`

进阶原则：引用高质量近期文献；综合各 Results 模块提炼更高层次指示意义；善用交叉验证/敏感性分析/第三方数据增强说服力；坦诚不足的同时强调创新与价值。

**局限性段落标准结构**：
```
Despite [advantages], [our approach] has several limitations.
First, [限制1 — 方法/数据层面].
Second, [限制2 — 模型假设简化层面].
Third, [限制3 — 推广性/时空尺度层面].
We acknowledge that [additional constraint].
Nevertheless, our [study] provides [key contribution].
Future improvements will require [next steps].
```

局限性表达类型库：
- 方法局限：`We did not explicitly account for...`、`We could not conduct [analysis] because of...`
- 数据局限：`Our analysis is limited by the availability of...`
- 模型简化：`Our model has simplifying assumptions concerning...`、`This means we are likely underestimating...`
- 推广性：`The generalizability of our findings to other [systems] remains to be tested.`
