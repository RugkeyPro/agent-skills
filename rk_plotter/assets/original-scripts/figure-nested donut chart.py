import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle
import numpy as np


# =========================================================
# 1. 基础数据
# =========================================================

total_mass = "0.73 Gg"

# 外环比例，单位 %
outer_data = {
    "Discharge": 96.3,
    "Residue": 2.6,
    "Degraded": 1.1,
}

# 内环比例，单位 %
inner_data = {
    "Losses": 97.4,
    "Other": 2.6,
}


# =========================================================
# 2. 颜色设置
# =========================================================

colors = {
    "outer_blue": "#5b78bf",
    "inner_blue": "#324879",
    "brown": "#7a3a16",
    "white": "#ffffff",
}


# =========================================================
# 3. 工具函数
# =========================================================

def add_wedge(ax, theta1, theta2, r, width, color,
              edgecolor="white", linewidth=1.2, zorder=2):
    """添加环形扇区"""
    wedge = Wedge(
        center=(0, 0),
        r=r,
        theta1=theta1,
        theta2=theta2,
        width=width,
        facecolor=color,
        edgecolor=edgecolor,
        linewidth=linewidth,
        zorder=zorder
    )
    ax.add_patch(wedge)
    return wedge


def pol2cart(radius, angle_deg):
    """极坐标转笛卡尔坐标"""
    angle = np.deg2rad(angle_deg)
    return radius * np.cos(angle), radius * np.sin(angle)


# =========================================================
# 4. 创建画布
# =========================================================

fig, ax = plt.subplots(figsize=(4.6, 4.2), dpi=300)
ax.set_aspect("equal")
ax.axis("off")


# =========================================================
# 5. 绘制外环
#    将两个小扇区放在右侧，便于标注
# =========================================================

outer_r = 1.00
outer_width = 0.32

# 角度换算
residue_angle = outer_data["Residue"] / 100 * 360
degraded_angle = outer_data["Degraded"] / 100 * 360

# 小扇区安排在右侧附近
residue_theta1 = 0
residue_theta2 = residue_angle

degraded_theta1 = -degraded_angle - 8
degraded_theta2 = -8

# 主体 Discharge 占据剩余大部分圆环
add_wedge(
    ax,
    theta1=residue_theta2,
    theta2=360 + degraded_theta1,
    r=outer_r,
    width=outer_width,
    color=colors["outer_blue"],
    edgecolor="white",
    linewidth=1.0
)

# Residue 小扇区
add_wedge(
    ax,
    theta1=residue_theta1,
    theta2=residue_theta2,
    r=outer_r,
    width=outer_width,
    color=colors["white"],
    edgecolor="white",
    linewidth=1.0
)

# Degraded 小扇区
add_wedge(
    ax,
    theta1=degraded_theta1,
    theta2=degraded_theta2,
    r=outer_r,
    width=outer_width,
    color=colors["inner_blue"],
    edgecolor="white",
    linewidth=1.0
)


# =========================================================
# 6. 绘制内环
# =========================================================

inner_r = 0.65
inner_width = 0.30

other_angle = inner_data["Other"] / 100 * 360

# Losses 主体
add_wedge(
    ax,
    theta1=other_angle,
    theta2=360,
    r=inner_r,
    width=inner_width,
    color=colors["inner_blue"],
    edgecolor="white",
    linewidth=1.2,
    zorder=3
)

# Other 小扇区，棕色
add_wedge(
    ax,
    theta1=0,
    theta2=other_angle,
    r=inner_r,
    width=inner_width,
    color=colors["brown"],
    edgecolor="white",
    linewidth=1.2,
    zorder=4
)


# =========================================================
# 7. 中心空白圆
# =========================================================

hole = Circle(
    (0, 0),
    radius=0.33,
    facecolor="white",
    edgecolor="white",
    linewidth=1.0,
    zorder=5
)

ax.add_patch(hole)

ax.text(
    0,
    0,
    total_mass,
    ha="center",
    va="center",
    fontsize=12,
    color="black",
    zorder=6
)


# =========================================================
# 8. 环内文字
# =========================================================

# 外环 Discharge 文本
x, y = pol2cart(0.82, 90)
ax.text(
    x,
    y,
    "Discharge\n(96.3% ± 0.9%)",
    ha="center",
    va="center",
    fontsize=10,
    color="white",
    zorder=6
)

# 内环 Losses 文本
x, y = pol2cart(0.50, 90)
ax.text(
    x,
    y,
    "Losses\n(97.4% ± 1.3%)",
    ha="center",
    va="center",
    fontsize=10,
    color="white",
    zorder=6
)


# =========================================================
# 9. 外部标注与引线
# =========================================================

# Residue 标注
residue_mid = (residue_theta1 + residue_theta2) / 2
x0, y0 = pol2cart(0.86, residue_mid)
x1, y1 = 1.28, 0.62

ax.plot(
    [x0, x1],
    [y0, y1],
    color="black",
    linewidth=0.8
)

ax.text(
    x1,
    y1,
    "Residue\n(2.6% ± 0.9%)",
    ha="center",
    va="center",
    fontsize=10
)

# Degraded 标注
degraded_mid = (degraded_theta1 + degraded_theta2) / 2
x0, y0 = pol2cart(0.86, degraded_mid)
x1, y1 = 1.34, -0.25

ax.plot(
    [x0, x1],
    [y0, y1],
    color="black",
    linewidth=0.8
)

ax.text(
    x1 + 0.02,
    y1 - 0.02,
    "Degraded\n(1.1% ± 0.4%)",
    ha="left",
    va="center",
    fontsize=10
)

# 小白点，强调内环小扇区
dot_x, dot_y = pol2cart(0.52, other_angle / 2)
ax.scatter(
    dot_x,
    dot_y,
    s=40,
    facecolor="white",
    edgecolor="white",
    zorder=7
)


# =========================================================
# 10. 显示范围
# =========================================================

ax.set_xlim(-1.15, 1.55)
ax.set_ylim(-1.08, 1.10)


# =========================================================
# 11. 保存图片
# =========================================================

plt.savefig(
    "mass_fate_nested_donut_chart.png",
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.04
)

plt.savefig(
    "mass_fate_nested_donut_chart.pdf",
    bbox_inches="tight",
    pad_inches=0.04
)

plt.show()