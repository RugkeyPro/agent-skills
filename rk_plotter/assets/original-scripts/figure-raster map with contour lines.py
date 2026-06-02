import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.ndimage import gaussian_filter
import cartopy.crs as ccrs
import cartopy.feature as cfeature


# =========================================================
# 1. 基础设置
# =========================================================

np.random.seed(42)

# 全球经纬度网格
lon = np.linspace(-180, 180, 721)
lat = np.linspace(-89.5, 89.5, 360)
Lon, Lat = np.meshgrid(lon, lat)


# =========================================================
# 2. 构造模拟 SST 极端差值数据
#    代表：99 percentile in SST - mean SST (°C)
# =========================================================

def hotspot(lon0, lat0, amp, sx=20, sy=10):
    """二维高斯热点"""
    return amp * np.exp(
        -(((Lon - lon0) ** 2) / (2 * sx ** 2)
          + ((Lat - lat0) ** 2) / (2 * sy ** 2))
    )


# 背景场：中高纬和西边界流区域较高，热带开阔海域较低
sst_extreme = (
    2.2
    + 1.3 * np.exp(-((Lat - 40) / 22) ** 2)
    + 0.9 * np.exp(-((Lat + 35) / 25) ** 2)
    + 0.5 * np.cos(np.deg2rad(Lon * 1.2)) * np.cos(np.deg2rad(Lat))
)

# 北大西洋、北太平洋、南大洋等高值区
sst_extreme += hotspot(-40, 45, 3.0, 35, 14)     # 北大西洋
sst_extreme += hotspot(160, 42, 2.7, 35, 14)     # 北太平洋
sst_extreme += hotspot(20, 55, 2.2, 25, 10)      # 欧洲近海
sst_extreme += hotspot(-150, -45, 1.6, 45, 12)   # 南太平洋
sst_extreme += hotspot(60, -45, 1.4, 45, 12)     # 南印度洋
sst_extreme += hotspot(-30, -45, 1.3, 45, 12)    # 南大西洋

# 热带太平洋低值带
sst_extreme -= 1.3 * np.exp(-(Lat / 12) ** 2) * np.exp(-((Lon + 140) / 70) ** 2)

# 加入平滑随机扰动，模拟卫星栅格空间纹理
noise = gaussian_filter(np.random.normal(size=Lon.shape), sigma=7)
sst_extreme += 0.7 * noise

# 平滑处理
sst_extreme = gaussian_filter(sst_extreme, sigma=1.5)

# 限制范围到 0–10
sst_extreme = np.clip(sst_extreme, 0, 10)


# =========================================================
# 3. 离散色带设置
#    紫色 → 蓝色 → 青绿色 → 黄绿色 → 黄色
# =========================================================

levels = np.arange(0, 11, 1)

colors = [
    "#4b1d7a",  # 0–1
    "#40327f",  # 1–2
    "#31507f",  # 2–3
    "#22728a",  # 3–4
    "#1d8d8d",  # 4–5
    "#209c84",  # 5–6
    "#2da56d",  # 6–7
    "#62b955",  # 7–8
    "#a9d63a",  # 8–9
    "#f4e51c",  # 9–10
]

cmap = mpl.colors.ListedColormap(colors)
norm = mpl.colors.BoundaryNorm(levels, cmap.N)


# =========================================================
# 4. 绘制全球地图
# =========================================================

fig = plt.figure(figsize=(8.0, 5.2), dpi=300)

ax = plt.axes(projection=ccrs.Robinson())
ax.set_global()

# 海洋栅格
im = ax.pcolormesh(
    lon,
    lat,
    sst_extreme,
    cmap=cmap,
    norm=norm,
    shading="auto",
    transform=ccrs.PlateCarree(),
    zorder=1
)

# 黑色等值线
contour_levels = np.arange(1, 11, 1)

cs = ax.contour(
    lon,
    lat,
    sst_extreme,
    levels=contour_levels,
    colors="black",
    linewidths=0.8,
    alpha=0.9,
    transform=ccrs.PlateCarree(),
    zorder=3
)

# 陆地遮盖
ax.add_feature(
    cfeature.LAND,
    facecolor="#f2f2f2",
    edgecolor="black",
    linewidth=0.65,
    zorder=4
)

# 海岸线
ax.add_feature(
    cfeature.COASTLINE,
    edgecolor="black",
    linewidth=0.65,
    zorder=5
)

# 可选：国界，原图中不明显，默认不加
# ax.add_feature(
#     cfeature.BORDERS,
#     edgecolor="0.35",
#     linewidth=0.25,
#     zorder=5
# )

# 去掉经纬度刻度
ax.set_xticks([])
ax.set_yticks([])

# Robinson 投影外框
ax.spines["geo"].set_linewidth(0.8)
ax.spines["geo"].set_edgecolor("0.5")


# =========================================================
# 5. 标题与子图编号
# =========================================================

ax.set_title(
    "Satellite: 99 percentile in SST - mean SST(°C)",
    fontsize=15,
    pad=10
)

# 如果需要左上角 a，保留；不需要可以注释
fig.text(
    0.055,
    0.88,
    "a",
    fontsize=18,
    fontweight="bold",
    ha="left",
    va="center"
)


# =========================================================
# 6. 水平离散色标
# =========================================================

cbar = plt.colorbar(
    im,
    ax=ax,
    orientation="horizontal",
    fraction=0.065,
    pad=0.08,
    shrink=0.83,
    ticks=levels,
    boundaries=levels,
    spacing="proportional",
    drawedges=True
)

cbar.ax.tick_params(
    labelsize=13,
    length=0,
    width=0.8
)

cbar.outline.set_linewidth(0.8)

# 色块之间边界线
if cbar.solids is not None:
    cbar.solids.set_edgecolor("black")
    cbar.solids.set_linewidth(0.4)

cbar.set_ticklabels([str(i) for i in levels])


# =========================================================
# 7. 保存图片
# =========================================================

plt.savefig(
    "global_sst_99percentile_minus_mean.png",
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.04
)

plt.savefig(
    "global_sst_99percentile_minus_mean.pdf",
    bbox_inches="tight",
    pad_inches=0.04
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")