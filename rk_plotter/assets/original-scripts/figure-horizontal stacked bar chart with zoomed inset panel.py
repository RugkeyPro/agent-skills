import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle
from matplotlib.lines import Line2D


# =========================================================
# 1. 示例数据
# =========================================================

regions = [
    "Southern Asia",
    "Sub-Saharan Africa",
    "South-eastern Asia",
    "Latin America and the Caribbean",
    "Eastern Asia",
    "Eastern Europe",
    "Western Asia",
    "Northern Africa",
    "Central Asia",
    "Rest of Europe",
    "Oceania",
    "Northern America",
]

# 单位：Mt year^-1
# 堆叠顺序：Rural -> Town -> City
rural = np.array([1.0, 2.5, 1.2, 1.1, 0.3, 0.5, 0.2, 0.2, 0.10, 0.08, 0.08, 0.02])
town  = np.array([8.8, 5.2, 3.6, 1.6, 2.4, 0.8, 0.8, 0.9, 0.45, 0.08, 0.05, 0.02])
city  = np.array([5.7, 5.8, 2.8, 2.0, 0.6, 1.0, 1.3, 1.3, 0.30, 0.10, 0.03, 0.02])

total = rural + town + city


# =========================================================
# 2. 颜色设置
# =========================================================

colors = {
    "Rural": "#45bea2",
    "Town":  "#f2b13e",
    "City":  "#cfd2d1",
}


# =========================================================
# 3. 创建画布
# =========================================================

fig = plt.figure(figsize=(6.6, 5.4), dpi=300)

# 主图和局部放大图手动布局，便于控制版式
ax = fig.add_axes([0.32, 0.36, 0.60, 0.56])
ax_zoom = fig.add_axes([0.30, 0.08, 0.64, 0.16])


# =========================================================
# 4. 主图：水平堆叠条形图
# =========================================================

y = np.arange(len(regions))
bar_h = 0.72

ax.barh(
    y,
    rural,
    height=bar_h,
    color=colors["Rural"],
    edgecolor="black",
    linewidth=0.8,
    zorder=3
)

ax.barh(
    y,
    town,
    left=rural,
    height=bar_h,
    color=colors["Town"],
    edgecolor="black",
    linewidth=0.8,
    zorder=3
)

ax.barh(
    y,
    city,
    left=rural + town,
    height=bar_h,
    color=colors["City"],
    edgecolor="black",
    linewidth=0.8,
    zorder=3
)

ax.set_yticks(y)
ax.set_yticklabels(regions, fontsize=9)
ax.invert_yaxis()

ax.set_xlim(0, 16)
ax.set_xticks(np.arange(0, 17, 2))
ax.set_xlabel("Plastic emissions (Mt year$^{-1}$)", fontsize=9)

ax.tick_params(
    axis="both",
    direction="out",
    length=3.5,
    width=0.8,
    labelsize=9
)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.spines["left"].set_linewidth(0.9)
ax.spines["bottom"].set_linewidth(0.9)

ax.grid(False)


# =========================================================
# 5. 图例
# =========================================================

legend_handles = [
    Patch(facecolor=colors["City"], edgecolor="black", linewidth=0.8, label="City"),
    Patch(facecolor=colors["Town"], edgecolor="black", linewidth=0.8, label="Town"),
    Patch(facecolor=colors["Rural"], edgecolor="black", linewidth=0.8, label="Rural"),
]

ax.legend(
    handles=legend_handles,
    loc="lower right",
    bbox_to_anchor=(0.98, 0.03),
    frameon=False,
    fontsize=9,
    handlelength=1.0,
    handleheight=1.0,
    handletextpad=0.5,
    labelspacing=0.5
)


# =========================================================
# 6. 局部放大图：Rest of Europe / Oceania / Northern America
# =========================================================

zoom_regions = ["Rest of Europe", "Oceania", "Northern America"]
zoom_idx = [regions.index(r) for r in zoom_regions]

zrural = rural[zoom_idx]
ztown = town[zoom_idx]
zcity = city[zoom_idx]

zy = np.arange(len(zoom_regions))

ax_zoom.barh(
    zy,
    zrural,
    height=0.72,
    color=colors["Rural"],
    edgecolor="black",
    linewidth=0.8,
    zorder=3
)

ax_zoom.barh(
    zy,
    ztown,
    left=zrural,
    height=0.72,
    color=colors["Town"],
    edgecolor="black",
    linewidth=0.8,
    zorder=3
)

ax_zoom.barh(
    zy,
    zcity,
    left=zrural + ztown,
    height=0.72,
    color=colors["City"],
    edgecolor="black",
    linewidth=0.8,
    zorder=3
)

ax_zoom.set_yticks(zy)
ax_zoom.set_yticklabels(zoom_regions, fontsize=9)
ax_zoom.invert_yaxis()

ax_zoom.set_xlim(0, 0.32)
ax_zoom.set_xticks(np.arange(0, 0.31, 0.05))
ax_zoom.set_xticklabels(
    ["0", "0.05", "0.10", "0.15", "0.20", "0.25", "0.30"],
    fontsize=8
)

ax_zoom.tick_params(
    axis="both",
    direction="out",
    length=3.5,
    width=0.8,
    labelsize=8
)

ax_zoom.spines["top"].set_visible(False)
ax_zoom.spines["right"].set_visible(False)

ax_zoom.spines["left"].set_linewidth(0.9)
ax_zoom.spines["bottom"].set_linewidth(0.9)

ax_zoom.grid(False)


# =========================================================
# 7. 放大框边界
# =========================================================

# 给局部放大图外部加一个矩形边框，接近原图效果
bbox = ax_zoom.get_position()

fig.add_artist(
    Rectangle(
        (bbox.x0 - 0.015, bbox.y0 - 0.045),
        bbox.width + 0.045,
        bbox.height + 0.085,
        transform=fig.transFigure,
        fill=False,
        edgecolor="black",
        linewidth=0.9,
        zorder=10
    )
)


# =========================================================
# 8. 左侧连接括号与引导线
# =========================================================

# 主图左侧 bracket，标示小值区域
ax.plot(
    [-0.45, -0.45],
    [8.7, 11.3],
    transform=ax.get_yaxis_transform(),
    color="black",
    linewidth=0.9,
    clip_on=False
)

ax.plot(
    [-0.45, -0.38],
    [8.7, 8.7],
    transform=ax.get_yaxis_transform(),
    color="black",
    linewidth=0.9,
    clip_on=False
)

ax.plot(
    [-0.45, -0.38],
    [11.3, 11.3],
    transform=ax.get_yaxis_transform(),
    color="black",
    linewidth=0.9,
    clip_on=False
)

# 从 bracket 到放大图的连接线
fig.add_artist(
    Line2D(
        [0.245, bbox.x0 - 0.015],
        [0.43, bbox.y1 + 0.040],
        transform=fig.transFigure,
        color="black",
        linewidth=0.8
    )
)

fig.add_artist(
    Line2D(
        [0.245, bbox.x0 - 0.015],
        [0.29, bbox.y0 - 0.045],
        transform=fig.transFigure,
        color="black",
        linewidth=0.8
    )
)


# =========================================================
# 9. 可选：左上角子图编号
# =========================================================

fig.text(
    0.03,
    0.92,
    "b",
    fontsize=15,
    fontweight="bold",
    ha="left",
    va="top"
)


# =========================================================
# 10. 保存图片
# =========================================================

plt.savefig(
    "regional_plastic_emissions_stacked_bar_zoom.png",
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.04
)

plt.savefig(
    "regional_plastic_emissions_stacked_bar_zoom.pdf",
    bbox_inches="tight",
    pad_inches=0.04
)

plt.show()