# 그래프 가독성 개선 (v3): 결론형 제목, 큰 글자, 단순한 형태
import os, re
H = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(H, "site_template.html")
s = open(p, encoding="utf-8").read()
assert "v3-charts" not in s

def rep(a, b):
    global s
    assert s.count(a) == 1, a
    s = s.replace(a, b)

# ---- CSS ----
rep("/* v2-bling */", """/* v3-charts */
svg text{font-size:13px}
svg text.v{fill:var(--ink);font-weight:700;font-size:14px}
svg text.ax{fill:var(--muted);font-size:12.5px}
svg text.ttl{fill:var(--muted);font-size:13px;font-weight:600}
svg .grid{stroke:var(--line);stroke-width:1}
.ck{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:13.5px;color:var(--muted);margin:6px 0 10px}
.ck span{display:inline-flex;align-items:center;gap:7px}
.ck i{display:inline-block;width:12px;height:12px;border-radius:50%}
.ck i.sq{border-radius:3px}.ck i.ln{width:22px;height:3px;border-radius:2px}
.how{font-size:14px;color:var(--ink);background:var(--soft);border-radius:10px;padding:9px 13px;margin:8px 0 12px}
.how b{color:var(--accent)}
h3.ct{font-size:20px;line-height:1.35}
h3.ct small{display:block;font-size:13px;font-weight:600;color:var(--accent);letter-spacing:.04em;margin-bottom:3px}
/* v2-bling */""")

# ---- 제목/설명 ----
rep('<h3>2) 연간 AI 보안 사고 분포</h3><p class="note">오른쪽 꼬리가 긴 분포입니다. 소수 기업에 사고가 몰립니다.</p>',
    '<h3 class="ct"><small>그래프 2 · 사고 건수 분포</small>대부분은 1~3건, 소수 기업에 사고가 몰린다</h3><div class="how"><b>읽는 법</b> 막대가 높을수록 그 건수의 사고를 겪은 기업이 많습니다.</div>')
rep('<h3>3) AI 도입 구간별 평균 사고</h3><p class="note">구간이 오를 때마다 사고가 계단식으로 늘어납니다.</p>',
    '<h3 class="ct"><small>그래프 3 · AI 도입 수준별 사고</small>AI를 많이 쓸수록 사고가 계단처럼 늘어난다</h3><div class="how"><b>읽는 법</b> 기업을 AI 도입 수준 5단계로 나눈 뒤, 단계별 연간 평균 사고 건수를 막대로 그렸습니다.</div>')
s, n = re.subn(r'<h3>4\) AI 도입 지수 × 사고 건수 \(600개사\)</h3>\s*<p class="note">.*?</p>\s*<div class="legend" id="lgScatter"></div>',
    '<h3 class="ct"><small>그래프 4 · 기업 600곳 전체 보기</small>오른쪽(AI를 많이 쓰는 기업)으로 갈수록 점들이 위로 올라간다</h3>'
    '<div class="how"><b>읽는 법</b> 회색 점 하나가 기업 하나입니다. 오른쪽일수록 AI를 많이 쓰고, 위쪽일수록 사고가 많습니다. 주황색 선은 구간별 평균입니다. AI 도입 지수가 0.1 오르면 사고가 약 <b id="slopeTxt"></b>건 늘어납니다.</div>'
    '<div class="ck" id="lgScatter"></div>', s, flags=re.S)
assert n == 1
rep('<h3>5) 상관행렬</h3><p class="note">보안 성숙도는 사고를 줄이는 쪽(음의 상관)이고, 섀도 AI는 늘리는 쪽입니다.</p>',
    '<h3 class="ct"><small>그래프 5 · 사고와 함께 움직이는 요인</small>AI 도입 수준이 사고와 가장 강하게 함께 움직인다</h3><div class="how"><b>읽는 법</b> 막대가 오른쪽(주황)이면 그 값이 클수록 사고가 많고, 왼쪽(파랑)이면 사고가 적습니다. 막대가 길수록 관계가 강합니다.</div>')
rep('<h3>6) 업종별 비교</h3>', '<h3 class="ct"><small>표 6 · 업종별 비교</small>살 가능성이 높은 기업은 IT·SaaS와 금융에 가장 많다</h3>')
rep('<h3>7) 세그먼트 지도: 업종 × 규모별 고의향 기업 수</h3><p class="note">색이 진할수록 먼저 공략할 시장입니다. 칸 안의 숫자는 고의향 기업 수 / 전체 기업 수입니다.</p>',
    '<h3 class="ct"><small>그래프 7 · 업종 × 규모 지도</small>가장 진한 칸부터 공략한다: IT·SaaS 중소·중견, 금융 중소</h3><div class="how"><b>읽는 법</b> 칸의 큰 숫자는 살 가능성이 높은 기업 수입니다. 색이 진할수록 그 수가 많습니다. 작은 글씨는 그 칸의 전체 기업 수입니다.</div>')
rep('<h3>8) AI 도입 × 보안 성숙도 4분면</h3><p class="note">중앙값 기준으로 나눴습니다. 큰 숫자는 연간 평균 사고 건수입니다.</p>',
    '<h3 class="ct"><small>그래프 8 · 네 그룹 비교</small>보안이 탄탄해도 AI를 많이 쓰면 사고가 많다</h3><div class="how"><b>읽는 법</b> 기업을 AI 도입(높음/낮음)과 보안 성숙도(높음/낮음)로 네 그룹으로 나눴습니다. 큰 숫자는 그룹의 연간 평균 사고 건수입니다.</div>')
rep('<h3>9) 섀도 AI 사분위별 평균 사고</h3><p class="note">보안팀이 모르는 AI 사용이 많을수록 사고가 늘어납니다.</p>',
    '<h3 class="ct"><small>그래프 9 · 섀도 AI와 사고</small>몰래 쓰는 AI가 많을수록 사고가 늘어난다</h3><div class="how"><b>읽는 법</b> 섀도 AI 비율 순으로 기업을 네 묶음으로 나눈 평균 사고 건수입니다.</div>')
rep('<h3 style="margin-top:14px">10) LLM 앱 수 구간별 평균 사고</h3>',
    '<h3 class="ct" style="margin-top:22px"><small>그래프 10 · AI 앱 수와 사고</small>AI 앱이 많을수록 사고가 늘어난다</h3><div class="how"><b>읽는 법</b> 사내 LLM 앱 개수별 평균 사고 건수입니다.</div>')
rep('<h3>11) 기업 규모별 비교</h3>', '<h3 class="ct"><small>표 11 · 규모별 비교</small>중소기업은 수가 많고, 대기업은 예산이 크다</h3>')
rep('<h3>12) 예산 집중도</h3>', '<h3 class="ct"><small>그래프 12 · 예산 집중도</small>예산은 소수의 큰 고객에 몰려 있다</h3>')
rep('<h3>13) 우선 공략 계정 Top 10</h3>', '<h3 class="ct"><small>표 13 · 우선 공략 계정</small>먼저 찾아갈 기업 10곳</h3>')
rep('<h3 style="margin-top:28px">1) 데이터 개요와 기술 통계</h3>', '<h3 class="ct" style="margin-top:28px"><small>표 1 · 데이터 개요</small>분석에 쓴 7개 숫자 항목의 요약</h3>')

# ---- render() 교체 ----
a = s.index("function render() {"); b = s.index("function renderDeep() {")
NEW = r"""function render() {
  ["cHist", "cBand", "cScatter", "cCorr", "cSeg", "lgScatter"].forEach(i => document.getElementById(i).innerHTML = "");
  const A = css("--accent"), C = css("--cyan"), M = css("--muted"), I = css("--ink"), SF = css("--surface");
  const T = (s, x, y, txt, cls = "ax", anchor = "middle") => { const t = el("text", { x, y, "text-anchor": anchor, class: cls }, s); t.textContent = txt; return t; };
  const hov = (node, html) => { node.addEventListener("mousemove", e => showTip(e, html)); node.addEventListener("mouseleave", hideTip); };

  // 표 1: 기술 통계
  let h = "<tr><th>항목</th><th>평균</th><th>중앙값</th><th>표준편차</th><th>최소</th><th>최대</th></tr>";
  for (const c of D.cols) { const s = D.summary[c]; h += `<tr><td>${LBL[c]}</td><td><b>${s.mean}</b></td><td>${s.median}</td><td>${s.std}</td><td>${s.min}</td><td>${s.max}</td></tr>`; }
  document.getElementById("tSummary").innerHTML = h;

  // 그래프 2: 사고 건수 분포 (막대 + 값 라벨 + 평균선)
  { const W = 520, Hh = 320, x0 = 20, base = 250, top = 40, s = svg("cHist", W, Hh), n = D.hist_inc.length, bw = (W - 40) / n, mx = Math.max(...D.hist_inc);
    el("line", { x1: x0, y1: base, x2: W - 20, y2: base, class: "grid" }, s);
    D.hist_inc.forEach((v, i) => { const hh = v / mx * (base - top), x = x0 + i * bw;
      const r = el("rect", { x: x + 3, y: base - hh, width: bw - 6, height: Math.max(hh, 1), fill: A, rx: 4, "fill-opacity": i >= 1 && i <= 3 ? 1 : .45 }, s);
      hov(r, `사고 <b>${i}${i == 12 ? "건 이상" : "건"}</b>: ${v}개사 (${(v / D.n * 100).toFixed(0)}%)`);
      if (v) T(s, x + bw / 2, base - hh - 7, v, "v");
      T(s, x + bw / 2, base + 20, i == 12 ? "12+" : i); });
    const mean = D.summary.ai_incidents_12m.mean, mxp = x0 + (mean + .5) * bw;
    el("line", { x1: mxp, y1: top - 14, x2: mxp, y2: base, stroke: I, "stroke-width": 2, "stroke-dasharray": "5 4" }, s);
    T(s, mxp + 8, top - 6, `평균 ${mean}건`, "v", "start");
    T(s, W / 2, base + 46, "연간 AI 보안 사고 건수 (막대 위 숫자 = 기업 수)", "ttl");
    const share = D.hist_inc.slice(1, 4).reduce((a, b) => a + b, 0) / D.n * 100;
    T(s, W - 20, top + 30, `1~3건이 전체의 ${share.toFixed(0)}%`, "ttl", "end"); }

  // 그래프 3: AI 도입 수준별 평균 사고 (막대)
  { const W = 520, Hh = 320, base = 236, top = 48, s = svg("cBand", W, Hh), n = D.by_ai.length, bw = (W - 40) / n, mx = Math.max(...D.by_ai.map(b => b.incidents));
    const names = ["매우 낮음", "낮음", "보통", "높음", "매우 높음"];
    el("line", { x1: 20, y1: base, x2: W - 20, y2: base, class: "grid" }, s);
    D.by_ai.forEach((b, i) => { const hh = b.incidents / mx * (base - top), x = 20 + i * bw;
      const r = el("rect", { x: x + 12, y: base - hh, width: bw - 24, height: Math.max(hh, 2), fill: A, rx: 5, "fill-opacity": .3 + .7 * (i / (n - 1)) }, s);
      hov(r, `AI 도입 ${names[i]} (${b.band})<br>평균 사고 <b>${b.incidents}건</b> · ${b.n}개사`);
      const t = T(s, x + bw / 2, base - hh - 9, b.incidents + "건", "v"); t.style.fontSize = "17px";
      T(s, x + bw / 2, base + 22, names[i], "v"); T(s, x + bw / 2, base + 40, `지수 ${b.band}`); T(s, x + bw / 2, base + 57, `${b.n}개사`); });
    const ratio = Math.round(D.by_ai[n - 1].incidents / D.by_ai[0].incidents);
    T(s, 24, 26, `가장 낮은 단계 → 가장 높은 단계: 약 ${ratio}배`, "v", "start"); }

  // 그래프 4: 산점도 (회색 점 + 구간 평균선)
  { const W = 1000, Hh = 440, L = 70, R = 30, top = 24, base = 370, s = svg("cScatter", W, Hh), mxY = Math.max(...D.scatter.map(p => p[1]));
    const X = v => L + v * (W - L - R), Y = v => base - v / mxY * (base - top);
    for (let g = 0; g <= mxY; g += 4) { el("line", { x1: L, y1: Y(g), x2: W - R, y2: Y(g), class: "grid" }, s); T(s, L - 10, Y(g) + 4, g + "건", "ax", "end"); }
    for (let g = 0; g <= 5; g++) T(s, X(g / 5), base + 22, (g / 5).toFixed(1));
    T(s, X(.5), base + 48, "AI 도입 지수  (왼쪽: 거의 안 씀  →  오른쪽: 많이 씀)", "ttl");
    const yt = T(s, 18, (top + base) / 2, "연간 사고 건수", "ttl"); yt.setAttribute("transform", `rotate(-90 18 ${(top + base) / 2})`);
    D.scatter.forEach((p, i) => { const c = el("circle", { cx: X(p[0]), cy: Y(p[1]) + ((i * 7919) % 11 - 5), r: 4, fill: M, "fill-opacity": .28 }, s);
      hov(c, `<b>${p[2]}</b> 기업<br>AI 도입 ${p[0]} · 사고 ${p[1]}건 · 보안 성숙도 ${p[3]}`); });
    const pts = D.by_ai.map((b, i) => [X(.1 + i * .2), Y(b.incidents), b]);
    el("polyline", { points: pts.map(p => p[0] + "," + p[1]).join(" "), fill: "none", stroke: A, "stroke-width": 4, "stroke-linejoin": "round", "stroke-linecap": "round" }, s);
    pts.forEach(p => { el("circle", { cx: p[0], cy: p[1], r: 9, fill: A, stroke: SF, "stroke-width": 3 }, s);
      const bg = el("rect", { x: p[0] - 34, y: p[1] - 44, width: 68, height: 26, rx: 13, fill: SF, stroke: A, "stroke-width": 1.5 }, s);
      const t = T(s, p[0], p[1] - 26, p[2].incidents + "건", "v"); hov(bg, `구간 ${p[2].band} 평균 <b>${p[2].incidents}건</b> (${p[2].n}개사)`); });
    document.getElementById("lgScatter").innerHTML = `<span><i style="background:${M};opacity:.5"></i>기업 1곳</span><span><i class="ln" style="background:${A}"></i>구간별 평균 사고 건수</span>`;
    document.getElementById("slopeTxt").textContent = (D.slope[0] / 10).toFixed(2); }

  // 그래프 5: 사고와의 관계 (순위 막대)
  { const k = D.cols.indexOf("ai_incidents_12m");
    const rows = D.cols.map((c, i) => ({ c, v: D.corr[k][i] })).filter(r => r.c != "ai_incidents_12m").sort((a, b) => b.v - a.v);
    const W = 520, rh = 44, top = 34, s = svg("cCorr", W, top + rows.length * rh + 34), zero = 290, unit = 190;
    const word = v => Math.abs(v) >= .5 ? "강함" : Math.abs(v) >= .3 ? "보통" : Math.abs(v) >= .1 ? "약함" : "거의 없음";
    T(s, zero + 6, 18, "사고가 많아짐 →", "ttl", "start"); T(s, zero - 6, 18, "← 사고가 적어짐", "ttl", "end");
    el("line", { x1: zero, y1: top - 6, x2: zero, y2: top + rows.length * rh, stroke: M, "stroke-width": 1.5 }, s);
    rows.forEach((r, i) => { const y = top + i * rh, w = Math.max(Math.abs(r.v) * unit, 2), pos = r.v >= 0;
      T(s, 150, y + 26, LBL[r.c], "v", "end");
      const b = el("rect", { x: pos ? zero + 1 : zero - 1 - w, y: y + 8, width: w, height: 26, rx: 5, fill: pos ? A : C }, s);
      hov(b, `${LBL[r.c]}와 사고 건수의 상관계수 <b>${r.v.toFixed(2)}</b> (${word(r.v)})`);
      T(s, pos ? zero + w + 8 : zero - w - 8, y + 26, `${r.v > 0 ? "+" : ""}${r.v.toFixed(2)} · ${word(r.v)}`, "v", pos ? "start" : "end"); });
    T(s, W / 2, top + rows.length * rh + 22, "숫자 = 상관계수 (−1 ~ +1, 0에 가까우면 관계 없음)", "ttl"); }

  // 표 6: 업종
  { const mxH = Math.max(...D.by_ind.map(r => r.hot));
    let h = "<tr><th>업종</th><th>기업 수</th><th>AI 도입</th><th>평균 사고</th><th>보안 성숙도</th><th>살 가능성 높은 기업</th></tr>";
    [...D.by_ind].sort((a, b) => b.hot - a.hot).forEach(r => h += `<tr><td><b>${r.industry}</b></td><td>${r.n}</td><td>${r.ai}</td><td>${r.incidents}건</td><td>${r.maturity}</td><td><div style="display:flex;align-items:center;gap:8px;justify-content:flex-end"><div class="bar" style="width:90px"><i style="width:${r.hot / mxH * 100}%"></i></div><b style="min-width:42px">${r.hot}곳</b></div></td></tr>`);
    document.getElementById("tInd").innerHTML = h; }

  // 그래프 7: 업종 × 규모 지도
  { const inds = [...D.by_ind].sort((a, b) => b.hot - a.hot).map(r => r.industry), sizes = [...new Set(D.seg.map(s => s.size))];
    const cw = 200, ch = 62, L = 110, s = svg("cSeg", L + sizes.length * cw, 44 + inds.length * ch), mx = Math.max(...D.seg.map(x => x.hot));
    sizes.forEach((z, j) => T(s, L + j * cw + cw / 2, 24, z, "v"));
    inds.forEach((ind, i) => { T(s, L - 14, 40 + i * ch + ch / 2 + 3, ind, "v", "end");
      sizes.forEach((z, j) => { const c = D.seg.find(x => x.industry == ind && x.size == z); if (!c) return;
        const f = c.hot / mx, r = el("rect", { x: L + j * cw, y: 36 + i * ch, width: cw - 6, height: ch - 6, fill: A, "fill-opacity": .1 + f * .9, rx: 8 }, s);
        hov(r, `<b>${ind} · ${z}</b><br>살 가능성 높은 기업 ${c.hot}곳 / 전체 ${c.n}곳 (${Math.round(c.hot / c.n * 100)}%)<br>평균 보안 예산 ${Math.round(c.budget).toLocaleString()}백만원`);
        const dark = f > .5, t = T(s, L + j * cw + cw / 2 - 3, 36 + i * ch + 30, c.hot + "곳", "v"); t.style.fontSize = "19px"; t.style.fill = dark ? "#1a1206" : I; t.style.pointerEvents = "none";
        const t2 = T(s, L + j * cw + cw / 2 - 3, 36 + i * ch + 48, `전체 ${c.n}곳 중`, "ax"); t2.style.fill = dark ? "#1a1206" : M; t2.style.pointerEvents = "none"; }); }); }
}
"""
s = s[:a] + NEW + s[b:]

# ---- renderDeep 의 가로 막대 가독성 ----
old_hbar = s[s.index("  const hbar = (id, rows) => {"):s.index('  hbar("cShadow", d.shadow_q);')]
new_hbar = r"""  const hbar = (id, rows, unit) => { const mx = Math.max(...rows.map(r => r.incidents)), rh = 46, s = svg(id, 520, rows.length * rh + 8);
    rows.forEach((r, i) => { const w = r.incidents / mx * 250, y = i * rh;
      const a = el("text", { x: 118, y: y + 28, "text-anchor": "end", class: "v" }, s); a.textContent = r.band + (unit || "");
      const b = el("rect", { x: 130, y: y + 9, width: w, height: 28, rx: 6, fill: A, "fill-opacity": .3 + .7 * (i / (rows.length - 1)) }, s);
      b.addEventListener("mousemove", e => showTip(e, `${r.band}${unit || ""}: 평균 <b>${r.incidents}건</b> · ${r.n}개사`)); b.addEventListener("mouseleave", hideTip);
      const v = el("text", { x: 140 + w, y: y + 29, class: "v" }, s); v.textContent = r.incidents + "건"; v.style.fontSize = "16px";
      const n = el("text", { x: 512, y: y + 28, "text-anchor": "end", class: "ax" }, s); n.textContent = r.n + "개사"; }); };
"""
s = s.replace(old_hbar, new_hbar)
rep('hbar("cShadow", d.shadow_q); hbar("cApps", d.by_apps);', 'hbar("cShadow", d.shadow_q); hbar("cApps", d.by_apps, "개");')
# 4분면: 축 라벨이 보이는 표 형태
old_q = s[s.index('  document.getElementById("cQuad").innerHTML'):s.index("  const hbar = (id, rows, unit)")]
new_q = r"""  document.getElementById("cQuad").innerHTML = d.quad.map(q => `<div class="q ${q.incidents == mxI ? "hot" : ""}"><div style="font-weight:700">${q.ai}<br>보안 ${q.mat}</div><div class="big ${q.incidents == mxI ? "gt" : ""}">${q.incidents}건</div><div class="bar" style="margin:6px 0 8px"><i style="width:${q.incidents / mxI * 100}%"></i></div><div class="note">${q.n}개사 · 살 가능성 높은 기업 ${q.hot}곳</div></div>`).join("");
"""
s = s.replace(old_q, new_q)
open(p, "w", encoding="utf-8").write(s)
print("patched v3", len(s))
