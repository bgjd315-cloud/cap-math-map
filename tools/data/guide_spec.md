# 解題引導 v2 規格（國中生版）

讀者是國中生，程度從 C 到 A 都有。目標是讓學生「自己想得出來」，不是看懂答案。
語氣：像老師在旁邊陪寫，句子短、口語、具體；不說教、不寫「相信你一定可以」這類客套話。
所有數學式仍遵守 data/style.md（$…$、\dfrac、$…$ 內不得有 /、無 Unicode 根號與上下標、台灣用語）。

## detail 物件新增／改寫的欄位

1. `read`（讀懂題目）— 必填
   - `given`：已知條件陣列，一條一項，用數學式寫清楚；圖上標示的數據也要列出並註明「圖上標示」。情境題要把文字翻成數量關係（例如「每週多 $2$ 圈」）。
   - `ask`：一句話，題目到底要求什麼；若可以，改寫成數學式（例如周長 $=\overline{AD}+\overline{DE}+\overline{EF}+\overline{FA}$）。
   - `keys`：2–4 組 [關鍵字或條件, 它在提示你什麼]。挑學生容易漏看或誤解的字眼（「至少」「最早」「取後不放回」「整數」「不含」「依序」、單位換算、圖形未依比例等）。
2. `crack`（破題）— 必填，2–4 題 [{q, a}]
   像蘇格拉底式提問，引導學生自己找到切入點。q 是提問，a 是想法（1–2 句）。順序要像真實的思考：先看要求 → 看缺什麼 → 從條件找到工具。最後一題的 a 要點出整題策略。
3. `concepts`（觀念引導）— 必填，1–3 個 {name, body, eg}
   - `name`：觀念名稱（例如「SAS 全等」「百分率的基準量」）。
   - `body`：2–4 句，用國中生聽得懂的話講「這個觀念是什麼、為什麼成立或為什麼可以這樣做、這題怎麼用到它」。可提醒常見誤解。
   - `eg`：可省；一個極短的小例子或反例，幫助理解（例如「$SSA$ 不一定全等：兩邊和非夾角相等，可以畫出兩種三角形」）。
   - 觀念引導和公式框分工：formulas 放公式本身；concepts 講道理與直覺，不要只是重抄公式。
4. `idea`：保留，改成一句話的「破題結論」（整題策略），會顯示在最上面。
5. `steps`：改得更細，3–6 步，每步一個小動作。每步 {q, hint, calc, why}
   - `q`：這一步要做什麼（提問句）。
   - `hint`：必填，一句提示，只指方向不給答案（例如「找一找哪兩個三角形各包含這三個條件」）。
   - `calc`：一行一式，不跳步；國中生容易卡的移項、通分、約分都要寫出來。
   - `why`：可省；這一步為什麼可以這樣做，或容易犯的錯。
6. 其餘欄位（formulas、answer、approx、check、wrong、tiers、takeaway）保留並沿用原規則；check 盡量寫出代回檢查或合理性判斷。
7. 非選題：read/crack/concepts 涵蓋全部小題；steps 的 q 前面加小題編號 (1)(2)。tiers 保留。

## 範例（115 年第 12 題）

```json
"read": {
  "given": ["$\\overline{AB}=15$、$\\overline{AC}=9$、$\\overline{BC}=16$（圖上標示）",
            "$D$ 在 $\\overline{AB}$ 上，$E$、$F$ 在 $\\overline{BC}$ 上",
            "$\\overline{BE}=\\overline{AF}$、$\\angle BED=\\angle AFC$、$\\overline{ED}=\\overline{FC}$"],
  "ask": "四邊形 $ADEF$ 的周長，也就是 $\\overline{AD}+\\overline{DE}+\\overline{EF}+\\overline{FA}$。",
  "keys": [["周長", "四條邊的和；不一定要每條邊都算出來，只要知道總和。"],
           ["兩組邊相等，加上一組角相等", "這是全等的訊號，先檢查角是不是夾在兩邊中間。"]]
},
"crack": [
  {"q": "$ADEF$ 的四條邊，有哪一條是題目直接給的？", "a": "一條都沒有。所以要想辦法把它們換成已知長度的線段。"},
  {"q": "三個相等的條件分別落在哪兩個三角形裡？", "a": "$\\overline{BE}$、$\\overline{ED}$、$\\angle BED$ 都在 $\\triangle BED$；$\\overline{AF}$、$\\overline{FC}$、$\\angle AFC$ 都在 $\\triangle AFC$。角剛好夾在兩邊中間。"},
  {"q": "全等之後，可以把哪些邊換掉？", "a": "$\\overline{BD}=\\overline{AC}$ 可以算出 $\\overline{AD}$；$\\overline{DE}$、$\\overline{FA}$ 可以換成 $\\overline{FC}$、$\\overline{BE}$，和 $\\overline{EF}$ 接成整條 $\\overline{BC}$。"}
],
"concepts": [
  {"name": "SAS 全等", "body": "兩個三角形有兩組邊對應相等，而且這兩邊所夾的角也相等，兩個三角形就完全一樣大。全等以後，對應的邊、對應的角都相等，可以拿來互相替換。", "eg": "角一定要夾在兩邊中間；兩邊和一個非夾角相等（$SSA$）不一定全等。"},
  {"name": "用相等的線段替換", "body": "求周長時，看不到的邊可以用相等的邊代替。如果替換後的幾段剛好首尾相接，就能合成一條已知長度的線段。"}
],
"steps": [
  {"q": "先確認哪兩個三角形全等。", "hint": "把三個條件分別圈在含有它們的三角形上。",
   "calc": ["$\\overline{BE}=\\overline{AF}$", "$\\angle BED=\\angle AFC$", "$\\overline{ED}=\\overline{FC}$", "所以 $\\triangle BED\\cong\\triangle AFC$（$SAS$）"], "why": ""},
  {"q": "$\\overline{BD}$ 對應到哪一條邊？", "hint": "$B$ 對應 $A$，$D$ 對應 $C$。",
   "calc": ["$\\overline{BD}=\\overline{AC}=9$"], "why": "對應頂點要照全等式的順序寫，才不會配錯邊。"},
  {"q": "$\\overline{AD}$ 多長？", "hint": "$D$ 在 $\\overline{AB}$ 上，$\\overline{AB}$ 被分成兩段。",
   "calc": ["$\\overline{AD}=\\overline{AB}-\\overline{BD}$", "$=15-9=6$"], "why": ""},
  {"q": "另外三條邊的和是多少？", "hint": "把 $\\overline{DE}$、$\\overline{FA}$ 換成 $\\overline{BC}$ 上的線段。",
   "calc": ["$\\overline{DE}+\\overline{EF}+\\overline{FA}$", "$=\\overline{FC}+\\overline{EF}+\\overline{BE}$", "$=\\overline{BC}=16$"], "why": "$\\overline{BE}$、$\\overline{EF}$、$\\overline{FC}$ 在 $\\overline{BC}$ 上首尾相接。"},
  {"q": "把周長加起來。", "hint": "周長 $=\\overline{AD}+$（另外三條邊的和）。",
   "calc": ["周長 $=6+16=22$"], "why": ""}
]
```
