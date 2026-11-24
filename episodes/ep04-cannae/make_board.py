# EP04 (한국어 《격전의 세계사》) 칸나이 전투 (기원전 216) 스토리보드 생성기 — 첫 생성용(기록). 나레이션은 script.md 문장을 순서대로 그대로 가져온다.
# ⚠️ storyboard.json을 손으로 고친 뒤에는 다시 돌리지 말 것 (수정 사항이 덮어써짐)
# 연출 스타일 v2 + 롱폼 표준(막 단위 TTS·절제된 효과음·BGM -24dB·싱크 ±0.5초) + 초반 후킹 표준(hook {hud, neg, question} · troops)
# 막 번호: Act 1 = 콜드 오프닝(0~60초), Act 2~7 = 본편 → 장면 "act" 1~7 = act1.mp3~act7.mp3
# 전장: 지도 아이템 phalanx(카르타고 파랑 · 로마 빨강) — 카르타고 전열 bend 음수 = 불룩한 초승달 · bend 양수 = 밀려서 오목 · wrap = 아프리카 보병 양익 포위
# 래스터: 새 권역 westmed_sea(z6) · italy_sea(z8) · apulia_sea(z11) · cannae_zoom(z14) (pipeline/geo.py RASTERS)
# 전장 좌표는 모식 배치 — 아우피두스강(오판토강) 어느 기슭이었는지 학설이 갈림. 로마군은 북쪽에서 남쪽을 보고 섰고 오른쪽 끝(서쪽)이 강이라고 가정
# 캐릭터 무대(stage)는 쓰지 않음 — 고대 카르타고·로마 캐릭터 그림이 없어서(재연 일러스트로)
import collections
import json
import pathlib
import re

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent.parent
EP = HERE.name
raw = (HERE / "script.md").read_text(encoding="utf-8")
ACTS = []
for a in raw.split("\n## ")[1:]:
    body = [l for l in a.split("\n")[1:] if l and not l.startswith((">", "#"))]
    ACTS.append([s for l in body for s in re.split(r"(?<=[.?])\s+", l.strip()) if s])

# 자막 표기(숫자) ← 낭독 문장(단어) — 긴 것부터 (사용자 지시: 자막 숫자는 숫자로)
SUBS = [
    ("기원전 이백십육년 팔월 이일", "기원전 216년 8월 2일"), ("기원전 이백삼십칠년", "기원전 237년"), ("기원전 이백십구년", "기원전 219년"),
    ("기원전 이백십육년", "기원전 216년"), ("기원전 이백이년", "기원전 202년"), ("기원전 오십이년", "기원전 52년"),
    ("팔월 이일", "8월 2일"), ("팔월 일일", "8월 1일"), ("팔월 한여름", "8월 한여름"),
    ("약 팔만 육천 명", "약 8만 6천 명"), ("오만에서 칠만 명", "5만에서 7만 명"), ("약 오만 명", "약 5만 명"), ("오만 명의", "5만 명의"),
    ("보병 이만 명과 기병 육천 명", "보병 2만 명과 기병 6천 명"), ("병사 이천 명", "병사 2천 명"), ("로마군 만오천 명", "로마군 1만 5천 명"), ("소 이천 마리", "소 2천 마리"),
    ("칠만 명 가까이", "7만 명 가까이"), ("칠만 명 가까운", "7만 명 가까운"), ("칠만 명이", "7만 명이"), ("약 사만 명", "약 4만 명"), ("사만 팔천여 명", "4만 8천여 명"),
    ("이만 명 가까이", "2만 명 가까이"), ("약 오천칠백 명", "약 5,700명"), ("사천 명", "4천 명"), ("약 육천 명", "약 6천 명"), ("약 만 명", "약 1만 명"),
    ("칠십여 명", "70여 명"), ("팔십여 명", "80여 명"), ("서른일곱 마리", "37마리"), ("군단을 여덟 개", "군단을 8개"),
    ("스물여섯 살", "26살"), ("스물아홉 살", "29살"), ("아홉 살", "9살"), ("여덟 달", "8달"), ("여섯 달", "6달"), ("십사 년", "14년"), ("십오 년", "15년"),
    ("이천 년", "2천 년"), ("백여 년", "100여 년"), ("두 배", "2배"), ("닷새", "5일"), ("세 겹", "3겹"),
]


def L(say):
    t = say
    for a, b in SUBS:
        t = t.replace(a, b)
    return {"t": t, "say": say} if t != say else say


S = []
CUR = {"act": 0, "i": 0}
NUM = {"n": 0}
PINS = {}


def take(n):
    a = ACTS[CUR["act"]]
    out = a[CUR["i"]:CUR["i"] + n]
    assert len(out) == n, (CUR, n, len(a))
    CUR["i"] += n
    return [L(x) for x in out]


def next_act():
    assert CUR["i"] == len(ACTS[CUR["act"]]), ("남은 문장", CUR, ACTS[CUR["act"]][CUR["i"]:])
    CUR["act"] += 1
    CUR["i"] = 0


def nid():
    return f"s{NUM['n'] + 1:03d}"


def sc(n, visual, **kw):
    i = nid()
    NUM["n"] += 1
    d = {"id": i, "act": CUR["act"] + 1, "lines": take(n), "visual": visual}
    d.update(kw)
    S.append(d)


def m(fr, to=None, items=None, **kw):
    v = {"type": "map", "from": fr, "to": to or fr, "items": items or []}
    v.update(kw)
    return v


def ai(img, kb="in"):
    return {"type": "ai", "img": img, "kb": kb}


def doc(head, rows, stamp, org, note="요지"):
    return {"type": "document", "org": org, "head": head, "rows": rows, "stamp": stamp, "note": note}


def text(big, style="yellow", sub=None):
    v = {"type": "text", "big": big, "style": style}
    if sub:
        v.update(sub=sub, subAt=0.4)
    return v


def black(a, b=None):
    v = {"type": "black", "text": a}
    if b:
        v.update(accent=b, accentAt=0.5)
    return v


def cmp(lt, lb, rt, rb, lc="blue", rc="red"):
    return {"type": "compare", "left": {"title": lt, "big": lb, "icon": "none", "color": lc}, "right": {"title": rt, "big": rb, "icon": "none", "color": rc, "at": 0.6}}


def bars(note, items):
    return {"type": "bars", "note": note, "items": items}


def reasons(title, items):
    return {"type": "reasons", "title": title, "items": items}


def checklist(title, items):
    return {"type": "checklist", "title": title, "items": items}


def ranks(profile, vs=None, title=None, labels=None, **kw):
    """정면 전열 대열 (Hook.tsx PhalanxTroops) — profile: 열마다 대열 깊이 · gr = 마케도니아, pe = 페르시아"""
    v = {"type": "troops", "side": "gr", "profile": profile}
    if vs:
        v["vs"] = {"side": "pe", "profile": vs}
    if title:
        v["title"] = title
    if labels:
        v["labels"] = labels
    v.update(kw)
    return v



# 사진: 위키미디어 공용 파일명을 웹 검색으로 확인한 것만 (2026-11-24)
PH = {
    "bust": ("File:Buste de Capoue de Hannibal au Musée National du Bardo 01.jpg",
             "한니발 흉상 · 카푸아 출토 · 나폴리 국립고고학박물관 소장 (한니발인지는 확실하지 않음)", ("한니발 흉상", "로마 시대")),
    "bust_old": ("File:Mommsen p265.jpg",
                 "한니발로 전해지는 흉상 · 카푸아 출토 · 1900년 무렵 사진", ("한니발 흉상", "1900년 무렵 사진")),
    "rhone": ("File:Hannibal's army crossing the Rhone.jpg",
              "론강을 건너는 한니발의 군대 · 앙리 폴 모트", ("앙리 폴 모트", "1878")),
    "turner": ("File:Joseph Mallord William Turner 081.jpg",
               "눈보라 속 알프스를 넘는 한니발 · 윌리엄 터너 · 테이트 브리튼", ("윌리엄 터너", "1812")),
    "fabius": ("File:N26 Fabius Cunctator, Schönbrunn (03).jpg",
               "꾸물거리는 사람 파비우스 조각상 · 빈 쇤브룬 궁전 정원", ("파비우스 조각상", "18세기")),
    "site": ("File:Area archeologica e Antiquarium di Canne della Battaglia - MIBAC 2013-05-02 00-03-51.jpg",
             "오늘날의 칸나이 유적 · 이탈리아 바를레타", ("칸나이 유적", "오늘날")),
    "ofanto": ("File:Ofanto dal ponte di Canosa verso nord.jpg",
               "오늘날의 오판토강 · 옛 아우피두스강 · 카노사 다리에서", ("오판토강", "오늘날")),
    "miniature": ("File:The battle of Cannae.jpg",
                  "칸나이 전투 · 리비우스 『로마사』 프랑스어 필사본 삽화 · 1400년 무렵", ("리비우스 필사본", "1400년 무렵")),
    "trumbull": ("File:John Trumbull - The Death of Paulus Aemilius at the Battle of Cannae - 1832.100 - Yale University Art Gallery.jpg",
                 "칸나이 전투에서 숨지는 파울루스 · 존 트럼불 · 예일대학교 미술관", ("존 트럼불", "1773")),
    "slodtz": ("File:Hannibal Slodtz Louvre MR2093.jpg",
               "칸나이에서 쓰러진 로마 기사들의 반지를 세는 한니발 · 세바스티앙 슬로츠 · 루브르 박물관", ("세바스티앙 슬로츠", "1704")),
    "scipio": ("File:Scipio Africanus the Elder.jpg",
               "스키피오로 전해지는 흉상 · 나폴리 국립고고학박물관", ("스키피오로 전해지는 흉상", "로마 시대")),
    "zama": ("File:Schlacht bei Zama Gemälde H P Motte.jpg",
             "자마 전투 · 앙리 폴 모트", ("앙리 폴 모트", "1890년 무렵")),
    "monument": ("File:Monumento Battaglia di Canne.JPG",
                 "칸나이 전투 기념비 · 칸나이 유적", ("칸나이 전투 기념비", "오늘날")),
}
def pin(key):
    sid = nid()
    PINS[f"{sid}-photo#0"] = PH[key][0]
    return f"{sid}-photo"


def ph(key, pos=None, marks=None):
    v = {"type": "photo", "kb": "in", "q": pin(key), "tag": f"{PH[key][2][0]} · {PH[key][2][1]}"}
    if pos:
        v["pos"] = pos
    if marks:
        v["marks"] = marks
    return v


def plabel(key):
    return PH[key][1]


def mk(t, x, y, on=None, color="yellow", at=None):
    d = {"text": t, "x": x, "y": y, "color": color}
    if on:
        d["on"] = on
    else:
        d["at"] = at or 0
    return d



DRAMA = "재연 일러스트"
# 좌표: 도시·강은 개략, 전장(field)은 모식 배치 — 로마군은 북쪽에서 남쪽을 보고 섰다고 가정(오른쪽 끝 = 서쪽 = 강 쪽)
P = {
    "carthage": [10.32, 36.85, "카르타고"], "newcarthage": [-0.98, 37.6, "카르타고 노바"], "saguntum": [-0.27, 39.68, "사군툼"],
    "sicily": [14.2, 37.5, "시칠리아"], "rhone": [4.65, 43.95, "론강"], "alps": [6.9, 45.25, "알프스"], "pyrenees": [1.5, 42.6, "피레네산맥"],
    "trebia": [9.6, 45.0, "트레비아강"], "trasimene": [12.1, 43.17, "트라시메노 호수"], "rome": [12.48, 41.9, "로마"],
    "gaul": [10.5, 45.3, "북부 이탈리아 · 갈리아 부족"], "falernus": [14.1, 41.15, "산으로 둘러싸인 분지"], "cannae": [16.15, 41.296, "칸나이"],
    "venusia": [15.81, 40.96, "베누시아"], "zama": [9.45, 36.3, "자마"], "sea_mid": [8.0, 39.5, "바다는 로마의 것"],
    "plain": [16.14, 41.278, "아우피두스강 옆 평평한 들판"],
    # --- 전장 (모식) ---
    "paullus": [16.115, 41.2845, "파울루스 · 로마 기병"], "varro": [16.169, 41.2835, "바로 · 동맹군 기병"], "servilius": [16.142, 41.287, "세르빌리우스 · 로마 보병"],
    "hasdrubal": [16.106, 41.2715, "하스드루발 · 무거운 기병"], "numid": [16.175, 41.2705, "누미디아 기병"], "hannibal": [16.142, 41.2735, "한니발 · 마고"],
    "afr_l": [16.12, 41.268, "아프리카 보병"], "afr_r": [16.164, 41.268, "아프리카 보병"], "center": [16.142, 41.277, "가운데"],
    "rcamp": [16.128, 41.297, "로마 진영"], "ccamp": [16.142, 41.258, "카르타고 진영"], "cannae_hill": [16.15, 41.296, "칸나이 언덕"],
    "river_pt": [16.104, 41.279, "아우피두스강"],
}
V = {
    "westmed": {"center": [4.5, 40.5], "span": 26.0}, "italy": {"center": [12.8, 42.0], "span": 10.0},
    "apulia": {"center": [15.9, 41.25], "span": 1.6}, "field": {"center": [16.14, 41.277], "span": 0.09},
}
LAND = {"home": ["380"], "foreign": ["724", "250", "788", "12", "504", "620", "756", "40", "705", "191", "434", "8", "70", "499", "300", "276", "470"]}

# --- 강 (개략) ---
OFANTO = [[15.55, 40.95], [15.8, 41.05], [16.0, 41.2], [16.05, 41.236], [16.085, 41.262], [16.11, 41.283], [16.135, 41.303], [16.16, 41.318], [16.2, 41.355]]
RIV = lambda path=OFANTO, at=0: {"k": "line", "path": path, "color": "#5aa0d8", "glow": False, "at": at}
# --- 원정로 (개략) ---
TO_ALPS = [[-0.98, 37.6], [0.6, 40.8], [2.5, 42.4], [4.65, 43.95], [6.9, 45.25], [7.7, 45.07], [9.6, 45.0]]
SEA_ROUTE = [[10.32, 36.85], [11.5, 38.8], [12.3, 41.6]]
TO_TRAS = [[9.6, 45.0], [10.6, 43.8], [12.1, 43.17]]
TO_SOUTH = [[12.1, 43.17], [13.6, 42.4], [14.1, 41.15], [15.3, 41.2], [16.15, 41.296]]
ROME_ARMY = [[12.48, 41.9], [14.2, 41.7], [15.5, 41.45], [16.15, 41.296]]
VARRO_FLEE = [[16.15, 41.296], [16.0, 41.12], [15.81, 40.96]]
MAGO_SEA = [[16.15, 41.296], [16.6, 40.0], [15.5, 38.2], [12.5, 37.3], [10.32, 36.85]]
SCIPIO = [[14.2, 37.5], [12.0, 37.3], [10.6, 36.9], [9.45, 36.3]]

# --- 전장 기하 (모식) ---
R_LINE = [[16.122, 41.283], [16.162, 41.283]]   # 로마 보병: 서(강 쪽) → 동 · 정면 = 남쪽(face 1)
C_LINE = [[16.116, 41.2705], [16.168, 41.2705]]  # 카르타고: 서 → 동 · 정면 = 북쪽(face -1)
R_DEEP = [9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
C_PROF = [8, 8, 3, 3, 3, 3, 3, 3, 8, 8]            # 양 끝 = 아프리카 보병(두껍게) · 가운데 = 갈리아·에스파냐(얇게)
LEVEL = [[16.112, 41.29], [16.172, 41.29], [16.172, 41.262], [16.112, 41.262]]
POCKET = [[16.12, 41.289], [16.164, 41.289], [16.166, 41.276], [16.142, 41.268], [16.118, 41.276]]
HASD_CHARGE = [[16.106, 41.2715], [16.11, 41.2775], [16.114, 41.2835]]
R_CAV_FLEE = [[16.114, 41.286], [16.12, 41.294], [16.128, 41.302]]
HASD_RIDE = [[16.116, 41.289], [16.13, 41.2925], [16.15, 41.2925], [16.169, 41.289]]
ALLIED_FLEE = [[16.17, 41.2845], [16.18, 41.291], [16.19, 41.298]]
REAR_HIT = [[16.166, 41.2925], [16.153, 41.29], [16.142, 41.2875]]
NUM_PATH = [[16.178, 41.271], [16.172, 41.279], [16.18, 41.274], [16.172, 41.281]]
AFR_L_TURN = [[16.117, 41.268], [16.121, 41.275], [16.128, 41.2795]]
AFR_R_TURN = [[16.167, 41.268], [16.163, 41.275], [16.156, 41.2795]]
R_PUSH = [[16.142, 41.2875], [16.142, 41.28], [16.142, 41.2735]]
SKIRM = [[16.135, 41.276], [16.135, 41.28]]
DUST = [[16.124, 41.279], [16.142, 41.278], [16.16, 41.279]]
RPH = lambda at=0, **kw: dict({"k": "phalanx", "path": R_LINE, "depth": R_DEEP, "face": 1, "px": 3.4, "color": "red", "at": at}, **kw)
CPH = lambda at=0, **kw: dict({"k": "phalanx", "path": C_LINE, "depth": C_PROF, "face": -1, "px": 3.4, "color": "blue", "at": at}, **kw)
BULGE = lambda at=0, **kw: CPH(at, bend=-30, bendAt=0, **kw)        # 로마군 쪽으로 불룩한 초승달
CONCAVE = lambda at=0, **kw: CPH(at, bend=40, **kw)                 # 뒤로 밀려 오목해진 초승달 (bendOn/bendAt 함께)
LOCK = lambda p, at=0.3, text=None, on=None: dict({"k": "lock", "p": p, "text": text or P[p][2]}, **({"on": on} if on else {"at": at}))
badge = lambda p, t, c="#111", at=0.3, dy=-70, on=None: dict({"k": "badge", "p": p, "text": t, "color": c, "dy": dy}, **({"on": on} if on else {"at": at}))
red_a = lambda path, at=0.3, w=1.0, on=None: dict({"k": "arrow", "path": path, "color": "red", "width": w}, **({"on": on} if on else {"at": at}))
blue_a = lambda path, at=0.3, w=1.0, on=None: dict({"k": "arrow", "path": path, "color": "blue", "width": w}, **({"on": on} if on else {"at": at}))
dash_r = lambda path, at=0.2, on=None: dict({"k": "arrow", "path": path, "color": "red", "dash": True}, **({"on": on} if on else {"at": at}))
dash_b = lambda path, at=0.2, on=None: dict({"k": "arrow", "path": path, "color": "blue", "dash": True}, **({"on": on} if on else {"at": at}))
mark = lambda p, color="red", at=0, text=None, on=None: dict({"k": "marker", "p": p, "color": color}, **({"text": text} if text else {}), **({"on": on} if on else {"at": at}))
unit = lambda p, t, color="red", at=0.1, pulse=False: dict({"k": "unit", "p": p, "text": t, "color": color, "at": at}, **({"pulse": True} if pulse else {}))
clash = lambda p, at=0.3, size=1.0, on=None: dict({"k": "clash", "p": p, "period": 0.9, "size": size}, **({"on": on} if on else {"at": at}))
swarm = lambda path, at=0.1, n=120, width=None, color=None: dict({"k": "swarm", "path": path, "at": at, "n": n}, **({"width": width} if width else {}), **({"color": color} if color else {}))
line = lambda path, at=0.1, color="#ffd400", on=None: dict({"k": "line", "path": path, "color": color, "glow": True}, **({"on": on} if on else {"at": at}))
zone = lambda path=None, text=None, at=0, on=None, color="#d8b46a": dict({"k": "zone", "path": path or LEVEL, "color": color}, **({"text": text} if text else {}), **({"on": on} if on else {"at": at}))
top = lambda t, s="yellow", at=0: [{"text": t, "style": s, "at": at, "pos": "top"}]
low = lambda t, s="dark", at=0: [{"text": t, "style": s, "at": at, "pos": "lower"}]
SW = lambda at=0: [{"id": "whoosh", "at": at}]
PING = lambda at=0.6: [{"id": "ping", "at": at}]
WIND = lambda at=0: [{"id": "wind", "at": at}]
FAR = lambda at=0: [{"id": "artillery_far", "at": at, "db": -32}]
HUD = lambda big, sub=None, sub2=None, at=0.0, color=None, count=None, on=None: dict({"big": big}, **({"sub": sub} if sub else {}), **({"sub2": sub2} if sub2 else {}),
                                                                                      **({"on": on} if on else {"at": at}), **({"color": color} if color else {}), **({"count": count} if count is not None else {}))

QUESTION = "일부러 중앙을 밀리게 한 한니발은\n어떻게 2배 가까운 로마군을\n통째로 가뒀을까"
FLD = lambda items, tilt=30, **kw: m("field", "field", [RIV()] + items, tilt=tilt, **kw)

# ===== 제1막 · 콜드 오프닝 (0~10초 사건 직격 → 모순 3단 → X 반전 → 중앙 질문 카드 → 타이틀) =====
# 레이어 교차: 3D 비행 → 병력 대열 → 사료(흉상) → 재연 그림 → 3D 초승달 → 병력 대열(밀림) → 재연 그림 → X → 지도+질문 카드 → 타이틀
sc(2, m("italy", "field", [RIV(), LOCK("plain", 1.2, "칸나이 들판")], flight=["italy", "apulia", "field"], flightDur=4.6, hud=True, tilt=26),
   hook={"hud": [HUD("기원전 216년 8월 2일", "칸나이 들판", "이탈리아 남부 아풀리아", count=False)]}, sfx=SW(0) + PING(1.4))
sc(2, ranks(C_PROF, R_DEEP + R_DEEP[:6], title="칸나이 · 기원전 216년"),
   hook={"hud": [HUD("약 8만 6천", "로마군", "로마 역사상 가장 큰 군대 · 폴리비오스", color="#FF3B30", on="팔만", count=False)]})
sc(1, ph("bust", pos="50% 30%"), label=plabel("bust"), hook={"hud": [HUD("약 5만", "한니발의 군대", "보병 4만 · 기병 1만", on="오만", count=False)]})
sc(1, ai("crushed"), label=DRAMA, hook={"hud": [HUD("거의 0", "들판에 남은 로마군", "해가 질 무렵", color="#FF3B30", on="거의", count=False)]})
sc(2, FLD([RPH(0), BULGE(0), badge("center", "일부러 얇게", "#1f5fbf", on="얇게", dy=60), LOCK("hannibal", on="한니발이 서")], tilt=32), sfx=PING(2.6))
sc(2, ranks(C_PROF, R_DEEP + R_DEEP[:6], bendOn="밀면", labels=[{"text": "밀수록 더 깊이", "x": 0.5, "y": 0.5, "color": "red", "on": "깊이"}]))
sc(1, ai("center_pushed"), label=DRAMA, hook={"hud": [HUD("5만~7만", "쓰러진 로마군", "리비우스 · 폴리비오스", color="#FF3B30", on="오만에서", count=False)]})
sc(2, black("숫자의 방심?", "운이었을까"), hook={"neg": {"text": "방심한 대군", "on": "방심했다가", "xOn": "그랬을까요"}})
sc(1, FLD([RPH(0), BULGE(0)], tilt=30), hook={"question": {"text": QUESTION, "at": 0.02}})
sc(1, {"type": "titlecard", "title": "일부러 밀렸다", "sub": "칸나이 전투 · 기원전 216년", "at": 0, "q": pin("trumbull")}, flash=True)
next_act()

# ===== 제2막 · 알프스를 넘은 맹세 =====
sc(2, m("westmed", "westmed", [LOCK("carthage", 0.6)], tilt=14), chapter={"num": "제2막", "title": "알프스를 넘은 맹세"},
   callouts=top("기원전 237년 무렵 · 카르타고"), sfx=SW(0) + PING(1.4))
sc(2, m("westmed", "westmed", [mark("carthage", "blue", 0), badge("sicily", "로마에 빼앗긴 시칠리아", "#c9242c", on="시칠리아를", dy=-70)], tilt=14))
sc(2, text("하밀카르", "blue", "한니발의 아버지 · 카르타고의 장군"))
sc(2, ai("oath"), label=DRAMA, callouts=top("아홉 살 소년의 맹세"))
sc(1, black("소년은", "맹세했다"))
sc(1, ph("bust_old", pos="50% 30%", marks=[mk("한니발", 0.5, 0.12, "한니발입니다")]), label=plabel("bust_old"))
sc(2, m("westmed", "westmed", [LOCK("newcarthage", on="에스파냐의"), badge("newcarthage", "26살 · 군대를 물려받다", "#1f5fbf", on="스물여섯", dy=70)], tilt=14))
sc(2, m("westmed", "westmed", [mark("newcarthage", "blue", 0), LOCK("saguntum", on="사군툼을"), badge("saguntum", "8달 포위", "#c9242c", on="여덟", dy=-70)], tilt=16))
sc(1, text("로마의 선전 포고", "red", "두 번째 전쟁의 시작"))
sc(2, m("westmed", "westmed", [dash_r(SEA_ROUTE, 0.2), badge("sea_mid", "바다는 로마의 것", "#c9242c", on="바다를", dy=-60)], tilt=12))
sc(2, black("아무도 생각 못 한 길", "걸어서"))
sc(1, m("westmed", "westmed", [blue_a(TO_ALPS, on="피레네산맥을", w=1.1), LOCK("alps", on="알프스를")], tilt=14), sfx=PING(1.8))
sc(4, reasons("한니발의 군대", [{"text": "아프리카 보병", "on": "아프리카의"}, {"text": "에스파냐 전사", "on": "전사들"},
                             {"text": "누미디아 기병", "on": "누미디아"}, {"text": "발레아레스 투석병", "on": "발레아레스"}]))
sc(1, text("하나로 묶은 사람", "yellow", "말도 풍습도 다른 군대"))
sc(2, ph("rhone", pos="50% 50%", marks=[mk("코끼리 37마리", 0.5, 0.14, "코끼리")]), label=plabel("rhone"))
sc(1, ai("elephant_raft"), label=DRAMA, callouts=top("론강 · 흙을 덮은 뗏목"))
sc(3, ph("turner", pos="50% 45%", marks=[mk("가을의 알프스", 0.5, 0.12, "알프스는")]), label=plabel("turner"), sfx=WIND(0))
sc(2, cmp("떠날 때", "훨씬 많았다", "알프스를 넘은 뒤", "보병 2만 · 기병 6천", "dark", "blue"))
sc(2, text("“적이 산에서 내려왔다”", "dark", "믿지 못한 로마"))
sc(2, m("westmed", "italy", [LOCK("gaul", on="갈리아"), blue_a([[7.7, 45.07], [9.0, 45.1], [10.5, 45.3]], on="하나둘")], flight=["westmed", "italy"], flightDur=2.4, tilt=16), sfx=SW(0))
sc(1, m("italy", "italy", [LOCK("trebia", on="트레비아강에서")], tilt=16), callouts=top("기원전 218년 겨울"))
sc(1, ai("trebia_ambush"), label=DRAMA)
sc(2, cmp("로마군", "굶은 채 얼음 강", "한니발군", "배를 채우고 불 옆에서", "red", "blue"))
sc(1, text("등 뒤의 기습", "blue", "숨어 있던 2천 명"))
sc(2, m("italy", "italy", [mark("trebia", "blue", 0), blue_a(TO_TRAS, 0.2), LOCK("trasimene", on="트라시메노")], tilt=16), callouts=top("기원전 217년 봄"))
sc(1, ai("trasimene_fog"), label=DRAMA)
sc(1, text("로마군 1만 5천 명", "red", "집정관 플라미니우스 전사"))
sc(2, text("“우리는 큰 싸움에서 졌다”", "yellow", "로마 광장 · 리비우스 22권 7절"))
sc(1, checklist("한니발의 싸움", [{"text": "땅을 먼저 고른다", "on": "땅을"}, {"text": "숨어서 기다린다", "on": "숨어서"}]))
sc(1, text("코끼리는 거의 다 죽다", "dark", "추위와 병"))
sc(1, ph("bust", pos="50% 30%", marks=[mk("한쪽 눈을 잃다", 0.5, 0.12, "한쪽")]), label=plabel("bust"))
next_act()

# ===== 제3막 · 기다린 남자와 서두른 남자 =====
MID = [nid()]
sc(1, m("italy", "italy", [LOCK("rome", 0.4)], tilt=14), pauseBefore=0.5, chapter={"num": "제3막", "title": "기다린 남자와 서두른 남자"})
sc(1, ph("fabius", pos="50% 25%", marks=[mk("파비우스 막시무스", 0.5, 0.12, "파비우스")]), label=plabel("fabius"))
sc(3, doc("독재관 파비우스의 명령", ["정면으로 싸우지 마라", "산 위에 머물러라", "뒤를 따라다녀라"], "지연 전술", "폴리비오스 3권 89절"))
sc(3, checklist("한니발의 약점", [{"text": "남의 땅에서 먹고 자야 한다", "on": "먹고"}, {"text": "보급도 증원군도 없다", "on": "보급도"}, {"text": "시간은 로마 편", "on": "시간은"}]))
sc(2, text("참지 못한 로마", "red", "불타는 들판 · 언덕 위의 군대"))
sc(2, m("italy", "italy", [LOCK("falernus", on="분지에"), badge("falernus", "고개를 막은 로마군", "#c9242c", on="고개를", dy=-70)], tilt=16))
sc(2, ai("oxen_torches"), label=DRAMA, callouts=top("소 2천 마리 · 불붙은 나뭇가지"), sfx=WIND(0))
sc(2, text("텅 빈 고개", "blue", "횃불에 속은 로마 병사들 · 리비우스 22권 17절"))
sc(2, text("“꾸물거리는 사람”", "yellow", "파비우스에게 붙은 별명"))
sc(1, black("로마는", "다른 길을"))
sc(1, text("기원전 216년", "yellow", "새 집정관 두 사람"))
sc(3, cmp("아이밀리우스 파울루스", "신중한 귀족", "테렌티우스 바로", "싸워서 끝낸다", "dark", "red"))
sc(3, ranks(R_DEEP + R_DEEP + R_DEEP[:4], side="pe", title="8개 군단 · 로마 역사상 가장 큰 군대"),
   hook={"hud": [HUD("약 8만 6천", "로마와 동맹군", "보병 8만 · 기병 6천 · 폴리비오스", color="#FF3B30", on="팔만", count=False)]})
sc(2, text("하루씩 번갈아 지휘", "red", "두 집정관 · 로마의 관습"))
sc(3, cmp("오늘", "파울루스", "내일", "바로", "dark", "red"))
sc(2, m("italy", "apulia", [RIV(), LOCK("cannae", on="칸나이"), badge("cannae", "로마군의 곡식 창고", "#111", on="곡식", dy=-80), blue_a(TO_SOUTH[-2:], 0.2)],
        flight=["italy", "apulia"], flightDur=2.4, tilt=18), sfx=SW(0))
sc(1, black("더 이상", "기다릴 수 없다"))
sc(2, m("apulia", "field", [RIV(), zone(LEVEL, "평평한 들판", on="평평한"), LOCK("river_pt", on="아우피두스강이")], flight=["apulia", "field"], flightDur=2.4, tilt=28), sfx=PING(2.0))
sc(2, bars("기병", [{"label": "한니발", "value": 10000, "display": "약 1만", "color": "blue", "on": "만 명"},
                    {"label": "로마", "value": 6000, "display": "약 6천", "color": "red", "on": "육천"}]))
sc(2, cmp("파울루스", "여기서는 싫다", "바로", "여기서 끝낸다", "dark", "red"))
sc(1, FLD([BULGE(0.2), badge("ccamp", "8월 1일 · 싸움을 걸다", "#1f5fbf", on="팔월", dy=-70)], tilt=28))
sc(1, text("파울루스는 나가지 않았다", "dark", "로마 진영"))
sc(1, FLD([unit("rcamp", "로마 진영", "red", 0.1), swarm([[16.135, 41.276], [16.12, 41.288], [16.11, 41.295]], 0.2, 60, 0.4), badge("river_pt", "물 긷는 병사", "#c9242c", on="물을", dy=-70)], tilt=30))
sc(1, black("분노", "끓어오르는 로마 진영"))
sc(1, text("8월 2일", "red", "바로가 지휘하는 날"))
next_act()

# ===== 제4막 · 초승달 =====
sc(2, FLD([unit("rcamp", "로마 진영", "red", 0.1, pulse=True), badge("rcamp", "붉은 겉옷 · 싸움의 신호", "#c9242c", on="붉은", dy=-80)], tilt=28), pauseBefore=0.5,
   chapter={"num": "제4막", "title": "초승달"}, callouts=top("기원전 216년 8월 2일 아침"), sfx=SW(0))
sc(2, FLD([RPH(on="줄을"), unit("rcamp", "진영 경비 약 1만", "red", 0.4)], tilt=30),
   hook={"hud": [HUD("약 7만", "들판에 선 로마 보병", "폴리비오스", color="#FF3B30", on="칠만", count=False)]})
sc(4, checklist("로마 군단의 3겹", [{"text": "앞 · 젊은 병사", "on": "젊은"}, {"text": "가운데 · 한창때의 병사", "on": "한창때의"}, {"text": "뒤 · 노련한 고참병", "on": "고참병이"}]))
sc(1, FLD([RPH(0), badge("servilius", "세르빌리우스 · 가운데 보병", "#c9242c", on="세르빌리우스가", dy=-70)], tilt=30))
sc(3, ranks(R_DEEP + R_DEEP + R_DEEP + R_DEEP, side="pe", title="앞뒤로 두껍게"), callouts=low("평소보다 훨씬 깊은 대열", "dark", 1.0))
sc(1, text("거대한 망치", "red", "한가운데를 내리쳐 부순다"))
sc(2, FLD([RPH(0), badge("paullus", "파울루스 · 로마 기병", "#c9242c", on="파울루스가", dy=-70), badge("varro", "바로 · 동맹군 기병", "#c9242c", on="바로가", dy=-70)], tilt=30))
sc(2, FLD([RPH(0), line(OFANTO[3:7], on="강은", color="#6fd0ff"), badge("river_pt", "강 = 오른쪽의 벽", "#111", on="벽이었습니다", dy=-60)], tilt=30), sfx=PING(0.8))
sc(2, FLD([RPH(0), CPH(on="맞은편")], tilt=30))
sc(2, ai("gisgo_laugh"), label=DRAMA, callouts=top("“적이 정말 많습니다”"))
sc(3, text("“기스고라는 이름은 하나도 없다”", "yellow", "플루타르코스 『파비우스 전』 15장"))
sc(2, text("웃음이 번지다", "blue", "대장의 여유"))
sc(1, black("그런데", "이상한 대열"))
sc(2, FLD([RPH(0), CPH(0), badge("center", "갈리아 · 에스파냐 보병", "#1f5fbf", on="갈리아", dy=70)], tilt=32))
sc(3, FLD([RPH(0), CPH(0, bend=-30, bendOn="불룩하게"), badge("center", "초승달", "#1f5fbf", on="초승달처럼요", dy=80)], tilt=34), sfx=PING(1.4))
sc(2, ranks(C_PROF, R_DEEP + R_DEEP[:6], title="얇은 가운데", labels=[{"text": "얇다", "x": 0.5, "y": 0.5, "color": "blue", "on": "얇았습니다"}]))
sc(3, FLD([RPH(0), BULGE(0), badge("afr_l", "아프리카 보병", "#1f5fbf", on="아프리카", dy=70), badge("afr_r", "로마군의 갑옷", "#1f5fbf", on="갑옷과", dy=70)], tilt=32))
sc(2, FLD([RPH(0), BULGE(0), unit("hasdrubal", "하스드루발 · 무거운 기병", "blue", 0.1), badge("numid", "누미디아 기병", "#1f5fbf", on="누미디아", dy=70)], tilt=30))
sc(1, black("한니발은", "어디에?"))
sc(2, FLD([RPH(0), BULGE(0), LOCK("hannibal", on="한가운데에"), badge("hannibal", "무너지기로 된 자리", "#111", on="무너지기로", dy=80)], tilt=34), sfx=PING(1.6))
sc(3, text("볼투르누스 바람", "dark", "로마군 얼굴로 흙먼지 · 리비우스에만 있는 기록"), sfx=WIND(0))
sc(4, bars("칸나이의 병력", [{"label": "로마 보병", "value": 70000, "display": "약 7만", "color": "red", "at": 0.2},
                         {"label": "한니발 보병", "value": 40000, "display": "약 4만", "color": "blue", "on": "사만"},
                         {"label": "한니발 기병", "value": 10000, "display": "약 1만", "color": "blue", "on": "기병은"}]))
sc(1, FLD([RPH(0), BULGE(0), dash_b(SKIRM, on="투석병과"), dash_r([[16.15, 41.282], [16.15, 41.277]], on="투창병들이")], tilt=32), sfx=FAR(0))
next_act()

# ===== 제5막 · 뒤집힌 초승달 =====
MID.append(nid())
sc(1, FLD([RPH(0), BULGE(0)], tilt=32), pauseBefore=0.5, chapter={"num": "제5막", "title": "뒤집힌 초승달"}, sfx=SW(0))
sc(1, FLD([RPH(0), BULGE(0), swarm(HASD_CHARGE, 0, 90, 0.5, "#1f5fbf"), clash([16.112, 41.2785], on="부딪쳤죠")], tilt=34), sfx=FAR(0))
sc(2, ai("cavalry_river"), label=DRAMA, callouts=top("말에서 내려 싸운 기병들"))
sc(1, text("로마 기병 붕괴", "red", "강가의 좁은 땅"))
sc(1, FLD([RPH(0), badge("paullus", "파울루스 부상", "#c9242c", on="다쳤다고", dy=-70)], tilt=32))
sc(1, FLD([RPH(0), BULGE(0), dash_r(R_CAV_FLEE, 0.1), swarm(R_CAV_FLEE, 0.3, 80, 0.4, "#1f5fbf")], tilt=32))
sc(2, FLD([RPH(0, run=22, runOn="밀고"), BULGE(0), red_a(R_PUSH, on="밀고", w=1.3)], tilt=32), sfx=PING(1.8))
sc(1, FLD([RPH(0, run=22, runAt=0), BULGE(0), clash("center", on="가운데였죠", size=1.2)], tilt=34))
sc(2, ai("center_pushed"), label=DRAMA)
sc(3, ph("miniature", pos="50% 50%", marks=[mk("8월 한여름의 들판", 0.5, 0.14, "한여름의")]), label=plabel("miniature"))
sc(3, text("“이기고 있다”", "red", "앞으로 몰려드는 로마 병사들"))
sc(3, FLD([RPH(0, run=30, runAt=0), CONCAVE(0, bendOn="평평해졌습니다"), badge("center", "뒤집힌 초승달", "#1f5fbf", on="뒤집힌", dy=80)], tilt=34), sfx=PING(2.6))
sc(2, ranks(C_PROF, R_DEEP + R_DEEP[:6], bendOn="빨려", labels=[{"text": "오목한 주머니", "x": 0.5, "y": 0.45, "color": "red", "on": "주머니"}]))
sc(2, FLD([RPH(0, run=30, runAt=0), CONCAVE(0, bendAt=0), LOCK("hannibal", on="한니발이")], tilt=34))
sc(2, text("발레아레스 투석병", "blue", "빽빽한 대열 · 빗나가기 어려운 돌"))
sc(2, black("밀리되", "무너지지 않는다"))
sc(1, text("양 옆에는?", "yellow", "로마군의 옆구리"))
sc(1, FLD([RPH(0, run=30, runAt=0), CONCAVE(0, bendAt=0), LOCK("afr_l", on="아프리카"), LOCK("afr_r", on="아프리카")], tilt=34))
sc(3, ai("africans_turn"), label=DRAMA, callouts=top("몸을 돌린 아프리카 보병", "blue"))
sc(1, FLD([RPH(0, run=30, runAt=0), CONCAVE(0, bendAt=0, wrap=55, wrapOn="파고들었죠"), blue_a(AFR_L_TURN, on="양쪽에서", w=1.2), blue_a(AFR_R_TURN, on="양쪽에서", w=1.2)], tilt=34), sfx=FAR(0))
sc(2, ranks(C_PROF, R_DEEP + R_DEEP[:6], bendAt=0, wrapOn="옆을", labels=[{"text": "똑같은 갑옷", "x": 0.5, "y": 0.42, "color": "red", "on": "똑같은"}]))
sc(2, FLD([badge("varro", "동맹군 기병", "#c9242c", on="동맹군", dy=-70), badge("numid", "누미디아 기병", "#1f5fbf", on="누미디아", dy=70)], tilt=30))
sc(4, checklist("누미디아 기병의 일", [{"text": "정면으로 부딪치지 않는다", "on": "정면으로"}, {"text": "달려들었다 빠진다", "on": "달려들었다가"},
                                    {"text": "이기지 않아도 된다", "on": "이기지"}, {"text": "붙잡아 두기만", "on": "붙잡아"}]))
sc(1, FLD([RPH(0, run=30, runAt=0), CONCAVE(0, bendAt=0, wrap=55, wrapAt=0), swarm(HASD_RIDE[:2], 0.2, 90, 0.5, "#1f5fbf"), badge("paullus", "하스드루발이 온다", "#1f5fbf", on="하스드루발이", dy=-70)], tilt=32))
next_act()

# ===== 제6막 · 닫힌 뒷문 =====
MID.append(nid())
sc(2, FLD([RPH(0, run=30, runAt=0), CONCAVE(0, bendAt=0, wrap=55, wrapAt=0), blue_a(HASD_RIDE, on="가로질러", w=1.3)], tilt=34), pauseBefore=0.5,
   chapter={"num": "제6막", "title": "닫힌 뒷문"}, sfx=SW(0))
sc(1, ai("hasdrubal_ride"), label=DRAMA)
sc(1, FLD([dash_r(ALLIED_FLEE, 0.1), swarm(HASD_RIDE[2:], 0.1, 100, 0.5, "#1f5fbf"), badge("varro", "달아나는 동맹군 기병", "#c9242c", on="달아났습니다", dy=-70)], tilt=32))
sc(1, FLD([dash_b(NUM_PATH[-2:] + [[16.19, 41.298]], 0.1), badge("numid", "추격은 누미디아에게", "#1f5fbf", on="맡겼습니다", dy=70)], tilt=30))
sc(2, FLD([RPH(0, run=30, runAt=0), CONCAVE(0, bendAt=0, wrap=55, wrapAt=0), blue_a(REAR_HIT, on="말머리를", w=1.4)], tilt=34), sfx=FAR(0))
sc(3, checklist("사방이 막혔다", [{"text": "앞 · 갈리아와 에스파냐", "on": "앞에는"}, {"text": "양옆 · 아프리카 보병", "on": "양쪽에는"}, {"text": "뒤 · 하스드루발의 기병", "on": "뒤에는"}]))
sc(2, FLD([RPH(0, run=30, runAt=0), CONCAVE(0, bendAt=0, wrap=55, wrapAt=0), zone(POCKET, "포위망", on="닫혔습니다", color="#c9242c"), blue_a(REAR_HIT, 0)], tilt=36),
   hook={"hud": [HUD("7만 vs 5만", "둘러싸인 쪽이 더 많았다", "로마 보병 · 한니발 전군", color="#FF3B30", on="칠만", count=False)]}, sfx=PING(1.2))
sc(1, black("더 많은 쪽이", "왜 못 뚫었나"))
sc(2, ai("crushed"), label=DRAMA)
sc(2, ranks([9] * 16, side="pe", title="싸울 수 있는 건 바깥 줄뿐", labels=[{"text": "안쪽 수만 명", "x": 0.5, "y": 0.45, "color": "red", "on": "수만"}]))
sc(1, text("사람의 벽", "red", "도망칠 수도 나아갈 수도 없다"))
sc(2, FLD([zone(POCKET, "포위망", 0, color="#c9242c"), CONCAVE(0, bendAt=0, wrap=55, wrapAt=0), clash("servilius", on="쓰러지면", size=1.3)], tilt=36), sfx=FAR(0))
sc(1, text("해가 질 때까지", "dark", "8월 2일 저녁"))
sc(2, ai("paullus_refuses"), label=DRAMA)
sc(2, text("“성벽을 굳게 지키라고 전하라”", "yellow", "파울루스 · 리비우스 22권 49절"))
sc(1, ph("trumbull", pos="50% 50%"), label=plabel("trumbull"))
sc(2, ph("trumbull", pos="62% 45%", marks=[mk("말을 내미는 젊은 장교", 0.36, 0.14, "말을"), mk("집정관 파울루스", 0.66, 0.14, "늙은")]), label=plabel("trumbull"))
sc(1, m("apulia", "apulia", [RIV(), dash_r(VARRO_FLEE, 0.2), LOCK("venusia", on="베누시아로")], tilt=18))
sc(1, black("그날", "로마군의 피해"))
sc(2, bars("로마군 전사자 · 옛 기록", [{"label": "폴리비오스", "value": 70000, "display": "7만", "color": "red", "on": "칠만"},
                                {"label": "리비우스", "value": 48200, "display": "4만 8천여 · 포로 2만 가까이", "color": "red", "on": "사만"}]))
sc(2, FLD([unit("rcamp", "진영 경비 약 1만 · 포로", "red", 0.2), mark("ccamp", "blue", 0.4)], tilt=30))
sc(2, ph("site", pos="50% 50%"), label=plabel("site"))
sc(1, text("집정관 1명 · 원로원 의원 80여 명", "red", "리비우스 22권 49절"))
sc(2, bars("한니발 쪽 전사자 · 폴리비오스", [{"label": "갈리아 병사", "value": 4000, "display": "4천", "color": "blue", "on": "사천"},
                                   {"label": "그 밖의 병사", "value": 1700, "display": "약 1,700", "color": "blue", "at": 0.3}]))
sc(2, FLD([CONCAVE(0, bendAt=0), badge("center", "가장 큰 값을 치른 가운데 줄", "#1f5fbf", on="가운데 줄이었습니다", dy=80)], tilt=34))
next_act()

# ===== 제7막 · 답 =====
sc(1, ai("maharbal"), label=DRAMA, pauseBefore=0.5, chapter={"num": "제7막", "title": "답"}, sfx=SW(0))
sc(2, text("“닷새 뒤에는 로마에서 저녁을”", "yellow", "기병 대장 마하르발"))
sc(2, m("apulia", "italy", [mark("cannae", "blue", 0), dash_b(ROME_ARMY[::-1], 0.3), LOCK("rome", on="성벽이")], flight=["apulia", "italy"], flightDur=2.2, tilt=14))
sc(3, text("“승리를 쓰는 법은 모르신다”", "red", "마하르발의 탄식 · 리비우스 22권 51절"))
sc(1, m("italy", "westmed", [dash_b(MAGO_SEA, 0.2), LOCK("carthage", on="카르타고로")], flight=["italy", "westmed"], flightDur=2.2, tilt=12))
sc(1, ph("slodtz", pos="50% 30%", marks=[mk("로마 기사들의 금반지", 0.5, 0.12, "금반지를")]), label=plabel("slodtz"))
sc(1, black("그런데 로마는", "무너지지 않았다"))
sc(3, checklist("로마의 대답", [{"text": "평화를 청하지 않는다", "on": "평화를"}, {"text": "포로의 몸값도 내지 않는다", "on": "몸값도"}, {"text": "노예에게 무기를", "on": "노예"}]))
sc(2, ai("varro_returns"), label=DRAMA, callouts=top("돌아온 집정관 바로"))
sc(2, text("“나라를 포기하지 않아 고맙다”", "yellow", "리비우스 22권 61절"))
sc(2, ph("fabius", pos="50% 25%", marks=[mk("다시 파비우스의 방식으로", 0.5, 0.12, "파비우스의")]), label=plabel("fabius"))
sc(1, ph("scipio", pos="50% 35%", marks=[mk("칸나이의 생존자 스키피오", 0.5, 0.12, "스키피오라는")]), label=plabel("scipio"))
sc(2, m("westmed", "westmed", [blue_a(SCIPIO, 0.2), LOCK("zama", on="자마에서")], tilt=14), callouts=top("기원전 202년 · 자마"))
sc(1, ph("zama", pos="50% 50%", marks=[mk("시칠리아로 쫓겨났던 칸나이 생존자들", 0.5, 0.12, "시칠리아로")]), label=plabel("zama"))
sc(2, FLD([RPH(0), BULGE(0)], tilt=30), hook={"question": {"text": QUESTION, "on": "어떻게", "kicker": "■ 답 ■"}})
sc(3, FLD([RPH(0, run=30, runOn="열어"), CONCAVE(0, bendOn="열어"), badge("center", "열어 준 길", "#1f5fbf", on="길을", dy=80)], tilt=34))
sc(2, FLD([RPH(0, run=30, runAt=0), CONCAVE(0, bendAt=0, wrap=55, wrapOn="닫혔습니다"), blue_a(AFR_L_TURN, 0.2), blue_a(AFR_R_TURN, 0.2)], tilt=34))
sc(1, FLD([RPH(0, run=30, runAt=0), CONCAVE(0, bendAt=0, wrap=55, wrapAt=0), blue_a(REAR_HIT, on="마지막", w=1.4), zone(POCKET, None, on="닫았습니다", color="#c9242c")], tilt=36), sfx=PING(1.2))
sc(1, cmp("로마의 숫자", "무기", "포위된 뒤", "벽", "red", "red"))
sc(1, FLD([CONCAVE(0, bendAt=0), LOCK("hannibal", on="한니발 자신이")], tilt=34))
sc(1, black("가장 큰 힘을", "덫으로"))
sc(2, cmp("전투", "한니발의 승리", "전쟁", "로마의 승리", "blue", "red"))
sc(1, ph("monument", pos="50% 50%"), label=plabel("monument"))
sc(2, m("westmed", "westmed", [mark("cannae", "blue", 0), LOCK("rome", 0.4, "로마 · 끝내 무너지지 않다")], tilt=12), callouts=top("이탈리아의 15년"))
sc(1, text("이천 년의 교과서", "yellow", "칸나이의 포위"))
sc(2, doc("칸나이 연구", ["독일 참모총장 슐리펜", "적은 숫자로 많은 적을", "완전히 둘러싸 없앤다"], "포위", "20세기 초"))
sc(1, ph("ofanto", pos="50% 55%"), label=plabel("ofanto"))
sc(2, text("다음 이야기", "yellow", "알레시아 공방전 · 기원전 52년"))
sc(1, {"type": "endcard", "title": "칸나이에서 쓰러진 모든 이들을 기억하며", "q": pin("site")}, tail=1.0)
assert CUR["i"] == len(ACTS[6]), (CUR, len(ACTS[6]))
SOMBER_FROM = [s["id"] for s in S if s.get("chapter", {}).get("num") == "제6막"][0]

# ===== 재연 일러스트 (countryball 반실사 + 일부 사실풍 풍경) — Cloudflare FLUX 무료 엔진 =====
CB = "Semi-realistic dramatic digital illustration in the style of polished history-YouTube countryball cartoons: "
CA = ("ancient Carthaginian soldiers whose heads are round balls painted deep navy blue with a small golden crescent-and-disc emblem, wearing bronze helmets and linen armor")
RO = ("ancient Roman legionaries whose heads are round balls painted crimson red with a small golden eagle emblem, wearing bronze helmets with tall plumes, mail shirts and large curved oval shields")
GA = "half-naked Gallic warriors whose heads are round balls painted forest green, with long swords and wooden shields"
HAN = ("a Carthaginian general whose head is a round ball painted deep navy blue with a golden crescent-and-disc emblem, with a short dark curly beard, "
       "wearing a crested bronze helmet, a bronze muscle cuirass and a dark red cloak")
PAU = "an old grey-haired Roman consul whose head is a round ball painted crimson red with a golden eagle emblem, wearing a bronze cuirass and a white toga-like cloak with a red border"
END = ", 216 BC ancient Mediterranean, leaving calm uncluttered dark background area in the upper right, absolutely no speech bubbles, no balloons, no text boxes, no captions, no text, no letters."
LAND_S = "painterly realistic digital illustration, cinematic, warm palette, film grain, no people's faces in close-up, no text, no letters."
AI = {
    "crushed": CB + RO + " packed shoulder to shoulder in a dense mass, trapped and unable to move, surrounded on all sides by " + CA + ", thick dust clouds at sunset, no blood" + END,
    "center_pushed": CB + RO + " in a deep formation pushing forward with shields, while " + GA + " step slowly backward in a curved line, dust in the air" + END,
    "oath": CB + "a small boy whose head is a round ball painted deep navy blue, placing his hand on a stone altar with a sacrificial fire, while his stern bearded father "
            "whose head is a round ball painted deep navy blue with a golden crescent emblem stands behind him in a dim Carthaginian temple" + END,
    "elephant_raft": CB + "war elephants standing on huge wooden rafts covered with earth being towed across a wide fast river by boats, " + CA + " rowing" + END,
    "trebia_ambush": CB + CA + " leaping out from tall reeds and bushes along a frozen winter riverbank to attack " + RO + " from behind, snow and sleet" + END,
    "trasimene_fog": CB + RO + " marching in a long column along a narrow lakeshore path in thick morning fog, while " + CA + " wait hidden on the hills above" + END,
    "oxen_torches": "A herd of oxen with burning bundles of branches tied to their horns running up a dark mountain slope at night, a line of flickering fires, ancient soldiers watching from a pass, " + LAND_S,
    "gisgo_laugh": CB + HAN + " laughing heartily on a low hill with his officers " + CA + ", looking at a vast Roman army in the distance across a flat plain" + END,
    "cavalry_river": CB + "heavy cavalry fighting in a chaotic tangled melee on a narrow strip of land beside a river, some riders dismounted fighting on foot, "
                     "Iberian and Gallic horsemen against " + RO + " on horses" + END,
    "africans_turn": CB + "African infantry whose heads are round balls painted deep navy blue, wearing captured Roman bronze helmets and mail and carrying Roman oval shields, "
                      "turning sideways together to attack the exposed flank of a dense Roman formation" + END,
    "hasdrubal_ride": CB + "a large mass of Carthaginian heavy cavalry whose heads are round balls painted deep navy blue galloping behind the back of a huge Roman infantry formation across a dusty plain" + END,
    "paullus_refuses": CB + PAU + " wounded and sitting on a rock on the battlefield, refusing with a raised hand as a young Roman officer whose head is a round ball painted crimson red offers him a horse, dust and chaos behind" + END,
    "maharbal": CB + "a Numidian cavalry commander whose head is a round ball painted dark navy blue, pointing urgently toward the horizon at night while " + HAN + " sits calmly in a tent lit by an oil lamp" + END,
    "varro_returns": CB + "a tired Roman consul whose head is a round ball painted crimson red arriving at a city gate, greeted respectfully by a crowd of Roman senators in white togas whose heads are round balls painted crimson red" + END,
    "thumb_bg": ("Cinematic photorealistic war painting, 16:9 wide shot from behind a huge Roman legion formation with red cloaks and oval shields, pushing into a curved enemy line on a dusty sunlit plain, "
                 "the enemy line bending backward like a crescent while enemy infantry and cavalry close in from both sides and behind, a river on the left, dramatic golden backlight, full color, high contrast, "
                 "the lower third of the frame darker, no text, no letters, no logos."),
}
used = {s["visual"]["img"] for s in S if s["visual"]["type"] == "ai"}
assert not used - set(AI), used - set(AI)
assert not set(AI) - used - {"thumb_bg"}, set(AI) - used
used = {s["visual"]["img"] for s in S if s["visual"]["type"] == "ai"}
assert not used - set(AI), used - set(AI)
assert not set(AI) - used - {"thumb_bg"}, set(AI) - used

# ===== 검사 =====
co = [s["visual"]["type"] for s in S if s["act"] == 1]
assert all(a != b for a, b in zip(co, co[1:])), co
for s in S:
    if s["visual"].get("q"):
        assert f"{s['visual']['q']}#0" in PINS, s["id"]
say = lambda l: l if isinstance(l, str) else l["say"]
disp = lambda l: l if isinstance(l, str) else l["t"]


def ons(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("on", "xOn", "checkOn", "sailOn", "runOn", "bendOn", "wrapOn", "untilOn") and isinstance(v, str):
                yield v
            else:
                yield from ons(v)
    elif isinstance(o, list):
        for v in o:
            yield from ons(v)


bad = []
for s in S:
    txt = " ".join(say(l) + " " + disp(l) for l in s["lines"])
    for w in ons({k: v for k, v in s.items() if k != "lines"}):
        if w not in txt:
            bad.append((s["id"], w))
assert not bad, bad


ids = [s["id"] for s in S]
chap = [i for i, s in enumerate(S) if s.get("chapter")]
sid = lambda i: S[i]["id"]
music = [{"id": "drone", "from": "s001", "to": sid(chap[0] - 1), "volume": 0.2},
         {"id": "theme", "from": sid(chap[0]), "to": sid(chap[1] - 1), "volume": 0.16},
         {"id": "analysis", "from": sid(chap[1]), "to": sid(chap[2] - 1), "volume": 0.16},
         {"id": "tension", "from": sid(chap[2]), "to": sid(chap[3] - 1), "volume": 0.17},
         {"id": "march", "from": sid(chap[3]), "to": sid(chap[4] - 1), "volume": 0.16},
         {"id": "somber", "from": sid(chap[4]), "to": sid(chap[5] - 1), "volume": 0.17},
         {"id": "analysis", "from": sid(chap[5]), "to": ids[-1], "volume": 0.16}]
assert SOMBER_FROM == sid(chap[4])
(HERE / "photo_pins.json").write_text(json.dumps(PINS, ensure_ascii=False, indent=1), encoding="utf-8")
# target_sec: 창욱 실측 초당 약 6.8자 → 약 8,250자 ≈ 20:13 + 장면 여백 (첫 미리보기 실측으로 갱신)
board = {"title": "일부러 밀렸다: 칸나이 전투", "subtitle": "가운데를 내주고 로마군 전체를 가둔 한니발 · 기원전 216년",
         "lang": "ko", "sub_max": 28, "voice": "ZJCNdZEjYwkOElxugmW2", "tempo": 1.02, "tts_mode": "act", "style": 2, "sfx_policy": "doc", "bgm_rel_db": -24, "sync_limit": 0.5,
         "target_sec": 1240, "midrolls": MID, "land": LAND, "places": P, "views": V, "music": music, "ai_images": AI, "scenes": S}
(HERE / "storyboard.json").write_text(json.dumps(board, ensure_ascii=False, indent=1), encoding="utf-8")
types = collections.Counter(s["visual"]["type"] for s in S)
print("scenes", len(S), "chars", sum(len(say(l)) for s in S for l in s["lines"]), "mid", MID, "chap", [sid(i) for i in chap],
      "ai", len(AI), "pins", len(PINS), dict(types))
