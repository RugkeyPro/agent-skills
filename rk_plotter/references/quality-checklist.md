# rk_plotter 图形质量检查清单

## 代码规范

- 独立绘图脚本必须先设置 `matplotlib.use("Agg")`，再导入 `matplotlib.pyplot`。
- 保持 `matplotlib.rcParams["svg.fonttype"] = "none"`，或导入 `scripts.rk_plotter_core` 继承该配置。
- 禁止 `plt.show()`。
- 使用 `save_figure()` 或显式 `plt.close(fig)` 关闭 figure。
- 默认导出 `png`, `pdf`, `svg`；PNG 600 dpi；透明背景；`bbox_inches="tight"`。

## 图形语义

- 图形类型必须回答用户的科学问题，不要只按外观选模板。
- 坐标轴、单位、图例、colorbar、统计指标必须可读且不互相遮挡。
- 模板中的虚拟数据生成段必须替换为用户真实数据读取和整理逻辑。
- 多面板图要保持面板标签、比例、配色和原模板构图逻辑。

## 文件检查

- 运行生成脚本后确认 `png/pdf/svg` 均存在且非空。
- 抽查 SVG 文本是否可编辑。
- 若质量不合格，修改绘图脚本后重新生成，直到通过检查。

```bash
python scripts/quality_check.py --script path/to/plot.py --output-dir outputs --formats png pdf svg
```
