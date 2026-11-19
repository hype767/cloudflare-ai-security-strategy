# site_template.html 에 v2 내용 보충 + 블링 디자인을 적용한다 (한 번만 실행)
import os
H = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(H, "site_template.html")
s = open(p, encoding="utf-8").read()
assert "v2-bling" not in s, "already patched"

def ins_before(anchor, block):
    global s
    assert s.count(anchor) == 1, anchor
    s = s.replace(anchor, block + anchor)

def rep(a, b):
    global s
    assert s.count(a) == 1, a
    s = s.replace(a, b)

# ---------- 1. CSS ----------
CSS = r"""
/* v2-bling */
:root{--glow:rgba(232,106,16,.28);--grad:linear-gradient(100deg,#f6821f 0%,#fbad41 38%,#ff5f8f 72%,#8f7bff 100%)}
:root[data-theme="dark"]{--glow:rgba(246,130,31,.45)}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--glow:rgba(246,130,31,.45)}}
body{background:
  radial-gradient(900px 500px at 85% -10%,color-mix(in srgb,var(--accent) 22%,transparent),transparent 70%),
  radial-gradient(700px 480px at -10% 20%,color-mix(in srgb,#8f7bff 16%,transparent),transparent 70%),
  var(--bg);background-attachment:fixed}
.hero{position:relative;overflow:hidden}
.hero-art{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;opacity:.55;z-index:0}
.hero > *:not(.hero-art){position:relative;z-index:1}
.hero-art path,.hero-art circle{fill:none;stroke:var(--accent);stroke-width:1.4;stroke-dasharray:1400;stroke-dashoffset:1400;animation:draw 5s ease forwards}
.hero-art .c2{stroke:var(--cyan);animation-delay:.8s}
.hero-art .c3{stroke:#8f7bff;animation-delay:1.5s}
.hero-art .pulse{stroke-dasharray:none;stroke-dashoffset:0;animation:pulse 3.2s ease-in-out infinite;transform-origin:center;transform-box:fill-box}
@keyframes draw{to{stroke-dashoffset:0}}
@keyframes pulse{0%,100%{opacity:.25;transform:scale(.9)}50%{opacity:.9;transform:scale(1.15)}}
h1 em,.gt{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent;background-size:200% 100%;animation:shine 7s linear infinite}
@keyframes shine{to{background-position:200% 0}}
.eyebrow{display:inline-flex;align-items:center;gap:8px}
.eyebrow::before{content:"";width:22px;height:2px;background:var(--grad);border-radius:2px}
h2{position:relative}
.card{position:relative;background:color-mix(in srgb,var(--surface) 86%,transparent);backdrop-filter:blur(10px);transition:transform .25s ease,box-shadow .25s ease,border-color .25s ease}
.card:hover{transform:translateY(-4px);border-color:color-mix(in srgb,var(--accent) 60%,var(--line));box-shadow:0 14px 40px -12px var(--glow)}
.kpi{overflow:hidden}
.kpi::after{content:"";position:absolute;inset:-1px;border-radius:14px;padding:1px;background:var(--grad);background-size:200% 100%;animation:shine 6s linear infinite;-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none}
.kpi .n{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent;font-size:46px}
video{box-shadow:0 30px 80px -30px var(--glow),0 0 0 1px color-mix(in srgb,var(--accent) 35%,var(--line))}
.layer .num,.step::before{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.insight{border-left:0;position:relative;overflow:hidden;border-radius:12px;padding-left:20px}
.insight::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--grad)}
.tag{border-color:color-mix(in srgb,var(--accent) 45%,var(--line));color:var(--accent)}
.marquee{overflow:hidden;border-block:1px solid var(--line);padding:12px 0;margin-top:8px;mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent)}
.marquee div{display:inline-flex;gap:38px;white-space:nowrap;animation:mq 28s linear infinite;font-weight:700;letter-spacing:.08em;font-size:13px;color:var(--muted)}
.marquee b{color:var(--accent)}
@keyframes mq{to{transform:translateX(-50%)}}
.reveal{opacity:0;transform:translateY(22px);transition:opacity .7s ease,transform .7s ease}
.reveal.on{opacity:1;transform:none}
.btn{display:inline-block;padding:12px 22px;border-radius:99px;background:var(--grad);background-size:200% 100%;animation:shine 6s linear infinite;color:#14100a;font-weight:800;text-decoration:none;box-shadow:0 10px 30px -10px var(--glow)}
.btn.ghost{background:none;border:1px solid var(--line);color:var(--ink);box-shadow:none;animation:none}
.flow{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:14px 0}
.flow div{border:1px dashed color-mix(in srgb,var(--accent) 50%,var(--line));border-radius:12px;padding:12px;font-size:14px;position:relative}
.flow b{display:block;color:var(--accent);font-size:12px;letter-spacing:.08em}
.flow .blk{border-style:solid;background:var(--soft)}
.quad{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.quad .q{border:1px solid var(--line);border-radius:12px;padding:14px;position:relative;overflow:hidden}
.quad .q .big{font-size:30px;font-weight:800}
.quad .q.hot{border-color:var(--accent);box-shadow:inset 0 0 40px -18px var(--glow)}
.calc{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:22px;align-items:center}
.calc label{display:block;font-size:14px;color:var(--muted);margin:12px 0 4px}
.calc label b{color:var(--ink);float:right}
.calc input[type=range]{width:100%;accent-color:var(--accent)}
.calc .out{font-size:clamp(34px,5vw,54px);font-weight:800;line-height:1.1}
details{border:1px solid var(--line);border-radius:12px;padding:14px 18px;background:color-mix(in srgb,var(--surface) 86%,transparent);margin-bottom:10px}
details summary{cursor:pointer;font-weight:700}
details[open]{border-color:color-mix(in srgb,var(--accent) 55%,var(--line))}
dl{display:grid;grid-template-columns:minmax(120px,200px) 1fr;gap:8px 18px;margin:0}
dt{font-weight:700;color:var(--accent)} dd{margin:0;color:var(--muted)}
td.l,th.l{text-align:left;white-space:normal}
.bar{height:8px;border-radius:8px;background:var(--line);overflow:hidden;min-width:80px}
.bar i{display:block;height:100%;background:var(--grad)}
@media (max-width:600px){dl{grid-template-columns:1fr} .quad{grid-template-columns:1fr}}
@media (prefers-reduced-motion: reduce){*{animation:none!important;transition:none!important}.reveal{opacity:1;transform:none}.hero-art path,.hero-art circle{stroke-dashoffset:0}}
"""
ins_before("</style>", CSS)

# ---------- 2. 내비 ----------
rep('<a href="#why">왜 지금인가</a><a href="#eda">데이터 분석</a><a href="#strategy">B2B 전략</a><a href="#roadmap">90일 실행</a><a href="#review">5color 검토</a>',
    '<a href="#why">왜 지금인가</a><a href="#scenario">공격 시나리오</a><a href="#reg">규제</a><a href="#eda">데이터 분석</a><a href="#strategy">B2B 전략</a><a href="#buyer">구매자</a><a href="#roi">ROI 계산기</a><a href="#roadmap">실행 계획</a><a href="#risk">리스크</a><a href="#faq">FAQ</a><a href="#review">5color</a>')

# ---------- 3. 히어로 ----------
rep('<header class="wrap">', '''<header class="wrap hero">
  <svg class="hero-art" viewBox="0 0 1120 620" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
    <circle cx="900" cy="200" r="230"/><circle class="c2" cx="900" cy="200" r="160"/><circle class="c3" cx="900" cy="200" r="90"/>
    <path class="c2" d="M0 520 C200 440 320 580 520 500 S 860 420 1120 500"/>
    <path class="c3" d="M0 560 C240 500 360 620 600 540 S 900 480 1120 560"/>
    <path d="M740 200 L820 150 L900 200 L980 150 L1060 200 M820 150 L820 250 L900 300 L980 250 L980 150"/>
    <circle class="pulse" cx="900" cy="200" r="10"/><circle class="pulse" cx="820" cy="150" r="6"/><circle class="pulse" cx="980" cy="250" r="6"/>
  </svg>''')
rep('<video src="cloudflare_ai_security_60s.mp4"', '''<p style="margin:0 0 26px"><a class="btn" href="#strategy">전략 바로 보기</a> &nbsp; <a class="btn ghost" href="#eda">데이터 근거 보기</a></p>
  <video src="cloudflare_ai_security_60s.mp4"''')
rep('<section id="why">', '''<div class="marquee" aria-hidden="true"><div>
<span><b>01</b> PROMPT INJECTION</span><span><b>02</b> DATA LEAKAGE</span><span><b>03</b> SHADOW AI</span><span><b>04</b> AGENT OVER-PERMISSION</span><span><b>05</b> MODEL SUPPLY CHAIN</span><span><b>06</b> AI-POWERED PHISHING</span>
<span><b>01</b> PROMPT INJECTION</span><span><b>02</b> DATA LEAKAGE</span><span><b>03</b> SHADOW AI</span><span><b>04</b> AGENT OVER-PERMISSION</span><span><b>05</b> MODEL SUPPLY CHAIN</span><span><b>06</b> AI-POWERED PHISHING</span>
</div></div>
<section id="why">''')

# ---------- 4. 왜 지금인가 보충 + 시나리오 + 규제 ----------
ins_before('''  <div class="insight"><b>결론.</b> AI 보안 예산은''', '''  <div class="grid g2" style="margin-top:16px">
    <div class="card"><h3>⑤ 모델·플러그인 공급망</h3><p>오픈소스 모델, 벡터 DB, MCP 서버, 플러그인이 새 공급망이 됐습니다. 검증하지 않은 구성 요소 하나가 전체 AI 앱의 약점이 됩니다.</p></div>
    <div class="card"><h3>⑥ AI로 강화된 공격</h3><p>공격자는 AI로 피싱 문구를 현지화하고, 취약점 탐색과 봇 트래픽을 자동화합니다. 공격 비용은 내려가고 방어 쪽의 처리량 부담은 올라갑니다.</p></div>
  </div>
  <h3 style="margin-top:28px">기존 보안 vs AI 시대 보안</h3>
  <div class="card tscroll"><table>
    <tr><th>구분</th><th class="l">기존 보안</th><th class="l">AI 시대 보안</th></tr>
    <tr><td>지키는 대상</td><td class="l">서버, 단말, 네트워크 경계</td><td class="l">프롬프트, 응답, 모델, 에이전트의 행동</td></tr>
    <tr><td>공격 형태</td><td class="l">코드와 패킷 (정해진 형식)</td><td class="l">자연어 (형식이 없고 맥락에 따라 달라짐)</td></tr>
    <tr><td>데이터 유출 경로</td><td class="l">메일, USB, 파일 전송</td><td class="l">AI 입력창 붙여 넣기, 모델 응답, 에이전트의 도구 호출</td></tr>
    <tr><td>통제 지점</td><td class="l">방화벽, 엔드포인트</td><td class="l">사람·앱·에이전트와 AI 사이의 모든 요청 경로</td></tr>
    <tr><td>구매 주체</td><td class="l">보안팀</td><td class="l">보안팀 + AI 플랫폼 팀 + 컴플라이언스</td></tr>
  </table></div>
''')

ins_before('<section id="eda">', '''<section id="scenario"><div class="wrap">
  <div class="eyebrow">공격 시나리오</div>
  <h2>사고는 이렇게 일어나고, 여기서 끊는다</h2>
  <p class="lead">고객 미팅에서 그대로 쓸 수 있는 세 가지 시나리오입니다. 주황색 칸이 클라우드플레어가 끊는 지점입니다.</p>
  <div class="card"><h3>시나리오 A · 고객 상담 챗봇에 대한 간접 프롬프트 인젝션</h3>
    <div class="flow"><div><b>1 침투</b>공격자가 상품 리뷰에 숨은 지시문을 심습니다</div><div><b>2 실행</b>챗봇이 리뷰를 읽고 지시를 따릅니다</div><div><b>3 유출</b>다른 고객의 주문 정보를 응답에 넣습니다</div><div class="blk"><b>차단 · AI 방화벽</b>요청과 응답에서 인젝션 패턴과 개인정보를 탐지해 막습니다</div></div></div>
  <div class="card" style="margin-top:14px"><h3>시나리오 B · 직원의 소스코드 붙여 넣기</h3>
    <div class="flow"><div><b>1 사용</b>개발자가 승인되지 않은 AI 도구에 가입합니다</div><div><b>2 입력</b>사내 소스코드와 API 키를 붙여 넣습니다</div><div><b>3 잔류</b>데이터가 외부 서비스에 남습니다</div><div class="blk"><b>차단 · 제로 트러스트</b>섀도 AI를 찾아내고 DLP가 비밀 키와 코드 입력을 막습니다</div></div></div>
  <div class="card" style="margin-top:14px"><h3>시나리오 C · 사내 AI 앱의 비용 폭주와 무단 호출</h3>
    <div class="flow"><div><b>1 노출</b>테스트용 LLM API 키가 저장소에 올라갑니다</div><div><b>2 악용</b>외부에서 키로 대량 호출합니다</div><div><b>3 피해</b>요금이 치솟고 로그가 없어 원인을 못 찾습니다</div><div class="blk"><b>차단 · AI 게이트웨이</b>모든 호출을 한 지점으로 모아 속도 제한과 로깅을 겁니다</div></div></div>
</div></section>

<section id="reg"><div class="wrap">
  <div class="eyebrow">규제 지도</div>
  <h2>규제가 구매 시점을 정한다</h2>
  <p class="lead">AI 보안은 "사고가 나면 사는 제품"에서 "감사에 대비해 미리 사는 제품"으로 바뀌고 있습니다. 업종별로 영업 메시지를 맞출 규제 축입니다.</p>
  <div class="card tscroll"><table>
    <tr><th>업종</th><th class="l">주요 규제·기준</th><th class="l">고객이 증명해야 하는 것</th><th class="l">대응 상품</th></tr>
    <tr><td>전 업종</td><td class="l">AI 기본법, 개인정보 보호법, ISMS-P</td><td class="l">AI에 들어가는 개인정보의 통제와 처리 기록</td><td class="l">AI 게이트웨이 로그, DLP</td></tr>
    <tr><td>금융</td><td class="l">전자금융감독규정, 망분리 규제 개선에 따른 생성형 AI 활용 요건</td><td class="l">외부 AI 사용 시 데이터 통제와 접근 기록</td><td class="l">제로 트러스트, 감사 로그 보관</td></tr>
    <tr><td>의료</td><td class="l">의료법, 보건의료 데이터 활용 가이드라인</td><td class="l">환자 정보가 외부 모델로 나가지 않음</td><td class="l">DLP, AI 방화벽</td></tr>
    <tr><td>공공</td><td class="l">국가정보원 보안 지침, 클라우드 보안인증(CSAP)</td><td class="l">인증받은 환경과 국내 데이터 처리</td><td class="l">파트너 공동 제안 (2단계 시장)</td></tr>
    <tr><td>수출·글로벌</td><td class="l">EU AI Act, GDPR</td><td class="l">고위험 AI의 로깅과 사람의 감독</td><td class="l">AI 게이트웨이, 데이터 지역 설정</td></tr>
  </table></div>
  <p class="note">규제 항목은 영업 방향을 잡기 위한 요약입니다. 제안서에 넣기 전에 법무·컴플라이언스 팀이 조항과 시행 시점을 확인해야 합니다.</p>
</div></section>

''')

# ---------- 5. 심화 EDA ----------
ins_before('''  <div class="grid g3" style="margin-top:16px">
    <div class="insight"><b>발견 1.</b>''', '''  <h3 style="margin-top:34px">심화 분석</h3>
  <div class="grid g2">
    <div class="card"><h3>8) AI 도입 × 보안 성숙도 4분면</h3><p class="note">중앙값 기준으로 나눴습니다. 큰 숫자는 연간 평균 사고 건수입니다.</p><div class="quad" id="cQuad"></div></div>
    <div class="card"><h3>9) 섀도 AI 사분위별 평균 사고</h3><p class="note">보안팀이 모르는 AI 사용이 많을수록 사고가 늘어납니다.</p><div id="cShadow"></div>
      <h3 style="margin-top:14px">10) LLM 앱 수 구간별 평균 사고</h3><div id="cApps"></div></div>
  </div>
  <div class="grid g2" style="margin-top:16px">
    <div class="card"><h3>11) 기업 규모별 비교</h3><div class="tscroll"><table id="tSize"></table></div><p class="note">보안 예산은 중앙값(백만원/년)입니다.</p></div>
    <div class="card"><h3>12) 예산 집중도</h3><div id="cPareto"></div></div>
  </div>
  <div class="card" style="margin-top:16px"><h3>13) 우선 공략 계정 Top 10</h3><p class="note">우선순위 점수 = 구매 의향 × 연간 보안 예산. 실제 CRM을 넣으면 영업팀의 지명 계정 목록이 됩니다.</p><div class="tscroll"><table id="tTop"></table></div></div>
  <div class="grid g3" style="margin-top:16px" id="deepInsights"></div>
  <details style="margin-top:16px"><summary>분석 방법과 한계</summary>
    <p>① 데이터: 업종 6개, 규모 3개로 구성한 가상 기업 600곳입니다. 업종별 규제 강도와 AI 도입 수준을 가정하고 난수(seed 2026)로 만들었습니다.<br>② 변수: AI 도입 지수(0~1), LLM 앱 수, 섀도 AI 비율, 보안 성숙도(1~5), 연간 AI 보안 사고, 연간 보안 예산, 구매 의향(0~1).<br>③ 방법: 기술 통계, 분포, 구간별 평균, 피어슨 상관, 단순 회귀, 4분면 분할, IQR 이상치.<br>④ 한계: 변수 사이의 관계를 제가 가정해 넣었기 때문에 결과는 그 가정을 다시 보여 줄 뿐입니다. 시장의 실제 크기나 인과를 증명하지 않습니다. 실제 영업·고객 데이터로 같은 코드(build/eda.py)를 다시 돌려야 근거로 쓸 수 있습니다.</p></details>

''')

# ---------- 6. 전략 보충 ----------
ins_before('''</div></section>

<section id="roadmap">''', '''
  <h3 style="margin-top:30px">경쟁 구도와 차별점</h3>
  <div class="card tscroll"><table>
    <tr><th>경쟁 유형</th><th class="l">강점</th><th class="l">약점</th><th class="l">클라우드플레어의 대응</th></tr>
    <tr><td>AI 보안 전문 스타트업</td><td class="l">프롬프트 탐지 기술이 깊음</td><td class="l">별도 도입과 연동이 필요하고 지연이 늘어남</td><td class="l">이미 지나가는 트래픽에서 바로 켭니다. 추가 구간이 없습니다</td></tr>
    <tr><td>기존 보안 플랫폼(SASE·방화벽)</td><td class="l">보안팀과의 기존 관계</td><td class="l">개발자와 AI 앱 영역이 약함</td><td class="l">개발자가 쓰는 AI 게이트웨이로 아래에서부터 들어갑니다</td></tr>
    <tr><td>클라우드 사업자의 자체 가드레일</td><td class="l">자사 모델과 묶여 있어 쉬움</td><td class="l">해당 클라우드와 모델 안에서만 작동</td><td class="l">어떤 모델, 어떤 클라우드든 같은 정책을 겁니다</td></tr>
    <tr><td>직접 구축</td><td class="l">요구에 딱 맞춤</td><td class="l">유지 인력과 위협 업데이트 부담</td><td class="l">진단 리포트로 직접 구축의 빈틈을 숫자로 보여 줍니다</td></tr>
  </table></div>
  <div class="insight"><b>한 문장 차별점.</b> "모델도 클라우드도 가리지 않고, 이미 트래픽이 지나가는 자리에서, 사람·앱·에이전트를 한 정책으로 지킨다."</div>

  <h3 style="margin-top:30px">제품별 판매 메시지</h3>
  <div class="card tscroll"><table>
    <tr><th>상품</th><th class="l">고객의 문제</th><th class="l">첫 문장</th><th class="l">증명 방법</th></tr>
    <tr><td>AI 게이트웨이</td><td class="l">누가 어떤 모델을 얼마나 쓰는지 모름</td><td class="l">"AI 비용과 사용 내역을 한 화면에서 보십시오"</td><td class="l">2주 로그로 팀별 사용량과 비용 리포트</td></tr>
    <tr><td>AI 방화벽</td><td class="l">공개 챗봇이 공격받을까 출시를 미룸</td><td class="l">"보안 검토 때문에 출시를 늦추지 마십시오"</td><td class="l">모의 인젝션 테스트 차단 결과</td></tr>
    <tr><td>제로 트러스트</td><td class="l">직원의 AI 사용을 막을 수도 풀 수도 없음</td><td class="l">"금지 대신 안전하게 허용하십시오"</td><td class="l">섀도 AI 목록과 민감 데이터 입력 시도 건수</td></tr>
  </table></div>
</div></section>

<section id="buyer"><div class="wrap">
  <div class="eyebrow">구매자와 설득</div>
  <h2>네 명이 결정한다, 각자 다른 말을 들어야 한다</h2>
  <div class="grid g2" style="margin-top:18px">
    <div class="card"><span class="tag">결정권자</span><h3>CISO</h3><p><b>걱정:</b> AI 사고가 나면 책임은 내가 진다. 그런데 AI를 막으면 현업이 반발한다.<br><b>들어야 할 말:</b> "금지하지 않고도 통제할 수 있습니다. 감사 때 보여 줄 기록이 남습니다."</p></div>
    <div class="card"><span class="tag">사용자</span><h3>CTO · AI 플랫폼 팀</h3><p><b>걱정:</b> 보안 도구가 응답 속도를 늦추고 개발을 막는다.<br><b>들어야 할 말:</b> "코드 한 줄, 주소만 바꾸면 됩니다. 비용과 캐싱까지 같이 해결됩니다."</p></div>
    <div class="card"><span class="tag">검토자</span><h3>컴플라이언스 · 법무</h3><p><b>걱정:</b> 규제 기관이 물으면 증빙을 낼 수 있는가.<br><b>들어야 할 말:</b> "누가, 언제, 어떤 데이터를 AI에 넣었는지 기록으로 제출할 수 있습니다."</p></div>
    <div class="card"><span class="tag">예산 승인</span><h3>CFO · 구매</h3><p><b>걱정:</b> 보안 도구가 또 하나 늘어난다.<br><b>들어야 할 말:</b> "기존 계약에 추가하는 방식이라 공급사가 늘지 않습니다. AI 요금 절감분으로 일부를 상쇄합니다."</p></div>
  </div>
  <h3 style="margin-top:28px">자주 나오는 반대와 답</h3>
  <details><summary>"우리는 아직 AI를 본격적으로 안 씁니다."</summary><p>진단을 돌리면 대부분 보안팀이 모르는 AI 사용이 나옵니다. 답은 주장 대신 4주 무료 진단 리포트로 합니다.</p></details>
  <details><summary>"클라우드 사업자의 기본 가드레일로 충분합니다."</summary><p>그 가드레일은 그 클라우드의 모델에만 걸립니다. 직원이 브라우저에서 쓰는 외부 AI와 다른 모델에는 닿지 않습니다.</p></details>
  <details><summary>"응답이 느려지지 않습니까?"</summary><p>고객 트래픽이 이미 지나가는 네트워크에서 검사하므로 경로가 추가되지 않습니다. 도입 전후 지연 시간을 측정해 리포트에 넣습니다.</p></details>
  <details><summary>"프롬프트 내용을 클라우드플레어가 보는 것 아닙니까?"</summary><p>로그 저장 범위, 보관 기간, 마스킹을 고객이 정합니다. 금융·의료는 본문을 저장하지 않는 설정을 기본 제안합니다.</p></details>
  <details><summary>"예산이 없습니다."</summary><p>AI 도입 프로젝트 예산의 일부로 잡습니다. EDA에서도 구매 의향은 보안 예산보다 AI 도입 수준과 더 강하게 움직였습니다.</p></details>
</div></section>

<section id="roi"><div class="wrap">
  <div class="eyebrow">ROI 계산기</div>
  <h2>고객 앞에서 바로 돌려 보는 <span class="gt">투자 효과</span></h2>
  <p class="lead">슬라이더를 움직이면 바로 계산됩니다. 모든 값은 가정이며, 미팅에서 고객의 숫자로 바꿔 씁니다.</p>
  <div class="card calc">
    <div>
      <label>직원 수 <b id="vEmp"></b></label><input type="range" id="iEmp" min="100" max="20000" step="100" value="2000">
      <label>연간 AI 보안 사고 건수 <b id="vInc"></b></label><input type="range" id="iInc" min="0" max="15" step="1" value="4">
      <label>사고 1건당 비용 (백만원) <b id="vCost"></b></label><input type="range" id="iCost" min="10" max="1000" step="10" value="150">
      <label>도입 후 사고 감소율 <b id="vRed"></b></label><input type="range" id="iRed" min="10" max="90" step="5" value="50">
      <label>1인당 연간 요금 (만원) <b id="vFee"></b></label><input type="range" id="iFee" min="2" max="30" step="1" value="8">
    </div>
    <div>
      <div class="note">연간 순효과</div><div class="out gt" id="oNet"></div>
      <table style="margin-top:14px"><tr><td>사고 비용 절감</td><td id="oSave"></td></tr><tr><td>도입 비용</td><td id="oFee"></td></tr><tr><td>투자 대비 효과 (ROI)</td><td id="oRoi"></td></tr><tr><td>손익분기 사고 감소율</td><td id="oBe"></td></tr></table>
    </div>
  </div>
</div></section>
''')
# 위 블록은 strategy 섹션을 닫았으므로 roadmap 앞의 기존 닫는 태그를 제거한다
rep('''</div></section>

</div></section>

<section id="roadmap">''', '''</div></section>

<section id="roadmap">''') if '''</div></section>

</div></section>

<section id="roadmap">''' in s else None

# ---------- 7. 실행 계획 보충 + 리스크 ----------
rep('<div class="eyebrow">04 · 90일 실행 계획</div>', '<div class="eyebrow">04 · 실행 계획</div>')
ins_before('<section id="review">', '''<section id="plan12"><div class="wrap">
  <div class="eyebrow">12개월 로드맵과 조직</div>
  <h2>분기별로 무엇이 달라지는가</h2>
  <div class="steps">
    <div class="card step"><h3>1분기 · 증명</h3><p>진단 15건, 유료 전환 5건. IT·SaaS에서 첫 고객 사례를 만듭니다.</p></div>
    <div class="card step"><h3>2분기 · 반복</h3><p>진단을 파트너가 돌리게 합니다. 금융 전용 패키지와 규제 대응 자료를 냅니다.</p></div>
    <div class="card step"><h3>3분기 · 확장</h3><p>기존 고객에 두 번째 방어선을 붙입니다. 의료·유통으로 넓힙니다.</p></div>
    <div class="card step"><h3>4분기 · 플랫폼</h3><p>AI 보안 번들을 엔터프라이즈 갱신 계약의 기본 항목으로 넣습니다.</p></div>
  </div>
  <h3 style="margin-top:28px">필요한 조직과 역할</h3>
  <div class="card tscroll"><table>
    <tr><th>역할</th><th>인원(제안)</th><th class="l">하는 일</th></tr>
    <tr><td>AI 보안 전담 영업</td><td>2명</td><td class="l">지명 계정 50곳 담당, 진단 제안</td></tr>
    <tr><td>솔루션 엔지니어</td><td>2명</td><td class="l">진단 실행, 리포트 작성, 기술 검증</td></tr>
    <tr><td>파트너 매니저</td><td>1명</td><td class="l">MSP·SI 교육과 공동 영업</td></tr>
    <tr><td>제품 마케팅</td><td>1명</td><td class="l">업종별 자료, 고객 사례, 웨비나</td></tr>
    <tr><td>컴플라이언스 자문</td><td>겸직</td><td class="l">규제 조항 검토, 금융·의료 제안서 감수</td></tr>
  </table></div>
  <h3 style="margin-top:28px">영업 플레이북: 진단 4주 일정</h3>
  <div class="flow"><div><b>1주차</b>범위 합의, 로그 수집 설정 (차단 없이 관찰만)</div><div><b>2주차</b>AI 사용 현황 수집: 도구 목록, 사용자 수, 요청량</div><div><b>3주차</b>위험 분석: 민감 데이터 입력, 인젝션 시도, 미승인 도구</div><div class="blk"><b>4주차</b>경영진 보고: 위험 3가지와 막는 방법, 견적</div></div>
</div></section>

<section id="risk"><div class="wrap">
  <div class="eyebrow">리스크와 대응</div>
  <h2>이 전략이 틀릴 수 있는 지점</h2>
  <div class="card tscroll"><table>
    <tr><th>리스크</th><th>가능성</th><th>영향</th><th class="l">대응</th><th class="l">조기 신호</th></tr>
    <tr><td>무료 진단이 유료로 안 넘어감</td><td>중</td><td>높음</td><td class="l">진단 범위를 좁히고 4주차 보고에 견적을 반드시 포함</td><td class="l">전환율 20% 미만</td></tr>
    <tr><td>클라우드 사업자가 가드레일을 무료로 묶음</td><td>높음</td><td>중</td><td class="l">멀티 모델·멀티 클라우드 고객에 집중</td><td class="l">단일 클라우드 고객의 이탈</td></tr>
    <tr><td>오탐으로 현업 불만</td><td>중</td><td>높음</td><td class="l">관찰 모드로 시작해 단계적으로 차단 전환</td><td class="l">차단 예외 요청 급증</td></tr>
    <tr><td>규제 시행 지연으로 구매 지연</td><td>중</td><td>중</td><td class="l">규제 대신 비용 절감·가시성 메시지로 전환</td><td class="l">금융권 검토 기간 장기화</td></tr>
    <tr><td>영업 인력의 AI 지식 부족</td><td>높음</td><td>중</td><td class="l">시나리오 3종 데모와 반대 처리 문답을 표준 교육으로</td><td class="l">미팅 후 기술 문의 폭증</td></tr>
  </table></div>
</div></section>

''')

# ---------- 8. FAQ + 용어 ----------
ins_before('<footer>', '''<section id="faq"><div class="wrap">
  <div class="eyebrow">FAQ · 용어</div>
  <h2>처음 듣는 사람을 위한 정리</h2>
  <div class="grid g2" style="margin-top:16px">
    <div>
      <details open><summary>AI 보안과 기존 보안은 무엇이 다른가요?</summary><p>기존 보안은 정해진 형식의 공격을 막습니다. AI는 자연어로 지시를 받기 때문에 "말"이 공격이 됩니다. 그래서 프롬프트와 응답의 내용을 봐야 합니다.</p></details>
      <details><summary>왜 네트워크 회사가 AI 보안을 하나요?</summary><p>AI 요청은 결국 네트워크를 지나갑니다. 이미 고객 트래픽 앞단에 있는 회사는 새 장비 없이 그 요청을 볼 수 있습니다.</p></details>
      <details><summary>가장 먼저 무엇을 팔아야 하나요?</summary><p>상품이 아니라 4주 무료 진단입니다. 진단 리포트의 숫자가 첫 상품을 정합니다.</p></details>
      <details><summary>중소기업은 어떻게 하나요?</summary><p>고의향 기업 수는 가장 많지만 예산이 작습니다. 직판 대신 파트너와 셀프서비스 요금제로 대응합니다.</p></details>
    </div>
    <div class="card"><dl>
      <dt>프롬프트 인젝션</dt><dd>입력에 숨긴 지시로 AI가 원래 규칙을 어기게 만드는 공격</dd>
      <dt>섀도 AI</dt><dd>회사 승인 없이 직원이 쓰는 AI 도구</dd>
      <dt>DLP</dt><dd>민감 데이터가 밖으로 나가는 것을 찾아 막는 기술</dd>
      <dt>제로 트러스트</dt><dd>사내망이라도 믿지 않고 매 요청마다 검증하는 보안 방식</dd>
      <dt>AI 게이트웨이</dt><dd>모든 AI 모델 호출이 거쳐 가는 단일 관문</dd>
      <dt>AI 에이전트</dt><dd>사람 대신 도구를 써서 일을 수행하는 AI</dd>
      <dt>Land &amp; Expand</dt><dd>작은 계약으로 들어가 사용 범위를 넓히는 영업 방식</dd>
    </dl></div>
  </div>
</div></section>

''')

# ---------- 9. JS ----------
ins_before("render();\nmatchMedia", r"""
function renderDeep() {
  const d = D.deep, A = css("--accent"), I = css("--ink"), L = css("--line");
  ["cShadow", "cApps", "cPareto"].forEach(i => document.getElementById(i).innerHTML = "");
  // 4분면
  const mxI = Math.max(...d.quad.map(q => q.incidents));
  document.getElementById("cQuad").innerHTML = d.quad.map(q => `<div class="q ${q.incidents == mxI ? "hot" : ""}"><div class="note">${q.ai} · ${q.mat}</div><div class="big ${q.incidents == mxI ? "gt" : ""}">${q.incidents}건</div><div class="note">${q.n}개사 · 구매 의향 ${q.intent} · 고의향 ${q.hot}곳</div></div>`).join("");
  const hbar = (id, rows) => { const mx = Math.max(...rows.map(r => r.incidents)), s = svg(id, 460, rows.length * 34 + 6);
    rows.forEach((r, i) => { el("text", { x: 96, y: i * 34 + 22, "text-anchor": "end" }, s).textContent = r.band;
      el("rect", { x: 104, y: i * 34 + 8, width: r.incidents / mx * 290, height: 20, rx: 5, fill: A, "fill-opacity": .35 + .65 * r.incidents / mx }, s);
      el("text", { x: 110 + r.incidents / mx * 290, y: i * 34 + 22, style: `fill:${I};font-weight:700` }, s).textContent = `${r.incidents}건 (n=${r.n})`; }); };
  hbar("cShadow", d.shadow_q); hbar("cApps", d.by_apps);
  // 규모 표
  let h = "<tr><th>규모</th><th>기업 수</th><th>보안 예산</th><th>LLM 앱</th><th>사고</th><th>구매 의향</th><th>고의향</th></tr>";
  d.by_size.forEach(r => h += `<tr><td>${r.size}</td><td>${r.n}</td><td>${r.budget_median.toLocaleString()}</td><td>${r.llm_apps}</td><td>${r.incidents}</td><td>${r.intent}</td><td><b>${r.hot}</b></td></tr>`);
  document.getElementById("tSize").innerHTML = h;
  // 예산 집중도
  const share = Math.round(d.hot_budget / d.all_budget * 100), par = Math.round(d.pareto * 100);
  document.getElementById("cPareto").innerHTML = `<p>고의향 기업의 보안 예산 합계는 <b>${Math.round(d.hot_budget / 100).toLocaleString()}억 원</b>으로 전체(${Math.round(d.all_budget / 100).toLocaleString()}억 원)의 ${share}%입니다.</p><div class="bar"><i style="width:${share}%"></i></div>
    <p style="margin-top:16px">고의향 기업 중 예산 상위 20%가 그 예산의 <b>${par}%</b>를 갖고 있습니다.</p><div class="bar"><i style="width:${par}%"></i></div>
    <p class="note" style="margin-top:14px">사고 건수 이상치(IQR 기준 ${d.outlier_thr}건 초과)는 ${d.outliers}개사입니다. 이 기업들은 진단 제안의 1순위입니다.</p>`;
  // Top 10
  h = "<tr><th>계정</th><th>업종</th><th>규모</th><th>직원 수</th><th>AI 도입</th><th>사고</th><th>보안 예산</th><th>구매 의향</th><th>우선순위</th></tr>";
  const mxP = d.top[0].priority;
  d.top.forEach(r => h += `<tr><td>${r.id}</td><td>${r.industry}</td><td>${r.size}</td><td>${r.employees.toLocaleString()}</td><td>${r.ai}</td><td>${r.incidents}</td><td>${Math.round(r.budget).toLocaleString()}</td><td>${r.intent}</td><td><div class="bar"><i style="width:${r.priority / mxP * 100}%"></i></div></td></tr>`);
  document.getElementById("tTop").innerHTML = h;
  // 심화 발견
  const q = d.quad, sq = d.shadow_q, ap = d.by_apps;
  const cut = Math.round((1 - q[1].incidents / q[0].incidents) * 100);
  document.getElementById("deepInsights").innerHTML = [
    `<b>발견 4.</b> AI 도입이 높은 기업은 보안 성숙도가 높아도 사고가 ${q[1].incidents}건입니다. 성숙도가 낮은 쪽(${q[0].incidents}건)보다 ${cut}% 적을 뿐입니다. 기존 보안 투자만으로는 AI 위험이 남습니다.`,
    `<b>발견 5.</b> 섀도 AI 상위 25% 기업의 사고는 ${sq[3].incidents}건으로 하위 25%(${sq[0].incidents}건)의 ${(sq[3].incidents / sq[0].incidents).toFixed(1)}배입니다. "먼저 보이게 하라"가 첫 메시지입니다.`,
    `<b>발견 6.</b> LLM 앱이 ${ap[ap.length - 1].band}개인 기업은 사고가 ${ap[ap.length - 1].incidents}건으로 ${ap[0].band}개 기업(${ap[0].incidents}건)의 ${(ap[ap.length - 1].incidents / ap[0].incidents).toFixed(1)}배입니다. 앱이 늘수록 게이트웨이의 가치가 커집니다.`,
    `<b>발견 7.</b> 고의향 기업 예산의 ${par}%가 상위 20%에 있습니다. 상위 계정은 직판으로, 나머지는 파트너로 나누는 근거입니다.`
  ].map(t => `<div class="insight">${t}</div>`).join("");
}
function calc() {
  const g = id => +document.getElementById(id).value, fmt = v => (v >= 100 ? (v / 100).toFixed(1) + "억 원" : Math.round(v).toLocaleString() + "백만 원");
  const emp = g("iEmp"), inc = g("iInc"), cost = g("iCost"), red = g("iRed"), fee = g("iFee");
  const save = inc * cost * red / 100, spend = emp * fee / 100, net = save - spend;
  document.getElementById("vEmp").textContent = emp.toLocaleString() + "명"; document.getElementById("vInc").textContent = inc + "건";
  document.getElementById("vCost").textContent = cost.toLocaleString(); document.getElementById("vRed").textContent = red + "%"; document.getElementById("vFee").textContent = fee;
  document.getElementById("oNet").textContent = (net < 0 ? "−" : "+") + fmt(Math.abs(net));
  document.getElementById("oSave").textContent = fmt(save); document.getElementById("oFee").textContent = fmt(spend);
  document.getElementById("oRoi").textContent = spend ? Math.round(net / spend * 100) + "%" : "-";
  const be = inc * cost ? spend / (inc * cost) * 100 : Infinity;
  document.getElementById("oBe").textContent = be <= 100 ? be.toFixed(0) + "%" : "달성 불가 (사고 비용보다 도입 비용이 큼)";
}
document.querySelectorAll(".calc input").forEach(i => i.addEventListener("input", calc)); calc();
renderDeep(); matchMedia("(prefers-color-scheme: dark)").addEventListener("change", renderDeep);
document.querySelectorAll("section .card, section .insight, section h2, section .lead, details").forEach(e => e.classList.add("reveal"));
if ("IntersectionObserver" in window) { const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add("on"); io.unobserve(e.target); } }), { threshold: .08 });
  document.querySelectorAll(".reveal").forEach(e => io.observe(e)); setTimeout(() => document.querySelectorAll(".reveal").forEach(e => e.classList.add("on")), 2500);
} else document.querySelectorAll(".reveal").forEach(e => e.classList.add("on"));
""")

# 5color 보완 카드 갱신
rep('<p>① 실제 CRM 데이터로 EDA 재실행 ② 경쟁사 비교표 추가 ③ 업종별 규제 조항 매핑</p>',
    '<p>반영함: 경쟁 구도, 규제 지도, 구매자별 메시지, ROI 계산기, 리스크 표.<br>남은 일: ① 실제 CRM 데이터로 EDA 재실행 ② 규제 조항의 법무 검토 ③ 가격 확정</p>')
open(p, "w", encoding="utf-8").write(s)
print("patched", len(s))
