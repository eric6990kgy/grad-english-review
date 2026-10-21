# 研究所英文複習器

台大商研所 英文(A)、政大科智所 英文 B 的複習工具：單字間隔複習與總覽、選擇題（單字、文法、克漏字、閱讀）、錯題本、作文計時。

- **獨立版**（本 repo，GitHub Pages）：不用登入，進度存在瀏覽器，可匯出／匯入進度檔換裝置。
- **Claude 版**（claude.ai Artifact）：多了 AI 作文批改、AI 出題與補字、考古題匯入、新聞出題，進度跟帳號同步。

## 結構

- `index.html`：頁面原始碼，Claude 版與獨立版共用（沒有 `window.claude` 時自動切成獨立版）。
- `docs/`：GitHub Pages 發佈內容，由下面的腳本產生，不要手改。
- `seed/export_bank.py`：把 Claude 版題庫（ArtifactData 匯出的 `bank/*.json`）轉成 `docs/bank.json`。
- `seed/build_site.py`：把 `index.html` 包上完整 HTML 外框，輸出到 `docs/index.html`。

## 更新題庫

```bash
python seed/export_bank.py <ArtifactData 匯出資料夾> docs/bank.json
python seed/build_site.py
git add docs && git commit -m "Update question bank" && git push
```
