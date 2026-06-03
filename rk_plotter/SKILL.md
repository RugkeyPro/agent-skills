---
name: rk_plotter
description: 科研绘图模板重构 skill。用于从 0 生成科研绘图脚本，或将用户已有绘图代码重构为模板基础脚本；必须以模板代码为母版，只替换数据、字段、文字、尺寸和导出设置，不默认改变图形基本形式。
---

# rk_plotter: 科研绘图模板重构 Skill

本 Skill 旨在通过**可读、可改、可交付**的完整 Python 绘图脚本服务于科学表达与模板改写流程。

---

## 核心工作原则
每次接收到科研绘图任务时，你必须：
1. **判断任务类型**：
   - **工作流 A (从 0 绘图)**: 根据数据结构选择匹配模板，复制模板代码并填入用户数据路径。
   - **工作流 B (重构旧绘图代码)**: 分离旧代码的数据逻辑和绘图逻辑，保留数据处理 block，用模板 plot() block 替换原有绘图主体。
   - **工作流 C (优化已有图)**: 原图结构合理时，仅用模板的 rcParams、配色和导出规则重写样式层。
2. **选择并阅读模板**：
   - 检查用户数据维度，对照 [template-index.md](file:///c:/Users/Lenovo/Desktop/essay1/.agents/skills/rk_plotter/references/template-index.md) 选择最佳模板。
   - 读取 [templates/](file:///c:/Users/Lenovo/Desktop/essay1/.agents/skills/rk_plotter/templates/) 目录下的对应 `.py` 脚本，以其代码为母版进行改写。
3. **显式数据绑定**：
   - 使用 `FIELD_MAP` 绑定实际列名，禁止直接使用列索引（如 `iloc[:, 0]`）强行猜测数据科学含义。
4. **输出完整脚本**：
   - 最终交付给用户的必须是**完整、独立运行**的脚本，不能只给出 diff 片段或黑盒函数调用。

---

## 🚫 禁止事项
除非用户明确要求，否则禁止：
- 改变基本图形类型（如把散点图改柱状图）。
- 改变面板/子图数量。
- 删除模板中的 colorbar、legend、参考线、误差带或 panel 标签（A/B/C/D）。
- 只输出 PNG，不输出 SVG/PDF 矢量图。
- 遗留交互式 blocking 语句 `plt.show()`。

---

## 📖 参考指南目录
请务必遵循以下文档执行具体操作：
- 🚀 **工作流规范**: [workflow.md](file:///c:/Users/Lenovo/Desktop/essay1/.agents/skills/rk_plotter/references/workflow.md)
- 📊 **模板索引**: [template-index.md](file:///c:/Users/Lenovo/Desktop/essay1/.agents/skills/rk_plotter/references/template-index.md)
- 🚧 **修改边界**: [edit-boundary.md](file:///c:/Users/Lenovo/Desktop/essay1/.agents/skills/rk_plotter/references/edit-boundary.md)
- 🎨 **样式规范**: [style-contract.md](file:///c:/Users/Lenovo/Desktop/essay1/.agents/skills/rk_plotter/references/style-contract.md)
- 🔧 **代码重构规则**: [refactor-code.md](file:///c:/Users/Lenovo/Desktop/essay1/.agents/skills/rk_plotter/references/refactor-code.md)
- ✅ **QA 检查清单**: [qa-checklist.md](file:///c:/Users/Lenovo/Desktop/essay1/.agents/skills/rk_plotter/references/qa-checklist.md)
