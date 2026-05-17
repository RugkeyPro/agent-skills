import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


# =========================================================
# 1. 构造示例数据
# =========================================================

np.random.seed(42)

methods = [
    "CMOMS",
    "XGBoost",
    "MTGNN",
    "CrossFormer",
    "TSMixer",
    "iTransFormer",
    "PredRNN",
    "STIMP"
]

# 示例 MAE 数据
# 实际使用时可替换为每个模型在多个样本 / 多个站点 / 多个时间窗口上的 MAE
data = {
    "CMOMS":       np.clip(np.random.normal(0.27, 0.035, 35), 0.15, 0.36),
    "XGBoost":     np.clip(np.random.normal(0.25, 0.080, 35), 0.10, 0.45),
    "MTGNN":       np.clip(np.random.normal(0.24, 0.085, 35), 0.08, 0.45),
    "CrossFormer": np.clip(np.random.normal(0.23, 0.075, 35), 0.08, 0.42),
    "TSMixer":     np.clip(np.random.normal(0.24, 0.070, 35), 0.10, 0.42),
    "iTransFormer":np.clip(np.random.normal(0.26, 0.095, 35), 0.10, 0.52),
    "PredRNN":     np.clip(np.random.normal(0.22, 0.070, 35), 0.06, 0.36),
    "STIMP":       np.clip(np.random.normal(0.19, 0.065, 35), 0.04, 0.34),
}

plot_data = [data[m] for m in methods]


# =========================================================
# 2. 颜色设置
# =========================================================

colors = {
    "CMOMS":        "#ff8c00",
    "XGBoost":      "#9bbce6",
    "MTGNN":        "#86c7cf",
    "CrossFormer":  "#a8d5a6",
    "TSMixer":      "#f7c9a9",
    "iTransFormer": "#334969",
    "PredRNN":      "#66ad5e",
    "STIMP":        "#ff6f66",
}


# =========================================================
# 3. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(6.4, 3.9), dpi=300)

positions = np.arange(1, len(methods) + 1)

box = ax.boxplot(
    plot_data,
    positions=positions,
    widths=0.78,
    patch_artist=True,
    showmeans=True,
    showfliers=False,
    medianprops=dict(
        color="black",
        linewidth=1.1
    ),
    meanprops=dict(
        marker="^",
        markerfacecolor="#c9332c",
        markeredgecolor="black",
        markeredgewidth=0.35,
        markersize=4.0
    ),
    whiskerprops=dict(
        color="0.25",
        linewidth=1.1
    ),
    capprops=dict(
        color="0.25",
        linewidth=1.1
    )
)

# 箱体颜色
for patch, method in zip(box["boxes"], methods):
    patch.set_facecolor(colors[method])
    patch.set_alpha(0.65)
    patch.set_edgecolor("0.2")
    patch.set_linewidth(1.2)


# =========================================================
# 4. 坐标轴样式
# =========================================================

ax.set_ylabel(
    "mae",
    fontsize=12
)

ax.set_xlabel(
    "methods",
    fontsize=13,
    labelpad=0
)

ax.set_xlim(0.4, len(methods) + 0.6)
ax.set_ylim(0.02, 0.54)

# 原图中 x 轴不显示各模型名称，只用 legend 说明
ax.set_xticks(positions)
ax.set_xticklabels([""] * len(methods))

ax.set_yticks([0.1, 0.2, 0.3, 0.4, 0.5])
ax.set_yticklabels(["0.1", "0.2", "0.3", "0.4", "0.5"], fontsize=10)

ax.tick_params(
    axis="x",
    length=0
)

ax.tick_params(
    axis="y",
    direction="out",
    length=3.5,
    width=0.8,
    labelsize=10
)

# 浅灰网格
ax.grid(
    axis="y",
    color="0.86",
    linewidth=0.8,
    alpha=0.9
)

ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_linewidth(0.8)
    spine.set_color("0.75")


# =========================================================
# 5. 右侧图例
# =========================================================

legend_handles = [
    Patch(
        facecolor=colors[m],
        edgecolor="none",
        label=m
    )
    for m in methods
]

legend = ax.legend(
    handles=legend_handles,
    loc="center left",
    bbox_to_anchor=(1.03, 0.50),
    frameon=True,
    fontsize=11,
    borderpad=0.6,
    labelspacing=0.55,
    handlelength=1.4,
    handletextpad=0.6
)

# legend 字体加粗，贴近原图
for text in legend.get_texts():
    text.set_fontweight("bold")

legend.get_frame().set_edgecolor("0.85")
legend.get_frame().set_linewidth(1.0)
legend.get_frame().set_facecolor("white")


# =========================================================
# 6. 底部研究区标题
# =========================================================

fig.text(
    0.08,
    0.04,
    "Yangtze River Estuary",
    ha="left",
    va="center",
    fontsize=18,
    fontweight="bold"
)


# =========================================================
# 7. 保存图片
# =========================================================

plt.subplots_adjust(
    left=0.13,
    right=0.72,
    bottom=0.23,
    top=0.92
)

plt.savefig(
    "model_mae_boxplot_yangtze_river_estuary.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "model_mae_boxplot_yangtze_river_estuary.pdf",
    bbox_inches="tight"
)

plt.show()