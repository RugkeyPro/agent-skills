import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


# =========================================================
# 1. 构造示例数据
# =========================================================

np.random.seed(42)

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

n_samples = 260


def make_shap_distribution(feature_name, n):
    """
    构造不同变量的模拟 SHAP 值和变量值。
    variable_value 范围为 0-1，用于蓝-红着色。
    """
    v = np.random.rand(n)

    if feature_name == "Charge product":
        # 主要集中在正向，带有较长负向尾部
        shap = 2.0 * v + np.random.normal(0, 0.8, n)
        tail = np.random.choice(n, size=45, replace=False)
        shap[tail] -= np.random.uniform(4, 16, size=len(tail))

    elif feature_name == "MWCO":
        # 高变量值倾向于负 SHAP，低变量值倾向于正 SHAP
        shap = 3.0 * (0.5 - v) + np.random.normal(0, 1.0, n)
        tail = np.random.choice(n, size=35, replace=False)
        shap[tail] -= np.random.uniform(1, 7, size=len(tail))

    elif feature_name == r"log K$_{ow}$":
        shap = 2.8 * (v - 0.45) + np.random.normal(0, 0.8, n)
        tail = np.random.choice(n, size=25, replace=False)
        shap[tail] -= np.random.uniform(2, 6, size=len(tail))

    elif feature_name == r"C$_{in}$":
        shap = np.random.normal(0, 1.4, n)
        tail = np.random.choice(n, size=40, replace=False)
        shap[tail] -= np.random.uniform(2, 6, size=len(tail))

    elif feature_name == "IS":
        shap = 1.5 * (v - 0.4) + np.random.normal(0, 0.55, n)

    elif feature_name == "Compound size":
        shap = 1.2 * (v - 0.55) + np.random.normal(0, 0.75, n)
        tail = np.random.choice(n, size=35, replace=False)
        shap[tail] -= np.random.uniform(1.5, 5.5, size=len(tail))
        pos_tail = np.random.choice(n, size=8, replace=False)
        shap[pos_tail] += np.random.uniform(2, 6, size=len(pos_tail))

    elif feature_name == "Pressure":
        shap = np.random.normal(0.1, 0.55, n)
        tail = np.random.choice(n, size=18, replace=False)
        shap[tail] -= np.random.uniform(1, 4, size=len(tail))

    elif feature_name == "WCA":
        shap = 0.8 * (v - 0.5) + np.random.normal(0, 0.45, n)

    else:
        shap = np.random.normal(0, 1, n)

    shap = np.clip(shap, -18, 8)
    return shap, v


shap_data = {}
value_data = {}

for f in features:
    shap_data[f], value_data[f] = make_shap_distribution(f, n_samples)


# =========================================================
# 2. 绘图参数
# =========================================================

# 蓝-红色带，模拟 SHAP 默认配色
cmap = mpl.colors.LinearSegmentedColormap.from_list(
    "blue_red",
    ["#008bff", "#ff0051"],
    N=256
)

norm = mpl.colors.Normalize(vmin=0, vmax=1)

fig, ax = plt.subplots(figsize=(5.2, 3.3), dpi=300)


# =========================================================
# 3. 绘制 beeswarm 风格散点
# =========================================================

for i, feature in enumerate(features):
    # 为了让第一个变量在最上方，y 坐标反向
    y_center = len(features) - 1 - i

    shap_values = shap_data[feature]
    variable_values = value_data[feature]

    # 根据 SHAP 值局部密度生成纵向抖动，形成蜂群效果
    # 这里用简单随机抖动模拟，实际 shap.summary_plot 会更精细
    jitter_strength = 0.26
    y_jitter = np.random.normal(0, jitter_strength, size=n_samples)

    # 高密度区域略收紧
    y_jitter = np.clip(y_jitter, -0.33, 0.33)

    ax.scatter(
        shap_values,
        y_center + y_jitter,
        c=variable_values,
        cmap=cmap,
        norm=norm,
        s=9,
        alpha=0.9,
        edgecolor="none",
        zorder=3
    )


# =========================================================
# 4. 坐标轴与参考线
# =========================================================

# x = 0 参考线
ax.axvline(
    0,
    color="0.65",
    linewidth=1.0,
    zorder=1
)

ax.set_xlim(-18, 8.5)
ax.set_xticks([-15, -10, -5, 0, 5])
ax.set_xticklabels(["-15", "-10", "-5", "0", "5"], fontsize=15)

ax.set_yticks(np.arange(len(features)))
ax.set_yticklabels(features[::-1], fontsize=12)

ax.set_xlabel(
    "SHAP value",
    fontsize=19,
    labelpad=4
)

# 横向浅虚线网格
ax.grid(
    axis="y",
    linestyle=":",
    linewidth=0.6,
    color="0.85",
    alpha=0.8
)

ax.grid(False, axis="x")

# 只保留底部坐标轴，风格接近原图
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

ax.spines["bottom"].set_linewidth(0.9)
ax.spines["bottom"].set_color("0.45")

ax.tick_params(
    axis="y",
    length=0,
    pad=6
)

ax.tick_params(
    axis="x",
    direction="out",
    length=3.5,
    width=0.8
)


# =========================================================
# 5. 颜色条：Variable value
# =========================================================

sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])

cbar = plt.colorbar(
    sm,
    ax=ax,
    fraction=0.035,
    pad=0.055
)

cbar.set_ticks([])
cbar.outline.set_visible(False)

cbar.set_label(
    "Variable value",
    fontsize=14,
    rotation=270,
    labelpad=18
)

# High / Low 标注
cbar.ax.text(
    1.8,
    1.00,
    "High",
    transform=cbar.ax.transAxes,
    ha="left",
    va="center",
    fontsize=11
)

cbar.ax.text(
    1.8,
    0.00,
    "Low",
    transform=cbar.ax.transAxes,
    ha="left",
    va="center",
    fontsize=11
)


# =========================================================
# 6. 可选：左上角子图编号
# =========================================================

# 如果需要 a)，取消下面注释
# fig.text(
#     0.02, 0.98,
#     "a)",
#     fontsize=16,
#     fontweight="bold",
#     ha="left",
#     va="top"
# )


# =========================================================
# 7. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "shap_summary_beeswarm_template.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "shap_summary_beeswarm_template.pdf",
    bbox_inches="tight"
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")