import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


# =========================================================
# 1. 示例数据
# =========================================================

countries = [
    "India", "Venezuela", "Thailand", "Viet Nam",
    "Pakistan", "Myanmar", "Indonesia", "Iran",
    "Japan", "Colombia", "Turkey", "Chile",
    "Mexico", "China", "Kazakhstan"
]

# 平均 drawdown ratio，用于国家标签
avg_ratio = np.array([
    39.06, 33.98, 28.54, 28.18,
    26.13, 26.09, 25.43, 25.41,
    25.04, 24.56, 23.83, 23.41,
    22.74, 22.61, 22.40
])

# 各观测等级占比，单位：%
# 每一行对应一个国家
# 列顺序：
# Low value, <10, 10-20, 20-40, 40-80, >80
data = np.array([
    [6,  3,  8, 58, 20,  5],   # India
    [8,  0,  0, 82,  5,  5],   # Venezuela
    [7,  0,  0, 62,  8, 23],   # Thailand
    [6,  3,  7, 48, 19, 17],   # Viet Nam
    [6,  0,  0, 60, 22, 12],   # Pakistan
    [8,  8,  0, 57, 18,  9],   # Myanmar
    [7,  3,  0, 32, 24, 34],   # Indonesia
    [8,  0, 30, 44, 14,  4],   # Iran
    [8,  0, 40, 30, 15,  7],   # Japan
    [9,  0, 31, 50, 10,  0],   # Colombia
    [9,  0, 33, 39, 10,  9],   # Turkey
    [8,  3, 22, 44, 23,  0],   # Chile
    [7,  4, 26, 44, 19,  0],   # Mexico
    [7,  0, 30, 18, 32, 13],   # China
    [8,  0, 38, 23, 30,  1],   # Kazakhstan
], dtype=float)

# 防止示例数据手动输入时每行不等于100，自动归一化
data = data / data.sum(axis=1, keepdims=True) * 100


# =========================================================
# 2. 颜色和标签
# =========================================================

levels = [
    "Low value",
    "<10",
    "10–20",
    "20–40",
    "40–80",
    ">80"
]

colors = {
    "Low value": "#d9d9d9",
    "<10": "#4f7fb9",
    "10–20": "#8fa9b8",
    "20–40": "#f4f3b5",
    "40–80": "#f4a36e",
    ">80": "#df3b2f",
}

level_colors = [colors[l] for l in levels]


# =========================================================
# 3. 创建画布
# =========================================================

fig, ax = plt.subplots(figsize=(4.6, 8.4), dpi=300)

n = len(countries)

# 为每个国家留出“标签行 + 柱状图行”的空间
y = np.arange(n)[::-1] * 1.18
bar_height = 0.55

left = np.zeros(n)


# =========================================================
# 4. 绘制横向百分比堆叠条形图
# =========================================================

for i, level in enumerate(levels):
    ax.barh(
        y,
        data[:, i],
        left=left,
        height=bar_height,
        color=colors[level],
        edgecolor="black",
        linewidth=0.8,
        label=level,
        zorder=3
    )
    left += data[:, i]


# =========================================================
# 5. 添加国家名称与平均比例标签
# =========================================================

for yi, country, ratio in zip(y, countries, avg_ratio):
    if country == "India":
        label = f"{country}: {ratio:.2f}% (Average drawdown ratio)"
    else:
        label = f"{country}: {ratio:.2f}%"

    ax.text(
        1.0,
        yi + 0.43,
        label,
        ha="left",
        va="center",
        fontsize=10,
        fontweight="bold",
        family="serif"
    )


# =========================================================
# 6. 坐标轴设置
# =========================================================

ax.set_xlim(0, 100)

ax.set_ylim(y.min() - 0.75, y.max() + 1.0)

ax.set_xlabel(
    "Percentage (%)",
    fontsize=13,
    fontweight="bold",
    family="serif"
)

ax.set_ylabel(
    "Countries",
    fontsize=16,
    fontweight="bold",
    family="serif",
    labelpad=10
)

ax.set_xticks([0, 20, 40, 60, 80, 100])
ax.set_xticklabels(
    ["0", "20", "40", "60", "80", "100"],
    fontsize=11,
    family="serif"
)

# y 轴不再显示默认国家名，因为已经手动写在条形上方
ax.set_yticks([])

ax.tick_params(
    axis="x",
    direction="out",
    length=4,
    width=1.0
)

ax.tick_params(
    axis="y",
    length=0
)

for spine in ax.spines.values():
    spine.set_linewidth(1.0)
    spine.set_color("black")

ax.grid(False)


# =========================================================
# 7. 顶部图例
# =========================================================

legend_handles = [
    Patch(
        facecolor=colors[level],
        edgecolor="black",
        linewidth=0.8,
        label=level
    )
    for level in levels
]

legend = ax.legend(
    handles=legend_handles,
    title="SWOT observation times per year",
    loc="upper center",
    bbox_to_anchor=(0.50, 1.065),
    ncol=6,
    frameon=False,
    fontsize=9,
    title_fontsize=12,
    handlelength=1.6,
    handleheight=0.9,
    handletextpad=0.35,
    columnspacing=0.55,
    borderpad=0.1
)

legend.get_title().set_fontweight("bold")
legend.get_title().set_family("serif")


# =========================================================
# 8. 可选子图编号
# =========================================================

# 如果需要右上角 d，取消注释
# ax.text(
#     0.98,
#     1.04,
#     "d",
#     transform=ax.transAxes,
#     ha="right",
#     va="bottom",
#     fontsize=18,
#     fontweight="bold",
#     family="serif"
# )


# =========================================================
# 9. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "swot_observation_times_stacked_bar.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "swot_observation_times_stacked_bar.pdf",
    bbox_inches="tight"
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")