---
name: Nature-Writer
description: >
  专业顶刊学术论文写作助手，专注于 Nature 正刊及其子刊（Nature Climate Change、Nature Communications、Nature Ecology & Evolution 等）风格的论文辅助、修改、生成与润色。当用户需要：撰写/润色论文任意章节（Abstract、Introduction、Methods、Results、Discussion、Conclusion）、修改学术语言表达、改进段落逻辑、规范论文叙事框架、将中文草稿翻译/改写为顶刊英文风格、检查语法与用词是否符合 Nature 发表标准，请立即调用此 skill。即使用户只说"帮我润色一下这段话"或"这个 Introduction 写得怎么样"，只要涉及学术论文写作，也应调用本 skill。
---

# Nature-Writer

基于对大量 Nature 系列期刊全文论文（生态学、环境科学、海洋科学、地球科学方向）的深度分析，提炼出其核心叙事框架、语言逻辑与写作规范，用于辅助研究者产出顶刊水准的英文学术论文。

---

## 一、论文宏观结构框架（IMRaD）

Nature 系列论文普遍遵循以下叙事结构，每个部分有严格的信息密度与逻辑顺序：

### Abstract（摘要）
按以下顺序压缩为 150–250 词：
1. **全球/学科重要性**：用 1 句话建立研究问题的宏观意义
2. **核心研究缺口**：用 1–2 句话指出现有研究的不足（"remains unclear / largely unknown / no global assessment"）
3. **本研究方法**：简述使用的模型、数据集或技术路线
4. **关键定量发现**：给出具体数字、范围、百分比（必须量化）
5. **研究意义与影响**：以 1–2 句话收尾，说明结果对管理、政策或科学认知的指导价值

**模板示例：**
> [Topic X] poses a [critical/major/significant] challenge to [ecosystem/human health/policy]. Despite [existing knowledge], [key gap] remains poorly understood. Here, we [develop/present/use] [method] to [objective], based on [data/model]. We find/estimate that [quantitative finding with numbers and units]. Our results suggest that [broader implication], highlighting the need for [action/future research].

---

### Introduction（引言）
遵循"漏斗式"结构：宏观→领域→具体问题→本研究。通常 4–6 段：

**风格与信息要求：**
- 以**短句**为主，避免过长复合句堆叠（必要时拆句）
- 一般情况下避免使用破折号串联多个分句（如 `sentence1——sentence2——sentence3`）
- Introduction 部分建议适当出现**量化信息**（关键规模/趋势/范围/比例，含单位）
- Introduction 中需要注明**参考文献**（必须真实可查；若用户未提供或无法核验，用占位符如 `[REF]` 标记）
- 从前言开始第一次出现缩写时，先写**全称（缩写）**；后文统一仅用缩写

**段落结构模板：**
- **P1（全球重要性）**：用宏观视角吸引读者，建立研究的社会/生态意义
- **P2（背景与已知）**：综述领域已有研究，建立知识框架
- **P3（研究缺口）**：以"However / Nevertheless / Yet / Despite..."开头，明确指出不足之处
- **P4（研究对象细节）**：介绍研究物种/区域/系统的特殊性与重要性
- **P5（本研究目标）**：以 "Here, we..." 为核心句，清晰阐明研究目的与方法
- **P6（研究意义预告）**：简述结论对领域的贡献

**关键转折句型：**
- `However, [key gap] remains [unclear/unexplored/uncertain].`
- `Despite [prior work], [limitation].`
- `To address this gap, we...`
- `Here, we present/develop/use [X] to [Y].`
- `To our knowledge, this is the first [global/systematic/quantitative] assessment of...`

---

### Methods / Materials and Methods（方法）
- 用**名词短语**而非"Step 1/2/3"命名小节（如"Habitat suitability modeling"、"Pesticide selection"）
- 优先**被动语态**：`Modeling was performed using...`, `Data were obtained from...`, `Records were cleaned by...`
- 必须提供足以复现的细节（软件版本、参数设置、数据来源、分辨率等）
- 引用已验证的方法时使用"following [ref]"或"as described in [ref]"
- 模型评估部分需说明评价指标（AUC、RMSE、r²、TSS等）及其阈值

**方法写作硬性规则（复现性与合规性优先）：**
- Methods 中同样需要**参考文献**（算法/指标/阈值/检验方法/软件包的经典出处；不可核验则用 `[REF]` 占位）
- 只介绍**方法**，不在 Methods 中展示结果、结论或对应图号（结果与图号应出现在 Results/Extended Data）
- 重要参数与超参数必须完整（例如分辨率、时间窗、过滤阈值、交叉验证折数、先验分布、MCMC 步数等）；若正文过长可移入**附录/补充材料**
- 明确模型运行的语言环境（R/Python）、版本、关键依赖包及版本（含随机种子与硬件/并行设置如适用）
- 参数取值必须有依据与来源（文献、经验规则、标准指南或预实验/敏感性分析）；避免“随意选取”
- 若存在验证或稳健性分析，需明确统计方法（例如置换检验、bootstrap、DeLong 检验、后验预测检验等）及其实现细节
- 注意公式排版：变量/参数通常使用**斜体**，函数名/运算符/缩写通常不用（以期刊公式规范为准）

---

### Results（结果）
- **纯陈述**，不解释机制（机制留给 Discussion）
- 每段以**主题句**开头，直接给出核心发现
- 大量使用定量语言：百分比、倍数、绝对值、置信区间
- 图表引用：`(Fig. X)`, `(Table 1)`, `as shown in Extended Data Fig. X`
- 地理/空间结果描述要指明具体区域

**结果组织：**
- 结果罗列不要过多和琐碎；能用图表承载的数据尽量放图表，让读者“看图得数”，正文聚焦关键模式与关键数值
- 凡涉及坐标轴、图例的两端均给出数值范围，避免读者猜测

**常用结果表达句型：**
- `We find/found that [X] was/is [Y] ([specific value, unit, CI]).`
- `[Variable A] showed/exhibited the greatest/highest/most significant [trend].`
- `The [model/analysis] revealed that [finding].`
- `Our results indicate that [X] accounts for [X%] of [total Y].`
- `[X] varied substantially across [regions/species/scenarios], ranging from [A] to [B].`

---

### Discussion（讨论）
遵循以下段落逻辑：

1. **核心发现重申**（不重复结果，而是用更高层次语言提炼）
2. **与前人研究对比**：`Our findings are consistent with / in contrast to / support the conclusion of [ref].`
3. **机制解释**：`This may be because...` / `This is likely driven by...` / `This could be attributed to...`
4. **更广泛意义**：对领域、政策、管理的影响
5. **局限性承认**：`Several limitations apply to this study. First, ... Second, ... However, ...`（必须有，且要具体）
6. **未来研究方向**：`Future studies should consider / Future improvements will require...`

---

### Conclusions（结论）
- 通常 1–2 段，简洁有力
- 重申主要发现（定量），强调贡献的新颖性
- 以行动建议或政策影响收尾

---

## 二、句法与语法规范

### 指代与引用表达
- 避免使用 `see below` 这类指代性表述；改为明确引用：`as described in Methods`, `(Fig. X)`, `in Extended Data Fig. X`, `in Supplementary Methods` 等

### 时态使用
| 位置 | 时态 | 示例 |
|------|------|------|
| 引言中的背景知识 | 一般现在时 | `Rivers transport sediment to oceans.` |
| 已发表研究的引用 | 现在完成时 | `Previous studies have shown that...` |
| 本研究方法描述 | 一般过去时 | `We used the MaxEnt model...` |
| 本研究结果 | 一般过去时或现在时 | `We found that... / Our results show that...` |
| 广义结论/意义 | 一般现在时 | `These findings suggest that rivers play a critical role in...` |

### 语态使用
- **被动语态**（方法、数据处理）：`Data were collected / Analyses were performed / Samples were processed`
- **主动语态**（发现、强调贡献）：`We find / We estimate / We demonstrate / Our results reveal`
- 避免第一人称在方法中过度使用，但发现部分用"we"更有力

### 数字与单位规范
- 单位紧跟数字：`0.94 Tg yr⁻¹`，`1,000 Mg`，`AUC > 0.8`
- 不确定度表达：`1,000 (893–1,224) Mg`，`95% CI: 0.13–3.8`，`mean ± s.d.`
- 百分比结合背景：`82% ± 15% was biodegraded`
- 大数字用科学计数法或词缀：`3 Tg`，`0.71 Gg`

---

## 三、词汇与用语指南

### 高频强力动词（替换"show/prove/confirm"）
| 弱词 | 推荐替换 |
|------|----------|
| show | demonstrate, reveal, indicate, suggest, highlight |
| find | identify, observe, detect, quantify, estimate |
| use | employ, utilize, apply, adopt, implement |
| study | investigate, assess, evaluate, examine, characterize |
| important | critical, crucial, fundamental, pivotal, essential |

### 研究缺口表达（Introduction核心句）
- `...remains largely unknown / poorly understood / unexplored.`
- `No [global/systematic/comprehensive] assessment of [X] exists to date.`
- `Previous studies have focused on [X], while [Y] has received less attention.`
- `Despite [known fact], the [mechanism/extent/drivers] of [X] remain unclear.`
- `This gap in knowledge hinders our ability to [manage/predict/understand] [X].`

### 科学不确定性表达（必须使用恰当的语气修饰词）
- **可能性高**：`likely`, `probably`, `suggest`, `indicate`
- **可能性中**：`may`, `could`, `might`, `potentially`
- **推测**：`is consistent with`, `lends support to`, `does not rule out`
- **避免过度确定**：不写 "proves that", "conclusively shows that"

### 段落连接词
| 功能 | 用语 |
|------|------|
| 转折/对比 | However, Nevertheless, By contrast, In contrast, Conversely, Yet |
| 递进/强调 | Furthermore, Moreover, In addition, Importantly, Notably |
| 因果 | Therefore, Thus, Hence, As a result, Consequently |
| 举例 | For example, For instance, Specifically, In particular |
| 总结 | Together, Overall, Taken together, In summary, Collectively |
| 引出意义 | These findings suggest / indicate / demonstrate / highlight |

---

## 四、Nature 写作的核心原则

1. **量化一切**：每个关键结论都需要数字支撑，避免定性描述代替定量结论
2. **开门见山**：每段的第一句即是中心句，不铺垫、不绕弯
3. **逻辑链完整**：问题→方法→结果→机制→意义，每步都需衔接
4. **承认局限**：Discussion 必须有诚实的 limitations 小节，这是顶刊的标志
5. **精准用词**：一词不多、一词不少，避免模糊表达
6. **全球/大尺度视角**：即使是区域研究，也要建立与全球趋势的联系
7. **图表自说话**：正文引用图表时不重复描述图注，而是解释图表的科学含义
8. **陈述边界与敏感性**：只要是模型产生的结果，都存在不确定性与敏感性；若用户未报告（或未做）不确定性/敏感性分析，应提示补充并在表述中使用恰当的限定语（may/could/likely）

---

## 五、各章节写作检查清单

### Abstract 检查项
- [ ] 是否建立了全球/宏观重要性？
- [ ] 是否明确指出了研究缺口？
- [ ] 是否包含了具体的定量发现（数字+单位）？
- [ ] 是否说明了研究意义？
- [ ] 字数是否在 150–250 词之间？

### Introduction 检查项
- [ ] 是否从宏观意义切入？
- [ ] 是否有明确的"However/Despite..."研究缺口句？
- [ ] 是否有清晰的"Here, we..."目标句？
- [ ] 引用是否覆盖了最新文献（近5年）？
- [ ] 是否避免了方法和结果的过早出现？
- [ ] 是否包含了适当的量化信息（含单位/范围/比例）？
- [ ] 首次出现缩写是否注明全称（Full term, ABBR.）并保持后文一致？
- [ ] 引用是否为真实可查文献；若无法核验是否用 `[REF]` 占位而非编造？

### Methods 检查项
- [ ] 是否使用了名词短语命名小节？
- [ ] 数据来源、软件版本、参数是否完整？
- [ ] 模型评估指标是否明确？
- [ ] 是否可以被独立复现？
- [ ] 是否仅介绍方法、不在 Methods 中展示结果/结论及结果图号？
- [ ] 方法/指标/阈值/验证统计检验是否有对应参考文献（或 `[REF]` 占位）？
- [ ] 是否交代 R/Python 环境与关键依赖包版本（含随机种子/并行设置如适用）？

### Discussion 检查项
- [ ] 是否将结果与前人对比（而不只是重复结果）？
- [ ] 是否解释了机制（"This is because / This may be due to"）？
- [ ] 是否有 limitations 段落且内容具体？
- [ ] 是否以更宏观的意义收尾？

---

## 六、常见问题修正指南

### 中式英文表达 → 顶刊表达

| 中式/弱表达 | Nature风格替换 |
|-------------|----------------|
| This paper studies X | Here, we investigate X |
| The result shows | Our results demonstrate / indicate |
| It can be seen from Fig. X | Figure X shows / As shown in Fig. X |
| The method is good/effective | The method performed well, with [AUC = X] |
| We think/believe that | We suggest / propose / hypothesize that |
| Many previous studies have said | Previous work has shown / demonstrated / reported |
| In conclusion, this study | Taken together, our findings |
| Very important | Critical / pivotal / fundamental |
| A lot of / lots of | Substantial / considerable / abundant |
| Get bigger/larger | Increase / expand / grow |
| Make worse | Exacerbate / intensify / aggravate |
| More and more | Increasingly / growing |

---

## 七、参考文献与资源

如需查看更多写作范例或特定期刊子刊的风格差异，参阅：
- [references/phrase-bank.md](references/phrase-bank.md) — 常用学术短语库（按功能分类）
- [references/section-templates.md](references/section-templates.md) — 各章节段落模板
- [Nature-essays.md](Nature-essays.md) — 原始论文语料（可作为参照范本）

---

## 使用说明

当用户提供文本需要润色或生成时，请：
1. **判断章节类型**（Abstract/Introduction/Methods/Results/Discussion）
2. **对照本 skill 中对应章节的结构和语言规范进行检查与改写**
3. **优先修正**：缺口句缺失、时态错误、定性描述替代定量、中式表达、段落逻辑不连贯
4. **保留原意**：在改善语言的同时忠实于作者原始科学表述
5. **提供修改说明**：简要指出修改了哪些方面（可选，根据用户需求）

如用户需要从零生成某章节，依据本 skill 的模板结构，结合用户提供的研究背景和数据，生成符合 Nature 投稿标准的段落。
