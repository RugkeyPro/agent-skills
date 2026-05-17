import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde, pearsonr
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D


# =========================================================
# 1. 构造示例数据
# =========================================================

np.random.seed(42)

n = 900

# truth：构造一个多峰分布，模拟真实 Chl_a 标准化值
truth_1 = np.random.normal(-0.75, 0.22, int(n * 0.45))
truth_2 = np.random.normal(0.10, 0.35, int(n * 0.40))
truth_3 = np.random.normal(0.60, 0.22, int(n * 0.15))
truth = np.concatenate([truth_1, truth_2, truth_3])

# STIMP：与 truth 高相关，误差较小
imputed_stimp = truth * 0.92 + np.random.normal(0, 0.16, truth.size)

# DINEOF：与 truth 相关性较弱，误差更大，并存在一定偏差
imputed_dineof = truth * 0.68 + np.random.normal(0, 0.28, truth.size) - 0.08

# 限制范围，贴近示例图
truth = np.clip(truth, -1.5, 2.0)
imputed_stimp = np.clip(imputed_stimp, -1.5, 2.1)
imputed_dineof = np.clip(imputed_dineof, -1.5, 2.1)


# =========================================================
# 2. 统计指标
# =========================================================

pcc_stimp, p_stimp = pearsonr(truth, imputed_stimp)
pcc_dineof, p_dineof = pearsonr(truth, imputed_dineof)


# =========================================================
# 3. 工具函数：二维 KDE 等高线
# =========================================================

def draw_kde_contour(ax, x, y, color, levels=9, linewidth=1.5):
    """
    在主图中绘制二维核密度等高线
    """
    values = np.vstack([x, y])
    kde = gaussian_kde(values)

    xmin, xmax = -1.5, 2.1
    ymin, ymax = -1.6, 2.1

    xx, yy = np.meshgrid(
        np.linspace(xmin, xmax, 180),
        np.linspace(ymin, ymax, 180)
    )

    zz = kde(np.vstack([xx.ravel(), yy.ravel()])).reshape(xx.shape)

    # 避免最低层过于贴边
    zmin = np.percentile(zz, 65)
    zmax = zz.max()
    contour_levels = np.linspace(zmin, zmax, levels)

    ax.contour(
        xx,
        yy,
        zz,
        levels=contour_levels,
        colors=color,
        linewidths=linewidth,
        alpha=0.9
    )


def draw_marginal_kde(ax, values, color, orientation="x"):
    """
    绘制边缘 KDE 密度图
    orientation='x' 用于顶部；
    orientation='y' 用于右侧。
    """
    grid = np.linspace(-1.5, 2.1, 300)
    kde = gaussian_kde(values)
    density = kde(grid)

    # 归一化，便于控制视觉比例
    density = density / density.max()

    if orientation == "x":
        ax.plot(grid, density, color=color, linewidth=1.5)
        ax.fill_between(grid, 0, density, color=color, alpha=0.25)
    else:
        ax.plot(density, grid, color=color, linewidth=1.5)
        ax.fill_betweenx(grid, 0, density, color=color, alpha=0.25)


# =========================================================
# 4. 创建联合分布布局
# =========================================================

fig = plt.figure(figsize=(6.0, 6.4), dpi=300)

gs = GridSpec(
    nrows=2,
    ncols=2,
    width_ratios=[5.0, 1.0],
    height_ratios=[1.0, 5.0],
    hspace=0.03,
    wspace=0.03
)

ax_top = fig.add_subplot(gs[0, 0])
ax_main = fig.add_subplot(gs[1, 0])
ax_right = fig.add_subplot(gs[1, 1], sharey=ax_main)


# =========================================================
# 5. 主图：二维 KDE 等高线
# =========================================================

# 1:1 线
ax_main.plot(
    [-1.5, 2.1],
    [-1.5, 2.1],
    color="0.25",
    linewidth=1.8,
    zorder=1
)

# 两种方法的 KDE 等高线
draw_kde_contour(
    ax_main,
    truth,
    imputed_stimp,
    color="#e41a1c",
    levels=10,
    linewidth=1.6
)

draw_kde_contour(
    ax_main,
    truth,
    imputed_dineof,
    color="#377eb8",
    levels=10,
    linewidth=1.6
)


# =========================================================
# 6. 边缘密度
# =========================================================

# 顶部：truth 的边缘分布
draw_marginal_kde(
    ax_top,
    truth,
    color="#e41a1c",
    orientation="x"
)

# 右侧：imputed 的边缘分布
draw_marginal_kde(
    ax_right,
    imputed_stimp,
    color="#e41a1c",
    orientation="y"
)

draw_marginal_kde(
    ax_right,
    imputed_dineof,
    color="#377eb8",
    orientation="y"
)


# =========================================================
# 7. 主图坐标轴设置
# =========================================================

ax_main.set_xlim(-1.5, 2.1)
ax_main.set_ylim(-1.6, 2.1)

ax_main.set_xlabel(
    "truth",
    fontsize=30,
    labelpad=4
)

ax_main.set_ylabel(
    "imputed",
    fontsize=30,
    labelpad=8
)

ax_main.set_xticks([-1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5, 2.0])
ax_main.set_yticks([-1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5, 2.0])

ax_main.tick_params(
    axis="both",
    labelsize=18,
    direction="out",
    length=4,
    width=1.0
)

for spine in ax_main.spines.values():
    spine.set_linewidth(1.2)
    spine.set_color("0.55")


# =========================================================
# 8. 顶部和右侧边缘图样式
# =========================================================

ax_top.set_xlim(ax_main.get_xlim())
ax_top.set_ylim(0, 1.08)
ax_top.axis("off")

ax_right.set_xlim(0, 1.08)
ax_right.set_ylim(ax_main.get_ylim())
ax_right.axis("off")


# =========================================================
# 9. 图例和 PCC 标注
# =========================================================

legend_handles = [
    Line2D([0], [0], color="#e41a1c", lw=2.0, label="STIMP"),
    Line2D([0], [0], color="#377eb8", lw=2.0, label="DINEOF"),
]

legend = ax_main.legend(
    handles=legend_handles,
    title="method",
    loc="upper left",
    frameon=True,
    fontsize=12,
    title_fontsize=12,
    borderpad=0.5,
    handlelength=1.8
)

legend.get_frame().set_edgecolor("0.85")
legend.get_frame().set_linewidth(1.0)
legend.get_frame().set_facecolor("white")


# PCC 文本
ax_main.text(
    0.29,
    0.91,
    f"PCC={pcc_stimp:.4f} pvalue={p_stimp:.2f}",
    transform=ax_main.transAxes,
    color="#e41a1c",
    fontsize=14,
    fontweight="bold",
    ha="left",
    va="center"
)

ax_main.text(
    0.29,
    0.86,
    f"PCC={pcc_dineof:.4f} pvalue={p_dineof:.2f}",
    transform=ax_main.transAxes,
    color="#377eb8",
    fontsize=14,
    fontweight="bold",
    ha="left",
    va="center"
)


# =========================================================
# 10. 底部缺失率标题
# =========================================================

fig.text(
    0.50,
    0.035,
    "missing rate 0.7",
    ha="center",
    va="center",
    fontsize=26,
    fontweight="bold"
)


# =========================================================
# 11. 保存图片
# =========================================================

plt.subplots_adjust(
    left=0.16,
    right=0.93,
    bottom=0.12,
    top=0.96
)

plt.savefig(
    "joint_kde_truth_imputed_missing_rate_07.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "joint_kde_truth_imputed_missing_rate_07.pdf",
    bbox_inches="tight"
)

plt.show()