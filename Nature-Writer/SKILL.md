---
name: Nature-Writer
description: >
  专业顶刊学术论文写作助手，专注于 Nature 正刊及其子刊（Nature Climate Change、Nature Communications、Nature Sustainability、Nature Ecology & Evolution、Nature Geoscience 等）风格的论文辅助、修改、生成与润色。当用户需要：撰写/润色论文任意章节（Abstract、Introduction、Methods、Results、Discussion、Conclusion）、修改学术语言表达、改进段落逻辑、规范论文叙事框架、将中文草稿翻译/改写为顶刊英文风格、检查语法与用词是否符合 Nature 发表标准，请立即调用此 skill。即使用户只说"帮我润色一下这段话"或"这个 Introduction 写得怎么样"，只要涉及学术论文写作，也应调用本 skill。
---

# Nature-Writer

基于对大量 Nature 系列期刊全文论文（生态学、环境科学、海洋科学、地球科学方向）的深度分析，提炼出其核心叙事框架、语言逻辑与写作规范，用于辅助研究者产出顶刊水准的英文学术论文。

---

## 零、Nature 正刊 vs 子刊结构总览

在开始写作前，必须明确目标期刊的格式要求，不同 Nature 期刊的结构差异显著。

### Nature 正刊（Article）结构
- **无独立 Introduction 标题** —— 正文以 "Main" 为整体标题，引言自然嵌入正文开头
- **无 "Results" 和 "Discussion" 分开** —— 结果与讨论通常融合在 "Main" 的连续叙事中
- **极简方法在文末** —— Methods 在正文末尾，以 "Methods" 为标题，详细方法放入 Extended Data / Supplementary Information
- **Abstract 极短（约 150 词）**，强调"一个核心发现"的叙事弧线
- **正文字数 3000–4000 词**，高度精炼

### Nature 子刊（NC、NCC、NS、NEE、NG）结构
- **有明确 Introduction 标题**（部分子刊如 NC 无 "Introduction" 标题，正文首段直接充当引言）
- **Results 和 Discussion 可分开可合并** —— NC 尤其灵活，"Results and Discussion" 合并形式常见
- **有独立 Methods 节**，可详细描述
- **Abstract 略长（150–250 词）**，包含具体数字和指标
- **正文字数 5000–8000 词**，允许更多技术细节

| 特征 | Nature 正刊 | Nature Communications | NCC/NS/NEE/NG |
|------|------------|---------------------|---------------|
| Introduction 标题 | 无（"Main"替代） | 无或"Introduction" | 通常有"Introduction" |
| Results/Discussion | 合并于"Main" | 灵活（可分可合） | 通常分开 |
| Abstract 长度 | ~150词，叙事性强 | ~200词，指标密集 | ~180词，情景导向 |
| Methods | 精简置于文末 | 独立、可详实 | 独立、中等长度 |
| 参考文献数量 | ~30-50 | ~50-80 | ~40-70 |

---

## 一、论文宏观结构框架（IMRaD / Main）

### Abstract（摘要）
按以下"四句式"结构压缩为 150–250 词（正刊 120–180 词，子刊 180–250 词）：

1. **研究背景/领域重要性**：1 句建立研究问题在学科或社会中的意义。避免泛泛的"The world is facing..."；用具体事实锚定。正刊用更宏大的叙事语言，子刊用更技术性的陈述。
2. **核心研究缺口**：1–2 句指出现有不足（"remains unclear / poorly understood / has not been established"）。这是 Abstract 的"张力点"——张力越强，读者越想往下读。
3. **本方法与核心发现**：2–3 句给出方法概述和最重要的量化发现。子刊须包含具体数字（百分比、范围、置信区间），正刊可不包含过多数字但必须有 1–2 个核心定量结果。
4. **研究意义与影响**：1 句收尾，说明结果对管理、政策、科学认知的指导价值。

**关键句法模式（基于真实顶刊分析）：**

> **类型 A — Nature 正刊风格（叙事优先）**
> "[Topic X] poses a [critical/significant] challenge to [ecosystem/society]. Despite [existing knowledge], [key gap] remains largely unknown. Here we [develop/present] [method] to [objective]. We estimate/find that [quantitative finding]. Our results [suggest/demonstrate] that [broader implication], highlighting [significance]."

> **类型 B — Nature Communications 风格（指标密集）**
> "[Topic X] plays a fundamental role in [ecosystem/process]. Yet, current tools/approaches remain inadequate for [specific goal], limited by [specific challenge]. Here we [develop/propose] [method], achieving [key metric: e.g., MAE reduction X%]. We find that [quantitative result 1] and [quantitative result 2]. Our results enable [application], providing [insight] for [field]."

> **类型 C — Nature Sustainability 风格（政策导向）**
> "[Topic X] is of growing concern due to [specific impact]. However, the [magnitude/extent] of [X] remains unclear, hindering [management/policy]. Here we [quantify/assess] [X] using [method]. We find that [quantitative finding with policy relevance]. These results underscore the need for [action/policy], with implications for [sustainability goals]."

**示例（Nature 正刊实际模式）：**
> *"Plastics in the marine environment have become a major concern because of their persistence at sea, and adverse consequences to marine life and potentially human health. Implementing mitigation strategies requires an understanding and quantification of marine plastic sources, taking spatial and temporal variability into account. Here we present a global model of plastic inputs from rivers into oceans based on waste management, population density and hydrological information. We estimate that between 1.15 and 2.41 million tonnes of plastic waste currently enters the ocean every year from rivers, with over 74% of emissions occurring between May and October."*

### Introduction（引言）
遵循"漏斗式"结构：宏观→领域→具体问题→本研究。通常 4–6 段：

**段落逻辑推进序列（必须严格按序，不可跳跃）：**
- **P1（全球/学科背景）**：用 1–2 个具体事实锚定研究领域的重要性。避免空洞的"The world is facing..."。**句末应出现一个量化数据**（如全球产量、受影响面积等）。
- **P2（领域已知知识）**：综述已有研究框架，引用经典文献。建立读者对领域当前认知水平的共识。
- **P3（研究缺口 — 语言张力核心）**：以 "However / Nevertheless / Yet / Despite..." 明确转折，指出具体知识缺口。**这一段是引言中最重要的一段**——张力越具体，研究的必要性越强。
- **P4（聚焦具体对象）**：深入介绍研究物种/区域/系统/方法的特殊性与重要性（可选，适用于研究高度聚焦的论文）
- **P5（本研究的方案与贡献 — "Here, we..."）**：清晰阐明研究目的、方法和核心贡献。**必须出现 "Here, we..." 或 "In this study, we..." 句式**。
- **P6（意义预告，可选）**：briefly preview the broader implications of the findings

**Introduction 的五种"缺口建立"句法：**
1. `Despite [prior work], [key aspect] remains [poorly understood / unexplored].`
2. `However, [a systematic/global/comprehensive] assessment of [X] does not yet exist.`
3. `[X] has been well studied in [context A], but [context B] has received much less attention.`
4. `A key uncertainty is that [specific knowledge gap], making it difficult to [predict/manage/understand].`
5. `To date, the [mechanism/extent/drivers] of [X] remain elusive / have not been established.`

**风格要求：**
- 每段第一句必须是 **topic sentence** —— 概括该段核心论点
- 段落内部遵循 "Claim → Evidence → Interpretation" 的三步推进（见下方"段落黄金模型"）
- 首次出现缩写时，写 **全称（缩写）**；后文统一仅用缩写
- Introduction 中适当嵌入**量化信息**（关键规模/趋势/范围/比例，含单位）
- 从 P3 开始，每段至少需要 2–3 个参考文献支撑

### Methods / Materials and Methods（方法）
- 用 **名词短语** 而非 "Step 1/2/3" 命名小节
- 优先 **被动语态**：`Modeling was performed using...`, `Data were obtained from...`
- 必须提供足以复现的细节（软件版本、参数设置、数据来源、分辨率等）
- 引用已验证的方法时使用 `following [ref]` 或 `as described in [ref]`

**方法写作硬性规则：**
- 只介绍 **方法**，不在 Methods 中展示结果、结论或对应图号
- 重要参数与超参数必须完整（分辨率、时间窗、过滤阈值、交叉验证折数等）
- 明确模型运行的语言环境（R/Python）、版本、关键依赖包及版本
- 参数取值必须有依据与来源（文献、经验规则、预实验/敏感性分析）
- 统计方法需明确：检验类型、效应量、置信区间计算方法、多重比较校正方法
- 模型评估部分需说明评价指标（AUC、RMSE、r²、TSS 等）及其阈值
- 公式排版：变量/参数用**斜体**，函数名/运算符/缩写通常不用
- 公式中的上下标使用 HTML 标签（<sup></sup>、<sub></sub>），而非 Unicode 特殊字符（如 ⁰¹²³⁴⁵⁶⁷⁸⁹）
- 专有名称（方法名、模型名、数据集名称等 Proper nouns）首字母大写
- 涉及定量关系或计算过程处，尽量配以公式表达

### Results（结果）
- **纯陈述**，不解释机制（机制留给 Discussion）
- 每段以 **主题句** 开头，直接给出核心发现
- 图表引用：`(Fig. X)`, `as shown in Extended Data Fig. X`

**结果三段论的"Claim-Evidence-Interpretation"模型（适用于每个子节）：**
1. **Claim（主张）**：本段核心发现，主题句中直接给出。*"Global zooplankton biomass declined by 7–16% from 1980 to 2100."*
2. **Evidence（证据）**：提供支撑数据。*"The decline in omnivorous zooplankton biomass was 8–18%, while filter feeders experienced a more modest decline of up to 6%."*
3. **Interpretation（解释 — 限于结果内的解释）**：用一两句话说明这个发现意味着什么、符合或不符合什么预期。*"These declines in zooplankton biomass are primarily caused by projected declines in phytoplankton biomass."*

注意：这里的 Interpretation 限于"结果内部的解释"（如数据模式的成因），**不是机制层面的深入讨论**（那是 Discussion 的工作）。

**数据呈现原则：**
- Results 中不逐条罗列原始数据，而是精选趋势、对比与异常值，突出核心发现
- 正文侧重呈现模式（趋势方向、差异幅度、变化范围、组间对比），避免罗列图表中的所有数值
- 图表已包含完整的数据细节信息，正文仅需引导读者聚焦最关键的发现，而非重复数据

**常用结果表达句型：**
- `We find/found that [X] was/is [Y] ([specific value, unit, CI]).`
- `[Variable A] showed/exhibited the greatest/highest/most significant [trend].`
- `Our results indicate that [X] accounts for [X%] of [total Y].`
- `[X] varied substantially across [regions/species/scenarios], ranging from [A] to [B].`

### Discussion（讨论）
遵循以下段落逻辑：

1. **核心发现重申**（不重复结果数字，而是用更高层次的语言提炼科学意义）
2. **与前人研究对比**：`Our findings are consistent with / in contrast to / support the conclusion of [ref].` 也可以支持某种"预期"（expectation）并挑战另一种"预期"
3. **机制解释**：`This may be because...` / `This is likely driven by...`
4. **局限性承认**：必须有，且要具体。Nature 系列期刊的 Discussion 必须有 Limitations 段落
5. **更广泛意义**：对领域、政策、管理的影响
6. **未来研究方向**：`Future studies should consider...`

**Discussion 的深入写作原则：**
- **引用高质量近期文献**支撑分析论证，增加讨论的学术深度与说服力
- **解释"为什么"而非重复"是什么"**：对每个核心结果追问其背后的机制原因，避免仅复述结果中的数字，需有文献支撑
- **文献对比不求完全一致**：与已有研究的差异恰恰是论文创新性的体现，重点从数据来源、方法差异、空间尺度、时间范围等角度解释为何存在不一致，并引用文献佐证
- **综合各结果模块**：将 Results 各部分发现的关联进行整合，提炼出更高层次的生态或环境指示意义，而非逐条孤立讨论
- **适度揭示局限并强调贡献**：在坦诚方法或数据不足的同时，突出本研究的创新性、独特性和学术价值
- **善用验证证据**：引用交叉验证结果、敏感性分析或第三方独立数据，增强读者对研究结论的认可

**局限性段落的标准结构（基于实际顶刊分析）：**
```
Despite [advantages], [our approach/model] has several limitations.
First, [specific limitation 1 — 方法/数据层面].
Second, [specific limitation 2 — 模型假设简化层面].
Third, [specific limitation 3 — 推广性/时空尺度层面].
We acknowledge that [additional constraint].
Nevertheless / Despite these limitations, our [study/model/method] provides [key contribution].
Future improvements will require [specific next steps].
```

**局限性表达的类型库：**
- **方法局限**：`We could not conduct a stochastic uncertainty analysis at full scale because of...`、`We did not explicitly account for...`
- **数据局限**：`Our analysis is limited by the availability of...`、`We acknowledge that...may suffer from uncertainty...`
- **模型简化**：`Our model has many simplifying assumptions concerning...`、`This means that we are likely to be underestimating...`
- **推广性**：`The generalizability of our findings to other [regions/systems] remains to be tested.`

**Nature 正刊 Discussion 的特色句法（从实际论文中提取）：**
- `Our results support the first part of this expectation ([A]) while challenging the expectation that [B].`
- `There is a need for more extensive monitoring of [X] with [specific recommendation].`
- `Nevertheless, we believe our [model/study] is an important step towards [broader goal].`

---

## 二、Nature 子刊专用写作指南

### Nature Climate Change (NCC) 特点
- **"因果链"叙事模式**：气候变化 → 气候变量变化 → 生态响应 → 生态系统服务影响
- **情景对比驱动**：必须使用多种 SSP/RCP 情景对比，贯穿全文
- **缩放的逻辑**：全球平均 → 按生物群系（biome）分区 → 按纬度/区域分解
- **关键术语**：projected shifts, ensemble mean, trophic amplification, under climate change, SSP scenarios

### Nature Sustainability (NS) 特点
- **"科学发现→管理建议"桥梁**：Results 后必须有专门的 policy/management implications 部分
- **政策导向句式**：`We advocate / We suggest / We urge / Our results can provide guidance for...`
- **不确定性处理的透明化**：坦诚局限后再给出政策建议
- **关键术语**：sustainability perspective, mitigation measures, actionable insights, long-term resilience, biodiversity targets

### Nature Ecology & Evolution (NEE) 特点
- **Research article**：强调进化/生态机制，与 NCC 的"环境驱动"叙事不同
- **Perspective/Commentary 特殊结构**：
  - 以让步开头：`[Established method] is a powerful tool for [purpose]`
  - 转折：`However, [misapplication] will lead to [problem]`
  - 分层论证：层层递进，每个论点都有引用支撑
  - 结语：强有力的总结句，带有警示或建议
- **高密度引用**：观点文章中几乎每句都有引用支撑

### Nature Geoscience (NG) 特点
- **"突破性发现"驱动**：Abstract 开篇即点出颠覆性结果
- **量化对比强化**：`threefold greater than`, `only 0.2% of X but receive 27% of Y`
- **多数据源交叉验证**：强调方法的严谨性
- **关键术语**：observation-constrained, mechanistic model, uncertainty bracketing

### 特例：Nature Communications 的灵活性
- Abstract 可以更技术化，接受更多的公式和指标引用
- "Results and Discussion" 合并形式可接受
- 允许正文中包含伪代码/算法概述
- 图表标题可更详细，包含方法关键参数

---

## 三、段落黄金模型："Claim-Evidence-Interpretation"

每一段（无论 Introduction、Results 还是 Discussion）都应尽可能遵循此模型：

**第一句 — Claim（主张）**：本段核心论点，一句话概括
**中间句 — Evidence（证据）**：支撑论点的数据、引用、逻辑推理
**最后句 — Interpretation/Significance（解释/意义）**：说明这个发现/证据意味着什么

**Results 中的 CEI 示例：**
> **Claim:** Global zooplankton biomass declined by 7–16% from 1980 to 2100.
> **Evidence:** Omnivorous zooplankton biomass exhibited the greatest decline of 8–18%, whereas filter feeders experienced a more modest decline of up to 6%.
> **Interpretation:** These declines are primarily caused by projected declines in phytoplankton biomass, with warming acting as a secondary driver.

**Introduction 中的 CEI 示例：**
> **Claim:** Zooplankton community structure determines energy transfer efficiency.
> **Evidence:** Communities dominated by carnivorous copepods (PPMR < 100) are expected to transfer less energy than those dominated by filter feeders (PPMR > 6 million).
> **Interpretation:** Better accounting for the diversity of zooplankton functional traits will therefore improve understanding of energy flow.

---

## 四、句法与语法规范

### 指代与引用表达
- 避免 `see below`；改为 `as described in Methods`, `(Fig. X)`, `in Extended Data Fig. X`
- 图表引用嵌入叙述：`Our model showed a peak in August (Fig. 2b)` — 图号放在句末括号内

### 时态使用
| 位置 | 时态 | 示例 |
|------|------|------|
| 引言中的背景知识 | 一般现在时 | `Rivers transport sediment to oceans.` |
| 已发表研究的引用 | 现在完成时/过去时 | `Previous studies have shown / X et al. reported that...` |
| 本研究方法描述 | 一般过去时 | `We used the MaxEnt model...` |
| 本研究结果 | 一般过去时（首选） | `We found that...` |
| 图表所显示 | 一般现在时 | `Fig. X shows / As shown in Fig. X` |
| 广义结论/意义 | 一般现在时 | `These findings suggest that...` |

**关键规则**：结果描述用过去时（`We found that`），但图表引导和结论意义用现在时（`Fig. X shows / These findings suggest`）。

### 标点使用
- **禁止使用破折号**：全文不得出现任何形式的破折号（em dash, —），包括插入语、解释说明或强调用途。替代方案：使用逗号、冒号、分号或括号。例如，将 "X — a key driver — contributes to Y" 改写为 "X, a key driver, contributes to Y" 或 "X (a key driver) contributes to Y"。
- 连接数值范围使用 en dash（–），如 "10–20 km"

### 语态使用
- **被动语态**（方法、数据处理）：`Data were collected`
- **主动语态**（发现、强调贡献）：`We find / We estimate / Our results reveal`
- 方法部分用被动、结果讨论部分用主动，形成自然的语态切换

### 数字与单位规范
- 单位紧跟数字：`0.94 Tg yr⁻¹`, `1,000 Mg`, `AUC > 0.8`
- 不确定度表达：`1,000 (893–1,224) Mg`, `95% CI: 0.13–3.8`
- 百分比结合背景：`82% ± 15% was biodegraded`

---

## 五、词汇与用语指南

### 高频强力动词（替换"show/prove/confirm"）
| 弱词 | 推荐替换 |
|------|----------|
| show | demonstrate, reveal, indicate, suggest, highlight, document |
| find | identify, observe, detect, quantify, estimate |
| use | employ, utilize, apply, adopt, implement |
| study (v.) | investigate, assess, evaluate, examine, characterize |
| important | critical, crucial, fundamental, pivotal, essential |
| change (n.) | shift, transformation, alteration, modification |
| increase | enhance, amplify, elevate, exacerbate |

### 研究缺口表达（Introduction 核心句）
- `...remains largely unknown / poorly understood / unexplored.`
- `No [global/systematic/comprehensive] assessment of [X] exists to date.`
- `Previous studies have focused on [X], while [Y] has received less attention.`
- `Despite [known fact], the [mechanism/extent/drivers] of [X] remain unclear.`
- `This gap in knowledge hinders our ability to [manage/predict/understand] [X].`
- `A key uncertainty is that [specific gap], making it difficult to...`

### "Here, we..."的创新声明句法
- `Here, we present/develop/use [method] to [objective].`
- `In this study, we extend/challenge/synthesize [existing framework] by...`
- `Here, we challenge this tenet by experimentally evaluating...`
- `To address this gap, we...`（比 "Here we" 更柔和，适合子刊）

### 科学不确定性表达
- **可能性高**：likely, probably, suggest, indicate, is consistent with
- **可能性中**：may, could, might, potentially, possibly
- **推测/谨慎**：does not rule out, raises the possibility, lends support to
- **避免过度确定**：不写 "proves that", "conclusively shows that", "confirms that"
- **子刊中的不确定性语气可略强于正刊** —— 特别是 NCC 和 NG

### 段落连接词
| 功能 | 用语 |
|------|------|
| 转折/对比 | However, Nevertheless, By contrast, Conversely, Yet, In contrast |
| 递进/强调 | Furthermore, Moreover, In addition, Importantly, Notably |
| 因果 | Therefore, Thus, Hence, As a result, Consequently |
| 举例 | For example, For instance, Specifically |
| 总结 | Together, Overall, Taken together, Collectively |
| 引出意义 | These findings suggest / indicate / demonstrate / highlight |

### 优秀表达摘录库（来自真实 Nature 子刊论文）

**表达 1: Nature 正刊风格的对比叙事**：
> *"A general expectation of climate change is that future marine ecosystems will support less fish biomass where primary production decreases, while the number of trophic steps between primary producers and fish is expected to substantially increase as mean phytoplankton size declines. Our results support the first part of this expectation (less phytoplankton means lower fish biomass) while challenging the expectation that future food webs will be much longer."*

**表达 2 — 模型定位的谦逊但自信**：
> *"It is more appropriate to think that AI-based GOFSs stand on the shoulders of numerical GOFSs."*

**表达 3 — 政策建议的"soft"表达**：
> *"We advocate incorporating habitat hotspot regions into a multifaceted conservation strategy that integrates ecological and socio-economic factors to improve conservation effectiveness."*

**表达 4 — "缺口声明"的精准定位**：
> *"Despite the importance of membrane and PFAS properties in governing PFAS transport, a fundamental property-structure-performance relationship has not been established for PFAS removal by polyamide NF and RO membranes."*

**表达 5 — 坦诚权衡（trade-off）句式**：
> *"The results indicate that the choice of an uncertainty-aware approach led to a minor decrease in prediction accuracy while enabling us to generate predictions with quantified uncertainty for a larger proportion of chemicals."*

---

## 六、Nature 写作的十条核心原则

1. **量化一切**：每个关键结论都需要数字支撑，避免定性描述代替定量结论
2. **开门见山**：每段的第一句即是中心句，不铺垫、不绕弯
3. **逻辑链完整**：问题→方法→结果→机制→意义，每步都需衔接，不可跳跃
4. **证据-主张匹配**：每个主张必须紧跟着支撑证据（数据或引用），不能"有主张无证据"
5. **承认局限**：Discussion 必须有诚实的 limitations 小节，这是顶刊的标志
6. **精准用词**：一词不多、一词不少，避免模糊表达；名词短语代替从句可压缩篇幅
7. **全球/大尺度视角**：即使是区域研究，也要建立与全球趋势的联系
8. **图表自说话**：正文引用图表时不重复描述图注，而是解释图表的科学含义
9. **不确定性敏感性**：模型结果必须报告不确定性和/或敏感性分析结果；若缺失应提示补充
10. **短句为主**：避免过长复合句堆叠（必要时拆句）；全文禁止使用任何形式的破折号

---

## 七、各章节写作检查清单

### Abstract 检查项
- [ ] 是否按照"四句式"结构压缩？（背景 → 缺口 → 方法+发现 → 意义）
- [ ] 是否包含至少1个具体定量发现（数字+单位）？
- [ ] 正刊是否控制在180词以内，子刊是否在250词以内？
- [ ] 是否避免了参考文献引用？

### Introduction 检查项
- [ ] 是否从宏观意义切入（P1）？
- [ ] 是否有明确的"Houever/Despite..."研究缺口句（P3）？
- [ ] 是否有清晰的"Here, we..."或类似目标句（P5）？
- [ ] 引用是否覆盖了最新文献（近5年）？
- [ ] 是否避免了方法和结果的过早出现？
- [ ] 是否包含适当的量化信息？
- [ ] 每段第一句是否为 topic sentence？

### Methods 检查项
- [ ] 是否使用了名词短语命名小节？
- [ ] 数据来源、软件版本、参数是否完整？
- [ ] 模型评估指标是否明确？
- [ ] 是否可以被独立复现？
- [ ] 是否仅介绍方法、不展示结果/结论？
- [ ] 统计检验是否有对应参考文献？

### Discussion 检查项
- [ ] 是否将结果与前人对比（而不只是重复结果）？
- [ ] 是否有 limitations 段落且内容具体？
- [ ] 是否解释了机制（"This is because / This may be due to"）？
- [ ] 是否以更宏观的意义收尾？
- [ ] 局限性是否按 First/Second/Third 结构组织？

---

## 八、常见问题修正指南

### 中式英文表达 → 顶刊表达

| 中式/弱表达 | Nature风格替换 |
|-------------|----------------|
| This paper studies X | Here, we investigate X |
| The result shows | Our results demonstrate / indicate |
| The method is good/effective | The method performed well, with [AUC = X] |
| We think/believe that | We suggest / propose / hypothesize that |
| Many previous studies have said | Previous work has shown / demonstrated / reported |
| In conclusion, this study | Taken together, our findings |
| Very important | Critical / pivotal / fundamental |
| A lot of / lots of | Substantial / considerable / abundant |
| Get bigger/larger | Increase / expand / grow |
| Make worse | Exacerbate / intensify / aggravate |
| More and more | Increasingly / growing |
| For a long time | Historically / Over the past decades |

---

## 九、与 Science 系列的写作差异

如果用户目标期刊是 **Science** 或 **Science Advances**，注意以下差异：

### Science（与 Nature 正刊的差异）
- **新闻价值优先**：Abstract 的第一句话必须抓住非专业读者的注意力
- **更短的正文**：仅 8–12 个自然段，约 2000–3000 词
- **Methods 在补充材料**：正文不设 Methods 部分
- **无独立 Introduction 标题**：正文首段直接作为引言
- **更强的故事性**：善用引文、隐喻和文化参照（如 Silent Spring 引文）
- **使用 "Here we show/report/document"** 而非 Nature 的 "Here we present/use"

### Science Advances（与 Nature Communications 的差异）
- 有明确 Introduction 标题（不同于 Science）
- 有独立 Methods 节在正文（不同于 Science，类似于 NC）
- Abstract 略长（150–200 词）
- 在 Science 的"新闻价值"和 NC 的"技术完整性"之间取平衡

---

## 十、参考文献与资源

如需查看更多写作范例或特定期刊子刊的风格差异，参阅：
- [references/phrase-bank.md](references/phrase-bank.md) — 常用学术短语库（按功能分类）
- [references/section-templates.md](references/section-templates.md) — 各章节段落模板
- [Nature-essays.md](Nature-essays.md) — 原始论文语料（可作为参照范本）

---

## 使用说明

当用户提供文本需要润色或生成时，请：
1. **判断目标期刊**（Nature 正刊/NC/NCC/NS/NEE/NG/Science 等）
2. **判断章节类型**（Abstract/Introduction/Methods/Results/Discussion）
3. **对照本 skill 中对应期刊类型的结构和语言规范进行检查与改写**
4. **优先修正**：缺口句缺失、CEI 段落模型不完整、时态错误、定性描述替代定量、中式表达、段落逻辑不连贯
5. **保留原意**：在改善语言的同时忠实于作者原始科学表述
6. **提供修改说明**：简要指出修改了哪些方面（可选，根据用户需求）

如用户需要从零生成某章节，依据本 skill 的模板结构，结合用户提供的研究背景和数据，生成符合 Nature 投稿标准的段落。
