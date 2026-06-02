import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.gridspec import GridSpec


# =========================================================
# 1. 示例数据
# =========================================================

# 主图类别
polymers = ["ABS", "PS", "PVC", "PP", "PE"]
x = np.arange(len(polymers))

# 正向部分：埋藏碳贡献
# 单位：%
buried_carbon_from_sedimented = np.array([3, 10, 6, 7, 10])
buried_carbon_from_beached = np.array([4, 8, 5, 20, 25])

# 负向部分：塑料去向比例
# 单位：%
sedimented_plastic = np.array([3, 9, 15, 7, 10])
beached_plastic = np.array([4, 7, 8, 18, 22])

# 右侧 Total 小面板
# 这里示例用 0–0.5 的比例尺度
total_buried_sedimented = 0.13
total_buried_beached = 0.22
total_sedimented = 0.18
total_beached = 0.27


# =========================================================
# 2. 颜色设置
# =========================================================

colors = {
    "buried_beached": "#b8d2ec",      # 浅蓝
    "buried_sedimented": "#4f94cf",   # 深蓝
    "sedimented": "#f07f2f",          # 橙色
    "beached": "#f6c6a6",             # 浅橙
}


# =========================================================
# 3. 创建画布：左侧主图 + 右侧 Total 面板
# =========================================================

fig = plt.figure(figsize=(7.2, 3.1), dpi=300)

gs = GridSpec(
    nrows=1,
    ncols=2,
    width_ratios=[5.3, 1.45],
    wspace=0.07
)

ax = fig.add_subplot(gs[0, 0])
ax_total = fig.add_subplot(gs[0, 1])


# =========================================================
# 4. 左侧主图：正负向堆叠柱状图
# =========================================================

bar_width = 0.34

# 正向：先画深蓝，再画浅蓝
ax.bar(
    x,
    buried_carbon_from_sedimented,
    width=bar_width,
    color=colors["buried_sedimented"],
    edgecolor="black",
    linewidth=0.35,
    zorder=3
)

ax.bar(
    x,
    buried_carbon_from_beached,
    bottom=buried_carbon_from_sedimented,
    width=bar_width,
    color=colors["buried_beached"],
    edgecolor="black",
    linewidth=0.35,
    zorder=3
)

# 负向：先画橙色，再继续向下画浅橙
ax.bar(
    x,
    -sedimented_plastic,
    width=bar_width,
    color=colors["sedimented"],
    edgecolor="black",
    linewidth=0.35,
    zorder=3
)

ax.bar(
    x,
    -beached_plastic,
    bottom=-sedimented_plastic,
    width=bar_width,
    color=colors["beached"],
    edgecolor="black",
    linewidth=0.35,
    zorder=3
)

# 零线
ax.axhline(
    0,
    color="black",
    linewidth=0.8,
    zorder=2
)


# =========================================================
# 5. 右侧 Total 面板
# =========================================================

x_total = [0]
total_width = 0.36

# 正向
ax_total.bar(
    x_total,
    total_buried_sedimented,
    width=total_width,
    color=colors["buried_sedimented"],
    edgecolor="black",
    linewidth=0.35,
    zorder=3
)

ax_total.bar(
    x_total,
    total_buried_beached,
    bottom=total_buried_sedimented,
    width=total_width,
    color=colors["buried_beached"],
    edgecolor="black",
    linewidth=0.35,
    zorder=3
)

# 负向
ax_total.bar(
    x_total,
    -total_sedimented,
    width=total_width,
    color=colors["sedimented"],
    edgecolor="black",
    linewidth=0.35,
    zorder=3
)

ax_total.bar(
    x_total,
    -total_beached,
    bottom=-total_sedimented,
    width=total_width,
    color=colors["beached"],
    edgecolor="black",
    linewidth=0.35,
    zorder=3
)

ax_total.axhline(
    0,
    color="black",
    linewidth=0.8,
    zorder=2
)


# =========================================================
# 6. 左侧主图坐标轴设置
# =========================================================

ax.set_xlim(-0.6, len(polymers) - 0.5)
ax.set_ylim(-45, 45)

ax.set_xticks(x)
ax.set_xticklabels(polymers, fontsize=12)

ax.set_ylabel(
    "Proportion (%)",
    fontsize=12
)

# 为了贴近原图，负向刻度也显示为正数
yticks = [-40, -30, -20, -10, 0, 10, 20, 30, 40]
yticklabels = ["40", "30", "20", "10", "0", "10", "20", "30", "40"]

ax.set_yticks(yticks)
ax.set_yticklabels(yticklabels, fontsize=10)

ax.tick_params(
    axis="both",
    direction="in",
    length=4,
    width=0.8
)

for spine in ax.spines.values():
    spine.set_linewidth(0.8)

ax.grid(False)


# =========================================================
# 7. 右侧 Total 面板坐标轴设置
# =========================================================

ax_total.set_xlim(-0.55, 0.55)
ax_total.set_ylim(-0.5, 0.5)

ax_total.set_xticks([0])
ax_total.set_xticklabels(["Total"], fontsize=12)

# y 轴放到右侧
ax_total.yaxis.tick_right()
ax_total.yaxis.set_label_position("right")

total_ticks = [-0.4, -0.2, 0, 0.2, 0.4]
total_ticklabels = ["0.4", "0.2", "0", "0.2", "0.4"]

ax_total.set_yticks(total_ticks)
ax_total.set_yticklabels(total_ticklabels, fontsize=10)

ax_total.tick_params(
    axis="both",
    direction="in",
    length=4,
    width=0.8
)

# 左侧不要重复刻度
ax_total.tick_params(
    axis="y",
    left=False,
    labelleft=False,
    right=True,
    labelright=True
)

for spine in ax_total.spines.values():
    spine.set_linewidth(0.8)

ax_total.grid(False)


# =========================================================
# 8. 图例设置
# =========================================================

# 上方蓝色图例
legend_top_handles = [
    Patch(
        facecolor=colors["buried_beached"],
        edgecolor="black",
        linewidth=0.35,
        label="Buried carbon from beached plastic"
    ),
    Patch(
        facecolor=colors["buried_sedimented"],
        edgecolor="black",
        linewidth=0.35,
        label="Buried carbon from sedimented plastic"
    )
]

legend_top = ax.legend(
    handles=legend_top_handles,
    loc="upper left",
    bbox_to_anchor=(0.02, 1.01),
    frameon=False,
    fontsize=10,
    handlelength=1.4,
    handleheight=0.9,
    handletextpad=0.4,
    borderpad=0.1,
    labelspacing=0.25
)

# 下方橙色图例
legend_bottom_handles = [
    Patch(
        facecolor=colors["sedimented"],
        edgecolor="black",
        linewidth=0.35,
        label="Sedimented plastic"
    ),
    Patch(
        facecolor=colors["beached"],
        edgecolor="black",
        linewidth=0.35,
        label="Beached plastic"
    )
]

legend_bottom = ax.legend(
    handles=legend_bottom_handles,
    loc="lower left",
    bbox_to_anchor=(0.02, 0.01),
    frameon=False,
    fontsize=10,
    handlelength=1.4,
    handleheight=0.9,
    handletextpad=0.4,
    borderpad=0.1,
    labelspacing=0.25
)

ax.add_artist(legend_top)


# =========================================================
# 9. 保存图片
# =========================================================

plt.savefig(
    "buried_carbon_plastic_diverging_bar.png",
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.04
)

plt.savefig(
    "buried_carbon_plastic_diverging_bar.pdf",
    bbox_inches="tight",
    pad_inches=0.04
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")