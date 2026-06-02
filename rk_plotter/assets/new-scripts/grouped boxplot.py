import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# 1. 构造示例数据
# =========================================================

np.random.seed(42)

groups = ["1-10", "10-100", "100-1000", ">1000"]

# 模拟不同面积等级下的 drawdown zone ratio
# 小面积湖泊/水库波动更大，大面积水体比例整体偏低
data = [
    np.random.beta(a=1.8, b=9.0, size=280),    # 1-10
    np.random.beta(a=2.0, b=11.0, size=320),   # 10-100
    np.random.beta(a=1.8, b=13.0, size=360),   # 100-1000
    np.random.beta(a=1.4, b=16.0, size=300),   # >1000
]

# 添加部分高值离群点，使图形更接近示例
data[0] = np.concatenate([data[0], np.random.uniform(0.45, 0.70, 12)])
data[1] = np.concatenate([data[1], np.random.uniform(0.38, 0.70, 10)])
data[2] = np.concatenate([data[2], np.random.uniform(0.35, 0.68, 18)])
data[3] = np.concatenate([data[3], np.random.uniform(0.22, 0.50, 15)])

# 限制范围
data = [np.clip(d, 0, 0.72) for d in data]


# =========================================================
# 2. 颜色设置
# =========================================================

colors = [
    "#e84d3c",  # 红色
    "#f3c083",  # 橙色
    "#9ec9bd",  # 青绿色
    "#4f79ad",  # 蓝色
]


# =========================================================
# 3. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(4.3, 3.1), dpi=300)

box = ax.boxplot(
    data,
    positions=np.arange(1, len(groups) + 1),
    widths=0.48,
    patch_artist=True,
    showfliers=True,
    medianprops=dict(
        color="0.25",
        linewidth=1.2
    ),
    boxprops=dict(
        edgecolor="black",
        linewidth=1.0
    ),
    whiskerprops=dict(
        color="black",
        linewidth=1.0
    ),
    capprops=dict(
        color="black",
        linewidth=1.0
    ),
    flierprops=dict(
        marker=".",
        markerfacecolor="black",
        markeredgecolor="black",
        markersize=2.5,
        alpha=0.85
    )
)

# 箱体填色
for patch, color in zip(box["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.90)


# =========================================================
# 4. 坐标轴设置
# =========================================================

ax.set_xticks(np.arange(1, len(groups) + 1))
ax.set_xticklabels(
    groups,
    fontsize=11,
    fontweight="bold",
    family="serif"
)

ax.set_xlabel(
    "Area (km$^2$)",
    fontsize=13,
    fontweight="bold",
    family="serif"
)

ax.set_ylabel(
    "Drawdown zone ratio",
    fontsize=12,
    fontweight="bold",
    family="serif"
)

ax.set_ylim(-0.10, 0.70)
ax.set_yticks([0.0, 0.2, 0.4, 0.6])
ax.set_yticklabels(
    ["0.0", "0.2", "0.4", "0.6"],
    fontsize=11,
    family="serif"
)

ax.tick_params(
    axis="both",
    direction="out",
    length=4,
    width=1.0
)

for spine in ax.spines.values():
    spine.set_linewidth(1.1)
    spine.set_color("black")

ax.grid(False)


# =========================================================
# 5. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "drawdown_zone_ratio_by_area_boxplot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "drawdown_zone_ratio_by_area_boxplot.pdf",
    bbox_inches="tight"
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")