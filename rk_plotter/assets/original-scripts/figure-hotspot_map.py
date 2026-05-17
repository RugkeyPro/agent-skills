import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.ndimage import gaussian_filter
import cartopy.crs as ccrs
import cartopy.feature as cfeature


# =========================================================
# 1. 基础参数设置
# =========================================================

np.random.seed(42)

# 全球经纬度网格
lon = np.linspace(-180, 180, 720)
lat = np.linspace(-60, 85, 360)
Lon, Lat = np.meshgrid(lon, lat)

# 热点值最大值，参考原图约 282.17
vmax = 282.17


# =========================================================
# 2. 构造随机/虚拟热点数据
#    思路：背景随机场 + 若干真实感热点中心
# =========================================================

def gaussian_hotspot(lon0, lat0, amp, sx=8, sy=5):
    """
    生成一个二维高斯热点
    lon0, lat0: 热点中心
    amp: 热点强度
    sx, sy: 经向和纬向扩散范围
    """
    return amp * np.exp(
        -(((Lon - lon0) ** 2) / (2 * sx ** 2)
          + ((Lat - lat0) ** 2) / (2 * sy ** 2))
    )


# 低强度背景值
hotspot = np.random.rand(*Lon.shape) * 12
hotspot = gaussian_filter(hotspot, sigma=4)

# 模拟全球濒危陆生脊椎动物热点区
# 可根据你的研究区或真实数据替换这些中心点
hotspot_centers = [
    # 中美洲、安第斯、加勒比
    (-90, 15, 180, 6, 4),
    (-78, 0, 230, 5, 8),
    (-72, -12, 140, 5, 7),

    # 西非、东非、马达加斯加
    (-5, 7, 90, 8, 5),
    (38, -3, 120, 5, 7),
    (47, -19, 170, 4, 7),

    # 南亚、东南亚、中国西南
    (78, 20, 210, 7, 5),
    (91, 25, 250, 6, 5),
    (101, 15, 240, 7, 6),
    (108, 5, 190, 6, 5),
    (121, 14, 130, 5, 5),

    # 新几内亚、澳洲东部
    (145, -6, 120, 6, 4),
    (150, -25, 80, 7, 5),

    # 地中海附近
    (15, 38, 80, 9, 4),
]

for lon0, lat0, amp, sx, sy in hotspot_centers:
    hotspot += gaussian_hotspot(lon0, lat0, amp, sx, sy)

# 平滑处理，让分布更像连续生态栅格
hotspot = gaussian_filter(hotspot, sigma=2)

# 归一化到 0 - vmax
hotspot = hotspot - np.nanmin(hotspot)
hotspot = hotspot / np.nanmax(hotspot) * vmax

# 低值略微压暗，突出热点
hotspot = hotspot ** 1.05


# =========================================================
# 3. 设置颜色映射
#    绿-黄-橙-红，类似原图
# =========================================================

colors = [
    "#2b8c5a",  # 深绿
    "#6fb96f",  # 绿
    "#d9ef8b",  # 黄绿
    "#fee08b",  # 黄
    "#f46d43",  # 橙红
    "#a50026",  # 深红
]

cmap = mpl.colors.LinearSegmentedColormap.from_list(
    "habitat_hotspot", colors, N=256
)

norm = mpl.colors.Normalize(vmin=0, vmax=vmax)


# =========================================================
# 4. 绘图
# =========================================================

fig = plt.figure(figsize=(13, 5.2), dpi=300)

# 主地图轴
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_global()
ax.set_extent([-180, 180, -60, 85], crs=ccrs.PlateCarree())

# 背景
ax.set_facecolor("white")

# 陆地底图
ax.add_feature(
    cfeature.LAND,
    facecolor="#e9e9e9",
    edgecolor="none",
    zorder=1
)

# 海岸线
ax.add_feature(
    cfeature.COASTLINE,
    linewidth=0.25,
    edgecolor="0.45",
    zorder=4
)

# 热点栅格
im = ax.imshow(
    hotspot,
    extent=[lon.min(), lon.max(), lat.min(), lat.max()],
    origin="lower",
    transform=ccrs.PlateCarree(),
    cmap=cmap,
    norm=norm,
    alpha=0.88,
    zorder=2
)

# 用海洋覆盖掉海上颜色，使其更接近“陆生脊椎动物”分布图
ax.add_feature(
    cfeature.OCEAN,
    facecolor="white",
    edgecolor="none",
    zorder=3
)

# 再加一次海岸线
ax.add_feature(
    cfeature.COASTLINE,
    linewidth=0.25,
    edgecolor="0.45",
    zorder=5
)

# 去掉经纬网、边框
ax.set_xticks([])
ax.set_yticks([])
ax.spines["geo"].set_visible(False)


# =========================================================
# 5. 左侧文字与色标
# =========================================================


# 左侧竖排分类标签
fig.text(
    0.065, 0.50,
    "Terrestrial vertebrates",
    rotation=90,
    fontsize=18,
    ha="center",
    va="center"
)

# 自定义色标位置
cax = fig.add_axes([0.105, 0.20, 0.026, 0.20])
cb = plt.colorbar(
    im,
    cax=cax,
    orientation="vertical"
)

cb.set_ticks([0, vmax])
cb.set_ticklabels(["0", f"{vmax:.2f}"])
cb.outline.set_visible(False)
cb.ax.tick_params(
    labelsize=13,
    length=0,
    pad=4
)

# 色标标题，竖排放置
fig.text(
    0.145, 0.30,
    "Hotspot\nvalue",
    rotation=270,
    fontsize=17,
    ha="center",
    va="center"
)


# =========================================================
# 6. 输出
# =========================================================

plt.subplots_adjust(left=0.08, right=0.99, top=0.96, bottom=0.04)

plt.savefig(
    "terrestrial_vertebrates_hotspot_map.png",
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.05
)

plt.savefig(
    "terrestrial_vertebrates_hotspot_map.pdf",
    bbox_inches="tight",
    pad_inches=0.05
)

plt.show()