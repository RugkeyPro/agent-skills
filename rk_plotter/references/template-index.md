# Template Index: Scientific Plotting Catalog

本索引用于帮助 agent 选择最接近的绘图模板。模板选择后，必须复制对应模板代码，再基于真实数据微调。

| Template ID | Use Case | Required Fields | Core Visual Grammar | Allowed Natural Adaptations |
|---|---|---|---|---|
| `predicted_vs_real_scatter` | 模型预测诊断 | `observed`, `predicted` | 单面板方形散点图 + 1:1 线 + 回归线 + 指标框 | 增加分组颜色、置信椭圆、边际分布、小型 inset，但保持预测-实测诊断语法 |
| `density_scatter` | 高密度 x/y 点 | `x`, `y` | KDE 密度着色散点 + colorbar | 增加阈值线、分组边界、inset、采样点高亮 |
| `dual_panel_scatter_fit` | 两组关系对比 | `x1`, `y1`, `x2`, `y2` | 左右双面板 + 共享范围 + 拟合线 | 增加置信带、分组点色、统计指标框，但保持双面板结构 |
| `multi_scenario_timeseries` | 多情景时间序列 | `x`, `series` | 多线趋势 + 顶部图例 | 增加情景线、误差带、事件阴影、参考线、局部 inset |
| `scenario_uncertainty_timeseries` | 时间序列不确定性 | `x`, `y`, `lower`, `upper` | 中心线 + 透明置信带 | 增加多组 uncertainty band、事件窗口、阈值线 |
| `event_period_timeseries` | 事件期时间序列 | `x`, `y` | 折线 + `axvspan` 事件阴影 | 增加多事件窗口、多线组、误差带 |
| `stacked_percent_bar` | 组成比例 | `group`, `components` | 100% 堆叠柱状图 + 顶部图例 | 增加组分、增加右轴辅助线、增加误差标记 |
| `horizontal_stacked_bar` | 横向组成比例 | `group`, `components` | 水平 100% 堆叠条形图 | 增加组分、排序、分面、参考线 |
| `boxen_plot` | 分组分布 | `group`, `value` | Seaborn boxen plot | 增加散点叠加、显著性符号、参考线 |
| `violin_boxplot` | 分布密度 + IQR | `group`, `value` | violin + box overlay | 增加散点、显著性符号、分组颜色 |
| `heatmap_2d` | 矩阵/相关性/响应面 | `x`, `y`, `value` | 二维色块 + colorbar | 增加单元格标注、显著性星号、等值线 |
| `raster_map` | 经纬度栅格 | `lon`, `lat`, `value` | 地图投影 + 栅格 + colorbar | 增加点层、边界框、inset；正式图不静默 fallback |
| `global_regional_sst_map` | 全球/区域 SST 变化 | `lon`, `lat`, `delta_sst` | PlateCarree 投影 + contourf + 海陆背景 + 底部 colorbar | 增加样区框、点层、区域 inset、等值线标签 |
| `choropleth_map` | 国家/行政区指标 | `region`, `value` | 分级着色地图 | 增加气泡点、边界、标签，但保持 choropleth 语法 |
| `shap_importance_bar` | 特征重要性 | `feature`, `importance` | 排序水平条形图 | 增加误差线、分组颜色、阈值线 |
| `multipanel_layout` | 多面板组合图 | custom | GridSpec 多面板 + panel labels | 可替换子图内容，但保持总体 panel 网格和标号风格 |
