import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.lines import Line2D


# =========================================================
# 1. 基础设置
# =========================================================

np.random.seed(42)

fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")


# =========================================================
# 2. 工具函数
# =========================================================

def dashed_panel(ax, x, y, w, h, label=None, title=None,
                 lw=1.0, color="0.35", fontsize=12):
    """绘制虚线面板"""
    rect = Rectangle(
        (x, y), w, h,
        fill=False,
        edgecolor=color,
        linewidth=lw,
        linestyle=(0, (5, 3)),
        zorder=1
    )
    ax.add_patch(rect)

    if label is not None:
        ax.text(
            x + 0.005, y + h - 0.01,
            label,
            ha="left", va="top",
            fontsize=15, fontweight="bold"
        )

    if title is not None:
        ax.text(
            x + w / 2, y + h - 0.012,
            title,
            ha="center", va="top",
            fontsize=fontsize, fontweight="bold"
        )

    return rect


def add_round_box(ax, x, y, w, h, text, fc="#dfe7d4", ec="0.25",
                  fontsize=10.5, textcolor="black", lw=0.8,
                  boxstyle="round,pad=0.01,rounding_size=0.004",
                  z=3):
    """圆角文本框"""
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=boxstyle,
        facecolor=fc,
        edgecolor=ec,
        linewidth=lw,
        zorder=z
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2, y + h / 2,
        text,
        ha="center", va="center",
        fontsize=fontsize, color=textcolor, zorder=z + 1
    )
    return patch


def add_rect_box(ax, x, y, w, h, text, fc="#e8e8e8", ec="0.5",
                 fontsize=10.5, textcolor="black", lw=0.8, z=3):
    """普通矩形文本框"""
    patch = Rectangle(
        (x, y), w, h,
        facecolor=fc,
        edgecolor=ec,
        linewidth=lw,
        zorder=z
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2, y + h / 2,
        text,
        ha="center", va="center",
        fontsize=fontsize, color=textcolor, zorder=z + 1
    )
    return patch


def add_arrow(ax, x1, y1, x2, y2, color="0.2", lw=1.0,
              style="-|>", ms=10, z=4):
    """箭头"""
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style,
        mutation_scale=ms,
        linewidth=lw,
        color=color,
        shrinkA=0, shrinkB=0,
        zorder=z
    )
    ax.add_patch(arrow)
    return arrow


def add_line(ax, x1, y1, x2, y2, color="0.35", lw=0.9, ls="-", z=2):
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, ls=ls, zorder=z)


def ocean_like_image(nx=140, ny=70, seed=0):
    """生成海洋风格占位图"""
    rng = np.random.default_rng(seed)
    x = np.linspace(0, 4 * np.pi, nx)
    y = np.linspace(0, 3 * np.pi, ny)
    X, Y = np.meshgrid(x, y)

    img = (
        0.35 * np.sin(X * 0.8 + seed * 0.4) +
        0.30 * np.cos(Y * 1.3) +
        0.20 * np.sin((X + Y) * 0.7) +
        0.08 * rng.normal(size=(ny, nx))
    )
    img = (img - img.min()) / (img.max() - img.min())
    return img


def draw_map_thumb(ax, x, y, w, h, label, seed=0):
    """绘制小地图占位图"""
    img = ocean_like_image(seed=seed)
    ax.imshow(
        img, extent=[x, x + w, y, y + h],
        origin="lower", cmap="turbo", aspect="auto", zorder=1
    )

    # 岸线占位
    coast_x = np.linspace(x + 0.02 * w, x + 0.98 * w, 20)
    coast_y = y + 0.2 * h + 0.55 * h * np.abs(np.sin(np.linspace(0, 3, 20) + 0.4 * seed))
    ax.plot(coast_x, coast_y, color="black", lw=0.8, zorder=2)

    # 外边框
    ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor="white", linewidth=1.0, zorder=3))

    # 标签
    ax.text(
        x + w / 2, y + 0.01,
        label,
        ha="center", va="top",
        fontsize=10.5, fontweight="bold",
        bbox=dict(facecolor="white", alpha=0.75, edgecolor="none", pad=1.0),
        zorder=4
    )


def draw_ts_box(ax, x, y, w, h, n_series=2, missing=False,
                future=False, color1="royalblue", color2="tomato",
                show_border=True, seed=0):
    """绘制时间序列占位图"""
    rng = np.random.default_rng(seed)

    if show_border:
        ax.add_patch(Rectangle((x, y), w, h, facecolor="white",
                               edgecolor="0.75", linewidth=0.8, zorder=1))

    # 缺失值区域
    if missing:
        for _ in range(4):
            xm = x + rng.uniform(0.08, 0.88) * w
            ww = rng.uniform(0.03, 0.08) * w
            ax.add_patch(Rectangle((xm, y), ww, h, facecolor="0.88",
                                   edgecolor="none", zorder=1.5))

    for i in range(n_series):
        xs = np.linspace(x + 0.04 * w, x + 0.96 * w, 30)
        base = y + (0.25 + 0.28 * i) * h
        wave = 0.12 * h * np.sin(np.linspace(0, 2 * np.pi, 30) + rng.uniform(0, 2))
        noise = rng.normal(scale=0.035 * h, size=30)
        ys = base + wave + noise

        c = color1 if (i % 2 == 0 or n_series == 1) else color2
        if future:
            ys = base + 0.20 * h * np.exp(-((np.linspace(-2, 2, 30)) ** 2)) + 0.02 * h * rng.normal(size=30)
            c = "#597df5"

        ax.plot(xs, ys, color=c, lw=1.0, zorder=2)


def draw_small_scatter_map(ax, x, y, w, h, seed=0):
    """绘制带点位的空间坐标占位图"""
    img = ocean_like_image(seed=seed)
    ax.imshow(
        img, extent=[x, x + w, y, y + h],
        origin="lower", cmap="turbo", aspect="auto", zorder=1
    )
    coast_x = np.linspace(x + 0.02 * w, x + 0.98 * w, 25)
    coast_y = y + 0.18 * h + 0.60 * h * np.abs(np.sin(np.linspace(0, 3.1, 25) + 0.5))
    ax.plot(coast_x, coast_y, color="black", lw=0.8, zorder=2)

    rng = np.random.default_rng(seed)
    px = x + rng.uniform(0.08, 0.92, 12) * w
    py = y + rng.uniform(0.12, 0.88, 12) * h
    colors = ["red", "deepskyblue", "gold"]
    for i in range(12):
        ax.scatter(px[i], py[i], s=18, color=colors[i % 3], edgecolor="black", linewidth=0.4, zorder=3)

    ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor="white", linewidth=1.0, zorder=4))


def draw_model_pipeline(ax, x, y, w, h, title, final_label,
                        module_fc="#dfe7d4", proj_fc="#dbe3f5"):
    """绘制 Embed -> TLT -> HSGNN -> Projection 流程"""
    add_rect_box(ax, x, y, w, h, "", fc="#f3f3f3", ec="0.3", lw=0.8, z=1)

    modules = [
        ("Embed", x + 0.05 * w, 0.26 * w),
        ("TLT", x + 0.30 * w, 0.20 * w),
        ("HSGNN", x + 0.51 * w, 0.20 * w),
        (final_label, x + 0.74 * w, 0.21 * w),
    ]

    box_h = 0.38 * h
    box_y = y + 0.31 * h

    for label, bx, bw in modules:
        fc = proj_fc if label == final_label else module_fc
        add_round_box(ax, bx, box_y, bw, box_h, label, fc=fc, fontsize=9.5)

    # 箭头
    for i in range(3):
        (_, bx1, bw1) = modules[i]
        (_, bx2, bw2) = modules[i + 1]
        add_arrow(ax, bx1 + bw1, box_y + box_h / 2, bx2, box_y + box_h / 2, lw=0.9, ms=9)

    ax.text(x + w / 2, y + h - 0.01, title, ha="center", va="top",
            fontsize=11.5, fontweight="bold")


def draw_noise_icon(ax, x, y, w, h):
    xs = np.linspace(x, x + w, 80)
    center = x + w / 2
    sigma = 0.18 * w
    ys = y + 0.1 * h + 0.75 * h * np.exp(-((xs - center) ** 2) / (2 * sigma ** 2))
    ax.plot(xs, ys, color="#8a8ab8", lw=1.0)


def draw_graph_icon(ax, x, y, w, h):
    pts = np.array([
        [x + 0.18 * w, y + 0.25 * h],
        [x + 0.48 * w, y + 0.74 * h],
        [x + 0.80 * w, y + 0.40 * h],
        [x + 0.55 * w, y + 0.18 * h],
    ])
    edges = [(0, 1), (1, 2), (0, 3), (3, 2)]
    for i, j in edges:
        ax.plot([pts[i, 0], pts[j, 0]], [pts[i, 1], pts[j, 1]], color="0.3", lw=0.8)
    for p in pts:
        ax.add_patch(Circle((p[0], p[1]), 0.012 * w, facecolor="#ff6b6b", edgecolor="black", lw=0.6))


# =========================================================
# 3. 主面板布局
# =========================================================

# a
xa, ya, wa, ha = 0.015, 0.67, 0.97, 0.31
dashed_panel(ax, xa, ya, wa, ha, label="a")

# b
xb, yb, wb, hb = 0.015, 0.40, 0.97, 0.22
dashed_panel(ax, xb, yb, wb, hb, label="b", title="Task")

# c
xc, yc, wc, hc = 0.015, 0.04, 0.20, 0.31
dashed_panel(ax, xc, yc, wc, hc, label="c", title="Inputs")

# d
xd, yd, wd, hd = 0.24, 0.18, 0.52, 0.17
dashed_panel(ax, xd, yd, wd, hd, label="d", title="Imputation")

# e
xe, ye, we, he = 0.24, 0.04, 0.52, 0.14
dashed_panel(ax, xe, ye, we, he, label="e", title="Prediction")

# f
xf, yf, wf, hf = 0.79, 0.04, 0.19, 0.31
dashed_panel(ax, xf, yf, wf, hf, label="f", title="Outputs")


# =========================================================
# 4. a 面板：研究区域
# =========================================================

# 中央世界示意底图占位
world_x, world_y, world_w, world_h = 0.17, 0.71, 0.66, 0.22
add_rect_box(ax, world_x, world_y, world_w, world_h, "",
             fc="#f4f4f4", ec="none", z=0)

# 轻微“大陆”占位块
for bx, by, bw, bh in [
    (world_x + 0.03, world_y + 0.10, 0.18, 0.10),
    (world_x + 0.23, world_y + 0.12, 0.14, 0.08),
    (world_x + 0.45, world_y + 0.11, 0.20, 0.11),
]:
    ax.add_patch(Rectangle((bx, by), bw, bh, facecolor="0.87", edgecolor="none", zorder=1))

# 四个区域小图
draw_map_thumb(ax, 0.16, 0.74, 0.21, 0.08, "Northern Gulf of Mexico", seed=1)
draw_map_thumb(ax, 0.39, 0.82, 0.12, 0.12, "Chesapeake Bay", seed=2)
draw_map_thumb(ax, 0.50, 0.69, 0.18, 0.13, "Pearl River Estuary", seed=3)
draw_map_thumb(ax, 0.72, 0.74, 0.11, 0.16, "Yangtze River Estuary", seed=4)

# 与中心世界示意连线
for (x1, y1, x2, y2) in [
    (0.26, 0.82, 0.33, 0.86),
    (0.45, 0.82, 0.41, 0.90),
    (0.59, 0.82, 0.57, 0.77),
    (0.76, 0.82, 0.70, 0.87),
]:
    add_line(ax, x1, y1, x2, y2, color="0.25", lw=0.9, ls=(0, (5, 3)))

# 顶部到下部面板 b 的虚线引导
add_line(ax, 0.40, 0.67, 0.06, 0.62, color="0.35", lw=1.0, ls=(0, (4, 3)))
add_line(ax, 0.60, 0.67, 0.98, 0.62, color="0.35", lw=1.0, ls=(0, (4, 3)))


# =========================================================
# 5. b 面板：任务定义
# =========================================================

# 左：Past Observation
ax.text(0.08, 0.58, "Past Observation", fontsize=10.5, fontweight="bold")
for i in range(4):
    x0 = 0.05 + i * 0.038
    y0 = 0.47 + i * 0.006
    draw_map_thumb(ax, x0, y0, 0.05, 0.10, "", seed=10 + i)
    ax.text(x0 + 0.038, y0 + 0.03, str(i + 1), color="white", fontsize=9, fontweight="bold")
# 省略号
ax.text(0.20, 0.52, "...", fontsize=16)

# 中：Prediction of Future Chl_a
ax.text(0.25, 0.58, "Prediction of Future Chl_a", fontsize=10.5, fontweight="bold")
for i in range(4):
    x0 = 0.24 + i * 0.038
    y0 = 0.47 + i * 0.006
    draw_map_thumb(ax, x0, y0, 0.05, 0.10, "", seed=20 + i)
    ax.text(x0 + 0.039, y0 + 0.07, "?", color="red", fontsize=11, fontweight="bold")

# 空间/时间关系箭头
add_arrow(ax, 0.13, 0.53, 0.34, 0.53, color="#ba7b2b", lw=1.1, ms=10)
add_arrow(ax, 0.13, 0.51, 0.34, 0.51, color="black", lw=0.9, ms=9)

# 右：时间窗
task_box_x, task_box_y, task_box_w, task_box_h = 0.42, 0.47, 0.38, 0.065
add_rect_box(ax, task_box_x, task_box_y, task_box_w, task_box_h, "",
             fc="white", ec="0.25", lw=0.8)

# 缺失值竖条
for xx in [0.47, 0.51, 0.57, 0.60, 0.64, 0.70]:
    ax.add_patch(Rectangle((xx, task_box_y), 0.008, task_box_h,
                           facecolor="0.85", edgecolor="none", zorder=2))

# 红色折线
xs = np.linspace(task_box_x + 0.01, task_box_x + task_box_w * 0.56, 18)
rng = np.random.default_rng(100)
ys = task_box_y + task_box_h * (0.15 + 0.70 * rng.random(len(xs)))
ax.plot(xs, ys, color="red", lw=0.8, zorder=3)

# 预测区说明
ax.text(task_box_x + task_box_w * 0.75, task_box_y + task_box_h / 2,
        "Future Chl_a to be Predicted", ha="center", va="center",
        fontsize=8.5, fontweight="bold")

# 图例
legend_x, legend_y, legend_w, legend_h = 0.81, 0.48, 0.17, 0.09
add_round_box(ax, legend_x, legend_y, legend_w, legend_h, "",
              fc="white", ec="0.35", fontsize=9, z=1)
# missing
ax.add_patch(Rectangle((legend_x + 0.015, legend_y + 0.057), 0.028, 0.012,
                       facecolor="0.85", edgecolor="none", zorder=3))
ax.text(legend_x + 0.05, legend_y + 0.063, "Missing Values", va="center", fontsize=8.3, fontweight="bold")
# spatial
add_arrow(ax, legend_x + 0.015, legend_y + 0.039, legend_x + 0.045, legend_y + 0.039, color="black", lw=0.8, ms=7)
ax.text(legend_x + 0.05, legend_y + 0.039, "Spatial Relationships", va="center", fontsize=8.3, fontweight="bold")
# temporal
add_arrow(ax, legend_x + 0.015, legend_y + 0.017, legend_x + 0.045, legend_y + 0.017, color="#ba7b2b", lw=0.8, ms=7)
ax.text(legend_x + 0.05, legend_y + 0.017, "Temporal Relationships", va="center", fontsize=8.3, fontweight="bold")


# =========================================================
# 6. c 面板：Inputs
# =========================================================

ax.text(xc + wc / 2, yc + hc - 0.05, "Past Observation\nwith Missing Value",
        ha="center", va="top", fontsize=10.5, fontweight="bold")

for i, lab in enumerate(["①", "②", "⋮", "N"]):
    yy = yc + hc - 0.11 - i * 0.04
    if i == 2:
        ax.text(xc + 0.01, yy + 0.012, lab, fontsize=12, ha="left", va="center")
    else:
        ax.text(xc + 0.01, yy + 0.012, lab, fontsize=10, ha="left", va="center")
    draw_ts_box(ax, xc + 0.03, yy, wc - 0.055, 0.028, n_series=2, missing=True, seed=200 + i)

ax.text(xc + wc / 2, yc + 0.11, "Spatial Coordinates",
        ha="center", va="center", fontsize=10.5, fontweight="bold")
draw_small_scatter_map(ax, xc + 0.025, yc + 0.02, wc - 0.05, 0.09, seed=12)

# 从 c 到 d/e 的箭头
add_arrow(ax, xc + wc + 0.005, yc + 0.17, xd - 0.003, yd + hd / 2, lw=1.0, ms=13)
add_arrow(ax, xc + wc + 0.005, yc + 0.11, xe - 0.003, ye + he / 2, lw=1.0, ms=13)


# =========================================================
# 7. d 面板：Imputation
# =========================================================

ax.text(xd + wd / 2, yd + hd - 0.045, "STDDM",
        ha="center", va="center", fontsize=11.5, fontweight="bold")

# 输入输出小图
draw_ts_box(ax, xd + 0.01, yd + 0.085, 0.08, 0.04, n_series=2, missing=True, seed=301)
draw_ts_box(ax, xd + wd - 0.09, yd + 0.085, 0.08, 0.04, n_series=2, missing=False, seed=302)

# 模型
draw_model_pipeline(ax, xd + 0.11, yd + 0.035, wd - 0.22, 0.085,
                    title="", final_label="Imputation\nProjection")

# 左右箭头
add_arrow(ax, xd + 0.09, yd + 0.105, xd + 0.11, yd + 0.105, lw=0.9, ms=10)
add_arrow(ax, xd + wd - 0.11, yd + 0.105, xd + wd - 0.09, yd + 0.105, lw=0.9, ms=10)

# 噪声与空间图
draw_noise_icon(ax, xd + 0.12, yd + 0.010, 0.06, 0.025)
ax.text(xd + 0.19, yd + 0.018, "Gaussian Noise", fontsize=10.5, fontweight="bold", va="center")
draw_graph_icon(ax, xd + 0.30, yd + 0.005, 0.06, 0.03)
ax.text(xd + 0.37, yd + 0.018, "Spatial Graph", fontsize=10.5, fontweight="bold", va="center")

# 上连模型
add_line(ax, xd + 0.15, yd + 0.035, xd + 0.15, yd + 0.08, color="0.25", lw=0.8)
add_line(ax, xd + 0.31, yd + 0.035, xd + 0.31, yd + 0.08, color="0.25", lw=0.8)


# =========================================================
# 8. e 面板：Prediction
# =========================================================

draw_ts_box(ax, xe + 0.01, ye + 0.04, 0.09, 0.055, n_series=2, missing=False, seed=401)
draw_ts_box(ax, xe + we - 0.09, ye + 0.04, 0.08, 0.055, n_series=2, future=True, seed=402)

draw_model_pipeline(ax, xe + 0.12, ye + 0.02, we - 0.24, 0.08,
                    title="", final_label="Prediction\nProjection")
ax.text(xe + we / 2, ye + 0.01, "Prediction Model", ha="center",
        va="bottom", fontsize=11, fontweight="bold")

add_arrow(ax, xe + 0.10, ye + 0.067, xe + 0.12, ye + 0.067, lw=0.9, ms=10)
add_arrow(ax, xe + we - 0.12, ye + 0.067, xe + we - 0.09, ye + 0.067, lw=0.9, ms=10)

# d 到 e 竖向箭头
add_arrow(ax, xd + wd / 2, yd, xe + we / 2, ye + he, lw=0.9, ms=10)


# =========================================================
# 9. f 面板：Outputs
# =========================================================

ax.text(xf + wf / 2, yf + hf - 0.07, "Impute Past Observation",
        ha="center", va="center", fontsize=10.5, fontweight="bold")
for i in range(3):
    draw_ts_box(ax, xf + 0.03, yf + hf - 0.11 - i * 0.045, wf - 0.06, 0.03,
                n_series=2, missing=False, seed=500 + i)

ax.text(xf + wf / 2, yf + 0.11, "Predict Future Chl_a",
        ha="center", va="center", fontsize=10.5, fontweight="bold")
for i in range(3):
    draw_ts_box(ax, xf + 0.03, yf + 0.07 - i * 0.045, wf - 0.06, 0.03,
                n_series=1, future=True, seed=600 + i)

# e/d 到 f 箭头
add_arrow(ax, xe + we + 0.005, ye + 0.07, xf - 0.004, yf + 0.14, lw=1.0, ms=13)
add_arrow(ax, xd + wd + 0.005, yd + 0.07, xf - 0.004, yf + 0.19, lw=1.0, ms=13)


# =========================================================
# 10. 保存与显示
# =========================================================

plt.savefig("stimp_overview_framework.png", dpi=300, bbox_inches="tight", pad_inches=0.05)
plt.savefig("stimp_overview_framework.pdf", bbox_inches="tight", pad_inches=0.05)
# Interactive display is disabled for reusable skill assets.
plt.close("all")