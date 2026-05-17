import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


# =========================================================
# 1. 示例数据
# =========================================================

years = np.arange(1982, 2017)

# 模拟年度 MHW days
global_average = np.array([
    34, 41, 24, 19, 23, 31, 24, 21, 20, 24,
    33, 26, 24, 23, 27, 44, 55, 31, 28, 30,
    33, 33, 32, 40, 35, 35, 38, 44, 65, 50,
    39, 44, 65, 94, 90
])

excluding_enso = np.array([
    22, 24, 23, 19, 21, 18, 20, 20, 20, 23,
    22, 21, 20, 22, 25, 30, 32, 24, 22, 28,
    32, 32, 33, 37, 32, 29, 35, 40, 41, 36,
    34, 40, 63, 77, 68
])


# =========================================================
# 2. ENSO 时期设置
#    每个元组表示阴影起止年份
# =========================================================

el_nino_periods = [
    (1982.6, 1983.8),
    (1986.2, 1987.4),
    (1991.2, 1992.0),
    (1992.6, 1993.1),
    (1994.1, 1994.5),
    (1997.0, 1998.4),
    (2009.7, 2010.2),
    (2014.9, 2016.5),
]

la_nina_periods = [
    (1988.0, 1988.9),
    (1998.6, 2000.0),
    (2007.2, 2008.1),
    (2008.5, 2008.9),
    (2010.3, 2011.4),
    (2011.8, 2012.3),
]


# =========================================================
# 3. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(7.4, 4.2), dpi=300)

# ENSO 背景阴影
for start, end in el_nino_periods:
    ax.axvspan(
        start,
        end,
        color="#f4b6bc",
        alpha=0.75,
        zorder=0
    )

for start, end in la_nina_periods:
    ax.axvspan(
        start,
        end,
        color="#aaa8ee",
        alpha=0.80,
        zorder=0
    )

# 折线
ax.plot(
    years,
    global_average,
    color="black",
    linewidth=2.0,
    label="Global average",
    zorder=3
)

ax.plot(
    years,
    excluding_enso,
    color="#ff3b3b",
    linewidth=2.0,
    label="Excluding ENSO",
    zorder=3
)


# =========================================================
# 4. 坐标轴设置
# =========================================================

ax.set_xlim(1981, 2016.8)
ax.set_ylim(10, 100)

ax.set_ylabel(
    "Annual MHW days",
    fontsize=15
)

ax.set_xticks([1985, 1990, 1995, 2000, 2005, 2010, 2015])
ax.set_yticks(np.arange(10, 101, 10))

ax.tick_params(
    axis="both",
    direction="in",
    length=6,
    width=1.0,
    labelsize=13,
    top=True,
    right=True
)

for spine in ax.spines.values():
    spine.set_linewidth(1.1)

ax.grid(False)


# =========================================================
# 5. 图例
# =========================================================

legend_handles = [
    Line2D(
        [0], [0],
        color="black",
        linewidth=2.0,
        label="Global average"
    ),
    Line2D(
        [0], [0],
        color="#ff3b3b",
        linewidth=2.0,
        label="Excluding ENSO"
    ),
    Patch(
        facecolor="#f4b6bc",
        edgecolor="#f4b6bc",
        alpha=0.75,
        label="El Niño period"
    ),
    Patch(
        facecolor="#aaa8ee",
        edgecolor="#aaa8ee",
        alpha=0.80,
        label="La Niña period"
    ),
]

legend = ax.legend(
    handles=legend_handles,
    loc="upper left",
    frameon=True,
    fancybox=False,
    framealpha=1,
    edgecolor="black",
    fontsize=13,
    handlelength=1.6,
    handletextpad=0.6,
    borderpad=0.7,
    labelspacing=0.6
)

legend.get_frame().set_linewidth(1.0)
legend.get_frame().set_facecolor("white")


# =========================================================
# 6. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "annual_mhw_days_enso_periods.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "annual_mhw_days_enso_periods.pdf",
    bbox_inches="tight"
)

plt.show()