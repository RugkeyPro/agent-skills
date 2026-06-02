---
rk_plotter_template: true
id: choropleth_kde_boxplot_combo
title: 分级设色地图+KDE 密度曲线图+箱线图（抖动散点）
category: map_distribution_combo
source_type: high_fidelity_markdown
template_path: templates/分级设色地图+KDE 密度曲线图+箱线图（抖动散点）.md
trigger_phrases:
  - 地图 KDE 箱线图
  - 空间分布加密度分布
  - choropleth kde boxplot
tags:
  - spatial
  - map
  - choropleth
  - kde
  - boxplot
  - jitter
  - multi_panel
data_profile:
  structure: regional_spatial_values_plus_grouped_samples
  required_fields:
    - geometry
    - region_value
    - group
    - value
  optional_fields:
    - bins
    - density_group
    - jitter
style_profile:
  layout: map_plus_distribution_panels
  aspect: wide
  primitives:
    - choropleth
    - kde_line
    - boxplot
    - jitter_scatter
  palette:
    - binned_map
    - group_density
dependencies:
  required:
    - numpy
    - pandas
    - matplotlib
  optional:
    - geopandas
    - cartopy
    - scipy
best_for: 把空间格局、总体密度分布和组间差异放在同一图中。
avoid_when: 只有点数据或没有组间分布问题。
---

![[Pasted image 20260520004743.png]] 一、图像类型识别与结构拆解

这是一张**三面板组合图**，主题是全球塑料排放空间分布及其统计分布差异。

```text
Panel a：全球国家尺度分级设色地图 / Choropleth map
Panel b：多城市塑料排放分布 KDE 密度曲线图，横轴为 log scale
Panel c：不同收入等级国家塑料排放箱线图 + 抖动散点
```

图像结构：

- **a 图**：世界地图，国家按 `Plastic emissions (kg cap⁻¹ year⁻¹)` 分级着色。
    
- **b 图**：6 个城市的塑料排放概率密度分布，横轴为对数坐标。
    
- **c 图**：按收入等级 `LIC、LMC、UMC、HIC` 比较塑料排放分布，箱线图上叠加黑色散点。
    
- 整体是典型环境科学论文图：上方大地图，下方左侧密度分布图，右侧箱线统计图。
    

---

## 二、单独的虚拟数据生成代码

```python
import numpy as np
import pandas as pd


def generate_country_plastic_emission_data(world, seed=42):
    """
    为世界国家边界生成虚拟塑料排放数据。

    参数
    ----
    world : GeoDataFrame
        Natural Earth 国家边界数据，需包含 ADMIN / NAME 字段。
    seed : int
        随机种子。

    返回
    ----
    DataFrame
        country, continent, income_category, plastic_emission
    """

    rng = np.random.default_rng(seed)

    df = world.copy()

    if "ADMIN" not in df.columns:
        df["ADMIN"] = df["NAME"]

    if "CONTINENT" not in df.columns:
        df["CONTINENT"] = "Unknown"

    income_categories = ["LIC", "LMC", "UMC", "HIC"]

    # 不同收入组的虚拟排放水平
    income_params = {
        "LIC": (11.0, 2.4),
        "LMC": (12.5, 3.5),
        "UMC": (9.0, 3.7),
        "HIC": (0.45, 0.35),
    }

    # 根据大洲给一个粗略收入组概率，仅用于模拟视觉效果
    continent_prob = {
        "Africa": [0.45, 0.35, 0.15, 0.05],
        "Asia": [0.10, 0.38, 0.42, 0.10],
        "Europe": [0.00, 0.05, 0.20, 0.75],
        "North America": [0.00, 0.15, 0.30, 0.55],
        "South America": [0.02, 0.28, 0.60, 0.10],
        "Oceania": [0.05, 0.25, 0.30, 0.40],
    }

    records = []

    for _, row in df.iterrows():
        country = row["ADMIN"]
        continent = row.get("CONTINENT", "Unknown")

        probs = continent_prob.get(continent, [0.15, 0.35, 0.35, 0.15])
        income = rng.choice(income_categories, p=probs)

        mean, sd = income_params[income]
        value = rng.normal(mean, sd)

        value = np.clip(value, 0.05, 24.5)

        records.append({
            "country": country,
            "continent": continent,
            "income_category": income,
            "plastic_emission": value
        })

    country_df = pd.DataFrame(records)

    # 手动强化若干国家色块，使地图更接近示例图的空间格局
    overrides = {
        "United States of America": 1.8,
        "Canada": 1.3,
        "Australia": 0.8,
        "New Zealand": 0.9,
        "China": 2.6,
        "Russia": 10.5,
        "Brazil": 5.8,
        "India": 5.4,
        "Mexico": 6.2,
        "Indonesia": 12.0,
        "South Africa": 9.5,
        "Saudi Arabia": 2.3,
        "Chile": 1.2,
        "Argentina": 7.5,
    }

    for country, value in overrides.items():
        country_df.loc[country_df["country"] == country, "plastic_emission"] = value

    return country_df


def generate_city_kde_data(seed=7, n_each=700):
    """
    生成 Panel b 的城市塑料排放分布数据。
    x 轴为 kg cap^-1 year^-1，适合 log-scale KDE。
    """

    rng = np.random.default_rng(seed)

    city_params = {
        "Hamburg":   {"mu": -1.55, "sigma": 0.33},
        "Los Angeles": {"mu": -1.25, "sigma": 0.35},
        "Shenzhen": {"mu": -0.85, "sigma": 0.38},
        "Maracaibo": {"mu": -0.25, "sigma": 0.30},
        "Agra": {"mu": 0.80, "sigma": 0.36},
        "Mogadishu": {"mu": 1.20, "sigma": 0.25},
    }

    rows = []

    for city, par in city_params.items():
        log10_values = rng.normal(par["mu"], par["sigma"], n_each)
        values = 10 ** log10_values

        for v in values:
            rows.append({
                "city": city,
                "plastic_emission": v
            })

    return pd.DataFrame(rows)


def generate_income_box_data(seed=123):
    """
    生成 Panel c 的收入等级箱线图数据。
    """

    rng = np.random.default_rng(seed)

    configs = {
        "LIC": {"n": 42, "mean": 11.5, "sd": 2.6},
        "LMC": {"n": 55, "mean": 12.3, "sd": 3.4},
        "UMC": {"n": 65, "mean": 9.5, "sd": 4.1},
        "HIC": {"n": 58, "mean": 0.45, "sd": 0.35},
    }

    rows = []

    for group, cfg in configs.items():
        values = rng.normal(cfg["mean"], cfg["sd"], cfg["n"])
        values = np.clip(values, 0.02, 26.0)

        # 加少量高值离群点
        if group in ["LIC", "LMC", "UMC"]:
            values[:2] = values[:2] + rng.uniform(6, 12, 2)

        for v in values:
            rows.append({
                "income_category": group,
                "plastic_emission": v
            })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    city_df = generate_city_kde_data()
    income_df = generate_income_box_data()

    city_df.to_csv("city_kde_plastic_emissions.csv", index=False)
    income_df.to_csv("income_box_plastic_emissions.csv", index=False)

    print(city_df.head())
    print(income_df.head())
```

---

## 三、完整 Python 绘图代码

```python
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["svg.fonttype"] = "none"

from scipy.stats import gaussian_kde
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.ticker import LogFormatterMathtext
from cartopy.io import shapereader as shpreader


# ============================================================
# 1. 数据生成函数
# ============================================================

def load_world_boundaries():
    shp_path = shpreader.natural_earth(
        resolution="110m",
        category="cultural",
        name="admin_0_countries"
    )

    world = gpd.read_file(shp_path)

    if "ADMIN" not in world.columns and "NAME" in world.columns:
        world["ADMIN"] = world["NAME"]

    return world


def generate_country_plastic_emission_data(world, seed=42):
    rng = np.random.default_rng(seed)

    df = world.copy()

    income_categories = ["LIC", "LMC", "UMC", "HIC"]

    income_params = {
        "LIC": (11.0, 2.4),
        "LMC": (12.5, 3.5),
        "UMC": (9.0, 3.7),
        "HIC": (0.45, 0.35),
    }

    continent_prob = {
        "Africa": [0.45, 0.35, 0.15, 0.05],
        "Asia": [0.10, 0.38, 0.42, 0.10],
        "Europe": [0.00, 0.05, 0.20, 0.75],
        "North America": [0.00, 0.15, 0.30, 0.55],
        "South America": [0.02, 0.28, 0.60, 0.10],
        "Oceania": [0.05, 0.25, 0.30, 0.40],
    }

    records = []

    for _, row in df.iterrows():
        country = row["ADMIN"]
        continent = row.get("CONTINENT", "Unknown")

        probs = continent_prob.get(continent, [0.15, 0.35, 0.35, 0.15])
        income = rng.choice(income_categories, p=probs)

        mean, sd = income_params[income]
        value = np.clip(rng.normal(mean, sd), 0.05, 24.5)

        records.append({
            "country": country,
            "continent": continent,
            "income_category": income,
            "plastic_emission": value
        })

    country_df = pd.DataFrame(records)

    overrides = {
        "United States of America": 1.8,
        "Canada": 1.3,
        "Australia": 0.8,
        "New Zealand": 0.9,
        "China": 2.6,
        "Russia": 10.5,
        "Brazil": 5.8,
        "India": 5.4,
        "Mexico": 6.2,
        "Indonesia": 12.0,
        "South Africa": 9.5,
        "Saudi Arabia": 2.3,
        "Chile": 1.2,
        "Argentina": 7.5,
    }

    for country, value in overrides.items():
        country_df.loc[country_df["country"] == country, "plastic_emission"] = value

    return country_df


def generate_city_kde_data(seed=7, n_each=700):
    rng = np.random.default_rng(seed)

    city_params = {
        "Hamburg": {"mu": -1.55, "sigma": 0.33},
        "Los Angeles": {"mu": -1.25, "sigma": 0.35},
        "Shenzhen": {"mu": -0.85, "sigma": 0.38},
        "Maracaibo": {"mu": -0.25, "sigma": 0.30},
        "Agra": {"mu": 0.80, "sigma": 0.36},
        "Mogadishu": {"mu": 1.20, "sigma": 0.25},
    }

    rows = []

    for city, par in city_params.items():
        log10_values = rng.normal(par["mu"], par["sigma"], n_each)
        values = 10 ** log10_values

        for v in values:
            rows.append({
                "city": city,
                "plastic_emission": v
            })

    return pd.DataFrame(rows)


def generate_income_box_data(seed=123):
    rng = np.random.default_rng(seed)

    configs = {
        "LIC": {"n": 42, "mean": 11.5, "sd": 2.6},
        "LMC": {"n": 55, "mean": 12.3, "sd": 3.4},
        "UMC": {"n": 65, "mean": 9.5, "sd": 4.1},
        "HIC": {"n": 58, "mean": 0.45, "sd": 0.35},
    }

    rows = []

    for group, cfg in configs.items():
        values = rng.normal(cfg["mean"], cfg["sd"], cfg["n"])
        values = np.clip(values, 0.02, 26.0)

        if group in ["LIC", "LMC", "UMC"]:
            values[:2] = values[:2] + rng.uniform(6, 12, 2)

        for v in values:
            rows.append({
                "income_category": group,
                "plastic_emission": v
            })

    return pd.DataFrame(rows)


world = load_world_boundaries()
country_df = generate_country_plastic_emission_data(world)
city_df = generate_city_kde_data()
income_df = generate_income_box_data()

world_plot = world.merge(
    country_df[["country", "plastic_emission"]],
    left_on="ADMIN",
    right_on="country",
    how="left"
)

world_plot["plastic_emission"] = world_plot["plastic_emission"].fillna(0.1)


# ============================================================
# 2. 配色与基础样式
# ============================================================

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "axes.linewidth": 1.1,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "savefig.dpi": 300,
})

# Panel a：分级地图颜色，非连续 cmap，而是 ListedColormap
map_colors = [
    "#9d6ab0",  # <1
    "#7c6fa3",  # 1–3
    "#8791b5",  # 3–5
    "#86adbf",  # 5–7
    "#77b8b2",  # 7–9
    "#70c3aa",  # 9–11
    "#84cfa5",  # 11–13
    "#9bd69b",  # 13–15
    "#c7d979",  # 15–17
    "#f1e46b",  # >17
]

bounds = [0, 1, 3, 5, 7, 9, 11, 13, 15, 17, 100]
map_cmap = ListedColormap(map_colors)
map_norm = BoundaryNorm(bounds, len(map_colors))

# Panel b：城市 KDE 多元配色
city_colors = {
    "Hamburg": "#b9ded6",
    "Los Angeles": "#82b9ca",
    "Shenzhen": "#b9a4c6",
    "Maracaibo": "#f3efc8",
    "Agra": "#f4c991",
    "Mogadishu": "#efb8a7",
}

# Panel c：收入等级箱线图配色
income_colors = {
    "LIC": "#39b894",
    "LMC": "#8fbad5",
    "UMC": "#d7bedc",
    "HIC": "#e9e1d5",
}

edge_color = "#555555"


# ============================================================
# 3. 创建画布
# ============================================================

fig = plt.figure(figsize=(10.2, 7.2), dpi=120)

gs = fig.add_gridspec(
    nrows=2,
    ncols=3,
    height_ratios=[1.38, 1.0],
    width_ratios=[1.25, 1.25, 1.05],
    left=0.06,
    right=0.98,
    bottom=0.08,
    top=0.96,
    hspace=0.22,
    wspace=0.20
)

ax_map = fig.add_subplot(gs[0, :])
ax_kde = fig.add_subplot(gs[1, 0:2])
ax_box = fig.add_subplot(gs[1, 2])


# ============================================================
# 4. Panel a：全球分级设色地图
# ============================================================

ax_map.set_facecolor("white")

world_plot.plot(
    ax=ax_map,
    column="plastic_emission",
    cmap=map_cmap,
    norm=map_norm,
    edgecolor="#777777",
    linewidth=0.35
)

ax_map.set_xlim(-180, 180)
ax_map.set_ylim(-60, 85)
ax_map.set_aspect("equal")
ax_map.axis("off")

ax_map.text(
    -177,
    82,
    "a",
    fontsize=16,
    fontweight="bold",
    ha="left",
    va="top"
)

# 自定义左侧图例
legend_x = -178
legend_y = 33
dy = 9.5

ax_map.text(
    legend_x,
    legend_y + 12,
    "Plastic emissions\n(kg cap$^{-1}$ year$^{-1}$)",
    ha="left",
    va="top",
    fontsize=8,
    linespacing=0.95
)

legend_labels = ["<1", "1–3", "3–5", "5–7", "7–9", "9–11", "11–13", "13–15", "15–17", ">17"]

for i, (color, label) in enumerate(zip(map_colors, legend_labels)):
    y = legend_y - i * dy
    ax_map.add_patch(
        plt.Rectangle(
            (legend_x + 1, y),
            8,
            5,
            facecolor=color,
            edgecolor="#666666",
            linewidth=0.3
        )
    )
    ax_map.text(
        legend_x + 11,
        y + 2.5,
        label,
        ha="left",
        va="center",
        fontsize=8
    )


# ============================================================
# 5. Panel b：多城市 KDE 密度曲线
# ============================================================

x_grid = np.logspace(-3, 2.2, 600)
log_grid = np.log10(x_grid)

for city in ["Hamburg", "Los Angeles", "Shenzhen", "Maracaibo", "Agra", "Mogadishu"]:
    vals = city_df.loc[city_df["city"] == city, "plastic_emission"].to_numpy()
    log_vals = np.log10(vals)

    kde = gaussian_kde(log_vals, bw_method=0.28)
    density = kde(log_grid)

    ax_kde.fill_between(
        x_grid,
        density,
        color=city_colors[city],
        alpha=0.65,
        edgecolor="black",
        linewidth=0.8,
        label=city
    )

    ax_kde.plot(
        x_grid,
        density,
        color="black",
        linewidth=0.8
    )

ax_kde.set_xscale("log")
ax_kde.set_xlim(8e-4, 1.6e2)
ax_kde.set_ylim(0, 1.65)

ax_kde.set_xlabel("Plastic emissions (kg cap$^{-1}$ year$^{-1}$)", fontsize=9)
ax_kde.set_ylabel("Density", fontsize=9)

ax_kde.set_xticks([1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2])
ax_kde.xaxis.set_major_formatter(LogFormatterMathtext())

ax_kde.tick_params(axis="both", labelsize=8)

ax_kde.legend(
    loc="upper left",
    frameon=False,
    fontsize=8,
    handlelength=0.8,
    handletextpad=0.4,
    labelspacing=0.25
)

ax_kde.text(
    -0.12,
    1.04,
    "b",
    transform=ax_kde.transAxes,
    fontsize=16,
    fontweight="bold",
    ha="left"
)


# ============================================================
# 6. Panel c：收入等级箱线图 + 散点
# ============================================================

groups = ["LIC", "LMC", "UMC", "HIC"]
positions = np.arange(1, len(groups) + 1)

box_data = [
    income_df.loc[income_df["income_category"] == g, "plastic_emission"].to_numpy()
    for g in groups
]

bp = ax_box.boxplot(
    box_data,
    positions=positions,
    widths=0.65,
    patch_artist=True,
    showfliers=False,
    medianprops=dict(color="black", linewidth=1.1),
    boxprops=dict(color="black", linewidth=1.0),
    whiskerprops=dict(color="black", linewidth=1.0),
    capprops=dict(color="black", linewidth=1.0)
)

for patch, g in zip(bp["boxes"], groups):
    patch.set_facecolor(income_colors[g])
    patch.set_alpha(0.95)

rng = np.random.default_rng(100)

for pos, g in zip(positions, groups):
    vals = income_df.loc[income_df["income_category"] == g, "plastic_emission"].to_numpy()
    jitter = rng.normal(0, 0.08, len(vals))

    ax_box.scatter(
        np.full(len(vals), pos) + jitter,
        vals,
        s=5,
        color="black",
        alpha=0.85,
        linewidth=0,
        zorder=3
    )

ax_box.set_xlim(0.45, 4.55)
ax_box.set_ylim(0, 27)

ax_box.set_xticks(positions)
ax_box.set_xticklabels(groups, fontsize=8)
ax_box.set_xlabel("Income category", fontsize=9)
ax_box.set_ylabel("Plastic emissions (kg cap$^{-1}$ year$^{-1}$)", fontsize=9)

ax_box.tick_params(axis="both", labelsize=8)

for spine in ["top", "right"]:
    ax_box.spines[spine].set_visible(False)

ax_box.text(
    -0.34,
    1.04,
    "c",
    transform=ax_box.transAxes,
    fontsize=16,
    fontweight="bold",
    ha="left"
)


# ============================================================
# 7. 统一边框与保存
# ============================================================

for ax in [ax_kde, ax_box]:
    for spine in ax.spines.values():
        spine.set_linewidth(1.0)
        spine.set_color("black")

plt.savefig(
    "reproduced_global_plastic_emissions_multipanel.png",
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.04
)

plt.close(fig)
```

---

## 四、标签总结

```text
# 图片类型：三面板组合图 / 全球分级设色地图 + KDE 密度图 + 箱线图
# 图形结构：上方一整幅世界地图，下方左侧 KDE 分布图，右侧收入等级箱线图
# 适合数据类型：国家尺度空间数据、城市尺度排放分布数据、收入等级分组统计数据
# Panel a：Choropleth map，国家面图层按 Plastic emissions 分级着色
# Panel b：多组 KDE 密度曲线图，横轴为 log-scale
# Panel c：箱线图 + jitter scatter
# 横轴变量：
# - Panel b：Plastic emissions，单位 kg cap^-1 year^-1
# - Panel c：Income category
# 纵轴变量：
# - Panel b：Density
# - Panel c：Plastic emissions，单位 kg cap^-1 year^-1
# 分组变量：
# - Panel b：Hamburg、Los Angeles、Shenzhen、Maracaibo、Agra、Mogadishu
# - Panel c：LIC、LMC、UMC、HIC
# 配色方案：
# Panel a 分级地图 ListedColormap：
# - <1：#9d6ab0
# - 1–3：#7c6fa3
# - 3–5：#8791b5
# - 5–7：#86adbf
# - 7–9：#77b8b2
# - 9–11：#70c3aa
# - 11–13：#84cfa5
# - 13–15：#9bd69b
# - 15–17：#c7d979
# - >17：#f1e46b
# Panel b 城市 KDE 配色：
# - Hamburg：#b9ded6
# - Los Angeles：#82b9ca
# - Shenzhen：#b9a4c6
# - Maracaibo：#f3efc8
# - Agra：#f4c991
# - Mogadishu：#efb8a7
# Panel c 收入等级箱线图配色：
# - LIC：#39b894
# - LMC：#8fbad5
# - UMC：#d7bedc
# - HIC：#e9e1d5
# 辅助颜色：
# - 国家边界：#777777
# - 箱线图边框：#000000
# - 散点：#000000
# - 背景：#ffffff
# cmap 色系：Panel a 使用 ListedColormap 自定义离散色带；Panel b 和 c 为多元自定义色号
# 视觉风格：环境科学论文图 / 全球污染排放空间统计图 / Nature 风格多面板图
# 推荐绘图库：geopandas + cartopy + matplotlib + scipy
# 复现难度：较高
```