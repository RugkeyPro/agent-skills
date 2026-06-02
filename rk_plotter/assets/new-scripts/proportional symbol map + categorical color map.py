import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import cartopy.crs as ccrs
import cartopy.feature as cfeature


# =========================================================
# 1. 构造示例点数据
# =========================================================

np.random.seed(42)

def make_cluster(lon0, lat0, n, lon_sd=10, lat_sd=6):
    lon = np.random.normal(lon0, lon_sd, n)
    lat = np.random.normal(lat0, lat_sd, n)
    return lon, lat


clusters = [
    # North America
    (-105, 50, 420, 18, 8),
    (-95, 35, 240, 13, 7),

    # South America
    (-60, -15, 300, 14, 12),
    (-70, -40, 120, 8, 7),

    # Europe
    (10, 50, 260, 14, 7),

    # Africa
    (20, 5, 360, 18, 16),
    (30, -25, 130, 10, 8),

    # Asia
    (75, 28, 420, 16, 10),
    (105, 35, 360, 16, 9),
    (110, 15, 180, 13, 7),

    # Australia
    (135, -25, 180, 12, 8),

    # High latitude Eurasia / Canada
    (80, 58, 260, 30, 6),
    (-120, 60, 220, 24, 5),
]

lon_all = []
lat_all = []

for lon0, lat0, n, lon_sd, lat_sd in clusters:
    lon, lat = make_cluster(lon0, lat0, n, lon_sd, lat_sd)
    lon_all.append(lon)
    lat_all.append(lat)

lon_all = np.concatenate(lon_all)
lat_all = np.concatenate(lat_all)

# 限制在图幅内
mask = (
    (lon_all >= -180) & (lon_all <= 180) &
    (lat_all >= -60) & (lat_all <= 75)
)

lon_all = lon_all[mask]
lat_all = lat_all[mask]

n_points = len(lon_all)

# 面积数据，单位 km²，使用对数分布更接近实际地理斑块面积
area = 10 ** np.random.uniform(0, 4, n_points)

# Drawdown area ratio，单位 %
# 构造一个空间上有高低差异的模拟值
ratio = (
    15
    + 25 * np.exp(-((lat_all - 25) / 25) ** 2)
    + 20 * np.sin(np.deg2rad(lon_all * 1.6)) ** 2
    + np.random.normal(0, 12, n_points)
)

ratio = np.clip(ratio, 0.1, 100)

df = pd.DataFrame({
    "lon": lon_all,
    "lat": lat_all,
    "area_km2": area,
    "drawdown_ratio": ratio
})


# =========================================================
# 2. 面积映射为圆圈大小
# =========================================================

def size_from_area(a):
    """
    将面积 km² 映射为 scatter 的面积大小 points²
    """
    a = np.asarray(a)
    return np.interp(
        np.log10(a),
        [0, 1, 2, 3, 4],
        [5, 10, 24, 55, 105]
    )


df["marker_size"] = size_from_area(df["area_km2"])


# =========================================================
# 3. Drawdown area ratio 分级配色
# =========================================================

ratio_bins = [0, 5, 10, 20, 50, 100]

ratio_labels = [
    "<5",
    "5–10",
    "10–20",
    "20–50",
    "50–100"
]

ratio_colors = [
    "#4f7fb9",  # <5 蓝
    "#a9c3d0",  # 5–10 浅蓝灰
    "#f3f1b2",  # 10–20 浅黄
    "#f4a56d",  # 20–50 橙
    "#df3f2f",  # 50–100 红
]

df["ratio_class"] = pd.cut(
    df["drawdown_ratio"],
    bins=ratio_bins,
    labels=ratio_labels,
    include_lowest=True
)

color_map = dict(zip(ratio_labels, ratio_colors))
df["color"] = df["ratio_class"].map(color_map)


# =========================================================
# 4. 绘制全球地图
# =========================================================

fig = plt.figure(figsize=(12.5, 5.4), dpi=300)

ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-180, 180, -60, 75], crs=ccrs.PlateCarree())

# 背景
ax.set_facecolor("white")

# 陆地底图
ax.add_feature(
    cfeature.LAND,
    facecolor="#f1f1f1",
    edgecolor="0.35",
    linewidth=0.45,
    zorder=0
)

ax.add_feature(
    cfeature.COASTLINE,
    edgecolor="0.25",
    linewidth=0.45,
    zorder=2
)

ax.add_feature(
    cfeature.BORDERS,
    edgecolor="0.55",
    linewidth=0.25,
    zorder=2
)

# 绘制气泡
for label in ratio_labels:
    sub = df[df["ratio_class"] == label]

    ax.scatter(
        sub["lon"],
        sub["lat"],
        s=sub["marker_size"],
        facecolor=color_map[label],
        edgecolor=color_map[label],
        linewidth=0.8,
        alpha=0.35,
        transform=ccrs.PlateCarree(),
        zorder=3
    )


# =========================================================
# 5. 经纬度刻度样式
# =========================================================

ax.set_xticks([-120, -60, 0, 60, 120, 180], crs=ccrs.PlateCarree())
ax.set_yticks([-60, -30, 0, 30, 60], crs=ccrs.PlateCarree())

ax.set_xticklabels(
    ["120°W", "60°W", "0°", "60°E", "120°E", "180"],
    fontsize=12,
    fontweight="bold"
)

ax.set_yticklabels(
    ["60°S", "30°S", "0°", "30°N", "60°N"],
    fontsize=12,
    fontweight="bold",
    rotation=90,
    va="center"
)

# x 轴刻度放到顶部
ax.tick_params(
    axis="x",
    labeltop=True,
    labelbottom=False,
    top=True,
    bottom=False,
    direction="out",
    length=4,
    width=1.0
)

ax.tick_params(
    axis="y",
    left=True,
    right=False,
    direction="out",
    length=4,
    width=1.0
)

for spine in ax.spines.values():
    spine.set_linewidth(1.0)
    spine.set_edgecolor("black")


# =========================================================
# 6. 左上角子图编号
# =========================================================

fig.text(
    0.055,
    0.92,
    "a",
    fontsize=18,
    fontweight="bold",
    ha="left",
    va="center"
)


# =========================================================
# 7. 面积图例：Area (km²)
# =========================================================

area_legend_values = [5, 50, 500, 2000]
area_legend_labels = ["1–10", "10–100", "100–1000", ">1000"]

area_handles = []

for val, lab in zip(area_legend_values, area_legend_labels):
    handle = Line2D(
        [0],
        [0],
        marker="o",
        linestyle="none",
        markerfacecolor="white",
        markeredgecolor="black",
        markeredgewidth=1.0,
        markersize=np.sqrt(size_from_area(val)),
        label=lab
    )
    area_handles.append(handle)

legend_area = ax.legend(
    handles=area_handles,
    title="Area (km²)",
    loc="lower center",
    bbox_to_anchor=(0.56, 0.09),
    ncol=4,
    frameon=False,
    fontsize=10,
    title_fontsize=10,
    handlelength=1.0,
    handletextpad=0.7,
    columnspacing=1.2,
    borderpad=0.2
)

legend_area.get_title().set_fontweight("bold")
ax.add_artist(legend_area)


# =========================================================
# 8. 颜色图例：Drawdown area ratio (%)
# =========================================================

ratio_handles = [
    Patch(
        facecolor=c,
        edgecolor="black",
        linewidth=0.4,
        label=l
    )
    for l, c in zip(ratio_labels, ratio_colors)
]

legend_ratio = ax.legend(
    handles=ratio_handles,
    title="Drawdown area ratio (%)",
    loc="lower center",
    bbox_to_anchor=(0.54, 0.005),
    ncol=5,
    frameon=False,
    fontsize=10,
    title_fontsize=10,
    handlelength=1.8,
    handleheight=0.9,
    handletextpad=0.5,
    columnspacing=1.0,
    borderpad=0.2
)

legend_ratio.get_title().set_fontweight("bold")


# =========================================================
# 9. 保存图片
# =========================================================

plt.savefig(
    "global_drawdown_area_ratio_bubble_map.png",
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.04
)

plt.savefig(
    "global_drawdown_area_ratio_bubble_map.pdf",
    bbox_inches="tight",
    pad_inches=0.04
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")