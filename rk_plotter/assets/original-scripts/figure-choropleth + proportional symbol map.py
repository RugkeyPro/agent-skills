import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.lines import Line2D
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader


# =========================================================
# 1. 随机种子
# =========================================================
np.random.seed(42)


# =========================================================
# 2. 读取全球底图（演示用：国家边界代替流域边界）
#    如果后续你有真实流域 shp，可直接替换这里
# =========================================================
shp_path = shpreader.natural_earth(
    resolution="110m",
    category="cultural",
    name="admin_0_countries"
)

reader = shpreader.Reader(shp_path)
records = list(reader.records())


# =========================================================
# 3. 为每个多边形随机生成 MeHg export
#    范围参考原图：约 0.01 ~ 1000+
#    使用对数分布更接近此类环境数据
# =========================================================
export_dict = {}

for rec in records:
    name = rec.attributes["NAME_LONG"]
    if name == "Antarctica":
        continue

    # 在 log10 空间随机，模拟 0.01 到 3000
    val = 10 ** np.random.uniform(-2, 3.4)
    export_dict[name] = val


# =========================================================
# 4. 构造随机的流域气泡点（MeHg yield）
#    为了更接近原图，用多个区域聚类生成
# =========================================================

def cluster_points(center_lon, center_lat, n, lon_sd=8, lat_sd=5):
    lons = np.random.normal(center_lon, lon_sd, n)
    lats = np.random.normal(center_lat, lat_sd, n)
    return lons, lats

bubble_lons = []
bubble_lats = []
bubble_yield = []

clusters = [
    (-60, -5, 12),    # Amazon
    (-90, 15, 8),     # Central America / Gulf
    (10, 50, 16),     # Europe
    (20, 5, 10),      # Africa
    (78, 22, 10),     # India
    (105, 15, 18),    # SE Asia
    (120, -5, 12),    # Indonesia
    (145, -20, 10),   # Australia / Oceania
    (-160, 60, 6),    # Alaska / Bering
    (170, -40, 5),    # New Zealand
]

for clon, clat, n in clusters:
    lons, lats = cluster_points(clon, clat, n)
    bubble_lons.extend(lons)
    bubble_lats.extend(lats)

    # yield 范围 0~700+，故意让部分高值出现
    vals = np.clip(np.random.gamma(shape=2.3, scale=160, size=n), 20, 760)
    bubble_yield.extend(vals)

bubble_lons = np.array(bubble_lons)
bubble_lats = np.array(bubble_lats)
bubble_yield = np.array(bubble_yield)

# 限制到全球显示范围
mask = (
    (bubble_lons >= -180) & (bubble_lons <= 180) &
    (bubble_lats >= -60) & (bubble_lats <= 85)
)

bubble_lons = bubble_lons[mask]
bubble_lats = bubble_lats[mask]
bubble_yield = bubble_yield[mask]


# =========================================================
# 5. 气泡大小映射函数
# =========================================================
def size_map(v):
    """
    把 MeHg yield 数值映射为散点面积（points^2）
    """
    v = np.asarray(v)
    return np.interp(v, [0, 700], [12, 260])


bubble_sizes = size_map(bubble_yield)


# =========================================================
# 6. 颜色映射：MeHg export（底图）
# =========================================================
cmap = mpl.cm.Blues
norm = mpl.colors.LogNorm(vmin=0.01, vmax=3000)


# =========================================================
# 7. 开始绘图
# =========================================================
fig = plt.figure(figsize=(12, 5.8), dpi=300)
ax = plt.axes(projection=ccrs.PlateCarree())

ax.set_extent([-180, 180, -60, 85], crs=ccrs.PlateCarree())
ax.set_facecolor("#d9d9d9")

# 海洋 / 陆地底色
ax.add_feature(cfeature.OCEAN, facecolor="#d9d9d9", zorder=0)
ax.add_feature(cfeature.LAND, facecolor="#f2f2f2", edgecolor="none", zorder=1)

# 绘制底图颜色（这里是国家多边形；真实应用中应换成流域多边形）
for rec in records:
    name = rec.attributes["NAME_LONG"]
    if name == "Antarctica":
        continue

    geom = rec.geometry
    val = export_dict[name]

    ax.add_geometries(
        [geom],
        crs=ccrs.PlateCarree(),
        facecolor=cmap(norm(val)),
        edgecolor="white",
        linewidth=0.5,
        zorder=2
    )

# 叠加气泡点
ax.scatter(
    bubble_lons,
    bubble_lats,
    s=bubble_sizes,
    transform=ccrs.PlateCarree(),
    facecolor="#f4a3a0",
    edgecolor="#e77d79",
    linewidth=0.4,
    alpha=0.95,
    zorder=4
)

# 边框与刻度
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_linewidth(0.8)
    spine.set_edgecolor("0.2")


# =========================================================
# 8. 气泡大小图例（MeHg yield）
# =========================================================
legend_levels = [75, 225, 375, 525, 675]
legend_labels = ["0–150", "150–300", "300–450", "450–600", ">600"]

handles = []
for val in legend_levels:
    ms = np.sqrt(size_map(val))  # scatter 的 s 是面积，因此 legend 用 sqrt
    h = Line2D(
        [0], [0],
        marker="o",
        linestyle="",
        markerfacecolor="white",
        markeredgecolor="black",
        markeredgewidth=0.8,
        markersize=ms,
        color="black"
    )
    handles.append(h)

leg = ax.legend(
    handles,
    legend_labels,
    title="MeHg yield\n(ng m$^{-2}$ yr$^{-1}$)",
    loc="lower left",
    bbox_to_anchor=(0.01, 0.02),
    frameon=False,
    fontsize=10,
    title_fontsize=11,
    handlelength=1.0,
    handletextpad=0.7,
    borderpad=0.3,
    labelspacing=0.55
)

ax.add_artist(leg)


# =========================================================
# 9. 水平 colorbar（MeHg export）
# =========================================================
sm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])

cbar = fig.colorbar(
    sm,
    ax=ax,
    orientation="horizontal",
    fraction=0.045,
    pad=0.12,
    shrink=0.72
)

cbar.set_label("MeHg export (kg yr$^{-1}$)", fontsize=12, labelpad=8)
cbar.set_ticks([0.01, 0.1, 1, 10, 100, 1000])
cbar.set_ticklabels(["0.01", "0.1", "1", "10", "100", "1,000"])
cbar.ax.tick_params(labelsize=10, length=0)
cbar.outline.set_linewidth(0.8)


# =========================================================
# 10. 保存与显示
# =========================================================
plt.savefig(
    "global_mehg_export_yield_map.png",
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.05
)

plt.savefig(
    "global_mehg_export_yield_map.pdf",
    bbox_inches="tight",
    pad_inches=0.05
)

# Interactive display is disabled for reusable skill assets.
plt.close("all")