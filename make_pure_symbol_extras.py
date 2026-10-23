# -*- coding: utf-8 -*-
"""重畫 card_color_code + symbols/*（純自畫，無實物相／教育局）。"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch, Arc
from matplotlib.patches import Polygon

font_manager.fontManager.addfont("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
font_manager.fontManager.addfont("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc")
plt.rcParams["font.family"] = "Noto Sans CJK TC"
plt.rcParams["axes.unicode_minus"] = False

OUT = Path("/workspace/dat-elec-3col/assets")
SYM = OUT / "symbols"
SYM.mkdir(parents=True, exist_ok=True)

NAVY = "#1B3A4B"
ORANGE = "#E07A1F"
INK = "#222222"
LINE = "#1A1A1A"
PALE = "#F4F7FA"
CREAM = "#FFF6EC"
ACK = "校本自製示意 · DAT"

COLORS = [
    ("黑", "#111111", 0),
    ("棕", "#8B4513", 1),
    ("紅", "#E53935", 2),
    ("橙", "#FB8C00", 3),
    ("黃", "#FDD835", 4),
    ("綠", "#43A047", 5),
    ("藍", "#1E88E5", 6),
    ("紫", "#8E24AA", 7),
    ("灰", "#9E9E9E", 8),
    ("白", "#FAFAFA", 9),
]
MULT = [
    ("黑", "#111111", "×1"),
    ("棕", "#8B4513", "×10"),
    ("紅", "#E53935", "×100"),
    ("橙", "#FB8C00", "×1k"),
    ("黃", "#FDD835", "×10k"),
    ("綠", "#43A047", "×100k"),
    ("藍", "#1E88E5", "×1M"),
    ("金", "#D4AF37", "×0.1"),
    ("銀", "#C0C0C0", "×0.01"),
]
TOL = [
    ("金", "#D4AF37", "±5%"),
    ("銀", "#C0C0C0", "±10%"),
    ("棕", "#8B4513", "±1%"),
    ("紅", "#E53935", "±2%"),
]


def save(fig, path):
    path = Path(path)
    fig.savefig(path, dpi=200, bbox_inches="tight", pad_inches=0.2, facecolor="white")
    plt.close(fig)
    print(path.name, path.stat().st_size)


def zh(ax, x, y, s, size=12, color=INK, ha="center", va="center", weight="regular", **kw):
    ax.text(x, y, s, ha=ha, va=va, fontsize=size, color=color, fontweight=weight, **kw)


def draw_resistor_body(ax, x, y, w, h, bands, body="#E8DCC8"):
    """Simple flat resistor body with color bands."""
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.08",
        facecolor=body, edgecolor=LINE, lw=1.5, zorder=2,
    ))
    # leads
    ax.plot([x - 0.35, x], [y + h / 2, y + h / 2], color=LINE, lw=2.2, zorder=1)
    ax.plot([x + w, x + w + 0.35], [y + h / 2, y + h / 2], color=LINE, lw=2.2, zorder=1)
    n = len(bands)
    gap = w / (n + 1.5)
    for i, c in enumerate(bands):
        bx = x + gap * (i + 0.7)
        ax.add_patch(Rectangle((bx, y + 0.04), 0.14, h - 0.08, facecolor=c, edgecolor="#333", lw=0.4, zorder=3))


def make_card_color_code():
    fig, ax = plt.subplots(figsize=(11, 7.2))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.2)
    ax.axis("off")

    ax.add_patch(Rectangle((0, 6.55), 11, 0.65, facecolor=NAVY, edgecolor="none"))
    zh(ax, 5.5, 6.88, "電阻色環對照（四環）· 自畫示意", size=17, color="white", weight="bold")

    # example resistor: 紅紅橙金 = 22k ±5%
    zh(ax, 5.5, 6.25, "例：紅 · 紅 · 橙 · 金  →  22 × 1k = 22 kΩ ±5%", size=13, color=NAVY, weight="bold")
    draw_resistor_body(ax, 3.2, 5.55, 4.6, 0.55, ["#E53935", "#E53935", "#FB8C00", "#D4AF37"])
    zh(ax, 2.6, 5.82, "位1", size=9, color="#555")
    zh(ax, 4.0, 5.82, "位2", size=9, color="#555")
    zh(ax, 5.5, 5.82, "倍數", size=9, color="#555")
    zh(ax, 7.0, 5.82, "誤差", size=9, color="#555")

    # digit table
    ax.add_patch(FancyBboxPatch((0.3, 2.55), 5.0, 2.75, boxstyle="round,pad=0.02,rounding_size=0.05",
                                facecolor=PALE, edgecolor="#C5D0DA", lw=1.2))
    zh(ax, 2.8, 5.05, "位1／位2（數字 0–9）", size=12, color=NAVY, weight="bold")
    for i, (name, hexc, n) in enumerate(COLORS):
        col = i % 5
        row = i // 5
        x = 0.55 + col * 0.95
        y = 4.45 - row * 0.85
        ax.add_patch(Rectangle((x, y), 0.55, 0.45, facecolor=hexc, edgecolor="#333", lw=0.6))
        label_c = "white" if n in (0, 1, 2, 6, 7) else INK
        zh(ax, x + 0.275, y + 0.22, str(n), size=11, color=label_c, weight="bold")
        zh(ax, x + 0.275, y - 0.18, name, size=9, color=INK)

    # multiplier
    ax.add_patch(FancyBboxPatch((5.5, 2.55), 2.55, 2.75, boxstyle="round,pad=0.02,rounding_size=0.05",
                                facecolor="#F0FBF0", edgecolor="#C5D0DA", lw=1.2))
    zh(ax, 6.775, 5.05, "倍數", size=12, color=NAVY, weight="bold")
    for i, (name, hexc, lab) in enumerate(MULT):
        y = 4.65 - i * 0.24
        ax.add_patch(Rectangle((5.7, y), 0.35, 0.18, facecolor=hexc, edgecolor="#333", lw=0.4))
        zh(ax, 6.25, y + 0.09, name, size=8, color=INK, ha="left")
        zh(ax, 7.7, y + 0.09, lab, size=8, color=INK, ha="right")

    # tolerance
    ax.add_patch(FancyBboxPatch((8.25, 2.55), 2.45, 2.75, boxstyle="round,pad=0.02,rounding_size=0.05",
                                facecolor="#FFF8F0", edgecolor="#C5D0DA", lw=1.2))
    zh(ax, 9.475, 5.05, "誤差", size=12, color=NAVY, weight="bold")
    for i, (name, hexc, lab) in enumerate(TOL):
        y = 4.55 - i * 0.45
        ax.add_patch(Rectangle((8.5, y), 0.5, 0.32, facecolor=hexc, edgecolor="#333", lw=0.5))
        zh(ax, 9.2, y + 0.16, name, size=10, color=INK, ha="left")
        zh(ax, 10.4, y + 0.16, lab, size=10, color=INK, ha="right")

    # formula box
    ax.add_patch(FancyBboxPatch((0.3, 0.55), 10.4, 1.75, boxstyle="round,pad=0.02,rounding_size=0.05",
                                facecolor=CREAM, edgecolor="#C5D0DA", lw=1.2))
    zh(ax, 5.5, 1.95, "讀法", size=13, color=NAVY, weight="bold")
    zh(ax, 5.5, 1.5, "R = (10 × 位1 + 位2) × 倍數  ± 誤差", size=13, color=INK)
    zh(ax, 5.5, 1.05, "四環：前兩環＝數字，第三環＝倍數，第四環＝誤差（金／銀常見）", size=11, color="#444")
    zh(ax, 5.5, 0.7, "五環：多一環有效數字；教學先掌握四環即可", size=11, color="#444")

    zh(ax, 5.5, 0.25, ACK, size=9, color="#666666")
    save(fig, OUT / "card_color_code.png")


def make_fuse_switch_relay():
    fig, ax = plt.subplots(figsize=(10, 7.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.5)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 6.85), 10, 0.65, facecolor=NAVY, edgecolor="none"))
    zh(ax, 5, 7.18, "保險絲 · 開關 · 繼電器（電路符號）", size=16, color="white", weight="bold")

    # Fuse panel
    ax.add_patch(FancyBboxPatch((0.35, 4.55), 9.3, 2.05, boxstyle="round,pad=0.02,rounding_size=0.05",
                                facecolor=PALE, edgecolor="#C5D0DA", lw=1.2))
    zh(ax, 5, 6.35, "保險絲 Fuse", size=14, color=NAVY, weight="bold")
    # symbol: rectangle with wire
    ax.plot([2.5, 3.2], [5.4, 5.4], color=LINE, lw=2.5)
    ax.add_patch(Rectangle((3.2, 5.15), 2.0, 0.5, fill=False, ec=LINE, lw=2.5))
    ax.plot([3.2, 5.2], [5.4, 5.4], color=LINE, lw=2.0)
    ax.plot([5.2, 5.9], [5.4, 5.4], color=LINE, lw=2.5)
    zh(ax, 4.2, 5.75, "1A", size=11, color=INK)
    zh(ax, 7.5, 5.4, "過流時熔斷，保護電路", size=12, color=INK, ha="left")

    # Switch panel
    ax.add_patch(FancyBboxPatch((0.35, 2.45), 9.3, 1.9, boxstyle="round,pad=0.02,rounding_size=0.05",
                                facecolor=CREAM, edgecolor="#C5D0DA", lw=1.2))
    zh(ax, 5, 4.1, "開關 Switch (SW)", size=14, color=NAVY, weight="bold")
    ax.plot([2.5, 3.5], [3.3, 3.3], color=LINE, lw=2.5)
    ax.plot(3.5, 3.3, "o", color=LINE, markersize=8)
    ax.plot([3.5, 4.6], [3.3, 3.85], color=LINE, lw=2.5)
    ax.plot(4.8, 3.3, "o", color=LINE, markersize=8)
    ax.plot([4.8, 5.8], [3.3, 3.3], color=LINE, lw=2.5)
    zh(ax, 7.5, 3.4, "閉合時電流才能通過", size=12, color=INK, ha="left")

    # Relay panel
    ax.add_patch(FancyBboxPatch((0.35, 0.45), 9.3, 1.8, boxstyle="round,pad=0.02,rounding_size=0.05",
                                facecolor=PALE, edgecolor="#C5D0DA", lw=1.2))
    zh(ax, 5, 2.0, "繼電器 Relay", size=14, color=NAVY, weight="bold")
    # coil
    ax.add_patch(Rectangle((2.3, 0.85), 1.4, 0.7, fill=False, ec=LINE, lw=2.2))
    zh(ax, 3.0, 1.2, "線圈", size=10, color=INK)
    ax.plot([2.3, 2.3], [0.85, 0.65], color=LINE, lw=1.8)
    ax.plot([3.7, 3.7], [0.85, 0.65], color=LINE, lw=1.8)
    # dashed link
    ax.plot([3.7, 5.0], [1.2, 1.2], color=LINE, lw=1.5, ls="--")
    # contact
    ax.plot([5.0, 5.0], [0.9, 1.5], color=LINE, lw=2.0)
    ax.plot([5.0, 6.0], [1.5, 1.7], color=LINE, lw=2.0)
    ax.plot(6.1, 1.35, "o", color=LINE, markersize=6)
    ax.plot([6.1, 6.8], [1.35, 1.35], color=LINE, lw=2.0)
    zh(ax, 5.0, 1.7, "COM", size=8, color="#555", ha="right")
    zh(ax, 6.5, 1.7, "NO", size=8, color="#555")
    zh(ax, 7.8, 1.2, "用小電流控制大電流／隔離", size=12, color=INK, ha="left")

    zh(ax, 5, 0.18, ACK, size=9, color="#666")
    save(fig, SYM / "fuse_switch_relay.png")


def make_speaker_buzzer_mic():
    fig, ax = plt.subplots(figsize=(10, 6.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 5.85), 10, 0.65, facecolor=NAVY, edgecolor="none"))
    zh(ax, 5, 6.18, "揚聲器 · 蜂鳴器 · 咪高風（電路符號）", size=15, color="white", weight="bold")

    panels = [
        (0.35, 3.15, "揚聲器 Speaker", "把電訊號轉成聲音"),
        (0.35, 1.55, "蜂鳴器 Buzzer", "簡單提示聲／警報"),
        (0.35, 0.0, "咪高風 Mic", "把聲音轉成電訊號"),
    ]
    # Speaker symbol
    ax.add_patch(FancyBboxPatch((0.35, 3.15), 9.3, 2.4, boxstyle="round,pad=0.02,rounding_size=0.05",
                                facecolor=PALE, edgecolor="#C5D0DA", lw=1.2))
    zh(ax, 5, 5.25, "揚聲器 Speaker", size=13, color=NAVY, weight="bold")
    ax.plot([2.8, 2.8], [3.6, 4.6], color=LINE, lw=2.5)
    ax.add_patch(Polygon([(2.8, 3.6), (2.8, 4.6), (3.6, 5.0), (3.6, 3.2)], closed=True,
                         fill=False, ec=LINE, lw=2.2))
    for r in (0.35, 0.55, 0.75):
        ax.add_patch(Arc((3.7, 4.1), r * 2, r * 2, angle=0, theta1=-40, theta2=40, color=ORANGE, lw=1.8))
    zh(ax, 6.5, 4.1, "電 → 聲", size=12, color=INK, ha="left")

    # Buzzer
    ax.add_patch(FancyBboxPatch((0.35, 1.6), 9.3, 1.35, boxstyle="round,pad=0.02,rounding_size=0.05",
                                facecolor=CREAM, edgecolor="#C5D0DA", lw=1.2))
    zh(ax, 5, 2.7, "蜂鳴器 Buzzer", size=13, color=NAVY, weight="bold")
    ax.add_patch(Circle((3.3, 2.15), 0.45, fill=False, ec=LINE, lw=2.2))
    zh(ax, 3.3, 2.15, "Bz", size=10, color=INK)
    ax.plot([2.5, 2.85], [2.15, 2.15], color=LINE, lw=2.0)
    ax.plot([3.75, 4.1], [2.15, 2.15], color=LINE, lw=2.0)
    zh(ax, 6.5, 2.15, "簡單提示聲／警報", size=12, color=INK, ha="left")

    # Mic
    ax.add_patch(FancyBboxPatch((0.35, 0.15), 9.3, 1.25, boxstyle="round,pad=0.02,rounding_size=0.05",
                                facecolor=PALE, edgecolor="#C5D0DA", lw=1.2))
    zh(ax, 5, 1.15, "咪高風 Microphone", size=13, color=NAVY, weight="bold")
    ax.add_patch(Circle((3.3, 0.65), 0.35, fill=False, ec=LINE, lw=2.2))
    ax.plot([3.3, 3.3], [0.3, 0.15], color=LINE, lw=2.0)
    ax.plot([3.0, 3.6], [0.15, 0.15], color=LINE, lw=2.0)
    for r in (0.5, 0.7):
        ax.add_patch(Arc((3.3, 0.65), r * 2, r * 2, angle=0, theta1=50, theta2=130, color=ORANGE, lw=1.6))
    zh(ax, 6.5, 0.65, "聲 → 電", size=12, color=INK, ha="left")

    zh(ax, 5, 0.02, ACK, size=8, color="#666")
    # fix ylim overlap - redraw ack inside last panel margin
    save(fig, SYM / "speaker_buzzer_mic.png")


def make_transformer():
    fig, ax = plt.subplots(figsize=(9, 5.0))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 5.0)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 4.35), 9, 0.65, facecolor=NAVY, edgecolor="none"))
    zh(ax, 4.5, 4.68, "變壓器 Transformer（電路符號）", size=16, color="white", weight="bold")

    ax.add_patch(FancyBboxPatch((0.4, 0.7), 8.2, 3.35, boxstyle="round,pad=0.02,rounding_size=0.05",
                                facecolor=PALE, edgecolor="#C5D0DA", lw=1.2))
    zh(ax, 4.5, 3.75, "只對交流升／降壓（電磁感應）", size=13, color=NAVY, weight="bold")

    # primary coil (left arcs)
    cx1 = 3.0
    for i, y in enumerate(np.linspace(1.4, 3.2, 5)):
        ax.add_patch(Arc((cx1, y), 0.7, 0.45, angle=0, theta1=90, theta2=270, color=LINE, lw=2.2))
    ax.plot([cx1 - 0.35, cx1 - 0.35], [1.2, 1.4], color=LINE, lw=2.0)
    ax.plot([cx1 - 0.35, cx1 - 0.35], [3.2, 3.4], color=LINE, lw=2.0)
    zh(ax, 2.2, 2.3, "一次側", size=11, color=INK)

    # core lines
    ax.plot([3.55, 3.55], [1.3, 3.3], color=LINE, lw=2.5)
    ax.plot([3.75, 3.75], [1.3, 3.3], color=LINE, lw=2.5)

    # secondary coil
    cx2 = 4.4
    for i, y in enumerate(np.linspace(1.4, 3.2, 5)):
        ax.add_patch(Arc((cx2, y), 0.7, 0.45, angle=0, theta1=-90, theta2=90, color=LINE, lw=2.2))
    ax.plot([cx2 + 0.35, cx2 + 0.35], [1.2, 1.4], color=LINE, lw=2.0)
    ax.plot([cx2 + 0.35, cx2 + 0.35], [3.2, 3.4], color=LINE, lw=2.0)
    zh(ax, 5.5, 2.3, "二次側", size=11, color=INK)

    zh(ax, 4.5, 1.05, "直流電池本身唔靠變壓器升壓", size=12, color="#444")
    zh(ax, 4.5, 0.35, ACK, size=9, color="#666")
    save(fig, SYM / "transformer.png")


if __name__ == "__main__":
    make_card_color_code()
    make_fuse_switch_relay()
    make_speaker_buzzer_mic()
    make_transformer()
    print("EXTRAS DONE")
