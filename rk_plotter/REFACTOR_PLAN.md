# rk_plotter 重构方案

> 评估范围：`SKILL.md` + 8 个 `references/*.md` + 4 个 `scripts/*.py` + 21 个 `templates/*.py` + `assets/`（original-scripts / new-scripts / previews）。

---

## 1. 现状评估

这是一个已经相当成熟的"科研绘图模板母版"skill，核心理念清晰：**复制模板 → 绑定真实数据 → 保持视觉风格 → 最小必要扩展**。三层渐进式加载（SKILL.md / references / templates+scripts）符合 skill 设计规范，模板大多带有 `TEMPLATE_ID / FIELD_MAP / TEXT_CONFIG / STYLE_CONFIG / EXPORT_CONFIG` + `load_data / prepare_data / plot / save_outputs / main` 的统一外壳，并配有 `list_options / check_plot / inspect_data / render_template_preview` 四个辅助脚本。

**结论：不需要推倒重来，而是做"收敛 + 去重 + 补齐自动化"的结构性重构。** 当前最大的代价不在绘图能力，而在 (a) 文档冗余导致的上下文膨胀与自相矛盾，(b) 模板/索引/脚本三者之间的"事实源"不一致，(c) 缺少机器可读的清单与预览映射，使选择和校验都依赖模型现场解析 markdown。

---

## 2. 核心问题（按影响排序）

### P0-1 文档严重重复、且存在自相矛盾
"必须先复制模板、不得自由发挥、保持视觉语法、正式图不得静默 fallback"这套话，在 `SKILL.md`、`high-fidelity-policy.md`、`workflow.md`、`edit-boundary.md`、`refactor-code.md`、`qa-checklist.md` 里各讲了一遍。代价是每次触发都要吞下大量重复文本。

更关键的是**矛盾**：`selection-interface.md` 说"**当用户要求选择时**才停下来列选项"，而 `high-fidelity-policy.md` 的"Required pre-plot questions"写成"**生成任何图之前**都要让用户从候选里选"。这两条对"是否每次都必须打断用户"给出了相反指令，模型只能二选一，行为不稳定。

### P0-2 模板契约已经"漂移"，SKILL.md 承诺的统一接口名存实亡
- `predicted_vs_real_scatter.py`：`prepare_data(df, field_map)`，正确按 `field_map` 绑定列。
- `raster_map.py`：`prepare_data(df, field_map, style)`，且**硬编码 `Path("data.csv").exists()`** 判断——`load_data` 接收的真实路径被忽略，用户传入任何非 `data.csv` 文件名都会**静默回退到合成数据**。这正是文档反复强调"禁止把 demo 数据伪装成真实数据"的那种 bug，却被模板自身触发。
- `STYLE_CONFIG` 字段在不同模板间不统一（如 `font_sans` vs `font_family`、有的有 `dpi/projection`、有的没有），`prepare_data` 签名也不统一（2 参 vs 3 参）。

`check_plot.py` 只做 token 子串检查（甚至 `"plot"` 这种过松的匹配），无法发现上述语义漂移。

### P1-1 "事实源"分散在三处且互相不同步
模板的元信息同时存在于：① `references/template-index.md` 的两套不同表头（上半部 mode 制、下半部 "Required Fields/Core Visual Grammar" 制）；② 每个模板文件头部注释；③ `list_options.py` 现场用正则解析 markdown 表格。三者没有单一可信源，已经出现不同步。

### P1-2 索引与模板的覆盖不一致、概念重叠
- `boxen_plot` 既是独立模板文件，又是 `violin_boxplot` 的 `boxen_letter_value` 模式——同一图型两个入口，选择时容易混乱。
- 索引里 `enriched_scatter / matrix_heatmap / time_event_flow / ordination_embedding / inference_distribution` 这些"image-derived"族声明了大量 mode，但与下半部 legacy 表（`predicted_vs_real_scatter / density_scatter / ...`）风格割裂，新人很难看出 21 个文件到底怎么映射。

### P1-3 预览渲染脚本的模板清单已过期
`render_template_preview.py` 的 `TEMPLATES_LIST` 硬编码了 16 个模板，缺少 5 个新族（`enriched_scatter / matrix_heatmap / time_event_flow / ordination_embedding / inference_distribution`）。硬编码清单必然随模板增长而失效，应改为扫描目录。

### P1-4 已有预览图未与模板建立映射，选择体验缺图
`assets/previews/` 下有 ~45 张语义化命名的 PNG（如 `shap_importance_barplot.png`），但文件名不对应 `TEMPLATE_ID`。结果是：一个绘图 skill 在让用户"选图型"时**给不出可视预览**，只能给文字描述。这是体验上最可惜的缺口。

### P2-1 仓库卫生
`.vscode/settings.json` 入库；skill 根目录残留产物 `china_lake_efficiency_bubble_map.pdf/png`。这些不该出现在交付包里，应清理并 `.gitignore`。

### P2-2 描述（description）触发面偏窄
当前 `description` 仅中文、且未覆盖常见触发语（"画图 / matplotlib / 期刊投稿配图 / 重画这张图 / 散点图箱线图地图"等）。skill 的 description 是触发主开关，建议按 skill-creator 规范写得更"主动"、含正反例语境。

### P2-3 输出规格的小不一致
`style-contract.md` 写 PNG 600 dpi 必须；`qa-checklist.md` 写"≥300，推荐 600"；模板里 `STYLE_CONFIG.dpi=300` 而 `EXPORT_CONFIG.dpi=600`。应统一口径，避免歧义。

---

## 3. 重构方案

### 3.1 建立单一可信源：`templates/manifest.json`（解决 P1-1 / P1-2 / P1-3 / P1-4）
新增一个机器可读清单，作为模板元信息的**唯一事实源**：

```json
{
  "templates": [
    {
      "id": "raster_map",
      "family": "map",
      "modes": ["log_raster", "contour_robinson", "quiver_log", "hotspot"],
      "required_fields": ["lon", "lat", "value"],
      "optional_fields": ["u", "v"],
      "tags": ["栅格", "环境场", "风险载荷", "经纬度"],
      "source_assets": ["figure-log-scale raster map.py", "..."],
      "preview": "assets/previews/global_plastic_ingestion_risk_map.png",
      "deps": ["cartopy"]
    }
  ]
}
```

随后：
- `list_options.py` 改为读 manifest（不再正则解析 markdown），并能直接给出每个模板的**预览路径**。
- `template-index.md` 降级为"人读导览"，由脚本从 manifest 自动生成，杜绝双表头与不同步。
- `render_template_preview.py` 改为遍历 manifest（或 `templates/*.py`），删除硬编码 `TEMPLATES_LIST`，并把产物写回 manifest 指定的 preview 路径，使预览与模板永久对齐。
- 顺手为 `assets/previews/*.png` 建立 → `TEMPLATE_ID(.mode)` 的映射，补齐"选图型时能看图"。

### 3.2 收敛文档：8 个 references → 3 个（解决 P0-1）
合并去重，并消除矛盾指令：

| 新文件 | 吸收原文件 | 职责 |
|---|---|---|
| `references/workflow.md` | workflow + refactor-code | A/B/C 三类工作流（从零 / 重构旧代码 / 优化已有图），合并重复段落 |
| `references/style-contract.md` | style-contract + high-fidelity-policy（输出契约部分） | 字体/画布/配色/输出/继承规则，单一来源 |
| `references/template-guide.md` | template-index + edit-boundary + selection-interface + qa-checklist | 模板选择 + 可改/可扩/禁改边界 + 选择交互 + QA 清单 |

SKILL.md 正文随之瘦身：保留"五条核心原则 + 三类工作流入口 + 指向三个 reference 的指针"，删掉与 reference 重复的长段。

**消除矛盾**：把"是否打断用户让其选择"统一为一条明确规则——
> 默认：依据数据与最近模板**自动决策并直接出图**，在脚本头注释里写明所选模板/模式/配色等关键决策。仅当用户出现"我想选/对比/列一下选项/换配色"等**显式选择意图**时，才调用 `list_options.py` 停下来征求选择。

这样既保留高保真母版理念，又不让每次绘图都被迫走问答，符合"能自动决策就别打断"的产品取向。

### 3.3 把模板契约写成"代码层强约束"（解决 P0-2）
- 抽出 `templates/_base.py`（或 `scripts/plot_base.py`），集中放 `apply_style / save_outputs / load_data` 的标准实现与统一的 `STYLE_CONFIG` 键集，模板 `import` 复用，消除各文件重复与漂移。
- 统一 `prepare_data` 签名与"真实数据优先"逻辑：**以 `load_data` 实际拿到的 DataFrame 为准**，删除所有 `Path("data.csv")` 硬编码回退；只有 DataFrame 为空才用合成数据，且在终端打印 `WARNING: using synthetic preview data`。先修 `raster_map.py`，再以它为范式扫一遍其余 20 个模板。
- 升级 `check_plot.py`：从"token 子串"升级为"**导入模板做结构化校验**"——确认存在 `FIELD_MAP/STYLE_CONFIG/EXPORT_CONFIG` 字典、`plot()` 返回 `Figure`、`EXPORT_CONFIG.formats` 含 svg/pdf/png、无 `plt.show()`、合成数据路径已打 WARNING。新增一条"对每个模板跑一次冒烟渲染"的 CI 式自检（依赖缺失如 cartopy 时跳过并标注）。

### 3.4 处理模板重叠（解决 P1-2）
二选一并在 manifest 标注：
- **推荐**：保留 `violin_boxplot` 的 `boxen_letter_value` 模式，将独立的 `boxen_plot.py` 标为 `alias → violin_boxplot:boxen_letter_value`（或直接合并删除），避免双入口。
- 在 manifest 用 `family` 字段（map / distribution / composition / scatter-diagnostic / timeseries / matrix / ordination / inference）给 21 个模板分组，索引按 family 呈现，替代现在割裂的"上下两张表"。

### 3.5 加一个"选型助手"脚本（提升每次调用质量，可选但高价值）
`scripts/suggest_template.py`：输入用户数据（复用 `inspect_data.py` 的 schema 输出），结合 manifest 的 `required_fields/tags`，输出 Top-3 候选模板 + 建议 `FIELD_MAP`（列名 → 模板键的初猜映射）。把"看列名→选模板→绑字段"这段每次都要现场推理的活儿固化成确定性脚本，降低 token 与出错率。

### 3.6 仓库卫生与规格统一（P2-1 / P2-3）
- 删除根目录残留产物，移除/忽略 `.vscode/`，补 `.gitignore`（`outputs/`、`*.pyc`、根目录 png/pdf）。
- 统一输出口径：正式图 PNG = 600 dpi 为准，`STYLE_CONFIG.dpi` 仅作交互预览（如 150/200），并在 style-contract 与 qa-checklist 用同一句话表述。

### 3.7 触发描述优化（P2-2）
改写 frontmatter `description`，更主动、覆盖更多语境与正反例，例如：
> 科研绘图模板母版 skill：用于生成 / 重构 / 美化期刊级 matplotlib 科研配图（散点诊断图、箱线/小提琴/raincloud、堆叠条形、时间序列、地图栅格/choropleth、SHAP/PCA、热图、多面板等）。**只要用户提到"画图 / 重画这张图 / 把代码改成出版级配图 / 配色 / 投稿图 / matplotlib 绘图 / 复现某张论文图"，即使没点名模板，也应触发本 skill**：先复制最接近的模板再接入真实数据。不处理纯数据分析、表格生成或非绘图代码。

可在收尾用 skill-creator 的 description 优化回路（`run_loop.py`）量化验证触发率。

---

## 4. 实施顺序（建议）

1. **第 1 步（地基）**：建 `templates/manifest.json` + 改造 `list_options.py` / `render_template_preview.py` 读 manifest；建立 previews 映射。→ 解锁 P1 全部。
2. **第 2 步（止血）**：修 `raster_map` 的 `data.csv` 静默回退 bug，抽 `_base.py` 统一契约，升级 `check_plot.py` 做结构化校验；用它扫全部 21 模板并修正漂移。→ 解决 P0-2。
3. **第 3 步（瘦身）**：8 references 合并为 3，统一"默认自动决策、显式才打断"的规则；SKILL.md 正文精简。→ 解决 P0-1。
4. **第 4 步（打磨）**：模板去重（boxen）、加 `suggest_template.py`、仓库卫生、dpi 口径统一、description 优化。→ 收尾 P1-2 与全部 P2。

每步都可独立交付、互不阻塞，建议每步后跑一次"全模板冒烟渲染 + check_plot"作为回归验证。

---

## 5. 验证方式

- **结构回归**：`check_plot.py`（升级版）对 21 个模板逐个跑结构化校验，全过。
- **渲染回归**：`render_template_preview.py` 全量渲染（缺依赖跳过并标注），人工抽看预览是否仍"像母版"。
- **真实数据回归**：构造 2–3 份带非 `data.csv` 文件名的真实数据，确认不再静默回退到合成数据。
- **触发回归**（可选）：用 skill-creator 的 description 优化回路，对 ~20 条正负触发样例测触发率。

---

## 6. 一句话总结

**保留绘图内核与高保真理念，重构的重点是"收敛"**：把分散在 markdown / 文件头 / 脚本里的模板事实统一到 `manifest.json`，把重复且互相矛盾的 8 份文档收敛成 3 份并定下"默认自动、显式才问"的清晰规则，再用 `_base.py` + 升级版 `check_plot.py` 把"统一模板契约"从口头承诺变成代码强约束，顺带修掉 `raster_map` 静默回退 demo 数据这个与 skill 初衷直接冲突的 bug。
