import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


# =========================================================
# 1. 构造随机示例数据
# =========================================================

np.random.seed(42)

n = 45000

# Habitat hotspot value
# 大量点集中在 0 附近，少量点延伸到 1，模拟原图左侧高密度结构
x_main = np.random.beta(a=0.55, b=5.5, size=int(n * 0.85))
x_tail = np.random.beta(a=1.4, b=3.8, size=int(n * 0.15))
x = np.concatenate([x_main, x_tail])

# Climate change magnitude
# 构造一个随 x 增大而逐渐收窄的楔形分布
upper = 1.00 - 0.28 * np.sqrt(x)
lower = 0.02 + 0.55 * np.sqrt(x)

# 在上下边界之间随机取值，略偏向中高值
r = np.random.beta(a=3.2, b=2.2, size=x.size)
y = lower + (upper - lower) * r

# 增加左侧近 0 值的竖向扩散，使图形更接近示例
left_mask = x < 0.035
y[left_mask] = np.random.beta(a=1.4, b=1.7, size=left_mask.sum())

# 加入少量噪声
y += np.random.normal(0, 0.035, size=y.size)

# 限制范围
x = np.clip(x, 0, 1)
y = np.clip(y, 0, 1)


# =========================================================
# 2. 计算二维核密度
# =========================================================

xy = np.vstack([x, y])
density = gaussian_kde(xy, bw_method=0.08)(xy)

# 为了让高密度点画在上层，按 density 排序
idx = density.argsort()
x = x[idx]
y = y[idx]
density = density[idx]


# =========================================================
# 3. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(4.2, 3.3), dpi=300)

sc = ax.scatter(
    x,
    y,
    c=density,
    s=1.0,
    cmap="viridis",
    edgecolors="none",
    alpha=0.95
)


# =========================================================
# 4. 坐标轴设置
# =========================================================

ax.set_xlim(-0.04, 1.05)
ax.set_ylim(-0.05, 1.05)

ax.set_xlabel(
    "Habitat hotspot value",
    fontsize=16,
    labelpad=10
)

ax.set_ylabel(
    "Climate change magnitude",
    fontsize=16,
    labelpad=6
)

ax.set_xticks([0, 0.25, 0.50, 0.75, 1.00])
ax.set_xticklabels(["0", "0.25", "0.50", "0.75", "1.00"], fontsize=12)

ax.set_yticks([0, 0.25, 0.50, 0.75, 1.00])
ax.set_yticklabels(["0", "0.25", "0.50", "0.75", "1.00"], fontsize=12)

ax.grid(
    True,
    color="0.90",
    linewidth=0.7,
    alpha=0.7
)

for spine in ax.spines.values():
    spine.set_linewidth(0.8)

ax.tick_params(
    axis="both",
    direction="out",
    length=4,
    width=0.8
)


# =========================================================
# 5. 嵌入式密度图例
# =========================================================

# 在主图右下角放一个横向 colorbar
cax = inset_axes(
    ax,
    width="47%",
    height="9%",
    loc="lower right",
    bbox_to_anchor=(-0.06, 0.13, 1, 1),
    bbox_transform=ax.transAxes,
    borderpad=0
)

cbar = plt.colorbar(
    sc,
    cax=cax,
    orientation="horizontal"
)

# 去掉数值刻度，只保留 Low / High
cbar.set_ticks([])
cbar.outline.set_linewidth(0.5)

# 图例标题和两端文字
cax.set_title(
    "Density",
    fontsize=13,
    pad=6
)

cax.text(
    0.0,
    -0.65,
    "Low",
    transform=cax.transAxes,
    ha="center",
    va="center",
    fontsize=12
)

cax.text(
    1.0,
    -0.65,
    "High",
    transform=cax.transAxes,
    ha="center",
    va="center",
    fontsize=12
)


# =========================================================
# 6. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "density_scatter_hotspot_climate.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "density_scatter_hotspot_climate.pdf",
    bbox_inches="tight"
)

plt.show()