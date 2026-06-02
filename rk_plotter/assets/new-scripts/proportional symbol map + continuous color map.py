import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.lines import Line2D
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader


# =========================================================
# 1. 构造示例湖泊点数据
# =========================================================

np.random.seed(42)

def make_cluster(lon0, lat0, n, lon_sd=2.5, lat_sd=1.5):
    lon = np.random.normal(lon0, lon_sd, n)
    lat = np.random.normal(lat0, lat_sd, n)
    return lon, lat


# 模拟中国主要湖泊分布区
clusters = [
    # 青藏高原
    (88, 33, 55, 4.5, 2.2),
    (92, 36, 45, 3.5, 1.5),
    (82, 34, 22, 2.5, 1.4),

    # 云贵高原
    (102, 25, 18, 2.2, 1.5),

    # 长江中下游
    (113, 30, 45, 3.0, 1.2),
    (119, 32, 25, 2.2, 1.0),

    # 华北、东北
    (116, 40, 28, 3.5, 2.0),
    (124, 46, 24, 3.0, 2.0),

    # 新疆、内蒙古
    (84, 45, 12, 3.0, 2.2),
    (112, 43, 18, 3.5, 2.0),

    # 华南
    (111, 24, 12, 2.0, 1.2),
]

lon_list = []
lat_list = []

for lon0, lat0, n, lon_sd, lat_sd in clusters:
    lon, lat = make_cluster(lon0, lat0, n, lon_sd, lat_sd)
    lon_list.append(lon)
    lat_list.append(lat)

lon = np.concatenate(lon_list)
lat = np.concatenate(lat_list)

# 限制在中国图幅范围内
mask = (
    (lon >= 73) & (lon <= 134) &
    (lat >= 18) & (lat <= 54)
)

lon = lon[mask]
lat = lat[mask]
n = len(lon)

# 湖泊面积，单位 km²，使用对数分布模拟
lake_area = 10 ** np.random.uniform(1.5, 3.6, n)

# 效率指标，单位 °C/10 km
# 这里人为设置西部和高原区较高，东部较低
efficiency = (
    0.25
    + 0.75 * np.exp(-((lon - 88) / 10) ** 2)
    + 0.45 * np.exp(-((lat - 33) / 7) ** 2)
    + 0.25 * np.random.random(n)
)

efficiency = np.clip(efficiency, 0, 2.0)


# =========================================================
# 2. 点大小映射函数
# =========================================================

def size_from_area(area):
    """
    将湖泊面积映射为 scatter 的面积大小，单位 points²
    """
    area = np.asarray(area)

    return np.interp(
        np.log10(area),
        [1.5, 2.0, 2.7, 3.0, 3.3, 3.6],
        [30, 45, 75, 110, 160, 230]
    )


sizes = size_from_area(lake_area)


# =========================================================
# 3. 颜色映射
# =========================================================

colors = [
    "#f3f5b0",
    "#d8efaa",
    "#aee0b1",
    "#74c6b8",
    "#39a6bf",
    "#2073b2",
    "#24368f",
]

cmap = mpl.colors.LinearSegmentedColormap.from_list(
    "efficiency_cmap",
    colors,
    N=256
)

norm = mpl.colors.Normalize(vmin=0, vmax=2.0)


# =========================================================
# 4. 读取中国边界
# =========================================================

country_shp = shpreader.natural_earth(
    resolution="10m",
    category="cultural",
    name="admin_0_countries"
)

country_records = list(shpreader.Reader(country_shp).records())

china_geoms = []
for rec in country_records:
    name = rec.attributes.get("ADMIN", "")
    if name in ["China", "Taiwan"]:
        china_geoms.append(rec.geometry)

# 省级边界
province_shp = shpreader.natural_earth(
    resolution="10m",
    category="cultural",
    name="admin_1_states_provinces_lines"
)


# =========================================================
# 5. 主图
# =========================================================

fig = plt.figure(figsize=(8.0, 5.6), dpi=300)

ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([73, 135, 18, 55], crs=ccrs.PlateCarree())

# 背景
ax.set_facecolor("white")

# 陆地和海洋
ax.add_feature(
    cfeature.OCEAN,
    facecolor="white",
    edgecolor="none",
    zorder=0
)

ax.add_feature(
    cfeature.LAND,
    facecolor="white",
    edgecolor="none",
    zorder=0
)

# 中国边界
for geom in china_geoms:
    ax.add_geometries(
        [geom],
        crs=ccrs.PlateCarree(),
        facecolor="white",
        edgecolor="black",
        linewidth=1.5,
        zorder=2
    )

# 省界
ax.add_geometries(
    shpreader.Reader(province_shp).geometries(),
    crs=ccrs.PlateCarree(),
    facecolor="none",
    edgecolor="0.75",
    linewidth=0.5,
    zorder=3
)

# 湖泊点
sc = ax.scatter(
    lon,
    lat,
    s=sizes,
    c=efficiency,
    cmap=cmap,
    norm=norm,
    edgecolor="black",
    linewidth=0.8,
    alpha=0.92,
    transform=ccrs.PlateCarree(),
    zorder=5
)


# =========================================================
# 6. 经纬度刻度
# =========================================================

ax.set_xticks([80, 90, 100, 110, 120, 130], crs=ccrs.PlateCarree())
ax.set_yticks([20, 30, 40, 50], crs=ccrs.PlateCarree())

ax.set_xticklabels(
    ["80°E", "90°E", "100°E", "110°E", "120°E", "130°E"],
    fontsize=11
)

ax.set_yticklabels(
    ["20°N", "30°N", "40°N", "50°N"],
    fontsize=11
)

ax.tick_params(
    axis="both",
    direction="out",
    length=4,
    width=1.0
)

for spine in ax.spines.values():
    spine.set_linewidth(1.2)
    spine.set_color("black")


# =========================================================
# 7. 左上角子图编号
# =========================================================

ax.text(
    0.02,
    0.97,
    "(d)",
    transform=ax.transAxes,
    ha="left",
    va="top",
    fontsize=20,
    fontweight="bold"
)

# 如果不需要编号，删除上面 ax.text(...) 即可。


# =========================================================
# 8. 湖泊面积图例
# =========================================================

area_legend_values = [80, 300, 750, 1500, 2600]
area_legend_labels = [
    "<100",
    "100–500",
    "500–1000",
    "1000–2000",
    ">2000"
]

area_handles = [
    Line2D(
        [0],
        [0],
        marker="o",
        linestyle="none",
        markerfacecolor="white",
        markeredgecolor="black",
        markeredgewidth=1.0,
        markersize=np.sqrt(size_from_area(v)),
        label=lab
    )
    for v, lab in zip(area_legend_values, area_legend_labels)
]

area_legend = ax.legend(
    handles=area_handles,
    title="Lake area (km$^2$)",
    loc="lower left",
    bbox_to_anchor=(0.02, 0.08),
    frameon=False,
    fontsize=9,
    title_fontsize=10,
    handlelength=1.2,
    handletextpad=0.7,
    labelspacing=0.55,
    borderpad=0.2
)

ax.add_artist(area_legend)


# =========================================================
# 9. 右侧颜色条
# =========================================================

cbar = plt.colorbar(
    sc,
    ax=ax,
    orientation="vertical",
    fraction=0.045,
    pad=0.03
)

cbar.set_label(
    "Efficiency\n(°C/10 km)",
    fontsize=12,
    fontweight="bold",
    rotation=0,
    labelpad=18,
    y=1.05
)

cbar.set_ticks(np.arange(0, 2.01, 0.2))
cbar.ax.tick_params(
    labelsize=9,
    length=3,
    width=0.8
)

cbar.outline.set_linewidth(1.0)


# =========================================================
# 10. 南海诸岛 inset 小图
# =========================================================

inset_ax = fig.add_axes(
    [0.69, 0.18, 0.16, 0.18],
    projection=ccrs.PlateCarree()
)

inset_ax.set_extent([105, 125, 3, 24], crs=ccrs.PlateCarree())
inset_ax.set_facecolor("white")

inset_ax.add_feature(
    cfeature.LAND,
    facecolor="white",
    edgecolor="black",
    linewidth=0.7,
    zorder=1
)

inset_ax.add_feature(
    cfeature.COASTLINE,
    edgecolor="black",
    linewidth=0.6,
    zorder=2
)

for geom in china_geoms:
    inset_ax.add_geometries(
        [geom],
        crs=ccrs.PlateCarree(),
        facecolor="none",
        edgecolor="black",
        linewidth=0.7,
        zorder=3
    )

inset_ax.set_xticks([])
inset_ax.set_yticks([])

for spine in inset_ax.spines.values():
    spine.set_linewidth(1.0)
    spine.set_color("black")


# =========================================================
# 11. 保存图片
# =========================================================

plt.savefig(
    "china_lake_efficiency_bubble_map.png",
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.04
)

plt.savefig(
    "china_lake_efficiency_bubble_map.pdf",
    bbox_inches="tight",
    pad_inches=0.04
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")