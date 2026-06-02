import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, LogFormatterMathtext


# =========================================================
# 1. 构造示例数据
# =========================================================

np.random.seed(42)

# 模拟年份
years = np.linspace(0, 30, 1200)

# Discharge to ocean：快速升高并逐渐接近 96.3%
discharge = 96.3 * (1 - np.exp(-years / 1.8))
discharge += 3.0 * np.exp(-years / 10) * np.sin(2 * np.pi * years / 1.1)
discharge += np.random.normal(0, 0.6, len(years))
discharge = np.clip(discharge, 8, 99)

# Residue：从高值快速下降，后期缓慢衰减，带周期波动
residue = (
    65 * np.exp(-years / 0.8)
    + 18 * np.exp(-years / 12)
    + 2.6
)
residue += 2.5 * np.exp(-years / 25) * np.sin(2 * np.pi * years / 0.85)
residue += np.random.normal(0, 0.35, len(years))
residue = np.clip(residue, 0.12, 100)

# Degraded：缓慢增加并接近 1.1%
degraded = 1.1 * (1 - np.exp(-years / 7.5))
degraded += 0.08 * np.exp(-years / 18) * np.sin(2 * np.pi * years / 0.9)
degraded += np.random.normal(0, 0.015, len(years))
degraded = np.clip(degraded, 0.1, 1.3)


# =========================================================
# 2. 颜色设置
# =========================================================

colors = {
    "Residue": "#c84c0c",             # 橙褐色
    "Degraded": "#3e5f9f",            # 深蓝
    "Discharge to ocean": "#5b86e5",  # 浅蓝
}


# =========================================================
# 3. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(6.4, 5.2), dpi=300)

# 右侧灰色阴影，可表示后期统计窗口
ax.axvspan(
    25,
    30,
    color="0.86",
    alpha=0.75,
    zorder=0
)

# 三条曲线
ax.plot(
    years,
    residue,
    color=colors["Residue"],
    linewidth=2.0,
    label="Residue (2.6 ± 0.9%)",
    zorder=3
)

ax.plot(
    years,
    degraded,
    color=colors["Degraded"],
    linewidth=2.0,
    label="Degraded (1.1 ± 0.4%)",
    zorder=3
)

ax.plot(
    years,
    discharge,
    color=colors["Discharge to ocean"],
    linewidth=2.0,
    label="Discharge to ocean (96.3 ± 0.9%)",
    zorder=3
)


# =========================================================
# 4. 坐标轴设置
# =========================================================

ax.set_yscale("log")

ax.set_xlim(0, 30)
ax.set_ylim(1e-1, 1.1e2)

ax.set_xlabel(
    "Simulated years",
    fontsize=16
)

ax.set_ylabel(
    "Fraction of cumulative yield into rivers, [%]",
    fontsize=16
)

ax.set_xticks(np.arange(0, 31, 5))

# 对数刻度：10^-1, 10^0, 10^1, 10^2
ax.yaxis.set_major_locator(LogLocator(base=10.0, numticks=4))
ax.yaxis.set_major_formatter(LogFormatterMathtext(base=10.0))

# 次刻度
ax.yaxis.set_minor_locator(
    LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1, numticks=40)
)

ax.tick_params(
    axis="both",
    which="major",
    direction="in",
    length=5,
    width=1.0,
    labelsize=13,
    top=True,
    right=True
)

ax.tick_params(
    axis="both",
    which="minor",
    direction="in",
    length=3,
    width=0.7,
    top=True,
    right=True
)

# 网格线
ax.grid(
    True,
    which="major",
    color="0.80",
    linewidth=0.8,
    alpha=0.7
)

ax.grid(
    True,
    which="minor",
    color="0.85",
    linewidth=0.5,
    linestyle=":",
    alpha=0.8
)

ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_linewidth(1.0)


# =========================================================
# 5. 图例
# =========================================================

legend = ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.58, 0.98),
    frameon=False,
    fontsize=12,
    handlelength=3.0,
    handletextpad=0.6,
    labelspacing=0.35
)

# 加粗图例线条
for line in legend.get_lines():
    line.set_linewidth(4.0)


# =========================================================
# 6. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "cumulative_yield_fate_log_timeseries.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "cumulative_yield_fate_log_timeseries.pdf",
    bbox_inches="tight"
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")