# EP02 (한국어 《격전의 세계사》) 살라미스 해전 (기원전 480) 스토리보드 생성기 — 첫 생성용(기록). 나레이션은 script.md 문장을 순서대로 그대로 가져온다.
# ⚠️ storyboard.json을 손으로 고친 뒤에는 다시 돌리지 말 것 (수정 사항이 덮어써짐)
# 연출 스타일 v2 + 롱폼 표준(막 단위 TTS·절제된 효과음·BGM -24dB·싱크 ±0.5초) + 초반 후킹 표준(hook {hud, neg, question})
# 막 번호: Act 1 = 콜드 오프닝(0~60초), Act 2~7 = 본편 → 장면 "act" 1~7 = act1.mp3~act7.mp3
# 해전: 지도 아이템 ships(color 파랑=그리스 · 빨강=페르시아, sailOn으로 진입) + swarm(밀집 대함대) + clash(충각 충돌)
# 래스터: 기존 aegean_sea·attica_sea + 새 권역 salamis_zoom_sea (pipeline/geo.py RASTERS)
# 캐릭터 무대(stage)는 쓰지 않음 — 고대 그리스·페르시아 캐릭터 그림이 없어서(재연 일러스트로)
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
    ("기원전 사백팔십년 구월", "기원전 480년 9월"), ("기원전 사백팔십년 팔월", "기원전 480년 8월"), ("기원전 사백팔십삼년", "기원전 483년"), ("기원전 사백팔십년", "기원전 480년"),
    ("약 일점오 킬로미터", "약 1.5km"), ("천이백일곱 척", "1,207척"), ("삼백칠십팔 척", "378척"), ("백팔십 척", "180척"), ("이백만 명", "200만 명"),
    ("삼십칠 미터", "37m"), ("백칠십 명", "170명"), ("열 드라크마", "10드라크마"), ("사백 명", "400명"), ("이백 척", "200척"), ("사십 척", "40척"),
    ("채찍질 삼백 번", "채찍질 300번"), ("서른 곳", "30곳"), ("이천오백 년", "2,500년"), ("십 년", "10년"), ("팔 년", "8년"),
    ("십이 년 전", "12년 전"), ("삼 년이", "3년이"), ("정예 삼백 명", "정예 300명"), ("열여섯 척", "16척"), ("열네 명", "14명"), ("네 명만", "4명만"), ("두 배", "2배"), ("다섯 배", "5배"), ("세 층", "3층"),
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
    if fr in ZOOM or (to or fr) in ZOOM:
        v["demSea"] = True
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


# 사진: 위키미디어 공용 파일명을 웹 검색으로 확인한 것만 (2026-11-19)
PH = {
    "xerxes_tomb": ("File:Xerxes tomb at Naqsh-e Rostam (4615488322).jpg",
                    "크세르크세스 1세의 것으로 보는 암굴 무덤 · 낙쉐 로스탐 (2008)", ("낙쉐 로스탐", "2008")),
    "treasury": ("File:The Treasury Reliefs (Best Viewed in \"Original\" Size) (4734172156).jpg",
                 "옥좌의 대왕과 뒤에 선 왕자 · 페르세폴리스 보물고 부조 · 테헤란 국립박물관 (인물 해석은 학자마다 다름)", ("페르세폴리스 부조", "기원전 5세기")),
    "leonidas": ("File:Leónidas en las Termópilas, por Jacques-Louis David.jpg",
                 "테르모필레의 레오니다스 · 자크 루이 다비드 (1814) · 루브르 박물관", ("자크 루이 다비드", "1814")),
    "themis": ("File:Busto di temistocle, da originale greco del V secolo ac, dal decumano presso il casamento del temistocle.JPG",
               "테미스토클레스 흉상 · 기원전 5세기 그리스 원작의 로마 시대 복제품 · 오스티아 박물관", ("테미스토클레스 흉상", "로마 시대 복제품")),
    "lavrio": ("File:Μεταλλευτική Στοά, Λαύριο 6880.jpg",
               "라우리온의 옛 광산 갱도 (2016)", ("라우리온 광산 갱도", "오늘날")),
    "olympias": ("File:The trireme Olympias on 23 February 2019.jpg",
                 "복원한 아테네 삼단노선 올림피아스호 (2019)", ("복원 삼단노선 올림피아스", "2019")),
    "olympias2": ("File:Trireme Olympias.jpg",
                  "복원한 삼단노선 올림피아스호 · 팔레오 팔리로", ("복원 삼단노선", "팔레오 팔리로")),
    "lenormant": ("File:ACMA Relief Lenormant.jpg",
                  "노 젓는 아테네 삼단노선 선원들 · 레노르망 부조 (기원전 410년 무렵) · 아크로폴리스 박물관", ("레노르망 부조", "기원전 410년 무렵")),
    "artemisia": ("File:Artemisia at the Battle of Salamis.jpg",
                  "살라미스의 아르테미시아 · 빌헬름 폰 카울바흐 (1868) 부분", ("빌헬름 폰 카울바흐", "1868")),
    "ostraka": ("File:Ostraka for Ostracism, 5th century BC, Museum of the Ancient Agora, Athens, Greece (13896440260).jpg",
                "도편추방에 쓴 도자기 조각들 · 기원전 5세기 · 아테네 고대 아고라 박물관", ("도편추방 투표 조각", "기원전 5세기")),
    "wrath": ("File:Wrath of Xerxes at Battle of Salamis by Wilhelm von Kaulbach.jpg",
              "살라미스를 내려다보는 크세르크세스 · 빌헬름 폰 카울바흐 (1868) 부분", ("빌헬름 폰 카울바흐", "1868")),
    "aeschylus": ("File:Aischylos Büste.jpg",
                  "아이스킬로스 흉상 · 로마 시대 복제품 · 카피톨리니 박물관", ("아이스킬로스", "로마 시대 복제품")),
    "ostrakon": ("File:AGMA Ostrakon Thémistocle 1.jpg",
                 "테미스토클레스의 이름이 적힌 도편 · 아테네 고대 아고라 박물관", ("테미스토클레스 도편", "기원전 5세기")),
    "salamina": ("File:View of Salamina 1.jpg",
                 "오늘날의 살라미스섬", ("살라미스섬", "오늘날")),
    "kaulbach": ("File:Battle of Salamis by Wilhelm von Kaulbach.jpg",
                 "살라미스 해전 · 빌헬름 폰 카울바흐 (1868)", ("빌헬름 폰 카울바흐", "1868")),
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
# 좌표는 개략 (함대 위치·전열은 통설 재구성 기준 모식 배치)
P = {
    "athens": [23.727, 37.972, "아테네"], "salamis": [23.5, 37.94, "살라미스섬"], "ampelakia": [23.538, 37.951, "살라미스 · 그리스 함대 기지"],
    "psyttaleia": [23.594, 37.937, "프시탈레이아"], "piraeus": [23.635, 37.942, "페이라이에우스"], "phaleron": [23.68, 37.935, "팔레론"],
    "aigaleos": [23.59, 37.963, "아이갈레오스산 · 크세르크세스의 자리"], "kynosoura": [23.579, 37.927, "키노수라곶"], "narrows": [23.566, 37.952, "가장 좁은 곳"],
    "westch": [23.405, 37.975, "서쪽 물길"], "megara": [23.345, 37.996, "메가라"], "eleusis": [23.542, 38.041, "엘레우시스"],
    "aegina": [23.43, 37.745, "아이기나"], "troezen": [23.36, 37.5, "트로이젠"], "isthmus": [22.99, 37.92, "코린토스 지협"], "corinth": [22.88, 37.906, "코린토스"],
    "laurion": [24.05, 37.715, "라우리온"], "delphi": [22.501, 38.482, "델포이"], "thermopylae": [22.536, 38.796, "테르모필레"], "artemision": [23.25, 39.0, "아르테미시온"],
    "sardis": [28.04, 38.49, "사르디스"], "abydos": [26.41, 40.195, "헬레스폰토스"], "halicarnassus": [27.424, 37.038, "할리카르나소스"],
    "magnesia": [27.53, 37.853, "마그네시아"], "plataea": [23.27, 38.215, "플라타이아"], "mycale": [27.15, 37.66, "미칼레"], "marathon": [23.98, 38.125, "마라톤"], "athos": [24.33, 40.157, "아토스곶"],
    "susa": [48.25, 32.19, "수사"], "persepolis": [52.89, 29.935, "페르세폴리스"], "sparta": [22.43, 37.075, "스파르타"],
}
V = {
    "aegean": {"center": [25.4, 38.6], "span": 8.5}, "central": {"center": [23.2, 38.35], "span": 3.0},
    "saronic": {"center": [23.48, 37.8], "span": 1.15}, "salamis": {"center": [23.52, 37.95], "span": 0.24}, "strait": {"center": [23.575, 37.948], "span": 0.085}, "north": {"center": [25.0, 39.4], "span": 6.5},
}
ZOOM = {"salamis", "strait"}
LAND = {"home": ["300"], "foreign": ["792", "100", "8", "807", "196", "380", "642", "688", "499", "70"]}

# --- 해전 기하 (개략) ---
G_SHIPS = [[23.557, 37.9565], [23.556, 37.955], [23.555, 37.9535], [23.554, 37.952], [23.553, 37.9505], [23.552, 37.949], [23.551, 37.9475], [23.55, 37.946]]  # 2026-11-19 미리보기 후 키노수라곶 위에서 물 위로
P_SHIPS = [[23.604, 37.9465], [23.6005, 37.947], [23.597, 37.9475], [23.5935, 37.948], [23.59, 37.9485], [23.5865, 37.949], [23.583, 37.9495], [23.5795, 37.95]]  # 프시탈레이아 북쪽 물길
P_COLUMN = [[23.645, 37.946], [23.615, 37.948], [23.595, 37.95], [23.578, 37.952]]
JAM = [[23.6, 37.949], [23.588, 37.95], [23.576, 37.951]]
ENTRANCE = [[23.64, 37.915], [23.615, 37.928], [23.6, 37.936]]
WEST_BLOCK = [[23.62, 37.9], [23.5, 37.86], [23.42, 37.88], [23.39, 37.93], [23.405, 37.97]]
TO_PHALERON = [[23.585, 37.948], [23.62, 37.93], [23.66, 37.932], [23.68, 37.935]]
XERXES = [[28.04, 38.49], [27.0, 39.6], [26.41, 40.195], [25.0, 40.75], [23.2, 40.6], [22.6, 39.6], [22.536, 38.796]]
XERXES_BACK = [[23.727, 37.972], [22.9, 39.2], [23.4, 40.6], [25.0, 40.75], [26.41, 40.195]]
FLEET = [[26.4, 40.3], [24.6, 40.1], [23.6, 39.6], [23.25, 39.0]]
TO_ISTHMUS = [[23.53, 37.945], [23.3, 37.87], [23.1, 37.88], [22.99, 37.92]]
SALAMIS_HELL = [[23.56, 37.93], [24.4, 38.3], [25.2, 39.6], [26.41, 40.195]]

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
GS = lambda at=0, n=8, **kw: dict({"k": "ships", "pts": G_SHIPS[:n], "at": at, "rot": -15, "color": "#1f5fbf", "size": 0.8}, **kw)
PS = lambda at=0, n=8, **kw: dict({"k": "ships", "pts": P_SHIPS[:n], "at": at, "rot": 210, "color": "#8a2a22", "size": 0.8}, **kw)
top = lambda t, s="yellow", at=0: [{"text": t, "style": s, "at": at, "pos": "top"}]
low = lambda t, s="dark", at=0: [{"text": t, "style": s, "at": at, "pos": "lower"}]
SW = lambda at=0: [{"id": "whoosh", "at": at}]
PING = lambda at=0.6: [{"id": "ping", "at": at}]
WIND = lambda at=0: [{"id": "wind", "at": at}]
SEA = lambda at=0: [{"id": "water", "at": at}]
HUD = lambda big, sub=None, sub2=None, at=0.0, color=None, count=None, on=None: dict({"big": big}, **({"sub": sub} if sub else {}), **({"sub2": sub2} if sub2 else {}),
                                                                                      **({"on": on} if on else {"at": at}), **({"color": color} if color else {}), **({"count": count} if count is not None else {}))
QUESTION = "아테네를 불태운 대함대는\n어떻게 자기 숫자 때문에\n무너졌을까"

# ===== 제1막 · 콜드 오프닝 (0~10초 사건 직격 → 모순 3단 → X 반전 → 중앙 질문 카드 → 타이틀) =====
# 레이어 교차: 3D 비행 → 재연 그림 → 3D 함대 진입 → 사료 그림 → 비교 카드 → 재연 그림 → 3D 봉쇄 → X → 지도+질문 카드 → 타이틀
sc(2, m("saronic", "strait", [LOCK("narrows", 1.0, "살라미스 해협")], flight=["aegean", "saronic", "salamis", "strait"], flightDur=4.4, hud=True, tilt=26),
   hook={"hud": [HUD("기원전 480년 9월", "살라미스 해협", "아테네 서쪽 바다", count=False)]}, sfx=SW(0) + PING(1.3))
sc(1, ai("strait_dawn"), label=DRAMA, hook={"hud": [HUD("약 1.5km", "해협의 가장 좁은 곳", "통설 · 개략", on="일점오", count=False)]}, sfx=SEA(0))
sc(1, m("strait", "strait", [swarm(P_COLUMN, 0.1, 140, 0.5), PS(0.4)], tilt=30, hud=True))
sc(1, ph("wrath", pos="50% 35%", marks=[mk("크세르크세스", 0.5, 0.16, "대왕")]), label=plabel("wrath"))
sc(2, cmp("함대", "1 : 2 가까이", "해 질 녘 잃은 배", "40 : 200", "blue", "red"),
   hook={"hud": [HUD("약 370척", "그리스 함대", "헤로도토스 378척", on="그리스보다"), HUD("약 200척", "페르시아가 잃은 배", "디오도로스", color="#FF3B30", on="다섯")]})
sc(2, ai("phoenician_collide"), label=DRAMA, hook={"hud": [HUD("페니키아", "페르시아 함대의 주력", "바다의 달인", count=False, on="페니키아")]})
sc(2, m("salamis", "salamis", [dash_r(WEST_BLOCK, 0.2), red_a(ENTRANCE, 0.5), LOCK("salamis", 1.2, "퇴로 차단"), badge("ampelakia", "그리스 장군의 부탁?", "#c9242c", on="부탁한", dy=-90)], tilt=24),
   sfx=PING(1.4))
sc(3, black("운? 바람?", "그것뿐이었을까"), hook={"neg": {"text": "운 좋은 승리", "on": "운이", "xOn": "그랬을까요"}})
sc(1, m("strait", "strait", [GS(0), PS(0)], tilt=30), hook={"question": {"text": QUESTION, "at": 0.02}})
sc(1, {"type": "titlecard", "title": "대함대를 꾀었다", "sub": "살라미스 해전 · 기원전 480년", "at": 0, "q": pin("kaulbach")}, flash=True)
next_act()

# ===== 제2막 · 불타는 도시 =====
sc(2, ph("xerxes_tomb", pos="50% 40%", marks=[mk("크세르크세스의 무덤", 0.5, 0.15, "크세르크세스")]), label=plabel("xerxes_tomb"), chapter={"num": "제2막", "title": "불타는 도시"})
sc(1, ph("treasury", pos="50% 50%", marks=[mk("아버지와 아들?", 0.5, 0.18, "아버지가")]), label=plabel("treasury"))
sc(1, m("aegean", "aegean", [mark("sardis", "red", 0.2), red_a(XERXES[:3], 0.6)], tilt=12), callouts=top("기원전 480년 봄 · 사르디스 출발", "red"))
sc(3, bars("크세르크세스의 군대", [{"label": "헤로도토스", "value": 2000000, "display": "200만 명 이상", "color": "red", "on": "이백만"},
                                 {"label": "현대 추정", "value": 300000, "display": "수십만 명?", "color": "dark", "on": "수십만"}]))
sc(1, m("north", "north", [LOCK("abydos", 0.4), red_a(XERXES[1:4], 0.5)], tilt=14), callouts=top("유럽과 아시아 사이 · 헬레스폰토스"), sfx=PING(1.0))
sc(2, ai("boat_bridge_whip"), label=DRAMA, callouts=low("“바다에 채찍질 300번” · 헤로도토스", "dark", 1))
sc(1, text("7일 밤낮", "yellow", "다리를 건넌 군대 · 헤로도토스의 기록"))
sc(4, m("north", "north", [LOCK("athos", text="아토스곶 운하", on="아토스곶"), mark("abydos", "red", 0)], tilt=14), callouts=top("크세르크세스 운하 · 헤로도토스 7권 22절"), sfx=PING(1.4))
sc(2, m("aegean", "aegean", [red_a(XERXES, 0.1, 1.2), red_a(FLEET, 0.4), badge("artemision", "전함 1,207척", "#c9242c", on="천이백일곱", dy=-80)], tilt=12))
sc(3, ai("earth_water"), label=DRAMA, callouts=top("흙과 물 = 항복의 표시"))
sc(2, text("30여 곳", "blue", "끝까지 싸우겠다고 모인 그리스 도시"))
sc(2, m("aegean", "central", [LOCK("thermopylae", 0.8)], flight=["aegean", "central"], flightDur=2.6, tilt=20), callouts=top("기원전 480년 8월 · 테르모필레"), sfx=SW(0))
sc(1, text("스파르타 정예 300명", "red", "그리고 그리스 동맹군 수천 명"))
sc(2, m("central", "central", [unit("artemision", "그리스 함대", "blue", 0.1, pulse=True), clash("artemision", 0.6)], tilt=18), callouts=top("아르테미시온 · 사흘"))
sc(1, m("central", "central", [{"k": "shock", "pts": ["artemision"], "at": 0.5, "period": 0.8}, badge("artemision", "폭풍 · 페르시아 배 수백 척?", "#c9242c", on="폭풍이", dy=-80)], tilt=18), sfx=WIND(0))
sc(1, ph("leonidas", pos="50% 40%"), label=plabel("leonidas"))
sc(1, text("에피알테스", "dark", "산길을 알려 준 그리스인 · 헤로도토스"))
sc(2, m("central", "saronic", [dash_b([[23.25, 39.0], [23.9, 38.6], [24.1, 38.0], [23.6, 37.9]], 0.2), red_a([[22.536, 38.796], [23.0, 38.4], [23.5, 38.1], [23.727, 37.972]], 0.8)],
        flight=["central", "saronic"], flightDur=2.6, tilt=18), sfx=SW(0))
sc(2, black("아테네의 결정", "도시를 비우자"))
sc(3, {"type": "flatmap", "center": [23.5, 37.78], "span": 1.3, "fill": {"300": "#f1e4c6"},
       "pins": [{"ll": [23.727, 37.972], "text": "아테네", "side": "right", "at": 0}, {"ll": [23.36, 37.5], "text": "트로이젠", "side": "below", "on": "트로이젠"},
                {"ll": [23.43, 37.745], "text": "아이기나", "side": "below", "on": "아이기나와"}, {"ll": [23.48, 37.94], "text": "살라미스섬", "side": "above", "on": "살라미스섬"}],
       "routes": [{"from": [23.727, 37.972], "to": [23.36, 37.5], "bend": 0.2, "dur": 1.3, "label": "여자와 아이", "on": "트로이젠"},
                  {"from": [23.727, 37.972], "to": [23.43, 37.745], "bend": 0.15, "dur": 1.2, "label": "노인과 재산", "on": "아이기나와"},
                  {"from": [23.727, 37.972], "to": [23.5, 37.94], "bend": -0.2, "dur": 1.0, "label": "배로", "on": "배에"}], "labels": [], "zoomTo": 0.94})
sc(2, ai("persians_acropolis"), label=DRAMA, callouts=top("텅 빈 아테네", "red"))
sc(2, ai("smoke_from_salamis"), label=DRAMA, sfx=WIND(0))
sc(3, black("이 모든 것을", "미리 내다본 사람"))
next_act()

# ===== 제3막 · 은과 나무 성벽 =====
MID = [nid()]
sc(3, ph("themis", pos="50% 30%", marks=[mk("테미스토클레스", 0.5, 0.14, "테미스토클레스")]), label=plabel("themis"), pauseBefore=0.5, chapter={"num": "제3막", "title": "은과 나무 성벽"})
sc(1, ai("themis_sea"), label=DRAMA)
sc(2, text("마라톤의 승리", "dark", "기원전 490년 · “이제 끝났다”"))
sc(3, doc("테미스토클레스의 생각", ["페르시아는 반드시 다시 온다", "다음에는 바다로 온다"], "예견", "플루타르코스 『테미스토클레스 전』"))
sc(1, m("saronic", "saronic", [LOCK("piraeus", text="페이라이에우스 군항", on="페이라이에우스"), mark("athens", "blue", 0)], tilt=18))
sc(3, m("saronic", "saronic", [LOCK("laurion", 1.0), mark("athens", "blue", 0.2)], tilt=18), callouts=top("기원전 483년 무렵 · 라우리온 은광"), sfx=PING(1.2))
sc(2, ph("lavrio", marks=[mk("1인당 10드라크마?", 0.5, 0.2, "열")]), label=plabel("lavrio"))
sc(2, black("그 돈으로", "배를 만들자"))
sc(3, m("saronic", "saronic", [mark("athens", "blue", 0), mark("aegina", "red", on="아이기나와의"), badge("aegina", "명분: 숙적 아이기나", "#c9242c", on="숙적", dy=-80)], tilt=16))
sc(1, text("삼단노선 200척", "blue", "아테네 함대"))
sc(3, ai("ostracism_vote"), label=DRAMA, callouts=top("정의로운 사람 · 아리스테이데스"))
sc(5, ai("aristides_writes"), label=DRAMA, callouts=low("“여기에 아리스테이데스라고 써 주시오” · 플루타르코스", "dark", 1))
sc(2, ph("ostraka", marks=[mk("도편추방 투표 조각", 0.5, 0.18, "쫓겨납니다")]), label=plabel("ostraka"))
sc(3, ph("olympias", pos="50% 55%", marks=[mk("노 3층", 0.5, 0.25, "세 층"), mk("길이 약 37m", 0.5, 0.75, "삼십칠", "red")]), label=plabel("olympias"))
sc(2, ai("ram_closeup"), label=DRAMA, callouts=low("청동 충각"))
sc(2, ph("lenormant", marks=[mk("노 젓는 시민", 0.5, 0.18, "가난한")]), label=plabel("lenormant"))
sc(2, text("노 젓는 시민", "blue", "아테네의 새 주인공"))
sc(1, m("central", "central", [LOCK("delphi", 0.4), mark("athens", "blue", 0)], tilt=16), callouts=top("델포이 신탁"))
sc(2, doc("첫 번째 신탁", ["도망쳐라 땅끝까지"], "흉", "헤로도토스 7권 140절"))
sc(4, doc("두 번째 신탁", ["나무 성벽만은 무너지지 않으리라", "신성한 살라미스여", "너는 여인의 자식들을 죽이리라"], "신탁", "헤로도토스 7권 141절"))
sc(3, cmp("나무 성벽은", "아크로폴리스 울타리", "나무 성벽은", "배", "dark", "blue"))
sc(5, ai("themis_assembly"), label=DRAMA, callouts=low("“나무 성벽은 배다”", "dark", 1))
sc(1, ai("evacuation_ships"), label=DRAMA, sfx=SEA(0))
sc(2, black("진짜 싸움은", "자기 편과의 싸움"))
next_act()

# ===== 제4막 · 흩어지려는 함대 =====
sc(1, m("saronic", "salamis", [GS(0.6)], flight=["saronic", "salamis"], flightDur=2.6, tilt=26), chapter={"num": "제4막", "title": "흩어지려는 함대"}, sfx=SW(0))
sc(3, bars("살라미스의 그리스 함대 · 헤로도토스", [{"label": "전체", "value": 378, "display": "378척", "color": "blue", "on": "삼백칠십팔"},
                                             {"label": "아테네", "value": 180, "display": "180척", "color": "blue", "on": "백팔십"}]))
sc(3, ai("eurybiades"), label=DRAMA, callouts=top("총사령관 · 스파르타의 에우리비아데스"))
sc(1, bars("살라미스 함대 · 헤로도토스", [{"label": "아테네", "value": 180, "display": "180척", "color": "blue", "at": 0}, {"label": "스파르타", "value": 16, "display": "16척", "color": "red", "on": "열여섯"}]))
sc(5, m("saronic", "saronic", [mark("salamis", "blue", 0), dash_b(TO_ISTHMUS, on="지협으로"), LOCK("isthmus", text="코린토스 지협", on="지협으로")], tilt=18),
   callouts=top("펠로폰네소스파: 지협으로 가자", "red"))
sc(3, ai("council_panic"), label=DRAMA, callouts=low("“아테네가 불타고 있다”", "red", 1))
sc(3, ai("staff_raised"), label=DRAMA, callouts=low("“때리시오 그러나 내 말은 들으시오” · 플루타르코스", "dark", 2))
sc(3, cmp("지협 앞바다", "넓다", "살라미스 해협", "좁다", "red", "blue"), callouts=top("수가 많은 쪽이 이기는 곳은?"))
sc(2, m("salamis", "strait", [GS(0), badge("narrows", "좁은 물길", "#1f5fbf", on="좁은", dy=-60)], flight=["salamis", "strait"], flightDur=2.2, tilt=30))
sc(3, ai("adeimantus_mock"), label=DRAMA, callouts=low("“나라도 없는 자가”", "red", 1))
sc(3, text("배 200척", "blue", "“이것이 우리의 나라다”"))
sc(3, {"type": "flatmap", "center": [20.0, 38.9], "span": 12, "fill": {"300": "#f1e4c6", "380": "#e8d9b8"},
       "pins": [{"ll": [23.5, 37.94], "text": "살라미스", "side": "below", "at": 0}, {"ll": [16.6, 40.2], "text": "이탈리아 남부", "side": "above", "on": "이탈리아로"}],
       "routes": [{"from": [23.5, 37.94], "to": [16.6, 40.2], "bend": 0.2, "dur": 1.6, "label": "새 도시", "on": "이탈리아로"}], "labels": [], "zoomTo": 0.92})
sc(1, bars("아테네 배가 빠지면", [{"label": "그리스 함대", "value": 378, "display": "378척", "color": "blue", "at": 0},
                              {"label": "남는 배", "value": 198, "display": "절반", "color": "red", "on": "반 토막"}]))
sc(1, black("에우리비아데스는", "남기로 했다"))
sc(2, m("saronic", "saronic", [line([[23.0, 37.96], [22.97, 37.885]], on="성벽을"), LOCK("isthmus", text="지협을 막는 성벽", on="성벽을"), mark("salamis", "blue", 0)], tilt=18))
sc(1, black("하지만", "오래가지 못했다"))
sc(3, ai("xerxes_council"), label=DRAMA, callouts=top("페르시아 작전 회의", "red"))
sc(3, ph("artemisia", pos="50% 30%", marks=[mk("아르테미시아", 0.5, 0.14, "아르테미시아")]), label=plabel("artemisia"))
sc(3, doc("아르테미시아의 조언", ["바다에서 싸우지 마십시오", "기다리면 그리스 함대는 저절로 흩어집니다"], "반대", "헤로도토스 8권 68절"))
sc(2, m("saronic", "saronic", [red_a([[23.727, 37.972], [23.35, 37.97], [22.99, 37.92]], on="진격하면"), mark("isthmus", "blue", 0.3)], tilt=18), callouts=top("아르테미시아의 예측", "red"))
sc(3, text("싸우자", "red", "크세르크세스의 결정"))
sc(3, ai("council_again"), label=DRAMA, callouts=low("다시 열린 그리스 작전 회의"))
next_act()

# ===== 제5막 · 거짓 밀서 =====
MID.append(nid())
sc(3, ai("sicinnus_boat"), label=DRAMA, pauseBefore=0.5, chapter={"num": "제5막", "title": "거짓 밀서"}, sfx=SEA(0))
sc(2, text("목숨을 건 심부름", "yellow", "훗날 큰 재산과 테스피아이 시민권 · 헤로도토스"))
sc(3, ai("sicinnus_persians"), label=DRAMA, callouts=top("시킨노스 · 테미스토클레스의 하인"))
sc(3, doc("테미스토클레스의 전갈", ["그리스군은 도망치려 한다", "지금 막으면 한 척도 못 빠져나간다", "그들은 서로 다투고 있다"], "밀서", "헤로도토스 8권 75절"))
sc(3, black("배신자의 밀서", "왜 믿었을까?"))
sc(4, reasons("크세르크세스가 믿은 이유", [{"text": "그리스 함대의 다툼은 사실", "on": "사실이었거든요"}, {"text": "마라톤 때도 내통자", "on": "내통하는"},
                                          {"text": "듣고 싶던 말", "on": "듣고"}]))
sc(2, text("포위 · 섬멸", "red", "대왕이 처음부터 바라던 그림"))
sc(3, m("salamis", "salamis", [dash_r(WEST_BLOCK, on="서쪽"), badge("westch", "이집트 배 200척?", "#c9242c", on="이집트", dy=-60)], tilt=22),
   callouts=top("밤 · 서쪽 물길 봉쇄", "red"))
sc(3, m("salamis", "strait", [PS(0.2), LOCK("psyttaleia", text="프시탈레이아 · 약 400명", on="프시탈레이아")], flight=["salamis", "strait"], flightDur=2.2, tilt=28), sfx=PING(1.6))
sc(2, ai("rowers_night"), label=DRAMA, callouts=top("밤새 노를 잡고"))
sc(2, m("salamis", "salamis", [PS(0), red_a(ENTRANCE, 0.2), mark("ampelakia", "blue", 0.5)], tilt=24), callouts=top("그리스 진영은 아무도 몰랐다"))
sc(3, ai("aristides_arrives"), label=DRAMA, callouts=top("아리스테이데스"))
sc(2, ph("ostraka", marks=[mk("도편추방", 0.5, 0.18, "도편추방")]), label=plabel("ostraka"))
sc(1, m("saronic", "saronic", [dash_b([[23.43, 37.745], [23.5, 37.84], [23.54, 37.93]], on="아이기나"), mark("aegina", "dark", 0)], tilt=16), callouts=top("아이기나에서 밤바다를 건너"))
sc(4, doc("아리스테이데스의 말", ["다툴 때가 아니다", "떠나고 싶어도 떠날 수 없다", "우리는 포위됐다"], "포위", "헤로도토스 8권 79절"))
sc(2, ai("themis_smile"), label=DRAMA, callouts=low("“그건 내가 한 일이다”", "dark", 1))
sc(3, text("“당신이 직접 말해 주시오”", "dark", "테미스토클레스가 아리스테이데스에게 · 헤로도토스 8권 80절"))
sc(2, m("strait", "strait", [PS(0), GS(0), blue_a([[23.595, 37.94], [23.578, 37.943], [23.565, 37.946]], on="넘어온")], tilt=30), callouts=top("페르시아 편에서 넘어온 배"))
sc(2, black("남은 길은", "싸우는 것"))
sc(1, m("salamis", "salamis", [dash_r(WEST_BLOCK, 0), red_a(ENTRANCE, 0.1), LOCK("salamis", 0.4, "퇴로 차단")], tilt=24), sfx=PING(0.8))
next_act()

# ===== 제6막 · 좁은 물길 =====
MID.append(nid())
sc(3, ai("xerxes_throne"), label=DRAMA, pauseBefore=0.5, chapter={"num": "제6막", "title": "좁은 물길"}, sfx=WIND(0))
sc(2, text("서기들", "dark", "잘 싸운 선장의 이름을 적다 · 헤로도토스 8권 90절"))
sc(1, m("strait", "strait", [GS(0.2), LOCK("aigaleos", 0.6)], tilt=30, hud=True), sfx=SEA(0))
sc(5, ai("greek_paean"), label=DRAMA, callouts=low("“그리스의 아들들이여 나아가라” · 아이스킬로스", "dark", 0))
sc(1, text("겁먹은 페르시아", "red", "아이스킬로스 『페르시아인들』"))
sc(1, ph("aeschylus", pos="50% 30%", marks=[mk("아이스킬로스", 0.5, 0.14, "아이스킬로스")]), label=plabel("aeschylus"))
sc(4, m("strait", "strait", [GS(0), dash_b([[23.562, 37.946], [23.552, 37.946], [23.545, 37.947]], on="뒤로"), badge("narrows", "뒤로 노를 젓다", "#1f5fbf", on="거꾸로", dy=-70)], tilt=30))
sc(3, m("strait", "strait", [GS(0), PS(0, sailOn="들어옵니다", dx=-0.012, dy=0.008), swarm(P_COLUMN, 0.3, 150, 0.5)], tilt=32))
sc(3, m("salamis", "strait", [badge("piraeus", "입구 · 넓다", "#111", on="넓습니다", dy=-60), badge("narrows", "안쪽 · 좁다", "#c9242c", on="좁아집니다", dy=-60)],
        flight=["salamis", "strait"], flightDur=2.4, tilt=30), sfx=SW(0))
sc(3, ai("jam"), label=DRAMA)
sc(2, cmp("달리는 삼단노선", "창", "멈춘 삼단노선", "표적", "blue", "red"))
sc(4, checklist("아테네 삼단노선", [{"text": "낮고 무거운 배", "on": "무겁고"}, {"text": "중장보병 14명", "on": "열네"}, {"text": "궁수 4명", "on": "네 명만"}, {"text": "무기는 충각", "on": "들이받는"}]))
sc(4, m("strait", "strait", [GS(0), PS(0), swarm(JAM, 0, 160, 0.4), blue_a([[23.562, 37.952], [23.574, 37.953]], on="튀어나옵니다"), clash([23.576, 37.953], on="들이받습니다"),
                             badge([23.562, 37.952], "아메이니아스", "#1f5fbf", on="아메이니아스", dy=-70)], tilt=32), sfx=PING(2.0))
sc(1, ai("ram_impact"), label=DRAMA)
sc(3, m("strait", "strait", [GS(0), swarm(JAM, 0, 160, 0.4), line([[23.6, 37.925], [23.585, 37.94], [23.575, 37.95]], on="바람이", color="#ffffff"),
                             badge("kynosoura", "아침 바람 · 플루타르코스", "#111", on="바람이", dy=-60)], tilt=30), sfx=WIND(0))
sc(3, reasons("페르시아 함대", [{"text": "페니키아", "on": "페니키아"}, {"text": "이집트", "on": "이집트"}, {"text": "키프로스", "on": "키프로스"}, {"text": "이오니아", "on": "이오니아"},
                              {"text": "말도 신호도 제각각", "on": "말도"}]))
sc(1, ai("rowers_night"), label=DRAMA, callouts=top("밤새 한숨도 못 잔 노잡이들"))
sc(3, m("strait", "strait", [GS(0), swarm(JAM, 0, 200, 0.35), clash([23.584, 37.95], 0.3), clash([23.592, 37.949], on="부딪힙니다"),
                             LOCK("aigaleos", text="대왕의 눈", on="대왕이")], tilt=34, hud=True), sfx=WIND(0))
sc(3, text("에우보이아 때보다 용감하게", "red", "대왕이 지켜본다는 두려움 · 헤로도토스 8권 86절"))
sc(1, m("strait", "strait", [GS(0), swarm(JAM, 0, 220, 0.35), clash([23.58, 37.952], on="짓누르는")], tilt=34), callouts=top("숫자가 무게가 되다", "red"))
sc(4, ai("artemisia_ram"), label=DRAMA, callouts=low("자기 편 배를 들이받다", "red", 2))
sc(3, ph("wrath", pos="50% 30%"), label=plabel("wrath"), callouts=low("“내 남자들은 여자가 되었고 내 여자들은 남자가 되었구나”", "dark", 2))
sc(2, ai("persians_in_water"), label=DRAMA)
sc(1, text("아리아비그네스 전사", "red", "크세르크세스의 동생 · 해군 사령관"))
sc(1, ph("kaulbach", pos="50% 50%"), label=plabel("kaulbach"))
sc(3, m("strait", "strait", [blue_a([[23.556, 37.94], [23.572, 37.941], [23.584, 37.943]], on="이끌고"), LOCK("psyttaleia", text="프시탈레이아", on="프시탈레이아섬")], tilt=30), sfx=PING(1.4))
sc(2, m("salamis", "salamis", [red_a([[23.585, 37.95], [23.6, 37.948], [23.625, 37.944]], 0.1), clash([23.615, 37.946], on="들이받았거든요"), badge([23.615, 37.946], "아이기나 배의 매복", "#1f5fbf", on="아이기나", dy=-70)], tilt=26))
sc(1, m("salamis", "saronic", [red_a(TO_PHALERON, 0.2), mark("phaleron", "red", 0.8)], flight=["salamis", "saronic"], flightDur=2.2, tilt=20))
sc(2, bars("잃은 배 · 디오도로스", [{"label": "페르시아", "value": 200, "display": "약 200척", "color": "red", "on": "이백"},
                               {"label": "그리스", "value": 40, "display": "약 40척", "color": "blue", "on": "사십"}]))
next_act()

# ===== 제7막 · 답 =====
sc(3, ai("phoenician_captains"), label=DRAMA, pauseBefore=0.5, chapter={"num": "제7막", "title": "답"})
sc(3, m("north", "north", [dash_b(SALAMIS_HELL, on="헬레스폰토스로"), LOCK("abydos", text="헬레스폰토스 다리", on="다리를")], tilt=12), sfx=PING(1.2))
sc(3, doc("두 번째 전갈", ["테미스토클레스가 대왕을 위해", "그리스 함대를 붙잡아 두었다"], "반쯤 거짓", "헤로도토스 8권 110절"))
sc(2, m("aegean", "aegean", [red_a(XERXES_BACK, 0.2, 1.2), mark("athens", "dark", 0)], tilt=12), callouts=top("크세르크세스 아시아로 철수", "red"))
sc(2, m("aegean", "aegean", [mark("plataea", "blue", on="플라타이아와"), mark("mycale", "blue", on="미칼레에서")], tilt=12), callouts=top("기원전 479년 · 플라타이아와 미칼레", "blue"))
sc(2, m("strait", "strait", [GS(0), swarm(JAM, 0, 160, 0.4)], tilt=30), hook={"question": {"text": QUESTION, "on": "어떻게", "kicker": "■ 답 ■"}})
sc(2, text("운이 아니었다", "yellow", "결정들이 이어진 사슬"))
sc(2, ph("olympias2", pos="50% 55%"), label=plabel("olympias2"), callouts=top("첫째 · 배", "blue"))
sc(2, m("salamis", "strait", [badge("narrows", "좁은 물길", "#1f5fbf", 0.3, -60)], flight=["salamis", "strait"], flightDur=2.0, tilt=28), callouts=top("둘째 · 장소", "blue"))
sc(2, ai("sicinnus_persians"), label=DRAMA, callouts=top("셋째 · 밀서", "blue"))
sc(2, ai("rowers_night"), label=DRAMA, callouts=top("넷째 · 피로", "blue"))
sc(2, m("strait", "strait", [GS(0), dash_b([[23.562, 37.946], [23.552, 37.946], [23.545, 37.947]], 0.2), PS(0, sailAt=0.3, dx=-0.012, dy=0.008)], tilt=30), callouts=top("다섯째 · 물러남", "blue"))
sc(2, ai("jam"), label=DRAMA, callouts=top("여섯째 · 무게", "blue"))
sc(2, ai("xerxes_throne"), label=DRAMA, callouts=low("대왕의 눈마저 독이 되다", "red", 0))
sc(2, checklist("살라미스 승리의 이유", [{"text": "배", "at": 0}, {"text": "장소", "at": 0.1}, {"text": "밀서", "at": 0.2}, {"text": "피로", "at": 0.3},
                                     {"text": "물러남", "at": 0.4}, {"text": "무게", "at": 0.5}, {"text": "좁은 물길 = 덫", "on": "덫이"}]))
sc(2, ph("aeschylus", pos="50% 30%"), label=plabel("aeschylus"), callouts=top("기원전 472년 · 비극 『페르시아인들』"))
sc(4, ph("ostrakon", marks=[mk("테미스토클레스", 0.5, 0.15, "이름을")]), label=plabel("ostrakon"))
sc(2, black("그가 찾아간 곳은", "페르시아"))
sc(3, m("aegean", "aegean", [LOCK("magnesia", text="마그네시아", on="마그네시아를"), mark("athens", "dark", 0)], tilt=12), callouts=top("아르타크세르크세스 1세의 신하로"), sfx=PING(1.0))
sc(1, ph("salamina"), label=plabel("salamina"))
sc(2, ai("strait_sunset"), label=DRAMA)
sc(1, text("다음 이야기", "yellow", "가우가멜라 전투 · 기원전 331년"))
sc(2, {"type": "endcard", "title": "살라미스의 좁은 물길에서 노를 저은 모든 이들을 기억하며", "q": pin("kaulbach")}, tail=1.0)
assert CUR["i"] == len(ACTS[6]), (CUR, len(ACTS[6]))
SOMBER_FROM = [s["id"] for s in S if s.get("chapter", {}).get("num") == "제7막"][0]

# ===== 재연 일러스트 (countryball 반실사 + 일부 사실풍 풍경) — 2026-11-19 Cloudflare FLUX 무료 엔진 =====
CB = "Semi-realistic dramatic digital illustration in the style of polished history-YouTube countryball cartoons: "
GR = ("ancient Athenian sailors and marines whose heads are round balls painted white with a small golden owl emblem, wearing bronze helmets and simple tunics")
PE = ("ancient Achaemenid Persian sailors and soldiers whose heads are round balls painted deep purple with a small golden winged-disc emblem, wearing soft felt caps and colorful tunics")
PHO = "Phoenician sailors whose heads are round balls painted dark red with a small golden palm-tree emblem, wearing conical caps"
XER = ("an Achaemenid Persian Great King whose head is a round ball painted deep purple with a golden winged-disc emblem, wearing a tall golden crenellated crown, "
       "a long square curled black beard and royal purple robes")
THEM = ("a clever middle-aged Athenian general whose head is a round ball painted white with a small golden owl emblem, with a short dark beard, "
        "a bronze helmet pushed up on top and a blue cloak")
TRI = "ancient Greek triremes with three banks of oars, bronze rams at the bow and painted eyes"
END = ", 480 BC ancient Greece, leaving calm uncluttered dark background area in the upper right, absolutely no speech bubbles, no balloons, no text boxes, no captions, no text, no letters."
LAND_S = "painterly realistic digital illustration, cinematic, desaturated palette, film grain, no people's faces in close-up, no text, no letters."
AI = {
    "strait_dawn": "Aerial view at dawn of a narrow sea strait between a rocky island and a mountainous coast in ancient Greece, hundreds of ancient warships with oars entering the strait from the open sea, mist, " + LAND_S,
    "phoenician_collide": CB + "two big Phoenician warships crashing into each other in a crowded narrow strait, their oars snapping, " + PHO + " shouting in panic" + END,
    "boat_bridge_whip": CB + "Persian soldiers, " + PE + ", whipping the sea with long whips beside a long bridge of boats tied together across a strait, " + XER + " watching angrily from the shore" + END,
    "earth_water": CB + "Persian envoys, " + PE + ", holding out a jar of water and a bowl of earth to nervous Greek city elders whose heads are round balls painted white, in a marble courtyard" + END,
    "persians_acropolis": CB + PE + " storming the burning temples on top of the Athenian Acropolis rock, flames and black smoke rising" + END,
    "smoke_from_salamis": "Refugees in ancient Greek clothes standing on a rocky island shore at dusk, looking across the water at a distant city on a hill with a huge column of black smoke rising, " + LAND_S,
    "themis_sea": CB + THEM + " standing alone on a rocky headland at sunset, looking out over the sea toward the east" + END,
    "ram_closeup": "Close-up of the bronze ram at the waterline of an ancient Greek trireme cutting through waves, oars in motion above, spray, " + LAND_S,
    "themis_assembly": CB + THEM + " pointing toward the sea while addressing a crowd of Athenian citizens whose heads are round balls painted white with a small golden owl emblem, on a rocky hillside" + END,
    "evacuation_ships": CB + "Athenian families, " + GR + ", boarding " + TRI + " at a crowded harbor, carrying baskets and children, the city on a hill behind" + END,
    "eurybiades": CB + "a stern Spartan admiral whose head is a round ball painted red with a white lambda emblem, wearing a red cloak and a crested bronze helmet, standing on the deck of a trireme" + END,
    "council_panic": CB + "Greek commanders whose heads are round balls painted in different city colors, shouting and rushing out of a tent toward their ships at night, one already raising a sail" + END,
    "adeimantus_mock": CB + "a sneering Corinthian admiral whose head is a round ball painted gold with a small winged-horse emblem, mocking " + THEM + " in a lamp-lit tent" + END,
    "xerxes_council": CB + XER + " seated on a throne in a large tent, surrounded by bowing admirals " + PE + " and " + PHO + ", all nodding" + END,
    "council_again": CB + "Greek commanders whose heads are round balls painted in different city colors arguing loudly around a table with a sea map in a tent at night" + END,
    "sicinnus_boat": "A small rowing boat slipping across a dark calm sea at night from an island toward distant enemy camp fires on the opposite shore, one cloaked man in the boat, " + LAND_S,
    "sicinnus_persians": CB + "a humble Greek servant whose head is a round ball painted white, kneeling and whispering to suspicious Persian admirals, " + PE + ", in a torch-lit camp at night" + END,
    "rowers_night": CB + "exhausted Persian rowers, " + PE + ", sitting at their oars inside a dark warship at night, yawning and slumped, lanterns" + END,
    "aristides_arrives": CB + "a calm grey-bearded Athenian statesman whose head is a round ball painted white with a small golden owl emblem, stepping off a small boat at night and calling out to " + THEM + END,
    "themis_smile": CB + THEM + " smiling slyly in a dark tent lit by an oil lamp, an older grey-bearded Athenian looking at him in surprise" + END,
    "ostracism_vote": CB + "a crowd of Athenian citizens whose heads are round balls painted white with a small golden owl emblem, dropping broken pottery shards into a large voting enclosure in a marble marketplace" + END,
    "aristides_writes": CB + "a calm grey-bearded Athenian statesman whose head is a round ball painted white with a small golden owl emblem, quietly scratching on a broken pottery shard held out by a puzzled peasant farmer whose head is a round ball painted white, in a busy marketplace" + END,
    "staff_raised": CB + "a stern Spartan admiral whose head is a round ball painted red with a white lambda emblem raising a wooden staff as if to strike " + THEM + ", who stands firm and keeps talking, other commanders watching in a tent" + END,
    "xerxes_throne": CB + XER + " seated on a golden throne on a mountain slope above a narrow strait full of warships at dawn, scribes with tablets beside him" + END,
    "greek_paean": CB + GR + " rowing " + TRI + " out from an island shore at dawn, singing with open mouths, a trumpeter at the bow" + END,
    "jam": CB + "hundreds of Persian warships crammed together in a narrow strait, their oars tangled and snapping, ships colliding, " + PHO + " and " + PE + " in chaos" + END,
    "ram_impact": CB + "a Greek trireme with a bronze ram smashing into the side of a Persian warship, wood splintering, " + GR + " cheering, " + PE + " falling into the sea" + END,
    "artemisia_ram": CB + "a fierce queen whose head is a round ball painted deep purple with a small golden star emblem, wearing a crown and armor, ordering her warship to ram another Persian warship" + END,
    "persians_in_water": CB + GR + " swimming strongly toward an island shore while " + PE + " cling to floating wreckage in the sea, broken oars everywhere" + END,
    "phoenician_captains": CB + PHO + " kneeling and begging before " + XER + " on a mountain slope, guards with spears behind them" + END,
    "strait_sunset": "The narrow strait of Salamis at sunset seen from a hill, calm water, the island across, a few small boats, golden light, " + LAND_S,
    "thumb_bg": ("Cinematic photorealistic war painting, 16:9 wide high-angle shot over a narrow sea strait at dawn: hundreds of ancient Persian warships jammed together and colliding, "
                 "broken oars, Greek triremes with bronze rams charging into their sides from the left, an island coast on the left and mountains on the right, "
                 "dramatic backlight, high contrast, the lower third of the frame darker, no text, no letters, no logos."),
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
# target_sec: 창욱 환산 약 7,000자 = 20:30 → 6,755자 ≈ 19:50 (첫 미리보기 실측으로 갱신)
board = {"title": "대함대를 꾀었다: 살라미스 해전", "subtitle": "좁은 해협에서 자기 숫자에 무너진 페르시아 함대 · 기원전 480년",
         "lang": "ko", "sub_max": 28, "voice": "ZJCNdZEjYwkOElxugmW2", "tempo": 1.02, "tts_mode": "act", "style": 2, "sfx_policy": "doc", "bgm_rel_db": -24, "sync_limit": 0.5,
         "target_sec": 1225, "midrolls": MID, "land": LAND, "places": P, "views": V, "music": music, "ai_images": AI, "scenes": S}
(HERE / "storyboard.json").write_text(json.dumps(board, ensure_ascii=False, indent=1), encoding="utf-8")
types = collections.Counter(s["visual"]["type"] for s in S)
print("scenes", len(S), "chars", sum(len(say(l)) for s in S for l in s["lines"]), "mid", MID, "chap", [sid(i) for i in chap],
      "ai", len(AI), "pins", len(PINS), dict(types))
