import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


# =========================================================
# 1. 基础数据
# =========================================================

categories = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%"]
N = len(categories)

# 这些数值可理解为误差指标（例如 MAE / RMSE），越小越好
# 为了更接近原图，STIMP 整体最优（数值较小）
data_raw = {
    "STIMP":        [0.035, 0.040, 0.045, 0.050, 0.060, 0.075, 0.090, 0.110, 0.140],
    "DINEOF":       [0.110, 0.130, 0.150, 0.170, 0.190, 0.220, 0.260, 0.300, 0.340],
    "CSDI":         [0.120, 0.135, 0.155, 0.175, 0.195, 0.220, 0.245, 0.280, 0.320],
    "ImputeFormer": [0.090, 0.110, 0.135, 0.165, 0.190, 0.220, 0.250, 0.280, 0.310],
    "Inpainter":    [0.105, 0.135, 0.165, 0.195, 0.220, 0.245, 0.270, 0.305, 0.350],
    "Lin-ITP":      [0.130, 0.150, 0.175, 0.195, 0.220, 0.245, 0.270, 0.295, 0.325],
    "MaskedAE":     [0.060, 0.080, 0.100, 0.125, 0.150, 0.180, 0.220, 0.270, 0.330],
    "Slide Window": [0.125, 0.145, 0.170, 0.190, 0.215, 0.235, 0.255, 0.285, 0.315],
    "TRMF":         [0.155, 0.185, 0.210, 0.230, 0.245, 0.265, 0.285, 0.320, 0.365],
}

# 颜色尽量贴近原图
colors = {
    "STIMP":        "#ff1e14",
    "DINEOF":       "#9c6a5d",
    "CSDI":         "#00b52d",
    "ImputeFormer": "#ffd200",
    "Inpainter":    "#1786c9",
    "Lin-ITP":      "#a56cc1",
    "MaskedAE":     "#ff8a00",
    "Slide Window": "#ff7ac8",
    "TRMF":         "#3b0000",
}


# =========================================================
# 2. 反向半径映射
#    原图表现为：数值越小越靠外，数值越大越靠内
# =========================================================

vmin = 0.04   # 外圈显示值
vmax = 0.50   # 内圈显示值

def reverse_scale(values, vmin=0.04, vmax=0.50):
    """
    将原始数值映射到雷达图半径：
    小值 -> 大半径（靠外）
    大值 -> 小半径（靠内）
    最终半径范围控制在 [0, 1]
    """
    values = np.asarray(values)
    r = (vmax - values) / (vmax - vmin)
    return np.clip(r, 0, 1)


# =========================================================
# 3. 雷达图角度
# =========================================================

angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]   # 闭合


# =========================================================
# 4. 创建画布
# =========================================================

fig = plt.figure(figsize=(8.0, 5.2), dpi=300)
ax = plt.subplot(111, polar=True)

# 从正上方开始，顺时针
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)


# =========================================================
# 5. 设置角度轴标签
# =========================================================

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=12)


# =========================================================
# 6. 设置径向刻度
#    显示的是原始值标签，但位置是反向后的半径
# =========================================================

tick_values = [0.50, 0.20, 0.10, 0.04]
tick_positions = reverse_scale(tick_values, vmin, vmax)

ax.set_yticks(tick_positions)
ax.set_yticklabels([f"{v:.2f}" for v in tick_values], fontsize=9)
ax.set_rlabel_position(100)  # 将径向标签放到右侧偏上的位置
ax.set_ylim(0, 1.05)

# 网格与边框
ax.grid(color="0.85", linewidth=1.0)
ax.spines["polar"].set_color("0.88")
ax.spines["polar"].set_linewidth(1.0)


# =========================================================
# 7. 绘制各方法雷达线
# =========================================================

for method, values in data_raw.items():
    r = reverse_scale(values, vmin, vmax).tolist()
    r += r[:1]

    ax.plot(
        angles,
        r,
        color=colors[method],
        linewidth=1.6,
        marker="o",
        markersize=2.5,
        label=method
    )

    # 原图里 STIMP 有淡淡填充，可只给 STIMP 填充
    if method == "STIMP":
        ax.fill(
            angles,
            r,
            color=colors[method],
            alpha=0.05
        )


# =========================================================
# 8. 图例
# =========================================================

legend_handles = [
    Line2D(
        [0], [0],
        color=colors[m],
        marker="o",
        linewidth=4,
        markersize=8,
        label=m
    )
    for m in data_raw.keys()
]

legend = ax.legend(
    handles=legend_handles,
    loc="center left",
    bbox_to_anchor=(1.05, 0.50),
    frameon=True,
    fontsize=11,
    borderpad=0.6,
    labelspacing=0.55,
    handlelength=1.8
)

for text in legend.get_texts():
    text.set_fontweight("bold")

legend.get_frame().set_edgecolor("0.85")
legend.get_frame().set_linewidth(1.0)
legend.get_frame().set_facecolor("white")


# =========================================================
# 9. 底部区域名称
# =========================================================

fig.text(
    0.10,
    0.06,
    "Yangtze River Estuary",
    ha="left",
    va="center",
    fontsize=22,
    fontweight="bold"
)


# =========================================================
# 10. 调整布局并保存
# =========================================================

plt.subplots_adjust(left=0.06, right=0.72, bottom=0.16, top=0.94)

plt.savefig(
    "radar_chart_yangtze_river_estuary.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "radar_chart_yangtze_river_estuary.pdf",
    bbox_inches="tight"
)

plt.show()