---
rk_plotter_template: true
id: diverging_stack_total_depth_profile
title: 正负向堆叠柱状图（右侧 Total 独立小面板）+深度剖面折线图
category: bar_profile_combo
source_type: high_fidelity_markdown
template_path: templates/正负向堆叠柱状图（右侧 Total 独立小面板）+深度剖面折线图.md
trigger_phrases:
  - 正负向堆叠柱状图
  - 贡献分解和深度剖面
  - diverging stacked bar depth profile
tags:
  - diverging
  - stacked_bar
  - positive_negative
  - total_panel
  - depth_profile
  - multi_panel
data_profile:
  structure: signed_component_matrix_plus_depth_series
  required_fields:
    - groups
    - components
    - signed_values
    - depth
    - profile_value
  optional_fields:
    - total
    - units
    - category_order
style_profile:
  layout: bar_total_profile_composite
  aspect: wide
  primitives:
    - barh
    - stacked_bar
    - zero_line
    - line
    - inverted_depth_axis
  palette:
    - diverging_components
    - profile_line
dependencies:
  required:
    - numpy
    - pandas
    - matplotlib
  optional: []
best_for: 展示正负贡献分解，并关联一个深度或垂向剖面。
avoid_when: 所有值均为正且只需普通组成比例。
---

![[Pasted image 20260520001612.png]]
一、图像类型识别与结构拆解

这是一张**双面板组合图**，包含两个不同图型：

```text
Panel c：正负向堆叠柱状图 + 右侧 Total 独立小面板
Panel d：深度剖面折线图 / 反向深度轴累积质量曲线图
```

核心结构：

- **c 图**：
    
    - 横轴：塑料类型，`ABS、PS、PVC、PE、PP`，右侧单独一个 `Total` 小面板。
        
    - 左纵轴：`Proportion (%)`。
        
    - 正值部分：蓝色系，表示 buried carbon。
        
    - 负值部分：橙色系，表示 plastic mass。
        
    - 每个柱子上下均为堆叠结构。
        
    - 中间有 `y = 0` 水平基准线。
        
    - 右侧 Total 面板使用另一套量纲，右 y 轴为 `Mass (Tg)`。
        
- **d 图**：
    
    - 横轴：`Mass (Tg)`。
        
    - 纵轴：`Depth (m)`，在右侧显示，深度向下增加。
        
    - y 轴近似对数尺度，刻度为 `10、100、1,000、5,000`。
        
    - 多条曲线表示不同塑料类型在沉积物深度上的累积质量分布。
        
    - 黑线为 `Total`，其余为 `PF、PP、PVC、PS、ABS`。
        

---

## 二、单独的虚拟数据生成代码

```python
import numpy as np
import pandas as pd


def generate_panel_c_data():
    """
    Panel c 虚拟数据：
    正值为 buried carbon，单位为 %
    负值为 plastic proportion，单位为 %
    Total 面板单独用 Mass，单位 Tg
    """

    categories = ["ABS", "PS", "PVC", "PE", "PP"]

    df = pd.DataFrame({
        "type": categories,

        # 正向堆叠：buried carbon
        "carbon_sedimented": [3.5, 9.8, 5.8, 6.2, 10.5],
        "carbon_beached":    [3.0, 8.7, 4.8, 21.5, 24.0],

        # 负向堆叠：plastic
        "plastic_sedimented": [4.0, 8.5, 12.5, 6.3, 9.8],
        "plastic_beached":    [2.5, 7.2, 9.5, 18.8, 22.0],
    })

    total = pd.DataFrame({
        "type": ["Total"],
        "carbon_sedimented": [0.13],
        "carbon_beached":    [0.21],
        "plastic_sedimented": [0.18],
        "plastic_beached":    [0.27],
    })

    return df, total


def generate_panel_d_data():
    """
    Panel d 虚拟数据：
    深度单位 m，Mass 单位 Tg。
    y 轴为深度，向下增加；x 轴为累积沉积塑料质量。
    """

    depth = np.array([
        10, 15, 20, 30, 50, 80, 120, 200, 300, 500,
        800, 1200, 2000, 3000, 5000
    ])

    df = pd.DataFrame({
        "Depth": depth,
        "Total": [0.000, 0.006, 0.012, 0.020, 0.030, 0.120, 0.145, 0.150, 0.155, 0.165, 0.172, 0.175, 0.178, 0.179, 0.180],
        "PF":    [0.000, 0.004, 0.008, 0.012, 0.018, 0.026, 0.032, 0.036, 0.039, 0.041, 0.042, 0.043, 0.043, 0.043, 0.043],
        "PP":    [0.000, 0.003, 0.006, 0.010, 0.016, 0.022, 0.026, 0.028, 0.030, 0.032, 0.033, 0.034, 0.034, 0.034, 0.034],
        "PVC":   [0.000, 0.006, 0.012, 0.020, 0.030, 0.038, 0.044, 0.048, 0.052, 0.054, 0.055, 0.056, 0.056, 0.056, 0.056],
        "PS":    [0.000, 0.003, 0.007, 0.012, 0.020, 0.027, 0.031, 0.034, 0.036, 0.038, 0.039, 0.040, 0.040, 0.040, 0.040],
        "ABS":   [0.000, 0.002, 0.004, 0.006, 0.009, 0.012, 0.014, 0.015, 0.0155, 0.016, 0.016, 0.016, 0.016, 0.016, 0.016],
    })

    return df


if __name__ == "__main__":
    panel_c, panel_c_total = generate_panel_c_data()
    panel_d = generate_panel_d_data()

    print(panel_c)
    print(panel_c_total)
    print(panel_d.head())
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
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter


# ============================================================
# 1. 虚拟数据生成
# ============================================================

def generate_panel_c_data():
    categories = ["ABS", "PS", "PVC", "PE", "PP"]

    df = pd.DataFrame({
        "type": categories,
        "carbon_sedimented": [3.5, 9.8, 5.8, 6.2, 10.5],
        "carbon_beached":    [3.0, 8.7, 4.8, 21.5, 24.0],
        "plastic_sedimented": [4.0, 8.5, 12.5, 6.3, 9.8],
        "plastic_beached":    [2.5, 7.2, 9.5, 18.8, 22.0],
    })

    total = pd.DataFrame({
        "type": ["Total"],
        "carbon_sedimented": [0.13],
        "carbon_beached":    [0.21],
        "plastic_sedimented": [0.18],
        "plastic_beached":    [0.27],
    })

    return df, total


def generate_panel_d_data():
    depth = np.array([
        10, 15, 20, 30, 50, 80, 120, 200, 300, 500,
        800, 1200, 2000, 3000, 5000
    ])

    df = pd.DataFrame({
        "Depth": depth,
        "Total": [0.000, 0.006, 0.012, 0.020, 0.030, 0.120, 0.145, 0.150, 0.155, 0.165, 0.172, 0.175, 0.178, 0.179, 0.180],
        "PF":    [0.000, 0.004, 0.008, 0.012, 0.018, 0.026, 0.032, 0.036, 0.039, 0.041, 0.042, 0.043, 0.043, 0.043, 0.043],
        "PP":    [0.000, 0.003, 0.006, 0.010, 0.016, 0.022, 0.026, 0.028, 0.030, 0.032, 0.033, 0.034, 0.034, 0.034, 0.034],
        "PVC":   [0.000, 0.006, 0.012, 0.020, 0.030, 0.038, 0.044, 0.048, 0.052, 0.054, 0.055, 0.056, 0.056, 0.056, 0.056],
        "PS":    [0.000, 0.003, 0.007, 0.012, 0.020, 0.027, 0.031, 0.034, 0.036, 0.038, 0.039, 0.040, 0.040, 0.040, 0.040],
        "ABS":   [0.000, 0.002, 0.004, 0.006, 0.009, 0.012, 0.014, 0.015, 0.0155, 0.016, 0.016, 0.016, 0.016, 0.016, 0.016],
    })

    return df


df_c, df_total = generate_panel_c_data()
df_d = generate_panel_d_data()


# ============================================================
# 2. 基础样式
# ============================================================

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "axes.linewidth": 0.9,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.size": 4,
    "ytick.major.size": 4,
    "savefig.dpi": 300,
})

colors = {
    "carbon_beached": "#b7d2ec",
    "carbon_sedimented": "#4f93cf",
    "plastic_sedimented": "#f47f2c",
    "plastic_beached": "#f6c7a5",
}

line_colors = {
    "Total": "black",
    "PF": "#68aa45",
    "PP": "#f3b000",
    "PVC": "#f27f1b",
    "PS": "#9e9e9e",
    "ABS": "#4d8df7",
}


# ============================================================
# 3. 画布布局
# ============================================================

fig = plt.figure(figsize=(14.2, 4.3), dpi=120)

gs = fig.add_gridspec(
    nrows=1,
    ncols=4,
    width_ratios=[2.55, 0.70, 0.18, 1.90],
    wspace=0.10
)

ax_c = fig.add_subplot(gs[0, 0])
ax_total = fig.add_subplot(gs[0, 1])
ax_gap = fig.add_subplot(gs[0, 2])
ax_d = fig.add_subplot(gs[0, 3])

ax_gap.axis("off")


# ============================================================
# 4. Panel c：正负向堆叠柱状图
# ============================================================

x = np.arange(len(df_c))
bar_width = 0.38

# 正向：buried carbon
ax_c.bar(
    x,
    df_c["carbon_sedimented"],
    width=bar_width,
    color=colors["carbon_sedimented"],
    edgecolor="#666666",
    linewidth=0.8
)

ax_c.bar(
    x,
    df_c["carbon_beached"],
    bottom=df_c["carbon_sedimented"],
    width=bar_width,
    color=colors["carbon_beached"],
    edgecolor="#666666",
    linewidth=0.8
)

# 负向：plastic
ax_c.bar(
    x,
    -df_c["plastic_sedimented"],
    width=bar_width,
    color=colors["plastic_sedimented"],
    edgecolor="#666666",
    linewidth=0.8
)

ax_c.bar(
    x,
    -df_c["plastic_beached"],
    bottom=-df_c["plastic_sedimented"],
    width=bar_width,
    color=colors["plastic_beached"],
    edgecolor="#666666",
    linewidth=0.8
)

ax_c.axhline(0, color="#444444", lw=0.8)

ax_c.set_xlim(-1.0, len(df_c) - 0.45)
ax_c.set_ylim(-50, 50)

ax_c.set_xticks(x)
ax_c.set_xticklabels(df_c["type"], fontsize=13)

ax_c.set_yticks(np.arange(-40, 41, 10))
ax_c.yaxis.set_major_formatter(FuncFormatter(lambda y, pos: f"{abs(int(y))}"))

ax_c.set_ylabel("Proportion (%)", fontsize=13)
ax_c.tick_params(axis="y", labelsize=11)


# c 图图例
legend1 = [
    Patch(facecolor=colors["carbon_beached"], edgecolor="black",
          label="Buried carbon from beached plastic"),
    Patch(facecolor=colors["carbon_sedimented"], edgecolor="black",
          label="Buried carbon from sedimented plastic"),
]

leg1 = ax_c.legend(
    handles=legend1,
    loc="upper left",
    frameon=False,
    fontsize=13,
    handlelength=1.4,
    handleheight=0.9,
    borderpad=0.2,
    labelspacing=0.25
)

ax_c.add_artist(leg1)

legend2 = [
    Patch(facecolor=colors["plastic_sedimented"], edgecolor="black",
          label="Sedimented plastic"),
    Patch(facecolor=colors["plastic_beached"], edgecolor="black",
          label="Beached plastic"),
]

ax_c.legend(
    handles=legend2,
    loc="lower left",
    bbox_to_anchor=(0.02, 0.01),
    frameon=False,
    fontsize=13,
    handlelength=1.4,
    handleheight=0.9,
    borderpad=0.2,
    labelspacing=0.25
)

ax_c.text(
    -0.12,
    1.04,
    "c",
    transform=ax_c.transAxes,
    fontsize=16,
    fontweight="bold",
    ha="left"
)


# ============================================================
# 5. Panel c 右侧 Total 小面板
# ============================================================

x_total = [0]

ax_total.bar(
    x_total,
    df_total["carbon_sedimented"],
    width=0.34,
    color=colors["carbon_sedimented"],
    edgecolor="#666666",
    linewidth=0.8
)

ax_total.bar(
    x_total,
    df_total["carbon_beached"],
    bottom=df_total["carbon_sedimented"],
    width=0.34,
    color=colors["carbon_beached"],
    edgecolor="#666666",
    linewidth=0.8
)

ax_total.bar(
    x_total,
    -df_total["plastic_sedimented"],
    width=0.34,
    color=colors["plastic_sedimented"],
    edgecolor="#666666",
    linewidth=0.8
)

ax_total.bar(
    x_total,
    -df_total["plastic_beached"],
    bottom=-df_total["plastic_sedimented"],
    width=0.34,
    color=colors["plastic_beached"],
    edgecolor="#666666",
    linewidth=0.8
)

ax_total.axhline(0, color="#444444", lw=0.8)

ax_total.set_xlim(-0.6, 0.6)
ax_total.set_ylim(-0.5, 0.5)

ax_total.set_xticks([0])
ax_total.set_xticklabels(["Total"], fontsize=13)

ax_total.set_yticks([-0.4, -0.2, 0, 0.2, 0.4])
ax_total.yaxis.set_major_formatter(FuncFormatter(lambda y, pos: f"{abs(y):.1f}" if y != 0 else "0"))

ax_total.yaxis.tick_right()
ax_total.yaxis.set_label_position("right")
ax_total.set_ylabel("Mass (Tg)", fontsize=13, rotation=270, labelpad=22)
ax_total.tick_params(axis="y", labelsize=11)


# ============================================================
# 6. Panel d：深度剖面折线图
# ============================================================

for name in ["Total", "PF", "PP", "PVC", "PS", "ABS"]:
    ax_d.plot(
        df_d[name],
        df_d["Depth"],
        color=line_colors[name],
        lw=1.1,
        label=name
    )

ax_d.set_yscale("log")
ax_d.invert_yaxis()

ax_d.set_xlim(0, 0.20)
ax_d.set_ylim(5500, 10)

ax_d.set_xticks([0, 0.05, 0.10, 0.15, 0.20])
ax_d.set_xticklabels(["0", "0.05", "0.10", "0.15", "0.20"], fontsize=12)

ax_d.set_yticks([10, 100, 1000, 5000])
ax_d.set_yticklabels(["10", "100", "1,000", "5,000"], fontsize=12)

ax_d.yaxis.tick_right()
ax_d.yaxis.set_label_position("right")

ax_d.set_xlabel("Mass (Tg)", fontsize=14)
ax_d.set_ylabel("Depth (m)", fontsize=14, rotation=270, labelpad=22)

ax_d.text(
    0.50,
    0.98,
    "Cumulative sediment plastic mass",
    transform=ax_d.transAxes,
    ha="center",
    va="top",
    fontsize=14
)

ax_d.legend(
    loc="upper right",
    bbox_to_anchor=(0.98, 0.90),
    frameon=False,
    fontsize=12,
    handlelength=1.0,
    handletextpad=0.5,
    labelspacing=0.15
)

ax_d.text(
    -0.01,
    1.04,
    "d",
    transform=ax_d.transAxes,
    fontsize=16,
    fontweight="bold",
    ha="left"
)


# ============================================================
# 7. 边框与保存
# ============================================================

for ax in [ax_c, ax_total, ax_d]:
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.9)
        spine.set_color("#444444")

plt.subplots_adjust(
    left=0.055,
    right=0.975,
    bottom=0.20,
    top=0.92,
    wspace=0.10
)

plt.savefig(
    "reproduced_buried_carbon_sediment_mass.png",
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.04
)

plt.close(fig)
```

---

## 四、可调整参数说明

控制 c 图柱宽：

```python
bar_width = 0.38
```

控制 c 图上下比例范围：

```python
ax_c.set_ylim(-50, 50)
```

控制 Total 小图质量范围：

```python
ax_total.set_ylim(-0.5, 0.5)
```

控制 d 图深度轴：

```python
ax_d.set_yscale("log")
ax_d.invert_yaxis()
ax_d.set_yticks([10, 100, 1000, 5000])
```

控制 d 图曲线颜色：

```python
line_colors = {
    "Total": "black",
    "PF": "#68aa45",
    "PP": "#f3b000",
    "PVC": "#f27f1b",
    "PS": "#9e9e9e",
    "ABS": "#4d8df7",
}
```

---

## 五、标签总结

```text
# 图片类型：双面板组合图
# Panel c：正负向堆叠柱状图 / Diverging stacked bar chart
# Panel d：深度剖面折线图 / Cumulative mass-depth profile
# Panel c 数据类型：分类变量 + 正负方向组成比例 + 总量质量
# Panel d 数据类型：连续深度变量 + 累积质量变量 + 多类别塑料类型
# Panel c 横轴变量：ABS、PS、PVC、PE、PP、Total
# Panel c 左 y 轴变量：Proportion，单位 %
# Panel c 右 y 轴变量：Mass，单位 Tg
# Panel d 横轴变量：Mass，单位 Tg
# Panel d 纵轴变量：Depth，单位 m，对数反向轴
# 颜色编码：蓝色系表示 buried carbon，橙色系表示 plastic；黑/绿/黄/橙/灰/蓝表示不同塑料类型
# 视觉风格：环境科学论文多面板图、Nature 风格、白底、细边框
# 推荐绘图库：matplotlib + pandas + numpy
# 复现难度：中等
```