# -*- coding: utf-8 -*-
"""零件純電路符號教學卡（校本自製示意 · DAT）— 無實物相、無教育局字。"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle

font_manager.fontManager.addfont("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
font_manager.fontManager.addfont("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc")
plt.rcParams["font.family"] = "Noto Sans CJK TC"
plt.rcParams["axes.unicode_minus"] = False

OUT = Path("/workspace/dat-elec-3col/assets")
OUT.mkdir(parents=True, exist_ok=True)

NAVY = "#1B3A4B"
ORANGE = "#E07A1F"
INK = "#222222"
LINE = "#1A1A1A"
PALE = "#F4F7FA"
CREAM = "#FFF6EC"
ACK = "校本自製示意 · DAT"


def save(fig, name):
    path = OUT / name
    fig.savefig(path, dpi=200, bbox_inches="tight", pad_inches=0.22, facecolor="white")
    plt.close(fig)
    print(name, path.stat().st_size)


def zh(ax, x, y, s, size=13, color=INK, ha="center", va="center", weight="regular", **kw):
    ax.text(x, y, s, ha=ha, va=va, fontsize=size, color=color, fontweight=weight, **kw)


def panel(ax, x0, y0, w, h, fc=PALE):
    ax.add_patch(FancyBboxPatch(
        (x0, y0), w, h, boxstyle="round,pad=0.012,rounding_size=0.04",
        linewidth=1.4, edgecolor="#C5D0DA", facecolor=fc, zorder=0,
    ))


def draw_resistor(ax, x, y, s=1.0):
    xs = np.array([0, 0.18, 0.28, 0.38, 0.48, 0.58, 0.68, 0.78, 1.0]) * s
    ys = np.array([0, 0, 0.22, -0.22, 0.22, -0.22, 0.22, 0, 0]) * s
    ax.plot(xs + x, ys + y, color=LINE, lw=3.2, solid_capstyle="round", zorder=3)


def draw_pot(ax, x, y, s=1.0):
    draw_resistor(ax, x, y, s)
    ax.annotate(
        "", xy=(x + 0.5 * s, y + 0.02 * s), xytext=(x + 0.5 * s, y - 0.38 * s),
        arrowprops=dict(arrowstyle="-|>", color=LINE, lw=2.4, mutation_scale=14),
        zorder=4,
    )


def draw_thermistor(ax, x, y, s=1.0):
    draw_resistor(ax, x, y, s)
    ax.plot([x + 0.22 * s, x + 0.78 * s], [y - 0.32 * s, y + 0.32 * s], color=LINE, lw=2.6, zorder=4)
    ax.plot([x + 0.18 * s, x + 0.28 * s], [y - 0.32 * s, y - 0.32 * s], color=LINE, lw=2.6, zorder=4)


def draw_ldr(ax, x, y, s=1.0):
    draw_resistor(ax, x, y, s)
    ax.add_patch(Circle((x + 0.5 * s, y), 0.42 * s, fill=False, ec=LINE, lw=2.2, zorder=3))
    for dx in (0.0, 0.12):
        ax.annotate(
            "",
            xy=(x + 0.18 * s + dx * s, y + 0.12 * s),
            xytext=(x - 0.05 * s + dx * s, y + 0.42 * s),
            arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.0, mutation_scale=11),
            zorder=4,
        )


def draw_capacitor(ax, x, y, s=1.0):
    ax.plot([x, x + 0.35 * s], [y, y], color=LINE, lw=3.0, zorder=3)
    ax.plot([x + 0.65 * s, x + 1.0 * s], [y, y], color=LINE, lw=3.0, zorder=3)
    ax.plot([x + 0.38 * s, x + 0.38 * s], [y - 0.28 * s, y + 0.28 * s], color=LINE, lw=3.4, zorder=3)
    ax.plot([x + 0.62 * s, x + 0.62 * s], [y - 0.28 * s, y + 0.28 * s], color=LINE, lw=3.4, zorder=3)


def draw_diode(ax, x, y, s=1.0):
    ax.plot([x, x + 0.32 * s], [y, y], color=LINE, lw=3.0, zorder=3)
    ax.plot([x + 0.68 * s, x + 1.0 * s], [y, y], color=LINE, lw=3.0, zorder=3)
    tri = Polygon(
        [(x + 0.32 * s, y - 0.26 * s), (x + 0.32 * s, y + 0.26 * s), (x + 0.62 * s, y)],
        closed=True, facecolor=LINE, edgecolor=LINE, lw=1.5, zorder=3,
    )
    ax.add_patch(tri)
    ax.plot([x + 0.66 * s, x + 0.66 * s], [y - 0.28 * s, y + 0.28 * s], color=LINE, lw=3.4, zorder=3)


def draw_led(ax, x, y, s=1.0):
    draw_diode(ax, x, y, s)
    for ox, oy in [(0.48, 0.18), (0.58, 0.10)]:
        ax.annotate(
            "",
            xy=(x + (ox + 0.22) * s, y + (oy + 0.28) * s),
            xytext=(x + ox * s, y + oy * s),
            arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.8, mutation_scale=10),
            zorder=4,
        )


def draw_npn(ax, x, y, s=1.0):
    ax.add_patch(Circle((x + 0.5 * s, y), 0.42 * s, fill=False, ec=LINE, lw=2.4, zorder=3))
    ax.plot([x + 0.32 * s, x + 0.32 * s], [y - 0.22 * s, y + 0.22 * s], color=LINE, lw=3.2, zorder=3)
    ax.plot([x, x + 0.32 * s], [y, y], color=LINE, lw=2.8, zorder=3)
    ax.plot([x + 0.32 * s, x + 0.62 * s], [y + 0.12 * s, y + 0.34 * s], color=LINE, lw=2.8, zorder=3)
    ax.plot([x + 0.62 * s, x + 0.62 * s], [y + 0.34 * s, y + 0.55 * s], color=LINE, lw=2.8, zorder=3)
    ax.annotate(
        "",
        xy=(x + 0.62 * s, y - 0.34 * s),
        xytext=(x + 0.32 * s, y - 0.12 * s),
        arrowprops=dict(arrowstyle="-|>", color=LINE, lw=2.6, mutation_scale=12),
        zorder=3,
    )
    ax.plot([x + 0.62 * s, x + 0.62 * s], [y - 0.34 * s, y - 0.55 * s], color=LINE, lw=2.8, zorder=3)
    zh(ax, x + 0.08 * s, y + 0.12 * s, "B", size=10, color=NAVY)
    zh(ax, x + 0.78 * s, y + 0.48 * s, "C", size=10, color=NAVY)
    zh(ax, x + 0.78 * s, y - 0.48 * s, "E", size=10, color=NAVY)


CARDS = [
    {
        "file": "card_resistor.png",
        "title": "電阻器 Resistor (R)",
        "gloss": "雙端零件，在接線柱之間產生電壓降，抗拒電流通過。",
        "draw": draw_resistor,
        "sym_note": "電路符號（鋸齒／IEC 亦可）",
    },
    {
        "file": "card_potentiometer.png",
        "title": "電位器 Potentiometer (VR)",
        "gloss": "可變電阻，常用作分壓器（例如音量控制）。",
        "draw": draw_pot,
        "sym_note": "電路符號（箭咀＝接帚）",
    },
    {
        "file": "card_thermistor.png",
        "title": "熱敏電阻器 Thermistor (NTC)",
        "gloss": "電阻值隨溫度改變；常用於溫度監測。",
        "draw": draw_thermistor,
        "sym_note": "電路符號（斜線＝溫度敏感）",
    },
    {
        "file": "card_ldr.png",
        "title": "光敏電阻器 LDR",
        "gloss": "光越強，電阻越小；常用於自動開／關路燈。",
        "draw": draw_ldr,
        "sym_note": "電路符號（箭咀＝入射光）",
    },
    {
        "file": "card_capacitor.png",
        "title": "電容器 Capacitor (C)",
        "gloss": "可在兩塊金屬板之間儲存電荷能量。",
        "draw": draw_capacitor,
        "sym_note": "電路符號（平行板）",
    },
    {
        "file": "card_diode.png",
        "title": "二極管 Diode",
        "gloss": "只允許電流單向流動，阻擋相反方向。",
        "draw": draw_diode,
        "sym_note": "電路符號（三角指向陰極）",
    },
    {
        "file": "card_led.png",
        "title": "發光二極管 LED",
        "gloss": "正向電流通過時會發亮；亦是一種二極管。",
        "draw": draw_led,
        "sym_note": "電路符號（箭咀＝發光）",
    },
    {
        "file": "card_transistor.png",
        "title": "晶體管 Transistor (NPN)",
        "gloss": "半導體器件，常用作放大器或電子開關。",
        "draw": draw_npn,
        "sym_note": "電路符號（B／C／E）",
    },
]


def make_card(card):
    """純符號卡：標題 + 大符號 + 說明 + ACK。無實物相、無教育局字。"""
    fig, ax = plt.subplots(figsize=(9.0, 5.2))
    ax.set_xlim(0, 9.0)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    ax.add_patch(Rectangle((0, 4.55), 9.0, 0.65, facecolor=NAVY, edgecolor="none", zorder=1))
    zh(ax, 4.5, 4.88, card["title"], size=18, color="white", weight="bold")

    panel(ax, 0.45, 1.05, 8.1, 3.25, fc=PALE)
    zh(ax, 4.5, 4.05, card["sym_note"], size=13, color=NAVY, weight="bold")

    # large centered symbol
    sx, sy, ss = 2.9, 2.45, 3.2
    card["draw"](ax, sx, sy, ss)

    zh(ax, 4.5, 0.65, card["gloss"], size=13, color=INK, ha="center")
    zh(ax, 4.5, 0.28, ACK, size=9, color="#666666", ha="center")

    save(fig, card["file"])


def make_index_strip():
    fig, ax = plt.subplots(figsize=(12, 2.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 2.2)
    ax.axis("off")
    zh(ax, 6, 1.85, "電子零件：電路符號示意（對照卡）", size=15, color=NAVY, weight="bold")
    labels = ["電阻", "電位器", "熱敏", "光敏", "電容", "二極管", "LED", "晶體管"]
    for i, lab in enumerate(labels):
        x = 0.6 + i * 1.4
        ax.add_patch(FancyBboxPatch(
            (x, 0.45), 1.2, 1.0, boxstyle="round,pad=0.02,rounding_size=0.06",
            facecolor=CREAM if i % 2 == 0 else PALE, edgecolor="#C5D0DA", lw=1.2,
        ))
        zh(ax, x + 0.6, 0.95, lab, size=11, color=INK, weight="bold")
    zh(ax, 6, 0.18, ACK, size=8, color="#666666")
    save(fig, "card_parts_index.png")


if __name__ == "__main__":
    for c in CARDS:
        make_card(c)
    make_index_strip()
    print("DONE", len(CARDS) + 1)
