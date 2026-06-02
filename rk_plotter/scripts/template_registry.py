TEMPLATES = {
    'hotspot_map': {'category': 'maps', 'kind': 'raster_map', 'title': 'Hotspot raster map', 'original': 'figure-hotspot_map.py', 'use': 'continuous spatial intensity or hotspot surfaces', 'preview': 'terrestrial_vertebrates_hotspot_map'},
    'boxen_plot': {'category': 'distributions', 'kind': 'boxen', 'title': 'Boxen style group distribution', 'original': 'figure-boxen_plot.py', 'use': 'group distributions with quantile bands', 'preview': 'amphibian_boxenplot_template'},
    'pca_biplot': {'category': 'scatter_model', 'kind': 'pca', 'title': 'PCA biplot with loading vectors', 'original': 'figure-PCA_Bi_Plot.py', 'use': 'ordination scores and loading arrows', 'preview': 'pca_biplot_unoccupied_habitats'},
    'stacked_percentage_bar': {'category': 'bar_composition', 'kind': 'stacked_percent', 'title': '100 percent stacked bar chart', 'original': 'figure-100%_stacked_bar_chart.py', 'use': 'composition shares across groups', 'preview': 'stacked_percentage_bar_hfi_levels'},
    'density_colored_scatter': {'category': 'scatter_model', 'kind': 'density_scatter', 'title': 'Density colored scatter plot', 'original': 'figure-density_colored_scatter_plot.py', 'use': 'dense point clouds with density color', 'preview': 'density_scatter_hotspot_climate'},
    'binary_proportion_bar': {'category': 'bar_composition', 'kind': 'binary_bar', 'title': 'Binary proportion bar chart', 'original': 'figure-binary_proportion_bar_chart.py', 'use': 'two-state proportions', 'preview': 'protected_unprotected_barplot'},
    'stacked_bar_over_time': {'category': 'bar_composition', 'kind': 'stacked_bar_time', 'title': 'Stacked bar chart over time', 'original': 'figure-stacked_bar_chart_over_time.py', 'use': 'temporal component bars', 'preview': 'stacked_bar_sales_volume_by_year'},
    'simulated_observed_timeseries': {'category': 'time_series', 'kind': 'observed_simulated', 'title': 'Simulated-observed time-series comparison', 'original': 'figure-simulated–observed time series comparison plot.py', 'use': 'model output versus observations', 'preview': 'simulated_observed_time_series'},
    'multi_scenario_timeseries': {'category': 'time_series', 'kind': 'multi_line_time', 'title': 'Multi-scenario time-series line plot', 'original': 'figure-multi-scenario time series line plot.py', 'use': 'multiple scenario trajectories', 'preview': 'multi_scenario_concentration_timeseries'},
    'horizontal_grouped_dual_axis_bar': {'category': 'bar_composition', 'kind': 'horizontal_dual_axis', 'title': 'Horizontal grouped bar with dual x-axes', 'original': 'figure-horizontal grouped bar chart with dual x-axes.py', 'use': 'paired metrics with paired units', 'preview': 'dual_axis_horizontal_bar_hg_mehg'},
    'stacked_area_chart': {'category': 'time_series', 'kind': 'stacked_area', 'title': 'Stacked area chart', 'original': 'figure-stacked area chart.py', 'use': 'cumulative flow or budget components', 'preview': 'riverine_hg_export_stacked_area'},
    'loglog_model_observation_scatter': {'category': 'scatter_model', 'kind': 'loglog_scatter', 'title': 'Log-log model-observation scatter', 'original': 'figure-log-log model–observation comparison scatter plot.py', 'use': 'comparisons spanning orders of magnitude', 'preview': 'model_observation_loglog_scatter'},
    'choropleth_proportional_symbol_map': {'category': 'maps', 'kind': 'choropleth_symbol', 'title': 'Choropleth plus proportional symbol map', 'original': 'figure-choropleth + proportional symbol map.py', 'use': 'choropleths with magnitude overlays', 'preview': 'global_mehg_export_yield_map'},
    'log_scale_raster_map': {'category': 'maps', 'kind': 'log_raster', 'title': 'Log-scale raster map', 'original': 'figure-log-scale raster map.py', 'use': 'right-skewed spatial fields', 'preview': 'global_plastic_ingestion_risk_map'},
    'latitudinal_profile_line': {'category': 'time_series', 'kind': 'latitudinal_profile', 'title': 'Latitudinal profile line plot', 'original': 'figure-latitudinal profile line plot.py', 'use': 'zonal means or meridional profiles', 'preview': 'latitudinal_profile_ingestion_risk'},
    'stacked_percentage_multiline_secondary_axis': {'category': 'bar_composition', 'kind': 'stacked_percent_line', 'title': 'Stacked percent bar plus multiline secondary axis', 'original': 'figure-stacked percentage bar + multi-line chart with secondary y-axis.py', 'use': 'composition bars plus related lines', 'preview': 'plastic_type_contribution_and_ingestion_risk'},
    'raster_quiver_log_colorbar': {'category': 'maps', 'kind': 'raster_quiver', 'title': 'Raster map with quiver and log colorbar', 'original': 'figure-raster map+quiver map+log colorbar.py', 'use': 'gridded fields with directional vectors', 'preview': 'global_microbe_exposure_risk_map'},
    'grouped_bar': {'category': 'bar_composition', 'kind': 'grouped_bar', 'title': 'Grouped bar chart', 'original': 'figure-grouped bar chart.py', 'use': 'side-by-side category comparisons', 'preview': 'future_risk_index_grouped_bar'},
    'conceptual_coupling_framework': {'category': 'framework', 'kind': 'framework', 'title': 'Conceptual coupling framework diagram', 'original': 'figure-conceptual coupling framework diagram.py', 'use': 'process frameworks and coupling diagrams', 'preview': 'nju_mp_darwin_coupling_framework'},
    'diverging_stacked_bar': {'category': 'bar_composition', 'kind': 'diverging_bar', 'title': 'Diverging stacked bar chart', 'original': 'figure-diverging stacked bar chart.py', 'use': 'signed contributions around zero', 'preview': 'buried_carbon_plastic_diverging_bar'},
    'depth_profile_cumulative_line': {'category': 'time_series', 'kind': 'depth_profile', 'title': 'Depth-profile cumulative line plot', 'original': 'figure-depth-profile cumulative line plot.py', 'use': 'vertical profiles or sediment columns', 'preview': 'cumulative_sediment_plastic_mass_depth_profile'},
    'predicted_vs_real_scatter': {'category': 'scatter_model', 'kind': 'predicted_real', 'title': 'Predicted vs real scatter plot', 'original': 'figure-Predicted vs. Real scatter plot.py', 'use': 'prediction diagnostics with one-to-one lines', 'preview': 'transformer_predicted_vs_real_removal'},
    'shap_summary_beeswarm': {'category': 'ml_explainability', 'kind': 'shap_beeswarm', 'title': 'SHAP summary beeswarm plot', 'original': 'figure-SHAP summary beeswarm plot.py', 'use': 'feature effects across samples', 'preview': 'shap_summary_beeswarm_template'},
    'shap_importance_bar': {'category': 'ml_explainability', 'kind': 'shap_bar', 'title': 'SHAP importance horizontal bar chart', 'original': 'figure-SHAP importance horizontal bar chart.py', 'use': 'ranked feature importance', 'preview': 'shap_importance_barplot'},
    'study_regions_task_inputs': {'category': 'framework', 'kind': 'study_framework', 'title': 'Study regions, tasks, and inputs overview', 'original': 'figure-study regions + task + inputs.py', 'use': 'overview figures for regions and inputs', 'preview': 'stimp_overview_framework'},
    'model_performance_boxplot': {'category': 'distributions', 'kind': 'model_boxplot', 'title': 'Model performance comparison boxplot', 'original': 'figure-model performance comparison boxplot.py', 'use': 'model error or metric comparisons', 'preview': 'model_mae_boxplot_yangtze_river_estuary'},
    'radar_chart': {'category': 'bar_composition', 'kind': 'radar', 'title': 'Radar chart', 'original': 'figure-radar chart.py', 'use': 'multimetric comparisons', 'preview': 'radar_chart_yangtze_river_estuary'},
    'joint_kde': {'category': 'distributions', 'kind': 'joint_kde', 'title': 'Joint KDE plot', 'original': 'figure-Joint KDE plot.py', 'use': 'paired distributions with marginal density', 'preview': 'joint_kde_truth_imputed_missing_rate_07'},
    'histogram_kde': {'category': 'distributions', 'kind': 'hist_kde', 'title': 'Histogram with KDE curve', 'original': 'figure-histogram with KDE curve.py', 'use': 'one-dimensional distribution with density', 'preview': 'prediction_uncertainty_histogram_kde'},
    'parity_plot': {'category': 'scatter_model', 'kind': 'parity', 'title': 'Parity plot', 'original': 'figure-parity plot.py', 'use': 'train/test predicted-vs-reported comparisons', 'preview': 'predicted_vs_reported_pod_scatter'},
    'histogram_ecdf': {'category': 'distributions', 'kind': 'hist_ecdf', 'title': 'Histogram plus empirical cumulative distribution', 'original': 'figure-histogram + empirical cumulative distribution plot.py', 'use': 'uncertainty distributions with cumulative probability', 'preview': 'prediction_uncertainty_hist_cdf'},
    'grouped_violin_boxplot': {'category': 'distributions', 'kind': 'violin_box', 'title': 'Grouped violin plot with boxplot overlay', 'original': 'figure-grouped violin plot with boxplot overlay.py', 'use': 'distribution shape plus median and IQR', 'preview': 'uncertainty_violin_boxplot_by_chemical_class'},
    'global_raster_vessel_fraction': {'category': 'maps', 'kind': 'raster_map', 'title': 'Global raster map of publicly tracked vessel fraction', 'original': 'figure-global raster map of publicly tracked vessel fraction.py', 'use': 'global gridded fractions or exposure', 'preview': 'global_publicly_tracked_fishing_vessels'},
    'horizontal_stacked_bar': {'category': 'bar_composition', 'kind': 'horizontal_stacked', 'title': 'Horizontal stacked bar chart', 'original': 'figure-horizontal stacked bar chart.py', 'use': 'composition across ranked long labels', 'preview': 'transport_energy_vessels_stacked_bar'},
    'country_choropleth_map': {'category': 'maps', 'kind': 'country_choropleth', 'title': 'Country-level choropleth map', 'original': 'figure-country-level choropleth map.py', 'use': 'country or administrative-unit maps', 'preview': 'global_country_plastic_emissions_choropleth'},
    'faceted_grouped_boxplot': {'category': 'distributions', 'kind': 'faceted_boxplot', 'title': 'Faceted grouped boxplot', 'original': 'figure-faceted grouped boxplot.py', 'use': 'grouped distributions split across facets', 'preview': 'regional_country_boxplots'},
    'horizontal_stacked_bar_zoom': {'category': 'bar_composition', 'kind': 'horizontal_stacked_zoom', 'title': 'Horizontal stacked bar with zoomed inset', 'original': 'figure-horizontal stacked bar chart with zoomed inset panel.py', 'use': 'small categories needing an inset', 'preview': 'regional_plastic_emissions_stacked_bar_zoom'},
    'hundred_percent_stacked_bar_compact': {'category': 'bar_composition', 'kind': 'stacked_percent', 'title': 'Compact 100 percent stacked bar chart', 'original': 'figure-100% stacked bar chart.py', 'use': 'narrow composition panels', 'preview': 'rigid_flexible_emissions_stacked_bar'},
    'overlapping_kde': {'category': 'distributions', 'kind': 'overlap_kde', 'title': 'Overlapping KDE density plot', 'original': 'figure-overlapping KDE density plot.py', 'use': 'several one-dimensional densities', 'preview': 'city_plastic_emissions_density_plot'},
    'scenario_uncertainty_timeseries': {'category': 'time_series', 'kind': 'scenario_uncertainty', 'title': 'Scenario time series with uncertainty bands', 'original': 'figure-scenario-based time series plot with uncertainty bands.py', 'use': 'scenario trajectories with uncertainty', 'preview': 'ssp_biomass_change_timeseries'},
    'scenario_response_curve': {'category': 'time_series', 'kind': 'response_curve', 'title': 'Scenario response curve plot', 'original': 'figure-scenario-based response curve plot.py', 'use': 'response curves or risk ratios', 'preview': 'warming_probability_ratio_rcp_scenarios'},
    'raster_contour_map': {'category': 'maps', 'kind': 'raster_contour', 'title': 'Raster map with contour lines', 'original': 'figure-raster map with contour lines.py', 'use': 'gridded fields with contour overlays', 'preview': 'global_sst_99percentile_minus_mean'},
    'event_period_timeseries': {'category': 'time_series', 'kind': 'event_period', 'title': 'Time-series line plot with event period', 'original': 'figure-time series line plot with event-period.py', 'use': 'time series with highlighted event windows', 'preview': 'annual_mhw_days_enso_periods'},
    'nested_donut': {'category': 'bar_composition', 'kind': 'nested_donut', 'title': 'Nested donut chart', 'original': 'figure-nested donut chart.py', 'use': 'hierarchical mass fate or budget composition', 'preview': 'mass_fate_nested_donut_chart'},
    'log_scale_timeseries': {'category': 'time_series', 'kind': 'log_timeseries', 'title': 'Log-scale time-series plot', 'original': 'figure-log-scale time series plot.py', 'use': 'series spanning orders of magnitude', 'preview': 'cumulative_yield_fate_log_timeseries'},
}
_ORIGINAL_FIXES = {
    'simulated_observed_timeseries': 'figure-simulated–observed time series comparison plot.py',
    'loglog_model_observation_scatter': 'figure-log-log model–observation comparison scatter plot.py',
}

_STYLE_PROFILES = {
    'hotspot_map': {'figsize': (13.0, 5.2), 'palette': 'sequential_spatial', 'cmap': 'viridis_or_custom_sequential', 'scale': ('linear',), 'layout': ('single_map', 'colorbar', 'plate_carree'), 'plot_primitives': ('imshow', 'colorbar', 'text')},
    'boxen_plot': {'figsize': (4.2, 5.8), 'palette': 'ordered_categorical', 'cmap': None, 'scale': ('linear',), 'layout': ('single_panel',), 'plot_primitives': ('quantile_bands', 'scatter')},
    'pca_biplot': {'figsize': (4.2, 4.1), 'palette': 'score_groups_plus_loadings', 'cmap': 'YlGnBu', 'scale': ('linear',), 'layout': ('single_panel', 'equal_reference_lines'), 'plot_primitives': ('scatter', 'loading_arrows', 'text')},
    'stacked_percentage_bar': {'figsize': (6.2, 4.8), 'palette': 'categorical_composition', 'cmap': None, 'scale': ('percent', 'linear'), 'layout': ('single_panel', 'legend'), 'plot_primitives': ('bar', 'stacked_bar')},
    'density_colored_scatter': {'figsize': (4.2, 3.3), 'palette': 'continuous_density', 'cmap': 'viridis', 'scale': ('linear',), 'layout': ('single_panel', 'inset_colorbar'), 'plot_primitives': ('scatter', 'density_color', 'one_to_one_line')},
    'binary_proportion_bar': {'figsize': (3.1, 3.4), 'palette': 'binary_contrast', 'cmap': None, 'scale': ('percent', 'linear'), 'layout': ('compact_single_panel',), 'plot_primitives': ('bar', 'text_labels')},
    'stacked_bar_over_time': {'figsize': (8.0, 4.9), 'palette': 'temporal_components', 'cmap': None, 'scale': ('linear',), 'layout': ('wide_single_panel', 'legend'), 'plot_primitives': ('bar', 'stacked_bar')},
    'simulated_observed_timeseries': {'figsize': (7.8, 2.6), 'palette': 'observed_vs_model', 'cmap': None, 'scale': ('linear',), 'layout': ('wide_low_panel',), 'plot_primitives': ('line', 'scatter')},
    'multi_scenario_timeseries': {'figsize': (7.4, 5.4), 'palette': 'scenario_lines', 'cmap': None, 'scale': ('linear',), 'layout': ('wide_single_panel', 'legend'), 'plot_primitives': ('line',)},
    'horizontal_grouped_dual_axis_bar': {'figsize': (3.6, 5.4), 'palette': 'paired_metric', 'cmap': None, 'scale': ('linear',), 'layout': ('horizontal', 'dual_x_axis'), 'plot_primitives': ('barh', 'text_labels')},
    'stacked_area_chart': {'figsize': (3.4, 5.0), 'palette': 'component_area', 'cmap': None, 'scale': ('linear',), 'layout': ('tall_single_panel', 'legend'), 'plot_primitives': ('stackplot', 'line')},
    'loglog_model_observation_scatter': {'figsize': (5.4, 5.2), 'palette': 'model_observation', 'cmap': None, 'scale': ('log_x', 'log_y'), 'layout': ('single_panel', 'one_to_one_line'), 'plot_primitives': ('scatter', 'errorbar', 'line', 'text')},
    'choropleth_proportional_symbol_map': {'figsize': (12.0, 5.8), 'palette': 'choropleth_plus_symbols', 'cmap': None, 'scale': ('log_color', 'linear_symbol_size'), 'layout': ('map_projection', 'colorbar', 'symbol_legend'), 'plot_primitives': ('choropleth', 'scatter', 'proportional_symbols')},
    'log_scale_raster_map': {'figsize': (7.0, 4.0), 'palette': 'log_sequential', 'cmap': 'magma_r_or_viridis', 'scale': ('log_color',), 'layout': ('map_projection', 'colorbar'), 'plot_primitives': ('pcolormesh',)},
    'latitudinal_profile_line': {'figsize': (2.2, 3.0), 'palette': 'single_profile', 'cmap': None, 'scale': ('linear',), 'layout': ('narrow_profile',), 'plot_primitives': ('line',)},
    'stacked_percentage_multiline_secondary_axis': {'figsize': (9.2, 5.7), 'palette': 'composition_plus_lines', 'cmap': None, 'scale': ('percent', 'linear_secondary'), 'layout': ('wide_single_panel', 'twin_y'), 'plot_primitives': ('bar', 'stacked_bar', 'line')},
    'raster_quiver_log_colorbar': {'figsize': (6.0, 2.9), 'palette': 'log_spatial_with_vectors', 'cmap': None, 'scale': ('log_color',), 'layout': ('map_projection', 'colorbar', 'quiver_overlay'), 'plot_primitives': ('pcolormesh', 'quiver', 'annotate')},
    'grouped_bar': {'figsize': (5.2, 3.2), 'palette': 'categorical_series', 'cmap': None, 'scale': ('linear',), 'layout': ('single_panel', 'legend'), 'plot_primitives': ('bar',)},
    'conceptual_coupling_framework': {'figsize': (12.2, 6.2), 'palette': 'framework_blocks', 'cmap': None, 'scale': ('none',), 'layout': ('axis_off', 'diagram_canvas'), 'plot_primitives': ('rectangles', 'arrows', 'text')},
    'diverging_stacked_bar': {'figsize': (7.2, 3.1), 'palette': 'diverging_categories', 'cmap': None, 'scale': ('signed_linear',), 'layout': ('grid_spec', 'zero_baseline'), 'plot_primitives': ('bar', 'stacked_bar')},
    'depth_profile_cumulative_line': {'figsize': (4.2, 3.0), 'palette': 'profile_line', 'cmap': None, 'scale': ('linear_x', 'depth_y'), 'layout': ('single_panel', 'inverted_y'), 'plot_primitives': ('line', 'text')},
    'predicted_vs_real_scatter': {'figsize': (3.7, 3.7), 'palette': 'prediction_scatter', 'cmap': None, 'scale': ('linear',), 'layout': ('square_panel', 'one_to_one_line'), 'plot_primitives': ('scatter', 'line', 'text')},
    'shap_summary_beeswarm': {'figsize': (5.2, 3.3), 'palette': 'feature_value_diverging', 'cmap': 'coolwarm', 'scale': ('linear',), 'layout': ('single_panel', 'feature_rank_axis'), 'plot_primitives': ('scatter', 'beeswarm', 'colorbar')},
    'shap_importance_bar': {'figsize': (3.8, 3.1), 'palette': 'single_importance', 'cmap': None, 'scale': ('linear',), 'layout': ('horizontal', 'ranked'), 'plot_primitives': ('barh',)},
    'study_regions_task_inputs': {'figsize': (14.0, 9.0), 'palette': 'overview_map_blocks', 'cmap': 'turbo', 'scale': ('mixed',), 'layout': ('multi_panel', 'map_plus_flow', 'axis_off'), 'plot_primitives': ('imshow', 'scatter', 'text', 'arrows')},
    'model_performance_boxplot': {'figsize': (6.4, 3.9), 'palette': 'model_categories', 'cmap': None, 'scale': ('linear',), 'layout': ('single_panel',), 'plot_primitives': ('boxplot', 'text')},
    'radar_chart': {'figsize': (8.0, 5.2), 'palette': 'multimetric_polygon', 'cmap': None, 'scale': ('normalized',), 'layout': ('polar', 'multi_axis'), 'plot_primitives': ('polar_line', 'fill', 'text')},
    'joint_kde': {'figsize': (6.0, 6.4), 'palette': 'density_contours', 'cmap': None, 'scale': ('linear',), 'layout': ('grid_spec', 'joint_marginal'), 'plot_primitives': ('contour', 'fill_between', 'fill_betweenx', 'scatter')},
    'histogram_kde': {'figsize': (6.0, 2.7), 'palette': 'single_distribution', 'cmap': None, 'scale': ('linear',), 'layout': ('wide_low_panel',), 'plot_primitives': ('hist', 'kde_line')},
    'parity_plot': {'figsize': (6.2, 3.6), 'palette': 'train_test_prediction', 'cmap': None, 'scale': ('linear',), 'layout': ('wide_single_panel', 'one_to_one_line'), 'plot_primitives': ('scatter', 'line', 'text')},
    'histogram_ecdf': {'figsize': (6.2, 3.7), 'palette': 'hist_plus_cdf', 'cmap': None, 'scale': ('linear',), 'layout': ('single_panel', 'twin_y'), 'plot_primitives': ('hist', 'ecdf_line', 'text')},
    'grouped_violin_boxplot': {'figsize': (8.2, 6.0), 'palette': 'grouped_distribution', 'cmap': None, 'scale': ('linear',), 'layout': ('wide_single_panel',), 'plot_primitives': ('violinplot', 'boxplot', 'scatter')},
    'global_raster_vessel_fraction': {'figsize': (12.5, 6.8), 'palette': 'fraction_map', 'cmap': 'sequential_fraction', 'scale': ('linear_0_1',), 'layout': ('map_projection', 'colorbar'), 'plot_primitives': ('pcolormesh', 'text')},
    'horizontal_stacked_bar': {'figsize': (6.1, 2.8), 'palette': 'categorical_composition', 'cmap': None, 'scale': ('linear',), 'layout': ('horizontal', 'legend'), 'plot_primitives': ('barh', 'text_labels')},
    'country_choropleth_map': {'figsize': (12.5, 5.4), 'palette': 'binned_choropleth', 'cmap': None, 'scale': ('binned_color',), 'layout': ('map_projection', 'discrete_colorbar'), 'plot_primitives': ('choropleth',)},
    'faceted_grouped_boxplot': {'figsize': (13.5, 2.15), 'palette': 'facet_categories', 'cmap': None, 'scale': ('linear',), 'layout': ('faceted_row', 'shared_axis'), 'plot_primitives': ('boxplot',)},
    'horizontal_stacked_bar_zoom': {'figsize': (6.6, 5.4), 'palette': 'composition_with_zoom', 'cmap': None, 'scale': ('linear',), 'layout': ('horizontal', 'inset_axes'), 'plot_primitives': ('barh', 'text_labels')},
    'hundred_percent_stacked_bar_compact': {'figsize': (2.0, 5.8), 'palette': 'compact_composition', 'cmap': None, 'scale': ('percent', 'linear'), 'layout': ('narrow_panel', 'legend'), 'plot_primitives': ('bar', 'stacked_bar')},
    'overlapping_kde': {'figsize': (7.4, 3.2), 'palette': 'overlap_density', 'cmap': None, 'scale': ('log_x',), 'layout': ('wide_single_panel',), 'plot_primitives': ('kde_line', 'fill_between')},
    'scenario_uncertainty_timeseries': {'figsize': (7.0, 5.8), 'palette': 'scenario_uncertainty', 'cmap': None, 'scale': ('linear',), 'layout': ('wide_single_panel', 'legend'), 'plot_primitives': ('line', 'fill_between')},
    'scenario_response_curve': {'figsize': (5.4, 4.4), 'palette': 'scenario_response', 'cmap': None, 'scale': ('linear',), 'layout': ('single_panel', 'legend'), 'plot_primitives': ('line', 'scatter', 'text')},
    'raster_contour_map': {'figsize': (8.0, 5.2), 'palette': 'raster_with_contours', 'cmap': None, 'scale': ('binned_color',), 'layout': ('map_projection', 'colorbar', 'contour_overlay'), 'plot_primitives': ('pcolormesh', 'contour', 'text')},
    'event_period_timeseries': {'figsize': (7.4, 4.2), 'palette': 'event_highlight', 'cmap': None, 'scale': ('linear',), 'layout': ('wide_single_panel', 'highlight_band'), 'plot_primitives': ('line', 'axvspan')},
    'nested_donut': {'figsize': (4.6, 4.2), 'palette': 'hierarchical_composition', 'cmap': None, 'scale': ('percent',), 'layout': ('square_panel', 'polar_like'), 'plot_primitives': ('pie', 'nested_rings', 'text')},
    'log_scale_timeseries': {'figsize': (6.4, 5.2), 'palette': 'log_time_lines', 'cmap': None, 'scale': ('log_y',), 'layout': ('wide_single_panel', 'legend'), 'plot_primitives': ('line',)},
}

_DETAILS = {
    'hotspot_map': (('spatial', 'map', 'lon_lat_grid', 'continuous_field', 'hotspot', 'global_extent', 'colorbar', 'wide'), 'regular lon/lat grid with one continuous raster field', ('lon', 'lat', 'raster'), 'global or regional hotspot surfaces where the main message is spatial intensity', 'point-only observations, categorical regions, or values requiring log normalization'),
    'boxen_plot': (('distribution', 'grouped_samples', 'quantiles', 'small_multiples_not_needed', 'tall', 'category_comparison'), 'multiple numeric samples grouped by category', ('groups', 'values'), 'distribution tails and quantile structure for several groups', 'very small sample sizes or paired observations that need connecting lines'),
    'pca_biplot': (('ordination', 'pca', 'scatter', 'loading_vectors', 'multivariate', 'feature_arrows', 'square'), 'ordination scores plus variable loadings', ('scores_x', 'scores_y', 'loadings'), 'PCA or ordination results where sample separation and variable loadings both matter', 'plain x/y relationships without ordination loadings'),
    'stacked_percentage_bar': (('composition', 'percent', 'groups', 'stacked', 'share', 'categorical', 'relative_abundance'), 'groups by components matrix normalized to 100 percent', ('groups', 'components', 'values'), 'component shares across a moderate number of groups', 'absolute totals or more than about eight hard-to-distinguish components'),
    'density_colored_scatter': (('scatter', 'dense_points', 'density', 'continuous_color', 'relationship', 'overplotting'), 'paired numeric x/y observations, often many points', ('x', 'y'), 'large point clouds where overlap hides density structure', 'small samples where direct labels or group colors are more useful'),
    'binary_proportion_bar': (('binary', 'proportion', 'percent', 'two_state', 'compact', 'bar'), 'two-category proportions for one or several groups', ('groups', 'values'), 'protected/unprotected, present/absent, yes/no comparisons', 'multi-component composition or uncertainty distributions'),
    'stacked_bar_over_time': (('composition', 'time_series', 'stacked', 'absolute_values', 'annual', 'components'), 'time index by components matrix', ('time', 'components', 'values'), 'annual or period totals split into components', 'smooth continuous trajectories where lines or areas are clearer'),
    'simulated_observed_timeseries': (('time_series', 'observed', 'simulated', 'model_validation', 'model_diagnostic', 'line', 'points', 'wide'), 'aligned time axis with observed and simulated values', ('time', 'observed', 'simulated'), 'model-observation comparison over time', 'many scenarios or uncertainty envelopes'),
    'multi_scenario_timeseries': (('time_series', 'scenario', 'multi_line', 'trajectory', 'projection', 'wide'), 'time axis with several named scenario series', ('time', 'series', 'labels'), 'several future or experimental trajectories', 'component sums where stacked area/bar would better show totals'),
    'horizontal_grouped_dual_axis_bar': (('bar', 'horizontal', 'dual_axis', 'paired_metrics', 'ranked_categories', 'long_labels'), 'categories with two metrics measured in different units', ('groups', 'metric_a', 'metric_b'), 'two related metrics with different units', 'single-unit comparisons where dual axes add confusion'),
    'stacked_area_chart': (('time_series', 'composition', 'stacked_area', 'cumulative', 'budget', 'components'), 'ordered x-axis with additive component series', ('x', 'series', 'labels'), 'additive components forming a total through time or depth', 'non-additive categories or values that cross below zero'),
    'loglog_model_observation_scatter': (('scatter', 'prediction', 'observed', 'modeled', 'predicted', 'one_to_one', 'model_validation', 'model_diagnostic', 'log_scale', 'orders_of_magnitude'), 'positive observed and modeled values spanning orders of magnitude', ('observed', 'modeled'), 'model validation when both axes are strictly positive and highly skewed', 'zero/negative values or narrow linear-range comparisons'),
    'choropleth_proportional_symbol_map': (('spatial', 'map', 'choropleth', 'proportional_symbol', 'two_metrics', 'regional', 'log_scale'), 'polygons or regions with a color metric and point magnitudes', ('geometry_or_region', 'color_value', 'symbol_value'), 'maps where rate/intensity and total magnitude must be shown together', 'single raster fields or point-only datasets'),
    'log_scale_raster_map': (('spatial', 'map', 'lon_lat_grid', 'continuous_field', 'log_scale', 'right_skewed', 'colorbar'), 'regular lon/lat grid with strictly positive skewed values', ('lon', 'lat', 'raster'), 'risk, concentration, or exposure grids spanning orders of magnitude', 'fields containing zeros/negatives unless transformed'),
    'latitudinal_profile_line': (('profile', 'latitude', 'zonal_mean', 'line', 'gradient', 'tall'), 'latitude or ordered gradient with one response', ('latitude', 'value'), 'summarizing spatial fields into a north-south profile', 'full 2D spatial patterns that need a map'),
    'stacked_percentage_multiline_secondary_axis': (('composition', 'percent', 'secondary_axis', 'multi_line', 'groups', 'combined_chart'), 'groups with component shares plus related response lines', ('groups', 'components', 'values', 'line_series'), 'linking changing composition to one or more summary metrics', 'unrelated metrics or too many line series for a readable secondary axis'),
    'raster_quiver_log_colorbar': (('spatial', 'map', 'lon_lat_grid', 'vector_field', 'quiver', 'log_scale', 'flow', 'colorbar'), 'lon/lat raster plus u/v vector fields', ('lon', 'lat', 'raster', 'u', 'v'), 'exposure or transport maps where magnitude and direction both matter', 'categorical regions or maps with dense vectors that obscure the raster'),
    'grouped_bar': (('bar', 'grouped', 'category_comparison', 'side_by_side', 'groups', 'series'), 'category by series matrix', ('groups', 'series', 'values'), 'a few series compared across categories', 'many categories, long labels, or parts-of-whole composition'),
    'conceptual_coupling_framework': (('framework', 'conceptual', 'workflow', 'process', 'diagram', 'arrows', 'wide'), 'nodes, process blocks, arrows, and annotations', ('nodes', 'links', 'labels'), 'graphical abstracts, method frameworks, and coupled-process schematics', 'quantitative comparisons that need axes'),
    'diverging_stacked_bar': (('composition', 'diverging', 'signed', 'positive_negative', 'zero_baseline', 'contribution'), 'groups by signed components matrix', ('groups', 'components', 'values'), 'positive and negative component contributions around zero', 'pure shares that sum to 100 percent or all-positive totals'),
    'depth_profile_cumulative_line': (('profile', 'depth', 'vertical', 'cumulative', 'line', 'inverted_axis'), 'depth coordinate with cumulative or profile values', ('depth', 'value'), 'sediment, ocean, soil, or atmospheric vertical profiles', 'ordinary calendar time series'),
    'predicted_vs_real_scatter': (('scatter', 'prediction', 'observed', 'predicted', 'one_to_one', 'model_validation', 'model_diagnostic', 'square'), 'paired true and predicted values', ('real', 'predicted'), 'quick regression diagnostics on the original scale', 'orders-of-magnitude data needing log-log axes'),
    'shap_summary_beeswarm': (('shap', 'features', 'effects', 'beeswarm', 'ml_explainability', 'feature_value', 'ranked'), 'samples by features matrix of SHAP/effect values', ('features', 'effects'), 'distribution and direction of feature effects across samples', 'only needing a simple ranked mean importance list'),
    'shap_importance_bar': (('shap', 'features', 'importance', 'bar', 'ranked', 'horizontal', 'ml_explainability'), 'features with scalar importance values', ('features', 'importance'), 'compact ranking of model feature importance', 'per-sample effect distributions or sign information'),
    'study_regions_task_inputs': (('framework', 'overview', 'study_region', 'inputs', 'tasks', 'multi_panel', 'map'), 'study regions, input layers, tasks, and output blocks', ('regions', 'inputs', 'tasks', 'outputs'), 'paper overview figures combining study area, task design, and data inputs', 'single quantitative relationship or simple chart'),
    'model_performance_boxplot': (('distribution', 'model_performance', 'boxplot', 'metrics', 'comparison', 'grouped_samples'), 'model groups with repeated metric values', ('models', 'values'), 'error or score distributions across models', 'single aggregate score per model where bars are enough'),
    'radar_chart': (('radar', 'multimetric', 'normalized', 'profile', 'polar', 'comparison'), 'one or more entities measured on normalized metrics', ('labels', 'values'), 'compact profiles across a small set of normalized metrics', 'raw metrics with incompatible scales or many categories'),
    'joint_kde': (('distribution', 'joint_density', 'kde', 'paired_samples', 'marginal_density', 'square'), 'paired numeric x/y samples', ('x', 'y'), 'bivariate density plus marginal distributions', 'very small samples or categorical axes'),
    'histogram_kde': (('distribution', 'histogram', 'kde', 'one_dimensional', 'uncertainty', 'density'), 'one numeric vector', ('values',), 'a single continuous distribution and its smoothed density', 'discrete counts or grouped distributions needing separate categories'),
    'parity_plot': (('scatter', 'prediction', 'observed', 'predicted', 'one_to_one', 'train_test', 'model_validation', 'model_diagnostic'), 'reported and predicted values, optionally split by subset', ('reported', 'predicted', 'subset'), 'parity diagnostics with train/test or method groups', 'strictly positive orders-of-magnitude data needing log-log axes'),
    'histogram_ecdf': (('distribution', 'histogram', 'ecdf', 'cumulative_probability', 'uncertainty', 'secondary_axis'), 'one numeric vector where density and cumulative probability both matter', ('values',), 'uncertainty or error distributions where percentiles are important', 'multiple groups where overlapping CDFs would clutter'),
    'grouped_violin_boxplot': (('distribution', 'violin', 'boxplot', 'grouped_samples', 'shape', 'median_iqr', 'category_comparison'), 'numeric samples split by groups and optional subgroups', ('groups', 'values'), 'full distribution shapes across groups', 'tiny n per group or values that need paired lines'),
    'global_raster_vessel_fraction': (('spatial', 'map', 'lon_lat_grid', 'continuous_field', 'fraction', 'global_extent', 'colorbar'), 'global lon/lat grid with bounded fraction values', ('lon', 'lat', 'raster'), 'bounded 0-1 or 0-100% global raster fields', 'country-level summaries or strongly log-skewed concentrations'),
    'horizontal_stacked_bar': (('composition', 'stacked', 'horizontal', 'long_labels', 'ranked_categories', 'bar'), 'groups with component values or shares, usually long labels', ('groups', 'components', 'values'), 'composition comparisons with long category labels', 'time trends or many small components requiring an inset'),
    'country_choropleth_map': (('spatial', 'map', 'choropleth', 'country', 'administrative_units', 'binned', 'regional'), 'country or administrative unit metric values', ('region', 'value'), 'national or administrative comparisons with discrete bins', 'regular gridded rasters or precise point locations'),
    'faceted_grouped_boxplot': (('distribution', 'boxplot', 'faceted', 'grouped_samples', 'regional', 'wide'), 'numeric samples grouped by category and split by facet', ('facet', 'groups', 'values'), 'many group distributions organized into readable facets', 'single small group comparison where one panel is enough'),
    'horizontal_stacked_bar_zoom': (('composition', 'stacked', 'horizontal', 'zoom_inset', 'small_categories', 'long_labels'), 'stacked horizontal categories with several small segments', ('groups', 'components', 'values'), 'composition bars where small segments need a zoomed inset', 'simple balanced components where an inset adds unnecessary complexity'),
    'hundred_percent_stacked_bar_compact': (('composition', 'percent', 'stacked', 'compact', 'narrow', 'share', 'groups'), 'few groups by components matrix normalized to 100 percent', ('groups', 'components', 'values'), 'narrow journal panels or side figures showing composition shares', 'many groups or components needing a wider layout'),
    'overlapping_kde': (('distribution', 'kde', 'overlap', 'multiple_groups', 'density', 'log_scale'), 'several numeric vectors to compare distribution shapes', ('values', 'labels'), 'several skewed one-dimensional distributions', 'histogram counts that must be read exactly'),
    'scenario_uncertainty_timeseries': (('time_series', 'scenario', 'uncertainty_band', 'projection', 'multi_line', 'confidence_interval'), 'time axis with scenario central estimates and uncertainty intervals', ('time', 'series', 'lower', 'upper', 'labels'), 'scenario projections with confidence bands or ensemble ranges', 'single observed-vs-simulated comparison without uncertainty'),
    'scenario_response_curve': (('response_curve', 'scenario', 'gradient', 'risk_ratio', 'line', 'threshold'), 'continuous gradient x with response curves by scenario', ('x', 'y', 'scenario'), 'dose-response, warming-response, or risk curves across scenarios', 'calendar time trajectories or categorical bars'),
    'raster_contour_map': (('spatial', 'map', 'lon_lat_grid', 'continuous_field', 'contour', 'gradient', 'colorbar'), 'lon/lat raster with contour-worthy continuous gradients', ('lon', 'lat', 'raster'), 'temperature, anomaly, or threshold fields where contours add structure', 'noisy rasters where contours imply false precision'),
    'event_period_timeseries': (('time_series', 'event_period', 'highlight', 'line', 'annual', 'intervention'), 'time series with one or more event windows', ('time', 'series', 'events'), 'changes before, during, and after named events', 'many overlapping event intervals that obscure the line'),
    'nested_donut': (('composition', 'hierarchical', 'donut', 'nested', 'budget', 'share'), 'two-level hierarchical composition values', ('outer', 'inner'), 'mass fate, budget, or taxonomy composition with two hierarchy levels', 'precise comparison of many small categories'),
    'log_scale_timeseries': (('time_series', 'log_scale', 'orders_of_magnitude', 'cumulative', 'line', 'positive_values'), 'positive time series spanning orders of magnitude', ('time', 'series', 'labels'), 'growth, cumulative yield, or concentration series over several orders of magnitude', 'zero/negative series or small linear-range variation'),
}

_OPTIONAL_REQUIRES = {
    'hotspot_map': ('cartopy', 'scipy'),
    'pca_biplot': ('scipy',),
    'density_colored_scatter': ('scipy',),
    'stacked_bar_over_time': ('pandas',),
    'simulated_observed_timeseries': ('pandas',),
    'multi_scenario_timeseries': ('pandas',),
    'choropleth_proportional_symbol_map': ('cartopy',),
    'log_scale_raster_map': ('cartopy', 'scipy'),
    'raster_quiver_log_colorbar': ('cartopy', 'scipy'),
    'joint_kde': ('scipy',),
    'histogram_kde': ('scipy',),
    'global_raster_vessel_fraction': ('cartopy', 'scipy'),
    'country_choropleth_map': ('cartopy',),
    'overlapping_kde': ('scipy',),
    'raster_contour_map': ('cartopy', 'scipy'),
}


def _aspect_label(figsize):
    width, height = figsize
    ratio = width / height
    if ratio >= 2.0:
        return 'panoramic'
    if ratio >= 1.45:
        return 'wide'
    if ratio <= 0.70:
        return 'tall'
    if 0.85 <= ratio <= 1.15:
        return 'square'
    return 'standard'


def _coordinate_type(tags, style):
    tag_set = set(tags)
    layout = set(style.get('layout', ()))
    scale = set(style.get('scale', ()))
    if 'polar' in layout:
        return 'polar'
    if 'map' in tag_set or 'spatial' in tag_set:
        if 'choropleth' in tag_set or 'country' in tag_set:
            return 'geographic_regions'
        if 'lon_lat_grid' in tag_set:
            return 'lon_lat_grid'
        return 'geographic'
    if 'log_x' in scale and 'log_y' in scale:
        return 'loglog_xy'
    if 'log_y' in scale:
        return 'time_log_y'
    if 'horizontal' in tag_set or 'horizontal' in layout:
        return 'horizontal_categorical'
    if 'depth' in tag_set:
        return 'depth_profile'
    if 'time_series' in tag_set:
        return 'time_value'
    if 'distribution' in tag_set:
        return 'categorical_or_numeric_distribution'
    if 'scatter' in tag_set or 'prediction' in tag_set:
        return 'xy'
    if 'composition' in tag_set:
        return 'categorical_composition'
    if 'framework' in tag_set:
        return 'axis_free_diagram'
    return 'cartesian'


for _template_id, _meta in TEMPLATES.items():
    if _template_id in _ORIGINAL_FIXES:
        _meta['original'] = _ORIGINAL_FIXES[_template_id]
    _style = dict(_STYLE_PROFILES[_template_id])
    _style['aspect'] = _aspect_label(_style['figsize'])
    _tags, _shape, _fields, _best_for, _avoid_when = _DETAILS[_template_id]
    _meta['tags'] = tuple(dict.fromkeys((_meta['category'], _meta['kind'], *_tags)))
    _meta['data_profile'] = {
        'shape': _shape,
        'required_fields': tuple(_fields),
        'signals': _meta['tags'],
    }
    _meta['style_profile'] = _style
    _meta['id'] = _template_id
    _meta['source_file'] = _meta['original']
    _meta['data_shape'] = _shape
    _meta['coordinates'] = _coordinate_type(_meta['tags'], _style)
    _meta['best_for'] = _best_for
    _meta['avoid_when'] = _avoid_when
    _meta['requires'] = ()
    _meta['optional_requires'] = _OPTIONAL_REQUIRES.get(_template_id, ())

CATEGORIES = sorted({item['category'] for item in TEMPLATES.values()})


def template_tags(template_id: str) -> tuple[str, ...]:
    return tuple(TEMPLATES[template_id].get('tags', ()))


def template_profile(template_id: str) -> dict:
    return TEMPLATES[template_id]
