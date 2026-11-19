# 클라우드파이어 AI 보안 B2B 시장 탐색적 데이터 분석 (시뮬레이션 데이터, seed 고정)
import json, csv, os
import numpy as np

rng = np.random.default_rng(2026)
OUT = os.path.join(os.path.dirname(__file__), "..")
N = 600
industries = ["금융", "의료", "제조", "유통", "공공", "IT·SaaS"]
ind_reg = {"금융": 0.9, "의료": 0.85, "제조": 0.5, "유통": 0.4, "공공": 0.95, "IT·SaaS": 0.55}
ind_ai = {"금융": 0.62, "의료": 0.48, "제조": 0.45, "유통": 0.55, "공공": 0.35, "IT·SaaS": 0.78}
sizes = ["중소(<300명)", "중견(300~1,000명)", "대기업(1,000명+)"]

rows = []
for i in range(N):
    ind = rng.choice(industries)
    size_i = rng.choice(3, p=[0.45, 0.33, 0.22])
    emp = int([rng.integers(50, 300), rng.integers(300, 1000), rng.integers(1000, 20000)][size_i])
    ai = float(np.clip(rng.normal(ind_ai[ind] + 0.08 * size_i, 0.15), 0.02, 0.99))  # AI 도입 지수 0~1
    llm_apps = int(max(0, rng.poisson(1 + ai * 12 * (1 + size_i * 0.6))))
    shadow = float(np.clip(rng.normal(0.45 - 0.15 * ind_reg[ind] + 0.1 * ai, 0.12), 0, 1))  # 섀도 AI 비율
    maturity = float(np.clip(rng.normal(1.8 + 1.6 * ind_reg[ind] + 0.4 * size_i, 0.6), 1, 5))  # 보안 성숙도 1~5
    lam = 0.4 + 4.2 * ai * (1 + shadow) - 0.55 * (maturity - 1)
    incidents = int(rng.poisson(max(lam, 0.15)))
    budget = round(float(emp * rng.lognormal(np.log(0.9 + ind_reg[ind]), 0.35) / 10), 1)  # 연간 보안 예산(백만원)
    intent = float(1 / (1 + np.exp(-(-3.2 + 2.4 * ai + 0.45 * incidents + 1.5 * ind_reg[ind] - 0.25 * (maturity - 3)))))
    rows.append(dict(id=f"C{i:04d}", industry=str(ind), size=sizes[size_i], employees=emp,
                     ai_adoption=round(ai, 3), llm_apps=llm_apps, shadow_ai=round(shadow, 3),
                     sec_maturity=round(maturity, 2), ai_incidents_12m=incidents,
                     sec_budget_mkrw=budget, buy_intent=round(intent, 3)))

with open(os.path.join(OUT, "data", "ai_security_accounts.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

num_cols = ["ai_adoption", "llm_apps", "shadow_ai", "sec_maturity", "ai_incidents_12m", "sec_budget_mkrw", "buy_intent"]
M = np.array([[r[c] for c in num_cols] for r in rows], dtype=float)

def desc(v):
    return dict(mean=round(float(v.mean()), 2), median=round(float(np.median(v)), 2), std=round(float(v.std()), 2),
                min=round(float(v.min()), 2), max=round(float(v.max()), 2), missing=0)

summary = {c: desc(M[:, j]) for j, c in enumerate(num_cols)}
corr = np.corrcoef(M.T).round(2).tolist()

by_ind = []
for ind in industries:
    sub = [r for r in rows if r["industry"] == ind]
    by_ind.append(dict(industry=ind, n=len(sub),
                       ai=round(float(np.mean([r["ai_adoption"] for r in sub])), 2),
                       incidents=round(float(np.mean([r["ai_incidents_12m"] for r in sub])), 2),
                       maturity=round(float(np.mean([r["sec_maturity"] for r in sub])), 2),
                       intent=round(float(np.mean([r["buy_intent"] for r in sub])), 2),
                       hot=sum(1 for r in sub if r["buy_intent"] >= 0.6)))

# AI 도입 구간별 사고
bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
by_ai = []
for a, b in zip(bins[:-1], bins[1:]):
    sub = [r for r in rows if a <= r["ai_adoption"] < b]
    if sub:
        by_ai.append(dict(band=f"{a:.1f}~{b:.1f}", n=len(sub),
                          incidents=round(float(np.mean([r["ai_incidents_12m"] for r in sub])), 2)))

hist_inc = np.bincount(np.minimum(M[:, 4].astype(int), 12), minlength=13).tolist()
scatter = [[r["ai_adoption"], r["ai_incidents_12m"], r["industry"], round(r["sec_maturity"], 1)] for r in rows]

# 세그먼트: 고의향(>=0.6) 계정 수 x 평균 예산
seg = []
for ind in industries:
    for s in sizes:
        sub = [r for r in rows if r["industry"] == ind and r["size"] == s]
        if sub:
            hot = [r for r in sub if r["buy_intent"] >= 0.6]
            seg.append(dict(industry=ind, size=s, n=len(sub), hot=len(hot),
                            budget=round(float(np.mean([r["sec_budget_mkrw"] for r in sub])), 0)))

slope = np.polyfit(M[:, 0], M[:, 4], 1).round(2).tolist()
r_ai_inc = round(float(np.corrcoef(M[:, 0], M[:, 4])[0, 1]), 2)
r_mat_inc = round(float(np.corrcoef(M[:, 3], M[:, 4])[0, 1]), 2)
hot_total = int(sum(1 for r in rows if r["buy_intent"] >= 0.6))

# --- 심화 분석 ---
def mean(xs): return round(float(np.mean(xs)), 2) if len(xs) else 0
# (a) 섀도 AI 사분위별 사고
q = np.quantile(M[:, 2], [0.25, 0.5, 0.75])
shadow_q = []
for i, name in enumerate(["하위 25%", "25~50%", "50~75%", "상위 25%"]):
    lo = -1 if i == 0 else q[i - 1]; hi = 2 if i == 3 else q[i]
    sub = [r for r in rows if lo < r["shadow_ai"] <= hi]
    shadow_q.append(dict(band=name, n=len(sub), incidents=mean([r["ai_incidents_12m"] for r in sub]),
                         shadow=mean([r["shadow_ai"] for r in sub])))
# (b) AI 도입 x 보안 성숙도 4분면
ai_med, mat_med = float(np.median(M[:, 0])), float(np.median(M[:, 3]))
quad = []
for an, af in [("AI 도입 높음", lambda r: r["ai_adoption"] >= ai_med), ("AI 도입 낮음", lambda r: r["ai_adoption"] < ai_med)]:
    for mn, mf in [("성숙도 낮음", lambda r: r["sec_maturity"] < mat_med), ("성숙도 높음", lambda r: r["sec_maturity"] >= mat_med)]:
        sub = [r for r in rows if af(r) and mf(r)]
        quad.append(dict(ai=an, mat=mn, n=len(sub), incidents=mean([r["ai_incidents_12m"] for r in sub]),
                         intent=mean([r["buy_intent"] for r in sub]), hot=sum(1 for r in sub if r["buy_intent"] >= 0.6)))
# (c) 규모별
by_size = []
for s in sizes:
    sub = [r for r in rows if r["size"] == s]
    by_size.append(dict(size=s, n=len(sub), budget_median=round(float(np.median([r["sec_budget_mkrw"] for r in sub])), 0),
                        llm_apps=mean([r["llm_apps"] for r in sub]), incidents=mean([r["ai_incidents_12m"] for r in sub]),
                        intent=mean([r["buy_intent"] for r in sub]), hot=sum(1 for r in sub if r["buy_intent"] >= 0.6)))
# (d) LLM 앱 수 구간별 사고
app_bins = [(0, 4), (5, 9), (10, 14), (15, 24), (25, 999)]
by_apps = []
for a, b in app_bins:
    sub = [r for r in rows if a <= r["llm_apps"] <= b]
    if sub: by_apps.append(dict(band=(f"{a}~{b}" if b < 999 else f"{a}+"), n=len(sub), incidents=mean([r["ai_incidents_12m"] for r in sub])))
# (e) 우선 공략 계정 점수 = 구매 의향 x 보안 예산
for r in rows: r["priority"] = round(r["buy_intent"] * r["sec_budget_mkrw"], 0)
top = sorted(rows, key=lambda r: -r["priority"])[:10]
top = [dict(id=r["id"], industry=r["industry"], size=r["size"], employees=r["employees"], ai=r["ai_adoption"],
            incidents=r["ai_incidents_12m"], budget=r["sec_budget_mkrw"], intent=r["buy_intent"], priority=r["priority"]) for r in top]
# (f) 고의향 기업 보안 예산 합계와 파레토
hot_rows = sorted([r for r in rows if r["buy_intent"] >= 0.6], key=lambda r: -r["sec_budget_mkrw"])
hot_budget = round(float(sum(r["sec_budget_mkrw"] for r in hot_rows)), 0)
all_budget = round(float(sum(r["sec_budget_mkrw"] for r in rows)), 0)
top20 = hot_rows[:max(1, len(hot_rows) // 5)]
pareto = round(float(sum(r["sec_budget_mkrw"] for r in top20)) / hot_budget, 2)
# (g) 이상치(IQR) 계정 수
q1, q3 = np.quantile(M[:, 4], [0.25, 0.75]); thr = q3 + 1.5 * (q3 - q1)
outliers = int((M[:, 4] > thr).sum())
deep = dict(shadow_q=shadow_q, quad=quad, by_size=by_size, by_apps=by_apps, top=top, hot_budget=hot_budget,
            all_budget=all_budget, pareto=pareto, outlier_thr=round(float(thr), 1), outliers=outliers,
            ai_med=round(ai_med, 2), mat_med=round(mat_med, 2))
print(json.dumps(deep, ensure_ascii=True)[:0])

res = dict(deep=deep, n=N, cols=num_cols, summary=summary, corr=corr, by_ind=by_ind, by_ai=by_ai, hist_inc=hist_inc,
           scatter=scatter, seg=seg, slope=slope, r_ai_inc=r_ai_inc, r_mat_inc=r_mat_inc, hot_total=hot_total)
with open(os.path.join(OUT, "data", "eda.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False)
print(json.dumps(dict(r_ai_inc=r_ai_inc, r_mat_inc=r_mat_inc, slope=slope, hot=hot_total, by_ind=by_ind, by_ai=by_ai), ensure_ascii=False, indent=0))
