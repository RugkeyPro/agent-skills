import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


# =========================================================
# 1. 示例数据
# =========================================================

regions = [
    "South Atlantic",
    "Indian",
    "South Pacific",
    "North Pacific",
    "North Atlantic",
    "Mediterranean",
    "Arctic",
    "Inland",
    "Southern Ocean"
]

# MeHg export，底部 x 轴单位：kg yr^-1
mehg = np.array([3950, 1650, 1850, 850, 600, 360, 420, 90, 45])
mehg_err = np.array([520, 260, 360, 180, 90, 70, 80, 35, 18])

# Hg export，顶部 x 轴单位：Mg yr^-1
hg = np.array([320, 285, 190, 105, 40, 28, 20, 8, 5])
hg_err = np.array([80, 65, 30, 40, 12, 10, 8, 4, 2])


# =========================================================
# 2. 双轴比例换算
#    底部轴：MeHg 0–5000 kg yr^-1
#    顶部轴：Hg 0–480 Mg yr^-1
# =========================================================

mehg_max = 5000
hg_max = 480

def hg_to_mehg_axis(x):
    """把 Hg 数值换算到底部 MeHg 坐标轴长度"""
    return x / hg_max * mehg_max

def mehg_to_hg_axis(x):
    """把底部 MeHg 坐标轴长度换算成顶部 Hg 数值"""
    return x / mehg_max * hg_max


hg_plot = hg_to_mehg_axis(hg)
hg_err_plot = hg_to_mehg_axis(hg_err)


# =========================================================
# 3. 颜色设置
# =========================================================

region_colors = {
    "South Atlantic": "#bdbdbd",
    "Indian": "#bdbdbd",
    "South Pacific": "#f39c12",
    "North Pacific": "#f4c542",
    "North Atlantic": "#74c7e6",
    "Mediterranean": "#9bd8f0",
    "Arctic": "#f3a0b5",
    "Inland": "#ffffff",
    "Southern Ocean": "#8ccf6a"
}

colors = [region_colors[r] for r in regions]


# =========================================================
# 4. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(3.6, 5.4), dpi=300)

y = np.arange(len(regions))

bar_height = 0.32
offset = 0.18

# Hg：实心条
ax.barh(
    y - offset,
    hg_plot,
    height=bar_height,
    color=colors,
    edgecolor="black",
    linewidth=0.8,
    xerr=hg_err_plot,
    error_kw=dict(
        ecolor="0.25",
        elinewidth=0.8,
        capsize=3,
        capthick=0.8
    ),
    label="Hg",
    zorder=3
)

# MeHg：斜线填充条
ax.barh(
    y + offset,
    mehg,
    height=bar_height,
    color=colors,
    edgecolor="black",
    linewidth=0.8,
    hatch="\\\\\\\\",
    xerr=mehg_err,
    error_kw=dict(
        ecolor="0.25",
        elinewidth=0.8,
        capsize=3,
        capthick=0.8
    ),
    label="MeHg",
    zorder=3
)


# =========================================================
# 5. 坐标轴设置
# =========================================================

ax.set_yticks(y)
ax.set_yticklabels(regions, fontsize=10)

# 让 South Atlantic 在最上方
ax.invert_yaxis()

ax.set_xlim(0, mehg_max)

ax.set_xlabel(
    "MeHg export (kg yr$^{-1}$)",
    fontsize=11,
    labelpad=10
)

ax.set_xticks([0, 2500, 5000])
ax.set_xticklabels(["0", "2,500", "5,000"], fontsize=10)

ax.tick_params(
    axis="x",
    direction="in",
    length=4,
    width=0.8
)

ax.tick_params(
    axis="y",
    length=0,
    width=0,
    pad=4
)

# 顶部 x 轴：Hg export
secax = ax.secondary_xaxis(
    "top",
    functions=(mehg_to_hg_axis, hg_to_mehg_axis)
)

secax.set_xlabel(
    "Hg export (Mg yr$^{-1}$)",
    fontsize=11,
    labelpad=8
)

secax.set_xticks([0, 240, 480])
secax.set_xticklabels(["0", "240", "480"], fontsize=10)

secax.tick_params(
    axis="x",
    direction="in",
    length=4,
    width=0.8
)

# 边框
for spine in ax.spines.values():
    spine.set_linewidth(0.8)

for spine in secax.spines.values():
    spine.set_linewidth(0.8)

ax.grid(False)


# =========================================================
# 6. 图例
# =========================================================

legend_handles = [
    Patch(
        facecolor="white",
        edgecolor="black",
        linewidth=0.8,
        label="Hg"
    ),
    Patch(
        facecolor="white",
        edgecolor="black",
        linewidth=0.8,
        hatch="\\\\\\\\",
        label="MeHg"
    )
]

ax.legend(
    handles=legend_handles,
    loc="lower right",
    bbox_to_anchor=(0.98, 0.02),
    frameon=False,
    fontsize=10,
    handlelength=1.5,
    handletextpad=0.4,
    borderpad=0.2,
    labelspacing=0.35
)


# =========================================================
# 7. 可选：左上角子图编号
# =========================================================

# 如需左上角字母 c，取消下面几行注释
# fig.text(
#     0.02, 0.98,
#     "c",
#     fontsize=16,
#     fontweight="bold",
#     ha="left",
#     va="top"
# )


# =========================================================
# 8. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "dual_axis_horizontal_bar_hg_mehg.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "dual_axis_horizontal_bar_hg_mehg.pdf",
    bbox_inches="tight"
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")