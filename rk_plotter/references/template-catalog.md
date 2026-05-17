# Template Catalog

Use this catalog before writing plotting code. Pick the closest template id, inspect `scripts/templates/<template_id>.py`, and replace `make_sample_data()` with real data while preserving `plot()` and `render()`.

| Template id | Category | Title | Use | Original script | Preview basename | Optional deps |
|---|---|---|---|---|---|---|
| `hotspot_map` | maps | Hotspot raster map | continuous spatial intensity or hotspot surfaces | `figure-hotspot_map.py` | `terrestrial_vertebrates_hotspot_map` | cartopy |
| `boxen_plot` | distributions | Boxen style group distribution | group distributions with quantile bands | `figure-boxen_plot.py` | `amphibian_boxenplot_template` | - |
| `pca_biplot` | scatter_model | PCA biplot with loading vectors | ordination scores and loading arrows | `figure-PCA_Bi_Plot.py` | `pca_biplot_unoccupied_habitats` | - |
| `stacked_percentage_bar` | bar_composition | 100 percent stacked bar chart | composition shares across groups | `figure-100%_stacked_bar_chart.py` | `stacked_percentage_bar_hfi_levels` | - |
| `density_colored_scatter` | scatter_model | Density colored scatter plot | dense point clouds with density color | `figure-density_colored_scatter_plot.py` | `density_scatter_hotspot_climate` | scipy |
| `binary_proportion_bar` | bar_composition | Binary proportion bar chart | two-state proportions | `figure-binary_proportion_bar_chart.py` | `protected_unprotected_barplot` | - |
| `stacked_bar_over_time` | bar_composition | Stacked bar chart over time | temporal component bars | `figure-stacked_bar_chart_over_time.py` | `stacked_bar_sales_volume_by_year` | - |
| `simulated_observed_timeseries` | time_series | Simulated-observed time-series comparison | model output versus observations | `figure-simulated–observed time series comparison plot.py` | `simulated_observed_time_series` | - |
| `multi_scenario_timeseries` | time_series | Multi-scenario time-series line plot | multiple scenario trajectories | `figure-multi-scenario time series line plot.py` | `multi_scenario_concentration_timeseries` | - |
| `horizontal_grouped_dual_axis_bar` | bar_composition | Horizontal grouped bar with dual x-axes | paired metrics with paired units | `figure-horizontal grouped bar chart with dual x-axes.py` | `dual_axis_horizontal_bar_hg_mehg` | - |
| `stacked_area_chart` | time_series | Stacked area chart | cumulative flow or budget components | `figure-stacked area chart.py` | `riverine_hg_export_stacked_area` | - |
| `loglog_model_observation_scatter` | scatter_model | Log-log model-observation scatter | comparisons spanning orders of magnitude | `figure-log-log model–observation comparison scatter plot.py` | `model_observation_loglog_scatter` | - |
| `choropleth_proportional_symbol_map` | maps | Choropleth plus proportional symbol map | choropleths with magnitude overlays | `figure-choropleth + proportional symbol map.py` | `global_mehg_export_yield_map` | cartopy |
| `log_scale_raster_map` | maps | Log-scale raster map | right-skewed spatial fields | `figure-log-scale raster map.py` | `global_plastic_ingestion_risk_map` | cartopy |
| `latitudinal_profile_line` | time_series | Latitudinal profile line plot | zonal means or meridional profiles | `figure-latitudinal profile line plot.py` | `latitudinal_profile_ingestion_risk` | - |
| `stacked_percentage_multiline_secondary_axis` | bar_composition | Stacked percent bar plus multiline secondary axis | composition bars plus related lines | `figure-stacked percentage bar + multi-line chart with secondary y-axis.py` | `plastic_type_contribution_and_ingestion_risk` | - |
| `raster_quiver_log_colorbar` | maps | Raster map with quiver and log colorbar | gridded fields with directional vectors | `figure-raster map+quiver map+log colorbar.py` | `global_microbe_exposure_risk_map` | cartopy |
| `grouped_bar` | bar_composition | Grouped bar chart | side-by-side category comparisons | `figure-grouped bar chart.py` | `future_risk_index_grouped_bar` | - |
| `conceptual_coupling_framework` | framework | Conceptual coupling framework diagram | process frameworks and coupling diagrams | `figure-conceptual coupling framework diagram.py` | `nju_mp_darwin_coupling_framework` | - |
| `diverging_stacked_bar` | bar_composition | Diverging stacked bar chart | signed contributions around zero | `figure-diverging stacked bar chart.py` | `buried_carbon_plastic_diverging_bar` | - |
| `depth_profile_cumulative_line` | time_series | Depth-profile cumulative line plot | vertical profiles or sediment columns | `figure-depth-profile cumulative line plot.py` | `cumulative_sediment_plastic_mass_depth_profile` | - |
| `predicted_vs_real_scatter` | scatter_model | Predicted vs real scatter plot | prediction diagnostics with one-to-one lines | `figure-Predicted vs. Real scatter plot.py` | `transformer_predicted_vs_real_removal` | - |
| `shap_summary_beeswarm` | ml_explainability | SHAP summary beeswarm plot | feature effects across samples | `figure-SHAP summary beeswarm plot.py` | `shap_summary_beeswarm_template` | - |
| `shap_importance_bar` | ml_explainability | SHAP importance horizontal bar chart | ranked feature importance | `figure-SHAP importance horizontal bar chart.py` | `shap_importance_barplot` | - |
| `study_regions_task_inputs` | framework | Study regions, tasks, and inputs overview | overview figures for regions and inputs | `figure-study regions + task + inputs.py` | `stimp_overview_framework` | - |
| `model_performance_boxplot` | distributions | Model performance comparison boxplot | model error or metric comparisons | `figure-model performance comparison boxplot.py` | `model_mae_boxplot_yangtze_river_estuary` | - |
| `radar_chart` | bar_composition | Radar chart | multimetric comparisons | `figure-radar chart.py` | `radar_chart_yangtze_river_estuary` | - |
| `joint_kde` | distributions | Joint KDE plot | paired distributions with marginal density | `figure-Joint KDE plot.py` | `joint_kde_truth_imputed_missing_rate_07` | scipy |
| `histogram_kde` | distributions | Histogram with KDE curve | one-dimensional distribution with density | `figure-histogram with KDE curve.py` | `prediction_uncertainty_histogram_kde` | scipy |
| `parity_plot` | scatter_model | Parity plot | train/test predicted-vs-reported comparisons | `figure-parity plot.py` | `predicted_vs_reported_pod_scatter` | - |
| `histogram_ecdf` | distributions | Histogram plus empirical cumulative distribution | uncertainty distributions with cumulative probability | `figure-histogram + empirical cumulative distribution plot.py` | `prediction_uncertainty_hist_cdf` | - |
| `grouped_violin_boxplot` | distributions | Grouped violin plot with boxplot overlay | distribution shape plus median and IQR | `figure-grouped violin plot with boxplot overlay.py` | `uncertainty_violin_boxplot_by_chemical_class` | - |
| `global_raster_vessel_fraction` | maps | Global raster map of publicly tracked vessel fraction | global gridded fractions or exposure | `figure-global raster map of publicly tracked vessel fraction.py` | `global_publicly_tracked_fishing_vessels` | cartopy |
| `horizontal_stacked_bar` | bar_composition | Horizontal stacked bar chart | composition across ranked long labels | `figure-horizontal stacked bar chart.py` | `transport_energy_vessels_stacked_bar` | - |
| `country_choropleth_map` | maps | Country-level choropleth map | country or administrative-unit maps | `figure-country-level choropleth map.py` | `global_country_plastic_emissions_choropleth` | cartopy |
| `faceted_grouped_boxplot` | distributions | Faceted grouped boxplot | grouped distributions split across facets | `figure-faceted grouped boxplot.py` | `regional_country_boxplots` | - |
| `horizontal_stacked_bar_zoom` | bar_composition | Horizontal stacked bar with zoomed inset | small categories needing an inset | `figure-horizontal stacked bar chart with zoomed inset panel.py` | `regional_plastic_emissions_stacked_bar_zoom` | - |
| `hundred_percent_stacked_bar_compact` | bar_composition | Compact 100 percent stacked bar chart | narrow composition panels | `figure-100% stacked bar chart.py` | `rigid_flexible_emissions_stacked_bar` | - |
| `overlapping_kde` | distributions | Overlapping KDE density plot | several one-dimensional densities | `figure-overlapping KDE density plot.py` | `city_plastic_emissions_density_plot` | scipy |
| `scenario_uncertainty_timeseries` | time_series | Scenario time series with uncertainty bands | scenario trajectories with uncertainty | `figure-scenario-based time series plot with uncertainty bands.py` | `ssp_biomass_change_timeseries` | - |
| `scenario_response_curve` | time_series | Scenario response curve plot | response curves or risk ratios | `figure-scenario-based response curve plot.py` | `warming_probability_ratio_rcp_scenarios` | - |
| `raster_contour_map` | maps | Raster map with contour lines | gridded fields with contour overlays | `figure-raster map with contour lines.py` | `global_sst_99percentile_minus_mean` | cartopy |
| `event_period_timeseries` | time_series | Time-series line plot with event period | time series with highlighted event windows | `figure-time series line plot with event-period.py` | `annual_mhw_days_enso_periods` | - |
| `nested_donut` | bar_composition | Nested donut chart | hierarchical mass fate or budget composition | `figure-nested donut chart.py` | `mass_fate_nested_donut_chart` | - |
| `log_scale_timeseries` | time_series | Log-scale time-series plot | series spanning orders of magnitude | `figure-log-scale time series plot.py` | `cumulative_yield_fate_log_timeseries` | - |

## Category Guide

- `maps`: rasters, choropleths, contours, proportional symbols, and vector overlays.
- `distributions`: box/violin/KDE/histogram/ECDF layouts.
- `scatter_model`: dense scatter, parity, log-log, ordination, and diagnostics.
- `time_series`: trajectories, profiles, event windows, uncertainty bands, and log-scale trends.
- `bar_composition`: grouped bars, stacked bars, percent shares, diverging bars, radar charts, and donut charts.
- `ml_explainability`: SHAP-style effects and importance.
- `framework`: conceptual and study-design diagrams.
