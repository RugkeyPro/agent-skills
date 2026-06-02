import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# 1. 构造示例数据
# =========================================================

np.random.seed(42)

# 训练集真实值：集中在 65–100%
n_train = 150
real_train = np.random.uniform(62, 100, n_train)

# 测试集真实值：集中在 72–100%
n_test = 55
real_test = np.random.uniform(72, 100, n_test)

# 构造预测值：接近真实值，带一定误差
pred_train = real_train + np.random.normal(0, 5.2, n_train)
pred_test = real_test + np.random.normal(0, 5.8, n_test)

# 限制范围
pred_train = np.clip(pred_train, 0, 100)
pred_test = np.clip(pred_test, 0, 100)


# =========================================================
# 2. 评价指标函数
# =========================================================

def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


def mae(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))


train_rmse = rmse(real_train, pred_train)
train_mae = mae(real_train, pred_train)

test_rmse = rmse(real_test, pred_test)
test_mae = mae(real_test, pred_test)


# =========================================================
# 3. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(3.7, 3.7), dpi=300)

# 1:1 理想预测线
ax.plot(
    [0, 100],
    [0, 100],
    color="red",
    linewidth=1.2,
    zorder=1
)

# 训练集散点
ax.scatter(
    real_train,
    pred_train,
    s=28,
    color="#7f8df2",
    alpha=0.65,
    edgecolor="#5d66c8",
    linewidth=0.3,
    label="Training data",
    zorder=3
)

# 测试集散点
ax.scatter(
    real_test,
    pred_test,
    s=30,
    color="#ef7f6d",
    alpha=0.75,
    edgecolor="#cf5d4f",
    linewidth=0.3,
    label="Testing data",
    zorder=4
)


# =========================================================
# 4. 坐标轴设置
# =========================================================

ax.set_xlim(-10, 110)
ax.set_ylim(-10, 115)

ax.set_xticks([0, 25, 50, 75, 100])
ax.set_yticks([0, 25, 50, 75, 100])

ax.set_xlabel(
    "Real removal (%)",
    fontsize=22,
    labelpad=8
)

ax.set_ylabel(
    "Pred removal (%)",
    fontsize=22,
    labelpad=8
)

ax.tick_params(
    axis="both",
    direction="in",
    length=4,
    width=1.2,
    labelsize=17
)

for spine in ax.spines.values():
    spine.set_linewidth(1.6)

ax.grid(False)


# =========================================================
# 5. 标题与指标文字
# =========================================================

ax.set_title(
    "Transformer",
    fontsize=18,
    pad=10
)

metric_text = (
    f"Training RMSE: {train_rmse:.1f}%\n"
    f"Training MAE: {train_mae:.1f}%\n"
    f"RMSE: {test_rmse:.1f}%\n"
    f"MAE: {test_mae:.1f}%"
)

ax.text(
    0.04,
    0.96,
    metric_text,
    transform=ax.transAxes,
    ha="left",
    va="top",
    fontsize=12
)


# =========================================================
# 6. 图例
# =========================================================

ax.legend(
    loc="lower right",
    frameon=False,
    fontsize=14,
    handlelength=0.8,
    handletextpad=0.4,
    borderpad=0.2,
    labelspacing=0.4,
    markerscale=1.4
)


# =========================================================
# 7. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "transformer_predicted_vs_real_removal.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "transformer_predicted_vs_real_removal.pdf",
    bbox_inches="tight"
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")