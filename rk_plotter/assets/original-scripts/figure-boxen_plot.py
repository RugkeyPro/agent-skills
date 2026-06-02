import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


# =========================================================
# 1. 随机生成示例数据
# =========================================================

np.random.seed(42)

# 三个濒危等级：VU, EN, CR
# 模拟 log[Area of native habitat (km²)] 数据
data = {
    "VU": np.random.normal(loc=11.1, scale=0.85, size=450),
    "EN": np.random.normal(loc=10.7, scale=0.80, size=420),
    "CR": np.random.normal(loc=10.5, scale=0.90, size=400),
}

# 限制数值范围，使其接近示例图 6—15
for key in data:
    data[key] = np.clip(data[key], 6.2, 15.0)


# =========================================================
# 2. 分层箱体绘制函数
# =========================================================

def draw_boxen(ax, values, x, color, width=0.82):
    """
    绘制类似 boxenplot / letter-value plot 的分层箱线图

    参数
    ----
    ax : matplotlib 坐标轴
    values : 一维数组
    x : x 轴位置
    color : 主颜色
    width : 最大箱体宽度
    """

    values = np.asarray(values)
    values = values[~np.isnan(values)]

    # 分位数层级，越靠近中位数箱体越宽
    quantile_pairs = [
        (0.025, 0.050, 0.18),
        (0.050, 0.100, 0.28),
        (0.100, 0.200, 0.42),
        (0.200, 0.350, 0.58),
        (0.350, 0.650, 1.00),
        (0.650, 0.800, 0.58),
        (0.800, 0.900, 0.42),
        (0.900, 0.950, 0.28),
        (0.950, 0.975, 0.18),
    ]

    # 轻微抖动散点，放在箱体后方
    jitter = np.random.normal(0, 0.035, size=len(values))
    ax.scatter(
        np.full_like(values, x) + jitter,
        values,
        s=9,
        color="0.60",
        alpha=0.18,
        zorder=1
    )

    # 竖向中心线，类似须线
    q_low, q_high = np.quantile(values, [0.025, 0.975])
    ax.plot(
        [x, x],
        [q_low, q_high],
        color="0.35",
        linewidth=1.2,
        alpha=0.65,
        zorder=2
    )

    # 绘制分层矩形
    for q1, q2, w_scale in quantile_pairs:
        y1, y2 = np.quantile(values, [q1, q2])
        rect_width = width * w_scale

        rect = Rectangle(
            (x - rect_width / 2, y1),
            rect_width,
            y2 - y1,
            facecolor=color,
            edgecolor="0.35",
            linewidth=0.8,
            alpha=0.82,
            zorder=3
        )
        ax.add_patch(rect)

    # 中位数横线
    median = np.median(values)
    ax.plot(
        [x - width * 0.48, x + width * 0.48],
        [median, median],
        color="0.25",
        linewidth=1.2,
        zorder=4
    )

    # 均值黑色菱形点
    mean = np.mean(values)
    ax.scatter(
        x,
        mean,
        marker="D",
        s=28,
        color="black",
        edgecolor="none",
        zorder=5
    )


# =========================================================
# 3. 开始绘图
# =========================================================

fig, ax = plt.subplots(figsize=(4.2, 5.8), dpi=300)

groups = ["VU", "EN", "CR"]
positions = [1, 2, 3]

# 颜色参考示例图：黄绿、橙色、红色
colors = {
    "VU": "#d8df27",
    "EN": "#d99036",
    "CR": "#c7191c",
}

for x, group in zip(positions, groups):
    draw_boxen(
        ax=ax,
        values=data[group],
        x=x,
        color=colors[group],
        width=0.82
    )


# =========================================================
# 4. 坐标轴与文字样式
# =========================================================

ax.set_xlim(0.48, 3.52)
ax.set_ylim(6, 15.1)

ax.set_xticks(positions)
ax.set_xticklabels(groups, fontsize=28)

ax.set_yticks([6, 9, 11, 13, 15])
ax.set_yticklabels([6, 9, 11, 13, 15], fontsize=22)

ax.set_title(
    "Amphibian",
    fontsize=30,
    pad=16
)

ax.set_ylabel(
    "log[Area of native\nhabitat (km$^2$)]",
    fontsize=28,
    labelpad=18
)

# 坐标轴线条
for spine in ax.spines.values():
    spine.set_linewidth(1.2)

ax.tick_params(
    axis="both",
    direction="out",
    length=7,
    width=1.2,
    pad=8
)

# 去掉网格，保持论文图风格
ax.grid(False)

plt.tight_layout()


# =========================================================
# 5. 保存图片
# =========================================================

plt.savefig(
    "amphibian_boxenplot_template.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "amphibian_boxenplot_template.pdf",
    bbox_inches="tight"
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")