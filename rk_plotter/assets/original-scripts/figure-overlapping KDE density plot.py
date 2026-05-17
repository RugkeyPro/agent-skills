import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.patches import Patch


# =========================================================
# 1. 构造示例数据
# =========================================================

np.random.seed(42)

cities = [
    "Hamburg",
    "Los Angeles",
    "Shenzhen",
    "Maracaibo",
    "Agra",
    "Mogadishu"
]

# 用 log10 空间生成数据，更适合塑料排放这类右偏分布
# 每个城市的参数为：log10 均值、标准差、样本量
params = {
    "Hamburg":     (-1.55, 0.23, 900),
    "Los Angeles": (-1.35, 0.25, 900),
    "Shenzhen":    (-0.95, 0.28, 900),
    "Maracaibo":   (-0.55, 0.22, 900),
    "Agra":        (0.75, 0.35, 900),
    "Mogadishu":   (1.20, 0.24, 900),
}

data = {}

for city, (mu, sigma, n) in params.items():
    log_values = np.random.normal(mu, sigma, n)

    # 给部分城市添加次峰，使分布更接近示例图
    if city == "Maracaibo":
        log_values = np.concatenate([
            log_values,
            np.random.normal(0.25, 0.25, 260)
        ])

    if city == "Agra":
        log_values = np.concatenate([
            log_values,
            np.random.normal(0.10, 0.25, 260)
        ])

    values = 10 ** log_values
    values = np.clip(values, 1e-3, 1e2)
    data[city] = values


# =========================================================
# 2. 颜色设置
# =========================================================

colors = {
    "Hamburg":     "#b8ded7",
    "Los Angeles": "#9ecae1",
    "Shenzhen":    "#cbb7d4",
    "Maracaibo":   "#f1edc7",
    "Agra":        "#f6d7ad",
    "Mogadishu":   "#f2c4b6",
}


# =========================================================
# 3. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(7.4, 3.2), dpi=300)

# 在 log10 空间计算 KDE，再把横轴转回真实值
x_log_grid = np.linspace(-3, 2, 600)
x_grid = 10 ** x_log_grid

for city in cities:
    values = data[city]

    log_values = np.log10(values)

    kde = gaussian_kde(log_values, bw_method=0.25)
    density = kde(x_log_grid)

    ax.fill_between(
        x_grid,
        density,
        0,
        color=colors[city],
        alpha=0.72,
        edgecolor="black",
        linewidth=0.9,
        label=city,
        zorder=2
    )

    ax.plot(
        x_grid,
        density,
        color="black",
        linewidth=0.8,
        zorder=3
    )


# =========================================================
# 4. 坐标轴设置
# =========================================================

ax.set_xscale("log")

ax.set_xlim(8e-4, 1.5e2)
ax.set_ylim(0, 1.75)

ax.set_xlabel(
    "Plastic emissions (kg cap$^{-1}$ year$^{-1}$)",
    fontsize=11,
    labelpad=8
)

ax.set_ylabel(
    "Density",
    fontsize=11
)

# 自定义横轴刻度，贴近原图写法
xticks = [1e-3, 1e-2, 1e-1, 1, 10, 100]
xticklabels = [
    r"$1 \times 10^{-3}$",
    r"$1 \times 10^{-2}$",
    r"$1 \times 10^{-1}$",
    r"$1 \times 10^{0}$",
    r"$1 \times 10^{1}$",
    r"$1 \times 10^{2}$",
]

ax.set_xticks(xticks)
ax.set_xticklabels(xticklabels, fontsize=9)

ax.set_yticks([0, 0.5, 1.0, 1.5])
ax.set_yticklabels(["0", "0.5", "1.0", "1.5"], fontsize=10)

ax.tick_params(
    axis="both",
    direction="out",
    length=4,
    width=0.9
)

# 只保留左轴和下轴
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.spines["left"].set_linewidth(1.0)
ax.spines["bottom"].set_linewidth(1.0)

ax.grid(False)


# =========================================================
# 5. 图例
# =========================================================

legend_handles = [
    Patch(
        facecolor=colors[city],
        edgecolor="black",
        linewidth=0.8,
        label=city
    )
    for city in cities
]

ax.legend(
    handles=legend_handles,
    loc="upper left",
    frameon=False,
    fontsize=8,
    handlelength=0.9,
    handleheight=0.9,
    handletextpad=0.35,
    labelspacing=0.35,
    borderpad=0.1
)


# =========================================================
# 6. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "city_plastic_emissions_density_plot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "city_plastic_emissions_density_plot.pdf",
    bbox_inches="tight"
)

plt.show()