import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


# =========================================================
# 1. 示例数据
# =========================================================

groups = ["HIC", "LMIC"]

# 比例数据，单位：%
flexible = np.array([33, 56])
rigid = np.array([67, 44])

# 检查每组是否加和为 100
assert np.allclose(flexible + rigid, 100), "每组 Flexible + Rigid 必须等于 100"


# =========================================================
# 2. 颜色设置
# =========================================================

colors = {
    "Rigid": "#a878a5",     # 紫色
    "Flexible": "#9bcce0"   # 浅蓝
}


# =========================================================
# 3. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(2.0, 5.8), dpi=300)

x = np.arange(len(groups))
bar_width = 0.68

# 底部：Flexible
ax.bar(
    x,
    flexible,
    width=bar_width,
    color=colors["Flexible"],
    edgecolor="black",
    linewidth=1.0,
    label="Flexible",
    zorder=3
)

# 顶部：Rigid
ax.bar(
    x,
    rigid,
    bottom=flexible,
    width=bar_width,
    color=colors["Rigid"],
    edgecolor="black",
    linewidth=1.0,
    label="Rigid",
    zorder=3
)


# =========================================================
# 4. 坐标轴设置
# =========================================================

ax.set_ylim(0, 100)
ax.set_xlim(-0.55, 1.55)

ax.set_xticks(x)
ax.set_xticklabels(groups, fontsize=10)

ax.set_yticks([0, 25, 50, 75, 100])
ax.set_yticklabels(["0", "25", "50", "75", "100"], fontsize=10)

ax.set_ylabel(
    "Proportion of emissions",
    fontsize=10,
    labelpad=8
)

ax.tick_params(
    axis="both",
    direction="out",
    length=3.5,
    width=0.9
)

# 只保留左轴和下轴，贴近原图
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.spines["left"].set_linewidth(1.0)
ax.spines["bottom"].set_linewidth(1.0)

ax.grid(False)


# =========================================================
# 5. 图例设置
# =========================================================

legend_handles = [
    Patch(
        facecolor=colors["Rigid"],
        edgecolor="black",
        linewidth=1.0,
        label="Rigid"
    ),
    Patch(
        facecolor=colors["Flexible"],
        edgecolor="black",
        linewidth=1.0,
        label="Flexible"
    )
]

ax.legend(
    handles=legend_handles,
    loc="upper center",
    bbox_to_anchor=(0.50, 1.12),
    ncol=2,
    frameon=False,
    fontsize=9,
    handlelength=1.2,
    handleheight=1.2,
    handletextpad=0.35,
    columnspacing=0.8,
    borderpad=0.1
)


# =========================================================
# 6. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "rigid_flexible_emissions_stacked_bar.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "rigid_flexible_emissions_stacked_bar.pdf",
    bbox_inches="tight"
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")