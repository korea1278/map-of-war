# EP01 (한국어 《격전의 세계사》 · 2026-11-18 영문 → 한국어 전환) 마라톤 전투 (기원전 490) 스토리보드 생성기 — 첫 생성용(기록). 나레이션은 script.md 문장을 순서대로 그대로 가져온다.
# ⚠️ storyboard.json을 손으로 고친 뒤에는 다시 돌리지 말 것 (수정 사항이 덮어써짐)
# 연출 스타일 v2 + 롱폼 표준(LONGFORM_STANDARD: 막 단위 TTS·절제된 효과음·BGM -24dB·싱크 ±0.5초) + 초반 후킹 표준(HOOK_STANDARD: hook {hud, neg, question} · troops)
# 막 번호: 사용자 지시서 기준 Act 1 = 콜드 오프닝(0~60초), Act 2~7 = 본편 → 장면 "act" 1~7 = act1.mp3~act7.mp3
# 한반도 밖 첫 전장: 보드 "land"(그리스·주변국 ISO 코드) + geo.py 래스터 aegean_sea·attica_sea·marathon_zoom_sea
# 새 엔진 부품(2026-11-18 이 편에서 추가): 지도 아이템 phalanx(가운데 얇고 양 날개 두꺼운 전열 띠 · bend/wrap/run) · zone(늪 빗금) · ships(해안 함선·출항)
#   · troops profile 정면 전열(gr/pe 병사 · runOn/bendOn/wrapOn = 돌격·중앙 후퇴·양익 포위)
# 캐릭터 무대(stage)는 쓰지 않음 — 고대 그리스·페르시아 캐릭터 그림이 없어서(SVG 볼 대체 대신 재연 일러스트로)
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
    ("기원전 사백구십구년", "기원전 499년"), ("기원전 사백구십이년", "기원전 492년"), ("기원전 사백구십년 구월", "기원전 490년 9월"), ("기원전 사백구십년", "기원전 490년"),
    ("이만에서 이만오천 명", "2만에서 2만 5,000명"), ("약 육천사백 명", "약 6,400명"), ("백구십이 명", "192명"),
    ("사십이 점 일구오 킬로미터", "42.195km"), ("이백사십 킬로미터", "240km"), ("약 사십 킬로미터", "약 40km"), ("약 십 킬로미터", "약 10km"),
    ("일점오 킬로미터", "1.5km"), ("이십 킬로그램", "20kg"), ("일 미터", "1m"), ("약 구 미터", "약 9m"), ("천팔백구십육년", "1896년"),
    ("스파르타군 이천 명", "스파르타군 2,000명"), ("이천 년", "2,000년"), ("약 구천 명", "약 9,000명"), ("약 천 명", "약 1,000명"), ("만 명", "1만 명"),
    ("배 스무 척", "배 20척"), ("다섯 척", "5척"), ("육백 척", "600척"), ("일곱 척", "7척"), ("육 년", "6년"), ("세 번씩", "3번씩"), ("이 년 뒤", "2년 뒤"),
    ("이십 년 전", "20년 전"), ("이십 년 동안", "20년 동안"), ("예순 살", "60살"), ("열 명", "10명"), ("열 개 부족", "10개 부족"), ("팔 스타디온", "8스타디온"),
    ("서른세 명", "33명"), ("서른 배", "30배"), ("두 배", "2배"), ("오백 년", "500년"), ("십칠 년", "17년"), ("십 년 뒤", "10년 뒤"), ("오십 탈란톤", "50탈란톤"),
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


def doc(head, rows, stamp, org, note="Paraphrase · summary"):
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
    """정면 전열 대열 (Hook.tsx PhalanxTroops) — profile: 열마다 대열 깊이"""
    v = {"type": "troops", "side": "gr", "profile": profile}
    if vs:
        v["vs"] = {"side": "pe", "profile": vs}
    if title:
        v["title"] = title
    if labels:
        v["labels"] = labels
    v.update(kw)
    return v


def lab(x, y, t, color="dark", on=None, at=None):
    d = {"x": x, "y": y, "text": t, "color": color}
    if on:
        d["on"] = on
    else:
        d["at"] = at or 0
    return d


# 사진: 위키미디어 공용 파일명을 웹 검색으로 확인한 것만 (2026-11-18)
PH = {
    "darius": ("File:Large stone relief depicting Darius I, seated on his throne, being approached by a high dignitary whose hand is raised to his mouth in a gesture of respectful greeting, Persepolis, Iran (47890487391).jpg",
               "옥좌에 앉은 다리우스 1세 · 페르세폴리스 부조", ("페르세폴리스 부조", "기원전 500년 무렵")),
    "archers": ("File:Frieze of Archers from the Palace of Darius I in Susa, Achaemenid Persian Period, reign of Darius I, c. 510 BC, Louvre Museum (12251246605).jpg",
               "궁수 부조 · 수사의 다리우스 1세 궁전 (기원전 510년 무렵) · 루브르 박물관", ("수사 · 채색 벽돌", "기원전 510년 무렵")),
    "guard": ("File:Head of a member of the so-called Immortals, the 1000 special royal guards. Glazed brick. From the East Gate of the Palace at Susa, Iran. Achaemenid period, 521-500 BCE. British Museum.jpg",
               "페르시아 왕실 근위병 · 수사 채색 벽돌 · 대영 박물관", ("수사 · 왕실 근위병", "기원전 521~500년")),
    "marsh": ("File:Marshlands of Marathon, with Pentelikon mountains in the background.jpg",
               "마라톤의 늪지와 펜텔리콘산 (2016)", ("마라톤 · 늪지", "2016")),
    "plain1": ("File:Plain of Marathon 1.jpg",
               "오늘날의 마라톤 평원", ("마라톤 평원", "오늘날")),
    "plain2": ("File:Plain of Marathon 2.jpg",
               "오늘날의 마라톤 평원", ("마라톤 평원", "오늘날")),
    "beach": ("File:Marathon beach.jpg",
               "오늘날의 마라톤 해변", ("마라톤 해변", "오늘날")),
    "miltiades": ("File:Miltiades (Roman replica).jpg",
               "밀티아데스 · 그리스 흉상의 로마 시대 복제품 · 슬로베니아 국립미술관", ("밀티아데스", "로마 시대 복제품")),
    "helmet": ("File:Helmet of Miltiades the Younger.jpg",
               "밀티아데스가 올림피아에 바친 청동 투구 · 올림피아 고고학 박물관", ("올림피아 · 청동 투구", "기원전 490년 무렵")),
    "hoplite": ("File:Athenian hoplite.jpg",
               "복원한 아테네 중장보병 장비 · 아테네 자피온 전시 (2010)", ("복원품", "2010")),
    "chigi": ("File:Chigi vase detail.jpg",
               "싸우는 중장보병 · 키지 항아리 (기원전 650년 무렵)", ("키지 항아리", "기원전 650년 무렵")),
    "herodotus": ("File:Marble bust of Herodotos MET DT11742 (cropped).jpg",
               "헤로도토스 · 로마 시대 대리석 흉상 · 메트로폴리탄 미술관", ("헤로도토스", "로마 시대 복제품")),
    "stoa": ("File:Miltiades fighting the Persians at the Battle of Marathon in the Stoa Poikile (reconstitution).jpg",
               "스토아 포이킬레의 마라톤 전투 그림 · 현대 복원도", ("스토아 포이킬레 · 복원도", "아테네")),
    "soros": ("File:The burial mound of the Athenians at Marathon on Januray 15, 2019.jpg",
               "소로스 · 마라톤 아테네인 전사자 무덤 (2019)", ("소로스", "2019")),
    "soros_old": ("File:Great Tumulus in the plain of Marathon - Dodwell Edward - 1819.jpg",
               "마라톤 평원의 큰 무덤 · 에드워드 도드웰 (1819)", ("에드워드 도드웰", "1819")),
    "plataean": ("File:The burial mound of the Plataeans in Marathon on January 15, 2019.jpg",
               "마라톤의 플라타이아인 무덤 (2019)", ("플라타이아인 무덤", "2019")),
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
# 좌표는 개략 (전열 위치·늪 범위·함선 위치는 통설 재구성 기준 모식 배치)
P = {
    "athens": [23.727, 37.972, "아테네"], "phaleron": [23.68, 37.935, "팔레론"], "sounion": [24.026, 37.651, "수니온곶"],
    "eretria": [23.795, 38.395, "에레트리아"], "plataea": [23.27, 38.215, "플라타이아"], "thebes": [23.32, 38.32, "테베"], "sparta": [22.43, 37.075, "스파르타"],
    "naxos": [25.38, 37.1, "낙소스"], "delos": [25.268, 37.396, "델로스"], "carystus": [24.42, 38.015, "카리스토스"], "paros": [25.15, 37.08, "파로스"],
    "sardis": [28.04, 38.49, "사르디스"], "miletus": [27.278, 37.53, "밀레토스"], "athos": [24.33, 40.157, "아토스산"], "samos": [26.95, 37.73, "사모스"],
    "chersonese": [26.45, 40.35, "트라키아 케르소네소스"], "susa": [48.25, 32.19, "수사"], "persepolis": [52.89, 29.935, "페르세폴리스"],
    "babylon": [44.42, 32.54, "바빌론"], "indus": [67.6, 26.2, "인더스강"],
    "marathon": [23.98, 38.125, "마라톤"], "soros": [23.9783, 38.1186, "소로스"], "herakleion": [23.948, 38.128, "헤라클레스 성역 · 그리스군 진영"],
    "gmarsh": [24.022, 38.148, "큰 늪"], "smarsh": [23.97, 38.092, "작은 늪"], "pcamp": [24.018, 38.138, "페르시아 진영"],
    "pentelikon": [23.885, 38.05, "펜텔리콘산"], "agrieliki": [23.94, 38.108, "아그리엘리키산"], "kotroni": [23.935, 38.158, "코트로니산"],
}
V = {
    "empire": {"center": [46.5, 30.0], "span": 50}, "aegean": {"center": [25.4, 38.6], "span": 8.5}, "ionia": {"center": [26.6, 38.2], "span": 4.6},
    "greece": {"center": [23.3, 37.85], "span": 3.4}, "attica": {"center": [23.8, 38.08], "span": 1.5},
    "marathon": {"center": [23.982, 38.118], "span": 0.18}, "plain": {"center": [23.985, 38.124], "span": 0.085}, "beach": {"center": [24.015, 38.13], "span": 0.075},
}
ZOOM = {"marathon", "plain", "beach"}
LAND = {"home": ["300"], "foreign": ["792", "100", "8", "807", "196", "380", "364", "368", "760", "818", "400", "422", "376", "275", "682", "434",
                                     "642", "688", "51", "31", "268", "4", "795", "586", "414", "48", "634", "784", "512", "887", "860", "762",
                                     "398", "804", "498", "348", "191", "70", "499", "703", "705", "729", "788", "12", "248"]}

# --- 전장 기하 (개략) ---
G_LINE = [[23.962, 38.131], [23.973, 38.111]]  # 그리스 전열: 왼쪽(북, 플라타이아) → 오른쪽(남, 칼리마코스) · 정면 = 동쪽(face -1)
P_LINE = [[23.986, 38.139], [23.997, 38.117]]  # 페르시아 전열: 북 → 남 · 정면 = 서쪽(face 1)
G_THIN = [8, 8, 8, 7, 4, 3, 3, 4, 7, 8, 8, 8]
P_DEEP = [3, 3, 4, 6, 8, 8, 8, 8, 6, 4, 3, 3]
GMARSH = [[23.996, 38.146], [24.012, 38.161], [24.035, 38.163], [24.05, 38.152], [24.04, 38.141], [24.02, 38.137], [24.004, 38.139]]
SMARSH = [[23.962, 38.098], [23.974, 38.1], [23.979, 38.092], [23.975, 38.083], [23.963, 38.086]]  # 2026-11-18 DEM 해안선 확인 후 육지 쪽으로 이동
SHIPS = [[24.004 + 0.0042 * k, 38.114 + 0.0028 * k] for k in range(12)]
ROAD_S = [[23.95, 38.125], [23.93, 38.1], [23.9, 38.075], [23.86, 38.045]]
ROAD_N = [[23.945, 38.14], [23.925, 38.16], [23.895, 38.175]]
RUN_SP = [[23.727, 37.972], [23.4, 37.98], [22.95, 37.93], [22.75, 37.72], [22.6, 37.5], [22.47, 37.28], [22.43, 37.075]]
PLAT_M = [[23.27, 38.215], [23.5, 38.2], [23.75, 38.17], [23.94, 38.13]]
ATH_M = [[23.727, 37.972], [23.8, 38.02], [23.88, 38.08], [23.945, 38.125]]
BACK_M = [[23.95, 38.12], [23.88, 38.075], [23.81, 38.02], [23.727, 37.975]]
FLEET_PH = [[24.04, 38.11], [24.12, 37.95], [24.1, 37.72], [24.0, 37.61], [23.85, 37.7], [23.72, 37.86], [23.68, 37.925]]
FLEET_490 = [[26.95, 37.73], [25.6, 37.2], [25.38, 37.12], [25.27, 37.42], [24.45, 37.98], [24.0, 38.25], [23.84, 38.37]]
FLEET_492 = [[26.6, 40.42], [25.6, 40.62], [24.6, 40.28], [24.38, 40.18]]
IONIA_HELP = [[23.727, 37.972], [24.9, 37.9], [26.6, 37.97], [27.35, 37.94], [28.04, 38.49]]
HOME = [[23.68, 37.925], [24.2, 37.75], [25.5, 37.6], [26.9, 37.75], [27.2, 37.9]]
SPARTA_M = [[22.43, 37.075], [22.6, 37.5], [22.95, 37.93], [23.4, 37.98], [23.727, 37.972]]
EMPIRE = [[26.0, 41.6], [29.5, 41.8], [35, 41.8], [41, 41.6], [47, 42], [53, 40.5], [58, 38.5], [63, 37.5], [67.5, 37.2], [70.5, 34.5], [71.5, 31], [70, 27],
          [66, 25], [61, 25.2], [57, 26.5], [52, 28], [50, 29.8], [48, 30], [45, 31.5], [40, 30], [36, 29.5], [34.5, 28], [33.5, 25], [32.8, 22], [31, 22],
          [29, 25], [25.5, 30.8], [26.8, 34], [27.2, 36.6], [26.6, 39.8], [26.0, 41.6]]
XERXES = [[29.0, 39.8], [27.0, 40.4], [25.0, 40.7], [23.2, 40.6], [22.6, 39.6], [23.3, 38.4]]

LOCK = lambda p, at=0.3, text=None, on=None: dict({"k": "lock", "p": p, "text": text or P[p][2]}, **({"on": on} if on else {"at": at}))
badge = lambda p, t, c="#111", at=0.3, dy=-70, on=None: dict({"k": "badge", "p": p, "text": t, "color": c, "dy": dy}, **({"on": on} if on else {"at": at}))
red_a = lambda path, at=0.3, w=1.0, on=None: dict({"k": "arrow", "path": path, "color": "red", "width": w}, **({"on": on} if on else {"at": at}))
blue_a = lambda path, at=0.3, w=1.0, on=None: dict({"k": "arrow", "path": path, "color": "blue", "width": w}, **({"on": on} if on else {"at": at}))
dash_r = lambda path, at=0.2: {"k": "arrow", "path": path, "color": "red", "dash": True, "at": at}
mark = lambda p, color="red", at=0, text=None, on=None: dict({"k": "marker", "p": p, "color": color}, **({"text": text} if text else {}), **({"on": on} if on else {"at": at}))
unit = lambda p, t, color="red", at=0.1, pulse=False: dict({"k": "unit", "p": p, "text": t, "color": color, "at": at}, **({"pulse": True} if pulse else {}))
clash = lambda p, at=0.3, size=1.0: {"k": "clash", "p": p, "at": at, "period": 0.9, "size": size}
swarm = lambda path, at=0.1, n=120, width=None, color=None: dict({"k": "swarm", "path": path, "at": at, "n": n}, **({"width": width} if width else {}), **({"color": color} if color else {}))
line = lambda path, at=0.1, color="#ffd400", on=None: dict({"k": "line", "path": path, "color": color, "glow": True}, **({"on": on} if on else {"at": at}))
zone = lambda path, text=None, color="#3fb6a8", at=0, on=None: dict({"k": "zone", "path": path, "color": color}, **({"text": text} if text else {}), **({"on": on} if on else {"at": at}))
ships = lambda at=0, sailOn=None, dx=0.03, dy=-0.025, n=12, **kw: dict({"k": "ships", "pts": SHIPS[:n], "at": at, "rot": -55, "dx": dx, "dy": dy}, **({"sailOn": sailOn} if sailOn else {}), **kw)
GPH = lambda at=0, **kw: dict({"k": "phalanx", "path": G_LINE, "depth": G_THIN, "face": -1, "px": 3.2, "color": "blue", "at": at}, **kw)
PPH = lambda at=0, **kw: dict({"k": "phalanx", "path": P_LINE, "depth": P_DEEP, "face": 1, "px": 3.2, "color": "red", "at": at}, **kw)
top = lambda t, s="yellow", at=0: [{"text": t, "style": s, "at": at, "pos": "top"}]
low = lambda t, s="dark", at=0: [{"text": t, "style": s, "at": at, "pos": "lower"}]
SW = lambda at=0: [{"id": "whoosh", "at": at}]
PING = lambda at=0.6: [{"id": "ping", "at": at}]
WIND = lambda at=0: [{"id": "wind", "at": at}]
SEA = lambda at=0: [{"id": "water", "at": at}]
HUD = lambda big, sub=None, sub2=None, at=0.0, color=None, count=None, on=None: dict({"big": big}, **({"sub": sub} if sub else {}), **({"sub2": sub2} if sub2 else {}),
                                                                                      **({"on": on} if on else {"at": at}), **({"color": color} if color else {}), **({"count": count} if count is not None else {}))
QUESTION = "기병도 궁수도 없던 농민 중장보병은\n어떻게 세계 최대 제국을\n바다로 몰아냈을까"

# ===== 제1막 · 콜드 오프닝 (후킹 표준: 0~10초 사건 직격 → 10~40초 모순 3단 → X 반전 → 중앙 질문 카드 → 타이틀) =====
# 레이어 교차: 3D 비행 → 병력 대열 → 재연 그림 → 3D 전열 → 사료 사진 → 비교 카드 → 병력 대열(돌격) → X → 지도+질문 카드 → 타이틀
sc(2, m("attica", "marathon", [LOCK("soros", 0.9, "마라톤")], flight=["aegean", "attica", "marathon"], flightDur=4.2, hud=True, tilt=26),
   hook={"hud": [HUD("기원전 490년", "마라톤 평원", "아테네에서 약 40km", count=False)]}, sfx=SW(0) + PING(1.2))
sc(1, ranks([6] * 12, title="청동의 한 줄"), hook={"hud": [HUD("1만 명", "아테네·플라타이아 중장보병", "추정", on="만 명")]})
sc(1, ai("persian_host"), label=DRAMA, hook={"hud": [HUD("2만~2만 5,000명", "페르시아 상륙군", "현대 추정 · 고대 기록은 훨씬 많음", color="#FF3B30", on="제국")]}, sfx=WIND(0.1))
sc(1, m("plain", "plain", [PPH(0), GPH(0, run=60, runOn="달리기"), badge("soros", "달려서 돌격", "#c9242c", on="달리기", dy=-90)], tilt=30))
sc(2, ph("archers", pos="50% 40%", marks=[mk("궁수", 0.5, 0.18, "궁수", "red"), mk("그리스 기병 0", 0.5, 0.68, "둘 다", "yellow")]), label=plabel("archers"),
   hook={"hud": [HUD("0", "그리스군의 기병 · 궁수", "마라톤 전장", color="#FF3B30", on="둘 다", count=False)]})
sc(2, cmp("병력", "1 : 2", "해 질 녘 전사자", "33 : 1", "blue", "red"))
sc(2, ranks(G_THIN, P_DEEP, title="걷지 않았다", runOn="뛰어들었"), hook={"hud": [HUD("8스타디온", "약 1.5km의 빈 땅", "달려서 건넜다", on="뛰어들었", count=False)]})
sc(3, black("운 좋은", "기적?"), hook={"neg": {"text": "운 좋은 기적", "on": "기적", "xOn": "그랬을까요"}})
sc(1, m("plain", "plain", [PPH(0), GPH(0)], tilt=30), hook={"question": {"text": QUESTION, "at": 0.02}})
sc(1, {"type": "titlecard", "title": "달려서 덮쳤다", "sub": "마라톤 전투 · 기원전 490년", "at": 0, "q": pin("plain1")}, flash=True)
next_act()

# ===== 제2막 · 잊지 않은 왕 =====
sc(2, ph("darius", pos="50% 35%", marks=[mk("다리우스 1세", 0.5, 0.16, "다리우스")]), label=plabel("darius"), chapter={"num": "제2막", "title": "잊지 않은 왕"})
sc(1, m("empire", "empire", [line(EMPIRE, 0.1, "#ff3b30"), mark("persepolis", "red", 0.4), mark("susa", "red", 0.6), mark("indus", "dark", on="인더스")], tilt=10),
   callouts=top("아케메네스 페르시아 제국 · 기원전 500년 무렵", "red"))
sc(1, text("세계 인구의 3분의 1?", "red", "현대 추정"))
sc(2, m("aegean", "ionia", [unit("miletus", "이오니아 반란", "blue", 0.2, pulse=True), mark("sardis", "red", 0.5)], flight=["aegean", "ionia"], flightDur=2.6),
   callouts=top("기원전 499년 · 이오니아"), sfx=SW(0))
sc(1, m("aegean", "aegean", [blue_a(IONIA_HELP[:3], 0.3), mark("athens", "blue", 0), mark("eretria", "blue", 0.2)]))
sc(2, bars("반란을 도우러 보낸 배", [{"label": "아테네", "value": 20, "display": "20척", "color": "blue", "on": "스무"},
                                  {"label": "에레트리아", "value": 5, "display": "5척", "color": "blue", "on": "다섯"}]))
sc(2, ai("sardis_burning"), label=DRAMA, callouts=low("기원전 498년 · 불타는 사르디스"))
sc(1, text("6년", "dark", "이오니아 반란 진압 · 기원전 499~493년"))
sc(1, black("하지만 다리우스는", "잊지 않았다"))
sc(2, ai("darius_arrow"), label=DRAMA)
sc(2, ai("servant_dinner"), label=DRAMA, callouts=low("“주인이시여, 아테네인을 잊지 마소서”", "dark", 1))
sc(2, m("aegean", "aegean", [red_a(FLEET_492, 0.1), {"k": "shock", "pts": ["athos"], "at": 1.2, "period": 0.8}, mark("athos", "dark", on="아토스")], tilt=16),
   callouts=top("기원전 492년 · 아토스산"))
sc(2, black("다리우스는", "다시 시도했다"))
sc(1, text("전함 600척", "red", "헤로도토스의 기록"))
sc(1, bars("페르시아 상륙군 · 현대 추정", [{"label": "적게", "value": 20000, "display": "2만 명", "color": "red", "on": "이만"},
                                        {"label": "많게", "value": 25000, "display": "2만 5,000명", "color": "red", "on": "이만오천"}]))
sc(3, ai("horse_transport"), label=DRAMA)
sc(1, ph("guard", pos="50% 30%"), label=plabel("guard"), callouts=top("다티스 · 아르타페르네스"))
sc(2, doc("대왕의 명령", ["아테네를 노예로", "에레트리아를 노예로", "포로를 대왕 앞으로"], "王命", "헤로도토스 6권 94절", "요지"))
sc(2, m("aegean", "aegean", [red_a(FLEET_490[:4], 0.1), mark("naxos", "red", on="낙소스"), mark("delos", "dark", 0.6)], tilt=14), callouts=low("기원전 490년 · 섬에서 섬으로"))
sc(2, ai("delos_incense"), label=DRAMA)
sc(2, text("자비", "yellow", "고개를 숙이는 자에게만"))
sc(2, m("aegean", "attica", [red_a(FLEET_490[3:], 0.2), LOCK("eretria", 1.2)], flight=["aegean", "attica"], flightDur=2.6, hud=True), callouts=top("에레트리아 포위 · 6일", "red"),
   sfx=SW(0) + PING(1.4))
sc(1, ai("eretria_gates"), label=DRAMA)
sc(2, ai("eretria_chains"), label=DRAMA)
sc(1, black("에레트리아는", "사라졌다"))
sc(1, m("attica", "attica", [mark("eretria", "dark", 0), line([[23.795, 38.39], [23.86, 38.3], [23.95, 38.16]], 0.2, "#ff3b30"), mark("athens", "blue", 0.5)], tilt=20),
   callouts=low("좁은 해협 건너편"))
sc(2, ai("hippias_ship"), label=DRAMA)
sc(1, text("히피아스", "dark", "아테네의 옛 참주 · 기원전 510년 추방"))
sc(2, reasons("아테네가 무너지면", [{"text": "히피아스 귀환", "on": "히피아스"}, {"text": "대왕의 하수인으로 통치", "on": "하수인"}]))
sc(3, m("attica", "marathon", [zone(GMARSH, None, at=1.2), mark("marathon", "red", 0.4)], flight=["attica", "marathon"], flightDur=3.0, tilt=24), callouts=top("아티카 동쪽 해안"), sfx=SW(0))
sc(2, ph("marsh", marks=[mk("마라톤 = ‘회향’", 0.5, 0.18, "회향")]), label=plabel("marsh"))
next_act()

# ===== 제3막 · 회향의 평원 =====
MID = [nid()]
sc(2, m("marathon", "marathon", [zone(GMARSH, None, at=0.6)], tilt=34, hud=True), pauseBefore=0.5, chapter={"num": "제3막", "title": "회향의 평원"}, sfx=SEA(0))
sc(2, m("marathon", "marathon", [zone(GMARSH, "큰 늪", on="커다란 늪"), zone(SMARSH, "작은 늪", "#3fb6a8", on="작은 늪")], tilt=34))
sc(1, m("marathon", "marathon", [zone(GMARSH, "큰 늪"), zone(SMARSH, "작은 늪"), badge("agrieliki", "산", "#111", 0.3), badge("kotroni", "산", "#111", 0.5)], tilt=34))
sc(1, m("marathon", "marathon", [line(ROAD_S, 0.1), line(ROAD_N, 0.4), badge("herakleion", "아테네로 가는 길", "#111", 0.6, -80)], tilt=30))
sc(2, cmp("기병에게는", "최고의 땅", "아테네에게는", "악몽", "red", "dark"))
sc(3, ai("assembly_debate"), label=DRAMA)
sc(2, black("성벽은", "에레트리아를 지키지 못했다"))
sc(3, ph("miltiades", pos="50% 30%", marks=[mk("밀티아데스", 0.5, 0.15, "밀티아데스")]), label=plabel("miltiades"))
sc(3, m("aegean", "aegean", [unit("chersonese", "밀티아데스의 식민지", "blue", 0.1, pulse=True), mark("sardis", "red", 0.5)], tilt=12), callouts=top("헬레스폰토스"))
sc(2, ai("danube_bridge"), label=DRAMA)
sc(3, text("페르시아가 싸우는 법", "yellow", "그리고 두려워하는 것"))
sc(3, m("aegean", "aegean", [dash_r([[26.45, 40.35], [25.6, 39.8], [24.6, 38.8], [23.727, 37.972]], 0.1), mark("athens", "blue", 0.6)], tilt=12), callouts=low("기원전 493년 · 아테네까지 쫓기다"))
sc(2, doc("혐의: 참주 정치", ["피고: 밀티아데스", "판결: 무죄"], "無罪", "아테네 법정 · 기원전 493년", "헤로도토스 6권 104절 · 요지"))
sc(2, ai("miltiades_assembly"), label=DRAMA)
sc(1, ph("hoplite", pos="50% 35%", marks=[mk("방패", 0.35, 0.6, "방패"), mk("창", 0.7, 0.3, "창", "red"), mk("청동 투구", 0.5, 0.14, "투구")]), label=plabel("hoplite"))
sc(2, reasons("그들은 누구였나", [{"text": "농부", "on": "농부"}, {"text": "도공", "on": "도공"}, {"text": "올리브 농사꾼", "on": "올리브"}, {"text": "가게 주인", "on": "가게"}]))
sc(2, ai("hoplites_neighbors"), label=DRAMA, hudCta={"at": 0, "dur": 7.0})
sc(1, m("attica", "attica", [blue_a(ATH_M, 0.2), mark("athens", "blue", 0), mark("marathon", "red", 0.6)], tilt=20), callouts=top("아테네군 약 9,000명 출전", "blue"))
sc(2, m("greece", "greece", [line(RUN_SP, 0.2, "#ffd400", on="전령"), mark("athens", "blue", 0), mark("sparta", "dark", 0.6)], tilt=14), callouts=low("필리피데스"))
sc(2, ai("runner_mountains"), label=DRAMA, callouts=top("약 240km · 이튿날 스파르타 도착"))
sc(3, doc("스파르타의 답", ["좋다", "하지만 보름달이 뜬 뒤에"], "斯巴達", "헤로도토스 6권 106절", "요지"))
sc(2, text("약 6일", "red", "보름달이 뜰 때까지"))
sc(2, black("아테네 홀로", "아니 거의 홀로"))
sc(2, ai("plataeans_arrive"), label=DRAMA)
sc(1, m("attica", "attica", [blue_a(PLAT_M, 0.1), mark("plataea", "blue", 0), mark("thebes", "dark", 0.4)], tilt=18), callouts=top("플라타이아 · 약 1,000명", "blue"))
sc(2, {"type": "flatmap", "center": [23.5, 38.1], "span": 1.7, "fill": {"300": "#f1e4c6"},
       "pins": [{"ll": [23.27, 38.215], "text": "플라타이아", "side": "below", "at": 0}, {"ll": [23.32, 38.32], "text": "테베", "side": "right", "on": "테베"},
                {"ll": [23.727, 37.972], "text": "아테네", "side": "below", "at": 0.3}],
       "routes": [{"from": [23.727, 37.972], "to": [23.27, 38.215], "bend": 0.2, "dur": 1.4, "label": "보호", "on": "지켜 준"}], "labels": [], "zoomTo": 0.92})
sc(1, bars("마라톤의 그리스군 (추정)", [{"label": "아테네", "value": 9000, "display": "약 9,000명", "color": "blue", "at": 0},
                                     {"label": "플라타이아", "value": 1000, "display": "약 1,000명", "color": "blue", "at": 0.3},
                                     {"label": "합계", "value": 10000, "display": "약 1만 명", "color": "dark", "on": "만 명"}]))
sc(2, m("marathon", "marathon", [unit("herakleion", "그리스군 진영", "blue", 0.1, pulse=True), line(ROAD_S, 0.5, "#2e66d8")], tilt=30), callouts=top("헤라클레스 성역"))
sc(2, ai("felled_trees"), label=DRAMA)
sc(2, m("beach", "beach", [ships(0), unit("pcamp", "페르시아 진영", "red", 0.6, pulse=True), zone(GMARSH, "큰 늪", at=0.9)], tilt=32), sfx=SEA(0))
sc(3, ai("hippias_sneeze"), label=DRAMA)
sc(3, ai("hippias_tooth"), label=DRAMA, callouts=low("“이 땅은 우리 것이 아니구나”", "dark", 1))
next_act()

# ===== 제4막 · 다섯 대 다섯 =====
sc(3, m("marathon", "marathon", [unit("herakleion", "그리스군", "blue", 0.1), unit("pcamp", "페르시아군", "red", 0.4), ships(0.2)], tilt=30, hud=True),
   chapter={"num": "제4막", "title": "다섯 대 다섯"}, callouts=top("대치 · 며칠 동안"))
sc(3, reasons("그리스군이 기다린 이유", [{"text": "스파르타가 온다", "on": "스파르타"}, {"text": "들판은 기병과 궁수의 땅", "on": "탁 트인"}]))
sc(3, ai("traitor_gate"), label=DRAMA, callouts=low("페르시아가 기다린 이유"))
sc(3, ranks([1] * 10, title="장군 10명", labels=[lab(0.5, 0.3, "부족마다 1명 · 하루씩 돌아가며 지휘", "dark", on="하루씩")]))
sc(3, bars("장군 10명의 의견", [{"label": "기다리자", "value": 5, "display": "5", "color": "blue", "on": "기다리자"}, {"label": "공격하자", "value": 5, "display": "5", "color": "red", "on": "공격하자"}]))
sc(3, ai("callimachus"), label=DRAMA, callouts=top("폴레마르코스 칼리마코스"))
sc(2, ai("miltiades_callimachus"), label=DRAMA)
sc(4, doc("칼리마코스에게", ["노예냐 자유냐", "기다리면 도시가 갈라진다", "지금 싸우면 이긴다"], "決斷", "헤로도토스 6권 109절", "요지"))
sc(1, bars("결정적인 한 표", [{"label": "기다리자", "value": 5, "display": "5", "color": "blue", "at": 0}, {"label": "공격하자", "value": 6, "display": "6", "color": "red", "on": "표를"}]))
sc(4, text("그는 기다렸다", "yellow", "자기 지휘 날이 올 때까지"))
sc(3, black("그는 왜", "기다렸을까?"))
sc(4, checklist("그리스군의 전력", [{"text": "중장보병", "on": "중장보병"}, {"text": "기병", "on": "기병은", "checkOn": "기병은", "bad": True},
                                 {"text": "궁수", "on": "궁수라", "checkOn": "궁수라", "bad": True}]))
sc(2, ph("archers", pos="50% 55%"), label=plabel("archers"), callouts=top("페르시아에는 둘 다 있었다", "red"))
sc(1, text("묘한 이야기", "dark", "『수다』 · 비잔티움 사전 · 서기 1000년 무렵"))
sc(1, ai("ionian_deserters"), label=DRAMA)
sc(2, doc("밤에 전해진 말", ["“기병이 떠났다”"], "?", "『수다』 (코리스 히페이스)", "후대 기록 · 논쟁 중"))
sc(3, black("이게", "사실이었을까?"))
sc(3, m("marathon", "attica", [dash_r(FLEET_PH, 0.6), mark("phaleron", "red", 1.2), mark("athens", "blue", 1.4)], flight=["marathon", "attica"], flightDur=2.6),
   callouts=top("학설 · 팔레론으로 가려 했다", "red"), sfx=SW(0))
sc(2, ai("horses_loading"), label=DRAMA)
sc(2, m("beach", "beach", [ships(0, sailOn="둘로", n=6), unit("pcamp", "기병 승선 중?", "red", 0.2, pulse=True), PPH(0.4)], tilt=30), callouts=low("학설 · 확인 안 됨"))
sc(2, ai("dawn_omens"), label=DRAMA, sfx=WIND(0))
sc(2, m("marathon", "plain", [blue_a([[23.948, 38.128], [23.958, 38.124], [23.966, 38.121]], 0.3), GPH(0.9)], flight=["marathon", "plain"], flightDur=2.4, tilt=30),
   callouts=top("새벽 · 그리스군이 내려오다"), sfx=SW(0))
next_act()

# ===== 제5막 · 팔 스타디온을 달리다 =====
MID.append(nid())
sc(3, ranks([8] * 6, [4] * 12, title="고민", labels=[lab(0.5, 0.2, "더 긴 페르시아 전열", "red", on="길었던"), lab(0.5, 0.52, "양쪽 끝을 감싸인다", "dark", on="감싸")]),
   pauseBefore=0.5, chapter={"num": "제5막", "title": "팔 스타디온을 달리다"})
sc(5, ranks(G_THIN, [4] * 12, title="상식을 깨다", labels=[lab(0.5, 0.52, "얇은 가운데", "red", on="얇게"), lab(0.15, 0.52, "두꺼운 날개", "blue", on="날개"),
                                                         lab(0.85, 0.52, "두꺼운 날개", "blue", on="날개")]))
sc(3, m("plain", "plain", [GPH(0), badge([23.973, 38.111], "칼리마코스", "#1f5fbf", on="오른쪽"), badge([23.962, 38.131], "플라타이아군", "#1f5fbf", on="플라타이아")], tilt=32))
sc(3, text("테미스토클레스 · 아리스테이데스", "dark", "얇은 가운데 · 플루타르코스의 기록"))
sc(1, text("앞으로의 20년", "yellow", "살라미스 · 플라타이아 · 아테네 제국"))
sc(2, m("plain", "plain", [GPH(0), PPH(0.2, text="페르시아 본토 병사 · 사카족")], tilt=32))
sc(2, ai("saka_warriors"), label=DRAMA)
sc(2, m("plain", "plain", [GPH(0), PPH(0), line([[23.968, 38.121], [23.991, 38.128]], 0.3, "#ffffff"), badge("soros", "8스타디온 ≈ 1.5km", "#111", on="팔", dy=-60)], tilt=32))
sc(1, black("그리고", "그 순간"))
sc(2, black("그리스군은 걷지 않았다", "달렸다"), sfx=WIND(0))
sc(2, ph("chigi", pos="50% 50%", marks=[mk("지름 약 1m 방패", 0.5, 0.2, "방패")]), label=plabel("chigi"))
sc(1, ph("helmet", pos="50% 45%", marks=[mk("청동 투구", 0.5, 0.82, "투구")]), label=plabel("helmet"))
sc(1, text("20kg 이상", "red", "중장보병 장비 무게 추정"))
sc(3, ranks([5] * 12, title="방패의 벽", runOn="달리다", labels=[lab(0.5, 0.28, "방패로 왼쪽 동료를 가린다", "dark", on="왼쪽")]))
sc(3, ai("persians_watch"), label=DRAMA, callouts=low("“미쳤다”", "red", 1))
sc(3, reasons("왜 달렸나", [{"text": "하늘을 덮는 화살", "on": "화살로"}, {"text": "죽음의 땅을 빨리 건넌다", "on": "빨리"}]))
sc(2, m("plain", "plain", [PPH(0), GPH(0, run=55, runOn="뛰기"), badge([23.98, 38.124], "화살 사정거리 안", "#c9242c", on="화살이", dy=-50)], tilt=32), sfx=PING(1.2))
sc(3, doc("헤로도토스 6권 112절", ["처음으로 달려서 돌격한 그리스인", "페르시아 복장 앞에서 두려워하지 않은 첫 그리스인"], "記錄", "헤로도토스 『역사』", "요지"))
sc(1, ai("clash"), label=DRAMA, sfx=WIND(0))
sc(3, cmp("페르시아", "고리버들 · 아마포", "그리스", "청동 · 나무", "red", "blue"))
sc(5, ranks(G_THIN, P_DEEP, title="가운데", bendOn="무너졌", labels=[lab(0.5, 0.52, "가운데가 무너진다", "red", on="무너졌")]))
sc(1, black("익숙한 이야기가", "되풀이되나?"))
sc(3, m("plain", "plain", [GPH(0, bend=30, bendAt=0), PPH(0), swarm([[23.99, 38.135], [24.0, 38.137], [24.012, 38.132]], 1.0, 70, 0.4),
                           swarm([[23.993, 38.116], [24.004, 38.118], [24.012, 38.124]], 1.2, 70, 0.4)], tilt=32), callouts=top("날개가 이긴다", "blue"))
sc(2, ai("wings_temptation"), label=DRAMA)
sc(3, checklist("본능이 외친 것", [{"text": "쫓아라", "on": "쫓으라고"}, {"text": "해변에서 끝장내라", "on": "끝장"}, {"text": "전리품을 챙겨라", "on": "전리품"}]))
sc(1, black("하지만 그들은", "그러지 않았다"))
sc(4, ranks(G_THIN, P_DEEP, title="덫", bendAt=0, wrapOn="방향을", labels=[lab(0.5, 0.52, "날개가 안쪽으로 돈다", "blue", on="방향을")]))
sc(1, ai("wings_turn"), label=DRAMA)
sc(2, m("plain", "plain", [PPH(0), GPH(0, bend=30, bendAt=0, wrap=70, wrapAt=0.2), blue_a([[23.962, 38.131], [23.976, 38.136], [23.986, 38.132]], 0.6),
                           blue_a([[23.973, 38.111], [23.985, 38.111], [23.993, 38.117]], 0.8), LOCK("soros", 1.0, "양익 포위")], tilt=34), sfx=PING(1.2))
next_act()

# ===== 제6막 · 배를 불태워라 =====
MID.append(nid())
sc(3, m("plain", "beach", [swarm([[23.985, 38.125], [24.0, 38.124], [24.012, 38.124]], 0.2, 150, 0.6), ships(0)], flight=["plain", "beach"], flightDur=2.4, tilt=32),
   pauseBefore=0.5, chapter={"num": "제6막", "title": "배를 불태워라"}, sfx=SW(0))
sc(3, m("beach", "beach", [zone(GMARSH, "큰 늪", "#3fb6a8", 0), swarm([[24.0, 38.135], [24.012, 38.143], [24.022, 38.15]], 0.3, 90, 0.5)], tilt=32))
sc(3, ai("fire_at_ships"), label=DRAMA, sfx=SEA(0))
sc(3, ai("battle_at_ships"), label=DRAMA, callouts=top("칼리마코스 전사", "red", 1))
sc(2, ai("cynegirus"), label=DRAMA)
sc(2, text("아이스킬로스", "dark", "그의 동생 · 훗날의 비극 작가"))
sc(3, m("beach", "beach", [ships(0, sailOn="나머지", n=12), badge([24.012, 38.119], "배 7척 노획", "#1f5fbf", on="일곱")], tilt=30))
sc(3, ai("epizelus"), label=DRAMA)
sc(2, text("전투 충격", "dark", "헤로도토스 6권 117절 · 에피젤로스 이야기"))
sc(4, bars("전사자 · 헤로도토스의 기록", [{"label": "페르시아", "value": 6400, "display": "약 6,400명", "color": "red", "on": "육천사백"},
                                       {"label": "아테네", "value": 192, "display": "192명", "color": "blue", "on": "백구십이"}]),
   hook={"hud": [HUD("6,400명", "페르시아군 전사자", "헤로도토스", color="#FF3B30", on="육천사백"), HUD("192명", "아테네군 전사자", "헤로도토스", on="백구십이")]})
sc(1, text("33 : 1", "red", "아테네인 1명당 페르시아인 전사자"))
sc(3, reasons("이 숫자는", [{"text": "페르시아 쪽은 부풀렸을 수도", "on": "부풀려"}, {"text": "그리스 쪽은 너무 적을 수도", "on": "너무 적을"},
                         {"text": "그래도 참패", "on": "참패"}]))
sc(1, black("그날은", "끝나지 않았다"))
sc(2, ai("shield_flash"), label=DRAMA)
sc(3, text("반역?", "red", "끝내 밝혀지지 않은 혐의 · 헤로도토스 6권 115절"))
sc(2, m("marathon", "attica", [red_a(FLEET_PH, 0.4), mark("sounion", "dark", on="수니온")], flight=["marathon", "attica"], flightDur=2.6, tilt=18), sfx=SW(0))
sc(3, m("attica", "attica", [red_a(FLEET_PH, 0), LOCK("athens", 0.5, "아테네 · 군대 없음")], tilt=18, hud=True), sfx=PING(0.8))
sc(1, black("전투만큼", "놀라운 일"))
sc(2, ai("march_back"), label=DRAMA)
sc(2, m("attica", "attica", [blue_a(BACK_M, 0.1), badge([23.84, 38.05], "약 40km · 같은 날", "#1f5fbf", on="사십"), mark("athens", "blue", 0.6)], tilt=20))
sc(3, ai("phaleron_wait"), label=DRAMA)
sc(2, ai("datis_turn"), label=DRAMA)
sc(1, m("aegean", "aegean", [red_a(HOME, 0.1)], tilt=12), callouts=low("아시아로 돌아가다"))
sc(2, m("greece", "greece", [blue_a(SPARTA_M, 0.1), mark("sparta", "dark", 0)], tilt=14), callouts=top("스파르타군 2,000명"))
sc(1, text("너무 늦었다", "red"))
sc(3, ai("spartans_view"), label=DRAMA)
next_act()

# ===== 제7막 · 답 =====
sc(3, black("전사자는", "마라톤에 남았다"), pauseBefore=0.5, chapter={"num": "제7막", "title": "답"})
sc(2, ph("soros", marks=[mk("소로스", 0.5, 0.16, "흙무덤")]), label=plabel("soros"))
sc(2, ph("soros_old", marks=[mk("높이 약 9m", 0.5, 0.2, "높이")]), label=plabel("soros_old"))
sc(1, ph("plataean"), label=plabel("plataean"))
sc(1, text("192명의 영웅", "yellow", "영웅으로 받들어지다"))
sc(1, ph("stoa"), label=plabel("stoa"))
sc(3, doc("아이스킬로스의 묘비명", ["작품 이야기는 한 줄도 없다", "그가 마라톤에서 싸웠다는 것", "메디아인이 그의 용기를 안다는 것"], "馬拉松", "고대 『아이스킬로스 전기』", "요지"))
sc(3, ai("runner_rejoice"), label=DRAMA, callouts=top("전설"))
sc(3, cmp("전설", "아테네로 달린 전령", "헤로도토스", "스파르타로 달린 전령", "dark", "blue"))
sc(3, ai("olympics_1896"), label=DRAMA, callouts=top("1896년 · 아테네"))
sc(2, m("plain", "plain", [PPH(0), GPH(0, bend=30, bendAt=0, wrap=70, wrapAt=0)], tilt=30), hook={"question": {"text": QUESTION, "on": "어떻게", "kicker": "■ 답 ■"}})
sc(2, text("기적이 아니었다", "yellow", "결정들이 이어진 사슬"))
sc(3, m("marathon", "marathon", [zone(GMARSH, "늪"), zone(SMARSH, "늪"), unit("herakleion", "그리스군 진영", "blue", 0.2)], tilt=32), callouts=top("첫째 · 땅", "blue"))
sc(3, m("beach", "beach", [ships(0, sailOn="기병이", n=6), PPH(0)], tilt=30), callouts=top("둘째 · 때", "blue"))
sc(2, ranks(G_THIN, P_DEEP, title="셋째 · 달리기", runAt=0))
sc(2, cmp("고리버들 · 아마포", "가볍다", "청동 · 창", "무겁다", "red", "blue"), callouts=top("넷째 · 갑옷", "blue"))
sc(3, ranks(G_THIN, P_DEEP, title="다섯째 · 대형", bendAt=0.3, wrapOn="양 날개"))
sc(2, ai("wings_turn"), label=DRAMA, callouts=top("여섯째 · 규율", "blue"))
sc(1, text("한 가지 더", "dark"))
sc(2, ai("pnyx_vote"), label=DRAMA, callouts=top("아테네 민주정 · 기원전 508년 무렵", "blue"))
sc(2, checklist("마라톤 승리의 이유", [{"text": "땅", "at": 0}, {"text": "때", "at": 0.1}, {"text": "달리기", "at": 0.2}, {"text": "갑옷", "at": 0.3},
                                     {"text": "대형", "at": 0.4}, {"text": "규율", "at": 0.5}, {"text": "자유로운 시민", "on": "자기 도시"}]))
sc(1, black("마라톤으로 전쟁이", "끝나지는 않았다"))
sc(1, m("aegean", "aegean", [red_a(XERXES, 0.1, 1.4), mark("athens", "blue", 0.4)], tilt=12), callouts=top("기원전 480년 · 크세르크세스", "red"))
sc(1, ph("miltiades", pos="50% 35%"), label=plabel("miltiades"))
sc(2, ai("miltiades_paros"), label=DRAMA, callouts=top("기원전 489년 · 파로스섬"))
sc(2, doc("판결", ["피고: 밀티아데스", "벌금: 50탈란톤"], "有罪", "아테네 법정 · 기원전 489년", "헤로도토스 6권 136절 · 요지"))
sc(1, text("빚은 아들이 갚았다", "dark", "키몬"))
sc(4, ai("marathon_dawn"), label=DRAMA)
sc(2, ai("servant_dinner"), label=DRAMA, callouts=low("“주인이시여, 아테네인을 잊지 마소서”", "dark", 1))
sc(1, ph("soros", pos="50% 60%"), label=plabel("soros"))
sc(2, {"type": "endcard", "title": "마라톤을 달린 모든 이들을 기억하며", "q": pin("plain2")}, tail=1.0)
assert CUR["i"] == len(ACTS[6]), (CUR, len(ACTS[6]))
SOMBER_FROM = [s["id"] for s in S if s.get("chapter", {}).get("num") == "제7막"][0]

# ===== 재연 일러스트 (countryball 반실사 + 일부 사실풍 풍경) =====
CB = "Semi-realistic dramatic digital illustration in the style of polished history-YouTube countryball cartoons: "
GR = ("ancient Athenian hoplites whose heads are round balls painted white with a small golden owl emblem, wearing bronze Corinthian helmets with red horsehair crests, "
      "bronze cuirasses and red tunics, carrying large round bronze-faced shields and long spears")
GR1 = ("an ancient Athenian hoplite whose head is a round ball painted white with a small golden owl emblem, wearing a bronze Corinthian helmet with a red horsehair crest, "
       "a bronze cuirass and a red tunic, carrying a large round bronze-faced shield and a long spear")
PE = ("ancient Achaemenid Persian soldiers whose heads are round balls painted deep purple with a small golden winged-disc emblem, wearing soft felt caps, "
      "colorful embroidered tunics and trousers, carrying wicker shields, bows and short spears")
DARIUS = ("an Achaemenid Persian Great King whose head is a round ball painted deep purple with a golden winged-disc emblem, wearing a tall golden crenellated crown, "
          "a long square curled black beard and royal purple robes")
MILT = ("an older Athenian general whose head is a round ball painted white with a small golden owl emblem, with a short grey beard, a bronze Corinthian helmet pushed up on top, "
        "and a red cloak")
HIPP = "a very old exiled Athenian man whose head is a round ball painted white and faded grey, with a long white beard and a Persian-style embroidered robe"
END = ", 490 BC ancient Greece, leaving calm uncluttered dark background area in the upper right, absolutely no speech bubbles, no balloons, no text boxes, no captions, no text, no letters."
LAND_S = "painterly realistic digital illustration, cinematic, desaturated palette, film grain, no people's faces in close-up, no text, no letters."
AI = {
    "persian_host": CB + "a vast army of " + PE + " drawn up on a coastal plain at dawn, dozens of beached triremes behind them, cavalry and archers in the ranks" + END,
    "sardis_burning": CB + "Greek rebels, " + GR + ", setting fire to the reed-roofed houses of the ancient Lydian city of Sardis at night, flames and smoke" + END,
    "darius_arrow": CB + DARIUS + " standing on a palace terrace in Persepolis, angrily shooting an arrow straight up into the sky, courtiers watching" + END,
    "servant_dinner": CB + DARIUS + " seated at a long dinner table in a lamp-lit palace hall while a bowing servant whose head is a round ball painted deep purple speaks to him" + END,
    "horse_transport": CB + "Persian horse-transport ships at sea, horses being led up wooden ramps into broad-hulled ships by " + PE + ", a large fleet of triremes behind" + END,
    "delos_incense": CB + PE + " burning incense on a stone altar in front of a small ancient Greek temple on the sacred island of Delos, calm sea behind" + END,
    "eretria_gates": "Night scene, two cloaked figures secretly opening the heavy wooden gate of an ancient Greek walled city, Persian soldiers waiting in the shadows outside, torches, " + LAND_S,
    "eretria_chains": CB + "captive Greek townspeople being led in chains to the shore by " + PE + ", an ancient walled Greek city smoking behind them" + END,
    "hippias_ship": CB + HIPP + " standing at the bow of a Persian trireme, staring toward a distant coastline, the Persian fleet sailing behind him" + END,
    "assembly_debate": CB + "a crowded ancient Athenian assembly on a rocky hillside, citizens whose heads are round balls painted white with a small golden owl emblem, arguing and raising hands" + END,
    "danube_bridge": CB + "a long bridge of boats across a wide river, " + MILT + " pointing at it and urging other Greek commanders to cut it" + END,
    "miltiades_assembly": CB + MILT + " standing on a stone speaker's platform addressing the Athenian assembly, pointing north, citizens listening" + END,
    "hoplites_neighbors": CB + GR + " of different ages, a farmer, a potter and an olive grower, strapping on their own armor in a village courtyard, families watching" + END,
    "runner_mountains": "A lone ancient Greek runner in a short tunic running along a rocky mountain track at sunrise in the Peloponnese, long shadows, dust, " + LAND_S,
    "plataeans_arrive": CB + "a column of " + GR + " marching down a mountain road into a camp, other hoplites cheering their arrival" + END,
    "felled_trees": CB + GR + " cutting down trees and dragging branches across open ground in front of their hillside camp to block cavalry" + END,
    "hippias_sneeze": CB + HIPP + " sneezing violently on a sandy beach, a single loose tooth flying out, Persian soldiers looking on in surprise" + END,
    "hippias_tooth": CB + HIPP + " kneeling in the sand searching for his lost tooth, sad and resigned, beached Persian ships behind" + END,
    "traitor_gate": "An ancient Athenian city gate at night, a hooded figure waiting in the shadows beside it, distant torches, tension, " + LAND_S,
    "callimachus": CB + "the Athenian war ruler, a stern hoplite commander whose head is a round ball painted white with a small golden owl emblem, wearing a crested bronze helmet and a blue cloak, standing in a hillside camp" + END,
    "miltiades_callimachus": CB + MILT + " earnestly speaking to a stern Athenian commander in a blue cloak inside a tent lit by an oil lamp at night" + END,
    "ionian_deserters": CB + "two Ionian Greek soldiers in Persian service slipping across a dark plain at night toward a hillside camp fire, whispering to an Athenian sentry" + END,
    "horses_loading": CB + "Persian grooms, " + PE + ", leading horses up wooden ramps onto beached transport ships at dawn, the beach busy and disordered" + END,
    "dawn_omens": CB + "an Athenian priest examining a sacrifice at an altar at dawn while " + GR + " stand ready behind him, mist over the plain" + END,
    "saka_warriors": CB + "fierce Saka warriors from the Central Asian steppe whose heads are round balls painted ochre and black, wearing tall pointed caps, holding battle axes and bows" + END,
    "persians_watch": CB + PE + " in a long line staring in disbelief as a distant line of Greek hoplites runs toward them across the plain, some laughing, some pointing" + END,
    "clash": CB + GR + " crashing at full speed into a line of " + PE + ", bronze shields smashing wicker shields, spears and dust" + END,
    "wings_temptation": CB + GR + " on the wing of the battle watching beaten Persian soldiers flee toward beached ships, a few hoplites starting to chase, an officer raising his arm to stop them" + END,
    "wings_turn": CB + "two blocks of " + GR + " wheeling inward from both sides onto a mass of surprised " + PE + " in the middle of a plain, dust clouds" + END,
    "fire_at_ships": CB + GR + " charging into the shallow surf toward beached Persian triremes, holding burning torches and shouting for fire, smoke rising" + END,
    "battle_at_ships": CB + "desperate fighting at the water's edge between " + GR + " and " + PE + " around the sterns of beached triremes, chaos and splashing water" + END,
    "cynegirus": CB + GR1 + " grabbing the curved wooden stern of a Persian trireme as it pulls away from the beach, a Persian sailor raising an axe above" + END,
    "epizelus": CB + GR1 + " standing frozen in the middle of the battle, his hands over his eyes, dust and fighting all around him" + END,
    "shield_flash": "A bright flash of sunlight reflected from a raised bronze shield on a mountainside above a coastal plain, a fleet of ancient ships pulling away from the shore below, " + LAND_S,
    "march_back": CB + "an exhausted column of " + GR + " marching fast along a dusty mountain road in the afternoon heat toward a distant city, carrying their shields" + END,
    "phaleron_wait": CB + GR + " standing in a long line on a beach near Athens in the evening, staring at a Persian fleet anchored offshore" + END,
    "datis_turn": CB + "a Persian admiral whose head is a round ball painted deep purple, standing on the deck of a trireme looking at Greek troops lined up on the distant shore, then turning away" + END,
    "spartans_view": CB + "Spartan hoplites whose heads are round balls painted red with a white lambda emblem, wearing red cloaks and bronze helmets, walking across a quiet battlefield at sunset, a burial mound in the distance" + END,
    "runner_rejoice": CB + GR1 + " collapsing after running into an ancient Athenian marketplace, arms raised, citizens rushing toward him" + END,
    "olympics_1896": "Runners in 1896 athletic clothing on a dusty country road in Greece, spectators in period clothing cheering, sepia tones, " + LAND_S,
    "pnyx_vote": CB + "ancient Athenian citizens whose heads are round balls painted white with a small golden owl emblem, voting by raising their hands on the Pnyx hill, the Acropolis behind" + END,
    "miltiades_paros": CB + MILT + " limping with a bandaged leg away from the walls of an island town, his soldiers retreating to their ships" + END,
    "marathon_dawn": "The quiet plain of Marathon at dawn seen from the hills, a large earthen burial mound in the middle, the bay and the sea beyond, golden light, " + LAND_S,
    "thumb_bg": ("Cinematic photorealistic war painting, 16:9 wide high-angle shot over the plain of Marathon at dawn: a long line of ancient Greek hoplites with round bronze shields "
                 "and red crests running forward in a cloud of dust, both wings of their line curving inward to envelop a dense mass of Persian soldiers with wicker shields, "
                 "dozens of beached triremes and the sea behind, golden backlight, high contrast, dramatic, the lower third of the frame darker, no text, no letters, no logos."),
}
used = {s["visual"]["img"] for s in S if s["visual"]["type"] == "ai"}
assert not used - set(AI), used - set(AI)
assert not set(AI) - used - {"thumb_bg"}, set(AI) - used

# ===== 레이어 교차 검사: 콜드 오프닝(act 1)에서 같은 화면 종류 연속 금지 =====
co = [s["visual"]["type"] for s in S if s["act"] == 1]  # 제1막 = 콜드 오프닝
assert all(a != b for a, b in zip(co, co[1:])), co
# 사진 장면마다 핀 필수 (핀 없으면 엉뚱한 사진이 자동 검색됨)
for s in S:
    if s["visual"].get("q"):
        assert f"{s['visual']['q']}#0" in PINS, s["id"]

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
board = {"title": "달려서 덮쳤다: 마라톤 전투", "subtitle": "기병도 궁수도 없이 제국을 바다로 몰아낸 농민들 · 기원전 490년",
         "lang": "ko", "sub_max": 28, "voice": "Srd5jY77m6kKijR9vy6R", "tempo": 1.02, "tts_mode": "act", "style": 2, "sfx_policy": "doc", "bgm_rel_db": -24, "sync_limit": 0.5,
         "target_sec": 1230, "midrolls": MID, "land": LAND, "places": P, "views": V, "music": music, "ai_images": AI, "scenes": S}
(HERE / "storyboard.json").write_text(json.dumps(board, ensure_ascii=False, indent=1), encoding="utf-8")
say = lambda l: l if isinstance(l, str) else l["say"]
types = collections.Counter(s["visual"]["type"] for s in S)
print("scenes", len(S), "chars", sum(len(say(l)) for s in S for l in s["lines"]), "mid", MID, "chap", [sid(i) for i in chap],
      "ai", len(AI), "pins", len(PINS), dict(types))
