---
rk_plotter_template: true
id: taxon_boxplot_pca_stacked_percent
title: 类群箱线图+PCA 双标图+堆叠百分比柱状图
category: ecology_multivariate_combo
source_type: high_fidelity_markdown
template_path: templates/类群箱线图+PCA 双标图+堆叠百分比柱状图.md
trigger_phrases:
  - 类群箱线图 PCA 堆叠百分比
  - 群落组成和PCA
  - taxon boxplot PCA stacked percent
tags:
  - distribution
  - pca
  - ordination
  - composition
  - stacked_bar
  - multi_panel
  - ecology
data_profile:
  structure: taxon_samples_plus_ordination_plus_composition_matrix
  required_fields:
    - taxon
    - value
    - scores
    - loadings
    - groups
    - components
  optional_fields:
    - ellipse_group
    - percent_values
    - environment_vectors
style_profile:
  layout: three_panel_composite
  aspect: wide
  primitives:
    - boxplot
    - scatter
    - ellipse
    - loading_arrows
    - stacked_bar
  palette:
    - taxon_groups
    - ordination_groups
    - composition_segments
dependencies:
  required:
    - numpy
    - pandas
    - matplotlib
  optional: []
best_for: 生态或组学数据中同时展示类群分布、排序空间和组成比例。
avoid_when: 没有 PCA/排序结果或只有单一分布比较。
---

![[Pasted image 20260520010941.png]]
一、图像类型识别与结构拆解

这是一张**复杂多面板生态统计图 / 保护生物学多指标组合图**，整体由左侧 `a–c` 与右侧 `d–e` 两部分组成。

```text
a：3×1 物种类群箱线图，表示 native habitat 面积
b：3×1 物种类群箱线图，表示 unoccupied habitats 比例
c：3×1 物种类群箱线图，表示 isolated habitats 比例
d：PCA 双标图 / PCA biplot，比较 Native habitats 与 Unoccupied habitats
e：堆叠百分比柱状图，比较不同 hotspot value quantile 下的 HFI levels 构成
```

核心结构：

- 左侧为 `3 行 × 3 列` 小面板箱线图。
    
- 列变量为物种类群：`Amphibian`、`Mammal`、`Reptile`。
    
- 横轴等级为濒危等级：`VU`、`EN`、`CR`。
    
- 右上为两个 PCA 双标图，包含点云、密度着色、变量箭头和变量名。
    
- 右下为两个百分比堆叠柱状图，展示不同人类足迹压力等级的比例变化。
    

---

## 二、单独的虚拟数据生成代码

```python
import numpy as np
import pandas as pd


def beta_scaled(rng, mean, concentration, n, low=0.002, high=1.0):
    a = mean * concentration
    b = (1 - mean) * concentration
    values = rng.beta(a, b, n)
    return np.clip(values, low, high)


def generate_boxplot_data(seed=42, n=520):
    rng = np.random.default_rng(seed)

    taxa = ["Amphibian", "Mammal", "Reptile"]
    status = ["VU", "EN", "CR"]

    area_means = {
        "Amphibian": {"VU": 11.1, "EN": 10.6, "CR": 10.4},
        "Mammal": {"VU": 12.2, "EN": 11.3, "CR": 11.0},
        "Reptile": {"VU": 11.0, "EN": 10.2, "CR": 10.5},
    }

    unoccupied_means = {
        "Amphibian": {"VU": 0.16, "EN": 0.22, "CR": 0.34},
        "Mammal": {"VU": 0.18, "EN": 0.22, "CR": 0.31},
        "Reptile": {"VU": 0.20, "EN": 0.23, "CR": 0.36},
    }

    isolated_means = {
        "Amphibian": {"VU": 0.18, "EN": 0.24, "CR": 0.36},
        "Mammal": {"VU": 0.20, "EN": 0.23, "CR": 0.30},
        "Reptile": {"VU": 0.18, "EN": 0.22, "CR": 0.29},
    }

    rows = []

    for taxon in taxa:
        for st in status:
            area = rng.normal(area_means[taxon][st], 0.85, n)
            area = np.concatenate([
                area,
                rng.normal(area_means[taxon][st] - 2.0, 0.55, 25),
                rng.normal(area_means[taxon][st] + 2.0, 0.65, 25)
            ])
            area = np.clip(area, 5.8, 17.5)

            for v in area:
                rows.append({
                    "panel": "native_area",
                    "taxon": taxon,
                    "status": st,
                    "value": v
                })

            unocc = beta_scaled(
                rng,
                mean=unoccupied_means[taxon][st],
                concentration=4.2,
                n=n + 50
            )

            for v in unocc:
                rows.append({
                    "panel": "unoccupied",
                    "taxon": taxon,
                    "status": st,
                    "value": v
                })

            iso = beta_scaled(
                rng,
                mean=isolated_means[taxon][st],
                concentration=3.6,
                n=n + 50
            )

            for v in iso:
                rows.append({
                    "panel": "isolated",
                    "taxon": taxon,
                    "status": st,
                    "value": v
                })

    return pd.DataFrame(rows)


def generate_pca_points(seed=7, n=8500):
    rng = np.random.default_rng(seed)

    rows = []

    for habitat in ["Native habitats", "Unoccupied habitats"]:
        if habitat == "Native habitats":
            centers = [(-1.2, -0.4), (1.8, 1.9), (-2.2, 1.2), (2.8, -1.0)]
            weights = [0.50, 0.25, 0.15, 0.10]
        else:
            centers = [(-1.0, -0.4), (2.0, 1.7), (-2.7, 1.1), (2.4, -1.2)]
            weights = [0.55, 0.22, 0.13, 0.10]

        comp = rng.choice(len(centers), size=n, p=weights)

        xs = np.zeros(n)
        ys = np.zeros(n)

        for i, (cx, cy) in enumerate(centers):
            mask = comp == i
            m = mask.sum()
            cov = np.array([[1.4, 0.35], [0.35, 0.85]])
            pts = rng.multivariate_normal([cx, cy], cov, m)
            xs[mask] = pts[:, 0]
            ys[mask] = pts[:, 1]

        # 轻微非线性拉伸，使点云更接近原图中的椭圆云团
        ys += 0.15 * xs + rng.normal(0, 0.35, n)
        xs = np.clip(xs, -6.2, 8.0)
        ys = np.clip(ys, -6.2, 7.0)

        for x, y in zip(xs, ys):
            rows.append({
                "habitat": habitat,
                "PC1": x,
                "PC2": y
            })

    return pd.DataFrame(rows)


def generate_pca_arrows():
    arrows = [
        ("AI", -4.7, 1.6),
        ("DD", -3.4, 2.0),
        ("PTC", -5.4, 0.6),
        ("BIO12", -5.6, -0.6),
        ("NDVI", -3.1, -1.5),
        ("SP", -0.2, 6.4),
        ("ELE", 1.9, 6.1),
        ("BIO2", 4.2, 0.7),
        ("BIO15", 3.0, -2.5),
        ("BIO1", -2.2, -5.2),
        ("HFI", -0.7, -3.6),
    ]

    return pd.DataFrame(arrows, columns=["variable", "x", "y"])


def generate_hfi_stack_data():
    quantiles = np.arange(5, 100, 10)

    native = pd.DataFrame({
        "habitat": "Native habitats",
        "quantile": quantiles,
        "12–50 (Very high pressure)": [8, 20, 16, 22, 13, 12, 13, 17, 18, 35],
        "6–11 (High pressure)":        [12, 26, 22, 21, 22, 23, 27, 32, 22, 30],
        "3–5 (Moderate pressure)":     [13, 20, 25, 22, 23, 28, 29, 28, 23, 20],
        "1–2 (Low pressure)":          [19, 12, 20, 19, 19, 15, 17, 15, 18, 9],
        "0 (No pressure)":             [48, 22, 17, 16, 23, 22, 14, 8, 19, 6],
    })

    unoccupied = pd.DataFrame({
        "habitat": "Unoccupied habitats",
        "quantile": quantiles,
        "12–50 (Very high pressure)": [2, 6, 8, 9, 10, 13, 18, 22, 20, 27],
        "6–11 (High pressure)":        [4, 8, 14, 13, 16, 20, 25, 30, 27, 33],
        "3–5 (Moderate pressure)":     [5, 11, 15, 16, 22, 26, 28, 24, 31, 22],
        "1–2 (Low pressure)":          [10, 9, 14, 16, 17, 19, 16, 14, 14, 10],
        "0 (No pressure)":             [79, 66, 49, 46, 35, 22, 13, 10, 8, 8],
    })

    return pd.concat([native, unoccupied], ignore_index=True)


if __name__ == "__main__":
    box_df = generate_boxplot_data()
    pca_df = generate_pca_points()
    arrow_df = generate_pca_arrows()
    hfi_df = generate_hfi_stack_data()

    box_df.to_csv("boxplot_panels_abc.csv", index=False)
    pca_df.to_csv("pca_points_panel_d.csv", index=False)
    arrow_df.to_csv("pca_arrows_panel_d.csv", index=False)
    hfi_df.to_csv("hfi_stack_panel_e.csv", index=False)
```

---

## 三、完整 Python 绘图代码

```python
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["svg.fonttype"] = "none"
from matplotlib.patches import Ellipse, Patch
from matplotlib.colors import Normalize
from matplotlib.ticker import FuncFormatter


# ============================================================
# 1. 虚拟数据生成
# ============================================================

def beta_scaled(rng, mean, concentration, n, low=0.002, high=1.0):
    a = mean * concentration
    b = (1 - mean) * concentration
    values = rng.beta(a, b, n)
    return np.clip(values, low, high)


def generate_boxplot_data(seed=42, n=520):
    rng = np.random.default_rng(seed)

    taxa = ["Amphibian", "Mammal", "Reptile"]
    status = ["VU", "EN", "CR"]

    area_means = {
        "Amphibian": {"VU": 11.1, "EN": 10.6, "CR": 10.4},
        "Mammal": {"VU": 12.2, "EN": 11.3, "CR": 11.0},
        "Reptile": {"VU": 11.0, "EN": 10.2, "CR": 10.5},
    }

    unoccupied_means = {
        "Amphibian": {"VU": 0.16, "EN": 0.22, "CR": 0.34},
        "Mammal": {"VU": 0.18, "EN": 0.22, "CR": 0.31},
        "Reptile": {"VU": 0.20, "EN": 0.23, "CR": 0.36},
    }

    isolated_means = {
        "Amphibian": {"VU": 0.18, "EN": 0.24, "CR": 0.36},
        "Mammal": {"VU": 0.20, "EN": 0.23, "CR": 0.30},
        "Reptile": {"VU": 0.18, "EN": 0.22, "CR": 0.29},
    }

    rows = []

    for taxon in taxa:
        for st in status:
            area = rng.normal(area_means[taxon][st], 0.85, n)
            area = np.concatenate([
                area,
                rng.normal(area_means[taxon][st] - 2.0, 0.55, 25),
                rng.normal(area_means[taxon][st] + 2.0, 0.65, 25)
            ])
            area = np.clip(area, 5.8, 17.5)

            for v in area:
                rows.append(["native_area", taxon, st, v])

            unocc = beta_scaled(rng, unoccupied_means[taxon][st], 4.2, n + 50)

            for v in unocc:
                rows.append(["unoccupied", taxon, st, v])

            iso = beta_scaled(rng, isolated_means[taxon][st], 3.6, n + 50)

            for v in iso:
                rows.append(["isolated", taxon, st, v])

    return pd.DataFrame(rows, columns=["panel", "taxon", "status", "value"])


def generate_pca_points(seed=7, n=8500):
    rng = np.random.default_rng(seed)
    rows = []

    for habitat in ["Native habitats", "Unoccupied habitats"]:
        if habitat == "Native habitats":
            centers = [(-1.2, -0.4), (1.8, 1.9), (-2.2, 1.2), (2.8, -1.0)]
            weights = [0.50, 0.25, 0.15, 0.10]
        else:
            centers = [(-1.0, -0.4), (2.0, 1.7), (-2.7, 1.1), (2.4, -1.2)]
            weights = [0.55, 0.22, 0.13, 0.10]

        comp = rng.choice(len(centers), size=n, p=weights)
        xs = np.zeros(n)
        ys = np.zeros(n)

        for i, (cx, cy) in enumerate(centers):
            mask = comp == i
            pts = rng.multivariate_normal(
                [cx, cy],
                [[1.4, 0.35], [0.35, 0.85]],
                mask.sum()
            )
            xs[mask] = pts[:, 0]
            ys[mask] = pts[:, 1]

        ys += 0.15 * xs + rng.normal(0, 0.35, n)
        xs = np.clip(xs, -6.2, 8.0)
        ys = np.clip(ys, -6.2, 7.0)

        for x, y in zip(xs, ys):
            rows.append([habitat, x, y])

    return pd.DataFrame(rows, columns=["habitat", "PC1", "PC2"])


def generate_pca_arrows():
    return pd.DataFrame(
        [
            ("AI", -4.7, 1.6),
            ("DD", -3.4, 2.0),
            ("PTC", -5.4, 0.6),
            ("BIO12", -5.6, -0.6),
            ("NDVI", -3.1, -1.5),
            ("SP", -0.2, 6.4),
            ("ELE", 1.9, 6.1),
            ("BIO2", 4.2, 0.7),
            ("BIO15", 3.0, -2.5),
            ("BIO1", -2.2, -5.2),
            ("HFI", -0.7, -3.6),
        ],
        columns=["variable", "x", "y"]
    )


def generate_hfi_stack_data():
    quantiles = np.arange(5, 100, 10)

    native = pd.DataFrame({
        "habitat": "Native habitats",
        "quantile": quantiles,
        "12–50 (Very high pressure)": [8, 20, 16, 22, 13, 12, 13, 17, 18, 35],
        "6–11 (High pressure)":        [12, 26, 22, 21, 22, 23, 27, 32, 22, 30],
        "3–5 (Moderate pressure)":     [13, 20, 25, 22, 23, 28, 29, 28, 23, 20],
        "1–2 (Low pressure)":          [19, 12, 20, 19, 19, 15, 17, 15, 18, 9],
        "0 (No pressure)":             [48, 22, 17, 16, 23, 22, 14, 8, 19, 6],
    })

    unoccupied = pd.DataFrame({
        "habitat": "Unoccupied habitats",
        "quantile": quantiles,
        "12–50 (Very high pressure)": [2, 6, 8, 9, 10, 13, 18, 22, 20, 27],
        "6–11 (High pressure)":        [4, 8, 14, 13, 16, 20, 25, 30, 27, 33],
        "3–5 (Moderate pressure)":     [5, 11, 15, 16, 22, 26, 28, 24, 31, 22],
        "1–2 (Low pressure)":          [10, 9, 14, 16, 17, 19, 16, 14, 14, 10],
        "0 (No pressure)":             [79, 66, 49, 46, 35, 22, 13, 10, 8, 8],
    })

    return pd.concat([native, unoccupied], ignore_index=True)


box_df = generate_boxplot_data()
pca_df = generate_pca_points()
arrow_df = generate_pca_arrows()
hfi_df = generate_hfi_stack_data()


# ============================================================
# 2. 绘图工具函数
# ============================================================

def point_density(x, y, bins=120, xlim=(-6.2, 8.2), ylim=(-6.2, 7.2)):
    counts, xedges, yedges = np.histogram2d(
        x,
        y,
        bins=bins,
        range=[xlim, ylim]
    )

    xi = np.searchsorted(xedges, x, side="right") - 1
    yi = np.searchsorted(yedges, y, side="right") - 1

    xi = np.clip(xi, 0, bins - 1)
    yi = np.clip(yi, 0, bins - 1)

    z = counts[xi, yi]
    return z / z.max()


def clean_prop_tick(x, pos):
    if abs(x - 0.003) < 1e-8:
        return "0"
    if abs(x - 1) < 1e-8:
        return "1.00"
    return f"{x:.2f}".rstrip("0").rstrip(".")


def plot_box_panel(ax, data, taxon, panel, ylabel, ylim, log_prop=False):
    status_order = ["VU", "EN", "CR"]
    colors = {
        "VU": "#e9ec3f",
        "EN": "#d78934",
        "CR": "#b51f26",
    }

    values = [
        data[
            (data["taxon"] == taxon) &
            (data["status"] == s) &
            (data["panel"] == panel)
        ]["value"].to_numpy()
        for s in status_order
    ]

    bp = ax.boxplot(
        values,
        positions=[1, 2, 3],
        widths=0.66,
        patch_artist=True,
        showmeans=True,
        meanprops=dict(marker=".", markerfacecolor="black", markeredgecolor="black", markersize=4),
        medianprops=dict(color="black", linewidth=0.8),
        boxprops=dict(linewidth=0.8),
        whiskerprops=dict(linewidth=0.8),
        capprops=dict(linewidth=0.8),
        flierprops=dict(
            marker=".",
            markersize=1.2,
            markerfacecolor="#bdbdbd",
            markeredgecolor="#bdbdbd",
            alpha=0.65
        )
    )

    for box, s in zip(bp["boxes"], status_order):
        box.set_facecolor(colors[s])
        box.set_edgecolor(colors[s])
        box.set_alpha(0.95)

    for k in ["whiskers", "caps"]:
        for item in bp[k]:
            item.set_color("#777777")

    ax.set_xlim(0.5, 3.5)
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(status_order, fontsize=12)
    ax.set_ylim(*ylim)

    if log_prop:
        ax.set_yscale("log")
        ax.set_yticks([0.003, 0.01, 0.03, 0.29, 1.0])
        ax.yaxis.set_major_formatter(FuncFormatter(clean_prop_tick))

    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(taxon, fontsize=13, pad=6)
    ax.tick_params(axis="both", labelsize=11)

    for spine in ax.spines.values():
        spine.set_linewidth(0.8)
        spine.set_color("#333333")


def plot_pca_panel(ax, habitat, xlabel):
    sub = pca_df[pca_df["habitat"] == habitat].copy()

    dens = point_density(
        sub["PC1"].to_numpy(),
        sub["PC2"].to_numpy()
    )

    order = np.argsort(dens)
    x = sub["PC1"].to_numpy()[order]
    y = sub["PC2"].to_numpy()[order]
    dens = dens[order]

    ax.scatter(
        x,
        y,
        c=dens,
        cmap="YlGnBu",
        s=1.0,
        alpha=0.55,
        linewidths=0,
        rasterized=True
    )

    ax.scatter(
        x[::9],
        y[::9],
        s=1.0,
        color="black",
        alpha=0.25,
        linewidths=0,
        rasterized=True
    )

    for _, r in arrow_df.iterrows():
        ax.annotate(
            "",
            xy=(r["x"], r["y"]),
            xytext=(0, 0),
            arrowprops=dict(
                arrowstyle="-|>",
                color="#e41a1c",
                linewidth=1.0,
                shrinkA=0,
                shrinkB=0,
                mutation_scale=6
            )
        )

        ax.text(
            r["x"] * 1.02,
            r["y"] * 1.02,
            r["variable"],
            fontsize=11,
            ha="center",
            va="center"
        )

    if habitat == "Native habitats":
        ellipse = Ellipse(
            xy=(-1.55, 2.25),
            width=1.55,
            height=1.05,
            angle=18,
            fill=False,
            edgecolor="#1b9e77",
            linewidth=1.2
        )
        ax.add_patch(ellipse)

    ax.set_xlim(-6.2, 8.2)
    ax.set_ylim(-5.8, 7.3)

    ax.set_title(habitat, fontsize=13, pad=7)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel("PC2 (21.6%)", fontsize=12)

    ax.grid(True, color="#e6e6e6", linewidth=0.6, alpha=0.65)
    ax.tick_params(labelsize=11)

    for spine in ax.spines.values():
        spine.set_linewidth(0.8)
        spine.set_color("#333333")


def plot_stack_panel(ax, habitat):
    sub = hfi_df[hfi_df["habitat"] == habitat]

    stack_order = [
        "12–50 (Very high pressure)",
        "6–11 (High pressure)",
        "3–5 (Moderate pressure)",
        "1–2 (Low pressure)",
        "0 (No pressure)",
    ]

    colors = {
        "0 (No pressure)": "#dff4e6",
        "1–2 (Low pressure)": "#49c2af",
        "3–5 (Moderate pressure)": "#3a88b5",
        "6–11 (High pressure)": "#443879",
        "12–50 (Very high pressure)": "#120a0a",
    }

    bottom = np.zeros(len(sub))
    x = sub["quantile"].to_numpy()

    for level in stack_order:
        ax.bar(
            x,
            sub[level].to_numpy(),
            bottom=bottom,
            width=8.6,
            color=colors[level],
            edgecolor="white",
            linewidth=0.8
        )
        bottom += sub[level].to_numpy()

    ax.set_xlim(-1, 101)
    ax.set_ylim(0, 105)
    ax.set_xticks(np.arange(0, 101, 10))
    ax.set_yticks([0, 25, 50, 75, 100])

    ax.set_title(habitat, fontsize=13, pad=7)
    ax.set_xlabel("Hotspot value quantile (%)", fontsize=12)
    ax.set_ylabel("Proportion (%)", fontsize=12)

    ax.grid(True, axis="y", color="#e6e6e6", linewidth=0.6, alpha=0.65)
    ax.tick_params(labelsize=11)

    for spine in ax.spines.values():
        spine.set_linewidth(0.8)
        spine.set_color("#333333")


# ============================================================
# 3. 基础样式
# ============================================================

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "axes.linewidth": 0.8,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "xtick.major.size": 3.5,
    "ytick.major.size": 3.5,
    "savefig.dpi": 300,
})


# ============================================================
# 4. 创建画布
# ============================================================

fig = plt.figure(figsize=(15.8, 8.8), dpi=130)

gs = fig.add_gridspec(
    nrows=3,
    ncols=6,
    width_ratios=[0.95, 0.95, 0.95, 0.26, 1.45, 1.45],
    height_ratios=[1, 1, 1],
    left=0.055,
    right=0.985,
    bottom=0.10,
    top=0.94,
    wspace=0.55,
    hspace=0.58
)

taxa = ["Amphibian", "Mammal", "Reptile"]

# 左侧 a-b-c 箱线图
box_axes = {}
for r in range(3):
    for c in range(3):
        box_axes[(r, c)] = fig.add_subplot(gs[r, c])

for c, taxon in enumerate(taxa):
    plot_box_panel(
        box_axes[(0, c)],
        box_df,
        taxon,
        "native_area",
        "log[Area of native\nhabitat (km$^2$)]",
        (6, 15 if taxon == "Amphibian" else 17),
        log_prop=False
    )

    plot_box_panel(
        box_axes[(1, c)],
        box_df,
        taxon,
        "unoccupied",
        "Proportion of\nunoccupied habitats",
        (0.003, 1.4),
        log_prop=True
    )

    plot_box_panel(
        box_axes[(2, c)],
        box_df,
        taxon,
        "isolated",
        "Proportion of\nisolated habitats",
        (0.003, 1.4),
        log_prop=True
    )

# 右侧 d PCA
gs_d = gs[0:2, 4:6].subgridspec(1, 2, wspace=0.24)
ax_d1 = fig.add_subplot(gs_d[0, 0])
ax_d2 = fig.add_subplot(gs_d[0, 1])

plot_pca_panel(ax_d1, "Native habitats", "PC1 (45.6%)")
plot_pca_panel(ax_d2, "Unoccupied habitats", "PC1 (43.6%)")

# 右侧 e 堆叠柱状图
gs_e = gs[2, 4:6].subgridspec(1, 2, wspace=0.27)
ax_e1 = fig.add_subplot(gs_e[0, 0])
ax_e2 = fig.add_subplot(gs_e[0, 1])

plot_stack_panel(ax_e1, "Native habitats")
plot_stack_panel(ax_e2, "Unoccupied habitats")


# ============================================================
# 5. 面板编号与图例
# ============================================================

box_axes[(0, 0)].text(
    -0.72, 1.13, "a",
    transform=box_axes[(0, 0)].transAxes,
    fontsize=16,
    fontweight="bold"
)

box_axes[(1, 0)].text(
    -0.72, 1.13, "b",
    transform=box_axes[(1, 0)].transAxes,
    fontsize=16,
    fontweight="bold"
)

box_axes[(2, 0)].text(
    -0.72, 1.13, "c",
    transform=box_axes[(2, 0)].transAxes,
    fontsize=16,
    fontweight="bold"
)

ax_d1.text(
    -0.16, 1.04, "d",
    transform=ax_d1.transAxes,
    fontsize=16,
    fontweight="bold"
)

ax_e1.text(
    -0.16, 1.08, "e",
    transform=ax_e1.transAxes,
    fontsize=16,
    fontweight="bold"
)

hfi_colors = {
    "0 (No pressure)": "#dff4e6",
    "1–2 (Low pressure)": "#49c2af",
    "3–5 (Moderate pressure)": "#3a88b5",
    "6–11 (High pressure)": "#443879",
    "12–50 (Very high pressure)": "#120a0a",
}

legend_handles = [
    Patch(facecolor=hfi_colors["0 (No pressure)"], edgecolor="none", label="0 (No pressure)"),
    Patch(facecolor=hfi_colors["1–2 (Low pressure)"], edgecolor="none", label="1–2 (Low pressure)"),
    Patch(facecolor=hfi_colors["3–5 (Moderate pressure)"], edgecolor="none", label="3–5 (Moderate pressure)"),
    Patch(facecolor=hfi_colors["6–11 (High pressure)"], edgecolor="none", label="6–11 (High pressure)"),
    Patch(facecolor=hfi_colors["12–50 (Very high pressure)"], edgecolor="none", label="12–50 (Very high pressure)"),
]

fig.legend(
    handles=legend_handles,
    title="HFI Levels",
    loc="lower center",
    bbox_to_anchor=(0.71, 0.015),
    ncol=3,
    frameon=False,
    fontsize=12,
    title_fontsize=12,
    handlelength=0.9,
    columnspacing=1.6,
    handletextpad=0.35
)


# ============================================================
# 6. 保存与显示
# ============================================================

plt.savefig(
    "reproduced_multispecies_habitat_pca_hfi.png",
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.04
)

plt.close(fig)
```

---

## 四、标签总结

```text
# 图片类型：复杂多面板生态统计图 / 箱线图 + PCA biplot + 堆叠百分比柱状图
# 图形结构：左侧 3×3 箱线图矩阵，右上 1×2 PCA 双标图，右下 1×2 堆叠柱状图
# Panel a：不同濒危等级下 native habitat 面积分布箱线图
# Panel b：不同濒危等级下 unoccupied habitats 比例箱线图
# Panel c：不同濒危等级下 isolated habitats 比例箱线图
# Panel d：Native habitats 与 Unoccupied habitats 的 PCA biplot
# Panel e：不同 hotspot value quantile 下 HFI levels 构成比例
# 适合数据类型：物种分布数据、栖息地面积数据、栖息地占用比例数据、PCA 降维结果、人类足迹分级组成数据
# 横轴变量：
# - Panel a-c：IUCN 威胁等级 VU、EN、CR
# - Panel d：PC1
# - Panel e：Hotspot value quantile
# 纵轴变量：
# - Panel a：log[Area of native habitat (km²)]
# - Panel b：Proportion of unoccupied habitats
# - Panel c：Proportion of isolated habitats
# - Panel d：PC2
# - Panel e：Proportion (%)
# 分组变量：
# - 物种类群：Amphibian、Mammal、Reptile
# - 威胁等级：VU、EN、CR
# - 栖息地类型：Native habitats、Unoccupied habitats
# - HFI Levels：0、1–2、3–5、6–11、12–50
# 配色方案：
# Panel a-c 箱线图：
# - VU：#e9ec3f
# - EN：#d78934
# - CR：#b51f26
# - 离群点：#bdbdbd
# - 坐标轴：#333333
# Panel d PCA 点云：
# - 点云密度 cmap：YlGnBu
# - YlGnBu 低值端：#ffffd9
# - YlGnBu 中值附近：#41b6c4
# - YlGnBu 高值端：#081d58
# - PCA 变量箭头：#e41a1c
# - 椭圆标注：#1b9e77
# - 网格线：#e6e6e6
# Panel e HFI 堆叠柱：
# - 0 (No pressure)：#dff4e6
# - 1–2 (Low pressure)：#49c2af
# - 3–5 (Moderate pressure)：#3a88b5
# - 6–11 (High pressure)：#443879
# - 12–50 (Very high pressure)：#120a0a
# - 柱间白色分隔线：#ffffff
# 背景：#ffffff
# 视觉风格：保护生物学 / 全球生态热点分析 / Nature 风格多面板统计图
# 推荐绘图库：matplotlib + pandas + numpy
# 复现难度：较高
```