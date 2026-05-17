import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


# =========================================================
# 1. 示例数据
# =========================================================

categories = [
    "Ingestion",
    "Entanglement\n(coastal)",
    "Entanglement\n(ocean)",
    "PFOS",
    "MeHg",
    "PAEs",
    "BPA"
]

# 三个等级的相对风险指数比值（%）
# 这里是模拟数据，整体趋势尽量接近示例图
high = np.array([355, 180, 165, 270, 345, 280, 260])
medium = np.array([165, 170,  35, 125, 165, 105, 102])
low = np.array([128, 155,  28,  85, 135,  70,  60])

x = np.arange(len(categories))
bar_width = 0.20


# =========================================================
# 2. 颜色设置
# =========================================================

colors = {
    "High":   "#c2b1c9",  # 淡紫色
    "Medium": "#b6d48a",  # 浅绿色
    "Low":    "#a8c7cf",  # 浅蓝灰
}


# =========================================================
# 3. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(5.2, 3.2), dpi=300)

# 三组柱子
ax.bar(
    x - bar_width,
    high,
    width=bar_width,
    color=colors["High"],
    edgecolor="white",
    linewidth=0.5,
    label="High",
    zorder=3
)

ax.bar(
    x,
    medium,
    width=bar_width,
    color=colors["Medium"],
    edgecolor="white",
    linewidth=0.5,
    label="Medium",
    zorder=3
)

ax.bar(
    x + bar_width,
    low,
    width=bar_width,
    color=colors["Low"],
    edgecolor="white",
    linewidth=0.5,
    label="Low",
    zorder=3
)


# =========================================================
# 4. 参考线
# =========================================================

ax.axhline(
    y=100,
    color="0.45",
    linestyle=(0, (4, 4)),
    linewidth=1.0,
    zorder=2
)


# =========================================================
# 5. 坐标轴设置
# =========================================================

ax.set_title(
    "Future risk index",
    fontsize=13,
    pad=6
)

ax.set_xticks(x)
ax.set_xticklabels(
    categories,
    rotation=45,
    ha="right",
    fontsize=10
)

ax.set_ylim(0, 400)
ax.set_yticks([0, 100, 200, 300, 400])

# 将 y 轴放到右侧，贴近原图
ax.yaxis.set_label_position("right")
ax.yaxis.tick_right()

ax.set_ylabel(
    "Relative risk index ratio (%)",
    fontsize=11,
    rotation=270,
    labelpad=16
)

# 左侧 y 轴刻度隐藏
ax.tick_params(
    axis="y",
    left=False,
    labelleft=False,
    right=True,
    labelright=True,
    direction="out",
    length=3.5,
    width=0.8,
    labelsize=10
)

ax.tick_params(
    axis="x",
    direction="out",
    length=3.5,
    width=0.8,
    labelsize=10
)

# 边框样式
ax.spines["left"].set_visible(True)
ax.spines["top"].set_visible(True)
ax.spines["right"].set_visible(True)
ax.spines["bottom"].set_visible(True)

for spine in ax.spines.values():
    spine.set_linewidth(0.8)

ax.grid(False)


# =========================================================
# 6. 图例
# =========================================================

legend_handles = [
    Patch(facecolor=colors["High"], edgecolor="none", label="High"),
    Patch(facecolor=colors["Medium"], edgecolor="none", label="Medium"),
    Patch(facecolor=colors["Low"], edgecolor="none", label="Low"),
]

ax.legend(
    handles=legend_handles,
    loc="upper right",
    frameon=False,
    fontsize=10,
    handlelength=0.8,
    handletextpad=0.35,
    borderpad=0.2,
    labelspacing=0.3
)


# =========================================================
# 7. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "future_risk_index_grouped_bar.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "future_risk_index_grouped_bar.pdf",
    bbox_inches="tight"
)

plt.show()