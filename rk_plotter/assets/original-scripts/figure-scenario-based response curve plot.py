import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# 1. 构造示例数据
# =========================================================

np.random.seed(42)

# 历史时期
x_hist = np.array([-0.2, 0.0, 0.4, 0.8, 1.1])
y_hist = np.array([0.0, 1.0, 3.5, 7.5, 9.0])

# RCP 2.6：升温幅度较低，曲线到 2°C 左右趋缓
x_rcp26 = np.array([1.1, 1.3, 1.5, 1.7, 1.9, 2.1])
y_rcp26 = np.array([9.0, 11.0, 14.0, 17.0, 19.0, 18.5])

# RCP 8.5：升温持续增加，概率比快速升高
x_rcp85 = np.array([1.1, 1.5, 2.0, 2.4, 3.0, 3.6, 4.2, 5.2])
y_rcp85 = np.array([9.0, 15.0, 22.0, 27.0, 34.0, 41.0, 47.0, 58.0])


# =========================================================
# 2. 生成多模式集合细线
# =========================================================

def make_ensemble_lines(x, y, n=8, x_jitter=0.05, y_jitter=3.0):
    """
    根据主曲线生成多条集合模拟曲线
    """
    lines = []
    for _ in range(n):
        xx = x + np.random.normal(0, x_jitter, size=len(x))
        yy = y + np.random.normal(0, y_jitter, size=len(y))

        # 保证基本单调性
        sort_idx = np.argsort(xx)
        xx = xx[sort_idx]
        yy = yy[sort_idx]
        yy = np.maximum.accumulate(yy)

        lines.append((xx, yy))
    return lines


ensemble_26 = make_ensemble_lines(x_rcp26, y_rcp26, n=7, y_jitter=2.0)
ensemble_85 = make_ensemble_lines(x_rcp85, y_rcp85, n=9, y_jitter=3.5)


# =========================================================
# 3. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(5.4, 4.4), dpi=300)

# RCP 8.5 集合细线
for xx, yy in ensemble_85:
    ax.plot(
        xx, yy,
        color="#ff9a9a",
        linewidth=1.0,
        alpha=0.85,
        zorder=1
    )

# RCP 2.6 集合细线
for xx, yy in ensemble_26:
    ax.plot(
        xx, yy,
        color="#9bb5e8",
        linewidth=1.0,
        alpha=0.85,
        zorder=1
    )

# 历史时期
ax.plot(
    x_hist,
    y_hist,
    color="black",
    linewidth=2.0,
    marker="o",
    markersize=4.5,
    zorder=4
)

# 主情景曲线
ax.plot(
    x_rcp85,
    y_rcp85,
    color="red",
    linewidth=2.0,
    label="Historical + RCP 8.5",
    zorder=5
)

ax.plot(
    x_rcp26,
    y_rcp26,
    color="#2446a8",
    linewidth=2.0,
    label="Historical + RCP 2.6",
    zorder=5
)

# 关键年代点
ax.scatter([0.0, 0.8], [1.0, 7.5], color="black", s=24, zorder=6)
ax.scatter([1.7, 2.4, 4.2], [17.0, 27.0, 47.0], color="red", s=28, zorder=6)
ax.scatter([1.55, 1.85], [15.5, 18.2], color="#2446a8", s=28, zorder=6)


# =========================================================
# 4. 年代标注
# =========================================================

ax.text(
    -0.42, 2.6,
    "1870s",
    color="black",
    fontsize=11
)

ax.text(
    0.35, 9.5,
    "2000s",
    color="black",
    fontsize=11
)

ax.text(
    1.55, 18.5,
    "2050s",
    color="#2446a8",
    fontsize=11
)

ax.text(
    1.88, 16.2,
    "2090s",
    color="#2446a8",
    fontsize=11
)

ax.text(
    1.65, 29.5,
    "2050s",
    color="red",
    fontsize=11
)

ax.text(
    3.40, 49.5,
    "2090s",
    color="red",
    fontsize=11
)


# =========================================================
# 5. 主坐标轴设置
# =========================================================

ax.set_xlim(-0.5, 5.5)
ax.set_ylim(-10, 70)

ax.set_xlabel(
    "Global warming (°C)",
    fontsize=13
)

ax.set_ylabel(
    "Probability ratio",
    fontsize=13
)

ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.set_yticks(np.arange(-10, 71, 10))

ax.tick_params(
    axis="both",
    direction="out",
    length=5,
    width=1.1,
    labelsize=11
)

# 上轴和右轴刻度，贴近原图风格
ax.tick_params(
    top=True,
    right=True,
    labeltop=False,
    labelright=False
)

for spine in ax.spines.values():
    spine.set_linewidth(1.1)


# =========================================================
# 6. 图例
# =========================================================

ax.legend(
    loc="upper left",
    frameon=False,
    fontsize=11,
    handlelength=2.5,
    borderpad=0.2,
    labelspacing=0.5
)


# =========================================================
# 7. 橙色辅助横轴：累计 CO2 排放量
# =========================================================

orange = "#f6a000"

# 假设累计 CO2 排放量与升温近似线性对应
# 这里仅为绘图模板，真实研究中应使用你的碳排放—升温换算关系
co2_ticks = np.array([500, 1000, 1500, 2000])
warming_positions = np.array([1.55, 2.55, 3.55, 4.55])

# 小刻度
for xpos in warming_positions:
    ax.plot(
        [xpos, xpos],
        [-10, -7.8],
        color=orange,
        linewidth=1.1,
        clip_on=False,
        zorder=8
    )

# 刻度文字
for xpos, lab in zip(warming_positions, co2_ticks):
    ax.text(
        xpos,
        -5.3,
        f"{lab:,}",
        color=orange,
        fontsize=11,
        ha="center",
        va="bottom"
    )

# 辅助轴标题
ax.text(
    3.10,
    2.0,
    "Cumulative CO$_2$ emissions\nfrom 1870 (Gt C)",
    color=orange,
    fontsize=11,
    ha="center",
    va="bottom"
)


# =========================================================
# 8. 可选：左下角子图编号
# =========================================================

# fig.text(
#     0.02, 0.02,
#     "d",
#     fontsize=16,
#     fontweight="bold"
# )


# =========================================================
# 9. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "warming_probability_ratio_rcp_scenarios.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "warming_probability_ratio_rcp_scenarios.pdf",
    bbox_inches="tight"
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")