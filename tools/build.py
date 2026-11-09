# Build the 會考數學 site from the 學測 site engine (ref/index.html) + data/*.json
import json, os, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(ROOT, *a)

src = open(P('ref', 'index.html'), encoding='utf-8').read()
lines = src.split('\n')

def rep(s, old, new, count=1):
    n = s.count(old)
    if n != count:
        sys.exit(f'replace expected {count} got {n}: {old[:80]!r}')
    return s.replace(old, new)

# ---------- data ----------
YEARS = [111, 112, 113, 114, 115]
DATA = []
for y in YEARS:
    f = P('data', f'{y}.json')
    if os.path.exists(f):
        DATA += json.load(open(f, encoding='utf-8'))
UNITS = json.load(open(P('data', 'units.json'), encoding='utf-8'))
NOTES = json.load(open(P('data', 'notes.json'), encoding='utf-8')) if os.path.exists(P('data', 'notes.json')) else {}
CARDS = json.load(open(P('data', 'cards.json'), encoding='utf-8')) if os.path.exists(P('data', 'cards.json')) else {}
NONSEL = json.load(open(P('data', 'nonsel.json'), encoding='utf-8'))
IMGS = {}
for d in DATA:
    fn = f"M{d['year']}-{int(d['no']):02d}.png" if d['exam'] == '選擇' else f"M{d['year']}-N{int(d['no'])}.png"
    if os.path.exists(P('site', 'q', fn)):
        IMGS[f"{d['exam']}|{d['year']}|{int(d['no'])}"] = [fn]
J = lambda o: json.dumps(o, ensure_ascii=False)

def line_idx(prefix):
    for i, l in enumerate(lines):
        if l.startswith(prefix):
            return i
    sys.exit('no line ' + prefix)

lines[line_idx('const DATA =')] = f'const DATA = {J(DATA)};'
lines[line_idx('const UNITS =')] = f'const UNITS = {J(UNITS)};'
lines[line_idx('const NOTES =')] = f'const NOTES = {J(NOTES)};'
lines[line_idx('const IMGS =')] = f'const IMGS = {J(IMGS)};'
lines[line_idx('const ART =')] = f"const ART = {J(sorted(f[:-5] for f in os.listdir(P('site','art')) if f.startswith('U') and f.endswith('.webp')))};"
lines[line_idx('const CARDS =')] = f'const CARDS = {J(CARDS)};'
lines[line_idx('const EXAMS=')] = f'const EXAMS=["選擇","非選"], YEARS={J(YEARS)}, DIFFS=["易","中","難"];\nconst NONSEL = {J(NONSEL)};'
s = '\n'.join(lines)

n_q = len(DATA)
n_pass = [d['rate'] for d in DATA if d.get('rate') is not None]

# ---------- head / masthead ----------
desc = f'看懂命題趨勢，找到備考方向。111–115 年國中教育會考數學科共 {n_q} 題，依單元整理出題次數、通過率與難度，附原題、答案與解題引導。'
s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', s)
s = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="會考數學考點導航">', s)
s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', s)
s = re.sub(r'<meta property="og:image" content="[^"]*">\n?', '', s)
s = rep(s, '<title>數學考點導航</title>', '<title>會考數學考點導航</title>')
s = rep(s, '<div class="eyebrow">111–115 學年度｜學測數 A・數 B｜分科數甲・數乙</div>', '<div class="eyebrow">111–115 年｜國中教育會考｜數學科</div>')
s = rep(s, '<h1>數學考點導航</h1>', '<h1>會考數學考點導航</h1>')
s = rep(s, '<p>大考數學，不只是做過多少題，更重要的是看懂考題背後的觀念與脈絡。</p>', '<p>會考數學，不只是做過多少題，更重要的是看懂考題背後的觀念與脈絡。</p>')
s = re.sub(r'<p>從近五年 17 份大考試卷出發.*?</p>', '<p>從近五年 5 份會考數學試卷、共 135 題出發，將歷屆試題依國中數學單元重新整理，透過出題次數、全國通過率與難度分析，幫助你掌握各單元的命題分布。從考點分析到實際練習，讓每一次複習都有方向。</p>', s, flags=re.S)
s = rep(s, '<li><b>看考點</b><span>掌握各單元歷年出題次數與配分</span></li>', '<li><b>看考點</b><span>掌握各單元歷年出題次數與通過率</span></li>')
s = rep(s, '<li><b>找試題</b><span>依考科、年度、難度與單元篩選</span></li>', '<li><b>找試題</b><span>依題型、年度、難度與單元篩選</span></li>')
s = re.sub(r'<img class="art hero" src="art/hero.webp" alt="[^"]*"', '<img class="art hero" src="art/hero.webp" alt="戴眼鏡、穿制服的柴犬吉祥物站在答案卡上，身邊漂浮著骰子、三角板、立方體與圓規"', s)
s = rep(s, '.hero-band{grid-area:band;background:#f7dbe2;', '.hero-band{grid-area:band;background:#d7ecf6;')

# accent: teal-blue instead of rose so the two sites are told apart
s = s.replace('--omr:#c8325a; --omr-soft:#f8e4ea;', '--omr:#1d6a86; --omr-soft:#e0eef3;')
s = s.replace('--heat-0:#eef0eb; --heat-1:#f3c9d4; --heat-2:#e891a8; --heat-3:#d4567a; --heat-4:#a8213f;', '--heat-0:#eef0eb; --heat-1:#cde4ec; --heat-2:#8fc2d5; --heat-3:#3f8fae; --heat-4:#1b5870;')
s = s.replace('--omr:#f0789a; --omr-soft:#3a2129;', '--omr:#6cc3e0; --omr-soft:#17303a;')
s = s.replace('--heat-0:#262b35; --heat-1:#4a2632; --heat-2:#7a3149; --heat-3:#b84468; --heat-4:#f0789a;', '--heat-0:#262b35; --heat-1:#1f3a46; --heat-2:#28566a; --heat-3:#3f8fae; --heat-4:#6cc3e0;')

# ---------- filter bar ----------
s = rep(s, '<span class="lab">考科</span>', '<span class="lab">題型</span>')
s = rep(s, '<button data-sort="points">配分</button><button data-sort="count">題數</button>', '<button data-sort="count">題數</button><button data-sort="hard">難度</button>')
s = rep(s, 'placeholder="搜尋：條件機率、外積、黎曼和…"', 'placeholder="搜尋：圓周角、盒狀圖、相似…"')
s = rep(s, '<h2><span>單元排行</span><span id="idx-unit">配分</span></h2>', '<h2><span>單元排行</span><span id="idx-unit">題數</span></h2>')

# overview table head + 非選 section
s = rep(s, '<thead><tr><th>名次</th><th>單元</th><th>題數</th><th>配分</th><th>占比</th><th class="bar-cell">相對比重</th><th>111–115 每年配分</th></tr></thead>',
        '<thead><tr><th>名次</th><th>單元</th><th>題數</th><th>占比</th><th>平均通過率</th><th class="bar-cell">相對比重</th><th>111–115 每年題數</th></tr></thead>')
s = rep(s, '每年配分色階', '每年題數色階')
s = rep(s, '少 → 多，格內數字為該年配分</div>', '少 → 多，格內數字為該年題數。難度依心測中心公布的全國通過率：$\\ge70\\%$ 為易、$45\\%$～$69\\%$ 為中、未滿 $45\\%$ 為難；非選擇題一律列為難。</div>')
s = rep(s, '    </section>\n    <div id="units"',
        '    </section>\n    <section class="overview nonsel" aria-labelledby="ns-h"><div><h2 class="sec" id="ns-h">非選擇題級分分布</h2><p class="note">兩題非選合計 $0$ 至 $6$ 級分，數字為全國到考生人數百分比（含兩題皆空白者）。</p></div><div class="ovtable"><table id="nstab"></table></div></section>\n    <div id="units"')

s = rep(s, '"全部考科與年度。"', '"全部題型與年度。"')
# footer
s = re.sub(r'<footer>.*?</footer>', '''<footer>
    <div>資料來源：國中教育會考網站（心理與教育測驗研究發展中心）歷屆試題、選擇題參考答案、各題通過率、非選擇題評分規準與各級分人數百分比統計表。解題引導為整理撰寫，非心測中心官方解答；難度依全國通過率分級。</div>
    <div><a href="https://cap.rcpet.edu.tw/examination.html" target="_blank" rel="noopener">國中教育會考歷屆試題</a></div>
  </footer>''', s, flags=re.S)

# ---------- engine ----------
s = s.replace('"qmap-state2"', '"capmap-state1"').replace('"qmap-done"', '"capmap-done"')
s = rep(s, 'sort:"points",ctx:false,todo:false,q:""', 'sort:"count",ctx:false,todo:false,q:""')
s = rep(s, 'state.sort=s.sort||"points"', 'state.sort=s.sort==="hard"?"hard":"count"')
s = rep(s, 'document.getElementById("idx-unit").textContent=state.sort==="points"?"配分":"題數";', 'document.getElementById("idx-unit").textContent=state.sort==="hard"?"平均通過率":"題數";')
s = rep(s, 'const examOrder={"數A":0,"數B":1,"數甲":2,"數乙":3};', 'const examOrder={"選擇":0,"非選":1};\nconst avgRate=qs=>{const r=qs.filter(d=>d.rate!=null);return r.length?r.reduce((a,d)=>a+d.rate,0)/r.length:null};\nconst pct=v=>v==null?"—":Math.round(v*100)+"%";')
# stats: 題 / 份試卷 / 平均通過率
s = rep(s, '<div class="stat"><b>${totalPts}</b><span>分</span></div><div class="stat"><b>${new Set(rows.map(d=>d.exam+d.year)).size}</b><span>份試卷</span></div>',
        '<div class="stat"><b>${new Set(rows.map(d=>d.year)).size}</b><span>份試卷</span></div><div class="stat"><b>${pct(avgRate(rows))}</b><span>選擇題平均通過率</span></div>')
s = rep(s, 'u.count++;u.points+=+d.points||0;u.yr[d.year]=(u.yr[d.year]||0)+(+d.points||0);u.qs.push(d)});',
        'u.count++;u.yr[d.year]=(u.yr[d.year]||0)+1;u.qs.push(d)});Object.values(by).forEach(u=>u.rate=avgRate(u.qs));')
s = rep(s, 'LIST=Object.values(by).sort((a,b)=>state.sort==="points"?b.points-a.points||b.count-a.count:b.count-a.count||b.points-a.points);',
        'LIST=Object.values(by).sort((a,b)=>state.sort==="hard"?(a.rate??2)-(b.rate??2)||b.count-a.count:b.count-a.count||(a.rate??2)-(b.rate??2));')
s = rep(s, 'const val=u=>state.sort==="points"?u.points:u.count;', 'const val=u=>state.sort==="hard"?(u.rate==null?0:1-u.rate):u.count;\n  const lab=u=>state.sort==="hard"?pct(u.rate):u.count;')
s = rep(s, '<span class="pt">${val(u)}</span>', '<span class="pt">${lab(u)}</span>')
s = rep(s, '<td class="num">${u.count}</td><td class="num">${u.points}</td><td class="num">${totalPts?(u.points/totalPts*100).toFixed(1):0}%</td>',
        '<td class="num">${u.count}</td><td class="num">${rows.length?(u.count/rows.length*100).toFixed(1):0}%</td><td class="num">${pct(u.rate)}</td>')
s = rep(s, 'title="${y} 年 ${u.yr[y]||0} 分"', 'title="${y} 年 ${u.yr[y]||0} 題"')
s = rep(s, '<span>${u.count} 題</span><span>${u.points} 分</span>', '<span>${u.count} 題</span><span>平均通過率 ${pct(u.rate)}</span>')
s = rep(s, '<h4>題數分布（考科 × 年度）</h4>', '<h4>題數分布（題型 × 年度）</h4>')
s = rep(s, '<span class="qm">${esc(d.type)}・${d.points}分${d.rate!=null?`・答對率 ${Math.round(d.rate*100)}%`:""}</span>',
        '<span class="qm">${esc(d.type)}${d.rate!=null?`・通過率 ${Math.round(d.rate*100)}%`:""}</span>')
s = rep(s, 'alt="${d.year} ${d.exam} 第${esc(d.no)}題${src.includes("-g")?"題組說明":"題目"}"', 'alt="${d.year} 年會考數學 ${d.exam}第${esc(d.no)}題"')
s = rep(s, '<span class="qx">${d.year}・${d.exam}</span><span class="qn"><span class="dot"></span>第${esc(d.no)}題</span>',
        '<span class="qx">${d.year}・會考</span><span class="qn"><span class="dot"></span>${d.exam==="非選"?"非選第"+esc(d.no)+"題":"第"+esc(d.no)+"題"}</span>')
# 非選 table + typeset legend/notes once
s = rep(s, 'sync();render();barH();', '''function nsTable(){const lv=["零","一","二","三","四","五","六"];
  document.getElementById("nstab").innerHTML=`<thead><tr><th>年度</th>${lv.map(l=>`<th>${l}級分</th>`).join("")}<th>平均級分</th></tr></thead><tbody>${YEARS.map(y=>{const r=NONSEL[y];if(!r)return"";const mx=Math.max(...r);const avg=r.reduce((a,v,i)=>a+v*i,0)/r.reduce((a,v)=>a+v,0);
  return `<tr><td class="rk">${y}</td>${r.map(v=>`<td class="num"><span class="nsb" style="--w:${v/mx*100}%">${v.toFixed(1)}%</span></td>`).join("")}<td class="num">${avg.toFixed(2)}</td></tr>`}).join("")}</tbody>`}
nsTable();
sync();render();barH();
window.addEventListener("load",()=>document.querySelectorAll(".legend,.nonsel .note").forEach(typeset));''')

# ---------- 解題引導 v2：讀懂題目 → 破題 → 觀念引導 → 一步一步來（提示 → 看做法）----------
NEW_SCAFFOLD = r'''function scaffold(d,sec){const t=d.detail;const steps=t.steps||[];const rd=t.read||{};const L=a=>a||[];
  const stepBody=s=>`${s.hint?`<p class="hint"><b>提示</b>${esc(s.hint)}</p>`:""}<details class="how"><summary>看做法</summary><div class="calc">${L(s.calc).map(l=>`<div>${esc(l)}</div>`).join("")}</div>${s.why?`<p class="why">${esc(s.why)}</p>`:""}</details>`;
  return `<details class="sol scaf"><summary><span class="show">開始解題引導</span><span class="hide">收起解題引導</span></summary>
  <div class="scb">
    <section class="sc-guide"><h6>這題的關鍵</h6><p>${esc(t.idea||"")}</p>
      <p class="sc-topic">考點：${esc(d.topic)}${d.context?`<span class="ctx">・${esc(d.context)}</span>`:""}${sec?`<span class="x">｜跨單元：${esc(sec)}</span>`:""}</p></section>
    ${L(rd.given).length?`<section class="sc-read"><h6><span class="stg">1</span>讀懂題目</h6>
      <div class="rd"><div class="rd-col"><b>已知</b><ul>${rd.given.map(g=>`<li>${esc(g)}</li>`).join("")}</ul></div>
      <div class="rd-col"><b>要求</b><p>${esc(rd.ask||"")}</p></div></div>
      ${L(rd.keys).length?`<div class="keys"><b>圈出關鍵字</b><ul>${rd.keys.map(k=>`<li><mark>${esc(k[0])}</mark><span>${esc(k[1])}</span></li>`).join("")}</ul></div>`:""}</section>`:""}
    ${L(t.crack).length?`<section class="sc-crack"><h6><span class="stg">2</span>破題：先問自己</h6><p class="sc-tip">先自己想一想，再點開對照。</p>
      <ol>${t.crack.map(c=>`<li><details class="ck"><summary><span class="sq">${esc(c.q)}</span><span class="sh">對照想法</span></summary><p>${esc(c.a)}</p></details></li>`).join("")}</ol></section>`:""}
    ${L(t.concepts).length||L(t.formulas).length?`<section class="sc-concept"><h6><span class="stg">3</span>觀念引導</h6>
      ${L(t.concepts).length?`<div class="cps">${t.concepts.map(c=>`<div class="cp"><div class="cp-n">${esc(c.name)}</div><p>${esc(c.body)}</p>${c.eg?`<p class="cp-eg"><b>例</b>${esc(c.eg)}</p>`:""}</div>`).join("")}</div>`:""}
      ${L(t.formulas).length?`<div class="sc-know"><div class="sub">會用到的公式</div><div class="fboxes">${t.formulas.map(fbox).join("")}</div></div>`:""}</section>`:""}
    <section class="sc-steps"><div class="sc-head"><h6><span class="stg">4</span>一步一步來</h6><button type="button" class="sc-all" data-all>全部展開</button></div>
      <p class="sc-tip">每一步先看提示，自己動手算，再點「看做法」對照。</p>
      <ol>${steps.map((s,i)=>`<li><details class="step"><summary><span class="sn">${i+1}</span><span class="sq">${esc(s.q)}</span><span class="sh">看提示</span></summary>${stepBody(s)}</details></li>`).join("")}</ol></section>
    <details class="sc-ans"><summary>算完了，看答案</summary><div>
      <p class="ansline"><b>答</b><span class="ans">${esc(t.answer||d.answer)}</span>${t.approx?`<span class="approx">${esc(t.approx)}</span>`:""}</p>
      ${t.check?`<p class="chk2"><b>驗算</b>${esc(t.check)}</p>`:""}
      ${L(t.wrong).length?`<div class="wrong"><b>常見錯誤</b><ul>${t.wrong.map(w=>`<li><span class="wopt">${esc(w.opt)}</span>${esc(w.how)}</li>`).join("")}</ul></div>`:""}
      ${L(t.tiers).length?`<div class="tiers"><b>評分重點</b><ul>${t.tiers.map(x=>`<li><span class="tk">${esc(x[0])}</span>${esc(x[1])}</li>`).join("")}</ul></div>`:""}
    </div></details>
    ${t.takeaway?`<p class="sc-take"><b>一句話心法</b>${esc(t.takeaway)}</p>`:""}
    ${d.pitfall&&!L(t.wrong).length?`<p class="sc-pit"><b>易錯</b>${esc(d.pitfall)}</p>`:""}
  </div></details>`}
'''
i0 = s.index('function scaffold(d,sec){'); i1 = s.index('/* KaTeX', i0)
s = s[:i0] + NEW_SCAFFOLD + s[i1:]
s = rep(s, 'const steps=[...box.querySelectorAll("details.step")];', 'const steps=[...box.querySelectorAll("details.step,details.how")];')
V2CSS = '''
.stg{display:inline-grid;place-items:center;width:1.55em;height:1.55em;border-radius:50%;background:var(--omr);color:var(--sheet);font-size:11px;font-family:var(--f-mono);margin-right:7px;vertical-align:1px}
.sc-read .rd{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px}
.rd-col{border:1px solid var(--rule);border-radius:8px;padding:8px 12px;background:var(--paper);min-width:0;overflow-x:auto}
.rd-col > b,.keys > b,.sc-know .sub{display:block;font-size:12px;letter-spacing:.08em;color:var(--ink-2);margin-bottom:3px;font-weight:500}
.rd-col ul{margin:0;padding-left:1.1em;display:grid;gap:3px}
.rd-col li::marker{color:var(--omr)}
.rd-col p{margin:0}
.keys{margin-top:8px}
.keys ul{list-style:none;margin:0;padding:0;display:grid;gap:5px}
.keys li{display:grid;grid-template-columns:auto minmax(0,1fr);gap:4px 10px;align-items:baseline}
.keys mark{background:var(--heat-1);color:var(--ink);padding:0 7px;border-radius:4px;font-weight:700;white-space:nowrap}
.sc-crack ol{margin:0;padding:0;list-style:none;display:grid;gap:6px}
details.ck{border:1px dashed var(--ink-3);border-radius:8px;background:var(--sheet)}
details.ck summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px;padding:8px 12px;align-items:baseline}
details.ck summary::-webkit-details-marker{display:none}
details.ck .sh{font-size:12px;color:var(--omr);white-space:nowrap}
details.ck[open] .sh{visibility:hidden}
details.ck > p{margin:0;padding:8px 12px 10px;border-top:1px dashed var(--rule)}
.cps{display:grid;gap:8px}
.cp{border-radius:8px;background:var(--omr-soft);padding:10px 14px;min-width:0}
.cp-n{font-weight:700;color:var(--omr);margin-bottom:2px}
.cp p{margin:0}
.cp-eg{font-size:13.5px;color:var(--ink-2);margin-top:4px!important}
.cp-eg b{font-size:12px;margin-right:6px;color:var(--omr)}
.sc-concept .sc-know{margin-top:10px}
.hint{margin:0;padding:0 12px 6px calc(12px + 1.6em + 10px);font-size:14px}
.hint b{font-size:12px;color:var(--mid);letter-spacing:.08em;margin-right:8px}
details.how{margin:0 12px 10px calc(12px + 1.6em + 10px);border-top:1px dashed var(--rule)}
details.how summary{cursor:pointer;font-size:13px;color:var(--omr);padding:6px 0;font-weight:500}
details.how .calc,details.how .why{padding-left:0!important}
@media (max-width:640px){.hint{padding-left:10px}details.how{margin-left:10px}}
'''
s = rep(s, '</style>\n\n<header class="mast">', V2CSS + '</style>\n\n<header class="mast">')

# small css for 非選 bars
s = rep(s, '</style>\n\n<header class="mast">', '.nsb{display:inline-block;min-width:4.2em;padding:1px 6px;border-radius:3px;background:linear-gradient(90deg,var(--omr-soft) var(--w),transparent var(--w))}\n</style>\n\n<header class="mast">')

os.makedirs(P('site'), exist_ok=True)
open(P('site', 'index.html'), 'w', encoding='utf-8').write(s)
art = s.split('<body>', 1)[1].replace('</body>', '').replace('</html>', '').lstrip('\n')
assert art.startswith('<title>')
open(P('site', 'artifact.html'), 'w', encoding='utf-8').write(art)
print('built', n_q, 'questions,', len(IMGS), 'images')
