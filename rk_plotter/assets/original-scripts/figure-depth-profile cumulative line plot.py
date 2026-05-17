import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


# =========================================================
# 1. 构造示例数据
# =========================================================

# 水深，单位 m
# 使用对数间隔，让浅水层变化更明显
depth = np.array([
    10, 15, 20, 30, 50, 75, 100,
    150, 200, 300, 500, 800, 1000,
    1500, 2000, 3000, 5000
])

# 不同塑料类型在不同深度处的累积沉积质量，单位 Tg
# 数据为模拟值，整体形态参考原图
PE = np.array([
    0.000, 0.002, 0.004, 0.007, 0.012, 0.018, 0.023,
    0.030, 0.035, 0.038, 0.041, 0.042, 0.043,
    0.043, 0.043, 0.043, 0.043
])

PP = np.array([
    0.000, 0.001, 0.003, 0.005, 0.010, 0.016, 0.022,
    0.027, 0.031, 0.035, 0.037, 0.038, 0.039,
    0.039, 0.039, 0.039, 0.039
])

PVC = np.array([
    0.000, 0.003, 0.006, 0.011, 0.020, 0.030, 0.038,
    0.044, 0.047, 0.050, 0.053, 0.055, 0.056,
    0.056, 0.056, 0.056, 0.056
])

PS = np.array([
    0.000, 0.001, 0.002, 0.004, 0.008, 0.013, 0.018,
    0.022, 0.026, 0.030, 0.033, 0.034, 0.035,
    0.035, 0.035, 0.035, 0.035
])

ABS = np.array([
    0.000, 0.0005, 0.001, 0.002, 0.004, 0.007, 0.010,
    0.013, 0.015, 0.016, 0.017, 0.017,
    0.017, 0.017, 0.017, 0.017, 0.017
])

# Total 可以由各类型相加，也可以替换成你的真实总量
total = PE + PP + PVC + PS + ABS


# =========================================================
# 2. 颜色设置
# =========================================================

colors = {
    "Total": "black",
    "PE": "#7cb342",
    "PP": "#f39c12",
    "PVC": "#f28e55",
    "PS": "#bdbdbd",
    "ABS": "#5dade2",
}


# =========================================================
# 3. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(4.2, 3.0), dpi=300)

# 横轴为质量，纵轴为深度
ax.plot(total, depth, color=colors["Total"], linewidth=1.1, label="Total")
ax.plot(PE, depth, color=colors["PE"], linewidth=1.0, label="PE")
ax.plot(PP, depth, color=colors["PP"], linewidth=1.0, label="PP")
ax.plot(PVC, depth, color=colors["PVC"], linewidth=1.0, label="PVC")
ax.plot(PS, depth, color=colors["PS"], linewidth=1.0, label="PS")
ax.plot(ABS, depth, color=colors["ABS"], linewidth=1.0, label="ABS")


# =========================================================
# 4. 坐标轴设置
# =========================================================

ax.set_xlim(0, 0.20)

ax.set_xlabel(
    "Mass (Tg)",
    fontsize=11
)

# 深度轴：对数坐标，并让深度向下增加
ax.set_yscale("log")
ax.set_ylim(5000, 10)

# y 轴放到右侧
ax.yaxis.tick_right()
ax.yaxis.set_label_position("right")

ax.set_ylabel(
    "Depth (m)",
    fontsize=11,
    rotation=270,
    labelpad=14
)

# x 轴刻度
ax.set_xticks([0, 0.05, 0.10, 0.15, 0.20])
ax.set_xticklabels(["0", "0.05", "0.10", "0.15", "0.20"], fontsize=10)

# y 轴刻度
ax.set_yticks([10, 100, 1000, 5000])
ax.set_yticklabels(["10", "100", "1,000", "5,000"], fontsize=10)

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
# 5. 图内标题
# =========================================================

ax.text(
    0.115,
    13,
    "Cumulative sediment plastic mass",
    ha="center",
    va="top",
    fontsize=11
)


# =========================================================
# 6. 图例
# =========================================================

ax.legend(
    loc="upper right",
    frameon=False,
    fontsize=9,
    handlelength=1.2,
    handletextpad=0.4,
    borderpad=0.2,
    labelspacing=0.25
)


# =========================================================
# 7. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "cumulative_sediment_plastic_mass_depth_profile.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "cumulative_sediment_plastic_mass_depth_profile.pdf",
    bbox_inches="tight"
)

plt.show()