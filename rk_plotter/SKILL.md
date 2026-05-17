---
name: rk_plotter
description: "通用科研绘图 skill。用于创建、重构、复用和渲染 publication-quality matplotlib 科学图，包括地图、时间序列、组间分布、散点/模型诊断、柱状/组成图、SHAP/机器学习解释图、雷达图、概念框架图和多面板科研图。触发场景：需要选择绘图模板、把随机示例数据替换为真实数据、统一字体/配色/导出格式、生成 PNG/PDF/SVG 图件、或检查科研图可读性与统计表达。"
---

# rk_plotter 通用科研绘图

## 工作流

1. 先判断用户想表达的问题类型：空间分布、时间变化、组间差异、组成比例、模型诊断、机器学习解释、概念框架或多指标比较。
2. 打开 `references/template-catalog.md`，选择最接近的 template id；不要从零重写已有图形结构。
3. 用 `scripts/templates/<template_id>.py` 作为起点，把 `make_sample_data()` 的随机示例数据替换为用户数据，保留 `plot()` 和 `render()` 接口。
4. 复用 `scripts/rk_plotter_core.py` 的 `apply_style()`、`save_figure()`、配色和尺寸常量；只有在期刊或用户明确要求时才局部覆盖样式。
5. 生成图后按 `references/quality-checklist.md` 检查：图形是否回答问题、坐标轴是否清楚、统计注释是否诚实、颜色是否可区分、导出是否完整。

## 统一配置要求

- 在任何独立绘图脚本中，先设置 `matplotlib.use("Agg")`，再导入 `matplotlib.pyplot`。
- 保持 `matplotlib.rcParams["svg.fonttype"] = "none"`，确保 SVG 中的文字可编辑。
- 默认输出 `png`, `pdf`, `svg`；PNG 用 600 dpi，所有格式使用 `bbox_inches="tight"` 和透明背景。
- 保存后必须关闭 figure：使用 `save_figure()` 或显式 `plt.close(fig)`。
- 禁用 `plt.show()`、`jet`、`rainbow` 和红绿对立作为主要编码。
- 图中随机数据只能用于模板演示；交付用户图件前必须替换为真实数据或明确标注为模拟示例。

## 模板调用

列出模板：

```bash
python scripts/render_template.py --template hotspot_map --output-dir outputs --list
```

渲染单个模板示例：

```bash
python scripts/render_template.py --template scenario_uncertainty_timeseries --output-dir outputs --formats png,pdf,svg
```

在新脚本中复用模板：

```python
from scripts.templates.scenario_uncertainty_timeseries import plot, render

fig, ax = plot(data=my_data)
render("outputs", basename="my_scenario_figure", data=my_data)
```

## 参考文件

- `references/template-catalog.md`：模板分类、适用数据、原始脚本来源和 preview 名称。
- `references/style-guide.md`：字体、尺寸、坐标轴、图例、colorbar 和导出规范。
- `references/color-palettes.md`：分类、连续、发散、log、地图、情景和模型比较配色。
- `references/plot-selection.md`：按科学问题选择图形。
- `references/statistical-boundaries.md` 与 `references/stat-annotations.md`：统计注释边界和常用标注写法。
- `references/quality-checklist.md`：交付前检查清单。

## 资产位置

- 标准模板：`scripts/templates/*.py`
- 核心绘图库：`scripts/rk_plotter_core.py`
- 渲染入口：`scripts/render_template.py`
- 原始随机数据脚本：`assets/original-scripts/`
- 历史 PNG/PDF 示例图：`assets/previews/`
