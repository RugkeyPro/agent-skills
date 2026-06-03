# Refactoring Existing Plot Code

当用户提供旧绘图脚本时，agent 的任务不是简单调色或改字号，而是将旧脚本重构为“模板母版脚本”。

---

## 1. 核心原则

必须首先选择最接近的模板，并复制模板绘图代码作为新脚本基础。

不得只在旧绘图代码上做局部美化，例如只改：
- `plt.rcParams`
- `color`
- `figsize`
- `dpi`
- `savefig`

如果旧图需要 publication-quality 输出，应以模板代码重建绘图主体。

---

## 2. 旧代码分区

将旧脚本分为四类：

### 2.1 Data Block：保留
包括：
- import；
- 文件读取；
- 数据筛选；
- 缺失值处理；
- 单位换算；
- 宽表/长表转换；
- 合并数据。

### 2.2 Analysis Block：保留
包括：
- 模型预测；
- 回归；
- 统计检验；
- 分组统计；
- 均值、标准差、置信区间；
- 自定义指标计算。

### 2.3 Plot Block：替换
包括：
- `plt.subplots()`
- `ax.plot()`
- `ax.scatter()`
- `ax.bar()`
- `sns.*plot()`
- 手动 legend；
- 手动 colorbar；
- 手动 tick；
- 手动 annotation。

原则上删除，用模板 `plot()` 主体替换。

### 2.4 Export Block：替换
包括：
- `plt.show()`
- `plt.savefig()`
- `fig.savefig()`
- `plt.close()`

用模板 `save_outputs()` 替换。

---

## 3. 允许保留旧变量名

Agent 可以保留旧脚本中具有明确含义的变量名，例如：
```python
model_df
summary_df
ci_df
pred_df
plot_df
```
但必须在 `prepare_data()` 中把它们整理为模板需要的字段结构。

---

## 4. 允许增加辅助函数

如果用户数据流程复杂，可以增加：
```python
compute_statistics()
prepare_uncertainty()
reshape_long_to_wide()
merge_model_outputs()
format_labels()
```
但最终绘图仍应使用复制来的模板 `plot()` 主体作为基础。

---

## 5. 微调与扩展

当旧图比模板更复杂时，允许在模板基础上微调扩展，例如：
- 双轴图扩展为三轴；
- 单情景线扩展为多情景线；
- 普通折线增加误差带；
- 地图增加点位图层；
- 柱状图增加误差棒；
- 散点图增加分组颜色。

扩展必须保持模板视觉风格。

---

## 6. 输出脚本要求

最终脚本必须完整包含：
* 模板头注释；
* `TEMPLATE_ID`
* `FIELD_MAP`
* `TEXT_CONFIG`
* `STYLE_CONFIG`
* `EXPORT_CONFIG`
* `load_data()`
* `prepare_data()`
* `plot()`
* `save_outputs()`
* `main()`

推荐在脚本头部注明：
```python
# SOURCE_MODE: refactor_existing_script
# TEMPLATE_BASE: copied_from_templates/<template_id>.py
# OLD_CODE_KEPT: data loading, cleaning, statistics
# OLD_CODE_REPLACED: plotting and exporting
```
