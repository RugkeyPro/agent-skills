import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# 1. 构造示例数据
# =========================================================

np.random.seed(42)

# 每个区域包含：国家、颜色、y轴范围、模拟均值和标准差
panels = {
    "Latin America and the Caribbean": {
        "countries": ["BRA", "MEX", "ARG"],
        "color": "#a23b92",
        "ylim": (0, 3.2),
        "params": [(1.4, 0.32), (0.75, 0.22), (0.35, 0.10)]
    },
    "Sub-Saharan Africa": {
        "countries": ["NGA", "COD", "TZA"],
        "color": "#1f77d0",
        "ylim": (0, 6.5),
        "params": [(3.4, 0.55), (0.95, 0.22), (0.75, 0.18)]
    },
    "Western Asia": {
        "countries": ["IRQ", "TUR", "SYR"],
        "color": "#a23b92",
        "ylim": (0, 2.2),
        "params": [(0.78, 0.22), (0.45, 0.12), (0.32, 0.10)]
    },
    "Southern Asia": {
        "countries": ["IND", "PAK", "BGD"],
        "color": "#1f77d0",
        "ylim": (0, 19),
        "params": [(9.0, 1.6), (2.5, 0.45), (1.7, 0.30)]
    },
    "South-eastern Asia": {
        "countries": ["IDN", "THA", "PHL"],
        "color": "#1f77d0",
        "ylim": (0, 6.5),
        "params": [(3.4, 0.55), (1.0, 0.22), (0.75, 0.22)]
    },
    "Oceania": {
        "countries": ["PNG", "SLB", "VUT"],
        "color": "#1f77d0",
        "ylim": (0, 0.32),
        "params": [(0.12, 0.035), (0.012, 0.004), (0.008, 0.003)]
    }
}


def make_values(mean, sd, n=250, lower=0):
    """
    生成带少量离群点的模拟数据
    """
    values = np.random.normal(mean, sd, n)
    values = np.clip(values, lower, None)

    # 添加少量高值离群点，使箱线图更接近示例图
    n_out = max(5, int(n * 0.04))
    outliers = np.random.normal(mean + 2.8 * sd, 0.5 * sd, n_out)
    outliers = np.clip(outliers, lower, None)

    return np.concatenate([values, outliers])


data = {}

for region, info in panels.items():
    data[region] = []
    for mean, sd in info["params"]:
        data[region].append(make_values(mean, sd))


# =========================================================
# 2. 创建多面板图
# =========================================================

fig, axes = plt.subplots(
    nrows=1,
    ncols=len(panels),
    figsize=(13.5, 2.15),
    dpi=300,
    sharey=False
)

plt.subplots_adjust(
    left=0.04,
    right=0.995,
    top=0.82,
    bottom=0.25,
    wspace=0.38
)


# =========================================================
# 3. 绘制每个区域的箱线图
# =========================================================

for ax, (region, info) in zip(axes, panels.items()):

    countries = info["countries"]
    color = info["color"]
    ylim = info["ylim"]
    values = data[region]

    bp = ax.boxplot(
        values,
        positions=np.arange(1, len(countries) + 1),
        widths=0.58,
        patch_artist=True,
        showfliers=True,
        medianprops=dict(
            color=color,
            linewidth=1.2
        ),
        boxprops=dict(
            facecolor="white",
            edgecolor=color,
            linewidth=1.0
        ),
        whiskerprops=dict(
            color=color,
            linewidth=1.0
        ),
        capprops=dict(
            color=color,
            linewidth=1.0
        ),
        flierprops=dict(
            marker="o",
            markerfacecolor=color,
            markeredgecolor=color,
            markersize=1.6,
            alpha=0.75
        )
    )

    # 设置箱体为浅色填充
    for patch in bp["boxes"]:
        patch.set_facecolor("white")
        patch.set_alpha(0.9)

    # 面板标题
    ax.set_title(
        region,
        fontsize=9,
        pad=6
    )

    # x轴国家缩写
    ax.set_xticks(np.arange(1, len(countries) + 1))
    ax.set_xticklabels(
        countries,
        fontsize=8
    )

    # y轴范围
    ax.set_ylim(*ylim)

    # 根据不同量级设置 y 轴刻度
    ymax = ylim[1]

    if ymax <= 0.35:
        yticks = np.arange(0, ymax + 0.001, 0.05)
    elif ymax <= 2.5:
        yticks = np.arange(0, ymax + 0.001, 0.5)
    elif ymax <= 7:
        yticks = np.arange(0, ymax + 0.001, 1)
    else:
        yticks = np.arange(0, ymax + 0.001, 2)

    ax.set_yticks(yticks)

    # 坐标轴样式
    ax.tick_params(
        axis="both",
        direction="out",
        length=2.5,
        width=0.7,
        labelsize=8,
        pad=2
    )

    # 只保留左轴和下轴
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_linewidth(0.8)
    ax.spines["bottom"].set_linewidth(0.8)

    ax.grid(False)


# =========================================================
# 4. 保存图片
# =========================================================

plt.savefig(
    "regional_country_boxplots.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "regional_country_boxplots.pdf",
    bbox_inches="tight"
)

plt.show()