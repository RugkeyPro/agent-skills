import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# 1. 构造示例数据
# =========================================================

np.random.seed(42)

classes = [
    "Thiophosphoric acid esters",
    "Organothiophosphorus compounds",
    "Alkyl fluorides",
    "Thioureas",
    "Organosulfur compounds (S)",
    "Benzo-p-dioxins",
    "Isothiocyanates (G)",
    "Pyridinium derivatives",
    "Thiocyanates (C)",
    "Dithiocarbamic acid esters",
    "Dithiophosphate O-esters",
    "Thiocarbonic acid derivatives",
    "Thiazolines",
    "Pyrrolidinylpyridines",
    "Thiophenes",
    "Thiazolidines",
    "Thialdazoles",
    "Azathioprines",
    "Nitrogen mustard compounds",
    "Vinyl chlorides",
    "Hydrazines",
    "Transition metal nitrides",
    "Benzothiazepines (C)",
    "Isothiocyanates (C)",
    "Alkyl chlorides",
]

n_classes = len(classes)

# 为每类生成不确定性数据，整体集中在 2–4.5，带少量高值离群点
data = []

base_means = np.array([
    3.6, 3.4, 3.2, 2.8, 2.7,
    4.2, 3.0, 3.5, 2.8, 3.1,
    3.0, 2.8, 3.2, 2.9, 3.1,
    3.0, 3.3, 3.1, 2.9, 3.2,
    3.4, 2.9, 3.2, 3.1, 3.6
])

for i, mu in enumerate(base_means):
    n = np.random.randint(30, 80)
    sigma = np.random.uniform(0.25, 0.55)

    values = np.random.normal(mu, sigma, n)

    # 给部分类别添加右尾，使小提琴形状更真实
    if i in [5, 7, 16, 22]:
        tail = np.random.normal(mu + 1.2, 0.45, 8)
        values = np.concatenate([values, tail])

    values = np.clip(values, 1.6, 8.7)
    data.append(values)


# =========================================================
# 2. 颜色设置
# =========================================================

colors = [
    "#b5b6e6", "#d6c253", "#7eb6b4", "#f1b4bd", "#e6a2a9",
    "#c99b3f", "#e6c674", "#d1b064", "#d6a8c4", "#c5a6db",
    "#b5a1e6", "#dba9be", "#d6c15d", "#b39442", "#b0a56a",
    "#9faee7", "#caa446", "#b98d45", "#a7a3dc", "#c78cd5",
    "#9ec9d4", "#bca042", "#d5a744", "#d0a15b", "#7fa1b5"
]


# =========================================================
# 3. 开始绘图
# =========================================================

fig, ax = plt.subplots(figsize=(8.2, 6.0), dpi=300)

positions = np.arange(1, n_classes + 1)


# =========================================================
# 4. 小提琴图
# =========================================================

violins = ax.violinplot(
    data,
    positions=positions,
    widths=0.75,
    showmeans=False,
    showmedians=False,
    showextrema=False
)

for body, color in zip(violins["bodies"], colors):
    body.set_facecolor(color)
    body.set_edgecolor("none")
    body.set_alpha(0.75)


# =========================================================
# 5. 箱线图叠加
# =========================================================

box = ax.boxplot(
    data,
    positions=positions,
    widths=0.42,
    patch_artist=True,
    showfliers=False,
    medianprops=dict(
        color="black",
        linewidth=1.3
    ),
    boxprops=dict(
        facecolor="white",
        edgecolor="black",
        linewidth=1.0,
        alpha=0.75
    ),
    whiskerprops=dict(
        color="black",
        linewidth=1.0
    ),
    capprops=dict(
        color="black",
        linewidth=1.0
    )
)

# 给箱体填充半透明对应颜色
for patch, color in zip(box["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.45)


# =========================================================
# 6. 黑色样本点 / 离群点
# =========================================================

for x, values in zip(positions, data):
    # 抽取部分点作为黑色散点，模拟图中离群点/观测点
    q1, q3 = np.percentile(values, [25, 75])
    iqr = q3 - q1
    outlier_mask = (values < q1 - 1.5 * iqr) | (values > q3 + 1.5 * iqr)

    outliers = values[outlier_mask]

    # 如果离群点太少，额外抽几个高值点
    if len(outliers) < 3:
        extra = np.sort(values)[-3:]
        outliers = np.unique(np.concatenate([outliers, extra]))

    jitter = np.random.normal(0, 0.035, len(outliers))

    ax.scatter(
        np.full(len(outliers), x) + jitter,
        outliers,
        s=14,
        color="black",
        edgecolor="none",
        zorder=5
    )


# =========================================================
# 7. 坐标轴设置
# =========================================================

ax.set_xlim(0.4, n_classes + 0.6)
ax.set_ylim(0.8, 9.2)

ax.set_ylabel(
    "uncertainty (95% CI width)",
    fontsize=13
)

ax.set_xticks(positions)
ax.set_xticklabels(
    classes,
    rotation=90,
    ha="center",
    va="top",
    fontsize=11
)

ax.set_yticks([2, 4, 6, 8])
ax.set_yticklabels(["2", "4", "6", "8"], fontsize=12)

# 横向网格线
ax.grid(
    axis="y",
    color="0.82",
    linewidth=0.7,
    alpha=0.9
)

# 轻微纵向网格线
ax.grid(
    axis="x",
    color="0.90",
    linewidth=0.5,
    alpha=0.5
)

ax.set_axisbelow(True)


# =========================================================
# 8. 顶部短刻度
# =========================================================

ax.tick_params(
    axis="x",
    bottom=True,
    top=True,
    labelbottom=True,
    labeltop=False,
    direction="out",
    length=7,
    width=1.6
)

ax.tick_params(
    axis="y",
    direction="out",
    length=6,
    width=1.6
)

for spine in ax.spines.values():
    spine.set_linewidth(1.0)
    spine.set_color("0.25")


# =========================================================
# 9. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "uncertainty_violin_boxplot_by_chemical_class.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "uncertainty_violin_boxplot_by_chemical_class.pdf",
    bbox_inches="tight"
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")