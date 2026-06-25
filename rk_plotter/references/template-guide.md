# Template Guide：选择 · 模式 · 修改边界 · 选择交互 · QA

本文件合并了原 template-index / edit-boundary / selection-interface / qa-checklist 与高保真选择规则。
模板元信息的**唯一事实源是 `templates/manifest.json`**；本文件是人读导览与规则说明。

---

## 1. 高保真母版定位

`templates/` 是从 `assets/original-scripts/` 与 `assets/new-scripts/` 提炼的高保真视觉母版，不是通用配方。
两个 asset 目录优先级相同；模板与源 asset 冲突时，除非用户另选，保留源 asset 的视觉语法。

模板只能来自本 skill 包：先读 manifest / `templates/TEMPLATE_ID.py`。用户目录、项目、notebook、输出目录里的脚本一律不作模板，只能用于恢复数据处理与科学意图。

---

## 2. 模板族与模式（导览）

完整列表与字段以 manifest 为准。运行 `python scripts/list_options.py --section templates` 可按 family 输出。

| Family | 模板 | 典型 modes |
|---|---|---|
| scatter_diagnostic | predicted_vs_real_scatter, density_scatter, dual_panel_scatter_fit, enriched_scatter | enrichment_bubble / marginal_true_pred / joint_kde_hist / grouped_regression / residual_diagnostic / shap_dependence |
| distribution | violin_boxplot（含 boxen_letter_value / violin_box / raincloud / faceted_boxplot）, boxen_plot（别名→ violin_boxplot:boxen_letter_value） | — |
| composition | stacked_percent_bar（vertical_percent / horizontal_percent / diverging_total / stacked_line）, horizontal_stacked_bar | — |
| timeseries | multi_scenario_timeseries, scenario_uncertainty_timeseries, event_period_timeseries, time_event_flow | ensemble_timeseries / event_timeline / paired_slope / sankey_multistage / alluvial_survival / ternary_bubble |
| map | raster_map（log_raster / contour_robinson / quiver_log / hotspot）, choropleth_map（country_choropleth / choropleth_symbols / proportional_continuous / proportional_categorical）, global_regional_sst_map | — |
| matrix | heatmap_2d, matrix_heatmap（triangular_corr / pair_corr_density / clustered_heatmap / expression_significance） | — |
| ordination | ordination_embedding（pca_biplot_marginal / pcoa_ellipse / rda_biplot / embedding_colorbar） | — |
| inference | inference_distribution（significance_box / taxonomic_stacked_bar / ridgeline_density / forest_ridgeline / posterior_distribution / dumbbell_caterpillar / roc_curve） | — |
| importance | shap_importance_bar | — |
| layout | multipanel_layout | — |

模式由各模板 `STYLE_CONFIG` 的 mode 键切换（如 `map_mode` / `scatter_mode` / `distribution_mode` / `bar_mode` / `heatmap_mode` / `ordination_mode` / `mode`，见 manifest 的 `mode_style_key`）。

---

## 3. 选择交互（仅在用户显式要选时触发）

触发词：用户说想选 / 挑 / 对比 / 决定 / 列出 / 浏览图型、模板、模式、配色、图例/colorbar、尺寸/期刊栏宽、地图投影/范围/inset、统计展示（CI、误差棒、拟合线、显著性、参考线、panel label、数值标注）等。

触发时：停在写绘图代码之前，列出完整候选再请用户选择，不要静默替用户决定。

```bash
python scripts/list_options.py --format markdown          # 全部
python scripts/list_options.py --section templates --section palettes --format markdown   # 子集
```

候选来源全部在本包内：模板/模式来自 manifest；配色与展示方案来自 `list_options.py` 内置目录；样式与输出规则见 `style-contract.md`。用户可组合兼容选项（如 log-raster 投影 + hotspot 配色 + 横向 colorbar）；只有会破坏源模板科学含义或视觉语法的组合才拒绝。

未触发时按 `workflow.md` 的默认规则自动决策并把选择写进脚本头注释。

---

## 4. 修改与扩展边界

### 4.1 总是允许
数据路径、读取逻辑、`FIELD_MAP`、标题、轴标签、单位、legend/colorbar 文本、字体族/字号、`figsize`、输出文件名/格式、PNG dpi、颜色 hex、线宽、点大小、透明度、tick 间距、图例列数与位置微调。

### 4.2 数据需要时允许（须继承模板风格）
- **同类数据系列**：多几条情景线 / 柱分组 / 散点组 / 堆叠组分；用模板原配色逻辑扩展，图形基本类型不变。
- **额外坐标轴**：双轴→三轴；轴色与对应系列一致；不遮挡、不改主轴含义。
- **误差线/不确定性带**：`errorbar` / `fill_between` / bootstrap CI；透明度低（alpha 0.1–0.2），颜色继承主系列。
- **参考线/阈值线**：均值、基准、阈值、1:1 线、事件线；灰色虚线低线宽（`color="#888888", linestyle="--", linewidth=0.8`），注释简短。
- **inset 局部放大**：不破坏主布局，字体/线宽 ≤ 主图，边框一致。
- **地图附加图层**：点位、边界、样区框、样线、inset；不改投影与主 colorbar 风格；正式输出不静默 fallback 成普通坐标图。

### 4.3 仅用户明确要求时
改图形基本类型、柱↔线、散点↔箱线、改统计方法、改轴变量含义、删模板核心元素、改多面板总布局、放弃 SVG/PDF、用高饱和非学术配色、图内加长段文字。

### 4.4 视觉相似度判据
改写后应：一眼仍像原模板；主图形类型不变；字体字号层级不变；配色一致；轴线/网格风格一致；legend/colorbar 仍属原风格；输出尺寸与格式合规。

---

## 5. 依赖缺失处理

模板 demo 数据仅用于预览。用户给真实数据/旧代码/明确字段时，必须替换 demo 数据逻辑，不得在正式输出误用示例数据，也不得把合成回退伪装成 publication-quality 输出（模板在回退时会向 stderr 打 `WARNING`）。

依赖（cartopy / seaborn / scipy，见 manifest `deps`）缺失时判断 fallback 是否改变核心视觉语法：快速预览可 fallback 但须标注 preview；正式科研图不得静默降级，应说明缺失并给安装建议或替代方案。

---

## 6. QA 清单（交付前逐项确认）

**模板母版**：基于某个 `templates/*.py` 复制改写？声明 `TEMPLATE_ID`？保留核心绘图函数结构？未黑盒 `import rk_plotter` 绘图？

**视觉相似**：一眼仍像原模板？图形基本类型不变？主布局/legend/colorbar/轴线一致？字体字号颜色线宽继承？新增元素未破坏平衡？

**数据绑定**：用 `FIELD_MAP` 显式绑定列？正式任务已替换 demo 数据？保留旧代码科学计算结果？处理 NaN/排序/单位？未出现 `Path("data.csv").exists()` 这类硬编码探测导致真实数据被静默替换？

**受控扩展**：新元素是同语法扩展？新轴与系列同色？误差线/带不遮挡主数据？参考线克制？inset 不破坏布局？无长段文字注释？

**输出**：输出 SVG + PDF + PNG？PNG 正式图 600 dpi？`plt.close(fig)`？无 `plt.show()`？

**自检**：`python scripts/check_plot.py 脚本.py` 通过（结构化校验，不只是语法）。
