import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# 1. 示例数据
# =========================================================

categories = ["Unprotected", "Protected"]
values = np.array([0.401, 0.599])   # 比例数据，范围 0–1

colors = ["#3d63d6", "#f23805"]     # 蓝色、红色


# =========================================================
# 2. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(3.1, 3.4), dpi=300)

bars = ax.bar(
    categories,
    values,
    width=0.90,
    color=colors,
    edgecolor="black",
    linewidth=1.0,
    zorder=3
)


# =========================================================
# 3. 添加柱顶百分比标签
# =========================================================

for bar, value in zip(bars, values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        value + 0.015,
        f"{value * 100:.1f}%",
        ha="center",
        va="bottom",
        fontsize=15
    )


# =========================================================
# 4. 坐标轴样式
# =========================================================

ax.set_ylabel(
    "Habitat proportion",
    fontsize=16,
    labelpad=8
)

ax.set_ylim(-0.04, 1.05)

ax.set_yticks([0, 0.25, 0.50, 0.75, 1.00])
ax.set_yticklabels(["0", "0.25", "0.50", "0.75", "1.00"], fontsize=12)

ax.tick_params(
    axis="x",
    labelsize=12,
    direction="out",
    length=4,
    width=0.8
)

ax.tick_params(
    axis="y",
    labelsize=12,
    direction="out",
    length=4,
    width=0.8
)

# 浅灰网格，接近示例图风格
ax.grid(
    True,
    axis="both",
    color="0.90",
    linewidth=0.7,
    alpha=0.7,
    zorder=0
)

for spine in ax.spines.values():
    spine.set_linewidth(0.8)

plt.tight_layout()


# =========================================================
# 5. 保存图片
# =========================================================

plt.savefig(
    "protected_unprotected_barplot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "protected_unprotected_barplot.pdf",
    bbox_inches="tight"
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")