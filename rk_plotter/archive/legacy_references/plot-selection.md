# Plot Selection

按科学问题选模板，不按图形外观硬套。优先使用 `scripts/select_template.py`，再核对 `template-catalog.md`。

| 科学问题 | 数据特征标签 | 首选模板 | 备选模板 |
|---|---|---|---|
| 空间连续强度、风险或暴露 | `spatial,lon_lat_grid,continuous_field` | `hotspot_map` | `log_scale_raster_map`, `global_raster_vessel_fraction` |
| 空间值跨数量级 | `spatial,lon_lat_grid,continuous_field,log_scale` | `log_scale_raster_map` | `raster_quiver_log_colorbar` |
| 栅格场叠加等值线 | `spatial,lon_lat_grid,continuous_field,contour` | `raster_contour_map` | `hotspot_map` |
| 国家或行政区比较 | `spatial,choropleth,country,regional` | `country_choropleth_map` | `choropleth_proportional_symbol_map` |
| 点/区域同时表达两个空间指标 | `spatial,choropleth,proportional_symbol,two_metrics` | `choropleth_proportional_symbol_map` | `country_choropleth_map` |
| 组间分布比较 | `distribution,grouped_samples,category_comparison` | `grouped_violin_boxplot` | `boxen_plot`, `model_performance_boxplot` |
| 一维不确定性分布 | `distribution,one_dimensional,uncertainty` | `histogram_kde` | `histogram_ecdf`, `overlapping_kde` |
| 二维联合分布 | `distribution,paired_samples,joint_density` | `joint_kde` | `density_colored_scatter` |
| 预测/观测诊断 | `prediction,observed,predicted,one_to_one` | `predicted_vs_real_scatter` | `parity_plot`, `loglog_model_observation_scatter` |
| PCA 或排序结果 | `ordination,pca,loading_vectors` | `pca_biplot` | `density_colored_scatter` |
| 情景时间序列 | `scenario,time_series,multi_line` | `multi_scenario_timeseries` | `scenario_uncertainty_timeseries` |
| 情景不确定性 | `scenario,time_series,uncertainty_band` | `scenario_uncertainty_timeseries` | `event_period_timeseries` |
| 事件期高亮 | `time_series,event_period,highlight` | `event_period_timeseries` | `simulated_observed_timeseries` |
| 组成比例 | `composition,percent,groups` | `stacked_percentage_bar` | `hundred_percent_stacked_bar_compact`, `horizontal_stacked_bar` |
| 有正负贡献 | `composition,diverging,signed` | `diverging_stacked_bar` | `grouped_bar` |
| 小类别需要放大 | `composition,stacked,zoom_inset` | `horizontal_stacked_bar_zoom` | `horizontal_stacked_bar` |
| SHAP 特征效应分布 | `shap,features,effects` | `shap_summary_beeswarm` | `shap_importance_bar` |
| 概念框架或研究设计 | `framework,conceptual,workflow` | `conceptual_coupling_framework` | `study_regions_task_inputs` |

## 使用规则
- 数据是连续栅格时，先在地图模板中选；数据是区域统计时，选 choropleth；数据是点关系时，选 scatter/model 模板。
- 组成数据先判断目标是“比例”还是“绝对总量”：比例用 100% stacked，绝对总量随时间用 stacked bar/area。
- 模型诊断优先保留一比一线；所有值为正且跨度大时改用 log-log 版本。
- 需要解释模型特征时，平均重要性用 bar，逐样本效应和方向用 beeswarm。
- 标签推荐只负责缩小候选范围；最终必须根据 `best_for`、`avoid_when` 和真实数据字段确认。
