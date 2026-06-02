import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.patches import Patch


# =========================================================
# 1. 构造示例数据
# =========================================================

np.random.seed(42)

# Drawdown zone ratio 范围为 0–1
# Natural lakes：更集中在较低比例区间
natural_lakes = np.random.beta(a=2.2, b=12.0, size=3000)

# Reservoirs：分布更宽，右尾更长
reservoirs = np.random.beta(a=2.0, b=7.0, size=3000)

natural_lakes = np.clip(natural_lakes, 0, 1)
reservoirs = np.clip(reservoirs, 0, 1)


# =========================================================
# 2. KDE 密度估计
# =========================================================

x_grid = np.linspace(0, 1, 500)

kde_lake = gaussian_kde(natural_lakes, bw_method=0.22)
kde_reservoir = gaussian_kde(reservoirs, bw_method=0.25)

density_lake = kde_lake(x_grid)
density_reservoir = kde_reservoir(x_grid)

# 转换为百分比频率显示
# 这里乘以 bin_width，使曲线高度接近直方图百分比含义
bin_width = 0.05
freq_lake = density_lake * 100 * bin_width
freq_reservoir = density_reservoir * 100 * bin_width


# =========================================================
# 3. 颜色设置
# =========================================================

lake_line = "red"
lake_fill = "#f4b6b6"

reservoir_line = "#2c6f9e"
reservoir_fill = "#9bb6c7"


# =========================================================
# 4. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(4.4, 3.1), dpi=300)

# Natural lakes
ax.fill_between(
    x_grid,
    freq_lake,
    0,
    color=lake_fill,
    alpha=0.55,
    edgecolor=lake_line,
    linewidth=0.8,
    zorder=2
)

ax.plot(
    x_grid,
    freq_lake,
    color=lake_line,
    linewidth=1.2,
    zorder=3
)

# Reservoirs
ax.fill_between(
    x_grid,
    freq_reservoir,
    0,
    color=reservoir_fill,
    alpha=0.65,
    edgecolor=reservoir_line,
    linewidth=0.8,
    zorder=1
)

ax.plot(
    x_grid,
    freq_reservoir,
    color=reservoir_line,
    linewidth=1.2,
    zorder=2
)


# =========================================================
# 5. 坐标轴设置
# =========================================================

ax.set_xlim(0, 1.0)
ax.set_ylim(0, 25)

ax.set_xlabel(
    "Drawdown zone ratio",
    fontsize=13,
    fontweight="bold",
    family="serif"
)

ax.set_ylabel(
    "Frequency",
    fontsize=13,
    fontweight="bold",
    family="serif"
)

ax.set_title(
    "Percentage (%)",
    fontsize=13,
    fontweight="bold",
    family="serif",
    pad=8
)

ax.set_xticks(np.arange(0, 1.01, 0.2))
ax.set_xticklabels(
    [f"{v:.1f}" for v in np.arange(0, 1.01, 0.2)],
    fontsize=10,
    family="serif"
)

ax.set_yticks([0, 5, 10, 15, 20, 25])
ax.set_yticklabels(
    ["0%", "5%", "10%", "15%", "20%", "25%"],
    fontsize=10,
    family="serif"
)

ax.tick_params(
    axis="both",
    direction="out",
    length=4,
    width=1.0
)

for spine in ax.spines.values():
    spine.set_linewidth(1.0)
    spine.set_color("black")

ax.grid(False)


# =========================================================
# 6. 图例
# =========================================================

legend_handles = [
    Patch(
        facecolor=lake_fill,
        edgecolor=lake_line,
        linewidth=1.0,
        label="Natural lakes"
    ),
    Patch(
        facecolor=reservoir_fill,
        edgecolor=reservoir_line,
        linewidth=1.0,
        label="Reservoirs"
    )
]

ax.legend(
    handles=legend_handles,
    loc="upper right",
    bbox_to_anchor=(0.96, 0.88),
    frameon=False,
    fontsize=9,
    handlelength=1.6,
    handleheight=1.1,
    handletextpad=0.45,
    labelspacing=0.6,
    prop={"family": "serif", "weight": "bold", "size": 8}
)


# =========================================================
# 7. 可选子图编号
# =========================================================

# 如果需要右上角 e 和右下角 f，可取消注释
# ax.text(
#     0.93, 1.02,
#     "e",
#     transform=ax.transAxes,
#     fontsize=16,
#     fontweight="bold",
#     family="serif"
# )
#
# ax.text(
#     0.93, -0.14,
#     "f",
#     transform=ax.transAxes,
#     fontsize=16,
#     fontweight="bold",
#     family="serif"
# )


# =========================================================
# 8. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "drawdown_zone_ratio_kde_lakes_reservoirs.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "drawdown_zone_ratio_kde_lakes_reservoirs.pdf",
    bbox_inches="tight"
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")