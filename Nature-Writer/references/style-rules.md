# 句子层规则参考：时态 / 标点 / 语态 / 用词 / 检查清单

> 这是"句子与用词层面"规则的唯一权威来源。润色（模式 B）和批评诊断（模式 C）主要对照本文件。功能句库见 `phrase-bank.md`。其中的硬规则（破折号、缩写首用、Methods 不含结果、单位格式、词数）可用 `scripts/lint.py` 机械校验。

---

## 时态

| 位置 | 时态 | 示例 |
|------|------|------|
| 引言中的背景知识 | 一般现在时 | `Rivers transport sediment to oceans.` |
| 已发表研究的引用 | 现在完成时/过去时 | `Previous studies have shown / X et al. reported that...` |
| 本研究方法描述 | 一般过去时 | `We used the MaxEnt model...` |
| 本研究结果 | 一般过去时（首选） | `We found that...` |
| 图表所显示 | 一般现在时 | `Fig. X shows / As shown in Fig. X` |
| 广义结论/意义 | 一般现在时 | `These findings suggest that...` |

关键规则：结果描述用过去时（We found that），但图表引导和结论意义用现在时（Fig. X shows / These findings suggest）。

---

## 标点

- **全文禁止任何形式的破折号（em dash —）**，包括插入语、解释、强调用途。替代：逗号、冒号、分号或括号。
  - `X — a key driver — contributes to Y` → `X, a key driver, contributes to Y` 或 `X (a key driver) contributes to Y`。
- 数值范围用 en dash（–）：`10–20 km`、`7–16%`。

（这是 0/1 可机械判定的硬规则，`lint.py` 会扫描破折号。）

---

## 语态

- **被动**（方法、数据处理）：`Data were collected`。
- **主动**（发现、强调贡献）：`We find / We estimate / Our results reveal`。
- 方法部分被动、结果讨论部分主动，形成自然切换。

---

## 数字与单位

- 单位紧跟数字：`0.94 Tg yr⁻¹`、`1,000 Mg`、`AUC > 0.8`。
- 不确定度：`1,000 (893–1,224) Mg`、`95% CI: 0.13–3.8`。
- 百分比结合背景：`82% ± 15% was biodegraded`。

---

## 指代与图表引用

- 避免 `see below`；改为 `as described in Methods`、`(Fig. X)`、`in Extended Data Fig. X`。
- 图表引用嵌入叙述，图号放句末括号：`Our model showed a peak in August (Fig. 2b)`。

---

## 强力动词替换（替换弱词 show/prove/confirm 等）

| 弱词 | 推荐替换 |
|------|----------|
| show | demonstrate, reveal, indicate, suggest, highlight, document |
| find | identify, observe, detect, quantify, estimate |
| use | employ, utilize, apply, adopt, implement |
| study (v.) | investigate, assess, evaluate, examine, characterize |
| important | critical, crucial, fundamental, pivotal, essential |
| change (n.) | shift, transformation, alteration, modification |
| increase | enhance, amplify, elevate, exacerbate |

---

## 科学不确定性表达

- 可能性高：likely, probably, suggest, indicate, is consistent with
- 可能性中：may, could, might, potentially, possibly
- 推测/谨慎：does not rule out, raises the possibility, lends support to
- **避免过度确定**：不写 proves that / conclusively shows that / confirms that
- 子刊不确定性语气可略强于正刊（尤其 NCC、NG）

---

## 段落连接词

| 功能 | 用语 |
|------|------|
| 转折/对比 | However, Nevertheless, By contrast, Conversely, Yet, In contrast |
| 递进/强调 | Furthermore, Moreover, In addition, Importantly, Notably |
| 因果 | Therefore, Thus, Hence, As a result, Consequently |
| 举例 | For example, For instance, Specifically |
| 总结 | Together, Overall, Taken together, Collectively |
| 引出意义 | These findings suggest / indicate / demonstrate / highlight |

---

## 中式英文 → 顶刊表达（润色与翻译时优先修正）

| 中式/弱表达 | Nature 风格替换 |
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

## 各章节检查清单（批评诊断模式 C 逐条对照）

### Abstract
- [ ] 是否按四句式结构（背景 → 缺口 → 方法+发现 → 意义）？
- [ ] 是否含至少 1 个具体定量发现（数字+单位）？
- [ ] 正刊 ≤150 词 / NC ≤250 词 / 其他子刊 ~180 词？
- [ ] 是否避免了参考文献引用？

### Introduction
- [ ] 是否从宏观意义切入（P1）且句末有量化数据？
- [ ] 是否有明确的 However/Despite 研究缺口句（P3）？
- [ ] 是否有清晰的 `Here, we...` 目标句（P5）？
- [ ] 引用是否覆盖近 5 年文献？
- [ ] 是否避免方法和结果过早出现？
- [ ] 每段首句是否为 topic sentence？

### Methods
- [ ] 是否用名词短语命名小节？
- [ ] 数据来源、软件版本、参数是否完整？
- [ ] 模型评估指标是否明确？
- [ ] 是否可独立复现？
- [ ] 是否仅介绍方法、不混入结果/结论？
- [ ] 统计检验是否有对应参考文献？

### Discussion
- [ ] 是否将结果与前人对比（而非重复结果）？
- [ ] 是否有 limitations 段落且内容具体（First/Second/Third）？
- [ ] 是否解释了机制（This is because / This may be due to）？
- [ ] 是否以更宏观的意义收尾？

---

## 十条核心原则（全 skill 纲领，亦在 SKILL.md 中）

1. **量化一切**：每个关键结论都需数字支撑。
2. **开门见山**：每段首句即中心句。
3. **逻辑链完整**：问题→方法→结果→机制→意义，不跳跃。
4. **证据-主张匹配**：每个主张紧跟支撑证据。
5. **承认局限**：Discussion 必须有诚实具体的 limitations。
6. **精准用词**：一词不多不少，名词短语压缩篇幅。
7. **全球/大尺度视角**：区域研究也要联系全球趋势。
8. **图表自说话**：引用图表时解释科学含义，不重复图注。
9. **不确定性敏感**：报告不确定性和/或敏感性分析。
10. **短句为主**：拆分过长复合句；全文禁破折号。
