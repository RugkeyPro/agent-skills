# Workflow: Scientific Plotting Procedures

## 总原则

所有工作流均遵循：

```text
复制模板代码优先，微调扩展其次。
```

不得只“参考”模板视觉效果后另写一套全新绘图代码。Agent 必须先复制最接近的模板 `.py` 文件的主体代码，再在该代码基础上接入真实数据、调整配置和添加必要元素。

---

## Workflow A: Drawing From Scratch

适用于用户有数据或字段，但没有旧绘图代码。

### Steps

1. 分析用户要表达的科学问题。
2. 检查数据结构：
   - 时间列；
   - 分组列；
   - 数值列；
   - 经纬度列；
   - 不确定性列；
   - 多指标列。
3. 从 `references/template-index.md` 选择最接近模板。
4. 复制 `templates/TEMPLATE_ID.py` 的完整代码作为输出脚本基础。
5. 替换数据读取逻辑：
   - 用户提供真实数据时，不保留 demo 数据作为正式输入；
   - 用户只要求预览时，可以保留 demo 数据。
6. 修改：
   - `FIELD_MAP`
   - `TEXT_CONFIG`
   - `STYLE_CONFIG`
   - `EXPORT_CONFIG`
7. 判断是否需要同语法扩展：
   - 多一个指标族：可增加额外轴；
   - 多一个分组：可增加同类系列；
   - 有 `sd/se/ci`：可增加误差线或误差带；
   - 有阈值：可增加参考线；
   - 有局部区域：可增加 inset。
8. 输出完整脚本。

---

## Workflow B: Refactoring Existing Code

适用于用户给出已有绘图脚本。

### 核心约束

不得直接在旧绘图代码上局部美化。必须优先用匹配模板替换旧绘图主体。

### Steps

1. 阅读旧脚本。
2. 将旧脚本分为：
   - Data block；
   - Analysis/statistics block；
   - Plot block；
   - Export block。
3. 保留 Data block 和 Analysis/statistics block。
4. 删除 Plot block 和 Export block。
5. 选择最接近模板。
6. 复制模板代码作为新绘图主体。
7. 将旧脚本最终产生的数据对象接入模板：
   - DataFrame；
   - Series；
   - NumPy array；
   - 统计结果表；
   - 模型预测结果。
8. 若旧脚本图形结构比模板更复杂，应判断是否属于同视觉语法扩展：
   - 双轴变三轴；
   - 单线变多线；
   - 单图层地图变多图层地图；
   - 普通折线增加 uncertainty band。
9. 保持模板视觉效果，统一输出 SVG/PDF/PNG。
10. 输出完整新脚本。

---

## Workflow C: Optimizing Existing Plot

适用于原始图形结构合理，但样式或导出不规范。

### Steps

1. 判断原图与哪个模板最接近。
2. 复制该模板的样式层、导出层和布局约束。
3. 尽量保留原图的数据表达关系。
4. 替换或规范：
   - rcParams；
   - 字体；
   - 字号；
   - 颜色；
   - 线宽；
   - grid；
   - legend；
   - colorbar；
   - savefig。
5. 若原图结构混乱或难以修复，应改用 Workflow B 重构。
