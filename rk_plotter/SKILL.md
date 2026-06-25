---
name: rk_plotter
description: 科研绘图模板母版 skill，用于生成、重构或美化期刊级 matplotlib 科研配图——散点诊断图(predicted vs observed / parity)、密度散点、箱线/小提琴/raincloud/boxen、堆叠条形、时间序列与不确定性带、地图(栅格/choropleth/proportional symbol/SST)、热图与相关矩阵、SHAP/PCA/排序降维、多面板组合图等。只要用户提到画图、绘图、重画这张图、把代码改成出版级/投稿级配图、配色、figure、plot、matplotlib、复现某张论文图，即使没点名模板，也应触发本 skill：先从 templates/manifest.json 选最接近的模板并复制其代码，再接入真实数据、保持视觉风格、做最小必要扩展。不处理纯数据分析、表格生成或与绘图无关的代码。
---

IMPORTANT: 模板事实源是 `templates/manifest.json`；选择前读它（或 `python scripts/list_options.py
--section templates`）。绘图前如需了解修改边界与选择交互规则，读 `references/template-guide.md`。

决策默认值（统一规则，取代旧的"出图前逐项征询"）：**默认根据数据与最近模板自动选定图型/
模式/配色/图例/尺寸/投影并直接出图，把关键决策写进脚本头注释**；仅当用户显式表达选择意图
（"我想选 / 对比 / 列出选项 / 换配色 / 用哪个模板"）时，才用
`python scripts/list_options.py --format markdown` 列出候选并等待选择。

CRITICAL TEMPLATE SOURCE RULE: 模板代码只能复制本 skill `templates/` 目录下的文件。绝不把用户当前
工作目录、项目、`outputs/`、notebook 或任意本地文件夹里的绘图脚本当作视觉母版。用户旧脚本只能用于
读取数据、分析逻辑、字段名与科学意图，其绘图块不得成为模板来源。

Templates are high-fidelity masters derived from `assets/original-scripts/` and
`assets/new-scripts/`, not generic recipes.
# rk_plotter: 科研绘图模板母版 Skill

本 Skill 通过**复制模板代码 + 接入真实数据 + 保持视觉风格 + 必要微调扩展**的方式，生成可读、可改、可交付的完整科研绘图脚本。

---

## 核心原则

### 1. 必须首先复制模板代码

任何绘图任务都必须先选择最接近的模板，并复制本 skill 根目录下 `templates/` 目录中对应 `.py` 文件的绘图代码作为母版。

如果当前工作目录或用户项目中存在其他绘图脚本，它们只能作为数据读取、统计流程或字段含义的参考，不能作为绘图母版，也不能替代本 skill 的 `templates/*.py`。

禁止直接从零自由重写一套新绘图代码，除非没有任何模板接近用户需求。

正确流程：

```text
读取本 skill 的模板索引 → 选择模板 → 复制本 skill 的模板代码 → 接入真实数据 → 微调字段/文字/尺寸/输出 → 必要时扩展元素
```

### 2. 尽可能保持模板视觉效果

改写时应尽量保留模板的：

* 图形基本类型；
* 主布局和子图结构；
* 字体、字号和字重；
* 颜色体系；
* 线宽、点大小、透明度；
* legend / colorbar 风格；
* 轴线、网格和边距；
* 图框大小；
* SVG/PDF/PNG 输出规范。

模板是视觉母版，不是仅供参考的代码片段。

### 3. 允许基于真实数据做必要扩展

不改变图形基本形式，不等于不能添加元素。若真实数据需要，允许在模板风格体系内增加：

* 同类型数据系列；
* 额外 y 轴或 x 轴；
* 误差线、误差带、置信区间；
* 参考线、阈值线、均值线；
* 局部 inset；
* 地图点层、边界层、区域框；
* 简短统计注释。

例如：模板是双轴柱状图，真实数据包含第三个指标族，agent 可以在模板基础上增加第三轴，但必须保持原模板的柱状图 + 轴线 + 配色 + 字体 + legend 风格。

### 4. 显式数据绑定

必须使用 `FIELD_MAP` 或等价的显式字段映射绑定真实列名。

禁止在有列名的数据中直接依赖：

```python
df.iloc[:, 0]
df.iloc[:, 1]
```

除非用户数据确实没有表头。

### 5. 交付完整脚本

最终输出必须是完整、独立运行的 Python 脚本，包含：

* `TEMPLATE_ID`
* `FIELD_MAP`
* `TEXT_CONFIG`
* `STYLE_CONFIG`
* `EXPORT_CONFIG`
* `load_data()`
* `prepare_data()`
* `plot()`
* `save_outputs()`
* `main()`

不要只输出 diff，也不要只输出黑盒函数调用。

---

## 三类工作流

### 工作流 A：从 0 绘图

适用于用户提供数据、字段或绘图需求，但没有旧绘图代码。

步骤：

1. 检查数据字段和科学问题。
2. 从本 skill 的 `references/template-index.md` 选择最接近模板。
3. 复制本 skill 的 `templates/TEMPLATE_ID.py`。
4. 修改 `FIELD_MAP`、`TEXT_CONFIG`、`STYLE_CONFIG`、`EXPORT_CONFIG`。
5. 替换模板中的 demo 数据读取逻辑，接入用户真实数据。
6. 如数据复杂度超过模板默认结构，在同视觉语法下做必要扩展。
7. 输出完整脚本。

### 工作流 B：重构旧绘图代码

适用于用户提供已有绘图脚本。

步骤：

1. 分离旧代码中的数据逻辑和绘图逻辑。
2. 保留数据读取、清洗、统计、模型预测、指标计算部分。
3. 删除旧绘图主体。
4. 从本 skill 的 `references/template-index.md` 选择最接近模板。
5. 复制本 skill 的模板绘图代码作为新绘图主体。
6. 将旧代码最终产生的数据变量接入模板。
7. 在模板风格下做必要微调和扩展。
8. 输出完整新脚本。

不得只在旧绘图代码上局部修改颜色、字体或 `savefig`。

### 工作流 C：优化已有图

适用于用户已有图形结构较合理，只需要美化、规范或导出。

步骤：

1. 判断原图对应的模板类型。
2. 复制本 skill 中最接近模板的样式层、导出层和布局约束。
3. 尽量保留原图科学含义和主要结构。
4. 替换或规范：rcParams、字体、字号、颜色、线宽、图例、输出格式。
5. 如果原图结构过乱，应转入工作流 B，用模板绘图主体重构。

---

## 数据与依赖处理原则

模板中的 demo 数据仅用于模板预览。若用户提供真实数据、旧代码或明确字段，必须替换模板中的 demo 数据逻辑，不得在正式输出中误用示例数据。

当模板依赖缺失时，agent 应判断 fallback 是否会改变模板核心视觉语法：

* 快速预览可以 fallback，但需标注为 preview；
* 正式科研输出、论文图、答辩图或用户要求模板一致时，不得静默降级；
* 如果 fallback 会改变核心视觉效果，应说明依赖缺失，并给出安装建议或替代方案。

---

## 禁止事项

除非用户明确要求，否则禁止：

* 不复制模板代码，直接自由发挥绘图；
* 改变图形基本类型；
* 改变变量科学含义；
* 改变统计方法；
* 删除模板中的 legend、colorbar、参考线、误差带、panel label 等核心元素；
* 添加大量文字注释破坏学术图面；
* 只输出 PNG，不输出 SVG/PDF；
* 遗留 `plt.show()`；
* 将模板 demo 数据伪装成用户真实数据；
* 将预览 fallback 伪装成正式 publication-quality 输出。

---

## 参考指南（已收敛为 3 份 + 1 个事实源）

* 模板事实源: `templates/manifest.json`（id / family / modes / required_fields / deps / preview）
* 工作流（A 从零 / B 重构旧代码 / C 优化）+ 统一决策规则: `references/workflow.md`
* 模板导览 + 修改边界 + 选择交互 + QA 清单: `references/template-guide.md`
* 样式与输出契约（字体/画布/配色/三格式/dpi）: `references/style-contract.md`

辅助脚本: `scripts/list_options.py`（列选项，读 manifest）、`scripts/inspect_data.py`（看数据 schema）、
`scripts/check_plot.py`（结构化自检，支持 `--all`）、`scripts/render_template_preview.py`（批量渲染预览，读 manifest）。

> 原 high-fidelity-policy / selection-interface / edit-boundary / refactor-code / qa-checklist / template-index
> 已合并进上述文件，留有重定向 stub，可安全删除。
