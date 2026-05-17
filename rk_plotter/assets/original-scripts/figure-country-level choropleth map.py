import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Patch
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader


# =========================================================
# 1. 基础设置
# =========================================================

np.random.seed(42)

# 读取 Natural Earth 国家边界
shp_path = shpreader.natural_earth(
    resolution="110m",
    category="cultural",
    name="admin_0_countries"
)

records = list(shpreader.Reader(shp_path).records())


# =========================================================
# 2. 构造示例塑料排放数据
#    单位：Mt year^-1
# =========================================================

emission = {}

for rec in records:
    name = rec.attributes.get("ADMIN", rec.attributes.get("NAME_LONG", ""))

    if name == "Antarctica":
        continue

    # 默认随机排放量：多数国家为低到中等
    value = np.random.lognormal(mean=-1.2, sigma=0.9)

    # 限制到 0–10
    value = np.clip(value, 0.02, 8.5)
    emission[name] = value


# 手动设置部分国家，使空间格局更接近示例图
manual_values = {
    "China": 4.0,
    "India": 6.5,
    "Indonesia": 2.8,
    "Brazil": 1.6,
    "Russia": 1.4,
    "United States of America": 0.8,
    "Mexico": 0.7,
    "Australia": 0.1,
    "Canada": 0.1,
    "Japan": 0.2,
    "South Africa": 0.8,
    "Egypt": 0.5,
    "Nigeria": 0.9,
    "Turkey": 0.4,
    "Vietnam": 0.8,
    "Thailand": 0.7,
    "Philippines": 0.9,
    "Malaysia": 0.6,
    "Pakistan": 2.5,
    "Bangladesh": 1.8,
}

for name, value in manual_values.items():
    emission[name] = value


# =========================================================
# 3. 分级区间与颜色
# =========================================================

bins = [0, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 2.0, 5.0, 10.0]

labels = [
    "0–0.1",
    "0.1–0.2",
    "0.2–0.4",
    "0.4–0.6",
    "0.6–0.8",
    "0.8–1.0",
    "1.0–2.0",
    "2.0–5.0",
    "5.0–10.0",
]

colors = [
    "#a56ab3",  # 紫色
    "#8d83b6",  # 蓝紫
    "#8fa5bd",  # 蓝灰
    "#80bec5",  # 青蓝
    "#73c4c0",  # 青绿
    "#7ecbb8",  # 浅绿青
    "#9cdda4",  # 绿色
    "#d7ef82",  # 黄绿
    "#fff07a",  # 黄色
]

cmap = mpl.colors.ListedColormap(colors)
norm = mpl.colors.BoundaryNorm(bins, cmap.N)


def get_color(value):
    """根据排放量返回对应分级颜色"""
    idx = np.digitize(value, bins, right=True) - 1
    idx = np.clip(idx, 0, len(colors) - 1)
    return colors[idx]


# =========================================================
# 4. 绘制地图
# =========================================================

fig = plt.figure(figsize=(12.5, 5.4), dpi=300)

ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-180, 180, -60, 85], crs=ccrs.PlateCarree())

ax.set_facecolor("white")

# 海洋和陆地底色
ax.add_feature(
    cfeature.OCEAN,
    facecolor="white",
    edgecolor="none",
    zorder=0
)

ax.add_feature(
    cfeature.LAND,
    facecolor="#f2f2f2",
    edgecolor="none",
    zorder=1
)

# 绘制国家分级设色
for rec in records:
    name = rec.attributes.get("ADMIN", rec.attributes.get("NAME_LONG", ""))

    if name == "Antarctica":
        continue

    value = emission.get(name, np.nan)

    if np.isnan(value):
        facecolor = "#f2f2f2"
    else:
        facecolor = get_color(value)

    ax.add_geometries(
        [rec.geometry],
        crs=ccrs.PlateCarree(),
        facecolor=facecolor,
        edgecolor="0.35",
        linewidth=0.35,
        zorder=2
    )

# 海岸线与国界
ax.add_feature(
    cfeature.COASTLINE,
    edgecolor="0.35",
    linewidth=0.35,
    zorder=3
)

ax.add_feature(
    cfeature.BORDERS,
    edgecolor="0.35",
    linewidth=0.25,
    zorder=3
)

# 去除坐标轴
ax.set_xticks([])
ax.set_yticks([])

for spine in ax.spines.values():
    spine.set_visible(False)


# =========================================================
# 5. 图例
# =========================================================

legend_handles = [
    Patch(
        facecolor=color,
        edgecolor="0.35",
        linewidth=0.4,
        label=label
    )
    for color, label in zip(colors, labels)
]

legend = ax.legend(
    handles=legend_handles,
    title="Plastic emissions\n(Mt year$^{-1}$)",
    loc="lower left",
    bbox_to_anchor=(0.01, 0.04),
    frameon=False,
    fontsize=9,
    title_fontsize=10,
    handlelength=1.4,
    handleheight=0.9,
    handletextpad=0.5,
    labelspacing=0.45,
    borderpad=0.2
)

legend._legend_box.align = "left"


# =========================================================
# 6. 保存图片
# =========================================================

plt.savefig(
    "global_country_plastic_emissions_choropleth.png",
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.03
)

plt.savefig(
    "global_country_plastic_emissions_choropleth.pdf",
    bbox_inches="tight",
    pad_inches=0.03
)

plt.show()