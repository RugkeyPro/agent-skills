# rk_plotter 标签体系

先判断数据结构，再判断图形任务；只在命中候选后读取 `templates/*.md` 全文。

| 数据结构 | 标签 | 常见字段 |
|---|---|---|
| 成对数值 | `paired_numeric`, `scatter` | x/y, observed/predicted, real/pred |
| 分组样本 | `grouped_samples`, `distribution` | group, value, hue |
| 时间序列 | `time_series` | time, value, group/scenario |
| 事件时间序列 | `intervention`, `event_period` | time, value, event_start, event_end |
| 组成矩阵 | `composition`, `stacked_bar` | groups, components, values |
| 正负贡献 | `diverging`, `positive_negative` | groups, components, signed_values |
| 经纬度栅格 | `spatial`, `lon_lat_grid` | lon, lat, raster |
| 行政区地图 | `spatial`, `choropleth` | geometry, region, value |
| 二维网格 | `heatmap`, `two_dimensional` | x, y, z |
| 节点流程 | `framework`, `workflow` | nodes, links, labels |

| 用户需求 | 推荐标签 |
|---|---|
| 模型预测值和实测值对比 | `scatter,prediction,observed,predicted,one_to_one` |
| 比较两组或多组样本分布 | `distribution,grouped_samples,boxplot` |
| 展示干预前后变化 | `time_series,intervention,event_period` |
| 展示年度总量及组成 | `time_series,composition,stacked_bar` |
| 展示组成比例 | `composition,percent,stacked_bar` |
| 展示正负贡献 | `diverging,positive_negative,stacked_bar` |
| 展示全球海洋栅格和纬向平均 | `spatial,lon_lat_grid,latitudinal_profile,log_color` |
| 展示行政区颜色和点大小 | `spatial,choropleth,bubble,proportional_symbol` |
| 展示二维响应面或热力图 | `heatmap,two_dimensional,continuous_field` |
| 展示科研流程或研究框架 | `framework,workflow,diagram` |

匹配优先级：必需字段 > 图形任务 > 标签 > 配色/比例。数据结构不匹配时，不要因为外观相似而选择模板。
