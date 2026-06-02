import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


# =========================================================
# 1. 构造示例数据
# =========================================================

np.random.seed(42)

groups = ["TP", "NEP", "EP", "IMXJ", "YGP", "China"]

data = {
    "TP": np.concatenate([
        np.random.normal(1.0, 0.45, 70),
        np.random.normal(2.3, 0.45, 12),
        np.array([3.8, 5.0])
    ]),
    "NEP": np.concatenate([
        np.random.normal(0.45, 0.22, 30),
        np.random.normal(0.85, 0.18, 12)
    ]),
    "EP": np.concatenate([
        np.random.normal(0.35, 0.25, 55),
        np.random.normal(1.25, 0.35, 12),
        np.array([2.1])
    ]),
    "IMXJ": np.concatenate([
        np.random.normal(0.65, 0.25, 35),
        np.random.normal(1.20, 0.35, 10),
        np.array([2.5])
    ]),
    "YGP": np.concatenate([
        np.random.normal(2.1, 0.65, 28),
        np.array([4.8])
    ]),
    "China": np.concatenate([
        np.random.normal(0.65, 0.35, 80),
        np.random.normal(1.4, 0.45, 20),
        np.array([3.1, 5.0])
    ])
}

# 限制范围，避免随机值过低
for g in groups:
    data[g] = np.clip(data[g], 0, 5.0)


# =========================================================
# 2. 颜色设置
# =========================================================

colors = {
    "TP": "#75c8b4",
    "NEP": "#ff9b72",
    "EP": "#9fb2d6",
    "IMXJ": "#e89aca",
    "YGP": "#a7d45a",
    "China": "#a91d1d",
}


# =========================================================
# 3. 绘制半小提琴图函数
# =========================================================

def draw_half_violin(
    ax,
    values,
    x,
    color,
    side="right",
    width=0.33,
    y_min=0,
    y_max=5.0,
    alpha=0.75
):
    """
    绘制半小提琴图。
    
    side='right' 表示密度向右展开；
    side='left'  表示密度向左展开。
    """
    values = np.asarray(values)
    values = values[~np.isnan(values)]

    if len(values) < 3:
        return

    y_grid = np.linspace(y_min, y_max, 300)
    kde = gaussian_kde(values, bw_method=0.30)
    density = kde(y_grid)

    # 归一化密度宽度
    density = density / density.max() * width

    if side == "right":
        x_left = np.full_like(y_grid, x)
        x_right = x + density
    else:
        x_left = x - density
        x_right = np.full_like(y_grid, x)

    ax.fill_betweenx(
        y_grid,
        x_left,
        x_right,
        facecolor=color,
        edgecolor="none",
        alpha=alpha,
        zorder=1
    )


# =========================================================
# 4. 开始绘图
# =========================================================

fig, ax = plt.subplots(figsize=(7.4, 4.2), dpi=300)

positions = np.arange(1, len(groups) + 1)

for i, group in enumerate(groups):
    x = positions[i]
    values = data[group]
    color = colors[group]

    # 半小提琴图，向右展开
    draw_half_violin(
        ax=ax,
        values=values,
        x=x + 0.08,
        color=color,
        side="right",
        width=0.34,
        y_min=0,
        y_max=5.0,
        alpha=0.78
    )

    # 抖动散点，放在箱线图左侧
    jitter = np.random.normal(loc=-0.05, scale=0.045, size=len(values))

    ax.scatter(
        np.full_like(values, x) + jitter,
        values,
        s=22,
        color=color,
        alpha=0.42,
        edgecolor="white",
        linewidth=0.3,
        zorder=3
    )

    # 箱线图
    box = ax.boxplot(
        values,
        positions=[x],
        widths=0.18,
        patch_artist=True,
        showfliers=False,
        medianprops=dict(
            color="black",
            linewidth=1.4
        ),
        boxprops=dict(
            facecolor="white",
            edgecolor="black",
            linewidth=1.2,
            alpha=0.82
        ),
        whiskerprops=dict(
            color="black",
            linewidth=1.1
        ),
        capprops=dict(
            color="black",
            linewidth=1.1
        )
    )

    # 在箱体上叠加半透明组内颜色
    for patch in box["boxes"]:
        patch.set_facecolor("white")
        patch.set_alpha(0.78)

    # 可选：显示均值点
    ax.scatter(
        x,
        np.mean(values),
        s=25,
        color=color,
        edgecolor="black",
        linewidth=0.4,
        zorder=5
    )


# =========================================================
# 5. 坐标轴设置
# =========================================================

ax.set_xlim(0.4, len(groups) + 0.7)
ax.set_ylim(-0.25, 5.25)

ax.set_xticks(positions)
ax.set_xticklabels(
    groups,
    fontsize=13
)

ax.set_ylabel(
    "LCC magnitude(°C)",
    fontsize=15,
    fontweight="bold"
)

ax.set_yticks(np.arange(0, 5.1, 1))
ax.set_yticklabels(
    [str(i) for i in range(0, 6)],
    fontsize=12
)

# 网格线
ax.grid(
    True,
    axis="both",
    color="0.88",
    linewidth=1.0,
    alpha=0.85
)

ax.set_axisbelow(True)

ax.tick_params(
    axis="both",
    direction="out",
    length=4,
    width=1.0
)

for spine in ax.spines.values():
    spine.set_linewidth(1.2)
    spine.set_color("black")


# =========================================================
# 6. 可选：左上角子图编号
# =========================================================

ax.text(
    0.01,
    0.98,
    "(a)",
    transform=ax.transAxes,
    ha="left",
    va="top",
    fontsize=20,
    fontweight="bold"
)

# 若不需要左上角编号，删除上面 ax.text(...) 这一段即可。


# =========================================================
# 7. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "lcc_magnitude_raincloud_plot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "lcc_magnitude_raincloud_plot.pdf",
    bbox_inches="tight"
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")