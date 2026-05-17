import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# =========================================================
# 1. 构造示例时间序列数据
# =========================================================

np.random.seed(42)

# 日期范围：2013-01 到 2014-01
dates = pd.date_range(
    start="2013-01-01",
    end="2014-01-20",
    freq="D"
)

n = len(dates)

# 构造模拟浓度数据
# 使用趋势项 + 季节波动 + 随机扰动
t = np.arange(n)

seasonal = (
    2.0 * np.sin(2 * np.pi * t / 365)
    + 1.2 * np.sin(2 * np.pi * (t - 40) / 90)
)

trend = np.interp(
    t,
    [0, 80, 170, 260, n - 1],
    [7.5, 13.0, 9.0, 8.0, 9.5]
)

noise = np.random.normal(0, 0.9, n)

simulated = trend + seasonal + noise

# 适当平滑，使曲线更接近示例图
simulated = pd.Series(simulated).rolling(
    window=3,
    center=True,
    min_periods=1
).mean().values

# 限制范围
simulated = np.clip(simulated, 3.5, 15.5)


# =========================================================
# 2. 构造观测点数据
# =========================================================

observed_dates = pd.to_datetime([
    "2013-01-20",
    "2013-03-08",
    "2013-04-08",
    "2013-05-05",
    "2013-06-15",
    "2013-07-15",
    "2013-09-07",
    "2013-10-05",
    "2013-11-08",
    "2013-12-05",
    "2014-01-02"
])

observed_values = np.array([
    9.5, 9.4, 8.3, 7.2, 8.4,
    5.7, 8.8, 9.7, 8.1, 9.2, 8.6
])


# =========================================================
# 3. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(7.8, 2.6), dpi=300)

# 模拟值折线
ax.plot(
    dates,
    simulated,
    color="#0072B2",
    linewidth=1.1,
    label="Simulated"
)

# 观测值散点
ax.scatter(
    observed_dates,
    observed_values,
    color="#ff7f0e",
    s=26,
    edgecolor="none",
    label="Observed",
    zorder=3
)


# =========================================================
# 4. 坐标轴设置
# =========================================================

ax.set_ylabel(
    "Concentration (ng L$^{-1}$)",
    fontsize=13
)

ax.set_ylim(0, 16)
ax.set_yticks(np.arange(0, 17, 2))

ax.set_xlim(
    pd.to_datetime("2013-01-01"),
    pd.to_datetime("2014-01-20")
)

# x 轴日期格式：2013-01, 2013-03, ...
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

ax.tick_params(
    axis="x",
    labelsize=11,
    direction="out",
    length=4,
    width=0.9,
    rotation=0
)

ax.tick_params(
    axis="y",
    labelsize=11,
    direction="out",
    length=4,
    width=0.9
)

# 边框
for spine in ax.spines.values():
    spine.set_linewidth(1.0)

# 不显示网格，贴近原图
ax.grid(False)


# =========================================================
# 5. 图例设置
# =========================================================

ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.15),
    ncol=2,
    frameon=True,
    fancybox=False,
    edgecolor="black",
    framealpha=1,
    fontsize=11,
    handlelength=1.4,
    handletextpad=0.4,
    columnspacing=0.9,
    borderpad=0.3
)


# =========================================================
# 6. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "simulated_observed_time_series.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "simulated_observed_time_series.pdf",
    bbox_inches="tight"
)

plt.show()