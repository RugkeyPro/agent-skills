# Workflow: 三类绘图工作流

总原则：**复制本 skill 的模板代码 → 接入真实数据 → 保持视觉风格 → 最小必要扩展**。
不得只"参考"模板效果后另写一套绘图代码，也不得把用户工作目录/项目/notebook 里的其他绘图脚本当作视觉母版——那些旧脚本只能提供数据逻辑、统计逻辑、字段名和科学意图。

模板的事实源是 `templates/manifest.json`（id / family / modes / required_fields / deps / preview）。
选择模板时先读 manifest（或运行 `python scripts/list_options.py --section templates`），再复制 `templates/TEMPLATE_ID.py`。

## 决策默认值：默认自动决策，显式才打断

为了不让每次绘图都变成问答，采用一条明确规则（这条规则优先于任何"出图前必须逐项征询"的旧表述）：

- **默认**：根据数据结构与最近的模板，**自动选定**图型/模式/配色/图例/尺寸/投影等并直接出图。把关键决策写进脚本头注释（`TEMPLATE_ID` / `MODE` / `PALETTE` 等），方便用户回看与修改。
- **仅当**用户表达了显式选择意图（"我想选 / 对比一下 / 列出选项 / 换个配色 / 用哪个模板"），才停下来调用 `python scripts/list_options.py --format markdown` 列出候选，等用户选定后再绘图。
- 模板很多时，先列出全部模板 ID/模式，再结合用户数据推荐最接近的 2–3 个。

## Workflow A：从零绘图

用户有数据/字段但没有旧绘图代码。

1. 明确要表达的科学问题。
2. 检查数据结构：时间列、分组列、数值列、经纬度列、不确定性列、多指标列。
3. 据此从 manifest 选最接近模板（匹配 `required_fields` 与 `tags`）。
4. 复制 `templates/TEMPLATE_ID.py` 的完整代码作为输出脚本基础。
5. 替换数据读取：用户给真实数据则不得在正式输出里保留 demo 数据；仅要预览时可保留。
6. 修改 `FIELD_MAP` / `TEXT_CONFIG` / `STYLE_CONFIG` / `EXPORT_CONFIG`（含 mode 字段）。
7. 按需做同语法扩展（见 `template-guide.md` 的"可扩展边界"）。
8. 输出完整脚本，并用 `python scripts/check_plot.py 脚本.py` 自检。

## Workflow B：重构旧绘图代码

用户给出已有绘图脚本。核心约束：不得只在旧绘图代码上局部美化，必须用匹配模板替换旧绘图主体。

1. 把旧脚本分为 Data block / Analysis block / Plot block / Export block。
2. **保留** Data block（读取、清洗、单位换算、宽长表转换、合并）与 Analysis block（模型预测、回归、检验、分组统计、CI、自定义指标）。
3. **删除** Plot block 与 Export block。
4. 从 manifest 选最接近模板，复制其绘图主体。
5. 把旧脚本最终产生的数据对象（DataFrame / Series / ndarray / 统计表 / 预测结果）接入模板的 `prepare_data`。
6. 旧图比模板复杂时，判断是否属于同视觉语法扩展（双轴→三轴、单线→多线、单图层地图→多图层、折线加误差带）。
7. 统一输出 SVG/PDF/PNG，输出完整新脚本。

推荐在脚本头注明来源：

```python
# SOURCE_MODE: refactor_existing_script
# TEMPLATE_BASE: copied_from_templates/<template_id>.py
# OLD_CODE_KEPT: data loading, cleaning, statistics
# OLD_CODE_REPLACED: plotting and exporting
```

允许保留有明确含义的旧变量名（`model_df` / `summary_df` / `ci_df` / `pred_df`），并可新增辅助函数（`compute_statistics` / `prepare_uncertainty` / `reshape_long_to_wide` 等），但最终绘图仍以复制来的模板 `plot()` 为基础。

## Workflow C：优化已有图

原图结构合理，只是样式/导出不规范。

1. 判断原图最接近哪个模板。
2. 复制该模板的样式层、导出层、布局约束。
3. 尽量保留原图的数据表达关系。
4. 规范 rcParams / 字体 / 字号 / 颜色 / 线宽 / grid / legend / colorbar / savefig。
5. 若原图结构过乱难以修复，转 Workflow B 用模板主体重建。
