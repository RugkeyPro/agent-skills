# Template Index: Scientific Plotting Catalog

See `high-fidelity-policy.md` before using any template. Map templates now expose
high-fidelity modes:

| Template ID | Mode | Source asset(s) | Use case | Visual contract |
|---|---|---|---|---|
| `choropleth_map` | `country_choropleth` | `figure-country-level choropleth map.py` | Global countries/regions or ocean regions colored by binned values | PlateCarree, white ocean, pale land, thin gray borders, internal lower-left patch legend |
| `choropleth_map` | `choropleth_symbols` | `figure-choropleth + proportional symbol map.py` | Polygon values plus scatter/bubble yield or site data | Blue log choropleth, pink proportional points, size legend, bottom horizontal colorbar |
| `choropleth_map` | `proportional_continuous` | `proportional symbol map + continuous color map.py` | Regional point locations with size and continuous color | PlateCarree regional extent, black point outlines, size legend, vertical colorbar, optional inset |
| `choropleth_map` | `proportional_categorical` | `proportional symbol map + categorical color map.py` | National/regional point locations with size and binned category color | Top longitude ticks, category legend, size legend, translucent categorical bubbles |
| `raster_map` | `log_raster` | `figure-log-scale raster map.py` | Default global raster map for environmental risk/load fields | PlateCarree, log colorbar, blue-cyan-yellow-orange-red-purple palette, white land mask |
| `raster_map` | `contour_robinson` | `figure-raster map with contour lines.py` | Global raster with discrete bands and contour overlays | Robinson projection, discrete colorbar with edges, black contour lines, gray land |
| `raster_map` | `quiver_log` | `figure-raster map+quiver map+log colorbar.py` | Ocean parameter fields with flow/current direction | PlateCarree wide single-column, log raster, quiver arrows, vertical log colorbar |
| `raster_map` | `hotspot` | `figure-hotspot_map.py` | Hotspot or terrestrial/ocean mask maps | White/ocean masking, green-yellow-red hotspot palette, inset-style vertical colorbar |

Composition/bar templates now expose high-fidelity modes:

| Template ID | Mode | Source asset(s) | Use case | Visual contract |
|---|---|---|---|---|
| `stacked_percent_bar` | `vertical_percent` | `figure-100%_stacked_bar_chart.py` | Quantile, treatment, or gradient-wise composition percentages | Vertical 100% stacked bars, green-blue-purple-black HFI palette, bottom multi-column legend |
| `stacked_percent_bar` | `horizontal_percent` | `horizontal 100% stacked bar chart.py` | Country/region rankings with long labels and binned composition | Horizontal 100% stacked bars, labels above bars, top compact legend |
| `stacked_percent_bar` | `diverging_total` | `figure-diverging stacked bar chart.py` | Positive/negative environmental contributions plus total panel | Main diverging stacked bars plus right Total panel, split blue/orange legends |
| `stacked_percent_bar` | `stacked_line` | `figure-stacked percentage bar + multi-line chart with secondary y-axis.py` | Composition plus secondary-axis risk/index trajectories | Pastel stacked bars, right-axis lines with markers, split bar/line legends |

Distribution templates now expose high-fidelity modes:

| Template ID | Mode | Source asset(s) | Use case | Visual contract |
|---|---|---|---|---|
| `violin_boxplot` | `boxen_letter_value` | `figure-boxen_plot.py` | Threat/status group distributions with robust quantile layers | Hand-drawn letter-value boxes, jitter background, mean diamond, large axis text |
| `violin_boxplot` | `violin_box` | `figure-grouped violin plot with boxplot overlay.py` | Many environmental/chemical classes with uncertainty distributions | Multicolor violins, internal boxplots, black outlier points, dense rotated labels |
| `violin_boxplot` | `raincloud` | `Raincloud plot.py` | Regional/group distribution with density, raw points, box and mean | Half violin, jittered points, narrow boxplot, mean dot, panel label |
| `violin_boxplot` | `faceted_boxplot` | `figure-faceted grouped boxplot.py` | Region-by-country grouped distributions | Compact single-row facets, colored outlines, per-panel y ranges |

New image-derived template families:

| Template ID | Modes | Source image family | Visual contract |
|---|---|---|---|
| `enriched_scatter` | `enrichment_bubble`, `marginal_true_pred`, `joint_kde_hist`, `grouped_regression`, `residual_diagnostic`, `shap_dependence` | Bubble enrichment, marginal prediction scatter, joint KDE/hist, grouped regression, SVR residuals, SHAP dependence | Preserve bubble-size legends, marginal density panels, dashed fits, confidence bands, metric annotations, and compact panel labels |
| `matrix_heatmap` | `triangular_corr`, `pair_corr_density`, `clustered_heatmap`, `expression_significance` | Correlation matrix, pair density/correlation matrix, clustered heatmap, scaled-expression heatmap | Preserve triangular masks, annotated cells, dendrograms, side annotations, significance stars/NS, and diverging colorbars |
| `time_event_flow` | `ensemble_timeseries`, `event_timeline`, `paired_slope`, `sankey_multistage`, `alluvial_survival`, `ternary_bubble` | Ensemble time series, timeline, paired slope plot, Sankey/alluvial, ternary bubble | Preserve compact timelines, alternating event labels, paired gray lines, pastel ribbons, survival colors, ternary legends |
| `ordination_embedding` | `pca_biplot_marginal`, `pcoa_ellipse`, `rda_biplot`, `embedding_colorbar` | PCA, PCoA, RDA/CCA, MDS/t-SNE/UMAP | Preserve group ellipses, biplot arrows, marginal densities, PERMANOVA annotations, and embedding colorbars |
| `inference_distribution` | `significance_box`, `taxonomic_stacked_bar`, `ridgeline_density`, `forest_ridgeline`, `posterior_distribution`, `dumbbell_caterpillar`, `roc_curve` | Boxplot letters, taxonomic composition, ridgelines, forest/ridgeline meta-analysis, posterior distributions, dumbbell/caterpillar, ROC | Preserve significance letters, compact legends, ridgeline offsets, CI bars, side heatmaps, expected/observed points, specificity axis |

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
