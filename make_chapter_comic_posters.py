# -*- coding: utf-8 -*-
"""自學電學：每章一份漫畫精簡海報（中四 DAT，繁中）。"""
import os
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Polygon, Rectangle, Arc, Ellipse
from matplotlib import font_manager
import numpy as np

font_manager.fontManager.addfont("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
font_manager.fontManager.addfont("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc")
plt.rcParams["font.family"] = "Noto Sans CJK TC"
plt.rcParams["axes.unicode_minus"] = False

OUT = Path("/workspace/dat-elec-3col/assets/posters")
OUT.mkdir(parents=True, exist_ok=True)

NAVY = "#1e3a5f"
INK = "#1f2937"
MUTED = "#64748b"


def save(fig, name):
    path = OUT / name
    fig.savefig(path, dpi=180, bbox_inches="tight", pad_inches=0.18, facecolor="#f8fafc")
    plt.close(fig)
    print(name, path.stat().st_size)


def zh(ax, x, y, s, size=11, color=INK, ha="center", va="center", weight="regular", **kw):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, fontweight=weight, **kw)


def round_box(ax, x, y, w, h, fc, ec="#cbd5e1", lw=1.5, r=0.08):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad=0.01,rounding_size={r}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=1,
    ))


def header(ax, badge, title, tip):
    round_box(ax, 0.15, 9.35, 1.9, 0.45, "#dbeafe", "#3b82f6", 1.6)
    zh(ax, 1.1, 9.57, badge, size=9, color="#1d4ed8", weight="bold")
    zh(ax, 5.5, 9.72, title, size=16, color=NAVY, weight="bold")
    round_box(ax, 0.15, 8.85, 10.7, 0.4, "#fff7ed", "#fb923c", 1.2)
    zh(ax, 5.5, 9.05, "【貼士】" + tip, size=10, color="#9a3412", ha="center")


def footer(ax, motto="掌握基本，電路無難度！｜DAT 自學電學精簡海報"):
    zh(ax, 5.5, 0.22, motto, size=9, color=MUTED)


def new_fig():
    fig, ax = plt.subplots(figsize=(11, 10))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 10)
    ax.axis("off")
    fig.patch.set_facecolor("#f8fafc")
    return fig, ax


# ---------- icons ----------
def icon_tank(ax, cx, cy, s=1.0):
    # water tank = voltage
    ax.add_patch(Rectangle((cx - 0.35 * s, cy - 0.35 * s), 0.7 * s, 0.7 * s, fill=False, ec="#be185d", lw=2))
    ax.add_patch(Rectangle((cx - 0.32 * s, cy - 0.32 * s), 0.64 * s, 0.4 * s, fc="#fda4af", ec="none"))
    zh(ax, cx, cy + 0.48 * s, "高壓", size=8, color="#be185d", weight="bold")


def icon_pipe(ax, cx, cy, s=1.0):
    ax.add_patch(FancyBboxPatch((cx - 0.45 * s, cy - 0.12 * s), 0.9 * s, 0.24 * s,
                                boxstyle="round,pad=0.01,rounding_size=0.08", fc="#93c5fd", ec="#1d4ed8", lw=1.5))
    ax.annotate("", xy=(cx + 0.4 * s, cy), xytext=(cx - 0.4 * s, cy),
                arrowprops=dict(arrowstyle="-|>", color="#1d4ed8", lw=2, mutation_scale=12))


def icon_narrow(ax, cx, cy, s=1.0):
    xs = [cx - 0.45 * s, cx - 0.1 * s, cx + 0.1 * s, cx + 0.45 * s]
    ys = [cy, cy + 0.18 * s, cy + 0.18 * s, cy]
    ax.plot(xs, [cy - 0.05 * s] * 4, color="#166534", lw=2)
    ax.plot([cx - 0.1 * s, cx + 0.1 * s], [cy - 0.05 * s, cy + 0.25 * s], color="#166534", lw=2)
    ax.plot([cx - 0.1 * s, cx + 0.1 * s], [cy - 0.05 * s, cy - 0.35 * s], color="#166534", lw=2)
    zh(ax, cx, cy + 0.42 * s, "窄管", size=8, color="#166534", weight="bold")


def ohm_triangle(ax, cx, cy, s=1.0):
    tri = Polygon(
        [(cx, cy + 0.55 * s), (cx - 0.55 * s, cy - 0.4 * s), (cx + 0.55 * s, cy - 0.4 * s)],
        closed=True, fc="#fef08a", ec="#ca8a04", lw=2, zorder=2,
    )
    ax.add_patch(tri)
    ax.plot([cx - 0.55 * s, cx + 0.55 * s], [cy - 0.05 * s, cy - 0.05 * s], color="#ca8a04", lw=1.5)
    zh(ax, cx, cy + 0.28 * s, "V", size=16, color="#854d0e", weight="bold")
    zh(ax, cx - 0.28 * s, cy - 0.25 * s, "I", size=14, color="#854d0e", weight="bold")
    zh(ax, cx + 0.28 * s, cy - 0.25 * s, "R", size=14, color="#854d0e", weight="bold")


# ========== posters ==========

def poster_ohm_intro():
    fig, ax = new_fig()
    header(ax, "中四 DAT · 01", "電壓 · 電流 · 電阻 · 歐姆定律",
           "記住三個字：V 推動　I 流動　R 阻礙｜電像水流，電路像水管")
    # three concept boxes
    boxes = [
        (0.2, 6.85, 3.4, 1.8, "#fce7f3", "#db2777", "電壓 V", "推動電荷流動嘅「力」\n像水壓", "單位：伏特 V", icon_tank),
        (3.8, 6.85, 3.4, 1.8, "#dbeafe", "#2563eb", "電流 I", "電荷流動速率\n像水流量", "單位：安培 A\n1 mA＝0.001 A", icon_pipe),
        (7.4, 6.85, 3.4, 1.8, "#dcfce7", "#16a34a", "電阻 R", "阻礙流動嘅程度\n像窄水管", "單位：歐姆 Ω\n1 kΩ＝1000 Ω", icon_narrow),
    ]
    for x, y, w, h, fc, ec, title, body, unit, icon in boxes:
        round_box(ax, x, y, w, h, fc, ec, 2)
        zh(ax, x + w / 2, y + h - 0.28, title, size=13, color=ec, weight="bold")
        icon(ax, x + 0.7, y + 0.75, 0.85)
        zh(ax, x + w / 2 + 0.35, y + 0.95, body, size=9.5, color=INK, ha="center", va="center")
        zh(ax, x + w / 2, y + 0.28, unit, size=9, color=MUTED)

    # ohm law + triangle
    round_box(ax, 0.2, 4.55, 5.2, 2.1, "#fffbeb", "#f59e0b", 2)
    zh(ax, 2.8, 6.4, "歐姆定律　V＝I×R", size=14, color="#b45309", weight="bold")
    ohm_triangle(ax, 1.35, 5.35, 1.05)
    zh(ax, 3.6, 5.7, "用手指遮住要求嘅量：", size=10, color=INK, ha="left")
    zh(ax, 3.6, 5.25, "求 V → I×R\n求 I → V／R\n求 R → V／I", size=11, color=INK, ha="left", va="center")

    round_box(ax, 5.6, 4.55, 5.2, 2.1, "#f0fdf4", "#22c55e", 2)
    zh(ax, 8.2, 6.4, "速算例子", size=13, color="#15803d", weight="bold")
    zh(ax, 8.2, 5.55,
       "Q1　I＝2 A，R＝5 Ω → V＝2×5＝10 V\n\n"
       "Q2　V＝12 V，R＝2.4 kΩ＝2400 Ω\n　　I＝12／2400＝0.005 A＝5 mA",
       size=10.5, color=INK, ha="center", va="center")

    round_box(ax, 0.2, 2.55, 10.6, 1.8, "#eff6ff", "#3b82f6", 1.5)
    zh(ax, 5.5, 4.05, "單位小抄（計數前必對齊）", size=12, color="#1d4ed8", weight="bold")
    zh(ax, 5.5, 3.25,
       "電壓 V｜伏特　　電流 I｜安培（mA＝÷1000）　　電阻 R｜歐姆（kΩ＝×1000）\n"
       "口訣：先對齊單位 → 寫公式 → 代入 → 寫答案單位",
       size=11, color=INK)

    round_box(ax, 0.2, 0.55, 10.6, 1.8, "#fef3c7", "#d97706", 1.5)
    zh(ax, 5.5, 1.95, "記住", size=12, color="#92400e", weight="bold")
    zh(ax, 5.5, 1.2, "V 推動　I 流動　R 阻礙　　｜　　V＝IR　是全家桶核心", size=12, color=INK)
    footer(ax)
    save(fig, "poster_01_ohm_intro.png")


def poster_parts():
    fig, ax = new_fig()
    header(ax, "中四 DAT · 02", "常用電子零件同換能器",
           "先分清：感測輸入　｜　被動元件　｜　控制保護　｜　輸出裝置")
    groups = [
        (0.2, 6.6, "#fce7f3", "#db2777", "被動／電阻家族",
         "電阻器　抗拒電流、產生電壓降\n電位器　可變電阻／分壓\n熱敏　溫度→電阻\n光敏 LDR　光強↑電阻↓\n電容器　儲存電荷能量"),
        (3.85, 6.6, "#dbeafe", "#2563eb", "半導體",
         "二極管　只准單向電流\nLED　正向通電發光\n晶體管　放大或電子開關\n集成電路 IC　微電路晶片"),
        (7.5, 6.6, "#dcfce7", "#16a34a", "換能／輸出",
         "揚聲器　電→聲\n蜂鳴器　電壓驅動發聲\n麥克風　聲→電\n（換能＝一種能量→另一種）"),
        (0.2, 3.9, "#fff7ed", "#ea580c", "控制／保護",
         "開關　閉合才通電\n繼電器　細控大、隔離\n保險絲　過流熔斷保護\n變壓器　交流升／降壓"),
        (5.85, 3.9, "#f3e8ff", "#7c3aed", "學習貼士",
         "每種零件記兩樣：\n① 用途　② 電路符號\n（App 右欄有符號示意卡）"),
    ]
    for x, y, fc, ec, title, body in groups:
        w = 3.5 if x < 5 else 4.95 if title == "控制／保護" else 4.95
        if title == "控制／保護":
            w = 5.4
        if title == "學習貼士":
            w = 4.95
        h = 2.5 if y > 5 else 2.4
        round_box(ax, x, y, w, h, fc, ec, 2)
        zh(ax, x + w / 2, y + h - 0.32, title, size=13, color=ec, weight="bold")
        zh(ax, x + w / 2, y + h / 2 - 0.15, body, size=10.5, color=INK, ha="center", va="center")

    round_box(ax, 0.2, 0.55, 10.6, 3.1, "#eff6ff", "#3b82f6", 1.5)
    zh(ax, 5.5, 3.35, "一圖分角色（流程）", size=12, color="#1d4ed8", weight="bold")
    steps = ["感測\nLDR／熱敏／咪", "處理\n電阻／電容／IC", "控制\n晶體管／繼電器", "輸出\nLED／喇叭／蜂鳴"]
    for i, t in enumerate(steps):
        x = 0.7 + i * 2.55
        round_box(ax, x, 1.1, 2.2, 1.7, "#fff", "#60a5fa", 1.5)
        zh(ax, x + 1.1, 1.95, t, size=11, color=NAVY, weight="bold")
        if i < 3:
            ax.annotate("", xy=(x + 2.35, 1.95), xytext=(x + 2.2, 1.95),
                        arrowprops=dict(arrowstyle="-|>", color="#3b82f6", lw=2, mutation_scale=14))
    footer(ax)
    save(fig, "poster_02_parts_intro.png")


def poster_solve(which):
    """which in v,i,r"""
    cfg = {
        "v": ("03", "公式變換：求電壓 V", "已知 I、R → 用 V＝I×R", "V＝I×R",
              "例：I＝2.5 A，R＝10 Ω\nV＝2.5×10＝25 V", "#fce7f3", "#db2777"),
        "i": ("04", "公式變換：求電流 I", "已知 V、R → 用 I＝V／R", "I＝V／R",
              "例：V＝1.5 V，R＝5 Ω\nI＝1.5／5＝0.3 A", "#dbeafe", "#2563eb"),
        "r": ("05", "公式變換：求電阻 R", "已知 V、I → 用 R＝V／I", "R＝V／I",
              "例：V＝12 V，I＝1.2 A\nR＝12／1.2＝10 Ω", "#dcfce7", "#16a34a"),
    }
    no, title, tip, formula, eg, fc, ec = cfg[which]
    fig, ax = new_fig()
    header(ax, f"中四 DAT · {no}", title, tip)
    round_box(ax, 0.5, 6.2, 4.5, 2.4, "#fffbeb", "#f59e0b", 2)
    zh(ax, 2.75, 8.2, "歐姆三角", size=13, color="#b45309", weight="bold")
    ohm_triangle(ax, 2.75, 7.0, 1.3)

    round_box(ax, 5.3, 6.2, 5.3, 2.4, fc, ec, 2)
    zh(ax, 7.95, 8.2, "今關公式", size=13, color=ec, weight="bold")
    zh(ax, 7.95, 7.35, formula, size=28, color=ec, weight="bold")
    zh(ax, 7.95, 6.55, "單位先換成 A 同 Ω 再計", size=11, color=MUTED)

    round_box(ax, 0.5, 3.5, 10.1, 2.4, "#f0fdf4", "#22c55e", 2)
    zh(ax, 5.55, 5.5, "速算示範", size=13, color="#15803d", weight="bold")
    zh(ax, 5.55, 4.4, eg, size=14, color=INK)

    round_box(ax, 0.5, 0.7, 10.1, 2.5, "#eff6ff", "#3b82f6", 1.5)
    zh(ax, 5.55, 2.8, "解題四步", size=13, color="#1d4ed8", weight="bold")
    zh(ax, 5.55, 1.7, "① 睇齊單位（kΩ、mA）　② 寫公式　③ 代入數字　④ 答案連單位", size=13, color=INK)
    footer(ax)
    save(fig, f"poster_{no}_solve_{which}.png")


def poster_power():
    fig, ax = new_fig()
    header(ax, "中四 DAT · 06", "功率 P＝V·I（同 I²R、V²／R）",
           "功率＝單位時間消耗能量｜單位：瓦特 W｜三式等價，按已知量揀")
    round_box(ax, 0.3, 6.5, 10.4, 2.1, "#fef3c7", "#d97706", 2)
    zh(ax, 5.5, 8.2, "三式全家桶", size=14, color="#92400e", weight="bold")
    formulas = [("P＝V×I", "已知 V、I"), ("P＝I²R", "已知 I、R"), ("P＝V²／R", "已知 V、R")]
    for i, (f, note) in enumerate(formulas):
        x = 0.7 + i * 3.4
        round_box(ax, x, 6.7, 3.0, 1.4, "#fff", "#f59e0b", 1.5)
        zh(ax, x + 1.5, 7.55, f, size=16, color="#b45309", weight="bold")
        zh(ax, x + 1.5, 7.0, note, size=11, color=MUTED)

    round_box(ax, 0.3, 3.9, 10.4, 2.3, "#ecfdf5", "#10b981", 2)
    zh(ax, 5.5, 5.85, "例子", size=13, color="#047857", weight="bold")
    zh(ax, 5.5, 4.8, "汽車電池 12 V，燈泡電流 1.75 A\nP＝V×I＝12×1.75＝21 W\n亦可用 P＝V²／R 反求 R＝V²／P", size=13, color=INK)

    round_box(ax, 0.3, 0.7, 10.4, 2.9, "#eff6ff", "#3b82f6", 1.5)
    zh(ax, 5.5, 3.25, "注意", size=13, color="#1d4ed8", weight="bold")
    zh(ax, 5.5, 2.0, "功率愈大＝同一時間消耗愈多能量\nLED 限流電阻都要計功耗，確保小於電阻額定功率", size=12, color=INK)
    footer(ax)
    save(fig, "poster_06_power.png")


def poster_divider():
    fig, ax = new_fig()
    header(ax, "中四 DAT · 07", "分壓器（串聯）",
           "串聯：電流相同｜電壓按電阻比例分配｜電阻愈大，分得電壓愈多")
    # simple series sketch
    round_box(ax, 0.3, 5.9, 5.0, 2.7, "#fff", "#64748b", 1.5)
    zh(ax, 2.8, 8.3, "串聯／分壓示意", size=12, color=NAVY, weight="bold")
    # battery left
    ax.add_patch(Rectangle((0.7, 6.4), 0.35, 1.6, fc="#fee2e2", ec="#dc2626", lw=1.5))
    zh(ax, 0.88, 7.2, "V", size=11, color="#b91c1c", weight="bold")
    # loop
    ax.plot([1.05, 4.6, 4.6, 1.05], [8.0, 8.0, 6.4, 6.4], color="#334155", lw=2)
    ax.add_patch(Rectangle((4.35, 7.35), 0.5, 0.45, fc="#e2e8f0", ec="#334155", lw=1.5))
    zh(ax, 4.6, 7.55, "R1", size=9)
    ax.add_patch(Rectangle((4.35, 6.6), 0.5, 0.45, fc="#e2e8f0", ec="#334155", lw=1.5))
    zh(ax, 4.6, 6.8, "R2", size=9)
    zh(ax, 5.15, 7.55, "V1", size=10, color="#dc2626", weight="bold")
    zh(ax, 5.15, 6.8, "V2", size=10, color="#dc2626", weight="bold")

    round_box(ax, 5.5, 5.9, 5.2, 2.7, "#fef3c7", "#d97706", 2)
    zh(ax, 8.1, 8.2, "公式", size=13, color="#92400e", weight="bold")
    zh(ax, 8.1, 7.2, "V1＝V×R1／(R1＋R2)\nV2＝V×R2／(R1＋R2)\n\n電位器＝常用可變分壓器", size=12, color=INK)

    round_box(ax, 0.3, 3.2, 10.4, 2.4, "#ecfdf5", "#10b981", 2)
    zh(ax, 5.5, 5.2, "例子", size=13, color="#047857", weight="bold")
    zh(ax, 5.5, 4.15, "V＝9 V，R1＝3 Ω，R2＝6 Ω\nV1＝9×3／9＝3 V　　V2＝9×6／9＝6 V", size=14, color=INK)

    round_box(ax, 0.3, 0.7, 10.4, 2.2, "#eff6ff", "#3b82f6", 1.5)
    zh(ax, 5.5, 2.5, "檢查口訣", size=12, color="#1d4ed8", weight="bold")
    zh(ax, 5.5, 1.5, "V1＋V2 應等於總電壓 V（兩電阻時）｜電流全路相同", size=12, color=INK)
    footer(ax)
    save(fig, "poster_07_divider.png")


def poster_shunt():
    fig, ax = new_fig()
    header(ax, "中四 DAT · 08", "分流（並聯）",
           "並聯：電壓相同｜電流按「另一邊電阻」比例分｜電阻愈小，分得電流愈大")
    round_box(ax, 0.3, 6.0, 10.4, 2.6, "#fef3c7", "#d97706", 2)
    zh(ax, 5.5, 8.25, "兩電阻分流", size=14, color="#92400e", weight="bold")
    zh(ax, 5.5, 7.1, "I1＝I×R2／(R1＋R2)　　I2＝I×R1／(R1＋R2)\n\n用「另一邊」電阻——電阻細嘅分支分到較大電流", size=13, color=INK)

    round_box(ax, 0.3, 3.4, 10.4, 2.3, "#ecfdf5", "#10b981", 2)
    zh(ax, 5.5, 5.3, "例子", size=13, color="#047857", weight="bold")
    zh(ax, 5.5, 4.3, "I＝10 A，R1＝10 Ω，R2＝30 Ω\nI1＝10×30／40＝7.5 A　　I2＝10−7.5＝2.5 A", size=14, color=INK)

    round_box(ax, 0.3, 0.7, 5.0, 2.4, "#dbeafe", "#2563eb", 1.5)
    zh(ax, 2.8, 2.7, "串聯記得", size=12, color="#1d4ed8", weight="bold")
    zh(ax, 2.8, 1.7, "總 R＝R1＋R2＋…\n電流相同", size=12, color=INK)

    round_box(ax, 5.6, 0.7, 5.1, 2.4, "#fce7f3", "#db2777", 1.5)
    zh(ax, 8.15, 2.7, "並聯記得", size=12, color="#be185d", weight="bold")
    zh(ax, 8.15, 1.7, "總 R 細過最小分支\n電壓相同", size=12, color=INK)
    footer(ax)
    save(fig, "poster_08_shunt.png")


def poster_color():
    fig, ax = new_fig()
    header(ax, "中四 DAT · 09", "電阻色環（四環）",
           "前兩環＝數字　｜　第三環＝倍數　｜　第四環＝誤差（金±5%／銀±10%）")
    # color digit table compact
    colors = [
        ("黑", "0", "#111"), ("棕", "1", "#92400e"), ("紅", "2", "#dc2626"),
        ("橙", "3", "#ea580c"), ("黃", "4", "#ca8a04"), ("綠", "5", "#16a34a"),
        ("藍", "6", "#2563eb"), ("紫", "7", "#7c3aed"), ("灰", "8", "#6b7280"), ("白", "9", "#e5e7eb"),
    ]
    round_box(ax, 0.25, 6.3, 10.5, 2.3, "#fff", "#94a3b8", 1.5)
    zh(ax, 5.5, 8.3, "色→數字（第1、2環）", size=12, color=NAVY, weight="bold")
    for i, (name, dig, c) in enumerate(colors):
        x = 0.45 + i * 1.02
        ax.add_patch(FancyBboxPatch((x, 6.55), 0.9, 1.4, boxstyle="round,pad=0.02,rounding_size=0.06",
                                    fc=c, ec="#334155", lw=1))
        tc = "#fff" if dig not in ("4", "8", "9") and name != "白" else "#111"
        if name in ("黃", "白", "灰"):
            tc = "#111"
        zh(ax, x + 0.45, 7.5, name, size=10, color=tc, weight="bold")
        zh(ax, x + 0.45, 6.9, dig, size=14, color=tc, weight="bold")

    round_box(ax, 0.25, 4.0, 10.5, 2.0, "#fff7ed", "#fb923c", 1.5)
    zh(ax, 5.5, 5.65, "倍數（第3環）精選", size=12, color="#c2410c", weight="bold")
    zh(ax, 5.5, 4.75, "黑×1　棕×10　紅×100　橙×1k　黃×10k　綠×100k　藍×1M　｜　金×0.1　銀×0.01", size=11, color=INK)

    round_box(ax, 0.25, 1.9, 10.5, 1.85, "#ecfdf5", "#10b981", 2)
    zh(ax, 5.5, 3.4, "例子", size=12, color="#047857", weight="bold")
    zh(ax, 5.5, 2.55, "棕·黑·紅·金 → 10×100＝1000 Ω＝1 kΩ ±5%\n紅·紅·橙·金 → 22×1000＝22 kΩ ±5%", size=12, color=INK)

    round_box(ax, 0.25, 0.45, 10.5, 1.25, "#eff6ff", "#3b82f6", 1.5)
    zh(ax, 5.5, 1.05, "讀法：由靠近端環嗰邊起，由左至右｜標稱 R＝(10×位1＋位2)×倍數", size=11, color=INK)
    footer(ax)
    save(fig, "poster_09_color_code.png")


def poster_led():
    fig, ax = new_fig()
    header(ax, "中四 DAT · 10", "LED 限流與功率",
           "LED 必須串聯限流電阻｜先把 mA 轉成 A 再計")
    round_box(ax, 0.3, 6.3, 10.4, 2.3, "#fef3c7", "#d97706", 2)
    zh(ax, 5.5, 8.2, "核心公式", size=14, color="#92400e", weight="bold")
    zh(ax, 5.5, 7.2, "R＝(Vs−Vf)／I\n\nVs＝電源　Vf＝LED 正向電壓　I＝目標電流（A）", size=14, color=INK)

    round_box(ax, 0.3, 3.7, 10.4, 2.3, "#ecfdf5", "#10b981", 2)
    zh(ax, 5.5, 5.6, "示範", size=13, color="#047857", weight="bold")
    zh(ax, 5.5, 4.55, "Vs＝9 V，Vf＝3 V，I＝6 mA＝0.006 A\nR＝(9−3)／0.006＝1000 Ω\nVr＝6 V → P＝I×Vr＝0.036 W（＜0.25 W 額定 → 安全）", size=12, color=INK)

    round_box(ax, 0.3, 0.7, 10.4, 2.7, "#eff6ff", "#3b82f6", 1.5)
    zh(ax, 5.5, 3.0, "功耗三式（電阻兩端）", size=12, color="#1d4ed8", weight="bold")
    zh(ax, 5.5, 1.8, "P＝V·I　｜　P＝I²R　｜　P＝V²／R\n實際功耗要小於電阻額定功率", size=13, color=INK)
    footer(ax)
    save(fig, "poster_10_led_limit.png")


def poster_battery():
    fig, ax = new_fig()
    header(ax, "中四 DAT · 11", "電池內阻",
           "真實電池＝理想電動勢 E ＋ 串聯內阻 r｜有負載時端電壓 V＜E")
    round_box(ax, 0.3, 6.2, 10.4, 2.4, "#fef3c7", "#d97706", 2)
    zh(ax, 5.5, 8.2, "模型同公式", size=14, color="#92400e", weight="bold")
    zh(ax, 5.5, 7.15, "I＝E／(R＋r)\nV＝E−I·r＝I·R　　（V＝負載端電壓）", size=15, color=INK)

    round_box(ax, 0.3, 3.6, 10.4, 2.3, "#ecfdf5", "#10b981", 2)
    zh(ax, 5.5, 5.5, "示範", size=13, color="#047857", weight="bold")
    zh(ax, 5.5, 4.45, "E＝12 V，r＝1 Ω，R＝99 Ω\nI＝12／100＝0.12 A　　V＝12−0.12×1＝11.88 V", size=13, color=INK)

    round_box(ax, 0.3, 0.7, 10.4, 2.6, "#eff6ff", "#3b82f6", 1.5)
    zh(ax, 5.5, 2.9, "記住", size=13, color="#1d4ed8", weight="bold")
    zh(ax, 5.5, 1.8, "有電流就有「內阻壓降」I·r\n端電壓永遠低於電動勢 E（有負載時）", size=13, color=INK)
    footer(ax)
    save(fig, "poster_11_battery_ir.png")


def poster_acdc():
    fig, ax = new_fig()
    header(ax, "中四 DAT · 14", "交流／直流 AC·DC",
           "分別在電子流動方向｜變壓器主要服務交流")
    round_box(ax, 0.3, 6.2, 5.1, 2.4, "#dbeafe", "#2563eb", 2)
    zh(ax, 2.85, 8.2, "直流 DC", size=14, color="#1d4ed8", weight="bold")
    # flat line
    ax.plot([0.7, 5.0], [7.2, 7.2], color="#1d4ed8", lw=3)
    zh(ax, 2.85, 6.7, "方向不變｜電池常用\n例：乾電池 1.5 V", size=12, color=INK)

    round_box(ax, 5.6, 6.2, 5.1, 2.4, "#fce7f3", "#db2777", 2)
    zh(ax, 8.15, 8.2, "交流 AC", size=14, color="#be185d", weight="bold")
    xs = np.linspace(5.95, 10.3, 80)
    ys = 7.2 + 0.35 * np.sin((xs - 5.95) * 4)
    ax.plot(xs, ys, color="#be185d", lw=2.5)
    zh(ax, 8.15, 6.7, "方向來回改｜市電常用\n例：約 220 V、50 Hz", size=12, color=INK)

    round_box(ax, 0.3, 3.5, 10.4, 2.4, "#fef3c7", "#d97706", 2)
    zh(ax, 5.5, 5.5, "週期同頻率", size=13, color="#92400e", weight="bold")
    zh(ax, 5.5, 4.4, "一個完整重複＝一個週期（360°）\n頻率 f（Hz）＝每秒週期數　　f＝1／T（T 以秒計）\n例：T＝0.1 s → f＝10 Hz", size=12, color=INK)

    round_box(ax, 0.3, 0.7, 10.4, 2.5, "#eff6ff", "#3b82f6", 1.5)
    zh(ax, 5.5, 2.7, "對照", size=12, color="#1d4ed8", weight="bold")
    zh(ax, 5.5, 1.6, "DC：穩定單向　　AC：正弦波來回　　變壓器：主要轉交流電壓", size=13, color=INK)
    footer(ax)
    save(fig, "poster_14_ac_dc.png")


def poster_transistor():
    fig, ax = new_fig()
    header(ax, "中四 DAT · 15", "電晶體作開關／驅動",
           "NPN：基極 B 控制｜集極 C 接負載｜發射極 E 常接地｜細電流控大電流")
    round_box(ax, 0.3, 6.3, 10.4, 2.3, "#fef3c7", "#d97706", 2)
    zh(ax, 5.5, 8.2, "開關模式", size=14, color="#92400e", weight="bold")
    zh(ax, 5.5, 7.2, "截止 ≈ 開路（唔通）　　飽和導通 ≈ 近似短路（通）\n可用 Ib≈Ic／β 粗估基極電流", size=13, color=INK)

    round_box(ax, 0.3, 3.7, 10.4, 2.3, "#ecfdf5", "#10b981", 2)
    zh(ax, 5.5, 5.6, "典型接法（一句）", size=13, color="#047857", weight="bold")
    zh(ax, 5.5, 4.55, "單片機腳 → 基極電阻 → B\nLED＋限流在 C 到 Vcc；E 接地\n適合驅動 LED、繼電器、細摩打", size=12, color=INK)

    round_box(ax, 0.3, 0.7, 10.4, 2.7, "#eff6ff", "#3b82f6", 1.5)
    zh(ax, 5.5, 3.0, "角色", size=12, color="#1d4ed8", weight="bold")
    zh(ax, 5.5, 1.8, "半導體器件｜常用作放大器或電動開關\n今關重點：開關／驅動，唔深入偏壓放大器", size=13, color=INK)
    footer(ax)
    save(fig, "poster_15_transistor.png")


def poster_boss():
    fig, ax = new_fig()
    header(ax, "中四 DAT · 綜合", "綜合小測解題流程",
           "先判斷「求邊個量」，再揀公式｜少用提示、一次答對")
    steps = [
        ("①", "睇題", "已知邊啲？\n求 V／I／R／P？"),
        ("②", "單位", "kΩ→Ω\nmA→A"),
        ("③", "公式", "歐姆／分壓\n分流／功率"),
        ("④", "代入", "計數\n寫步驟"),
        ("⑤", "答案", "連單位\n自檢合理性"),
    ]
    for i, (n, t, b) in enumerate(steps):
        x = 0.35 + i * 2.1
        round_box(ax, x, 5.8, 1.95, 2.7, "#fff", "#3b82f6", 2)
        zh(ax, x + 0.97, 8.1, n + " " + t, size=13, color="#1d4ed8", weight="bold")
        zh(ax, x + 0.97, 6.8, b, size=11, color=INK)
        if i < 4:
            ax.annotate("", xy=(x + 2.05, 7.1), xytext=(x + 1.95, 7.1),
                        arrowprops=dict(arrowstyle="-|>", color="#3b82f6", lw=2, mutation_scale=12))

    round_box(ax, 0.3, 3.2, 10.4, 2.3, "#fef3c7", "#d97706", 2)
    zh(ax, 5.5, 5.1, "公式速查", size=13, color="#92400e", weight="bold")
    zh(ax, 5.5, 4.1, "V＝IR　｜　P＝VI＝I²R＝V²／R\n分壓：V1＝V·R1／(R1＋R2)　｜　分流：I1＝I·R2／(R1＋R2)", size=12, color=INK)

    round_box(ax, 0.3, 0.7, 10.4, 2.2, "#ecfdf5", "#10b981", 1.5)
    zh(ax, 5.5, 2.4, "自檢", size=12, color="#047857", weight="bold")
    zh(ax, 5.5, 1.5, "分壓：V1＋V2≈V　｜　分流：I1＋I2＝I　｜　內阻：有載時 V＜E", size=12, color=INK)
    footer(ax)
    save(fig, "poster_12_boss_flow.png")


if __name__ == "__main__":
    poster_ohm_intro()
    poster_parts()
    for w in ("v", "i", "r"):
        poster_solve(w)
    poster_power()
    poster_divider()
    poster_shunt()
    poster_color()
    poster_led()
    poster_battery()
    poster_acdc()
    poster_transistor()
    poster_boss()
    print("DONE", len(list(OUT.glob("poster_*.png"))))
