import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


# =========================================================
# 1. 基础数据
# =========================================================

np.random.seed(42)

body_sizes = [1, 2, 3, 4, 6, 9, 13, 18, 27, 39, 58, 84, 123, 180, 263, 385, 562, 823, 1203, 1759]
x = np.arange(len(body_sizes))

# 塑料类型
plastic_types = ["PP", "PE", "PVC", "PS", "ABS"]

# 颜色尽量贴近原图
plastic_colors = {
    "PP":  "#e8d790",   # 浅黄
    "PE":  "#cfd6dc",   # 灰蓝
    "PVC": "#9fd9df",   # 浅青
    "PS":  "#d9cbd4",   # 淡粉灰
    "ABS": "#8b89aa",   # 蓝紫灰
}

# =========================================================
# 2. 构造堆叠百分比数据（每列加和 = 100）
#    趋势模拟原图：小体型以 PVC / PS / ABS 为主，
#    大体型 PP 比例增加
# =========================================================

n = len(body_sizes)

pp  = np.interp(np.arange(n), [0, 10, 14, 19], [0, 3, 25, 30]) + np.random.uniform(-2, 2, n)
pe  = np.interp(np.arange(n), [0, 8, 13, 19], [5, 2, 18, 15]) + np.random.uniform(-1.5, 1.5, n)
pvc = np.interp(np.arange(n), [0, 10, 15, 19], [45, 45, 30, 28]) + np.random.uniform(-3, 3, n)
ps  = np.interp(np.arange(n), [0, 10, 15, 19], [35, 38, 18, 20]) + np.random.uniform(-2, 2, n)
abs_ = np.interp(np.arange(n), [0, 8, 15, 19], [15, 15, 8, 7]) + np.random.uniform(-1.5, 1.5, n)

# 防止负值
pp   = np.clip(pp,   0.2, None)
pe   = np.clip(pe,   0.2, None)
pvc  = np.clip(pvc,  0.2, None)
ps   = np.clip(ps,   0.2, None)
abs_ = np.clip(abs_, 0.2, None)

stack_raw = np.vstack([pp, pe, pvc, ps, abs_])

# 归一化为百分比，使每个体型组加总 = 100
stack_pct = stack_raw / stack_raw.sum(axis=0) * 100

pp, pe, pvc, ps, abs_ = stack_pct


# =========================================================
# 3. 构造右轴折线数据（摄入风险指数）
# =========================================================

# 蓝线：Mesopelagic index
mesopelagic = np.array([
    12.7, 7.2, 7.9, 8.1, 8.8, 9.5, 13.0, 13.0, 12.1, 10.7,
    11.4, 10.0, 7.5, 5.7, 8.6, 6.6, 5.2, 3.9, 3.2, 9.9
])

# 橙线：Epipelagic index
epipelagic = np.array([
    6.4, 5.9, 6.3, 5.5, 4.7, 4.1, 5.2, 4.7, 4.1, 3.5,
    5.0, 5.2, 4.6, 4.0, 8.9, 7.6, 6.2, 4.7, 4.5, 6.9
])

# 红线：Migratory index
migratory = np.array([
    3.6, 3.1, 3.2, 2.7, 2.4, 2.2, 2.6, 2.4, 2.2, 2.0,
    2.4, 2.5, 2.3, 2.2, 3.9, 3.5, 3.0, 2.4, 2.1, 2.1
])


# =========================================================
# 4. 绘图
# =========================================================

fig, ax1 = plt.subplots(figsize=(9.2, 5.7), dpi=300)

# ---------- 左轴：100%堆叠柱 ----------
bottom = np.zeros(n)

for label, values in zip(
    ["PP", "PE", "PVC", "PS", "ABS"],
    [pp, pe, pvc, ps, abs_]
):
    ax1.bar(
        x,
        values,
        bottom=bottom,
        width=0.66,
        color=plastic_colors[label],
        edgecolor="white",
        linewidth=0.5,
        label=label,
        zorder=2
    )
    bottom += values


# =========================================================
# 5. 左轴设置
# =========================================================

ax1.set_xlim(-0.6, n - 0.4)
ax1.set_ylim(0, 110)

ax1.set_ylabel(
    "Contribution ratio of different plastic types (%)",
    fontsize=13
)

ax1.set_xlabel(
    "Body size (mm)",
    fontsize=13,
    labelpad=10
)

ax1.set_xticks(x)
ax1.set_xticklabels([f"{v:,}" for v in body_sizes], fontsize=10)
ax1.set_yticks(np.arange(0, 101, 10))

ax1.tick_params(
    axis="x",
    direction="out",
    length=4,
    width=0.8,
    rotation=0
)

ax1.tick_params(
    axis="y",
    direction="out",
    length=4,
    width=0.8,
    labelsize=10
)

ax1.grid(False)


# =========================================================
# 6. 右轴：折线图
# =========================================================

ax2 = ax1.twinx()

ax2.plot(
    x, epipelagic,
    color="#ff7f00",
    marker="o",
    markersize=5,
    linewidth=2.2,
    label="Epipelagic index",
    zorder=5
)

ax2.plot(
    x, migratory,
    color="#d9481d",
    marker="^",
    markersize=5,
    linewidth=2.2,
    label="Migratory index",
    zorder=5
)

ax2.plot(
    x, mesopelagic,
    color="#2f5da8",
    marker="s",
    markersize=4.5,
    linewidth=3.0,
    label="Mesopelagic index",
    zorder=5
)

ax2.set_ylim(0, 13.8)
ax2.set_yticks(np.arange(1, 14, 1))
ax2.set_ylabel(
    "Ingestion risk index",
    fontsize=13,
    rotation=270,
    labelpad=18
)

ax2.tick_params(
    axis="y",
    direction="out",
    length=4,
    width=0.8,
    labelsize=10
)


# =========================================================
# 7. 边框样式
# =========================================================

for spine in ax1.spines.values():
    spine.set_linewidth(0.8)

for spine in ax2.spines.values():
    spine.set_linewidth(0.8)

ax1.spines["top"].set_visible(False)
ax2.spines["top"].set_visible(False)


# =========================================================
# 8. 图例（分两部分，尽量贴近原图）
# =========================================================

plastic_handles = [
    Patch(facecolor=plastic_colors[k], edgecolor="none", label=k)
    for k in ["PP", "PE", "PVC", "PS", "ABS"]
]

line_handles = [
    Line2D([0], [0], color="#ff7f00", marker="o", markersize=5, linewidth=1.5, label="Epipelagic index"),
    Line2D([0], [0], color="#d9481d", marker="^", markersize=5, linewidth=1.5, label="Migratory index"),
    Line2D([0], [0], color="#2f5da8", marker="s", markersize=3.5, linewidth=1.5, label="Mesopelagic index"),
]

legend1 = ax1.legend(
    handles=plastic_handles,
    loc="upper center",
    bbox_to_anchor=(0.73, -0.11),
    ncol=5,
    frameon=False,
    fontsize=10,
    handlelength=1.2,
    handletextpad=0.4,
    columnspacing=1.2
)

legend2 = ax1.legend(
    handles=line_handles,
    loc="upper center",
    bbox_to_anchor=(0.76, -0.18),
    ncol=2,
    frameon=False,
    fontsize=10,
    handlelength=1.2,
    handletextpad=0.5,
    columnspacing=1.3
)

ax1.add_artist(legend1)


# =========================================================
# 9. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "plastic_type_contribution_and_ingestion_risk.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "plastic_type_contribution_and_ingestion_risk.pdf",
    bbox_inches="tight"
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")