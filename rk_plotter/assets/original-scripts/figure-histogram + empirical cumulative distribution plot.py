import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# 1. 构造示例数据
# =========================================================

np.random.seed(42)

# standardized: 样本量较大，均值较低，分布更集中
n_standardized = 1778
standardized = np.random.lognormal(
    mean=np.log(3.10) - 0.5 * 0.22**2,
    sigma=0.22,
    size=n_standardized
)

# non-standardized: 样本量较小，均值较高，右尾更长
n_nonstandardized = 257
nonstandardized = np.random.lognormal(
    mean=np.log(3.725) - 0.5 * 0.28**2,
    sigma=0.28,
    size=n_nonstandardized
)

# 限制极端值，使图形范围接近示例
standardized = np.clip(standardized, 1.4, 8.3)
nonstandardized = np.clip(nonstandardized, 1.6, 8.3)

mean_standardized = standardized.mean()
mean_nonstandardized = nonstandardized.mean()


# =========================================================
# 2. 直方图参数
# =========================================================

bins = np.linspace(1.5, 8.5, 65)

# 将频数转换为百分比
weights_standardized = np.ones_like(standardized) * 100 / len(standardized)
weights_nonstandardized = np.ones_like(nonstandardized) * 100 / len(nonstandardized)


# =========================================================
# 3. 计算经验累积分布函数 ECDF
# =========================================================

def ecdf(values):
    values = np.sort(values)
    cumulative = np.arange(1, len(values) + 1) / len(values) * 100
    return values, cumulative


x_std, y_std = ecdf(standardized)
x_non, y_non = ecdf(nonstandardized)


# =========================================================
# 4. 绘图
# =========================================================

fig, ax1 = plt.subplots(figsize=(6.2, 3.7), dpi=300)

# 左轴：直方图
ax1.hist(
    standardized,
    bins=bins,
    weights=weights_standardized,
    color="#8fb9ff",
    edgecolor="white",
    linewidth=0.4,
    alpha=0.75,
    label="standardized",
    zorder=2
)

ax1.hist(
    nonstandardized,
    bins=bins,
    weights=weights_nonstandardized,
    color="#1d27ff",
    edgecolor="white",
    linewidth=0.4,
    alpha=0.65,
    label="non-standardized",
    zorder=3
)

ax1.set_xlabel(
    "prediction uncertainty (95% CI width)",
    fontsize=12
)

ax1.set_ylabel(
    "Fraction of chemicals [%]",
    fontsize=12
)

ax1.set_xlim(1.0, 8.7)
ax1.set_ylim(0, 20.5)

ax1.set_xticks([2, 3, 4, 5, 6, 7, 8])
ax1.set_yticks([0, 5, 10, 15, 20])

ax1.tick_params(
    axis="both",
    direction="out",
    length=6,
    width=1.4,
    labelsize=11
)

# 浅灰网格
ax1.grid(
    True,
    color="0.78",
    linewidth=0.8,
    alpha=0.9
)

ax1.set_axisbelow(True)


# =========================================================
# 5. 右轴：累积分布曲线
# =========================================================

ax2 = ax1.twinx()

ax2.plot(
    x_non,
    y_non,
    color="#001eff",
    linewidth=2.0,
    zorder=5
)

ax2.plot(
    x_std,
    y_std,
    color="#669cff",
    linewidth=2.0,
    zorder=4
)

ax2.set_ylim(0, 100)
ax2.set_yticks([0, 20, 40, 60, 80, 100])

ax2.set_ylabel(
    "Cumulative fraction [%]",
    fontsize=12
)

ax2.tick_params(
    axis="y",
    direction="out",
    length=6,
    width=1.4,
    labelsize=11
)


# =========================================================
# 6. 右上角文字标注
# =========================================================

ax1.text(
    0.95,
    0.96,
    f"non-standardized\nmean: {mean_nonstandardized:.3f}\nn={n_nonstandardized}",
    transform=ax1.transAxes,
    ha="right",
    va="top",
    fontsize=11,
    color="#001eff",
    family="monospace"
)

ax1.text(
    0.95,
    0.70,
    f"standardized\nmean: {mean_standardized:.3f}\nn={n_standardized:,}",
    transform=ax1.transAxes,
    ha="right",
    va="top",
    fontsize=11,
    color="#669cff",
    family="monospace"
)


# =========================================================
# 7. 边框样式
# =========================================================

for spine in ax1.spines.values():
    spine.set_linewidth(1.2)

for spine in ax2.spines.values():
    spine.set_linewidth(1.2)


# =========================================================
# 8. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "prediction_uncertainty_hist_cdf.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "prediction_uncertainty_hist_cdf.pdf",
    bbox_inches="tight"
)

plt.show()