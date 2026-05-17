import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# =========================================================
# 1. 构造示例数据
# =========================================================

np.random.seed(42)

years = np.arange(1982, 2017)

categories = [
    "Imidacloprid",
    "Acetamiprid",
    "Nitenpyram",
    "Thiamethoxam",
    "Thiacloprid",
    "Clothianidin",
    "Dinotefuran"
]

# 模拟不同农药在不同年份的销售量
data = pd.DataFrame(index=years, columns=categories, dtype=float)
data[:] = 0

for year in years:
    # 早期几乎无销售
    if year < 1993:
        values = np.zeros(len(categories))

    # 1993—1998：主要是 Imidacloprid 少量增长
    elif year < 1999:
        values = np.array([
            np.random.uniform(40, 220),   # Imidacloprid
            np.random.uniform(0, 40),     # Acetamiprid
            np.random.uniform(0, 10),     # Nitenpyram
            0,
            0,
            0,
            0
        ])

    # 1999—2005：多个品种开始出现
    elif year < 2006:
        values = np.array([
            np.random.uniform(500, 950),
            np.random.uniform(20, 80),
            np.random.uniform(10, 60),
            np.random.uniform(50, 250),
            np.random.uniform(0, 40),
            np.random.uniform(0, 80),
            np.random.uniform(0, 250)
        ])

    # 2006—2009：总量上升，Dinotefuran 和 Thiamethoxam 增加
    elif year < 2010:
        values = np.array([
            np.random.uniform(150, 900),
            np.random.uniform(20, 100),
            np.random.uniform(20, 100),
            np.random.uniform(350, 850),
            np.random.uniform(50, 130),
            np.random.uniform(250, 550),
            np.random.uniform(800, 1400)
        ])

    # 2010 以后：总量明显升高
    else:
        values = np.array([
            np.random.uniform(150, 1100),
            np.random.uniform(30, 150),
            np.random.uniform(30, 150),
            np.random.uniform(500, 1300),
            np.random.uniform(70, 180),
            np.random.uniform(350, 900),
            np.random.uniform(900, 1900)
        ])

    data.loc[year] = values

# 为了让总量更接近示例图，设置一个逐年增长系数
growth_factor = np.interp(
    years,
    [1982, 1995, 2003, 2010, 2016],
    [0.0, 0.6, 1.0, 1.5, 1.8]
)

data = data.mul(growth_factor, axis=0)

# 控制总量上限，避免过高
row_sum = data.sum(axis=1)
scale = np.where(row_sum > 4200, 4200 / row_sum, 1)
data = data.mul(scale, axis=0)


# =========================================================
# 2. 颜色设置
# =========================================================

colors = {
    "Dinotefuran":   "#6ec9dc",  # 青蓝
    "Clothianidin": "#c052ad",  # 紫红
    "Thiacloprid":  "#4b224e",  # 深紫
    "Thiamethoxam": "#cce6bf",  # 浅绿
    "Nitenpyram":   "#e41a1c",  # 红
    "Acetamiprid":  "#f5e98b",  # 浅黄
    "Imidacloprid": "#3d5aa9",  # 蓝
}

# 堆叠顺序：从柱子底部到顶部
stack_order = [
    "Imidacloprid",
    "Acetamiprid",
    "Nitenpyram",
    "Thiamethoxam",
    "Thiacloprid",
    "Clothianidin",
    "Dinotefuran"
]

# 图例显示顺序：与示例图一致，从上到下
legend_order = [
    "Dinotefuran",
    "Clothianidin",
    "Thiacloprid",
    "Thiamethoxam",
    "Nitenpyram",
    "Acetamiprid",
    "Imidacloprid"
]


# =========================================================
# 3. 绘制堆叠柱状图
# =========================================================

fig, ax = plt.subplots(figsize=(8.0, 4.9), dpi=300)

bottom = np.zeros(len(years))

for cat in stack_order:
    ax.bar(
        years,
        data[cat].values,
        bottom=bottom,
        width=0.42,
        color=colors[cat],
        edgecolor="black",
        linewidth=0.45,
        label=cat
    )
    bottom += data[cat].values


# =========================================================
# 4. 坐标轴样式
# =========================================================

ax.set_xlim(1981.0, 2016.8)
ax.set_ylim(0, 4500)

ax.set_xlabel(
    "Year",
    fontsize=12
)

ax.set_ylabel(
    "Sales volume in Shimane Prefecture (kg)",
    fontsize=12
)

# x 轴每两年显示一个刻度
xticks = np.arange(1982, 2017, 2)
ax.set_xticks(xticks)
ax.set_xticklabels(
    xticks,
    rotation=90,
    fontsize=10
)

ax.set_yticks(np.arange(0, 4501, 500))
ax.set_yticklabels(
    np.arange(0, 4501, 500),
    fontsize=10
)

ax.tick_params(
    axis="both",
    direction="in",
    length=4,
    width=0.8
)

for spine in ax.spines.values():
    spine.set_linewidth(0.9)


# =========================================================
# 5. 图例设置
# =========================================================

handles, labels = ax.get_legend_handles_labels()
handle_dict = dict(zip(labels, handles))

legend_handles = [handle_dict[label] for label in legend_order]

ax.legend(
    legend_handles,
    legend_order,
    loc="upper left",
    bbox_to_anchor=(0.06, 0.80),
    frameon=False,
    fontsize=10,
    handlelength=0.7,
    handletextpad=0.25,
    borderpad=0.2,
    labelspacing=0.35
)


# =========================================================
# 6. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "stacked_bar_sales_volume_by_year.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "stacked_bar_sales_volume_by_year.pdf",
    bbox_inches="tight"
)

plt.show()