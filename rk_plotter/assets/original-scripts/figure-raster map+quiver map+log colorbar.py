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
lon = np.linspace(-180, 180, 361)
lat = np.linspace(-75, 75, 151)
Lon, Lat = np.meshgrid(lon, lat)


# =========================================================
# 2. 构造“微生物污染负荷 / 暴露风险”示例场
#    这里用随机模拟数据，后续可替换为真实数据
# =========================================================

def gaussian_hotspot(lon0, lat0, amp, sx=18, sy=10):
    """生成二维高斯热点"""
    return amp * np.exp(
        -(((Lon - lon0) ** 2) / (2 * sx ** 2)
          + ((Lat - lat0) ** 2) / (2 * sy ** 2))
    )

# 背景场：模拟低纬高、中高纬次高、南大洋低值
base = (
    0.22
    + 0.40 * np.exp(-(Lat / 38) ** 2)                 # 热带带状增强
    + 0.16 * np.exp(-((Lat - 35) / 18) ** 2)          # 北中纬次高
    + 0.08 * np.exp(-((Lat + 20) / 20) ** 2)          # 南低纬次高
)

# 加入热点，模拟高风险海区 / 高暴露区
field = (
    base
    + gaussian_hotspot(-70, 20, 0.65, 18, 10)     # 加勒比/西大西洋
    + gaussian_hotspot(-30, 35, 0.55, 20, 10)     # 北大西洋环流区
    + gaussian_hotspot(10, 45, 0.42, 18, 8)       # 欧洲近海
    + gaussian_hotspot(120, 20, 0.70, 18, 10)     # 西北太平洋
    + gaussian_hotspot(80, 10, 0.48, 22, 12)      # 印度洋
    + gaussian_hotspot(145, -10, 0.40, 20, 10)    # 印尼-西太平洋
)

# 加入纬向波动，模拟环流带/塑料聚集带
field += 0.12 * (np.sin(np.deg2rad(Lon * 1.7)) + 1) * np.exp(-(Lat / 28) ** 2)

# 平滑随机扰动
noise = gaussian_filter(np.random.rand(*Lon.shape), sigma=4)
field += 0.08 * noise

# 南大洋降低
field -= 0.35 * np.exp(-((Lat + 55) / 13) ** 2)

# 归一化
field = field - field.min()
field = field / field.max()

# 映射到对数范围（接近示例图：10^-6 到 10^-1）
vmin = 1e-6
vmax = 2e-1
log_field = np.log10(vmin) + field * (np.log10(vmax) - np.log10(vmin))
risk = 10 ** log_field


# =========================================================
# 3. 构造“风力 + 海流共同作用”的矢量场
#    这里只做示意：副热带环流 + 赤道流 + 西风漂流
# =========================================================

# 稀疏箭头网格
qlon = np.arange(-170, 171, 15)
qlat = np.arange(-60, 61, 15)
QLon, QLat = np.meshgrid(qlon, qlat)

# 风/流场简化模拟
U = (
    0.8 * np.cos(np.deg2rad(QLat)) * np.sin(np.deg2rad(QLon / 1.4))
    + 0.7 * np.exp(-(QLat / 18) ** 2)     # 赤道东/西向分量
    - 0.6 * np.exp(-((QLat + 45) / 12) ** 2)  # 南大洋西风漂流
)
V = (
    0.45 * np.sin(np.deg2rad(QLat * 1.7))
    + 0.22 * np.cos(np.deg2rad(QLon * 1.3))
)

# 局部强化，模拟副热带环流
U += 0.35 * np.exp(-((QLat - 25) / 10) ** 2)
U -= 0.25 * np.exp(-((QLat + 25) / 10) ** 2)

# 归一化一下，让箭头更协调
speed = np.sqrt(U**2 + V**2)
U = U / (speed + 1e-6)
V = V / (speed + 1e-6)


# =========================================================
# 4. 配色
#    接近原图：蓝 -> 白黄 -> 橙 -> 红
# =========================================================

colors = [
    "#3d46b5",  # 深蓝
    "#6c83d7",
    "#b9d4f2",
    "#fff2bf",
    "#f7c66a",
    "#f98f52",
    "#e34a33"
]

cmap = mpl.colors.LinearSegmentedColormap.from_list(
    "contaminant_load",
    colors,
    N=256
)

norm = mpl.colors.LogNorm(vmin=vmin, vmax=vmax)


# =========================================================
# 5. 绘图
# =========================================================

fig = plt.figure(figsize=(6.0, 2.9), dpi=300)
ax = plt.axes(projection=ccrs.PlateCarree())

ax.set_extent([-180, 180, -75, 75], crs=ccrs.PlateCarree())
ax.set_facecolor("#bdbdbd")

# 背景网格线（较浅）
gl = ax.gridlines(
    draw_labels=False,
    linewidth=0.45,
    color="0.75",
    alpha=0.7,
    linestyle="-"
)

# 风险栅格 / 负荷栅格
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

# 叠加箭头
ax.quiver(
    QLon,
    QLat,
    U,
    V,
    transform=ccrs.PlateCarree(),
    color="black",
    scale=28,
    width=0.0026,
    headwidth=3.2,
    headlength=4.2,
    headaxislength=3.6,
    alpha=0.9,
    zorder=3
)

# 陆地
ax.add_feature(
    cfeature.LAND,
    facecolor="#d9d9d9",
    edgecolor="black",
    linewidth=0.5,
    zorder=4
)

# 海岸线
ax.add_feature(
    cfeature.COASTLINE,
    edgecolor="black",
    linewidth=0.45,
    zorder=5
)

# 坐标刻度
ax.set_xticks(np.arange(-150, 181, 60), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-60, 61, 30), crs=ccrs.PlateCarree())

# 不显示 x 标签，接近原图
ax.set_xticklabels([])

# y 标签显示纬度
ax.set_yticklabels(
    ["60° S", "30° S", "0°", "30° N", "60° N"],
    fontsize=9
)

ax.tick_params(
    axis="both",
    direction="out",
    length=3,
    width=0.8
)

# 边框
for spine in ax.spines.values():
    spine.set_linewidth(0.8)

# 标题
ax.set_title(
    "Load of contaminants",
    fontsize=12,
    pad=6
)

# 左侧变量名称（可换成你的具体指标名）
ax.text(
    -0.09, 0.50,
    "PFOS",
    transform=ax.transAxes,
    fontsize=11,
    ha="right",
    va="center"
)

# 右上角箭头尺度说明
ax.annotate(
    "",
    xy=(0.86, 0.95),
    xytext=(0.77, 0.95),
    xycoords="axes fraction",
    arrowprops=dict(
        arrowstyle="->",
        color="red",
        lw=1.1
    )
)

ax.text(
    0.865, 0.95,
    "0.3 m s$^{-1}$",
    transform=ax.transAxes,
    fontsize=9,
    color="black",
    va="center",
    ha="left"
)


# =========================================================
# 6. 纵向对数色标
# =========================================================

cbar = plt.colorbar(
    im,
    ax=ax,
    orientation="vertical",
    fraction=0.05,
    pad=0.02,
    extend="both"
)

cbar.set_ticks([1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1])
cbar.set_ticklabels([
    r"$10^{-6}$",
    r"$10^{-5}$",
    r"$10^{-4}$",
    r"$10^{-3}$",
    r"$10^{-2}$",
    r"$10^{-1}$"
])

cbar.ax.tick_params(labelsize=9, length=3, width=0.7)
cbar.outline.set_linewidth(0.8)


# =========================================================
# 7. 保存
# =========================================================

plt.savefig(
    "global_microbe_exposure_risk_map.png",
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.04
)

plt.savefig(
    "global_microbe_exposure_risk_map.pdf",
    bbox_inches="tight",
    pad_inches=0.04
)

plt.show()