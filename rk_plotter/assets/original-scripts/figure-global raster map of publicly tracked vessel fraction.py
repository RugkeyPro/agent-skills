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

lon = np.linspace(-180, 180, 720)
lat = np.linspace(-60, 75, 360)
Lon, Lat = np.meshgrid(lon, lat)


# =========================================================
# 2. 构造模拟渔船活动强度
#    这里用热点 + 近岸带状分布模拟工业渔船活动
# =========================================================

def hotspot(lon0, lat0, amp, sx=8, sy=5):
    return amp * np.exp(
        -(((Lon - lon0) ** 2) / (2 * sx ** 2)
          + ((Lat - lat0) ** 2) / (2 * sy ** 2))
    )


activity = np.zeros_like(Lon, dtype=float)

# 全球主要渔业活动区模拟热点
hotspots = [
    # 东亚、东南亚
    (122, 32, 1.8, 8, 5),
    (138, 36, 1.6, 7, 5),
    (115, 20, 1.5, 9, 6),
    (105, 5, 1.6, 10, 6),
    (122, -5, 1.5, 10, 6),

    # 欧洲、北大西洋
    (-5, 50, 1.2, 12, 6),
    (10, 58, 1.1, 11, 5),
    (-20, 42, 1.0, 12, 6),

    # 美洲近海
    (-75, 35, 1.0, 10, 6),
    (-90, 25, 1.1, 9, 5),
    (-78, -10, 1.1, 8, 8),
    (-72, -35, 1.0, 8, 8),

    # 非洲与印度洋
    (-15, 15, 0.9, 12, 7),
    (40, -5, 0.8, 10, 7),
    (75, 12, 0.9, 10, 6),

    # 澳洲、新西兰
    (145, -35, 0.9, 10, 6),
    (170, -42, 0.8, 8, 5),
]

for h in hotspots:
    activity += hotspot(*h)

# 加入随机场，模拟细碎渔船轨迹分布
noise = gaussian_filter(np.random.random(Lon.shape), sigma=2)
activity += 0.25 * noise

# 让活动主要集中在中低纬和大陆边缘附近的视觉效果
lat_factor = (
    0.45
    + 0.45 * np.exp(-(Lat / 35) ** 2)
    + 0.15 * np.exp(-((Lat - 45) / 18) ** 2)
)
activity *= lat_factor

activity = gaussian_filter(activity, sigma=1.2)
activity = activity / activity.max()


# =========================================================
# 3. 构造“公开追踪比例”
#    数值范围 0–100%
# =========================================================

# 基础比例场
tracked_fraction = 50 + 40 * np.sin(np.deg2rad(Lon * 1.2)) * np.cos(np.deg2rad(Lat * 1.4))
tracked_fraction += 25 * gaussian_filter(np.random.normal(size=Lon.shape), sigma=10)

# 区域性偏差：东亚/东南亚偏低，欧洲偏高
tracked_fraction -= 35 * hotspot(125, 20, 1, 22, 16)
tracked_fraction -= 20 * hotspot(105, -5, 1, 18, 12)
tracked_fraction += 35 * hotspot(5, 55, 1, 25, 12)
tracked_fraction += 20 * hotspot(-20, 45, 1, 22, 10)

tracked_fraction = np.clip(tracked_fraction, 0, 100)

# 只显示有明显渔船活动的区域
display_field = np.where(activity > 0.24, tracked_fraction, np.nan)


# =========================================================
# 4. 配色：0% 红色，50% 浅色，100% 蓝色
# =========================================================

cmap = mpl.colors.LinearSegmentedColormap.from_list(
    "tracked_fraction",
    [
        (0.00, "#d4002f"),
        (0.25, "#f06b78"),
        (0.50, "#f1c0ad"),
        (0.75, "#5ab6d6"),
        (1.00, "#0077b6"),
    ],
    N=256
)

cmap.set_bad((1, 1, 1, 0))

norm = mpl.colors.Normalize(vmin=0, vmax=100)


# =========================================================
# 5. 绘图
# =========================================================

fig = plt.figure(figsize=(12.5, 6.8), dpi=300)

ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-180, 180, -58, 75], crs=ccrs.PlateCarree())

ax.set_facecolor("white")

# 灰色陆地
ax.add_feature(
    cfeature.LAND,
    facecolor="#f2f2f2",
    edgecolor="none",
    zorder=0
)

# 模拟渔船公开追踪比例
im = ax.pcolormesh(
    lon,
    lat,
    display_field,
    cmap=cmap,
    norm=norm,
    shading="auto",
    transform=ccrs.PlateCarree(),
    zorder=2,
    alpha=0.95
)

# 海岸线和国家边界
ax.add_feature(
    cfeature.COASTLINE,
    linewidth=0.45,
    edgecolor="0.70",
    zorder=4
)

ax.add_feature(
    cfeature.BORDERS,
    linewidth=0.25,
    edgecolor="0.82",
    zorder=4
)

# 用淡灰色线模拟海域统计单元 / EEZ 边界
for lon0 in np.arange(-170, 181, 20):
    ax.plot(
        [lon0, lon0 + 8, lon0 + 5, lon0 - 5, lon0],
        [-55, -25, 5, 35, 65],
        color="0.86",
        linewidth=0.35,
        alpha=0.65,
        transform=ccrs.PlateCarree(),
        zorder=1
    )


# =========================================================
# 6. 区域文字标注
# =========================================================

region_labels = [
    (-135, 35, "17%\npublicly\ntracked"),
    (-80, -20, "23%"),
    (5, 45, "61%"),
    (0, -5, "22%"),
    (82, 25, "22%"),
    (135, -32, "25%"),
]

for x, y, text in region_labels:
    ax.text(
        x,
        y,
        text,
        ha="center",
        va="center",
        fontsize=12,
        color="black",
        transform=ccrs.PlateCarree(),
        zorder=6
    )


# =========================================================
# 7. 标题
# =========================================================

ax.text(
    -177,
    72,
    "Industrial fishing vessels",
    ha="left",
    va="center",
    fontsize=13,
    transform=ccrs.PlateCarree(),
    zorder=6
)

# 如果需要左上角子图编号，可取消注释
# ax.text(
#     -180,
#     72,
#     "a",
#     ha="left",
#     va="center",
#     fontsize=15,
#     fontweight="bold",
#     transform=ccrs.PlateCarree(),
#     zorder=6
# )


# =========================================================
# 8. 坐标轴样式
# =========================================================

ax.set_xticks([])
ax.set_yticks([])

for spine in ax.spines.values():
    spine.set_visible(False)


# =========================================================
# 9. 水平色标
# =========================================================

cbar = plt.colorbar(
    im,
    ax=ax,
    orientation="horizontal",
    fraction=0.045,
    pad=0.08,
    shrink=0.45
)

cbar.set_label(
    "Fraction of vessels publicly tracked per km$^2$",
    fontsize=13,
    labelpad=8
)

cbar.set_ticks([0, 25, 50, 75, 100])
cbar.set_ticklabels(["0%", "25%", "50%", "75%", "100%"])

cbar.ax.tick_params(
    labelsize=12,
    length=5,
    width=0.8
)

cbar.outline.set_visible(False)


# =========================================================
# 10. 保存图片
# =========================================================

plt.savefig(
    "global_publicly_tracked_fishing_vessels.png",
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.03
)

plt.savefig(
    "global_publicly_tracked_fishing_vessels.pdf",
    bbox_inches="tight",
    pad_inches=0.03
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")