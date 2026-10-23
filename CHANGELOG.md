# CHANGELOG · 電學三欄

## 2026-10-23 · 去裁圖信用、改校本自製
- 頁腳／`noteZh`／`uiNoteZh`／零件 tips：改為「校本自製示意圖 · DAT」，唔再提及外來教材來源。
- `questions.json` 同 `app.js` 內嵌 BANK：舊裁圖路徑全部改指根目錄自畫／教學卡（`card_*`、`color_code_chart.png`、`formula_card.png`、`step_solve.png`、`led_power.png`、分壓／分流／串並聯／AC·DC 等）。
- 無卡覆蓋嘅三張（喇叭／蜂鳴器／咪、保險絲／開關／繼電器、變壓器）放喺 `assets/symbols/`。
- 刪未用 orphan 色環裁圖；生成腳本改名為 `make_symbol_photo_cards.py`。
- 重打 offline 包（主檔＋ no-edb 別名）。

## 較早
- 零件教學卡 `card_*.png`；右欄定義可附 figure；計數關 materializeLevel 抽數；分壓／分流 multi 輸入。

## 2026-10-23 no-EDB pure symbols
- Rewrote all card_*.png as pure circuit-symbol cards (no photos, ACK=校本自製示意 · DAT)
- Redrew card_color_code.png + assets/symbols/{fuse_switch_relay,speaker_buzzer_mic,transformer}.png
- Text: 符號＋實物 → 電路符號示意; removed 學習資源本節實物圖
