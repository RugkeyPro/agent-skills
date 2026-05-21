---
name: rk_plotter
description: 通用科研绘图 skill。用于根据真实数据结构和科学问题，从高保真 Markdown 模板库中选择、复用、改写并生成 publication-quality matplotlib 绘图脚本和 png/pdf/svg 图像；适用于散点/模型诊断、时间序列、地图、组成图、分布图、多面板综合图和科研流程框图。也用于把用户上传到 new_templates 的同风格 Markdown 绘图模板同步接入正式 templates 模板库。
---

# rk_plotter

## 绘图流程

1. 先识别用户真实数据结构：字段、单位、分组、时间轴、空间坐标、是否成对观测、是否组成矩阵。
2. 读取 `references/template-index.md`，只根据触发词、标签、数据结构和适用场景选择候选模板。
3. 命中后再读取对应 `templates/*.md` 全文；不要从零重画，不要读取 `new_templates/` 作为绘图入口。
4. 保留模板的构图、配色、比例、面板结构、图例和特殊 artist 逻辑；把模板中的虚拟数据段替换为用户真实数据读取和整理代码。
5. 生成独立 Python 绘图脚本，脚本开头必须先设置 `matplotlib.use("Agg")`，再导入 `matplotlib.pyplot`。
6. 使用 `scripts/rk_plotter_core.py` 的 `apply_style()` 和 `save_figure()` 导出图像。
7. 按 `references/quality-checklist.md` 检查；不合格就修改脚本并重新出图，直到通过。

## 生成脚本硬性规范

```python
import matplotlib
matplotlib.use("Agg")

from scripts.rk_plotter_core import apply_style, save_figure
import matplotlib.pyplot as plt
```

- 保持 `matplotlib.rcParams["svg.fonttype"] = "none"`，确保 SVG 文本可编辑。
- 默认导出 `png`, `pdf`, `svg`；PNG 600 dpi；透明背景；`bbox_inches="tight"`。
- 保存后必须关闭 figure：优先使用 `save_figure()`，或显式 `plt.close(fig)`。
- 禁止 `plt.show()`。

## 模板接入流程

当用户说“同步 `new_templates`”“接入新模板”“把新模板加入 `rk_plotter`”时：

1. 扫描 `new_templates/*.md`，不要把它们直接用于绘图。
2. 运行 dry run：
   ```bash
   python scripts/sync_new_templates.py --source new_templates --target templates --index references/template-index.md --dry-run
   ```
3. 若缺少接入卡片，读取新模板全文，从图像类型、适用场景、代码、配色、比例和依赖中补齐元数据。
4. 处理重复或相似模板：只接入更完整的版本，或在模板卡片中记录 `related_templates`。
5. 同步到正式库：
   ```bash
   python scripts/sync_new_templates.py --source new_templates --target templates --index references/template-index.md
   ```
6. 默认复制，保留 `new_templates/` 原始上传文件；只有用户明确要求时才加 `--move`。

## 模板接入卡片

正式模板 Markdown 顶部必须包含 YAML 接入卡片，字段包括 `id`、`title`、`category`、`trigger_phrases`、`tags`、`data_profile`、`style_profile`、`dependencies`、`best_for`、`avoid_when`。

## 参考文件

- `references/template-index.md`：正式模板路由表，绘图前先读。
- `references/template-tags.md`：数据结构、科学问题与标签映射。
- `references/quality-checklist.md`：出图后的规范检查。
- `templates/`：正式高保真 Markdown 模板库。
- `new_templates/`：用户上传模板暂存区，只有同步流程会读取。
