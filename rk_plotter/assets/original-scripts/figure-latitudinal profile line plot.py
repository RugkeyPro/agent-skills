import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# 1. 构造示例纬度数据
# =========================================================

np.random.seed(42)

lat = np.linspace(-80, 80, 400)


# =========================================================
# 2. 构造三条示例曲线
#    这里只是模拟形状，后续可替换为真实数据
# =========================================================

def gaussian(x, mu, sigma, amp=1.0):
    return amp * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))

# Ingestible plastic：在低纬和北半球中高纬有峰值
plastic = (
    gaussian(lat, -30, 12, 0.70) +
    gaussian(lat,  35, 15, 0.90) +
    gaussian(lat,  55, 10, 0.55)
)

# Organism biomass：北半球高纬偏高，也在热带有一定值
biomass = (
    gaussian(lat, 60, 14, 1.00) +
    gaussian(lat, 15, 18, 0.70) +
    gaussian(lat, -5, 18, 0.35)
)

# Ingestion risk：综合前两者，并加一些起伏
risk = (
    0.55 * plastic +
    0.45 * biomass +
    0.10 * np.sin(np.deg2rad(lat * 8)) +
    0.06 * np.sin(np.deg2rad(lat * 20))
)

# 保证非负
plastic = np.clip(plastic, 0, None)
biomass = np.clip(biomass, 0, None)
risk = np.clip(risk, 0, None)

# 归一化到 0–1，便于画在同一横轴上
def normalize(x):
    x = np.asarray(x)
    return (x - x.min()) / (x.max() - x.min())

plastic = normalize(plastic)
biomass = normalize(biomass)
risk = normalize(risk)


# =========================================================
# 3. 绘图
# =========================================================

fig, ax = plt.subplots(figsize=(2.2, 3.0), dpi=300)

ax.plot(
    risk, lat,
    color="#4c9be8",
    linewidth=1.1,
    label="Ingestion risk"
)

ax.plot(
    biomass, lat,
    color="#ff8c33",
    linewidth=1.0,
    label="Organism biomass"
)

ax.plot(
    plastic, lat,
    color="#a020b0",
    linewidth=1.0,
    label="Ingestible plastic"
)


# =========================================================
# 4. 坐标轴样式
# =========================================================

ax.set_ylim(-80, 80)
ax.set_xlim(0, 1.05)

# 纵轴纬度刻度
ax.set_yticks([-60, -30, 0, 30, 60])
ax.set_yticklabels(
    ["60° S", "30° S", "0°", "30° N", "60° N"],
    fontsize=9
)

# 原图几乎不显示横轴刻度，可隐藏
ax.set_xticks([])

ax.tick_params(
    axis="y",
    direction="in",
    length=3,
    width=0.8,
    labelsize=9
)

ax.tick_params(
    axis="x",
    length=0
)

for spine in ax.spines.values():
    spine.set_linewidth(0.8)

ax.grid(False)


# =========================================================
# 5. 图例放在下方
# =========================================================

ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.06),
    frameon=False,
    ncol=1,
    fontsize=9,
    handlelength=1.1,
    handletextpad=0.4,
    borderpad=0.1,
    labelspacing=0.35
)


# =========================================================
# 6. 保存图片
# =========================================================

plt.tight_layout()

plt.savefig(
    "latitudinal_profile_ingestion_risk.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "latitudinal_profile_ingestion_risk.pdf",
    bbox_inches="tight"
)

plt.show()