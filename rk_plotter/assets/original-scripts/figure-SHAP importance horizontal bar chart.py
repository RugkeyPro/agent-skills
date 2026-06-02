import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# 1. 示例数据
# =========================================================

features = [
    "Charge product",
    "MWCO",
    r"log K$_{ow}$",
    r"C$_{in}$",
    "IS",
    "Compound size",
    "Pressure",
    "WCA"
]

# 示例 SHAP importance，可理解为 mean(|SHAP value|)
importance = np.array([
    98,
    89,
    52,
    46,
    33,
    30,
    28,
    20
])


# =========================================================
# 2. 排序
#    原图中重要性最高的变量在最上方
# =========================================================

order = np.argsort(importance)
features_sorted = np.array(features)[order]
importance_sorted = importance[order]


# =========================================================
# 3. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(3.8, 3.1), dpi=300)

ax.barh(
    features_sorted,
    importance_sorted,
    height=0.70,
    color="#6470ff",
    edgecolor="#6470ff",
    linewidth=0.8
)


# =========================================================
# 4. 坐标轴设置
# =========================================================

ax.set_xlim(0, 105)

ax.set_xticks([0, 20, 40, 60, 80, 100])
ax.set_xticklabels([0, 20, 40, 60, 80, 100], fontsize=13)

ax.set_xlabel(
    "SHAP Importance",
    fontsize=18,
    labelpad=8
)

ax.tick_params(
    axis="y",
    labelsize=11,
    direction="in",
    length=3.5,
    width=1.0
)

ax.tick_params(
    axis="x",
    labelsize=13,
    direction="in",
    length=4,
    width=1.0
)

# 边框样式
for spine in ax.spines.values():
    spine.set_linewidth(1.4)

# 不显示网格，贴近原图
ax.grid(False)


# =========================================================
# 5. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "shap_importance_barplot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "shap_importance_barplot.pdf",
    bbox_inches="tight"
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")