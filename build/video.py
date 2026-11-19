# 클라우드플레어 AI 보안 전략 60초 영상: 키네틱 타이포그래피 + 라인 아트 + 내레이션
import os, sys, json, math, wave, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FPS, W, H = 30, 1920, 1080
OW, OH = 1280, 720
TOTAL = 60.0
BG = (10, 12, 20)
FG = (240, 238, 232)
ORANGE = (246, 130, 31)   # 클라우드플레어 오렌지 계열
AMBER = (251, 173, 65)
CYAN = (90, 200, 230)
RED = (235, 80, 70)
DIM = (70, 78, 96)
FB = "C:/Windows/Fonts/malgunbd.ttf"
FR = "C:/Windows/Fonts/malgun.ttf"
_fc = {}
def font(sz, bold=True):
    k = (int(sz), bold)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FB if bold else FR, max(8, int(sz)))
    return _fc[k]

eda = json.load(open(os.path.join(ROOT, "data", "eda.json"), encoding="utf-8"))
SUBS = [
    "AI 시대, 보안의 경계가 사라지고 있습니다.",
    "모든 기업이 AI를 쓰고, 공격자도 AI를 씁니다.",
    "프롬프트 인젝션, 데이터 유출, 섀도 AI. 위협은 이제 모델 안에서 시작됩니다.",
    "600개 기업 시뮬레이션 분석 결과, AI 도입 지수가 높은 기업은 사고가 30배 많았습니다.",
    "클라우드플레어는 AI 게이트웨이, AI 방화벽, 제로 트러스트로 세 겹의 방어선을 세웁니다.",
    "IT와 금융에서 먼저 이기고, 의료와 제조로 넓힙니다. 진단으로 시작해 플랫폼으로 확장합니다.",
    "AI를 믿고 쓰게 만드는 회사. 클라우드플레어.",
]

# ---------- 오디오 타임라인 ----------
segs = []
for i in range(7):
    w = wave.open(os.path.join(HERE, "audio", f"seg{i}.wav"))
    sr = w.getframerate()
    segs.append(np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768)
durs = [len(s) / sr for s in segs]
LEAD = 0.45
pad = (TOTAL - sum(durs) - LEAD * 7) / 7
scene_len = [d + LEAD + pad for d in durs]
starts = np.cumsum([0] + scene_len[:-1]).tolist()
mix = np.zeros(int(TOTAL * sr) + sr, dtype=np.float32)
for s, st in zip(segs, starts):
    a = int((st + LEAD) * sr); mix[a:a + len(s)] += s * 0.95
t = np.arange(len(mix)) / sr
pad_snd = (0.035 * np.sin(2 * np.pi * 55 * t) + 0.02 * np.sin(2 * np.pi * 82.5 * t) + 0.012 * np.sin(2 * np.pi * 110 * t + 0.5 * np.sin(2 * np.pi * 0.1 * t)))
env = np.clip(t / 2.0, 0, 1) * np.clip((TOTAL - t) / 2.5, 0, 1)
mix = mix + pad_snd * env
mix = mix[:int(TOTAL * sr)]
mix = np.clip(mix, -1, 1)
apath = os.path.join(HERE, "audio", "narration_full.wav")
with wave.open(apath, "wb") as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(sr)
    wv.writeframes((mix * 32767).astype(np.int16).tobytes())

# ---------- 헬퍼 ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def lerp(c1, c2, a): a = clamp(a); return tuple(int(c1[i] + (c2[i] - c1[i]) * a) for i in range(3))
def prog(t, a, b): return clamp((t - a) / (b - a)) if b > a else 1.0

def poly(d, pts, frac, col, w=4, closed=False):
    if closed: pts = pts + [pts[0]]
    L = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    tot = sum(L); rem = tot * clamp(frac)
    for i, l in enumerate(L):
        if rem <= 0: break
        p0, p1 = pts[i], pts[i + 1]
        f = min(1, rem / l) if l else 1
        d.line([p0, (p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f)], fill=col, width=w)
        rem -= l

def circle_pts(cx, cy, r, a0=0, a1=360, n=90):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

def ktext(d, txt, x, y, sz, t, t0, col=FG, anchor="lm", dy=60, dur=0.55, bold=True, out=None):
    """단어가 아래에서 튀어 오르며 나타나고(out 시점부터) 위로 사라지는 키네틱 텍스트"""
    p = eo(prog(t, t0, t0 + dur))
    if p <= 0: return
    a = p; yy = y + (1 - p) * dy
    if out is not None:
        q = eio(prog(t, out, out + 0.4)); a *= (1 - q); yy -= q * dy * 0.6
    if a <= 0.01: return
    s = sz * (0.86 + 0.14 * p)
    d.text((x, yy), txt, font=font(s, bold), fill=lerp(BG, col, a), anchor=anchor)

def kword_stagger(d, words, x, y, sz, t, t0, gap=0.14, cols=None, out=None):
    fx = x
    for i, wd in enumerate(words):
        c = cols[i] if cols else FG
        ktext(d, wd, fx, y, sz, t, t0 + i * gap, col=c, out=out)
        fx += font(sz).getlength(wd + " ")

# ---------- 장면 ----------
def sc0(d, t, L):  # 경계가 사라진다
    cx, cy = 1340, 540
    sq = [(cx - 300, cy - 300), (cx + 300, cy - 300), (cx + 300, cy + 300), (cx - 300, cy + 300)]
    poly(d, sq, eo(prog(t, 0.1, 1.6)), CYAN, 5, closed=True)
    br = eio(prog(t, 2.6, 5.0))
    if br > 0:  # 경계가 점선으로 부서지며 흩어짐
        d.rectangle([0, 0, W, H], fill=None)
        for k in range(48):
            ang = k / 48 * 2 * math.pi
            r0 = 300 / max(abs(math.cos(ang)), abs(math.sin(ang)))
            r = r0 + br * (120 + 260 * ((k * 37) % 11) / 11)
            x, y = cx + r * math.cos(ang), cy + r * math.sin(ang)
            d.line([(x - 14, y), (x + 14, y)], fill=lerp(BG, CYAN, 1 - br * 0.7), width=4)
        d.rectangle([cx - 306, cy - 306, cx + 306, cy + 306], outline=BG, width=14)
    for i, (px, py) in enumerate([(cx - 120, cy - 60), (cx + 90, cy - 110), (cx + 30, cy + 90), (cx - 150, cy + 130), (cx + 160, cy + 60)]):
        p = eo(prog(t, 0.8 + i * 0.12, 1.4 + i * 0.12))
        if p > 0:
            ox = (px - cx) * br * 0.9; oy = (py - cy) * br * 0.9
            d.ellipse([px + ox - 12 * p, py + oy - 12 * p, px + ox + 12 * p, py + oy + 12 * p], outline=FG, width=4)
    ktext(d, "AI 시대,", 140, 380, 96, t, 0.3)
    ktext(d, "보안의 경계가", 140, 510, 96, t, 0.9)
    ktext(d, "사라진다", 140, 650, 128, t, 1.6, col=ORANGE)

def sc1(d, t, L):  # 모두가 AI를 쓴다, 공격자도
    nodes = [(1150, 300), (1450, 260), (1650, 450), (1350, 520), (1100, 640), (1500, 760), (1750, 700)]
    edges = [(0, 1), (1, 2), (0, 3), (1, 3), (3, 2), (3, 4), (3, 5), (5, 6), (2, 6), (4, 5)]
    for i, (a, b) in enumerate(edges):
        poly(d, [nodes[a], nodes[b]], eo(prog(t, 0.2 + i * 0.08, 0.8 + i * 0.08)), DIM, 3)
    for i, (x, y) in enumerate(nodes):
        p = eo(prog(t, 0.3 + i * 0.1, 0.8 + i * 0.1))
        if p > 0: d.ellipse([x - 22 * p, y - 22 * p, x + 22 * p, y + 22 * p], outline=CYAN, width=4)
    # 공격자 노드
    ax, ay = 1780, 230
    pa = eo(prog(t, 2.6, 3.2))
    if pa > 0:
        tri = [(ax, ay - 40 * pa), (ax + 36 * pa, ay + 26 * pa), (ax - 36 * pa, ay + 26 * pa)]
        poly(d, tri, 1, RED, 5, closed=True)
        for j, n in enumerate([1, 2, 6]):
            poly(d, [(ax, ay), nodes[n]], eo(prog(t, 3.1 + j * 0.25, 3.9 + j * 0.25)), RED, 3)
    ktext(d, "모든 기업이", 140, 400, 92, t, 0.3)
    ktext(d, "AI를 쓴다", 140, 520, 120, t, 0.8, col=CYAN)
    ktext(d, "공격자도.", 140, 680, 120, t, 2.7, col=RED)

def sc2(d, t, L):  # 위협은 모델 안에서
    layers = [[(1180, 330 + i * 140) for i in range(4)], [(1430, 260 + i * 140) for i in range(5)], [(1680, 400 + i * 140) for i in range(3)]]
    k = 0
    for la, lb in zip(layers[:-1], layers[1:]):
        for a in la:
            for b in lb:
                poly(d, [a, b], eo(prog(t, 0.2 + k * 0.012, 0.9 + k * 0.012)), DIM, 2); k += 1
    for li, la in enumerate(layers):
        for a in la:
            p = eo(prog(t, 0.4 + li * 0.25, 0.9 + li * 0.25))
            if p > 0: d.ellipse([a[0] - 18 * p, a[1] - 18 * p, a[0] + 18 * p, a[1] + 18 * p], outline=FG, width=4)
    crack = [(1300, 180), (1340, 300), (1300, 380), (1380, 470), (1340, 560), (1420, 660), (1390, 780), (1460, 900)]
    poly(d, crack, eo(prog(t, 4.6, 6.4)), ORANGE, 6)
    items = [("프롬프트 인젝션", ORANGE, 0.4), ("데이터 유출", AMBER, 1.6), ("섀도 AI", RED, 2.7)]
    for i, (w, c, t0) in enumerate(items):
        ktext(d, w, 140, 300 + i * 140, 100, t, t0, col=c)
    ktext(d, "위협은 모델 안에서 시작된다", 140, 780, 64, t, 4.3, col=FG)

def sc3(d, t, L):  # EDA: 30배
    data = eda["by_ai"]; vals = [b["incidents"] for b in data]
    ratio = vals[-1] / vals[0]
    x0, y0, cw, ch = 1000, 820, 780, 520
    poly(d, [(x0, y0 - ch - 20), (x0, y0), (x0 + cw + 20, y0)], eo(prog(t, 0.1, 0.9)), DIM, 3)
    pts = [(x0 + 60 + i * (cw - 80) / (len(vals) - 1), y0 - vals[i] / max(vals) * (ch - 40)) for i in range(len(vals))]
    p = eo(prog(t, 0.8, 3.6))
    poly(d, pts, p, ORANGE, 6)
    for i, (x, y) in enumerate(pts):
        if p >= i / (len(pts) - 1) - 1e-6:
            d.ellipse([x - 11, y - 11, x + 11, y + 11], outline=AMBER, width=4)
            d.text((x, y - 34), f"{vals[i]:.2f}", font=font(30), fill=FG, anchor="mm")
            d.text((x, y0 + 36), data[i]["band"], font=font(26, False), fill=DIM, anchor="mm")
    d.text((x0 + cw / 2, y0 + 86), "AI 도입 지수 구간 → 연간 AI 보안 사고(평균)", font=font(28, False), fill=lerp(BG, DIM, prog(t, 1, 1.6)), anchor="mm")
    n = ratio * eo(prog(t, 0.6, 3.4))
    ktext(d, "600개 기업 분석", 140, 300, 56, t, 0.2, col=CYAN)
    if t > 0.6:
        d.text((140, 470), f"{min(n, 30):.0f}×", font=font(250), fill=ORANGE, anchor="lm")
    ktext(d, "AI 도입 상위 기업의", 140, 650, 58, t, 2.2)
    ktext(d, "보안 사고 빈도", 140, 730, 58, t, 2.5)
    ktext(d, "시뮬레이션 데이터 · 5.02 ÷ 0.16 ≈ 31 · r = %.2f" % eda["r_ai_inc"], 140, 830, 30, t, 3.2, col=DIM, bold=False)

def sc4(d, t, L):  # 3겹 방어선
    cx, cy = 1400, 560
    labels = [("제로 트러스트", "Cloudflare One", CYAN, 380), ("AI 방화벽", "Firewall for AI", AMBER, 270), ("AI 게이트웨이", "AI Gateway", ORANGE, 160)]
    for i, (k, e, c, r) in enumerate(labels):
        t0 = 0.5 + i * 1.6
        poly(d, circle_pts(cx, cy, r, -90, 270, 120), eo(prog(t, t0, t0 + 1.3)), c, 6)
        p = eo(prog(t, t0 + 0.6, t0 + 1.2))
        if p > 0:
            d.line([(cx + r * 0.71, cy - r * 0.71), (cx + r * 0.71 + 60, cy - r * 0.71 - 60)], fill=lerp(BG, c, p), width=3)
    # 중앙 AI 코어
    pc = eo(prog(t, 0.2, 0.8))
    if pc > 0:
        d.ellipse([cx - 60 * pc, cy - 60 * pc, cx + 60 * pc, cy + 60 * pc], outline=FG, width=5)
        d.text((cx, cy), "AI", font=font(50 * pc + 1), fill=FG, anchor="mm")
    ktext(d, "세 겹의 방어선", 120, 230, 92, t, 0.2, col=FG)
    for i, (k, e, c, r) in enumerate(reversed(labels)):
        t0 = 0.5 + (2 - i) * 1.6 + 0.5
        ktext(d, f"0{i + 1}  {k}", 120, 420 + i * 150, 66, t, 0.9 + i * 1.6, col=c)
        ktext(d, e, 205, 480 + i * 150, 32, t, 1.1 + i * 1.6, col=DIM, bold=False)

def sc5(d, t, L):  # 시장 진입 경로
    seg = [("IT·SaaS", 230, ORANGE), ("금융", 400, ORANGE), ("의료", 570, AMBER), ("제조", 740, AMBER)]
    hot = {b["industry"]: b["hot"] for b in eda["by_ind"]}
    for i, (name, y, c) in enumerate(seg):
        t0 = 0.3 + i * 0.7
        bw = hot[name] / max(hot.values()) * 520
        p = eo(prog(t, t0, t0 + 0.9))
        ktext(d, name, 140, y, 60, t, t0, col=c)
        if p > 0:
            d.rectangle([420, y - 22, 420 + bw * p, y + 22], outline=c, width=4)
            d.text((440 + bw * p, y), f"구매의향 상위 {int(hot[name] * p)}개사", font=font(28, False), fill=FG, anchor="lm")
    # 경로 라인: 진단 -> 확장 -> 플랫폼
    steps = [("진단", 1180), ("확장", 1450), ("플랫폼", 1720)]
    for j in range(2):
        poly(d, [(steps[j][1] + 44, 520), (steps[j + 1][1] - 44, 520)], eo(prog(t, 4.0 + j * 0.9, 4.6 + j * 0.9)), CYAN, 5)
    for i, (n, x) in enumerate(steps):
        p = eo(prog(t, 3.6 + i * 0.9, 4.1 + i * 0.9))
        if p > 0:
            d.ellipse([x - 40 * p, 520 - 40 * p, x + 40 * p, 520 + 40 * p], outline=CYAN, width=5)
            d.text((x, 620), n, font=font(46 * p + 1), fill=lerp(BG, FG, p), anchor="mm")
    ktext(d, "Land & Expand", 1180, 380, 52, t, 3.4, col=DIM, bold=False)

def sc6(d, t, L):  # 클로징: 클라우드 라인 아트
    cx, cy = 960, 400
    cloud = circle_pts(cx - 150, cy + 30, 90, 90, 270, 40) + circle_pts(cx - 30, cy - 40, 130, 190, 340, 50) + circle_pts(cx + 140, cy + 20, 100, 260, 450, 50)
    cloud = cloud + [(cx - 150, cy + 120)]
    poly(d, cloud, eo(prog(t, 0.1, 1.8)), ORANGE, 7)
    # 방패
    sh = [(cx, cy - 20), (cx + 70, cy + 5), (cx + 60, cy + 80), (cx, cy + 115), (cx - 60, cy + 80), (cx - 70, cy + 5)]
    poly(d, sh, eo(prog(t, 1.2, 2.2)), FG, 5, closed=True)
    poly(d, [(cx - 28, cy + 50), (cx - 6, cy + 72), (cx + 32, cy + 28)], eo(prog(t, 2.0, 2.5)), FG, 6)
    ktext(d, "AI를 믿고 쓰게 만드는 회사", cx, 680, 64, t, 0.6, anchor="mm")
    ktext(d, "클라우드플레어", cx, 800, 120, t, 1.6, col=ORANGE, anchor="mm")

SCENES = [sc0, sc1, sc2, sc3, sc4, sc5, sc6]

def frame(T):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    si = max(i for i in range(7) if starts[i] <= T)
    t = T - starts[si]; L = scene_len[si]
    SCENES[si](d, t, L)
    # 장면 전환: 끝 0.35초 페이드
    fade = clamp((t - (L - 0.35)) / 0.35) if si < 6 else clamp((T - (TOTAL - 1.0)) / 1.0)
    # 진행 라인 + 자막
    d.line([(0, H - 6), (W * T / TOTAL, H - 6)], fill=ORANGE, width=6)
    sub = SUBS[si]
    sa = prog(t, LEAD, LEAD + 0.3) * (1 - prog(t, LEAD + durs[si] + 0.3, LEAD + durs[si] + 0.6))
    if sa > 0:
        d.text((W / 2, H - 70), sub, font=font(34, False), fill=lerp(BG, (200, 200, 205), sa), anchor="mm")
    d.text((W - 60, 60), "CLOUDFLARE · AI SECURITY", font=font(24), fill=DIM, anchor="rm")
    im = im.resize((OW, OH), Image.LANCZOS)
    if fade > 0:
        im = Image.blend(im, Image.new("RGB", (OW, OH), BG), fade)
    return im

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for i in range(7):
            frame(starts[i] + scene_len[i] * 0.75).save(os.path.join(HERE, f"still{i}.png"))
        print("starts", [round(s, 2) for s in starts]); sys.exit()
    out = os.path.join(ROOT, "cloudflare_ai_security_60s.mp4")
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    p = subprocess.Popen([ff, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}", "-r", str(FPS), "-i", "-",
                          "-i", apath, "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    n = int(TOTAL * FPS)
    for f in range(n):
        p.stdin.write(frame(f / FPS).tobytes())
        if f % 300 == 0: print("frame", f, flush=True)
    p.stdin.close(); p.wait()
    print("done", out)
