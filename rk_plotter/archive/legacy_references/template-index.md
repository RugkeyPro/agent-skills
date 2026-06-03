# rk_plotter 模板索引

正式模板只来自 `templates/*.md`；`new_templates/` 是上传暂存区，未同步前不参与绘图匹配。

| ID | 类别 | 标题 | 触发词 | 标签 | 数据结构 | 布局/比例 | 模板文件 |
|---|---|---|---|---|---|---|---|
| `model_validation_scatter` | scatter_model | 模型预测验证散点图 | 模型预测 vs 实测; 预测值和观测值对比; predicted vs observed; parity plot | `scatter,prediction,observed,predicted,one_to_one,model_diagnostic,two_panel` | paired_numeric_by_model_dataset | two_panel / wide | `templates/模型预测验证散点图.md` |
| `research_workflow_framework` | framework | 科研流程框图 | 科研流程; 研究框架; 方法框图; workflow diagram | `framework,workflow,conceptual,diagram,arrows,process` | nodes_links_annotations | axis_free_multi_block / wide | `templates/科研流程框图.md` |
| `grouped_bar_stacked_area_loglog_validation` | multi_panel | 分组水平柱状图、多类别堆叠面积图、双对数散点验证图 | 多面板综合图; 水平柱状图 堆叠面积 双对数散点; 模型验证组合图 | `multi_panel,bar,stacked_area,loglog_scatter,model_validation,composition,time_series` | category_metrics_plus_component_timeseries_plus_prediction_pairs | three_panel_composite / wide | `templates/分组水平柱状图、多类别堆叠面积图、双对数散点验证图.md` |
| `dual_panel_timeseries_line` | time_series | 双面板时间序列折线图 | 双面板时间序列; 两组时间变化; time series two panels; 双指标折线 | `time_series,line,two_panel,trend,date_axis,comparison` | time_series_by_panel | two_panel_horizontal / wide | `templates/双面板时间序列折线图.md` |
| `density_scatter_two_group_bar` | scatter_bar_combo | 二维密度散点图+两组柱状图 | 二维密度散点 加柱状图; dense scatter with bars; 点云密度和组间比较 | `scatter,density,bar,two_group,combo,continuous_color` | paired_numeric_plus_group_summary | scatter_plus_bar_panels / wide | `templates/二维密度散点图+两组柱状图.md` |
| `choropleth_bubble_map` | map | 分级着色地图 + 气泡点图 | 分级着色地图; 气泡地图; choropleth bubble map; 行政区着色加点大小 | `spatial,map,choropleth,bubble,proportional_symbol,regional,log_color` | polygons_with_point_metrics | map_with_legends / wide | `templates/分级着色地图 + 气泡点图.md` |
| `boxplot_group_distribution` | distribution | 箱线图 | 箱线图; 组间分布比较; boxplot; 分组样本分布 | `distribution,boxplot,grouped_samples,category_comparison,median_iqr` | numeric_samples_by_group | single_or_grouped_panel / standard | `templates/箱线图.md` |
| `diverging_stack_total_depth_profile` | bar_profile_combo | 正负向堆叠柱状图（右侧 Total 独立小面板）+深度剖面折线图 | 正负向堆叠柱状图; 贡献分解和深度剖面; diverging stacked bar depth profile | `diverging,stacked_bar,positive_negative,total_panel,depth_profile,multi_panel` | signed_component_matrix_plus_depth_series | bar_total_profile_composite / wide | `templates/正负向堆叠柱状图（右侧 Total 独立小面板）+深度剖面折线图.md` |
| `choropleth_kde_boxplot_combo` | map_distribution_combo | 分级设色地图+KDE 密度曲线图+箱线图（抖动散点） | 地图 KDE 箱线图; 空间分布加密度分布; choropleth kde boxplot | `spatial,map,choropleth,kde,boxplot,jitter,multi_panel` | regional_spatial_values_plus_grouped_samples | map_plus_distribution_panels / wide | `templates/分级设色地图+KDE 密度曲线图+箱线图（抖动散点）.md` |
| `stacked_percent_dual_axis_line` | composition_timeseries_combo | 百分比堆叠柱状图 + 双 y 轴折线图组合图 | 百分比堆叠柱状图 双y轴折线; 组成比例加趋势线; stacked percent dual axis line | `composition,percent,stacked_bar,dual_axis,line,combo` | groups_by_components_plus_secondary_series | single_panel_twin_y / wide | `templates/百分比堆叠柱状图 + 双 y 轴折线图组合图.md` |
| `taxon_boxplot_pca_stacked_percent` | ecology_multivariate_combo | 类群箱线图+PCA 双标图+堆叠百分比柱状图 | 类群箱线图 PCA 堆叠百分比; 群落组成和PCA; taxon boxplot PCA stacked percent | `distribution,pca,ordination,composition,stacked_bar,multi_panel,ecology` | taxon_samples_plus_ordination_plus_composition_matrix | three_panel_composite / wide | `templates/类群箱线图+PCA 双标图+堆叠百分比柱状图.md` |
| `two_dimensional_distribution` | distribution_2d | 二维分布图 | 二维分布图; 二维密度; 二维概率分布; 2d distribution | `distribution,two_dimensional,heatmap,density,log_color,contour` | x_y_grid_or_paired_samples | single_density_panel / standard | `templates/二维分布图.md` |
| `timeseries_stacked_bar` | time_series_composition | 时间序列堆叠柱状图 | 时间序列堆叠柱状图; 年度组成柱状图; stacked bar over time | `time_series,stacked_bar,composition,annual,components` | time_by_components_matrix | wide_single_panel / wide | `templates/时间序列堆叠柱状图.md` |
| `six_panel_ml_performance` | ml_evaluation | 六面板机器学习预测性能评估组合图 | 六面板机器学习性能评估; 模型性能组合图; machine learning performance panels; 多模型评估 | `machine_learning,model_evaluation,multi_panel,bar,scatter,boxplot,metrics` | model_metrics_plus_prediction_pairs_plus_error_distribution | six_panel_grid / wide | `templates/六面板机器学习预测性能评估组合图.md` |
| `horizontal_stacked_column_chart` | composition | 水平堆叠柱状图 | 水平堆叠柱状图; 横向组成柱状; horizontal stacked column chart | `composition,horizontal,stacked_bar,long_labels,components` | groups_by_components_matrix | horizontal_single_panel / wide | `templates/水平堆叠柱状图.md` |
| `joint_distribution_plot` | distribution_2d | 联合分布图 | 联合分布图; 边缘分布和散点; joint distribution; joint KDE | `distribution,joint,marginal_density,scatter,kde,paired_samples` | paired_numeric_samples | joint_with_marginals / square | `templates/联合分布图.md` |
| `horizontal_stacked_bar` | composition | 水平堆叠条形图 | 水平堆叠条形图; 横向百分比条形图; horizontal stacked bar | `composition,horizontal,stacked_bar,percent,long_labels` | groups_by_components_matrix | compact_horizontal / wide | `templates/水平堆叠条形图.md` |
| `horizontal_stacked_bar_v2` | composition | 水平堆叠条形图2 | 水平堆叠条形图2; 另一版水平堆叠条形; horizontal stacked bar alternative | `composition,horizontal,stacked_bar,percent,alternative_style` | groups_by_components_matrix | horizontal_with_prominent_legend / wide | `templates/水平堆叠条形图2.md` |
| `intervention_period_timeseries` | time_series | 干预期标注时间序列图 | 干预期标注时间序列; 事件窗口时间序列; intervention period time series; 政策前后变化 | `time_series,intervention,event_period,highlight,line,date_axis` | time_series_with_event_windows | wide_line_with_event_spans / wide | `templates/干预期标注时间序列图.md` |
| `dual_panel_scatter_fit` | scatter_model | 双面板散点拟合图 | 双面板散点拟合; 两组散点回归; scatter fit two panels; 关系拟合对比 | `scatter,fit_line,regression,two_panel,relationship,model_annotation` | paired_numeric_by_panel | two_panel_horizontal / wide | `templates/双面板散点拟合图.md` |
| `scatter_relationship_plot` | scatter_model | 散点关系图 | 散点关系图; 连续变量关系; scatter relationship; log scatter | `scatter,relationship,continuous_color,log_scale,trend,overplotting` | paired_numeric_with_optional_color_size | single_scatter_panel / standard | `templates/散点关系图.md` |
| `two_dimensional_heatmap` | heatmap | 二维热力图 | 二维热力图; 二维响应面; heatmap; contour heatmap | `heatmap,two_dimensional,grid,continuous_field,colorbar,contour` | x_y_grid_with_z_values | single_heatmap_panel / standard | `templates/二维热力图.md` |
| `marine_map_latitudinal_profile` | map_profile_combo | 海洋空间分布图 + 纬向剖面线图 | 海洋空间分布图; 全球海洋栅格 纬向剖面; marine map latitudinal profile; 经纬度栅格加纬向剖面 | `spatial,map,lon_lat_grid,latitudinal_profile,log_color,ocean,multi_panel` | lon_lat_grid_plus_latitude_profiles | profile_plus_map / wide | `templates/海洋空间分布图 + 纬向剖面线图.md` |

## 使用规则

1. 先根据用户数据和绘图任务在本表中匹配触发词、标签和数据结构。
2. 命中后再读取对应 `templates/*.md` 全文，保留原模板构图、配色、比例和特殊 artist 逻辑。
3. 多个候选接近时，同时读取候选模板全文，对比 `best_for` 与 `avoid_when` 后择优或组合。
4. 不读取 `new_templates/` 作为绘图入口；只有用户要求同步时才处理暂存模板。
