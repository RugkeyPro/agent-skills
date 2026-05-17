import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


# =========================================================
# 1. 示例数据
# =========================================================

regions = [
    "Asia",
    "Europe",
    "N. America",
    "Africa",
    "S. America",
    "Australia"
]

# 总船舶数
total = np.array([22000, 4800, 2600, 2500, 1400, 800])

# 未公开追踪船舶数
not_tracked = np.array([6800, 300, 450, 380, 260, 180])

# 公开追踪船舶数
tracked = total - not_tracked


# =========================================================
# 2. 颜色设置
# =========================================================

colors = {
    "Not publicly tracked": "#e2464d",  # 红色
    "Publicly tracked": "#5b99c8",      # 蓝色
}


# =========================================================
# 3. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(6.1, 2.8), dpi=300)

y = np.arange(len(regions))

# 红色：未公开追踪
ax.barh(
    y,
    not_tracked,
    height=0.45,
    color=colors["Not publicly tracked"],
    edgecolor="none",
    label="Not publicly tracked"
)

# 蓝色：公开追踪，堆叠在红色右侧
ax.barh(
    y,
    tracked,
    left=not_tracked,
    height=0.45,
    color=colors["Publicly tracked"],
    edgecolor="none",
    label="Publicly tracked"
)


# =========================================================
# 4. 右侧总数标签
# =========================================================

for yi, value in zip(y, total):
    ax.text(
        value + 550,
        yi,
        f"{value:,}",
        ha="left",
        va="center",
        fontsize=11
    )


# =========================================================
# 5. 坐标轴设置
# =========================================================

ax.set_yticks(y)
ax.set_yticklabels(regions, fontsize=12)

# Asia 放在最上方
ax.invert_yaxis()

ax.set_xlim(0, 26000)

ax.set_title(
    "Transport and energy (number of vessels)",
    fontsize=13,
    pad=8
)

# 原图不显示 x 轴刻度和坐标轴线
ax.set_xticks([])
ax.tick_params(axis="x", length=0)
ax.tick_params(axis="y", length=0)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.grid(False)


# =========================================================
# 6. 图例
# =========================================================

legend_handles = [
    Patch(
        facecolor=colors["Not publicly tracked"],
        edgecolor="none",
        label="Not publicly tracked"
    ),
    Patch(
        facecolor=colors["Publicly tracked"],
        edgecolor="none",
        label="Publicly tracked"
    )
]

ax.legend(
    handles=legend_handles,
    title="2017–2021",
    loc="lower right",
    bbox_to_anchor=(0.98, -0.08),
    frameon=False,
    fontsize=11,
    title_fontsize=11,
    handlelength=1.0,
    handleheight=1.0,
    handletextpad=0.5,
    labelspacing=0.6
)


# =========================================================
# 7. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "transport_energy_vessels_stacked_bar.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "transport_energy_vessels_stacked_bar.pdf",
    bbox_inches="tight"
)

plt.show()