# -*- coding: utf-8 -*-
"""AC/DC、零件符號、NPN 開關教學圖 — 跟 dat-logic-tutor 白底粗線畫風。"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (
    FancyBboxPatch, Circle, Rectangle, FancyArrowPatch,
    Arc, Polygon, Ellipse,
)
from matplotlib import font_manager

font_manager.fontManager.addfont("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
font_manager.fontManager.addfont("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc")
plt.rcParams["font.family"] = "Noto Sans CJK TC"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["mathtext.fontset"] = "dejavusans"

OUT = "/workspace/dat-elec-3col/assets"
os.makedirs(OUT, exist_ok=True)

NAVY = "#1B3A4B"
ORANGE = "#E07A1F"
TEAL = "#1F6F5B"
RED = "#B23A3A"
INK = "#222222"
LINE = "#1A1A1A"
PALE = "#F4F7FA"
CREAM = "#FFF6EC"
MINT = "#EEF7F3"


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=200, bbox_inches="tight", pad_inches=0.28, facecolor="white")
    plt.close(fig)
    print(name, os.path.getsize(path))


def zh(ax, x, y, s, size=13, color=INK, ha="center", va="center", weight="regular"):
    ax.text(x, y, s, ha=ha, va=va, fontsize=size, color=color, fontweight=weight)


def math(ax, x, y, s, size=16, color=INK, ha="center", va="center", weight="regular"):
    ax.text(x, y, s, ha=ha, va=va, fontsize=size, color=color, fontweight=weight)


def box(ax, x, y, w, h, ec=NAVY, fc="white", lw=2.2, r=0.08):
    p = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.012,rounding_size={r}",
        facecolor=fc, edgecolor=ec, linewidth=lw,
    )
    ax.add_patch(p)
    return p


# =============================================================================
# 1. ac_dc_wave.png
# =============================================================================
def make_ac_dc_wave():
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 6.2))
    fig.patch.set_facecolor("white")
    fig.suptitle("交流電 AC  vs  直流電 DC", fontsize=20, color=NAVY, fontweight="bold", y=0.98)

    # --- Left: AC sine ---
    ax = axes[0]
    ax.set_facecolor(CREAM)
    t = np.linspace(0, 2 * np.pi, 400)
    v = np.sin(t)
    ax.plot(t, v, color=ORANGE, lw=2.8, zorder=3)
    ax.axhline(0, color=LINE, lw=1.4, zorder=2)
    ax.axvline(0, color=LINE, lw=1.0, alpha=0.5)

    # peak Vm
    ax.plot([np.pi / 2], [1.0], "o", color=RED, ms=8, zorder=4)
    ax.annotate(
        r"$V_m$", xy=(np.pi / 2, 1.0), xytext=(np.pi / 2 + 0.55, 1.15),
        fontsize=15, color=RED, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=RED, lw=1.8),
    )
    # trough
    ax.plot([3 * np.pi / 2], [-1.0], "o", color=RED, ms=7, zorder=4)
    ax.annotate(
        r"$-V_m$", xy=(3 * np.pi / 2, -1.0), xytext=(3 * np.pi / 2 + 0.35, -1.25),
        fontsize=13, color=RED,
        arrowprops=dict(arrowstyle="->", color=RED, lw=1.5),
    )
    # zero crossings
    for zx in (0, np.pi, 2 * np.pi):
        ax.plot([zx], [0], "o", color=TEAL, ms=6, zorder=4)
    ax.annotate(
        "過零", xy=(np.pi, 0), xytext=(np.pi + 0.15, 0.45),
        fontsize=11, color=TEAL,
        arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.4),
    )
    # period T double arrow
    ax.annotate(
        "", xy=(2 * np.pi, -1.45), xytext=(0, -1.45),
        arrowprops=dict(arrowstyle="<->", color=NAVY, lw=2.0),
    )
    ax.text(np.pi, -1.62, r"週期 $T$", ha="center", va="top", fontsize=13, color=NAVY, fontweight="bold")

    ax.set_xlim(-0.35, 2 * np.pi + 0.45)
    ax.set_ylim(-1.85, 1.55)
    ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
    ax.set_xticklabels(["0", r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$"], fontsize=11)
    ax.set_yticks([-1, 0, 1])
    ax.set_yticklabels([r"$-V_m$", "0", r"$V_m$"], fontsize=11)
    ax.set_xlabel("時間", fontsize=13, color=INK)
    ax.set_ylabel("電壓", fontsize=13, color=INK)
    ax.set_title("交流電 AC", fontsize=16, color=ORANGE, fontweight="bold", pad=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_linewidth(2.0)
        ax.spines[sp].set_color(LINE)
    ax.tick_params(width=1.6, length=5)
    math(ax, np.pi, 1.38, r"$v = V_m\sin(\omega t)$", size=14, color=NAVY)

    # --- Right: DC flat ---
    ax = axes[1]
    ax.set_facecolor(MINT)
    t2 = np.linspace(0, 2 * np.pi, 50)
    vdc = np.ones_like(t2) * 0.75
    ax.plot(t2, vdc, color=TEAL, lw=3.0, zorder=3)
    ax.axhline(0, color=LINE, lw=1.4, zorder=2)
    ax.axvline(0, color=LINE, lw=1.0, alpha=0.5)
    ax.fill_between(t2, 0, vdc, color=TEAL, alpha=0.12, zorder=1)

    ax.annotate(
        "穩定電壓", xy=(np.pi, 0.75), xytext=(np.pi * 0.55, 1.2),
        fontsize=14, color=TEAL, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.8),
    )
    math(ax, np.pi * 1.35, 0.75 + 0.22, r"$V$", size=15, color=TEAL)

    ax.set_xlim(-0.35, 2 * np.pi + 0.45)
    ax.set_ylim(-0.55, 1.55)
    ax.set_xticks([0, np.pi, 2 * np.pi])
    ax.set_xticklabels(["0", r"$\pi$", r"$2\pi$"], fontsize=11)
    ax.set_yticks([0, 0.75])
    ax.set_yticklabels(["0", r"$V$"], fontsize=12)
    ax.set_xlabel("時間", fontsize=13, color=INK)
    ax.set_ylabel("電壓", fontsize=13, color=INK)
    ax.set_title("直流電 DC", fontsize=16, color=TEAL, fontweight="bold", pad=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_linewidth(2.0)
        ax.spines[sp].set_color(LINE)
    ax.tick_params(width=1.6, length=5)

    fig.text(
        0.5, 0.02,
        "AC：方向／大小隨時間變　　DC：方向同大小大致不變",
        ha="center", va="bottom", fontsize=13, color=INK,
    )
    fig.tight_layout(rect=[0, 0.06, 1, 0.93])
    save(fig, "ac_dc_wave.png")


# =============================================================================
# 2. parts_symbols.png  — IEC-ish schematic symbols
# =============================================================================
def _resistor(ax, cx, cy, horiz=True, scale=1.0):
    """Zigzag resistor centered at (cx, cy)."""
    lw = 2.4
    if horiz:
        n = 6
        xs, ys = [], []
        w = 0.95 * scale
        h = 0.22 * scale
        x0 = cx - w / 2
        step = w / n
        xs.append(x0)
        ys.append(cy)
        for i in range(n):
            xs.append(x0 + (i + 0.5) * step)
            ys.append(cy + (h if i % 2 == 0 else -h))
        xs.append(x0 + w)
        ys.append(cy)
        # lead lines
        ax.plot([cx - w / 2 - 0.35 * scale, x0], [cy, cy], color=LINE, lw=lw)
        ax.plot([x0 + w, cx + w / 2 + 0.35 * scale], [cy, cy], color=LINE, lw=lw)
        ax.plot(xs, ys, color=LINE, lw=lw)
    else:
        n = 6
        w = 0.22 * scale
        h = 0.95 * scale
        y0 = cy - h / 2
        step = h / n
        xs, ys = [cx], [y0]
        for i in range(n):
            xs.append(cx + (w if i % 2 == 0 else -w))
            ys.append(y0 + (i + 0.5) * step)
        xs.append(cx)
        ys.append(y0 + h)
        ax.plot([cx, cx], [cy - h / 2 - 0.35 * scale, y0], color=LINE, lw=lw)
        ax.plot([cx, cx], [y0 + h, cy + h / 2 + 0.35 * scale], color=LINE, lw=lw)
        ax.plot(xs, ys, color=LINE, lw=lw)


def _potentiometer(ax, cx, cy, scale=1.0):
    """Resistor with arrow tap (VR)."""
    _resistor(ax, cx, cy, horiz=True, scale=scale)
    # arrow from below to mid
    ax.annotate(
        "", xy=(cx, cy + 0.08 * scale), xytext=(cx, cy - 0.55 * scale),
        arrowprops=dict(arrowstyle="->", color=LINE, lw=2.2, mutation_scale=14),
    )


def _thermistor(ax, cx, cy, scale=1.0):
    """Resistor with diagonal bar (NTC)."""
    _resistor(ax, cx, cy, horiz=True, scale=scale)
    # diagonal slash through body
    ax.plot(
        [cx - 0.55 * scale, cx + 0.25 * scale],
        [cy - 0.45 * scale, cy + 0.5 * scale],
        color=LINE, lw=2.4,
    )


def _ldr(ax, cx, cy, scale=1.0):
    """Resistor in circle with light arrows (LDR)."""
    _resistor(ax, cx, cy, horiz=True, scale=0.75 * scale)
    r = 0.55 * scale
    ax.add_patch(Circle((cx, cy), r, fill=False, ec=LINE, lw=2.2))
    # light arrows from top-left
    for dy in (0.15, -0.05):
        ax.annotate(
            "", xy=(cx - 0.2 * scale, cy + 0.15 * scale + dy),
            xytext=(cx - 0.95 * scale, cy + 0.55 * scale + dy),
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.0, mutation_scale=12),
        )


def _capacitor(ax, cx, cy, scale=1.0):
    """Two parallel plates."""
    lw = 2.6
    gap = 0.12 * scale
    h = 0.45 * scale
    ax.plot([cx - gap, cx - gap], [cy - h, cy + h], color=LINE, lw=lw)
    ax.plot([cx + gap, cx + gap], [cy - h, cy + h], color=LINE, lw=lw)
    ax.plot([cx - 0.55 * scale, cx - gap], [cy, cy], color=LINE, lw=2.4)
    ax.plot([cx + gap, cx + 0.55 * scale], [cy, cy], color=LINE, lw=2.4)


def _diode(ax, cx, cy, scale=1.0):
    """Triangle + bar, current left→right."""
    lw = 2.4
    s = 0.32 * scale
    tri = Polygon(
        [(cx - s, cy - s), (cx - s, cy + s), (cx + s * 0.85, cy)],
        closed=True, facecolor=LINE, edgecolor=LINE, lw=1.5,
    )
    ax.add_patch(tri)
    ax.plot([cx + s * 0.85, cx + s * 0.85], [cy - s, cy + s], color=LINE, lw=2.8)
    ax.plot([cx - 0.55 * scale, cx - s], [cy, cy], color=LINE, lw=lw)
    ax.plot([cx + s * 0.85, cx + 0.55 * scale], [cy, cy], color=LINE, lw=lw)


def _led(ax, cx, cy, scale=1.0):
    """Diode + light arrows."""
    _diode(ax, cx, cy, scale=scale)
    for i, dy in enumerate((0.35, 0.55)):
        ax.annotate(
            "", xy=(cx + 0.15 * scale + i * 0.08, cy + 0.75 * scale),
            xytext=(cx - 0.05 * scale + i * 0.08, cy + 0.35 * scale),
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.0, mutation_scale=11),
        )


def _switch(ax, cx, cy, scale=1.0):
    """Open switch (SPST)."""
    lw = 2.4
    ax.plot([cx - 0.55 * scale, cx - 0.18 * scale], [cy, cy], color=LINE, lw=lw)
    ax.plot([cx + 0.18 * scale, cx + 0.55 * scale], [cy, cy], color=LINE, lw=lw)
    ax.add_patch(Circle((cx - 0.18 * scale, cy), 0.07 * scale, fc="white", ec=LINE, lw=2.0, zorder=3))
    ax.add_patch(Circle((cx + 0.18 * scale, cy), 0.07 * scale, fc="white", ec=LINE, lw=2.0, zorder=3))
    # open blade
    ax.plot(
        [cx - 0.18 * scale, cx + 0.22 * scale],
        [cy, cy + 0.35 * scale],
        color=LINE, lw=lw,
    )


def _relay(ax, cx, cy, scale=1.0):
    """Simple coil (rectangle) + contact above."""
    lw = 2.2
    # coil box
    w, h = 0.55 * scale, 0.35 * scale
    ax.add_patch(Rectangle((cx - w / 2, cy - h / 2 - 0.15 * scale), w, h,
                           fill=False, ec=LINE, lw=lw))
    # coil zigzag inside
    xs = np.linspace(cx - w / 2 + 0.05, cx + w / 2 - 0.05, 7)
    ys = [cy - 0.15 * scale + (0.1 if i % 2 else -0.1) * scale for i in range(7)]
    ax.plot(xs, ys, color=LINE, lw=1.8)
    # leads
    ax.plot([cx - w / 2 - 0.3 * scale, cx - w / 2], [cy - 0.15 * scale, cy - 0.15 * scale], color=LINE, lw=lw)
    ax.plot([cx + w / 2, cx + w / 2 + 0.3 * scale], [cy - 0.15 * scale, cy - 0.15 * scale], color=LINE, lw=lw)
    # contact (NO) above with dashed link
    ax.plot([cx - 0.25 * scale, cx - 0.25 * scale], [cy + 0.15 * scale, cy + 0.55 * scale], color=LINE, lw=lw)
    ax.plot([cx + 0.25 * scale, cx + 0.25 * scale], [cy + 0.15 * scale, cy + 0.55 * scale], color=LINE, lw=lw)
    ax.add_patch(Circle((cx - 0.25 * scale, cy + 0.55 * scale), 0.06 * scale, fc="white", ec=LINE, lw=1.8))
    ax.add_patch(Circle((cx + 0.25 * scale, cy + 0.55 * scale), 0.06 * scale, fc="white", ec=LINE, lw=1.8))
    ax.plot([cx - 0.25 * scale, cx + 0.18 * scale], [cy + 0.55 * scale, cy + 0.72 * scale], color=LINE, lw=lw)
    # dashed mechanical link
    ax.plot([cx, cx], [cy + h / 2 - 0.15 * scale, cy + 0.55 * scale], color=TEAL, lw=1.6, ls="--")


def _transformer(ax, cx, cy, scale=1.0):
    """Two windings with core lines."""
    lw = 2.2
    # left winding (arcs)
    for i, dy in enumerate(np.linspace(-0.35, 0.35, 4) * scale):
        ax.add_patch(Arc((cx - 0.18 * scale, cy + dy), 0.28 * scale, 0.22 * scale,
                         theta1=90, theta2=270, color=LINE, lw=lw))
    # right winding
    for i, dy in enumerate(np.linspace(-0.35, 0.35, 4) * scale):
        ax.add_patch(Arc((cx + 0.18 * scale, cy + dy), 0.28 * scale, 0.22 * scale,
                         theta1=-90, theta2=90, color=LINE, lw=lw))
    # core
    ax.plot([cx - 0.04 * scale, cx - 0.04 * scale], [cy - 0.45 * scale, cy + 0.45 * scale], color=LINE, lw=2.0)
    ax.plot([cx + 0.04 * scale, cx + 0.04 * scale], [cy - 0.45 * scale, cy + 0.45 * scale], color=LINE, lw=2.0)
    # leads
    ax.plot([cx - 0.55 * scale, cx - 0.32 * scale], [cy + 0.35 * scale, cy + 0.35 * scale], color=LINE, lw=lw)
    ax.plot([cx - 0.55 * scale, cx - 0.32 * scale], [cy - 0.35 * scale, cy - 0.35 * scale], color=LINE, lw=lw)
    ax.plot([cx + 0.32 * scale, cx + 0.55 * scale], [cy + 0.35 * scale, cy + 0.35 * scale], color=LINE, lw=lw)
    ax.plot([cx + 0.32 * scale, cx + 0.55 * scale], [cy - 0.35 * scale, cy - 0.35 * scale], color=LINE, lw=lw)


def make_parts_symbols():
    fig, ax = plt.subplots(figsize=(12.4, 8.0))
    ax.set_xlim(0, 12.4)
    ax.set_ylim(0, 8.0)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    zh(ax, 6.2, 7.55, "常用電子零件符號", size=20, color=NAVY, weight="bold")
    zh(ax, 6.2, 7.15, "IEC 風格示意（教學用）", size=12, color="#555")

    # 2 rows of 5
    items = [
        ("電阻 R", _resistor, {}),
        ("電位器 VR", _potentiometer, {}),
        ("熱敏電阻 NTC", _thermistor, {}),
        ("光敏電阻 LDR", _ldr, {}),
        ("電容 C", _capacitor, {}),
        ("二極管 Diode", _diode, {}),
        ("發光二極管 LED", _led, {}),
        ("開關 SW", _switch, {}),
        ("繼電器 Relay", _relay, {}),
        ("變壓器 Transformer", _transformer, {}),
    ]

    cols, rows = 5, 2
    cell_w, cell_h = 2.35, 3.0
    x0, y_top = 0.35, 6.55

    for idx, (label, drawer, kwargs) in enumerate(items):
        r, c = divmod(idx, cols)
        x = x0 + c * cell_w
        y = y_top - (r + 1) * cell_h
        # cell background
        bg = CREAM if (r + c) % 2 == 0 else MINT
        box(ax, x, y, cell_w - 0.12, cell_h - 0.18, ec=NAVY, fc=bg, lw=1.8, r=0.1)
        # symbol center
        sx = x + (cell_w - 0.12) / 2
        sy = y + (cell_h - 0.18) * 0.55
        drawer(ax, sx, sy, scale=1.05, **kwargs)
        zh(ax, sx, y + 0.32, label, size=12, color=NAVY, weight="bold")

    save(fig, "parts_symbols.png")


# =============================================================================
# 3. transistor_switch.png
# =============================================================================
def make_transistor_switch():
    fig, ax = plt.subplots(figsize=(11.6, 7.4))
    ax.set_xlim(0, 11.6)
    ax.set_ylim(0, 7.4)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    zh(ax, 5.8, 7.05, "NPN 電晶體作開關", size=20, color=NAVY, weight="bold")
    zh(ax, 5.8, 6.65, "基極小電流控制集極大電流（截止／飽和）", size=12, color="#555")

    # outer frame
    box(ax, 0.35, 0.35, 11.0, 6.0, ec=NAVY, fc=PALE, lw=2.0, r=0.1)

    lw = 2.4
    # --- NPN symbol position ---
    tx, ty = 5.5, 3.2  # transistor center (collector junction)

    # Collector vertical line up
    ax.plot([tx, tx], [ty, ty + 1.8], color=LINE, lw=lw)
    # Emitter diagonal down-right
    ax.plot([tx, tx + 0.9], [ty, ty - 1.1], color=LINE, lw=lw)
    # Base horizontal into junction
    ax.plot([tx - 1.4, tx], [ty, ty], color=LINE, lw=lw)
    # thick base bar (NPN symbol bar)
    ax.plot([tx, tx], [ty - 0.35, ty + 0.35], color=LINE, lw=4.5, solid_capstyle="butt")
    # emitter arrow (NPN: out from junction along emitter)
    ax.annotate(
        "", xy=(tx + 0.75, ty - 0.92), xytext=(tx + 0.25, ty - 0.3),
        arrowprops=dict(arrowstyle="->", color=LINE, lw=2.4, mutation_scale=16),
    )

    # Labels B C E
    zh(ax, tx - 1.55, ty + 0.25, "B", size=14, color=NAVY, weight="bold")
    zh(ax, tx + 0.25, ty + 1.55, "C", size=14, color=NAVY, weight="bold")
    zh(ax, tx + 1.15, ty - 1.0, "E", size=14, color=NAVY, weight="bold")
    zh(ax, tx + 0.55, ty + 0.15, "NPN", size=12, color=TEAL, weight="bold")

    # --- Emitter to GND ---
    ax.plot([tx + 0.9, tx + 0.9], [ty - 1.1, 1.1], color=LINE, lw=lw)
    # GND symbol
    gx, gy = tx + 0.9, 1.1
    ax.plot([gx - 0.35, gx + 0.35], [gy, gy], color=LINE, lw=2.6)
    ax.plot([gx - 0.22, gx + 0.22], [gy - 0.12, gy - 0.12], color=LINE, lw=2.2)
    ax.plot([gx - 0.1, gx + 0.1], [gy - 0.24, gy - 0.24], color=LINE, lw=2.0)
    zh(ax, gx + 0.55, gy - 0.05, "GND", size=12, color=INK)

    # --- Base resistor Rb and Vin ---
    # wire left from base
    bx = tx - 1.4
    # Rb zigzag
    _resistor(ax, bx - 1.0, ty, horiz=True, scale=0.85)
    # extend to Vin
    ax.plot([bx - 1.0 - 0.95 * 0.85 / 2 - 0.35 * 0.85 - 0.15, 0.9], [ty, ty], color=LINE, lw=lw)
    # Vin label box
    box(ax, 0.55, ty - 0.35, 0.9, 0.7, ec=ORANGE, fc=CREAM, lw=2.0, r=0.06)
    zh(ax, 1.0, ty, r"$V_{in}$", size=14, color=ORANGE, weight="bold")
    zh(ax, bx - 1.0, ty + 0.55, r"$R_b$", size=13, color=NAVY, weight="bold")

    # Ib arrow
    ax.annotate(
        "", xy=(bx - 0.15, ty + 0.28), xytext=(bx - 1.5, ty + 0.28),
        arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.0, mutation_scale=12),
    )
    zh(ax, bx - 0.85, ty + 0.55, r"$I_b$", size=12, color=ORANGE, weight="bold")

    # --- Collector load: LED + Rs to Vcc ---
    # horizontal from collector top to left then up? Classic: Vcc -- Rs -- LED -- C
    top_y = ty + 1.8
    # from C go left then through LED and Rs to Vcc on left-top... better: Vcc on top
    # Collector goes up to LED cathode? Convention: Vcc - Rs - LED anode-cathode - C
    # So from top: Vcc, then Rs, then LED, then down to C

    # vertical already at tx up to top_y; continue with LED above
    led_y = top_y + 0.85
    # LED (pointing down = current into collector)
    # draw diode pointing down: triangle pointing down + bar above
    s = 0.28
    # bar (cathode toward collector = bottom for LED when current from Vcc down)
    # Current Vcc → Rs → LED anode → cathode → C
    # So LED triangle points down (toward C), bar is on cathode side (bottom of triangle tip? wait)
    # Standard: triangle points in current direction; bar is cathode.
    # Current down: tip at bottom, bar at tip (cathode at bottom near C)
    tri = Polygon(
        [(tx - s, led_y + s * 0.3), (tx + s, led_y + s * 0.3), (tx, led_y - s * 0.7)],
        closed=True, facecolor=LINE, edgecolor=LINE, lw=1.5,
    )
    ax.add_patch(tri)
    # cathode bar near tip
    tip_y = led_y - s * 0.7
    ax.plot([tx - s, tx + s], [tip_y, tip_y], color=LINE, lw=2.8)
    ax.plot([tx, tip_y], [tx, top_y], color=LINE, lw=lw)
    # light arrows
    ax.annotate(
        "", xy=(tx + 0.55, led_y + 0.45), xytext=(tx + 0.25, led_y + 0.05),
        arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.8, mutation_scale=10),
    )
    ax.annotate(
        "", xy=(tx + 0.7, led_y + 0.3), xytext=(tx + 0.4, led_y - 0.1),
        arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.8, mutation_scale=10),
    )
    zh(ax, tx + 1.05, led_y, "LED", size=12, color=ORANGE, weight="bold")

    # Rs above LED
    rs_y = led_y + 0.95
    _resistor(ax, tx, rs_y, horiz=False, scale=0.7)
    zh(ax, tx + 0.7, rs_y, r"$R_s$", size=13, color=NAVY, weight="bold")

    # Vcc rail
    vcc_y = rs_y + 0.95 * 0.7 / 2 + 0.35 * 0.7 + 0.25
    ax.plot([tx - 0.8, tx + 0.8], [vcc_y, vcc_y], color=LINE, lw=2.6)
    ax.plot([tx, rs_y + 0.95 * 0.7 / 2 + 0.35 * 0.7], [tx, vcc_y], color=LINE, lw=lw)
    box(ax, tx - 0.55, vcc_y + 0.12, 1.1, 0.5, ec=TEAL, fc=MINT, lw=2.0, r=0.05)
    zh(ax, tx, vcc_y + 0.37, r"$+V_{cc}$", size=13, color=TEAL, weight="bold")

    # Ic arrow on collector
    ax.annotate(
        "", xy=(tx - 0.35, ty + 0.9), xytext=(tx - 0.35, ty + 1.7),
        arrowprops=dict(arrowstyle="->", color=RED, lw=2.0, mutation_scale=12),
    )
    zh(ax, tx - 0.75, ty + 1.35, r"$I_c$", size=12, color=RED, weight="bold")

    # --- Annotation panels ---
    box(ax, 7.6, 4.2, 3.4, 1.7, ec=ORANGE, fc=CREAM, lw=2.0, r=0.08)
    zh(ax, 9.3, 5.5, "重點", size=13, color=ORANGE, weight="bold")
    zh(ax, 9.3, 5.0, "基極小電流", size=13, color=INK)
    zh(ax, 9.3, 4.6, "控制集極大電流", size=13, color=INK)

    box(ax, 7.6, 1.8, 3.4, 2.1, ec=TEAL, fc=MINT, lw=2.0, r=0.08)
    zh(ax, 9.3, 3.5, "開關狀態", size=13, color=TEAL, weight="bold")
    zh(ax, 9.3, 3.0, "截止：無 Ib → 如開路", size=12, color=INK)
    zh(ax, 9.3, 2.5, "飽和：有足夠 Ib → 如閉合", size=12, color=INK)
    zh(ax, 9.3, 2.1, "（LED／負載亮）", size=11, color="#555")

    # left note
    zh(ax, 2.8, 1.5, "輸入高電位 → 飽和導通 → 負載有電流", size=12, color=NAVY)

    save(fig, "transistor_switch.png")


if __name__ == "__main__":
    make_ac_dc_wave()
    make_parts_symbols()
    make_transistor_switch()
    print("---")
    for name in ("ac_dc_wave.png", "parts_symbols.png", "transistor_switch.png"):
        p = os.path.join(OUT, name)
        print(f"{name}: exists={os.path.exists(p)} size={os.path.getsize(p)}")
