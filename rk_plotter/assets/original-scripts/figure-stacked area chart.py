import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


# =========================================================
# 1. 构造示例数据
# =========================================================

months = np.arange(1, 13)

month_labels = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

# 各区域月度贡献，单位：Mg month^-1
# 这里的数据为示例数据，整体趋势模拟原图：夏末秋初最高
data = {
    "South Atlantic": np.array([39, 41, 44, 43, 37, 32, 33, 30, 28, 25, 27, 31]),
    "Indian":         np.array([ 8,  7, 10, 11, 14, 20, 25, 39, 45, 31, 17, 12]),
    "South Pacific":  np.array([10,  9, 10, 10, 12, 13, 17, 19, 18, 19, 14, 13]),
    "North Pacific":  np.array([ 6,  6,  7,  7,  6,  7,  8,  9,  8,  7,  5,  4]),
    "Mediterranean":  np.array([ 4,  4,  5,  6,  7,  6,  4,  3,  2,  2,  2,  2]),
    "North Atlantic": np.array([ 3,  4,  6,  5,  7, 10,  9,  5,  4,  3,  2,  2]),
    "Arctic":         np.array([ 0,  0,  0,  0,  0,  1,  2,  2,  2,  1,  0,  0]),
    "Southern Ocean": np.array([ 0,  0,  1,  1,  1,  1,  2,  2,  2,  1,  1,  1]),
    "Inland":         np.array([0.5, 0.4, 0.6, 0.5, 0.5, 0.7, 0.8, 0.9, 0.8, 0.6, 0.5, 0.5]),
}


# =========================================================
# 2. 设置堆叠顺序和颜色
# =========================================================

# 从底部到顶部的堆叠顺序
stack_order = [
    "South Atlantic",
    "Indian",
    "South Pacific",
    "North Pacific",
    "Mediterranean",
    "North Atlantic",
    "Arctic",
    "Southern Ocean",
    "Inland"
]

colors = {
    "Inland":         "#7ac943",
    "North Atlantic": "#ff8f8f",
    "Mediterranean":  "#55b8e8",
    "South Pacific":  "#ff9800",
    "South Atlantic": "#bfbfbf",
    "Southern Ocean": "#ffc7c7",
    "Arctic":         "#bfe7fb",
    "North Pacific":  "#f4c542",
    "Indian":         "#d9d9d9",
}

y_values = [data[name] for name in stack_order]
stack_colors = [colors[name] for name in stack_order]


# =========================================================
# 3. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(3.4, 5.0), dpi=300)

ax.stackplot(
    months,
    y_values,
    colors=stack_colors,
    edgecolor="none",
    linewidth=0
)


# =========================================================
# 4. 坐标轴设置
# =========================================================

ax.set_xlim(0.5, 12.5)
ax.set_ylim(0, 150)

ax.set_ylabel(
    "Riverine Hg export (Mg month$^{-1}$)",
    fontsize=12
)

ax.set_xlabel(
    "Month",
    fontsize=12,
    labelpad=10
)

# 原图只显示隔月标签
tick_months = [1, 3, 5, 7, 9, 11]
tick_labels = ["January", "March", "May", "July", "September", "November"]

ax.set_xticks(tick_months)
ax.set_xticklabels(
    tick_labels,
    rotation=45,
    ha="right",
    fontsize=10
)

ax.set_yticks([0, 30, 60, 90, 120, 150])
ax.set_yticklabels([0, 30, 60, 90, 120, 150], fontsize=10)

ax.tick_params(
    axis="both",
    direction="in",
    length=4,
    width=0.8
)

for spine in ax.spines.values():
    spine.set_linewidth(0.9)

ax.grid(False)


# =========================================================
# 5. 图例设置
# =========================================================

legend_order = [
    "Inland",
    "North Atlantic",
    "Mediterranean",
    "South Pacific",
    "South Atlantic",
    "Southern Ocean",
    "Arctic",
    "North Pacific",
    "Indian"
]

legend_handles = [
    Patch(
        facecolor=colors[name],
        edgecolor="none",
        label=name
    )
    for name in legend_order
]

ax.legend(
    handles=legend_handles,
    loc="upper left",
    bbox_to_anchor=(0.02, 0.995),
    frameon=False,
    ncol=2,
    fontsize=10,
    handlelength=0.6,
    handletextpad=0.3,
    columnspacing=1.1,
    labelspacing=0.55,
    borderpad=0.1
)


# =========================================================
# 6. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "riverine_hg_export_stacked_area.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "riverine_hg_export_stacked_area.pdf",
    bbox_inches="tight"
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")