# Template Tags

标签用于把“用户的数据和问题”映射到 45 个模板。先提取标签，再运行 selector，最后核对 catalog。

## 标签维度
- 问题类型：`spatial`, `distribution`, `prediction`, `composition`, `time_series`, `scenario`, `framework`, `shap`。
- 数据形态：`lon_lat_grid`, `grouped_samples`, `prediction_pairs`, `scenario_timeseries`, `one_dimensional`, `paired_samples`, `hierarchical`, `vector_field`。
- 视觉编码：`continuous_field`, `percent`, `stacked`, `density`, `one_to_one`, `uncertainty_band`, `choropleth`, `proportional_symbol`, `quiver`, `contour`。
- 尺度/布局：`log_scale`, `wide`, `tall`, `square`, `horizontal`, `faceted`, `secondary_axis`, `zoom_inset`。

## 问题描述到标签
| 用户描述 | 建议标签 |
|---|---|
| 想画全球/区域热点图、风险图、暴露图 | `spatial,lon_lat_grid,continuous_field` |
| 数值跨好几个数量级，想用对数色标 | `spatial,lon_lat_grid,continuous_field,log_scale` |
| 想在地图上叠加方向、流速或风场 | `spatial,lon_lat_grid,vector_field,quiver` |
| 想比较两组或多组数据的分布 | `distribution,grouped_samples,category_comparison` |
| 想展示一列不确定性或误差分布 | `distribution,one_dimensional,uncertainty` |
| 想展示两个变量的联合密度 | `distribution,paired_samples,joint_density` |
| 想展示模型预测 vs 实测 | `prediction,observed,predicted,one_to_one` |
| 预测和实测都为正且跨度大 | `prediction,observed,predicted,one_to_one,log_scale` |
| 想展示多个情景随时间变化 | `scenario,time_series,multi_line` |
| 想展示情景时间序列及置信区间 | `scenario,time_series,uncertainty_band` |
| 想展示组成比例或百分比结构 | `composition,percent,groups` |
| 想展示正负贡献 | `composition,diverging,signed` |
| 想展示 SHAP 每个样本的特征效应 | `shap,features,effects` |
| 想展示特征重要性排序 | `shap,features,importance` |
| 想画研究框架、流程和输入输出 | `framework,conceptual,workflow` |

## 推荐流程
1. 从用户数据中提取 3-6 个标签。优先写数据形态和科学问题，例如 `spatial,lon_lat_grid,continuous_field`。
2. 如果数值跨度超过一个数量级并且全部为正，加入 `log_scale`。
3. 如果有置信区间、集合范围或上下界，加入 `uncertainty_band`。
4. 如果是模型验证，加入 `prediction,observed,predicted,one_to_one`。
5. 运行：`python scripts/select_template.py --tags <tags> --top 5 --explain`。
6. 读取推荐结果的 `best_for` 和 `avoid_when`；若目标数据触发 `avoid_when`，选择下一个模板。

也可以让 selector 对常见需求短句做轻量推断：

```bash
python scripts/select_template.py --query "想比较两组数据的分布" --top 5 --explain
python scripts/select_template.py --query "想展示模型预测 vs 实测" --json
```

## 示例
- 全球连续栅格风险：`spatial,lon_lat_grid,continuous_field,log_scale` -> `log_scale_raster_map` 或 `raster_quiver_log_colorbar`。
- 未来情景和不确定性：`scenario,time_series,uncertainty_band` -> `scenario_uncertainty_timeseries`。
- 预测值与观测值：`prediction,observed,predicted,one_to_one` -> `predicted_vs_real_scatter`, `parity_plot`, 或 `loglog_model_observation_scatter`。
- 组间组成比例：`composition,percent,groups` -> `stacked_percentage_bar` 或 `hundred_percent_stacked_bar_compact`。
- SHAP 逐样本效应：`shap,features,effects` -> `shap_summary_beeswarm`。
