# 每年更新流程（加入新一年的會考數學）

網站永遠顯示「有資料的最近五年」。加入 `NEW` 年（例如 116）後，`build.py` 會自動改成 112–116，標題、題數、年度表頭都跟著變；舊年份的 json 留在 `tools/data/` 不刪。

以下 `NEW` 代表要加入的年度，`REPO` 是這個 repo 的根目錄。Python 一律用 `python -X utf8`，需要 pymupdf、pdfplumber、Pillow。

## 0. 先確認官方檔案都公布了

心測中心歷屆試題頁：`https://cap.rcpet.edu.tw/exam/NEW/NEWexam.html`（頁面裡的連結都是 Google Drive）。

```bash
curl -sL "https://cap.rcpet.edu.tw/exam/NEW/NEWexam.html" | grep -o 'href="https://drive.google.com/file/d/[^/]*/[^"]*"[^>]*>[^<]*' | sed -E 's#href="https://drive.google.com/file/d/([^/]*)/.*>([^<]*)#\1 \2#' | grep -E '參考答案|^[^ ]+ 數學科$|通過率|數學非選|第一題|第二題'
```

需要這 6 個檔：`數學科`（試題本）、`參考答案`、`各題通過率`、`數學非選擇題各級分人數百分比統計表`、非選 `第一題`、`第二題`（評分規準）。
**任何一個還沒公布（尤其是通過率），就停在這裡，不要改任何檔案**，回報缺哪些。

下載（每個 Drive id 一次）：

```bash
curl -sL "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t" -o NEW-math.pdf
```

檔名用 `NEW-math.pdf`、`NEW-ans.pdf`、`NEW-pass.pdf`、`NEW-nonsel.pdf`、`NEW-rubric1.pdf`、`NEW-rubric2.pdf`，放在 repo 外的暫存資料夾（不要 commit PDF）。確認每個檔開頭是 `%PDF-`。

## 1. 答案、通過率、非選級分 → `tools/data/key.json`、`nonsel.json`

用 pdfplumber 的 `pages[0].extract_table()`：

- 參考答案表：表頭是「國文｜英語(閱讀、聽力)｜數學｜社會｜自然」，**數學在第 5 欄（index 5）**，資料從第 3 列開始。
- 通過率表：表頭「題序｜國文｜英語(聽力)｜英語(閱讀)｜數學｜社會｜自然」，**數學在 index 4**。
- 非選級分表：第 2 列的 7 個百分比（零到六級分，含兩題皆空白者那一版，即第一張表）。

**欄位順序以當年 PDF 的表頭為準，先印出表頭核對再取值。** 驗證：第 1 題自己算一次，答案要和取出的字母一致。
把 `{"ans": {"1": "C", …}, "pass": {"1": "0.83", …}}` 加進 `key.json` 的 `"NEW"`；把 7 個數字加進 `nonsel.json` 的 `"NEW"`。

## 2. 題目圖 → `q/MNEW-01.png` … `q/MNEW-25.png`、`q/MNEW-N1.png`、`q/MNEW-N2.png`

用 pymupdf 以 `Matrix(2,2)` 渲染試題本，每題從題號上方裁到下一題上方，整個文字欄寬，包含圖與選項；不含頁首頁尾與非選作答空白。跨頁就上下拼接。去白邊留約 12px，轉 8-bit 灰階 PNG，每張 150KB 以下。
題組共用的文章或表格，放在每一題的圖上方。**每張有圖的裁切都要用眼睛看過**。

## 3. 寫 `tools/data/NEW.json`（27 筆）

先讀 `tools/data/style.md`（數學式體例）與 `tools/data/guide_spec.md`（解題引導 v2 規格）。格式完全比照 `tools/data/115.json`：

- 順序：選擇 1–25，接著非選 1–2；`exam` 為 `選擇`／`非選`，`no` 為字串，`type` 為 `單選`／`非選`，`points` 為 1。
- `unit` 只能用 `units.json` 的代碼；`secondary` 可空。
- `rate`：選擇題填通過率數字，非選填 null。`difficulty`：通過率 $\ge0.70$ 易、$0.45$～$0.69$ 中、未滿 $0.45$ 難；非選一律難。
- `answer` 選擇題寫 `(C)` 這種格式，必須等於官方答案。
- `detail` 必須有 `idea`、`read`、`crack`、`concepts`、`formulas`、`steps`（每步有 hint）、`answer`、`check`、`wrong`（選擇題，自己算過）、`tiers`（非選，依評分規準寫零到三級分）、`takeaway`。
- 每題都要自己解一次，看著題目圖解；和官方答案不同時，重看題目直到一致。`verified` 設 true。

27 題分量大，可以分成幾段寫，但交出前整份跑第 5 步的檢查。

## 4. 更新單元說明 `tools/data/notes.json`

新的五年範圍（例如 112–116）重算每個單元的題數、平均通過率、每年題數，改寫 `notes.json` 中數字或「哪一年起」之類的敘述，讓它和新資料一致。不要寫資料裡沒有的說法。`cards.json`（公式卡）通常不用動。

## 5. 檢查、建置

```bash
python -X utf8 tools/lint.py     # 必須 problems: 0
python -X utf8 tools/build.py    # 產生 index.html
```

用無頭瀏覽器開 `index.html`（在 repo 根目錄起 `python -m http.server`），確認沒有 console error、總覽年度變成新的五年、隨機開兩題 NEW 年的解題引導看得到所有段落。

## 6. 發布

```bash
git add -A
git commit -m "加入 NEW 年會考數學"
git push
```

推上去後等 GitHub Pages 建置（`gh api repos/bgjd315-cloud/cap-math-map/pages/builds/latest --jq .status` 變成 `built`），再確認 `https://bgjd315-cloud.github.io/cap-math-map/` 的標題列年度是新的五年。

回報：新增了幾題、哪些題目讀圖不確定、通過率最低的三題、各單元題數的明顯變化。
