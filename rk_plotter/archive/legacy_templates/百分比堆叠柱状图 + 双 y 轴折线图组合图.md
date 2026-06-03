---
rk_plotter_template: true
id: stacked_percent_dual_axis_line
title: 百分比堆叠柱状图 + 双 y 轴折线图组合图
category: composition_timeseries_combo
source_type: high_fidelity_markdown
template_path: templates/百分比堆叠柱状图 + 双 y 轴折线图组合图.md
trigger_phrases:
  - 百分比堆叠柱状图 双y轴折线
  - 组成比例加趋势线
  - stacked percent dual axis line
tags:
  - composition
  - percent
  - stacked_bar
  - dual_axis
  - line
  - combo
data_profile:
  structure: groups_by_components_plus_secondary_series
  required_fields:
    - groups
    - components
    - percent_values
    - line_value
  optional_fields:
    - line_group
    - secondary_units
    - annotations
style_profile:
  layout: single_panel_twin_y
  aspect: wide
  primitives:
    - stacked_bar
    - line
    - twinx
    - legend
  palette:
    - composition_segments
    - secondary_lines
dependencies:
  required:
    - numpy
    - pandas
    - matplotlib
  optional: []
best_for: 展示组成比例变化并叠加一个相关总量或指数。
avoid_when: 两套 y 轴变量无明确关系或线条过多。
---

![[Pasted image 20260520001231.png]] 一、图像类型识别与结构拆解

这是一个**百分比堆叠柱状图 + 双 y 轴折线图组合图**。

图像结构：

```text
主图：不同体长 Body size 下，不同塑料类型的贡献比例
左 y 轴：Contribution ratio of different plastic types (%)
右 y 轴：Ingestion risk index
x 轴：Body size (mm)
柱状图：PP、PE、PVC、PS、ABS 五类塑料，百分比堆叠，总和为 100%
折线图：Epipelagic index、Migratory index、Mesopelagic index
图例：底部右侧，塑料类型色块 + 三条指数折线
```

---

## 二、单独的虚拟数据生成代码

```python
import numpy as np
import pandas as pd


def generate_body_size_plastic_data():
    """
    生成用于复现该图的虚拟数据。

    body_size: 体长，单位 mm
    PP, PE, PVC, PS, ABS: 不同塑料类型贡献比例，单位 %
    Epipelagic index, Migratory index, Mesopelagic index: 摄食风险指数
    """

    body_size = [
        1, 2, 3, 4, 6, 9, 13, 18, 27, 39,
        58, 84, 123, 180, 263, 385, 562, 823, 1203, 1759
    ]

    pp =  [0, 3, 2, 2, 3, 2, 1, 2, 2, 1, 1, 7, 7, 7, 25, 24, 25, 25, 25, 29]
    pe =  [0, 5, 4, 4, 4, 3, 3, 3, 4, 3, 2, 6, 5, 5, 23, 20, 18, 20, 19, 23]
    pvc = [50, 38, 44, 44, 44, 45, 46, 43, 44, 45, 47, 42, 43, 44, 25, 29, 30, 27, 30, 21]
    ps =  [35, 40, 35, 35, 35, 35, 35, 37, 35, 36, 36, 32, 32, 31, 19, 19, 19, 20, 18, 19]

    abs_ = [100 - a - b - c - d for a, b, c, d in zip(pp, pe, pvc, ps)]

    epipelagic =  [6.5, 6.0, 6.4, 5.6, 4.8, 4.2, 5.4, 4.9, 4.4, 3.9,
                   5.3, 5.4, 4.8, 4.3, 8.8, 7.8, 6.4, 4.9, 4.7, 6.9]

    migratory =   [3.7, 3.2, 3.3, 2.9, 2.6, 2.4, 2.8, 2.5, 2.3, 2.1,
                   2.6, 2.7, 2.5, 2.3, 3.9, 3.6, 3.1, 2.5, 2.3, 2.3]

    mesopelagic = [12.8, 6.4, 7.0, 7.2, 7.9, 8.5, 13.0, 13.0, 12.1, 10.6,
                   11.2, 8.8, 6.7, 5.2, 8.5, 6.0, 4.7, 3.5, 2.9, 8.8]

    df = pd.DataFrame({
        "Body size": body_size,
        "PP": pp,
        "PE": pe,
        "PVC": pvc,
        "PS": ps,
        "ABS": abs_,
        "Epipelagic index": epipelagic,
        "Migratory index": migratory,
        "Mesopelagic index": mesopelagic,
    })

    return df


df = generate_body_size_plastic_data()
print(df.head())
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
from matplotlib.patches import Rectangle


# ============================================================
# 1. 虚拟数据
# ============================================================

def generate_body_size_plastic_data():
    body_size = [
        1, 2, 3, 4, 6, 9, 13, 18, 27, 39,
        58, 84, 123, 180, 263, 385, 562, 823, 1203, 1759
    ]

    pp =  [0, 3, 2, 2, 3, 2, 1, 2, 2, 1, 1, 7, 7, 7, 25, 24, 25, 25, 25, 29]
    pe =  [0, 5, 4, 4, 4, 3, 3, 3, 4, 3, 2, 6, 5, 5, 23, 20, 18, 20, 19, 23]
    pvc = [50, 38, 44, 44, 44, 45, 46, 43, 44, 45, 47, 42, 43, 44, 25, 29, 30, 27, 30, 21]
    ps =  [35, 40, 35, 35, 35, 35, 35, 37, 35, 36, 36, 32, 32, 31, 19, 19, 19, 20, 18, 19]
    abs_ = [100 - a - b - c - d for a, b, c, d in zip(pp, pe, pvc, ps)]

    epipelagic =  [6.5, 6.0, 6.4, 5.6, 4.8, 4.2, 5.4, 4.9, 4.4, 3.9,
                   5.3, 5.4, 4.8, 4.3, 8.8, 7.8, 6.4, 4.9, 4.7, 6.9]

    migratory =   [3.7, 3.2, 3.3, 2.9, 2.6, 2.4, 2.8, 2.5, 2.3, 2.1,
                   2.6, 2.7, 2.5, 2.3, 3.9, 3.6, 3.1, 2.5, 2.3, 2.3]

    mesopelagic = [12.8, 6.4, 7.0, 7.2, 7.9, 8.5, 13.0, 13.0, 12.1, 10.6,
                   11.2, 8.8, 6.7, 5.2, 8.5, 6.0, 4.7, 3.5, 2.9, 8.8]

    return pd.DataFrame({
        "Body size": body_size,
        "PP": pp,
        "PE": pe,
        "PVC": pvc,
        "PS": ps,
        "ABS": abs_,
        "Epipelagic index": epipelagic,
        "Migratory index": migratory,
        "Mesopelagic index": mesopelagic,
    })


df = generate_body_size_plastic_data()


# ============================================================
# 2. 基础样式
# ============================================================

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "axes.linewidth": 1.0,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "xtick.major.size": 4,
    "ytick.major.size": 4,
    "savefig.dpi": 300,
})

plastic_colors = {
    "PP":  "#f6e6a6",
    "PE":  "#bed3df",
    "PVC": "#8bdbe4",
    "PS":  "#ddc5d1",
    "ABS": "#77799c",
}

line_colors = {
    "Epipelagic index":  "#ff7f00",
    "Migratory index":   "#d83418",
    "Mesopelagic index": "#2e5ca7",
}


# ============================================================
# 3. 创建画布
# ============================================================

fig, ax = plt.subplots(figsize=(11.0, 6.4), dpi=120)

x = np.arange(len(df))
bar_width = 0.62


# ============================================================
# 4. 百分比堆叠柱状图
# ============================================================

bottom = np.zeros(len(df))

for plastic in ["PP", "PE", "PVC", "PS", "ABS"]:
    ax.bar(
        x,
        df[plastic],
        bottom=bottom,
        width=bar_width,
        color=plastic_colors[plastic],
        edgecolor="white",
        linewidth=1.0,
        zorder=1
    )
    bottom += df[plastic].to_numpy()


# ============================================================
# 5. 右轴折线图
# ============================================================

ax2 = ax.twinx()

ax2.plot(
    x,
    df["Epipelagic index"],
    color=line_colors["Epipelagic index"],
    marker="o",
    markersize=8,
    linewidth=3.0,
    zorder=5
)

ax2.plot(
    x,
    df["Migratory index"],
    color=line_colors["Migratory index"],
    marker="^",
    markersize=9,
    linewidth=3.0,
    zorder=5
)

ax2.plot(
    x,
    df["Mesopelagic index"],
    color=line_colors["Mesopelagic index"],
    marker="o",
    markersize=5,
    linewidth=4.0,
    zorder=6
)


# ============================================================
# 6. 坐标轴设置
# ============================================================

ax.set_xlim(-0.5, len(df) - 0.35)
ax.set_ylim(0, 110)
ax2.set_ylim(0, 14)

ax.set_xticks(x)
ax.set_xticklabels(
    [f"{v:,}" for v in df["Body size"]],
    fontsize=10
)

ax.set_yticks(np.arange(0, 101, 10))
ax2.set_yticks(np.arange(1, 14, 1))

ax.set_ylabel("Contribution ratio of different plastic types (%)", fontsize=12)
ax2.set_ylabel("Ingestion risk index", fontsize=12, rotation=270, labelpad=18)
ax.set_xlabel("Body size (mm)", fontsize=12)

ax.tick_params(axis="y", labelsize=10)
ax2.tick_params(axis="y", labelsize=10)

# 边框风格：保留左右和底部，弱化顶部
ax.spines["top"].set_visible(False)
ax2.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

for spine in ["left", "bottom"]:
    ax.spines[spine].set_linewidth(1.0)
    ax.spines[spine].set_color("#333333")

ax2.spines["right"].set_linewidth(1.0)
ax2.spines["right"].set_color("#333333")

ax.grid(False)
ax2.grid(False)


# ============================================================
# 7. 自定义底部图例
# ============================================================

legend_ax = fig.add_axes([0.56, 0.015, 0.38, 0.15])
legend_ax.axis("off")

# 色块图例
box_y = 0.62
box_w = 0.145
box_h = 0.24
gap = 0.012

for i, name in enumerate(["PP", "PE", "PVC", "PS", "ABS"]):
    x0 = i * (box_w + gap)
    legend_ax.add_patch(
        Rectangle(
            (x0, box_y),
            box_w,
            box_h,
            facecolor=plastic_colors[name],
            edgecolor="none"
        )
    )
    legend_ax.text(
        x0 + box_w / 2,
        box_y + box_h / 2,
        name,
        ha="center",
        va="center",
        fontsize=11
    )

# 折线图例：第一行
legend_ax.plot(
    [0.00, 0.05],
    [0.35, 0.35],
    color=line_colors["Epipelagic index"],
    marker="o",
    markersize=4,
    linewidth=1.8,
    clip_on=False
)
legend_ax.text(
    0.07,
    0.35,
    "Epipelagic index",
    ha="left",
    va="center",
    fontsize=11
)

legend_ax.plot(
    [0.48, 0.53],
    [0.35, 0.35],
    color=line_colors["Mesopelagic index"],
    marker="o",
    markersize=3,
    linewidth=2.0,
    clip_on=False
)
legend_ax.text(
    0.55,
    0.35,
    "Mesopelagic index",
    ha="left",
    va="center",
    fontsize=11
)

# 折线图例：第二行
legend_ax.plot(
    [0.00, 0.05],
    [0.10, 0.10],
    color=line_colors["Migratory index"],
    marker="^",
    markersize=5,
    linewidth=1.8,
    clip_on=False
)
legend_ax.text(
    0.07,
    0.10,
    "Migratory index",
    ha="left",
    va="center",
    fontsize=11
)

legend_ax.set_xlim(-0.02, 1.05)
legend_ax.set_ylim(0, 1)


# ============================================================
# 8. 布局与保存
# ============================================================

plt.subplots_adjust(
    left=0.08,
    right=0.89,
    bottom=0.25,
    top=0.98
)

plt.savefig(
    "reproduced_plastic_contribution_ingestion_index.png",
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.04
)

plt.close(fig)
```

---

## 四、可调整参数说明

控制柱宽：

```python
bar_width = 0.62
```

控制右轴指数范围：

```python
ax2.set_ylim(0, 14)
ax2.set_yticks(np.arange(1, 14, 1))
```

控制五类塑料颜色：

```python
plastic_colors = {
    "PP":  "#f6e6a6",
    "PE":  "#bed3df",
    "PVC": "#8bdbe4",
    "PS":  "#ddc5d1",
    "ABS": "#77799c",
}
```

控制三条指数线的颜色和样式：

```python
line_colors = {
    "Epipelagic index":  "#ff7f00",
    "Migratory index":   "#d83418",
    "Mesopelagic index": "#2e5ca7",
}
```

---

## 五、标签总结

```text
# 图片类型：百分比堆叠柱状图 + 双 y 轴多折线图
# 图形结构：单面板组合图，柱状图表示组成比例，折线表示摄食风险指数
# 适合数据类型：分类体长数据、组成比例数据、风险指数数据
# x 轴变量：Body size，单位 mm
# 左 y 轴变量：Contribution ratio of different plastic types，单位 %
# 右 y 轴变量：Ingestion risk index
# 柱状图分组变量：PP、PE、PVC、PS、ABS
# 折线变量：Epipelagic index、Migratory index、Mesopelagic index
# 视觉编码：颜色表示塑料类型，线型和 marker 表示生态层指数
# 配色方案：浅黄、浅蓝、青色、粉紫、深蓝灰 + 橙/红/蓝折线
# 图例形式：底部右侧组合图例，色块图例与折线图例分离
# 视觉风格：环境科学论文组合图 / Nature 风格数据可视化
# 推荐绘图库：matplotlib + pandas + numpy
# 复现难度：中等
```