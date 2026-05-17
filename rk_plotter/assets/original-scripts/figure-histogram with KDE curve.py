import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


# =========================================================
# 1. 构造示例数据
# =========================================================

np.random.seed(42)

# 模拟“prediction uncertainty (95% CI width)”数据
# 采用右偏分布，形状接近原图
n = 2500
uncertainty = np.random.lognormal(mean=0.7, sigma=0.38, size=n)

# 限制范围，模拟极少数高值尾部
uncertainty = np.clip(uncertainty, 1.2, 10.0)


# =========================================================
# 2. 直方图参数
# =========================================================

bins = np.linspace(1.2, 10.0, 55)

# 用百分比而不是频数
weights = np.ones_like(uncertainty) * 100 / len(uncertainty)


# =========================================================
# 3. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(6.0, 2.7), dpi=300)

# 直方图
ax.hist(
    uncertainty,
    bins=bins,
    weights=weights,
    color="#7b7fe0",
    edgecolor="white",
    linewidth=0.5,
    alpha=0.85,
    zorder=2
)

# KDE 曲线
x_grid = np.linspace(1.2, 10.0, 500)
kde = gaussian_kde(uncertainty, bw_method=0.22)
bin_width = bins[1] - bins[0]

# 将密度转换成“百分比高度”，便于和直方图统一
y_kde = kde(x_grid) * 100 * bin_width

ax.plot(
    x_grid,
    y_kde,
    color="blue",
    linewidth=1.2,
    zorder=3
)


# =========================================================
# 4. 坐标轴样式
# =========================================================

ax.set_xlabel(
    "prediction uncertainty (95% CI width)",
    fontsize=14
)

ax.set_ylabel(
    "fraction of chemicals [%]",
    fontsize=14
)

ax.set_xlim(0.8, 10.3)
ax.set_ylim(0, 10.5)

ax.set_xticks([2, 4, 6, 8, 10])
ax.set_yticks([0, 2, 4, 6, 8, 10])

ax.tick_params(
    axis="both",
    direction="out",
    length=6,
    width=1.2,
    labelsize=13,
    pad=8
)

# 浅灰网格，贴近原图风格
ax.grid(
    True,
    color="0.85",
    linewidth=0.8,
    alpha=0.7
)

ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_linewidth(1.0)
    spine.set_color("0.35")


# =========================================================
# 5. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "prediction_uncertainty_histogram_kde.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "prediction_uncertainty_histogram_kde.pdf",
    bbox_inches="tight"
)

plt.show()