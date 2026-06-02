import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, LogFormatterMathtext


# =========================================================
# 1. 构造示例数据
# =========================================================

np.random.seed(42)

def generate_log_data(n, x_min, x_max, scatter=0.35):
    """
    在 log10 空间生成接近 1:1 线的散点数据
    """
    logx = np.random.uniform(np.log10(x_min), np.log10(x_max), n)
    logy = logx + np.random.normal(0, scatter, n)

    x = 10 ** logx
    y = 10 ** logy
    return x, y


data = {
    "South America": generate_log_data(1, 1e5, 4e5, scatter=0.12),
    "North America": generate_log_data(28, 1e1, 3e4, scatter=0.45),
    "Europe": generate_log_data(8, 1, 2e3, scatter=0.45),
    "Asia": generate_log_data(22, 2e1, 5e4, scatter=0.35),
    "Africa": generate_log_data(3, 5e2, 3e3, scatter=0.35),
}

# 手动设置两个代表性大流域点，使其接近原图
data["South America"] = (
    np.array([2.2e5]),
    np.array([3.2e5])
)

# 给 Asia 加入一个 Yangtze 点
asia_x, asia_y = data["Asia"]
asia_x = np.append(asia_x, 4.8e4)
asia_y = np.append(asia_y, 4.5e4)
data["Asia"] = (asia_x, asia_y)


# =========================================================
# 2. 设置样式
# =========================================================

styles = {
    "South America": {
        "marker": "s",
        "color": "#61c3f2",
        "edgecolor": "black",
        "size": 90
    },
    "North America": {
        "marker": "o",
        "color": "#ffa72b",
        "edgecolor": "black",
        "size": 85
    },
    "Europe": {
        "marker": "D",
        "color": "white",
        "edgecolor": "black",
        "size": 60
    },
    "Asia": {
        "marker": "^",
        "color": "#f4a6a6",
        "edgecolor": "black",
        "size": 85
    },
    "Africa": {
        "marker": "o",
        "color": "#bfe3f6",
        "edgecolor": "black",
        "size": 85
    },
}


# =========================================================
# 3. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(5.4, 5.2), dpi=300)

# 1:1 参考线
ax.plot(
    [1, 1e6],
    [1, 1e6],
    color="black",
    linewidth=0.9,
    zorder=1
)

# 绘制分类散点
for region, (x, y) in data.items():
    style = styles[region]

    ax.scatter(
        x,
        y,
        s=style["size"],
        marker=style["marker"],
        facecolor=style["color"],
        edgecolor=style["edgecolor"],
        linewidth=0.9,
        label=region,
        zorder=3
    )


# =========================================================
# 4. 添加部分误差线
# =========================================================

# 为了模拟原图，只给部分点添加纵向误差线
error_points = [
    ("South America", 0, 0.75),
    ("Asia", -1, 0.15),
    ("Asia", 3, 0.30),
    ("Asia", 6, 0.45),
    ("Asia", 10, 0.40),
    ("North America", 5, 0.35),
    ("North America", 12, 0.50),
    ("North America", 20, 0.90),
]

for region, idx, err_log_scale in error_points:
    x, y = data[region]

    if idx < 0:
        idx = len(x) + idx

    if idx >= len(x):
        continue

    xi = x[idx]
    yi = y[idx]

    # 在对数空间设置误差范围
    yerr_lower = yi - yi / (10 ** err_log_scale)
    yerr_upper = yi * (10 ** err_log_scale) - yi

    ax.errorbar(
        xi,
        yi,
        yerr=np.array([[yerr_lower], [yerr_upper]]),
        fmt="none",
        ecolor="black",
        elinewidth=0.8,
        capsize=4,
        capthick=0.8,
        zorder=2
    )


# =========================================================
# 5. 添加文字标注
# =========================================================

# Amazon 标注
amazon_x = data["South America"][0][0]
amazon_y = data["South America"][1][0]

ax.text(
    amazon_x * 0.68,
    amazon_y * 1.02,
    "Amazon",
    fontsize=11,
    ha="right",
    va="center"
)

# Yangtze 标注
yangtze_x = data["Asia"][0][-1]
yangtze_y = data["Asia"][1][-1]

ax.text(
    yangtze_x * 0.78,
    yangtze_y * 1.00,
    "Yangtze",
    fontsize=11,
    ha="right",
    va="center"
)


# =========================================================
# 6. 坐标轴设置
# =========================================================

ax.set_xscale("log")
ax.set_yscale("log")

ax.set_xlim(1, 1e6)
ax.set_ylim(1, 1e6)

ax.set_xlabel(
    "Model (kg yr$^{-1}$)",
    fontsize=12,
    labelpad=8
)

ax.set_ylabel(
    "Observation (kg yr$^{-1}$)",
    fontsize=12,
    labelpad=8
)

# 主刻度：10^0 到 10^6
major_locator = LogLocator(base=10.0, numticks=7)
major_formatter = LogFormatterMathtext(base=10.0)

ax.xaxis.set_major_locator(major_locator)
ax.yaxis.set_major_locator(major_locator)

ax.xaxis.set_major_formatter(major_formatter)
ax.yaxis.set_major_formatter(major_formatter)

# 次刻度
ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1))
ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1))

ax.tick_params(
    axis="both",
    which="major",
    direction="in",
    length=4,
    width=0.8,
    labelsize=10
)

ax.tick_params(
    axis="both",
    which="minor",
    direction="in",
    length=2,
    width=0.6
)

for spine in ax.spines.values():
    spine.set_linewidth(0.9)

ax.grid(False)


# =========================================================
# 7. 图例设置
# =========================================================

ax.legend(
    loc="upper left",
    frameon=False,
    fontsize=10,
    handlelength=1.0,
    handletextpad=0.5,
    labelspacing=0.6,
    borderpad=0.2
)


# =========================================================
# 8. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "model_observation_loglog_scatter.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "model_observation_loglog_scatter.pdf",
    bbox_inches="tight"
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")