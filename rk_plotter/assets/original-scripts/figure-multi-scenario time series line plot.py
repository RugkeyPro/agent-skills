import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# =========================================================
# 1. 构造示例时间序列数据
# =========================================================

np.random.seed(42)

# 时间范围：2013-03-01 至 2014-04-01
dates = pd.date_range(
    start="2013-03-01",
    end="2014-04-01",
    freq="D"
)

n = len(dates)
t = np.arange(n)


# =========================================================
# 2. 构造具有季节波动和随机扰动的浓度数据
# =========================================================

def make_series(base_level, peak_scale, noise_scale, lower=0, upper=120):
    """
    生成类似环境浓度时间序列的数据
    base_level : 基础浓度水平
    peak_scale : 峰值波动强度
    noise_scale : 随机扰动强度
    """

    # 年内趋势：春季上升，夏季回落，秋冬升高，次年春季下降
    trend = np.interp(
        t,
        [0, 70, 130, 230, 310, n - 1],
        [45, 70, 50, 85, 55, 48]
    )

    # 周期波动
    seasonal = (
        8 * np.sin(2 * np.pi * t / 85)
        + 5 * np.sin(2 * np.pi * t / 32)
    )

    # 随机扰动
    noise = np.random.normal(0, noise_scale, n)

    # 若干脉冲峰值，模拟降雨、排放或模型扰动
    pulses = np.zeros(n)
    pulse_days = np.random.choice(np.arange(20, n - 20), size=24, replace=False)

    for d in pulse_days:
        width = np.random.uniform(1.5, 4.5)
        height = np.random.uniform(8, 24) * peak_scale
        pulses += height * np.exp(-((t - d) ** 2) / (2 * width ** 2))

    y = base_level + 0.55 * trend + seasonal + noise + pulses

    # 简单平滑，避免过度毛刺
    y = pd.Series(y).rolling(
        window=3,
        center=True,
        min_periods=1
    ).mean().values

    return np.clip(y, lower, upper)


# 四个情景 / 站点
S1 = make_series(base_level=15, peak_scale=1.0, noise_scale=8.0, lower=35, upper=112)
S2 = make_series(base_level=-5, peak_scale=0.65, noise_scale=7.0, lower=15, upper=95)
S3 = make_series(base_level=12, peak_scale=0.85, noise_scale=6.5, lower=35, upper=105)
S4 = make_series(base_level=-18, peak_scale=0.45, noise_scale=6.0, lower=10, upper=75)


# =========================================================
# 3. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(7.4, 5.4), dpi=300)

ax.plot(
    dates,
    S1,
    color="red",
    linewidth=1.0,
    linestyle="-",
    label="S1"
)

ax.plot(
    dates,
    S2,
    color="#7ac943",
    linewidth=1.0,
    linestyle=(0, (6, 4)),
    label="S2"
)

ax.plot(
    dates,
    S3,
    color="#0072b2",
    linewidth=1.0,
    linestyle=(0, (6, 4)),
    label="S3"
)

ax.plot(
    dates,
    S4,
    color="gray",
    linewidth=1.0,
    linestyle=(0, (6, 4)),
    label="S4"
)


# =========================================================
# 4. 坐标轴设置
# =========================================================

ax.set_ylabel(
    "Concentration (ng L$^{-1}$)",
    fontsize=15
)

ax.set_ylim(0, 120)
ax.set_yticks(np.arange(0, 121, 20))

ax.set_xlim(
    pd.to_datetime("2013-03-01"),
    pd.to_datetime("2014-04-01")
)

# 每月一个主刻度
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

plt.setp(
    ax.get_xticklabels(),
    rotation=45,
    ha="right",
    fontsize=11
)

plt.setp(
    ax.get_yticklabels(),
    fontsize=11
)

# 网格线
ax.grid(
    True,
    axis="both",
    color="0.90",
    linewidth=0.8,
    alpha=0.9
)

ax.set_axisbelow(True)

# 坐标轴边框
for spine in ax.spines.values():
    spine.set_linewidth(1.0)

ax.tick_params(
    axis="both",
    direction="out",
    length=4,
    width=0.9
)


# =========================================================
# 5. 图例
# =========================================================

ax.legend(
    loc="upper right",
    frameon=True,
    fancybox=False,
    framealpha=1,
    edgecolor="black",
    fontsize=12,
    handlelength=2.2,
    handletextpad=0.5,
    borderpad=0.4
)




# =========================================================
# 7. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "multi_scenario_concentration_timeseries.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "multi_scenario_concentration_timeseries.pdf",
    bbox_inches="tight"
)

plt.show()