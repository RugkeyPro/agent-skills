# QA Checklist

Before completing a plotting task or delivering a script, verify every item on this checklist.

---

## 1. Template Motherboard

- [ ] 脚本是否基于某个 `templates/*.py` 模板复制改写？
- [ ] 是否声明 `TEMPLATE_ID`？
- [ ] 是否保留模板核心绘图函数结构？
- [ ] 是否避免黑盒导入 `rk_plotter` 进行绘图？

---

## 2. Visual Similarity

- [ ] 改写后图形一眼看上去仍像原模板？
- [ ] 图形基本类型是否保持不变？
- [ ] 主布局、legend、colorbar、轴线风格是否保持一致？
- [ ] 字体、字号、颜色和线宽是否继承模板？
- [ ] 新增元素是否没有破坏主图平衡？

---

## 3. Data Binding

- [ ] 是否用 `FIELD_MAP` 显式绑定数据列？
- [ ] 是否替换了正式任务中的 demo 数据逻辑？
- [ ] 是否保留旧代码中的科学计算结果？
- [ ] 是否处理 NaN、排序和单位？

---

## 4. Controlled Adaptation

如果新增了元素：
- [ ] 新元素是否是同视觉语法扩展？
- [ ] 新轴是否与对应数据系列颜色一致？
- [ ] 误差线/带是否不遮挡主数据？
- [ ] 参考线是否简洁克制？
- [ ] inset 是否不破坏主布局？
- [ ] 没有添加长段文字注释？

---

## 5. Output

- [ ] 是否输出 SVG？
- [ ] 是否输出 PDF？
- [ ] 是否输出 PNG？
- [ ] PNG 是否至少 300 dpi，正式图推荐 600 dpi？
- [ ] 是否 `plt.close(fig)`？
- [ ] 是否没有 `plt.show()`？

---

## 6. Syntax

- [ ] 是否通过 `python -m py_compile script.py` 语法编译检查？
