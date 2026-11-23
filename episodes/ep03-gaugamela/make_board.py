# EP03 (한국어 《격전의 세계사》) 가우가멜라 전투 (기원전 331) 스토리보드 생성기 — 첫 생성용(기록). 나레이션은 script.md 문장을 순서대로 그대로 가져온다.
# ⚠️ storyboard.json을 손으로 고친 뒤에는 다시 돌리지 말 것 (수정 사항이 덮어써짐)
# 연출 스타일 v2 + 롱폼 표준(막 단위 TTS·절제된 효과음·BGM -24dB·싱크 ±0.5초) + 초반 후킹 표준(hook {hud, neg, question} · troops)
# 막 번호: Act 1 = 콜드 오프닝(0~60초), Act 2~7 = 본편 → 장면 "act" 1~7 = act1.mp3~act7.mp3
# 전장: 지도 아이템 phalanx(마케도니아 파랑 · 페르시아 빨강) + zone(다리우스가 다져 놓은 평지) + swarm(기병·낫 전차)
# 래스터: 새 권역 neareast_sea(z6) · mesopotamia(z8) · nineveh(z11) · gaugamela_zoom(z14) (pipeline/geo.py RASTERS)
# 전장 좌표는 모식 배치 — 정확한 전장 위치는 학계에서도 미확정(텔 고멜 일대 설이 유력), 마케도니아군은 서쪽에서 동쪽을 보고 섰다고 가정
# 캐릭터 무대(stage)는 쓰지 않음 — 고대 마케도니아·페르시아 캐릭터 그림이 없어서(재연 일러스트로)
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
    ("기원전 삼백삼십일년 시월 일일", "기원전 331년 10월 1일"), ("기원전 삼백삼십일년 구월 이십일", "기원전 331년 9월 20일"), ("기원전 삼백삼십삼년 십일월", "기원전 333년 11월"),
    ("기원전 삼백삼십육년", "기원전 336년"), ("기원전 삼백삼십일년", "기원전 331년"), ("기원전 삼백삼십년", "기원전 330년"), ("기원전 이백십육년", "기원전 216년"),
    ("다리우스 삼세", "다리우스 3세"), ("필리포스 이세", "필리포스 2세"), ("약 사만칠천 명", "약 4만 7천 명"), ("사만 명에서 수십만 명", "4만 명에서 수십만 명"),
    ("보병 백만 명", "보병 100만 명"), ("기병 사만 명", "기병 4만 명"), ("오만에서 십만 명", "5만에서 10만 명"), ("백 명에서 오백 명", "100명에서 500명"),
    ("약 육십 명", "약 60명"), ("백 킬로미터", "100km"), ("전차 이백 대", "전차 200대"), ("무기 이백 대", "무기 200대"), ("코끼리 열다섯 마리", "코끼리 15마리"),
    ("은 만 탈란톤", "은 1만 탈란톤"), ("스물다섯 살", "25살"), ("서른두 살", "32살"), ("스무 살", "20살"), ("이백 년", "200년"), ("일곱 달", "7달"), ("두 달", "2달"),
    ("이 년 뒤", "2년 뒤"), ("열하루 뒤", "11일 뒤"), ("나흘 동안", "4일 동안"), ("세 가지", "3가지"),
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


# 사진: 위키미디어 공용 파일명을 웹 검색으로 확인한 것만 (2026-11-23)
PH = {
    "mosaic": ("File:Alexander Mosaic (6000 x 3730).jpg",
               "알렉산드로스 모자이크 · 폼페이 파우누스의 집 · 나폴리 국립고고학박물관 (이소스 또는 가우가멜라를 그린 것으로 봄)", ("알렉산드로스 모자이크", "로마 시대")),
    "darius_mosaic": ("File:Darius III mosaic.jpg",
                      "전차 위의 다리우스 3세 · 알렉산드로스 모자이크 부분 · 나폴리 국립고고학박물관", ("알렉산드로스 모자이크 부분", "로마 시대")),
    "darius_close": ("File:Darius close up.JPG",
                     "다리우스 3세 · 알렉산드로스 모자이크 부분 · 나폴리 국립고고학박물관", ("알렉산드로스 모자이크 부분", "로마 시대")),
    "brueghel": ("File:Battle of Gaugamela.jpg",
                 "이소스 전투 · 얀 브뤼헐 · 루브르 박물관 (예전에는 가우가멜라 전투로 알려짐)", ("얀 브뤼헐", "17세기 초")),
    "azara": ("File:Azara herm Louvre Ma436.jpg",
              "알렉산드로스 흉상 '아자라 헤르마' · 리시포스 원작의 로마 시대 복제품 · 루브르 박물관", ("알렉산드로스 흉상", "로마 시대 복제품")),
    "bust_ist": ("File:Bust of Alexander the Great.jpg",
                 "알렉산드로스 흉상 · 기원전 2세기 · 이스탄불 고고학박물관", ("알렉산드로스 흉상", "기원전 2세기")),
    "veronese": ("File:Paolo Veronese - The Family of Darius before Alexander - Google Art Project.jpg",
                 "알렉산드로스 앞의 다리우스 가족 · 파올로 베로네세 · 런던 내셔널 갤러리", ("파올로 베로네세", "1565년 무렵")),
    "diary": ("File:British Museum, Babylon Astronomical Diary, 331-330 BC.jpg",
              "가우가멜라 전투를 적은 바빌론 천문 일지 · 기원전 331~330년 · 대영박물관", ("바빌론 천문 일지", "기원전 331년")),
    "tablet": ("File:Clay tablet. Rev. Alexander's defeat of the last Achaemenid King Darius III at the battle of Gaugamela on Oct. 1, 331 BCE and its triumphant entry into Babylon. From Babylon, Iraq. British Museum.jpg",
               "다리우스 3세의 패배와 알렉산드로스의 바빌론 입성을 적은 점토판 뒷면 · 대영박물관", ("바빌론 점토판", "기원전 331년")),
    "lebrun": ("File:Charles le Brun - Bataille d'Arbélès (Louvre, INV 2895) Alexander and eagle.jpg",
               "아르벨라 전투의 알렉산드로스 · 샤를 르 브룅 부분 · 루브르 박물관", ("샤를 르 브룅", "1669")),
    "courtois": ("File:Jacques Courtois - Alexander the Great, victorious over Darius at the battle of Gaugamela.jpg",
                 "가우가멜라에서 다리우스를 이긴 알렉산드로스 · 자크 쿠르투아", ("자크 쿠르투아", "17세기")),
    "man_flight": ("File:Batalla de Gaugamela (M.A.N. Inv.1980-60-1) 02.jpg",
                   "달아나는 다리우스 · 가우가멜라 전투 부조 부분 · 스페인 국립고고학박물관 (르 브룅 그림을 본뜸)", ("가우가멜라 전투 부조", "18세기")),
    "persepolis": ("File:Persepolis Ruins.jpg",
                   "오늘날의 페르세폴리스 유적 · 이란", ("페르세폴리스", "오늘날")),
    "pellegrini": ("File:Giovanni Antonio Pellegrini - Alexander at the Corpse of the Dead Darius - Google Art Project.jpg",
                   "다리우스의 시신 앞의 알렉산드로스 · 조반니 안토니오 펠레그리니", ("조반니 안토니오 펠레그리니", "18세기")),
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
# 좌표: 도시·강은 개략, 전장(field)은 모식 배치
P = {
    "pella": [22.52, 40.76, "펠라"], "hellespont": [26.41, 40.2, "헬레스폰토스"], "granicus": [27.3, 40.25, "그라니코스강"],
    "issus": [36.2, 36.85, "이소스"], "tyre": [35.2, 33.27, "티로스"], "gaza": [34.45, 31.5, "가자"], "memphis": [31.25, 29.85, "멤피스"],
    "alexandria": [29.92, 31.2, "알렉산드리아"], "siwa": [25.52, 29.2, "시와 오아시스"], "thapsacus": [38.45, 35.95, "탑사코스 (추정)"],
    "babylon": [44.42, 32.54, "바빌론"], "susa": [48.25, 32.19, "수사"], "persepolis": [52.89, 29.935, "페르세폴리스"], "ecbatana": [48.51, 34.8, "엑바타나"],
    "darius_death": [54.3, 36.17, "다리우스가 숨진 곳 (추정)"], "nineveh": [43.15, 36.36, "니네베 · 오늘날 모술"], "arbela": [44.01, 36.19, "아르벨라 · 오늘날 에르빌"],
    "gaugamela": [43.494, 36.573, "가우가멜라 (텔 고멜 설)"], "crossing": [42.98, 36.66, "티그리스 도하 (추정)"],
    # --- 전장 (모식) ---
    "darius": [43.493, 36.525, "다리우스 · 근위대"], "gap": [43.489, 36.503, "틈"], "bessus": [43.49, 36.472, "베소스 · 박트리아 기병"],
    "mazaeus": [43.49, 36.578, "마자이오스"], "parm": [43.44, 36.552, "파르메니온 · 테살리아 기병"], "alex": [43.44, 36.498, "알렉산드로스 · 친위 기병대"],
    "mcamp": [43.41, 36.525, "마케도니아 진영"], "pcamp": [43.51, 36.53, "페르시아 진영"], "edge": [43.468, 36.488, "다져 놓은 땅 끝"],
}
V = {
    "empire": {"center": [38.5, 36.3], "span": 34.0}, "levant": {"center": [33.0, 33.3], "span": 16.0}, "meso": {"center": [41.6, 34.6], "span": 12.0},
    "nineveh": {"center": [43.55, 36.4], "span": 1.5}, "field": {"center": [43.462, 36.516], "span": 0.2}, "iran": {"center": [48.0, 33.2], "span": 16.0},
}
LAND = {"home": ["368"], "foreign": ["300", "792", "760", "364", "422", "376", "400", "818", "414", "682", "196", "100", "807", "8", "51", "31", "268", "275", "4", "795"]}

# --- 강 (개략) ---
TIGRIS = [[42.2, 37.3], [42.7, 36.95], [43.13, 36.36], [43.3, 35.7], [43.8, 34.9], [44.4, 33.3], [45.5, 32.5], [47.0, 31.0]]
EUPHRATES = [[38.0, 36.9], [38.3, 36.3], [39.0, 35.95], [40.1, 35.3], [40.9, 34.5], [41.9, 34.3], [43.0, 33.4], [44.3, 32.5], [46.0, 31.0]]
RIV = lambda path, at=0: {"k": "line", "path": path, "color": "#5aa0d8", "glow": False, "at": at}
# --- 원정로 (개략) ---
TO_ASIA = [[22.52, 40.76], [24.5, 40.9], [26.41, 40.2], [27.3, 40.25]]
TO_ISSUS = [[27.3, 40.25], [30.5, 38.5], [33.5, 37.0], [36.2, 36.85]]
COAST = [[36.2, 36.85], [35.9, 35.5], [35.6, 34.4], [35.2, 33.27]]
TO_EGYPT = [[35.2, 33.27], [34.45, 31.5], [32.3, 30.9], [31.25, 29.85]]
NORTH = [[29.92, 31.2], [34.3, 31.6], [35.2, 33.27], [36.4, 35.3], [38.45, 35.95]]
DARIUS_EAST = [[36.2, 36.85], [38.5, 36.4], [41.0, 34.5], [44.42, 32.54]]
NORTH_ROUTE = [[38.45, 35.95], [39.6, 36.6], [41.3, 37.0], [42.98, 36.66]]
SOUTH_DIRECT = [[38.45, 35.95], [40.5, 34.8], [42.6, 33.6], [44.42, 32.54]]
D_TO_GAUG = [[44.42, 32.54], [44.2, 34.0], [43.9, 35.5], [43.494, 36.55]]
CROSS = [[42.85, 36.7], [43.05, 36.63]]
TO_FIELD = [[43.05, 36.63], [43.25, 36.56], [43.42, 36.52]]
TO_ARBELA = [[43.5, 36.52], [43.7, 36.38], [44.01, 36.19]]
D_FLEE_E = [[44.01, 36.19], [46.0, 35.3], [48.51, 34.8]]
D_LAST = [[48.51, 34.8], [51.0, 35.6], [54.3, 36.17]]
A_CHASE = [[44.42, 32.54], [48.25, 32.19], [52.89, 29.935], [50.5, 33.5], [48.51, 34.8], [51.5, 35.7], [54.3, 36.17]]

# --- 전장 기하 (모식 · 마케도니아는 서쪽에서 동쪽을 본다 → 오른쪽 = 남쪽) ---
G_LINE = [[43.44, 36.556], [43.44, 36.497]]       # 마케도니아 앞줄: 왼쪽(북, 파르메니온) → 오른쪽(남, 알렉산드로스) · 정면 = 동쪽(face -1)
G_LINE2 = [[43.43, 36.553], [43.43, 36.5]]        # 두 번째 줄
G_SHIFT = [[43.447, 36.537], [43.449, 36.476]]    # 오른쪽으로 비켜 걸은 뒤
P_LINE = [[43.49, 36.588], [43.49, 36.47]]        # 페르시아 전열: 북(마자이오스) → 남(베소스) · 정면 = 서쪽(face 1)
P_STRETCH = [[43.49, 36.588], [43.486, 36.452]]   # 왼쪽으로 늘어난 전열
G_EVEN = [7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
G_THIN = [3, 3, 3, 3, 3, 3, 3, 3]
P_DEEP = [5, 6, 7, 8, 9, 9, 8, 7, 6, 5]
P_GAP = [5, 6, 7, 8, 9, 2, 0.4, 2, 6, 5]           # 가운데 아래쪽에 틈
LEVEL = [[43.452, 36.567], [43.484, 36.567], [43.484, 36.49], [43.452, 36.49]]   # 다져 놓은 평지
CHARIOTS = [[43.484, 36.522], [43.465, 36.517], [43.447, 36.513]]
BESSUS_RIDE = [[43.488, 36.468], [43.472, 36.452], [43.452, 36.458]]
ENCIRCLE = [[43.488, 36.468], [43.46, 36.447], [43.43, 36.46], [43.418, 36.49]]
FLANK = [[43.449, 36.476], [43.437, 36.468]]
WEDGE = [[43.449, 36.478], [43.466, 36.49], [43.482, 36.5], [43.494, 36.521]]
D_FLEE = [[43.495, 36.525], [43.525, 36.51], [43.56, 36.49]]
MAZAEUS = [[43.49, 36.58], [43.466, 36.572], [43.446, 36.562]]
RAID = [[43.488, 36.54], [43.445, 36.53], [43.413, 36.526]]
BACK_LINE = [[43.43, 36.53], [43.42, 36.528]]
RETURN = [[43.494, 36.522], [43.475, 36.545], [43.452, 36.558]]
MAZ_BACK = [[43.452, 36.565], [43.48, 36.578], [43.51, 36.59]]

# 2026-11-23 미리보기 뒤 수정: 전장이 남북으로 너무 길어 화면(기울인 지도) 밖으로 잘림 → 위도를 중심(36.517) 기준 0.45배로 눌러 한 화면에
_SQ = lambda q: [q[0], round(36.517 + (q[1] - 36.517) * 0.45, 5)]
for _n in ("G_LINE", "G_LINE2", "G_SHIFT", "P_LINE", "P_STRETCH", "LEVEL", "CHARIOTS", "BESSUS_RIDE", "ENCIRCLE", "FLANK", "WEDGE", "D_FLEE", "MAZAEUS", "RAID", "BACK_LINE", "RETURN", "MAZ_BACK"):
    globals()[_n] = [_SQ(q) for q in globals()[_n]]
for _k in ("darius", "gap", "bessus", "mazaeus", "parm", "alex", "mcamp", "pcamp", "edge"):
    P[_k] = _SQ(P[_k][:2]) + [P[_k][2]]
FP = lambda *pts: [_SQ(list(q)) for q in pts]   # 장면 안에 직접 적은 전장 좌표용

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
GPH = lambda at=0, path=G_LINE, depth=G_EVEN, **kw: dict({"k": "phalanx", "path": path, "depth": depth, "face": -1, "px": 5.5, "color": "blue", "at": at}, **kw)
GPH2 = lambda at=0, **kw: GPH(at, G_LINE2, G_THIN, **kw)
GPHS = lambda at=0, **kw: GPH(at, G_SHIFT, G_EVEN, **kw)
PPH = lambda at=0, path=P_LINE, depth=P_DEEP, **kw: dict({"k": "phalanx", "path": path, "depth": depth, "face": 1, "px": 5.5, "color": "red", "at": at}, **kw)
PPHS = lambda at=0, depth=P_DEEP, **kw: PPH(at, P_STRETCH, depth, **kw)
top = lambda t, s="yellow", at=0: [{"text": t, "style": s, "at": at, "pos": "top"}]
low = lambda t, s="dark", at=0: [{"text": t, "style": s, "at": at, "pos": "lower"}]
SW = lambda at=0: [{"id": "whoosh", "at": at}]
PING = lambda at=0.6: [{"id": "ping", "at": at}]
WIND = lambda at=0: [{"id": "wind", "at": at}]
FAR = lambda at=0: [{"id": "artillery_far", "at": at, "db": -32}]
HUD = lambda big, sub=None, sub2=None, at=0.0, color=None, count=None, on=None: dict({"big": big}, **({"sub": sub} if sub else {}), **({"sub2": sub2} if sub2 else {}),
                                                                                      **({"on": on} if on else {"at": at}), **({"color": color} if color else {}), **({"count": count} if count is not None else {}))
QUESTION = "적이 직접 골라 다진 전장에서\n알렉산드로스는 왜\n오른쪽으로 비켜 걸었을까"

# ===== 제1막 · 콜드 오프닝 (0~10초 사건 직격 → 모순 3단 → X 반전 → 중앙 질문 카드 → 타이틀) =====
# 레이어 교차: 3D 비행 → 사료(모자이크) → 3D 평지·전차 → 병력 대열 → 재연 그림 → 3D 비켜 걷기 → 재연 그림 → X → 지도+질문 카드 → 타이틀
sc(2, m("empire", "field", [LOCK("gaugamela", 1.0, "가우가멜라 평원")], flight=["empire", "meso", "nineveh", "field"], flightDur=4.6, hud=True, tilt=26),
   hook={"hud": [HUD("기원전 331년 10월 1일", "가우가멜라 평원", "지금의 이라크 북부", count=False)]}, sfx=SW(0) + PING(1.4))
sc(1, ph("darius_close", pos="50% 35%", marks=[mk("페르시아 대왕 다리우스 3세", 0.5, 0.15, "다리우스")]), label=plabel("darius_close"))
sc(2, m("field", "field", [zone(LEVEL, "다져 놓은 평지", on="평평하게"), PPH(0), swarm(CHARIOTS, 0, 90, 0.5)], tilt=32, hud=True),
   hook={"hud": [HUD("200대", "낫을 단 전차", "아리아노스", on="이백", count=False)]})
sc(2, ranks([5] * 10, [8] * 16),
   hook={"hud": [HUD("약 4만 7천", "알렉산드로스의 군대", "보병 4만 · 기병 7천 · 아리아노스", on="사만칠천", count=False),
                 HUD("5만~10만+", "다리우스의 군대", "현대 추정", color="#FF3B30", on="훨씬", count=False)]})
sc(1, ai("darius_flees"), label=DRAMA, hook={"hud": [HUD("먼저 도망친 쪽", "대왕 다리우스", "해가 지기 전", count=False, on="등을")]})
sc(3, m("field", "field", [zone(LEVEL, "다리우스가 고른 땅"), PPH(0), GPH(0), blue_a([[43.44, 36.50935], [43.445, 36.5026], [43.449, 36.49585]], on="오른쪽으로", w=1.2)], tilt=30),
   sfx=PING(2.2))
sc(2, ai("chariot_lanes"), label=DRAMA, hook={"hud": [HUD("거의 0", "낫 전차가 부순 대열", "아리아노스", color="#FF3B30", on="거의", count=False)]})
sc(2, black("무모한 돌격?", "운이었을까"), hook={"neg": {"text": "운 좋은 돌격", "on": "무모한", "xOn": "그랬을까요"}})
sc(1, m("field", "field", [zone(LEVEL), PPH(0), GPH(0)], tilt=30), hook={"question": {"text": QUESTION, "at": 0.02}})
sc(1, {"type": "titlecard", "title": "단 한 번의 돌격", "sub": "가우가멜라 전투 · 기원전 331년", "at": 0, "q": pin("courtois")}, flash=True)
next_act()

# ===== 제2막 · 달아난 대왕 =====
sc(2, m("empire", "levant", [LOCK("issus", on="이소스")], flight=["empire", "levant"], flightDur=2.6, tilt=16), chapter={"num": "제2막", "title": "달아난 대왕"},
   callouts=top("기원전 333년 11월 · 이소스"), sfx=SW(0) + PING(1.6))
sc(1, ph("brueghel", pos="50% 45%", marks=[mk("산과 바다 사이 좁은 들판", 0.5, 0.15, "좁은")]), label=plabel("brueghel"))
sc(2, text("같은 해 왕이 된 두 사람", "yellow", "기원전 336년"))
sc(1, ph("azara", pos="50% 25%", marks=[mk("알렉산드로스 · 20살", 0.5, 0.12, "스무")]), label=plabel("azara"))
sc(1, ph("darius_mosaic", pos="50% 35%", marks=[mk("다리우스 3세", 0.5, 0.12, "다리우스")]), label=plabel("darius_mosaic"))
sc(2, m("empire", "empire", [mark("pella", "blue", 0), blue_a(TO_ASIA, on="헬레스폰토스"), LOCK("granicus", on="그라니코스강")], tilt=12), callouts=top("기원전 334년 · 아시아로", "blue"))
sc(1, black("이제", "대왕이 직접"))
sc(2, m("levant", "levant", [blue_a(TO_ISSUS, 0.2), LOCK("issus", 0.6), badge("issus", "좁은 들판", "#c9242c", on="좁은", dy=-80)], tilt=16))
sc(2, ai("issus_flight"), label=DRAMA)
sc(1, ph("veronese", pos="50% 50%", marks=[mk("대왕의 가족", 0.5, 0.15, "어머니와")]), label=plabel("veronese"))
sc(1, text("왕족의 대접", "blue", "붙잡힌 대왕의 어머니·아내·딸들"))
sc(2, ai("sisygambis_bow"), label=DRAMA, callouts=top("대왕의 어머니 시시감비스"))
sc(2, text("“그도 알렉산드로스입니다”", "yellow", "쿠르티우스·아리아노스가 전하는 이야기"))
sc(1, ph("mosaic", pos="50% 50%", marks=[mk("폼페이 · 파우누스의 집", 0.5, 0.12, "폼페이의")]), label=plabel("mosaic"))
sc(1, ph("mosaic", pos="18% 45%", marks=[mk("알렉산드로스", 0.3, 0.15, "젊은 왕")]), label=plabel("mosaic"))
sc(2, ph("darius_close", pos="50% 40%", marks=[mk("손을 뻗은 대왕", 0.5, 0.15, "손을")]), label=plabel("darius_close"))
sc(1, m("levant", "levant", [mark("issus", "blue", 0), dash_r(DARIUS_EAST, 0.2), LOCK("babylon", 0.9, "대왕은 동쪽으로")], tilt=14))
sc(2, m("levant", "levant", [blue_a(COAST, 0.2), badge("tyre", "항구 빼앗기", "#1f5fbf", on="항구를", dy=-80)], tilt=16), callouts=top("페르시아 함대의 항구를 하나씩", "blue"))
sc(2, ai("tyre_causeway"), label=DRAMA, callouts=top("섬 도시 티로스 · 7달"))
sc(1, ai("darius_letter"), label=DRAMA)
sc(3, doc("다리우스의 제안", ["유프라테스강 서쪽 땅 전부", "은 1만 탈란톤", "대왕의 딸과 혼인"], "제안", "아리아노스 2권 25절"))
sc(2, text("“제가 알렉산드로스라면”", "dark", "늙은 장군 파르메니온"))
sc(3, text("“나도 파르메니온이라면”", "yellow", "알렉산드로스의 대답 · 아리아노스 2권 25절"))
sc(2, m("levant", "levant", [blue_a(TO_EGYPT, 0.2), LOCK("gaza", on="가자도"), mark("memphis", "blue", on="이집트에")], tilt=16), sfx=PING(0.9))
sc(2, {"type": "flatmap", "center": [29.0, 30.4], "span": 9.5, "fill": {"818": "#f1e4c6"},
       "pins": [{"ll": [31.25, 29.85], "text": "멤피스", "side": "right", "at": 0}, {"ll": [25.52, 29.2], "text": "시와 오아시스", "side": "below", "on": "시와"}],
       "routes": [{"from": [31.25, 29.85], "to": [25.52, 29.2], "bend": -0.2, "dur": 1.4, "label": "사막을 건너", "on": "사막"}], "labels": [], "zoomTo": 0.94})
sc(2, m("levant", "levant", [LOCK("alexandria", on="새 도시를")], tilt=16), callouts=top("기원전 331년 · 알렉산드리아"))
sc(1, text("지중해의 항구", "blue", "모두 마케도니아의 손에"))
sc(2, m("levant", "meso", [blue_a(NORTH, 0.2, 1.1), LOCK("babylon", text="목표 · 바빌론", on="바빌론이었습니다")], flight=["levant", "meso"], flightDur=2.4, tilt=14), sfx=SW(0))
sc(2, black("이번에는", "도망치지 않는다"))
next_act()

# ===== 제3막 · 대왕이 고른 땅 =====
MID = [nid()]
sc(1, m("meso", "meso", [LOCK("babylon", 0.4)], tilt=14), pauseBefore=0.5, chapter={"num": "제3막", "title": "대왕이 고른 땅"})
sc(3, reasons("대왕이 불러 모은 군대", [{"text": "박트리아 기병", "on": "박트리아의"}, {"text": "초원의 기마 궁수", "on": "기마 궁수"}, {"text": "인도 코끼리 15마리", "on": "코끼리"}]))
sc(1, ai("scythe_chariot"), label=DRAMA, callouts=top("낫 전차 200대", "red"))
sc(3, bars("다리우스의 군대", [{"label": "아리아노스", "value": 1040000, "display": "보병 100만 + 기병 4만", "color": "red", "on": "백만"},
                            {"label": "현대 추정", "value": 100000, "display": "5만~10만 이상", "color": "dark", "on": "오만에서"}]))
sc(3, text("더 긴 창과 칼", "red", "디오도로스 17권 53절"))
sc(3, cmp("이소스", "좁은 땅", "이번에는", "넓은 평원", "red", "blue"))
sc(2, m("meso", "nineveh", [RIV(TIGRIS), LOCK("gaugamela", on="가우가멜라"), red_a(D_TO_GAUG, on="바빌론에서")], flight=["meso", "nineveh"], flightDur=2.4, tilt=20), sfx=SW(0))
sc(1, text("낙타의 집", "yellow", "가우가멜라라는 이름의 뜻"))
sc(3, ai("leveling"), label=DRAMA, callouts=top("평원을 더 평평하게"))
sc(2, text("낫 전차", "red", "대열째 베어 버리는 무기"))
sc(3, checklist("낫 전차의 조건", [{"text": "평평한 땅", "on": "평평해야"}, {"text": "돌 하나도 안 된다", "on": "돌 하나"}, {"text": "도랑 하나도 안 된다", "on": "도랑"}]))
sc(3, m("field", "field", [zone(LEVEL, "다져 놓은 평지", 0.2), PPH(0), swarm(CHARIOTS, 0.4, 90, 0.5)], tilt=32, hud=True), callouts=low("“여기서만 싸우면 된다”", "red", 1.5))
sc(4, m("meso", "meso", [RIV(TIGRIS), RIV(EUPHRATES), LOCK("thapsacus", on="탑사코스에서"), dash_b(SOUTH_DIRECT, on="곧장"), blue_a(NORTH_ROUTE, on="북쪽으로", w=1.1)], tilt=14),
   callouts=top("남쪽 길: 더위 · 말 먹이 부족", "red", 3.0))
sc(2, text("마자이오스", "red", "앞서 나가 마을과 곡식을 불태우다"))
sc(2, ai("tigris_crossing"), label=DRAMA, callouts=top("티그리스강 도하"))
sc(2, m("nineveh", "nineveh", [RIV(TIGRIS), blue_a(CROSS, 0.1), LOCK("crossing", 0.4), mark("gaugamela", "red", on="평원으로")], tilt=20), sfx=PING(0.8))
sc(3, ai("eclipse"), label=DRAMA, callouts=top("기원전 331년 9월 20일 밤"), sfx=WIND(0))
sc(2, ph("diary", pos="50% 50%", marks=[mk("월식 · 서쪽 바람", 0.5, 0.15, "월식이")]), label=plabel("diary"))
sc(1, black("달이 사라졌다", "병사들의 공포"))
sc(2, text("달 · 해 · 땅에 제물", "yellow", "알렉산드로스 · 아리아노스 3권 7절"))
sc(1, m("nineveh", "nineveh", [RIV(TIGRIS), blue_a(TO_FIELD, 0.1), mark("gaugamela", "red", 0.5)], tilt=20), callouts=top("열하루 뒤"))
next_act()

# ===== 제4막 · 훔치지 않는 승리 =====
sc(2, m("nineveh", "field", [unit("mcamp", "마케도니아 진영", "blue", 0.6, pulse=True)], flight=["nineveh", "field"], flightDur=2.4, tilt=26),
   chapter={"num": "제4막", "title": "훔치지 않는 승리"}, callouts=top("나흘 휴식"), sfx=SW(0))
sc(1, ai("alex_ridge"), label=DRAMA)
sc(2, text("왕비 스타테이라의 죽음", "dark", "포로로 지내던 중 · 플루타르코스"))
sc(1, ph("veronese", pos="30% 50%"), label=plabel("veronese"))
sc(2, doc("다리우스의 기도", ["페르시아의 운이 다했다면", "내 왕좌에는 알렉산드로스만"], "기도", "플루타르코스 『알렉산드로스 전』 30장"))
sc(2, ai("night_council"), label=DRAMA, callouts=top("밤의 작전 회의"))
sc(2, doc("파르메니온의 조언", ["지금 밤에 치자", "적은 우리 숫자를 모른다", "대군은 어둠 속에서 엉킨다"], "야습", "아리아노스 3권 10절"))
sc(1, black("그럴듯한", "제안"))
sc(2, text("“나는 승리를 훔치지 않겠다”", "yellow", "알렉산드로스 · 아리아노스·플루타르코스"))
sc(2, black("허세?", "아니면 계산"))
sc(4, reasons("밤에 싸우지 않은 이유", [{"text": "다리우스에게 남을 핑계", "on": "어둠과"}, {"text": "다시 모여들 군대", "on": "다시 동쪽에서"}, {"text": "아군끼리의 혼란", "on": "아군도"}]))
sc(2, text("핑계 없는 승리", "blue", "대왕이 고른 땅 · 대낮 · 정면"))
sc(2, m("field", "field", [PPH(0), zone(LEVEL, None, at=0), badge("darius", "밤새 무장", "#c9242c", on="밤새", dy=-80)], tilt=30, hud=True))
sc(2, ai("persians_awake"), label=DRAMA, sfx=WIND(0))
sc(2, ai("alex_sleeps"), label=DRAMA)
sc(3, text("“우리는 이미 이겼다”", "yellow", "플루타르코스 『알렉산드로스 전』 32장"))
sc(3, m("field", "field", [GPH(0), GPH2(on="두 번째 줄")], tilt=32), callouts=top("두 겹의 대열", "blue"))
sc(3, m("field", "field", [GPH(0), GPH2(0), line([[43.44, 36.53455], [43.43, 36.53905]], on="비스듬히", color="#6fb3ff"), line([[43.44, 36.508], [43.43, 36.5035]], on="비스듬히", color="#6fb3ff")], tilt=32),
   callouts=low("뒤로 꺾은 양쪽 끝", "dark", 1.0))
sc(1, cmp("마케도니아 전열", "짧다", "페르시아 전열", "훨씬 길다", "blue", "red"))
sc(2, text("네모난 상자", "blue", "어디로 돌아와도 막는다"))
sc(3, m("field", "field", [GPH(0), GPH2(0), badge("parm", "파르메니온 · 테살리아 기병", "#1f5fbf", on="파르메니온과", dy=-70),
                           badge("alex", "알렉산드로스 · 친위 기병대", "#1f5fbf", on="친위", dy=70)], tilt=30), callouts=top("가운데 · 사리사 밀집 보병", "blue"))
sc(1, m("field", "field", [GPH(0), PPH(0), LOCK("darius", on="대왕의")], tilt=30), sfx=PING(0.8))
sc(4, m("field", "field", [PPH(0), badge("bessus", "베소스 · 박트리아", "#c9242c", on="베소스", dy=70), badge("mazaeus", "마자이오스", "#c9242c", on="마자이오스", dy=-70),
                           badge("darius", "근위대 · 그리스인 용병", "#c9242c", on="근위대와", dy=-80), swarm(CHARIOTS, 0, 80, 0.5)], tilt=30))
sc(1, ph("mosaic", pos="18% 45%", marks=[mk("부케팔로스", 0.3, 0.75, "부케팔로스를")]), label=plabel("mosaic"))
next_act()

# ===== 제5막 · 오른쪽으로 =====
MID.append(nid())
sc(2, m("field", "field", [GPH(0), PPH(0), zone(LEVEL, None, 0)], tilt=32, hud=True), pauseBefore=0.5, chapter={"num": "제5막", "title": "오른쪽으로"},
   callouts=top("기원전 331년 10월 1일 아침"), sfx=SW(0))
sc(1, ai("plain_dawn"), label=DRAMA, sfx=WIND(0))
sc(2, m("field", "field", [GPH(0), PPH(0), badge("bessus", "더 오른쪽까지", "#c9242c", on="뻗어", dy=70)], tilt=30))
sc(3, m("field", "field", [zone(LEVEL, None, 0), PPH(0), GPHS(on="미끄러지듯"), blue_a([[43.44, 36.50935], [43.445, 36.5035], [43.449, 36.49765]], on="오른쪽으로", w=1.2)], tilt=30),
   sfx=PING(1.2))
sc(2, text("“저대로 가면?”", "red", "당황한 페르시아 장군들"))
sc(3, m("field", "field", [zone(LEVEL, "다져 놓은 평지", 0), PPH(0), GPHS(0), badge("edge", "땅 끝", "#111", on="바깥으로", dy=60)], tilt=32))
sc(2, m("field", "field", [zone(LEVEL, None, 0), GPHS(0), PPHS(on="늘어지기"), red_a([[43.49, 36.50035], [43.488, 36.4936], [43.486, 36.48775]], on="늘어지기")], tilt=30))
sc(2, black("시간 문제", "전차의 땅이 끝난다"))
sc(2, text("“돌아 나가서 앞을 막아라”", "red", "다리우스의 명령"))
sc(1, m("field", "field", [GPHS(0), PPHS(0), swarm(BESSUS_RIDE, 0.1, 140, 0.5)], tilt=30), sfx=FAR(0))
sc(2, m("field", "field", [GPHS(0), PPHS(0), dash_r(ENCIRCLE, on="뒤로"), badge("mcamp", "포위?", "#c9242c", on="갇히게", dy=-70)], tilt=30))
sc(2, m("field", "field", [GPHS(0), line(FLANK, on="꺾어", color="#6fb3ff"), swarm(BESSUS_RIDE, 0, 140, 0.5), clash([43.44, 36.49315], on="받아")], tilt=32), sfx=PING(1.6))
sc(1, ph("bust_ist", pos="50% 25%"), label=plabel("bust_ist"))
sc(4, checklist("조금씩 아껴 내보낸 기병", [{"text": "용병 기병 한 무리", "on": "먼저"}, {"text": "밀리면 또 한 무리", "on": "또 한"}, {"text": "적 기병을 붙잡아 두다", "on": "붙잡아"}]))
sc(1, m("field", "field", [GPHS(0), PPHS(0), swarm(BESSUS_RIDE, 0, 200, 0.6), red_a([[43.49, 36.50935], [43.482, 36.4981], [43.466, 36.49045]], on="몰려갔죠")], tilt=30))
sc(2, black("비장의 무기", "낫 전차"))
sc(2, m("field", "field", [GPHS(0), PPHS(0), swarm(CHARIOTS, 0, 110, 0.55), red_a(CHARIOTS, on="달려듭니다", w=1.2)], tilt=32, hud=True),
   hook={"hud": [HUD("200대", "낫 전차 돌격", "아리아노스 3권 13절", on="낫 전차", count=False)]})
sc(3, ai("javelin_chariot"), label=DRAMA, callouts=top("투창병 · 궁수"))
sc(3, ai("chariot_lanes"), label=DRAMA, callouts=low("좌우로 갈라선 대열", "dark", 1.5))
sc(2, m("field", "field", [GPHS(0), dash_r([[43.449, 36.51475], [43.43, 36.5143], [43.415, 36.51385]], 0.2), badge([43.449, 36.51475], "열린 길", "#1f5fbf", 0.4, -70)], tilt=32))
sc(1, bars("낫 전차 200대", [{"label": "돌격한 전차", "value": 200, "display": "200대", "color": "red", "at": 0},
                          {"label": "대열을 부순 전차", "value": 4, "display": "거의 없음", "color": "blue", "on": "거의"}]))
sc(2, text("코끼리 15마리", "dark", "싸움에 나섰다는 기록조차 없다"))
sc(3, m("field", "field", [GPHS(0), PPHS(0, depth=P_GAP), red_a([[43.49, 36.50935], [43.482, 36.4981], [43.466, 36.49045]], 0.2), LOCK("gap", on="틈이")], tilt=32, hud=True), sfx=PING(2.4))
next_act()

# ===== 제6막 · 틈 =====
MID.append(nid())
sc(2, m("field", "field", [GPHS(0), PPHS(0, depth=P_GAP), LOCK("gap", 0.3)], tilt=32), pauseBefore=0.5, chapter={"num": "제6막", "title": "틈"}, sfx=SW(0))
sc(3, ai("wedge_charge"), label=DRAMA, callouts=top("친위 기병대의 쐐기", "blue"))
sc(1, text("쐐기", "blue", "앞은 좁게 · 뒤로 갈수록 넓게"))
sc(2, m("field", "field", [GPHS(0), PPHS(0, depth=P_GAP), blue_a(WEDGE, on="곧장", w=1.4)], tilt=34, hud=True), sfx=FAR(0))
sc(2, ph("darius_mosaic", pos="50% 35%", marks=[mk("전차 위의 다리우스", 0.5, 0.12, "전차 위의")]), label=plabel("darius_mosaic"))
sc(1, m("field", "field", [PPHS(0, depth=P_GAP), blue_a(WEDGE, 0), LOCK("darius", on="대왕")], tilt=34), sfx=PING(1.0))
sc(2, ph("lebrun", pos="50% 40%"), label=plabel("lebrun"), sfx=WIND(0))
sc(2, ai("darius_flees"), label=DRAMA)
sc(2, ph("man_flight", pos="50% 45%", marks=[mk("가장 먼저 달아난 대왕 · 아리아노스", 0.5, 0.12, "가장 먼저")]), label=plabel("man_flight"))
sc(1, m("field", "field", [PPHS(0, depth=P_GAP), dash_r(D_FLEE, 0.1), clash("darius", 0.3)], tilt=32))
sc(2, text("급한 전갈", "red", "왼쪽 날개 · 파르메니온"))
sc(2, m("field", "field", [GPHS(0), red_a(MAZAEUS, on="마자이오스가", w=1.2), clash("parm", on="밀어붙이고"), badge("parm", "테살리아 기병", "#1f5fbf", on="테살리아", dy=-70)], tilt=30))
sc(2, m("field", "field", [GPHS(0), red_a(RAID, on="뚫고"), badge([43.447, 36.52285], "보병 대열의 틈", "#c9242c", on="틈이", dy=-70), unit("mcamp", "진영", "blue", 0.2)], tilt=30))
sc(2, ai("camp_raid"), label=DRAMA, callouts=top("다리우스의 어머니 시시감비스"))
sc(1, m("field", "field", [GPH2(0), blue_a(BACK_LINE, on="돌아서서"), clash("mcamp", on="몰아냈습니다")], tilt=30))
sc(3, cmp("쫓을 것인가", "달아나는 대왕", "구할 것인가", "무너지는 왼쪽", "red", "blue"))
sc(1, black("그는", "말을 돌렸다"))
sc(2, text("파르메니온 탓?", "dark", "훗날의 논란 · 플루타르코스"))
sc(2, m("field", "field", [blue_a(RETURN, 0.1, 1.2), clash([43.475, 36.5296], on="부딪힙니다", size=1.3)], tilt=32, hud=True), sfx=FAR(0))
sc(1, text("친위 기병 약 60명 전사", "red", "헤파이스티온 부상 · 아리아노스 3권 15절"))
sc(2, m("field", "field", [GPHS(0), dash_r(MAZ_BACK, on="물러났거든요")], tilt=30))
sc(1, ph("courtois", pos="50% 50%"), label=plabel("courtois"))
sc(3, m("field", "nineveh", [blue_a(TO_ARBELA, 0.3, 1.1), LOCK("arbela", on="아르벨라에"), badge("arbela", "대왕의 전차 · 활 · 보물", "#111", on="보물이", dy=80)],
        flight=["field", "nineveh"], flightDur=2.4, tilt=20), sfx=SW(0))
sc(2, bars("페르시아군 전사자 · 옛 기록", [{"label": "아리아노스", "value": 300000, "display": "30만", "color": "red", "at": 0.2},
                                    {"label": "디오도로스", "value": 90000, "display": "9만", "color": "red", "at": 0.5},
                                    {"label": "쿠르티우스", "value": 40000, "display": "4만", "color": "red", "on": "사만"}]))
sc(1, text("마케도니아 전사자", "blue", "기록에 따라 100~500명"))
next_act()

# ===== 제7막 · 답 =====
sc(1, m("nineveh", "meso", [RIV(TIGRIS), RIV(EUPHRATES), LOCK("babylon", 0.8, "바빌론 · 성문을 열다")], flight=["nineveh", "meso"], flightDur=2.4, tilt=14),
   pauseBefore=0.5, chapter={"num": "제7막", "title": "답"}, sfx=SW(0))
sc(3, ph("tablet", pos="50% 50%", marks=[mk("“왕은 군대에게 버림받았다”", 0.5, 0.14, "버림받았다")]), label=plabel("tablet"))
sc(2, ph("persepolis", pos="50% 55%"), label=plabel("persepolis"))
sc(2, m("iran", "iran", [red_a(D_FLEE_E, on="엑바타나로"), LOCK("ecbatana", on="엑바타나로")], tilt=12))
sc(3, m("iran", "iran", [dash_b(A_CHASE, 0.1), red_a(D_LAST, 0.3), LOCK("darius_death", on="붙잡습니다"), badge("darius_death", "베소스", "#c9242c", on="베소스가", dy=-80)], tilt=12),
   callouts=top("기원전 330년 여름", "red"), sfx=PING(1.6))
sc(3, ph("pellegrini", pos="50% 50%"), label=plabel("pellegrini"))
sc(1, text("200년 넘은 제국의 끝", "dark", "아케메네스 페르시아 · 기원전 550~330년"))
sc(2, ph("azara", pos="50% 25%", marks=[mk("서른두 살에 세상을 떠나다", 0.5, 0.12, "서른두")]), label=plabel("azara"))
sc(2, m("field", "field", [zone(LEVEL, None, 0), PPH(0), GPH(0)], tilt=30), hook={"question": {"text": QUESTION, "on": "왜", "kicker": "■ 답 ■"}})
sc(2, m("field", "field", [zone(LEVEL, "다리우스의 진짜 무기 · 땅", 0), PPH(0), swarm(CHARIOTS, 0.3, 90, 0.5)], tilt=32))
sc(1, m("field", "field", [zone(LEVEL, None, 0), PPH(0), GPHS(0.3), blue_a([[43.44, 36.50935], [43.445, 36.5035], [43.449, 36.49765]], 0.2, 1.2), badge("edge", "땅 밖으로", "#1f5fbf", 0.8, 60)], tilt=30))
sc(2, cmp("따라오지 않으면", "전차를 버린다", "따라오면", "전열이 늘어난다", "red", "red"))
sc(2, m("field", "field", [GPHS(0), PPHS(0, depth=P_GAP), LOCK("gap", on="찢어졌습니다")], tilt=32), sfx=PING(1.6))
sc(2, black("그 틈은", "적이 스스로 벌렸다"))
sc(4, checklist("그날 알렉산드로스가 한 일", [{"text": "적이 고른 땅에서 싸우지 않았다", "on": "적이 고른"}, {"text": "적을 움직이게 했다", "on": "움직이게"},
                                            {"text": "틈이 열린 순간 한 사람만", "on": "한 사람만"}]))
sc(3, cmp("숫자 · 땅", "다리우스", "움직임", "알렉산드로스", "red", "blue"))
sc(1, ai("wedge_charge"), label=DRAMA, callouts=low("아침부터 준비된 단 한 번의 돌격", "dark", 0.5))
sc(2, ai("plain_today"), label=DRAMA)
sc(3, text("다음 이야기", "yellow", "칸나이 전투 · 기원전 216년"))
sc(1, {"type": "endcard", "title": "가우가멜라에서 싸운 모든 이들을 기억하며", "q": pin("mosaic")}, tail=1.0)
assert CUR["i"] == len(ACTS[6]), (CUR, len(ACTS[6]))
SOMBER_FROM = [s["id"] for s in S if s.get("chapter", {}).get("num") == "제7막"][0]

# ===== 재연 일러스트 (countryball 반실사 + 일부 사실풍 풍경) — Cloudflare FLUX 무료 엔진 =====
CB = "Semi-realistic dramatic digital illustration in the style of polished history-YouTube countryball cartoons: "
MA = ("ancient Macedonian soldiers whose heads are round balls painted royal blue with a small golden sixteen-ray sun emblem, wearing bronze helmets, linen armor and red cloaks")
PE = ("ancient Achaemenid Persian soldiers whose heads are round balls painted deep purple with a small golden winged-disc emblem, wearing soft felt caps and colorful long-sleeved tunics")
ALEX = ("a young Macedonian king whose head is a round ball painted royal blue with a golden sixteen-ray sun emblem, with wavy golden-brown hair, "
        "wearing a plumed bronze helmet, a white and gold cuirass and a purple cloak")
DAR = ("an Achaemenid Persian Great King whose head is a round ball painted deep purple with a golden winged-disc emblem, wearing a tall golden crenellated crown, "
       "a long square curled black beard and royal purple robes")
PARM = "an old grey-bearded Macedonian general whose head is a round ball painted royal blue with a small golden sun emblem, wearing a bronze helmet and a dark cloak"
CHAR = "Persian scythed war chariots with long curved blades sticking out from the wheel hubs, pulled by four horses"
END = ", 331 BC ancient Near East, leaving calm uncluttered dark background area in the upper right, absolutely no speech bubbles, no balloons, no text boxes, no captions, no text, no letters."
LAND_S = "painterly realistic digital illustration, cinematic, desaturated warm palette, film grain, no people's faces in close-up, no text, no letters."
AI = {
    "plain_dawn": "A vast flat dusty plain in northern Mesopotamia at dawn, low hills on the horizon, an enormous ancient army in long lines stretching to the horizon, dust rising in golden light, " + LAND_S,
    "darius_flees": CB + DAR + " turning his golden chariot around and fleeing in panic through clouds of dust, his guards " + PE + " scattering" + END,
    "chariot_lanes": CB + MA + " in a dense phalanx with long pikes stepping aside to open a lane, " + CHAR + " rushing harmlessly through the empty lane" + END,
    "issus_flight": CB + ALEX + " charging on a black horse along a narrow coastal plain between mountains and the sea toward " + DAR + " who turns his chariot to flee" + END,
    "sisygambis_bow": CB + "an old Persian queen mother whose head is a round ball painted deep purple, in black veils, bowing low before a tall Macedonian officer, while " + ALEX + " smiles kindly beside them in a royal tent" + END,
    "tyre_causeway": "Ancient soldiers building a long stone causeway across the sea toward a walled island city, siege towers, ships, waves, " + LAND_S,
    "darius_letter": CB + "a Persian envoy whose head is a round ball painted deep purple, kneeling and offering a sealed scroll to " + ALEX + ", while " + PARM + " leans in to listen, in a military tent" + END,
    "scythe_chariot": CB + CHAR + " racing across a flat plain, driven by " + PE + ", dust trailing behind" + END,
    "leveling": CB + PE + " working with hoes and axes cutting bushes and flattening bumps on a huge dusty plain, overseers on horses" + END,
    "tigris_crossing": CB + MA + " wading neck-deep across a fast-flowing river holding their weapons above their heads, horses swimming beside them" + END,
    "eclipse": "A blood-red total lunar eclipse in the night sky above an ancient army camp with tents and campfires on a plain, frightened soldiers looking up, " + LAND_S,
    "alex_ridge": CB + ALEX + " on a horse on top of a low ridge with a few riders, looking down at a huge Persian army camp stretching across the plain to the horizon" + END,
    "night_council": CB + PARM + " pointing at a map on a table and urging " + ALEX + ", who shakes his head firmly, inside a lamp-lit tent at night, other officers watching" + END,
    "persians_awake": CB + PE + " standing exhausted in full armor beside their horses all night long, holding spears, torches in the dark, yawning" + END,
    "alex_sleeps": CB + ALEX + " sleeping peacefully on a camp bed at dawn, while " + PARM + " stands over him shaking his shoulder to wake him" + END,
    "javelin_chariot": CB + "Macedonian light javelin throwers and archers whose heads are round balls painted royal blue, throwing javelins at " + CHAR + ", grabbing the reins and pulling the drivers down" + END,
    "wedge_charge": CB + ALEX + " leading a wedge-shaped formation of Macedonian companion cavalry with long lances, charging into a gap in the Persian battle line, dust everywhere" + END,
    "camp_raid": CB + "Persian riders whose heads are round balls painted deep purple bursting into a Macedonian baggage camp, while an old veiled Persian queen mother refuses to go with them, sitting calmly" + END,
    "plain_today": "The wide empty plain near Mosul in northern Iraq today at sunset, dry grass, a distant low hill and a small village, calm and quiet, " + LAND_S,
    "thumb_bg": ("Cinematic photorealistic war painting, 16:9 wide shot on a dusty flat plain: a young Macedonian king in a plumed bronze helmet charging on a black horse at the tip of a wedge of cavalry "
                 "toward a Persian Great King standing in a golden chariot who is turning to flee, scythed chariots and huge armies in the dust behind, dramatic golden backlight, "
                 "full color, high contrast, the lower third of the frame darker, no text, no letters, no logos."),
}
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
prev_id = lambda x: ids[ids.index(x) - 1]
music = [{"id": "drone", "from": "s001", "to": sid(chap[0] - 1), "volume": 0.2},
         {"id": "theme", "from": sid(chap[0]), "to": sid(chap[1] - 1), "volume": 0.16},
         {"id": "analysis", "from": sid(chap[1]), "to": sid(chap[2] - 1), "volume": 0.16},
         {"id": "tension", "from": sid(chap[2]), "to": sid(chap[3] - 1), "volume": 0.17},
         {"id": "march", "from": sid(chap[3]), "to": sid(chap[4] - 1), "volume": 0.16},
         {"id": "tension", "from": sid(chap[4]), "to": prev_id(SOMBER_FROM), "volume": 0.17},
         {"id": "somber", "from": SOMBER_FROM, "to": ids[-1], "volume": 0.17}]
(HERE / "photo_pins.json").write_text(json.dumps(PINS, ensure_ascii=False, indent=1), encoding="utf-8")
# target_sec: 창욱 실측 초당 약 6.8자 → 약 8,080자 ≈ 19:50 + 장면 여백 (첫 미리보기 실측으로 갱신)
board = {"title": "단 한 번의 돌격: 가우가멜라 전투", "subtitle": "대왕이 고른 땅에서 싸우지 않은 알렉산드로스 · 기원전 331년",
         "lang": "ko", "sub_max": 28, "voice": "ZJCNdZEjYwkOElxugmW2", "tempo": 1.02, "tts_mode": "act", "style": 2, "sfx_policy": "doc", "bgm_rel_db": -24, "sync_limit": 0.5,
         "target_sec": 1230, "midrolls": MID, "land": LAND, "places": P, "views": V, "music": music, "ai_images": AI, "scenes": S}
(HERE / "storyboard.json").write_text(json.dumps(board, ensure_ascii=False, indent=1), encoding="utf-8")
types = collections.Counter(s["visual"]["type"] for s in S)
print("scenes", len(S), "chars", sum(len(say(l)) for s in S for l in s["lines"]), "mid", MID, "chap", [sid(i) for i in chap],
      "ai", len(AI), "pins", len(PINS), dict(types))
