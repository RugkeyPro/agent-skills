import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


# =========================================================
# 1. 构造示例数据
# =========================================================

# x 轴：Hotspot value quantile (%)
quantiles = np.arange(0, 101, 10)

# 五类 HFI 压力等级
levels = [
    "0 (No pressure)",
    "1–2 (Low pressure)",
    "3–5 (Moderate pressure)",
    "6–11 (High pressure)",
    "12–50 (Very high pressure)"
]

# 颜色尽量贴近示例图
colors = {
    "0 (No pressure)": "#d9f2e3",          # 浅绿
    "1–2 (Low pressure)": "#45bfa9",       # 青绿色
    "3–5 (Moderate pressure)": "#2f7fa3",  # 蓝绿色
    "6–11 (High pressure)": "#46366f",     # 紫色
    "12–50 (Very high pressure)": "#0b0303" # 黑色
}

# 示例比例数据：每一列对应一个热点值分位点
# 行顺序与 levels 一致
# 每一列相加应为 100
data = np.array([
    [48, 22, 17, 16, 24, 22, 14,  8, 19, 15,  8],  # 0
    [18, 12, 20, 18, 17, 16, 17, 15, 16, 21,  7],  # 1–2
    [14, 20, 29, 26, 21, 27, 30, 29, 28, 22, 21],  # 3–5
    [12, 24, 25, 22, 21, 22, 23, 27, 30, 23, 29],  # 6–11
    [ 8, 22,  9, 18, 17, 13, 16, 21,  7, 19, 35],  # 12–50
])

# 检查每列是否加和为 100
assert np.allclose(data.sum(axis=0), 100), "每个分位点的堆叠比例之和必须为 100"


# =========================================================
# 2. 绘制百分比堆叠柱状图
# =========================================================

fig, ax = plt.subplots(figsize=(6.2, 4.8), dpi=300)

bottom = np.zeros(len(quantiles))

# 注意：为了让图中黑色高压等级在最底部，
# 绘图顺序从 Very high pressure 到 No pressure
plot_order = [
    "12–50 (Very high pressure)",
    "6–11 (High pressure)",
    "3–5 (Moderate pressure)",
    "1–2 (Low pressure)",
    "0 (No pressure)"
]

level_to_index = {level: i for i, level in enumerate(levels)}

for level in plot_order:
    idx = level_to_index[level]
    values = data[idx]

    ax.bar(
        quantiles,
        values,
        bottom=bottom,
        width=8.8,
        color=colors[level],
        edgecolor="white",
        linewidth=1.0,
        align="center",
        label=level
    )

    bottom += values


# =========================================================
# 3. 坐标轴样式
# =========================================================

ax.set_title(
    "Native habitats",
    fontsize=15,
    pad=8
)

ax.set_xlabel(
    "Hotspot value quantile (%)",
    fontsize=13
)

ax.set_ylabel(
    "Proportion (%)",
    fontsize=13
)

ax.set_xlim(-2, 102)
ax.set_ylim(0, 105)

ax.set_xticks(np.arange(0, 101, 10))
ax.set_yticks([0, 25, 50, 75, 100])

ax.tick_params(
    axis="both",
    labelsize=11,
    direction="out",
    length=4,
    width=0.9
)

# 背景网格，接近原图风格
ax.grid(
    axis="y",
    color="0.88",
    linewidth=0.7
)

ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_linewidth(0.9)


# =========================================================
# 4. 完整 legend
# =========================================================

legend_handles = [
    Patch(facecolor=colors["0 (No pressure)"], edgecolor="none",
          label="0 (No pressure)"),
    Patch(facecolor=colors["1–2 (Low pressure)"], edgecolor="none",
          label="1–2 (Low pressure)"),
    Patch(facecolor=colors["3–5 (Moderate pressure)"], edgecolor="none",
          label="3–5 (Moderate pressure)"),
    Patch(facecolor=colors["6–11 (High pressure)"], edgecolor="none",
          label="6–11 (High pressure)"),
    Patch(facecolor=colors["12–50 (Very high pressure)"], edgecolor="none",
          label="12–50 (Very high pressure)")
]

legend = ax.legend(
    handles=legend_handles,
    title="HFI Levels",
    ncol=3,
    frameon=False,
    fontsize=11,
    title_fontsize=12,
    loc="upper center",
    bbox_to_anchor=(0.5, -0.30),
    handlelength=0.9,
    handleheight=0.9,
    columnspacing=1.6,
    handletextpad=0.4
)

# legend 标题左对齐
legend._legend_box.align = "left"


# =========================================================
# 5. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "stacked_percentage_bar_hfi_levels.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "stacked_percentage_bar_hfi_levels.pdf",
    bbox_inches="tight"
)

plt.show()