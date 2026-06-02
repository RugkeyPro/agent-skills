import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Wedge, Arc
import matplotlib as mpl


# =========================================================
# 1. 基础设置
# =========================================================

mpl.rcParams["font.family"] = "Arial"
mpl.rcParams["axes.unicode_minus"] = False


# =========================================================
# 2. 工具函数
# =========================================================

def add_box(ax, x, y, w, h, text, fc="#d9e8f8", ec="white",
            fontsize=11, color="black", lw=1.0, zorder=3):
    """添加矩形文本框"""
    rect = Rectangle(
        (x, y), w, h,
        facecolor=fc,
        edgecolor=ec,
        linewidth=lw,
        zorder=zorder
    )
    ax.add_patch(rect)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=color,
        zorder=zorder + 1
    )
    return rect


def add_arrow(ax, x1, y1, x2, y2, color="black", lw=1.0,
              arrowstyle="-|>", mutation_scale=8, zorder=4):
    """添加箭头"""
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=arrowstyle,
        mutation_scale=mutation_scale,
        linewidth=lw,
        color=color,
        shrinkA=0,
        shrinkB=0,
        zorder=zorder
    )
    ax.add_patch(arrow)
    return arrow


def add_line(ax, x1, y1, x2, y2, color="0.3", lw=1.0, zorder=2):
    """添加普通连线"""
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw, zorder=zorder)


def add_bracket(ax, x, y1, y2, direction="right", width=0.25,
                color="#536d9c", lw=0.8):
    """添加简单括号形连接线"""
    if direction == "right":
        add_line(ax, x, y1, x + width, y1, color=color, lw=lw)
        add_line(ax, x + width, y1, x + width, y2, color=color, lw=lw)
        add_line(ax, x + width, y2, x, y2, color=color, lw=lw)
    else:
        add_line(ax, x, y1, x - width, y1, color=color, lw=lw)
        add_line(ax, x - width, y1, x - width, y2, color=color, lw=lw)
        add_line(ax, x - width, y2, x, y2, color=color, lw=lw)


# =========================================================
# 3. 颜色
# =========================================================

blue = "#6fa8dc"
green = "#a6cdbf"
light_blue = "#d8e9fb"
dark_blue = "#3e5a8a"
pink = "#f6b0a7"
mauve = "#b99aac"
grey_pink = "#e4d5d7"
purple_grey = "#8e91b3"
ring_blue = "#d6e8fb"


# =========================================================
# 4. 画布
# =========================================================

fig, ax = plt.subplots(figsize=(12.2, 6.2), dpi=300)

ax.set_xlim(0, 12)
ax.set_ylim(0, 6)
ax.axis("off")


# =========================================================
# 5. 左侧：NJU-MP 模型输入与塑料迁移过程
# =========================================================

# 顶部三类排放源
add_box(ax, 0.2, 5.0, 1.0, 0.35, "Riverine", fc=blue, fontsize=11)
add_box(ax, 1.2, 5.0, 1.0, 0.35, "Coastal", fc=blue, fontsize=11)
add_box(ax, 2.2, 5.0, 1.0, 0.35, "Ocean", fc=blue, fontsize=11)

# 汇合线
add_line(ax, 0.4, 5.0, 0.4, 4.82)
add_line(ax, 0.4, 4.82, 2.9, 4.82)
add_line(ax, 2.9, 5.0, 2.9, 4.82)
add_line(ax, 1.65, 4.82, 1.65, 4.68)

ax.text(
    1.65, 4.55,
    "Plastic emissions",
    ha="center",
    va="center",
    fontsize=11
)

add_arrow(ax, 1.65, 4.38, 1.65, 4.18, lw=0.9)

# 迁移过程模块
processes = [
    ("Sinking and rising", 3.75),
    ("Drifting", 3.25),
    ("Fragmentation/abrasion", 2.75),
    ("Beaching", 2.25),
    ("Biofouling and defouling", 1.75),
]

for label, y in processes:
    add_box(ax, 0.7, y, 1.8, 0.36, label, fc=green, fontsize=11)

# 过程模块右侧括号
add_bracket(ax, 2.5, 1.75, 3.93, direction="right", width=0.28, color="#536d9c", lw=0.8)

# Observation
add_box(ax, 2.9, 3.95, 1.4, 0.35, "Observation", fc=grey_pink, fontsize=11)
add_arrow(ax, 3.55, 3.72, 3.55, 3.25, lw=0.9)

# 模型集合估计
ax.text(
    3.55, 2.80,
    "Model ensemble\nand\noptimal\nestimation",
    ha="center",
    va="center",
    fontsize=11
)

# 过程到模型估计
add_line(ax, 2.78, 2.78, 3.15, 2.78, color="#536d9c", lw=0.8)
add_line(ax, 4.05, 2.78, 4.35, 2.78, color="#536d9c", lw=0.8)

# 左侧模型标签
ax.text(
    3.55, 1.45,
    "NJU-MP model",
    ha="center",
    va="center",
    fontsize=11,
    color="#9694bf"
)

add_arrow(ax, 3.55, 1.28, 3.55, 0.95, color="#9694bf", lw=0.9)

add_box(ax, 2.5, 0.62, 2.2, 0.34, "(1) Carbon storage", fc=light_blue, fontsize=11)


# =========================================================
# 6. 中部：耦合圆环与核心模块
# =========================================================

# 浅蓝色圆环
ring = Wedge(
    center=(7.0, 2.75),
    r=2.25,
    theta1=0,
    theta2=360,
    width=0.34,
    facecolor=ring_blue,
    edgecolor="none",
    zorder=1
)
ax.add_patch(ring)

# 圆环内部双向循环箭头，用 arc + arrowheads 表示
arc1 = Arc(
    (7.0, 2.75), 2.8, 2.8,
    theta1=35,
    theta2=145,
    color="#8e91b3",
    linewidth=1.6,
    zorder=2
)
ax.add_patch(arc1)

add_arrow(ax, 7.78, 3.95, 7.88, 3.88, color="#8e91b3", lw=1.4, mutation_scale=10)

arc2 = Arc(
    (7.0, 2.75), 2.8, 2.8,
    theta1=215,
    theta2=315,
    color="#8e91b3",
    linewidth=1.6,
    zorder=2
)
ax.add_patch(arc2)

add_arrow(ax, 7.95, 1.55, 8.05, 1.65, color="#8e91b3", lw=1.4, mutation_scale=10)

# Coupling 文本
ax.text(
    7.65, 2.70,
    "Coupling",
    ha="center",
    va="center",
    fontsize=12,
    color="#536d9c",
    zorder=4
)

# 左侧进入耦合的模型状态变量
left_core = [
    ("6 Size groups", 3.65, 1.35),
    ("5 Polymer types", 3.08, 1.60),
    ("Distributions", 2.50, 1.35),
    ("Flux", 1.93, 0.65),
]

for text, y, w in left_core:
    add_box(
        ax, 4.65, y, w, 0.35,
        text,
        fc=dark_blue,
        ec="white",
        fontsize=11,
        color="white"
    )

# 左侧大括号连接
add_bracket(ax, 4.55, 1.93, 3.65, direction="left", width=0.28, color="#536d9c", lw=0.8)
add_line(ax, 4.35, 2.78, 4.55, 2.78, color="#536d9c", lw=0.8)

# 生态系统模型模块
add_box(
    ax, 7.4, 3.65, 1.75, 0.36,
    "Marine ecosystem",
    fc=purple_grey,
    ec="white",
    fontsize=11
)

add_box(
    ax, 6.4, 1.95, 2.75, 0.36,
    "Marine biogeochemical cycle",
    fc=purple_grey,
    ec="white",
    fontsize=11
)

# 顶部实验参数
add_box(ax, 6.05, 5.55, 1.95, 0.36, "Laboratory studies", fc=pink, fontsize=11)
add_arrow(ax, 7.03, 5.48, 7.03, 5.10, lw=0.9)

ax.text(
    7.03, 4.93,
    "Growth impact parameter",
    ha="center",
    va="center",
    fontsize=11
)
add_arrow(ax, 7.03, 4.74, 7.03, 4.47, lw=0.9)

ax.text(
    7.03, 4.38,
    "(3) Growth impacts on phytoplankton",
    ha="center",
    va="center",
    fontsize=11
)

# 底部 DOC 模块
ax.text(
    7.03, 0.78,
    "(2) DOC releasing",
    ha="center",
    va="center",
    fontsize=11
)

add_arrow(ax, 7.03, 0.66, 7.03, 0.48, lw=0.9)

ax.text(
    7.03, 0.34,
    "DOC releasing rate",
    ha="center",
    va="center",
    fontsize=11
)

add_box(ax, 6.10, -0.05, 1.95, 0.36, "Laboratory studies", fc=pink, fontsize=11)


# =========================================================
# 7. 右侧：Darwin 生态系统模型外部作用
# =========================================================

# Interplay 弧线括号
arc_right1 = Arc(
    (9.55, 2.75), 1.0, 2.2,
    theta1=-65,
    theta2=65,
    color="#8e91b3",
    linewidth=1.0,
    zorder=2
)
arc_right2 = Arc(
    (10.25, 2.75), 1.0, 2.2,
    theta1=115,
    theta2=245,
    color="#8e91b3",
    linewidth=1.0,
    zorder=2
)
ax.add_patch(arc_right1)
ax.add_patch(arc_right2)

ax.text(
    9.90, 2.80,
    "Interplay",
    ha="center",
    va="center",
    fontsize=11
)

add_box(
    ax, 10.25, 3.60, 1.55, 0.52,
    "Diversity and\nbiogeography",
    fc=mauve,
    ec="white",
    fontsize=11
)

add_box(
    ax, 10.30, 2.02, 1.75, 0.34,
    "Elemental cycle",
    fc=mauve,
    ec="white",
    fontsize=11
)

# Darwin 模型标签
ax.text(
    9.95, 1.48,
    "Darwin ecosystem model",
    ha="center",
    va="center",
    fontsize=11,
    color="#c69aaa"
)


# =========================================================
# 8. 保存与显示
# =========================================================

plt.savefig(
    "nju_mp_darwin_coupling_framework.png",
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.08
)

plt.savefig(
    "nju_mp_darwin_coupling_framework.pdf",
    bbox_inches="tight",
    pad_inches=0.08
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")