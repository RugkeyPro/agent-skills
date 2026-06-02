import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


# =========================================================
# 1. 随机生成 PCA 空间中的样点数据
# =========================================================

np.random.seed(42)

# 主体点云：模拟未占据栖息地在 PCA 空间中的分布
n1 = 9000
x1 = np.random.normal(loc=0.2, scale=1.45, size=n1)
y1 = np.random.normal(loc=-0.7, scale=1.05, size=n1)

# 扩散点云：模拟外围环境空间
n2 = 3500
x2 = np.random.normal(loc=1.2, scale=2.3, size=n2)
y2 = np.random.normal(loc=-0.1, scale=1.8, size=n2)

# 少量离散点
n3 = 700
x3 = np.random.uniform(-6, 8, n3)
y3 = np.random.normal(loc=0.5, scale=2.2, size=n3)

x = np.concatenate([x1, x2, x3])
y = np.concatenate([y1, y2, y3])

# 限制绘图范围
mask = (x >= -6.2) & (x <= 8.2) & (y >= -6.2) & (y <= 7.5)
x = x[mask]
y = y[mask]


# =========================================================
# 2. 计算二维核密度，用颜色表示点密度
# =========================================================

xy = np.vstack([x, y])
density = gaussian_kde(xy)(xy)

# 为了让高密度点显示在上方，按密度排序
idx = density.argsort()
x = x[idx]
y = y[idx]
density = density[idx]


# =========================================================
# 3. 设置环境变量箭头
#    这些箭头相当于 PCA biplot 中的变量载荷
# =========================================================

vectors = {
    "PTC":  (-4.9,  0.4),
    "AI":   (-4.3,  1.3),
    "DD":   (-3.3,  1.5),
    "NDVI": (-3.9, -0.3),
    "BIO12":(-5.3, -2.2),
    "BIO1": (-2.1, -5.5),
    "SP":   (-0.3,  6.2),
    "ELE":  (1.8,  6.2),
    "BIO2": (4.2,  0.8),
    "BIO15":(2.8, -1.9),
    "HFI":  (0.0, -3.5),
}


# =========================================================
# 4. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(4.2, 4.1), dpi=300)

# 背景灰色散点，增强真实点云感
ax.scatter(
    x,
    y,
    s=1.2,
    c="0.55",
    alpha=0.18,
    linewidths=0,
    zorder=1
)

# 根据核密度着色的散点
# YlGnBu：低密度偏黄，高密度偏蓝，接近示例图效果
sc = ax.scatter(
    x,
    y,
    c=density,
    s=2.0,
    cmap="YlGnBu",
    alpha=0.75,
    linewidths=0,
    zorder=2
)

# 环境变量箭头
for name, (vx, vy) in vectors.items():
    ax.annotate(
        "",
        xy=(vx, vy),
        xytext=(0, 0),
        arrowprops=dict(
            arrowstyle="-",
            color="red",
            linewidth=1.1,
            shrinkA=0,
            shrinkB=0
        ),
        zorder=4
    )

    # 标签位置略微外移
    label_x = vx * 1.03
    label_y = vy * 1.03

    ax.text(
        label_x,
        label_y,
        name,
        fontsize=12,
        color="black",
        ha="center",
        va="center",
        zorder=5
    )


# =========================================================
# 5. 坐标轴、网格和标题设置
# =========================================================

ax.set_title(
    "Unoccupied habitats",
    fontsize=13,
    pad=6
)

ax.set_xlabel(
    "PC1 (43.6%)",
    fontsize=13
)

ax.set_ylabel(
    "PC2 (21.6%)",
    fontsize=13
)

ax.set_xlim(-6.3, 8.2)
ax.set_ylim(-6.3, 7.5)

ax.set_xticks(np.arange(-6, 9, 2))
ax.set_yticks(np.arange(-6, 8, 2))

# 浅灰色网格
ax.grid(
    True,
    color="0.90",
    linewidth=0.6,
    alpha=0.8
)

# 原点参考线，可选
ax.axhline(0, color="0.65", linewidth=0.5, zorder=0)
ax.axvline(0, color="0.65", linewidth=0.5, zorder=0)

# 边框样式
for spine in ax.spines.values():
    spine.set_linewidth(0.9)

ax.tick_params(
    axis="both",
    labelsize=11,
    direction="out",
    length=3.5,
    width=0.8
)

plt.tight_layout()


# =========================================================
# 6. 保存图片
# =========================================================

plt.savefig(
    "pca_biplot_unoccupied_habitats.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "pca_biplot_unoccupied_habitats.pdf",
    bbox_inches="tight"
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")