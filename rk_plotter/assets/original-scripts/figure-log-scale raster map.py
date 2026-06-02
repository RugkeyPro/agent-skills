import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.ndimage import gaussian_filter
import cartopy.crs as ccrs
import cartopy.feature as cfeature


# =========================================================
# 1. 基础参数
# =========================================================

np.random.seed(42)

# 全球经纬度网格
lon = np.linspace(-180, 180, 720)
lat = np.linspace(-80, 85, 360)
Lon, Lat = np.meshgrid(lon, lat)


# =========================================================
# 2. 模拟“海洋塑料摄入风险”数据
#    单位参考原图：mol C m^-3 kg m^-3
# =========================================================

# 模拟不同海洋生物类型与体型参数
# 可根据研究对象替换，例如 fish / zooplankton / turtle / seabird
species_group = "fish"

species_factor = {
    "zooplankton": 1.40,
    "fish": 1.00,
    "turtle": 0.70,
    "seabird": 0.55,
    "mammal": 0.35,
}

# 体型参数：单位 kg
# 假设体型越大，单位体重塑料摄入风险相对降低
body_mass_kg = 0.2
body_size_factor = body_mass_kg ** (-0.25)

bio_factor = species_factor[species_group] * body_size_factor


# =========================================================
# 3. 构造空间风险场
# =========================================================

# 背景随机场
noise = np.random.rand(*Lon.shape)
noise = gaussian_filter(noise, sigma=8)

# 纬度梯度：中低纬海域风险较高，南大洋较低
lat_gradient = (
    0.55
    + 0.35 * np.exp(-(Lat / 35) ** 2)
    + 0.25 * np.exp(-((Lat - 35) / 20) ** 2)
)

# 模拟副热带环流聚集区
def hotspot(lon0, lat0, amp, sx=18, sy=10):
    return amp * np.exp(
        -(((Lon - lon0) ** 2) / (2 * sx ** 2)
          + ((Lat - lat0) ** 2) / (2 * sy ** 2))
    )

risk_pattern = (
    0.45 * noise
    + lat_gradient
    + hotspot(-145, 30, 1.2, 24, 11)   # 北太平洋
    + hotspot(-40, 35, 1.0, 22, 10)     # 北大西洋
    + hotspot(70, 15, 0.9, 24, 12)      # 印度洋
    + hotspot(115, -15, 0.9, 28, 12)    # 印尼—澳洲附近
    + hotspot(-15, -25, 0.7, 25, 12)    # 南大西洋
    + hotspot(-110, -25, 0.8, 26, 12)   # 南太平洋
)

# 加入近岸带状高风险结构
coastal_like = (
    0.35 * np.exp(-((Lat - 20) / 18) ** 2)
    * (0.5 + 0.5 * np.sin(np.deg2rad(Lon * 2.5)))
)

risk_pattern += coastal_like

# 平滑
risk_pattern = gaussian_filter(risk_pattern, sigma=2)

# 归一化到 0–1
risk_pattern = risk_pattern - risk_pattern.min()
risk_pattern = risk_pattern / risk_pattern.max()

# 映射到对数风险范围：10^-14 到 10^-10
log_min = -14
log_max = -10

log_risk = log_min + risk_pattern * (log_max - log_min)

# 加入生物体型与种类影响
log_risk = log_risk + np.log10(bio_factor)

risk = 10 ** log_risk

# 限制到色标范围
risk = np.clip(risk, 1e-14, 1e-10)


# =========================================================
# 4. 设置颜色映射
#    蓝 → 青 → 黄 → 橙 → 红 → 紫，接近原图
# =========================================================

colors = [
    "#2b008f",  # 深蓝紫
    "#0047ff",  # 蓝
    "#00c7ff",  # 青
    "#ffff66",  # 黄
    "#ffb000",  # 橙
    "#ff0000",  # 红
    "#8e008e",  # 紫
]

cmap = mpl.colors.LinearSegmentedColormap.from_list(
    "plastic_ingestion_risk",
    colors,
    N=256
)

norm = mpl.colors.LogNorm(vmin=1e-14, vmax=1e-10)


# =========================================================
# 5. 绘制全球地图
# =========================================================

fig = plt.figure(figsize=(7.0, 4.0), dpi=300)

ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-180, 180, -75, 85], crs=ccrs.PlateCarree())

# 海洋底色
ax.set_facecolor("white")

# 风险栅格
im = ax.pcolormesh(
    lon,
    lat,
    risk,
    cmap=cmap,
    norm=norm,
    shading="auto",
    transform=ccrs.PlateCarree(),
    zorder=1
)

# 陆地白色掩膜
ax.add_feature(
    cfeature.LAND,
    facecolor="white",
    edgecolor="black",
    linewidth=0.45,
    zorder=3
)

# 海岸线
ax.add_feature(
    cfeature.COASTLINE,
    linewidth=0.45,
    edgecolor="black",
    zorder=4
)

# 国界可选，原图主要是海岸线，不建议太重
ax.add_feature(
    cfeature.BORDERS,
    linewidth=0.20,
    edgecolor="black",
    alpha=0.55,
    zorder=4
)

# 坐标轴外框
ax.set_xticks([])
ax.set_yticks([])

for spine in ax.spines.values():
    spine.set_linewidth(0.8)
    spine.set_edgecolor("black")


# =========================================================
# 6. 水平对数色标
# =========================================================

cbar = plt.colorbar(
    im,
    ax=ax,
    orientation="horizontal",
    fraction=0.09,
    pad=0.10,
    shrink=0.94,
    extend="both"
)

cbar.set_label(
    "Ingestion risk (mol C m$^{-3}$ kg m$^{-3}$)",
    fontsize=11,
    labelpad=7
)

cbar.set_ticks([1e-14, 1e-13, 1e-12, 1e-11, 1e-10])
cbar.set_ticklabels([
    r"$10^{-14}$",
    r"$10^{-13}$",
    r"$10^{-12}$",
    r"$10^{-11}$",
    r"$10^{-10}$"
])

cbar.ax.tick_params(
    labelsize=9,
    length=3,
    width=0.7
)

cbar.outline.set_linewidth(0.8)


# =========================================================
# 7. 保存图片
# =========================================================

plt.savefig(
    "global_plastic_ingestion_risk_map.png",
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.04
)

plt.savefig(
    "global_plastic_ingestion_risk_map.pdf",
    bbox_inches="tight",
    pad_inches=0.04
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")