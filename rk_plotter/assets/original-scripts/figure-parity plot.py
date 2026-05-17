import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# 1. 构造示例数据
# =========================================================

np.random.seed(42)

n_train = 257
n_test = 257

# 训练集：预测值集中在 0–2 附近，少量负值
pred_train = np.concatenate([
    np.random.normal(0.9, 0.65, int(n_train * 0.88)),
    np.random.normal(-0.8, 0.75, n_train - int(n_train * 0.88))
])

reported_train = (
    0.75 * pred_train
    + np.random.normal(0.15, 0.75, n_train)
)

# 测试集：噪声更大，相关性较弱
pred_test = np.concatenate([
    np.random.normal(1.0, 0.75, int(n_test * 0.90)),
    np.random.normal(-0.3, 0.70, n_test - int(n_test * 0.90))
])

reported_test = (
    0.45 * pred_test
    + np.random.normal(0.25, 1.00, n_test)
)

# 限制范围，使其接近示例图
pred_train = np.clip(pred_train, -6.5, 4.5)
reported_train = np.clip(reported_train, -7.2, 4.2)

pred_test = np.clip(pred_test, -6.5, 4.5)
reported_test = np.clip(reported_test, -7.2, 4.2)


# =========================================================
# 2. 评价指标函数
# =========================================================

def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


def mae(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))


def mdae(y_true, y_pred):
    return np.median(np.abs(y_true - y_pred))


def r2_score(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - ss_res / ss_tot


train_rmse = rmse(reported_train, pred_train)
train_mae = mae(reported_train, pred_train)
train_mdae = mdae(reported_train, pred_train)
train_r2 = r2_score(reported_train, pred_train)

test_rmse = rmse(reported_test, pred_test)
test_mae = mae(reported_test, pred_test)
test_mdae = mdae(reported_test, pred_test)
test_r2 = r2_score(reported_test, pred_test)


# =========================================================
# 3. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(6.2, 3.6), dpi=300)

# 训练集散点
ax.scatter(
    pred_train,
    reported_train,
    s=18,
    color="#0a8a8f",
    alpha=0.35,
    edgecolor="none",
    label="Training data"
)

# 测试集散点
ax.scatter(
    pred_test,
    reported_test,
    s=18,
    color="#4d5ee8",
    alpha=0.38,
    edgecolor="none",
    label="Test data (CV)"
)

# 1:1 参考线
ax.plot(
    [-7.5, 4.5],
    [-7.5, 4.5],
    linestyle=":",
    color="0.45",
    linewidth=1.3,
    zorder=1
)


# =========================================================
# 4. 坐标轴设置
# =========================================================

ax.set_xlim(-7.5, 4.5)
ax.set_ylim(-7.5, 4.5)

ax.set_xlabel(
    "predicted POD [log(mg/kg-d)]",
    fontsize=12
)

ax.set_ylabel(
    "reported POD [log(mg/kg-d)]",
    fontsize=12
)

ax.set_xticks([-6, -4, -2, 0, 2, 4])
ax.set_yticks([-6, -4, -2, 0, 2, 4])

ax.tick_params(
    axis="both",
    direction="out",
    length=7,
    width=1.6,
    labelsize=11
)

# 浅灰网格
ax.grid(
    True,
    color="0.80",
    linewidth=0.7,
    alpha=0.9
)

ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_linewidth(1.0)
    spine.set_color("0.35")


# =========================================================
# 5. 添加评价指标文字
# =========================================================

train_text = (
    "Training data\n"
    f"RMSE:   {train_rmse:5.3f}\n"
    f"MAE:    {train_mae:5.3f}\n"
    f"MdAE:   {train_mdae:5.3f}\n"
    f"R2:     {train_r2:5.3f}\n"
    f"n={n_train}"
)

test_text = (
    "Test data (CV)\n"
    f"RMSE:   {test_rmse:5.3f}\n"
    f"MAE:    {test_mae:5.3f}\n"
    f"MdAE:   {test_mdae:5.3f}\n"
    f"R2:     {test_r2:5.3f}\n"
    f"n={n_test}"
)

ax.text(
    -7.2,
    4.1,
    train_text,
    ha="left",
    va="top",
    fontsize=11,
    color="#008b8b",
    family="monospace"
)

ax.text(
    4.1,
    -2.0,
    test_text,
    ha="right",
    va="top",
    fontsize=11,
    color="blue",
    family="monospace"
)


# =========================================================
# 6. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "predicted_vs_reported_pod_scatter.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "predicted_vs_reported_pod_scatter.pdf",
    bbox_inches="tight"
)

plt.show()