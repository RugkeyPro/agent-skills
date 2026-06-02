---
name: rk_plotter
description: "通用科研绘图 skill。用于根据数据特征和科学问题选择、复用、改写和渲染 publication-quality matplotlib 图形；内置 45 个带标签的科研绘图模板，提供强大的包级程序化调用 API，支持模板自动路由、智能字段映射、高像素导出和 Trace 质量一致性审计。"
---

# rk_plotter 通用科研绘图 (程序化 API 包版本)

`rk_plotter` 已经重构为结构化的 Python 包，为大语言模型 (LLMs) 提供了一套极度稳定、参数化和防局部乱改的程序化科学可视化流水线。

---

## 核心程序化流水线 (Programmatic API Workflow)

在处理用户的绘图请求时，**强烈推荐** 采用以下程序化逻辑来构建最终的 Python 绘图脚本。这种模式能够极大程度降低模型临场判断的不稳定性，并防止局部乱改导致的渲染崩溃：

```python
import sys
from pathlib import Path
import pandas as pd

# 1. 确保 rk_plotter 可被正常导入（若作为包本地安装，可以直接 import rk_plotter；
#    或者在脚本头部动态添加 rk_plotter 的父级目录到 sys.path 中）：
skill_root = str(Path(__file__).resolve().parent)  # 假设 rk_plotter 包文件夹与脚本在同一目录下
if skill_root not in sys.path:
    sys.path.insert(0, skill_root)

from rk_plotter import select_template, load_template, save_figure, write_trace
from rk_plotter.quality import verify_consistency

# 2. 读取/加载用户的真实 DataFrame 数据
df = pd.read_csv("user_dataset.csv")  # 或者是用户提供的其他数据加载逻辑

# 3. 程序化路由选择模板 (输入请求文本、列名与数据形态)
match = select_template(
    user_request="我想要一张模型预测值和实测值对比的散点图，带1比1线",
    columns=list(df.columns),
    data_shape=df.shape
)
print(f"自动路由选择的最佳模板为: {match.template_id} (匹配分: {match.score})")

# 4. 加载特定模板实例
template = load_template(match.template_id)

# 5. 自动推断并匹配 DataFrame 中的字段映射关系 (如 real->'Observed', predicted->'Predicted')
field_mapping = template.infer_fields(df)
print(f"智能匹配的字段关系为: {field_mapping}")

# 6. 调用模板执行绘图 (传入 DataFrame、字段绑定字典以及自定义期刊配置)
fig = template.plot(
    df=df,
    field_mapping=field_mapping,
    config={
        "x_label": "Observed COD Removal (%)",  # 覆盖坐标轴标签
        "y_label": "Predicted COD Removal (%)",
        "title": "COD Removal Validation Model (R2/RMSE/MAE)"  # 覆盖标题
    }
)

# 7. 保存高分辨率矢量和栅格图片 (PNG 600 DPI, PDF, SVG 文本可编辑)
paths = save_figure(fig, output_dir="outputs", basename="model_validation_plot")

# 8. 写入执行 Trace 审计日志
trace_path = write_trace(
    output_dir="outputs",
    template_id=match.template_id,
    field_mapping=field_mapping,
    paths=paths
)

# 9. 执行 Trace 一致性自检 (检查文件尺寸与生成状态)
audit = verify_consistency(trace_path)
print(f"质量一致性检查通过: {audit['all_passed']}")
```

---

## 核心 API 说明

### 1. `select_template(user_request, columns, data_shape)`
- **功能**：根据用户自然语言或 tags 描述，结合输入数据的列名和形态，计算最相似的模板并返回。
- **返回**：`TemplateMatch` 对象（包含 `template_id`，`score`，`matched_tags` 属性）。

### 2. `load_template(template_id)`
- **功能**：从模板库中加载模板实例。
- **返回**：`Template` 类实例。

### 3. `template.infer_fields(df)`
- **功能**：采用内置的**语义匹配规则**，自动识别 DataFrame 的列名（支持多国语言及常用简称，例如 `obs`/`real` 对应 `observed`，`pred`/`sim` 对应 `predicted`）。若语义匹配失败则降级为位置匹配。
- **返回**：`dict[str, str]` 字段映射字典。

### 4. `template.plot(df, field_mapping, config)`
- **功能**：动态载入对应的制图模板，自动将 DataFrame 列绑定到 Matplotlib / Seaborn 对应参数中，并覆盖自定义 config 属性，输出期刊级图表。
- **返回**：`matplotlib.figure.Figure` 对象。

### 5. `save_figure(fig, output_dir, basename, formats=("png", "pdf", "svg"), dpi=600)`
- **功能**：统一的科学制图高分辨率保存。自动开启透明背景，去除多余白边（`bbox_inches="tight"`），确保 SVG 字体保持矢量可编辑性，自动在保存后关闭 figure 释放内存。

### 6. `write_trace(output_dir, template_id, field_mapping, paths)` 和 `verify_consistency(trace_path)`
- **功能**：审计图表输出品质。检查生成的文件大小是否为零，保障质量稳定性。

---

## 图类型快速检索 (Visual Tags Catalog)

若需要使用终端 CLI 或特定 tags，可以参考下表：

| 用户需求场景 | 匹配标签 | 推荐模板 ID |
|---|---|---|
| 经纬度网格、热点、空间暴露 | `spatial,lon_lat_grid,continuous_field` | `hotspot_map`, `log_scale_raster_map`, `raster_contour_map` |
| 国家/行政区指标分布 | `spatial,choropleth,country` | `country_choropleth_map` |
| 多组数值分布 (letter-value) | `distribution,grouped_samples,category_comparison` | `boxen_plot` |
| 预测值与实测值诊断 (回归/ML) | `prediction,observed,predicted,one_to_one` | `predicted_vs_real_scatter` |
| 观测点密度散点 (scipy-KDE) | `scatter,dense_points,density` | `density_colored_scatter` |
| 未来情景多曲线时间序列 | `scenario,time_series,multi_line` | `multi_scenario_timeseries` |
| 组成比例、百分比堆叠柱状图 | `composition,percent,groups` | `stacked_percentage_bar`, `horizontal_stacked_bar` |
| 特征重要性及 SHAP 分析 | `shap,features,effects` / `shap,features,importance` | `shap_summary_beeswarm`, `shap_importance_bar` |

---

## 向后兼容性说明 (Backward Compatibility)
本 Skill 仍完整保留了旧版命令行和 shims 接口。任何现有的调用 `python scripts/select_template.py` 或从 `scripts.templates.<template_id>` 导入的老代码均能在零修改的情况下继续流畅运行，因为它们已在底层重定向并共享了全新的 `rk_plotter` 顶级程序包服务。
