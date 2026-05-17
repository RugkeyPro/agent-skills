import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


# =========================================================
# 1. 构造示例数据
# =========================================================

np.random.seed(42)

years = np.arange(1980, 2101)

# 不同情景开始明显分化的年份
split_year = 2018


def make_series(years, start_year, end_value, noise_scale=0.7):
    """
    生成带随机波动的长期变化趋势
    start_year : 情景开始年份
    end_value  : 2100 年左右的变化终值
    """
    y = np.zeros_like(years, dtype=float)

    # 历史期：轻微下降
    hist_mask = years < start_year
    y[hist_mask] = np.interp(
        years[hist_mask],
        [years.min(), start_year - 1],
        [0.0, -2.5]
    )

    # 未来期：按情景下降
    fut_mask = years >= start_year
    y[fut_mask] = np.interp(
        years[fut_mask],
        [start_year, years.max()],
        [-2.5, end_value]
    )

    # 加入年代际波动和随机扰动
    oscillation = (
        0.8 * np.sin(2 * np.pi * (years - 1980) / 38)
        + 0.4 * np.sin(2 * np.pi * (years - 1980) / 11)
    )

    noise = np.random.normal(0, noise_scale, len(years))

    y = y + 0.45 * oscillation + noise

    return y


# 三种 SSP 情景
ssp126 = make_series(years, split_year, end_value=-7.0,  noise_scale=0.65)
ssp370 = make_series(years, split_year, end_value=-13.0, noise_scale=0.75)
ssp585 = make_series(years, split_year, end_value=-18.5, noise_scale=0.85)


# =========================================================
# 2. 构造不确定性范围
# =========================================================

def uncertainty_width(years, base=2.0, future_increase=3.0):
    """
    构造随时间增加的不确定性宽度
    """
    t = (years - years.min()) / (years.max() - years.min())
    width = base + future_increase * t
    width += 0.5 * np.sin(2 * np.pi * t * 3)
    return np.clip(width, 1.0, None)


w126 = uncertainty_width(years, base=2.0, future_increase=2.2)
w370 = uncertainty_width(years, base=2.2, future_increase=3.8)
w585 = uncertainty_width(years, base=2.4, future_increase=4.5)

ssp126_low, ssp126_high = ssp126 - w126, ssp126 + w126
ssp370_low, ssp370_high = ssp370 - w370, ssp370 + w370
ssp585_low, ssp585_high = ssp585 - w585, ssp585 + w585


# =========================================================
# 3. 颜色设置
# =========================================================

colors = {
    "SSP 1–2.6": "#33217f",   # 深紫蓝
    "SSP 3–7.0": "#4ca995",   # 青绿色
    "SSP 5–8.5": "#ad48a1",   # 紫红色
}


# =========================================================
# 4. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(7.0, 5.8), dpi=300)

# 不确定性阴影
ax.fill_between(
    years,
    ssp126_low,
    ssp126_high,
    color=colors["SSP 1–2.6"],
    alpha=0.18,
    linewidth=0
)

ax.fill_between(
    years,
    ssp370_low,
    ssp370_high,
    color=colors["SSP 3–7.0"],
    alpha=0.20,
    linewidth=0
)

ax.fill_between(
    years,
    ssp585_low,
    ssp585_high,
    color=colors["SSP 5–8.5"],
    alpha=0.18,
    linewidth=0
)

# 主趋势线
ax.plot(
    years,
    ssp126,
    color=colors["SSP 1–2.6"],
    linewidth=3.5,
    label="SSP 1–2.6"
)

ax.plot(
    years,
    ssp370,
    color=colors["SSP 3–7.0"],
    linewidth=3.5,
    label="SSP 3–7.0"
)

ax.plot(
    years,
    ssp585,
    color=colors["SSP 5–8.5"],
    linewidth=3.5,
    label="SSP 5–8.5"
)

# 0% 参考线
ax.axhline(
    0,
    color="black",
    linewidth=3.0,
    linestyle=(0, (6, 6)),
    zorder=1
)


# =========================================================
# 5. 坐标轴设置
# =========================================================

ax.set_xlim(1979, 2101)
ax.set_ylim(-23.5, 7.5)

ax.set_xlabel(
    "Year",
    fontsize=20,
    labelpad=12
)

ax.set_ylabel(
    r"$\Delta$ biomass (%)",
    fontsize=20,
    labelpad=12
)

ax.set_xticks([1980, 2010, 2040, 2070, 2100])
ax.set_xticklabels(
    ["1980", "2010", "2040", "2070", "2100"],
    fontsize=16
)

ax.set_yticks([-20, -10, 0])
ax.set_yticklabels(
    ["−20", "−10", "0"],
    fontsize=16
)

ax.tick_params(
    axis="both",
    direction="out",
    length=7,
    width=1.1
)

for spine in ax.spines.values():
    spine.set_linewidth(1.0)
    spine.set_color("0.35")

ax.grid(False)


# =========================================================
# 6. 顶部图例
# =========================================================

legend_handles = [
    Patch(
        facecolor=colors["SSP 1–2.6"],
        edgecolor="none",
        label="SSP 1–2.6"
    ),
    Patch(
        facecolor=colors["SSP 3–7.0"],
        edgecolor="none",
        label="SSP 3–7.0"
    ),
    Patch(
        facecolor=colors["SSP 5–8.5"],
        edgecolor="none",
        label="SSP 5–8.5"
    )
]

ax.legend(
    handles=legend_handles,
    loc="lower center",
    bbox_to_anchor=(0.5, 1.02),
    ncol=3,
    frameon=False,
    fontsize=17,
    handlelength=1.3,
    handleheight=1.3,
    columnspacing=1.8,
    handletextpad=0.5
)


# =========================================================
# 7. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "ssp_biomass_change_timeseries.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "ssp_biomass_change_timeseries.pdf",
    bbox_inches="tight"
)

plt.show()