# EP01 (영문 《Map of War》) 마라톤 전투 (기원전 490) 스토리보드 생성기 — 첫 생성용(기록). 나레이션은 script.md 문장을 순서대로 그대로 가져온다.
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
    ("four hundred ninety-nine BC", "499 BC"), ("four hundred ninety-two BC", "492 BC"), ("four hundred ninety BC", "490 BC"),
    ("twenty to twenty-five thousand", "20,000 to 25,000"), ("six thousand four hundred", "6,400"), ("One hundred ninety-two", "192"),
    ("one hundred ninety-two", "192"), ("one hundred fifty miles", "150 miles"), ("six hundred warships", "600 warships"),
    ("Two thousand Spartans", "2,000 Spartans"), ("Two thousand years", "2,000 years"), ("eighteen ninety-six", "1896"),
    ("Ten thousand", "10,000"), ("ten thousand", "10,000"), ("nine thousand", "9,000"), ("one thousand men", "1,000 men"),
    ("five hundred years", "500 years"), ("Thirty-three", "33"), ("twenty-six miles", "26 miles"), ("Seventeen years", "17 years"),
    ("Twenty years", "20 years"), ("next twenty years", "next 20 years"), ("Ten years later", "10 years later"), ("ten years later", "10 years later"),
    ("two to one", "2 to 1"), ("thirty to one", "30 to 1"), ("twenty ships", "20 ships"), ("Eretria sent five", "Eretria sent 5"),
    ("six years", "6 years"), ("three times", "3 times"), ("six days", "6 days"), ("seventh day", "7th day"), ("third day", "3rd day"),
    ("six miles", "6 miles"), ("about sixty years old", "about 60 years old"), ("ten generals", "10 generals"), ("ten tribes", "10 tribes"),
    ("Five said", "5 said"), ("three words", "3 words"), ("eight stades", "8 stades"), ("three feet", "3 feet"), ("fifty pounds", "50 pounds"),
    ("seven ships", "7 ships"), ("thirty feet", "30 feet"), ("fifty talents", "50 talents"),
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
               "Darius I enthroned · Persepolis relief", ("PERSEPOLIS · RELIEF", "c. 500 BC")),
    "archers": ("File:Frieze of Archers from the Palace of Darius I in Susa, Achaemenid Persian Period, reign of Darius I, c. 510 BC, Louvre Museum (12251246605).jpg",
                "Frieze of Archers · Palace of Darius I, Susa (c. 510 BC) · Louvre", ("SUSA · GLAZED BRICK", "c. 510 BC")),
    "guard": ("File:Head of a member of the so-called Immortals, the 1000 special royal guards. Glazed brick. From the East Gate of the Palace at Susa, Iran. Achaemenid period, 521-500 BCE. British Museum.jpg",
              "Persian royal guard · glazed brick, Susa · British Museum", ("SUSA · ROYAL GUARD", "521–500 BC")),
    "marsh": ("File:Marshlands of Marathon, with Pentelikon mountains in the background.jpg", "Marshland at Marathon with Mount Pentelikon behind (2016)", ("MARATHON · MARSHLAND", "2016")),
    "plain1": ("File:Plain of Marathon 1.jpg", "The plain of Marathon today", ("MARATHON · THE PLAIN", "TODAY")),
    "plain2": ("File:Plain of Marathon 2.jpg", "The plain of Marathon today", ("MARATHON · THE PLAIN", "TODAY")),
    "beach": ("File:Marathon beach.jpg", "The beach at Marathon today", ("MARATHON · THE BEACH", "TODAY")),
    "miltiades": ("File:Miltiades (Roman replica).jpg", "Miltiades · Roman copy of a Greek bust · National Gallery of Slovenia", ("MILTIADES", "ROMAN COPY")),
    "helmet": ("File:Helmet of Miltiades the Younger.jpg", "Bronze helmet dedicated by Miltiades at Olympia · Archaeological Museum of Olympia", ("OLYMPIA · BRONZE HELMET", "c. 490 BC")),
    "hoplite": ("File:Athenian hoplite.jpg", "Reconstructed Athenian hoplite equipment · Zappeion exhibition, Athens (2010)", ("RECONSTRUCTION", "2010")),
    "chigi": ("File:Chigi vase detail.jpg", "Hoplites in battle · Chigi vase (c. 650 BC)", ("CHIGI VASE", "c. 650 BC")),
    "herodotus": ("File:Marble bust of Herodotos MET DT11742 (cropped).jpg", "Herodotus · Roman marble bust · Metropolitan Museum of Art", ("HERODOTUS", "ROMAN COPY")),
    "stoa": ("File:Miltiades fighting the Persians at the Battle of Marathon in the Stoa Poikile (reconstitution).jpg",
             "Battle of Marathon painting in the Stoa Poikile · modern reconstruction", ("STOA POIKILE · RECONSTRUCTION", "ATHENS")),
    "soros": ("File:The burial mound of the Athenians at Marathon on Januray 15, 2019.jpg", "The Soros · burial mound of the Athenians at Marathon (2019)", ("THE SOROS", "2019")),
    "soros_old": ("File:Great Tumulus in the plain of Marathon - Dodwell Edward - 1819.jpg", "The great tumulus at Marathon · Edward Dodwell (1819)", ("EDWARD DODWELL", "1819")),
    "plataean": ("File:The burial mound of the Plataeans in Marathon on January 15, 2019.jpg", "Burial mound of the Plataeans at Marathon (2019)", ("TUMULUS OF THE PLATAEANS", "2019")),
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


DRAMA = "Dramatization"
# 좌표는 개략 (전열 위치·늪 범위·함선 위치는 통설 재구성 기준 모식 배치)
P = {
    "athens": [23.727, 37.972, "Athens"], "phaleron": [23.68, 37.935, "Phaleron"], "sounion": [24.026, 37.651, "Cape Sounion"],
    "eretria": [23.795, 38.395, "Eretria"], "plataea": [23.27, 38.215, "Plataea"], "thebes": [23.32, 38.32, "Thebes"], "sparta": [22.43, 37.075, "Sparta"],
    "naxos": [25.38, 37.1, "Naxos"], "delos": [25.268, 37.396, "Delos"], "carystus": [24.42, 38.015, "Carystus"], "paros": [25.15, 37.08, "Paros"],
    "sardis": [28.04, 38.49, "Sardis"], "miletus": [27.278, 37.53, "Miletus"], "athos": [24.33, 40.157, "Mount Athos"], "samos": [26.95, 37.73, "Samos"],
    "chersonese": [26.45, 40.35, "Thracian Chersonese"], "susa": [48.25, 32.19, "Susa"], "persepolis": [52.89, 29.935, "Persepolis"],
    "babylon": [44.42, 32.54, "Babylon"], "indus": [67.6, 26.2, "Indus"],
    "marathon": [23.98, 38.125, "Marathon"], "soros": [23.9783, 38.1186, "Soros"], "herakleion": [23.948, 38.128, "Herakleion · Greek camp"],
    "gmarsh": [24.022, 38.148, "Great Marsh"], "smarsh": [23.998, 38.1, "Small Marsh"], "pcamp": [24.018, 38.138, "Persian camp"],
    "pentelikon": [23.885, 38.05, "Mt Pentelikon"], "agrieliki": [23.955, 38.098, "Mt Agrieliki"], "kotroni": [23.935, 38.158, "Mt Kotroni"],
}
V = {
    "empire": {"center": [46.5, 30.0], "span": 50}, "aegean": {"center": [25.4, 38.6], "span": 8.5}, "ionia": {"center": [26.6, 38.2], "span": 4.6},
    "greece": {"center": [23.3, 37.85], "span": 3.4}, "attica": {"center": [23.8, 38.08], "span": 1.5},
    "marathon": {"center": [23.99, 38.125], "span": 0.16}, "plain": {"center": [23.985, 38.124], "span": 0.085}, "beach": {"center": [24.015, 38.13], "span": 0.075},
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
SMARSH = [[23.988, 38.104], [24.0, 38.109], [24.012, 38.101], [24.003, 38.092], [23.99, 38.095]]
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
QUESTION = "How did citizen-farmer hoplites\nwith no cavalry or archers\ndrive the world's largest empire into the sea?"

# ===== ACT 1 · 콜드 오프닝 (후킹 표준: 0~10초 사건 직격 → 10~40초 모순 3단 → X 반전 → 중앙 질문 카드 → 타이틀) =====
# 레이어 교차: 3D 비행 → 병력 대열 → 재연 그림 → 3D 전열 → 사료 사진 → 비교 카드 → 병력 대열(돌격) → X → 질문 카드 → 타이틀
sc(2, m("attica", "marathon", [LOCK("soros", 0.9, "MARATHON")], flight=["aegean", "attica", "marathon"], flightDur=4.2, hud=True, tilt=26),
   hook={"hud": [HUD("490 BC", "The plain of Marathon", "26 miles from Athens", count=False)]}, sfx=SW(0) + PING(1.2))
sc(1, ranks([6] * 12, title="ONE LINE OF BRONZE"), hook={"hud": [HUD("10,000", "Athenian & Plataean hoplites", "approximate", on="Ten thousand")]})
sc(1, ai("persian_host"), label=DRAMA, hook={"hud": [HUD("20,000–25,000", "Persian landing force", "modern estimates · ancient sources: far more", color="#FF3B30", on="largest")]}, sfx=WIND(0.1))
sc(1, m("plain", "plain", [PPH(0), GPH(0, run=60, runOn="run"), badge("soros", "AT A RUN", "#c9242c", on="run", dy=-90)], tilt=30))
sc(2, ph("archers", pos="50% 40%", marks=[mk("ARCHERS", 0.5, 0.18, "archers", "red"), mk("GREEK CAVALRY: 0", 0.5, 0.82, "neither", "yellow")]), label=plabel("archers"),
   hook={"hud": [HUD("0", "Greek cavalry · Greek archers", "at Marathon", color="#FF3B30", on="neither", count=False)]})
sc(2, cmp("MEN IN THE FIELD", "1 : 2", "DEAD BY SUNSET", "33 : 1", "blue", "red"))
sc(2, ranks(G_THIN, P_DEEP, title="NO WALKING", runOn="ran"), hook={"hud": [HUD("8 STADES", "of open ground · about a mile", "crossed at a run", on="ran", count=False)]})
sc(3, black("A LUCKY", "MIRACLE?"), hook={"neg": {"text": "A LUCKY MIRACLE", "on": "miracle", "xOn": "Or was it"}})
sc(1, m("plain", "plain", [PPH(0), GPH(0)], tilt=30), hook={"question": {"text": QUESTION, "at": 0.02}})
sc(1, {"type": "titlecard", "title": "THEY CHARGED AT A RUN", "sub": "The Battle of Marathon · 490 BC", "at": 0, "q": pin("plain1")}, flash=True)
next_act()

# ===== ACT 2 · THE KING WHO REMEMBERED =====
sc(2, ph("darius", pos="50% 35%", marks=[mk("DARIUS I", 0.5, 0.16, "Darius")]), label=plabel("darius"), chapter={"num": "ACT 2", "title": "THE KING WHO REMEMBERED"})
sc(1, m("empire", "empire", [line(EMPIRE, 0.1, "#ff3b30"), mark("persepolis", "red", 0.4), mark("susa", "red", 0.6), mark("indus", "dark", on="Indus")], tilt=10),
   callouts=top("THE ACHAEMENID PERSIAN EMPIRE · c. 500 BC", "red"))
sc(1, text("PERHAPS 1 IN 3", "red", "of all people on Earth · modern estimate"))
sc(2, m("aegean", "ionia", [unit("miletus", "IONIAN REVOLT", "blue", 0.2, pulse=True), mark("sardis", "red", 0.5)], flight=["aegean", "ionia"], flightDur=2.6),
   callouts=top("499 BC · IONIA"), sfx=SW(0))
sc(1, m("aegean", "aegean", [blue_a(IONIA_HELP[:3], 0.3), mark("athens", "blue", 0), mark("eretria", "blue", 0.2)]))
sc(2, bars("Ships sent to help the revolt", [{"label": "Athens", "value": 20, "display": "20 ships", "color": "blue", "on": "twenty"},
                                             {"label": "Eretria", "value": 5, "display": "5 ships", "color": "blue", "on": "five"}]))
sc(2, ai("sardis_burning"), label=DRAMA, callouts=low("498 BC · SARDIS BURNS"))
sc(1, text("6 YEARS", "dark", "to crush the Ionian revolt · 499–493 BC"))
sc(1, black("BUT DARIUS", "DID NOT FORGET"))
sc(2, ai("darius_arrow"), label=DRAMA)
sc(2, ai("servant_dinner"), label=DRAMA, callouts=low("“MASTER, REMEMBER THE ATHENIANS”", "dark", 1))
sc(2, m("aegean", "aegean", [red_a(FLEET_492, 0.1), {"k": "shock", "pts": ["athos"], "at": 1.2, "period": 0.8}, mark("athos", "dark", on="Athos")], tilt=16),
   callouts=top("492 BC · MOUNT ATHOS"))
sc(2, black("DARIUS", "TRIED AGAIN"))
sc(1, text("600 WARSHIPS", "red", "according to Herodotus"))
sc(1, bars("Persian landing force · modern estimates", [{"label": "Low", "value": 20000, "display": "20,000", "color": "red", "on": "twenty"},
                                                        {"label": "High", "value": 25000, "display": "25,000", "color": "red", "on": "twenty-five"}]))
sc(3, ai("horse_transport"), label=DRAMA)
sc(1, ph("guard", pos="50% 30%"), label=plabel("guard"), callouts=top("DATIS & ARTAPHERNES"))
sc(2, doc("THE KING'S ORDERS", ["Enslave Athens", "Enslave Eretria", "Bring the prisoners to the king"], "ROYAL", "Herodotus 6.94", "Summary"))
sc(2, m("aegean", "aegean", [red_a(FLEET_490[:4], 0.1), mark("naxos", "red", on="Naxos"), mark("delos", "dark", 0.6)], tilt=14), callouts=low("490 BC · ISLAND BY ISLAND"))
sc(2, ai("delos_incense"), label=DRAMA)
sc(2, text("GENEROUS", "yellow", "to those who submitted"))
sc(2, m("aegean", "attica", [red_a(FLEET_490[3:], 0.2), LOCK("eretria", 1.2)], flight=["aegean", "attica"], flightDur=2.6, hud=True), callouts=top("SIEGE OF ERETRIA · 6 DAYS", "red"),
   sfx=SW(0) + PING(1.4))
sc(1, ai("eretria_gates"), label=DRAMA)
sc(2, ai("eretria_chains"), label=DRAMA)
sc(1, black("ERETRIA", "WAS GONE"))
sc(1, m("attica", "attica", [mark("eretria", "dark", 0), line([[23.795, 38.39], [23.86, 38.3], [23.95, 38.16]], 0.2, "#ff3b30"), mark("athens", "blue", 0.5)], tilt=20),
   callouts=low("ACROSS A NARROW STRAIT"))
sc(2, ai("hippias_ship"), label=DRAMA)
sc(1, text("HIPPIAS", "dark", "Former tyrant of Athens · expelled 510 BC"))
sc(2, reasons("IF ATHENS FELL", [{"text": "Hippias returns", "on": "Hippias"}, {"text": "Rules as the king's servant", "on": "servant"}]))
sc(3, m("attica", "marathon", [zone(GMARSH, None, at=1.2), mark("marathon", "red", 0.4)], flight=["attica", "marathon"], flightDur=3.0, tilt=24), callouts=top("THE EAST COAST OF ATTICA"), sfx=SW(0))
sc(2, ph("marsh", marks=[mk("MARATHON = “FENNEL”", 0.5, 0.18, "fennel")]), label=plabel("marsh"))
next_act()

# ===== ACT 3 · THE PLAIN OF FENNEL =====
MID = [nid()]
sc(2, m("marathon", "marathon", [zone(GMARSH, None, at=0.6)], tilt=34, hud=True), pauseBefore=0.5, chapter={"num": "ACT 3", "title": "THE PLAIN OF FENNEL"}, sfx=SEA(0))
sc(2, m("marathon", "marathon", [zone(GMARSH, "GREAT MARSH", on="great marsh"), zone(SMARSH, "SMALL MARSH", "#3fb6a8", on="smaller marsh")], tilt=34))
sc(1, m("marathon", "marathon", [zone(GMARSH, "GREAT MARSH"), zone(SMARSH, "SMALL MARSH"), badge("agrieliki", "MOUNTAINS", "#111", 0.3), badge("kotroni", "MOUNTAINS", "#111", 0.5)], tilt=34))
sc(1, m("marathon", "marathon", [line(ROAD_S, 0.1), line(ROAD_N, 0.4), badge("herakleion", "ROADS TO ATHENS", "#111", 0.6, -80)], tilt=30))
sc(2, cmp("FOR CAVALRY", "PERFECT", "FOR ATHENS", "NIGHTMARE", "red", "dark"))
sc(3, ai("assembly_debate"), label=DRAMA)
sc(2, black("WALLS HAD NOT", "SAVED ERETRIA"))
sc(3, ph("miltiades", pos="50% 30%", marks=[mk("MILTIADES", 0.5, 0.15, "Miltiades")]), label=plabel("miltiades"))
sc(3, m("aegean", "aegean", [unit("chersonese", "MILTIADES' COLONY", "blue", 0.1, pulse=True), mark("sardis", "red", 0.5)], tilt=12), callouts=top("THE HELLESPONT"))
sc(2, ai("danube_bridge"), label=DRAMA)
sc(3, text("HE KNEW HOW IT FOUGHT", "yellow", "and what it feared"))
sc(3, m("aegean", "aegean", [dash_r([[26.45, 40.35], [25.6, 39.8], [24.6, 38.8], [23.727, 37.972]], 0.1), mark("athens", "blue", 0.6)], tilt=12), callouts=low("493 BC · CHASED TO ATHENS"))
sc(2, doc("CHARGE: TYRANNY", ["Defendant: Miltiades", "Verdict: acquitted"], "ACQUITTED", "Athenian court · 493 BC", "Herodotus 6.104 · summary"))
sc(2, ai("miltiades_assembly"), label=DRAMA)
sc(1, ph("hoplite", pos="50% 35%", marks=[mk("SHIELD", 0.35, 0.6, "shield"), mk("SPEAR", 0.7, 0.3, "spear", "red"), mk("BRONZE HELMET", 0.5, 0.14, "helmet")]), label=plabel("hoplite"))
sc(2, reasons("WHO THEY WERE", [{"text": "Farmers", "on": "farmers"}, {"text": "Potters", "on": "potters"}, {"text": "Olive growers", "on": "olive"}, {"text": "Shopkeepers", "on": "shopkeepers"}]))
sc(2, ai("hoplites_neighbors"), label=DRAMA, hudCta={"at": 0, "dur": 7.0})
sc(1, m("attica", "attica", [blue_a(ATH_M, 0.2), mark("athens", "blue", 0), mark("marathon", "red", 0.6)], tilt=20), callouts=top("≈9,000 ATHENIANS MARCH", "blue"))
sc(2, m("greece", "greece", [line(RUN_SP, 0.2, "#ffd400", on="runner"), mark("athens", "blue", 0), mark("sparta", "dark", 0.6)], tilt=14), callouts=low("PHILIPPIDES"))
sc(2, ai("runner_mountains"), label=DRAMA, callouts=top("≈150 MILES · REACHED SPARTA THE NEXT DAY"))
sc(3, doc("SPARTA'S ANSWER", ["Yes", "But not before the full moon"], "SPARTA", "Herodotus 6.106", "Summary"))
sc(2, text("≈6 DAYS", "red", "until the full moon"))
sc(2, black("ATHENS ALONE", "OR ALMOST"))
sc(2, ai("plataeans_arrive"), label=DRAMA)
sc(1, m("attica", "attica", [blue_a(PLAT_M, 0.1), mark("plataea", "blue", 0), mark("thebes", "dark", 0.4)], tilt=18), callouts=top("PLATAEA · ≈1,000 MEN", "blue"))
sc(2, {"type": "flatmap", "center": [23.5, 38.1], "span": 1.7, "fill": {"300": "#f1e4c6"},
                 "pins": [{"ll": [23.27, 38.215], "text": "Plataea", "side": "below", "at": 0}, {"ll": [23.32, 38.32], "text": "Thebes", "side": "right", "on": "Thebes"},
                          {"ll": [23.727, 37.972], "text": "Athens", "side": "below", "at": 0.3}],
                 "routes": [{"from": [23.727, 37.972], "to": [23.27, 38.215], "bend": 0.2, "dur": 1.4, "label": "Protection", "on": "protected"}], "labels": [], "zoomTo": 0.92})
sc(1, bars("The Greek army at Marathon (approx.)", [{"label": "Athenians", "value": 9000, "display": "≈9,000", "color": "blue", "at": 0},
                                                    {"label": "Plataeans", "value": 1000, "display": "≈1,000", "color": "blue", "at": 0.3},
                                                    {"label": "Total", "value": 10000, "display": "≈10,000", "color": "dark", "on": "ten thousand"}]))
sc(2, m("marathon", "marathon", [unit("herakleion", "GREEK CAMP", "blue", 0.1, pulse=True), line(ROAD_S, 0.5, "#2e66d8")], tilt=30), callouts=top("SANCTUARY OF HERACLES"))
sc(2, ai("felled_trees"), label=DRAMA)
sc(2, m("beach", "beach", [ships(0), unit("pcamp", "PERSIAN CAMP", "red", 0.6, pulse=True), zone(GMARSH, "GREAT MARSH", at=0.9)], tilt=32), sfx=SEA(0))
sc(3, ai("hippias_sneeze"), label=DRAMA)
sc(3, ai("hippias_tooth"), label=DRAMA, callouts=low("“THIS LAND IS NOT OURS.”", "dark", 1))
next_act()

# ===== ACT 4 · FIVE VOTES AGAINST FIVE =====
sc(3, m("marathon", "marathon", [unit("herakleion", "GREEKS", "blue", 0.1), unit("pcamp", "PERSIANS", "red", 0.4), ships(0.2)], tilt=30, hud=True),
   chapter={"num": "ACT 4", "title": "FIVE VOTES AGAINST FIVE"}, callouts=top("STANDOFF · SEVERAL DAYS"))
sc(3, reasons("WHY THE GREEKS WAITED", [{"text": "Sparta was coming", "on": "Sparta"}, {"text": "Open ground favored horse and bow", "on": "open ground"}]))
sc(3, ai("traitor_gate"), label=DRAMA, callouts=low("WHY PERSIA WAITED"))
sc(3, ranks([1] * 10, title="10 GENERALS", labels=[lab(0.5, 0.3, "1 per tribe · 1 day of command each", "dark", on="turn")]))
sc(3, bars("The ten generals", [{"label": "Wait", "value": 5, "display": "5", "color": "blue", "on": "wait"}, {"label": "Attack", "value": 5, "display": "5", "color": "red", "on": "attack"}]))
sc(3, ai("callimachus"), label=DRAMA, callouts=top("THE POLEMARCH CALLIMACHUS"))
sc(2, ai("miltiades_callimachus"), label=DRAMA)
sc(4, doc("TO CALLIMACHUS", ["Enslave Athens or make her free", "Wait and the city will split", "Fight now and we can win"], "VOTE", "Herodotus 6.109", "Paraphrase"))
sc(1, bars("The deciding vote", [{"label": "Wait", "value": 5, "display": "5", "color": "blue", "at": 0}, {"label": "Attack", "value": 6, "display": "6", "color": "red", "on": "fight"}]))
sc(4, text("HE WAITED", "yellow", "for his own day of command"))
sc(3, black("WHY DID", "HE WAIT?"))
sc(4, checklist("THE GREEK ARMY", [{"text": "Heavy infantry", "on": "Heavy"}, {"text": "Cavalry", "on": "No cavalry", "checkOn": "No cavalry", "bad": True},
                                   {"text": "Archers", "on": "No archers", "checkOn": "No archers", "bad": True}]))
sc(2, ph("archers", pos="50% 55%"), label=plabel("archers"), callouts=top("PERSIA HAD BOTH", "red"))
sc(1, text("A STRANGE STORY", "dark", "The Suda · Byzantine dictionary · c. AD 1000"))
sc(1, ai("ionian_deserters"), label=DRAMA)
sc(2, doc("A MESSAGE IN THE NIGHT", ["“The cavalry are away.”"], "?", "The Suda (chōris hippeis)", "Late source · disputed"))
sc(3, black("WAS IT", "TRUE?"))
sc(3, m("marathon", "attica", [dash_r(FLEET_PH, 0.6), mark("phaleron", "red", 1.2), mark("athens", "blue", 1.4)], flight=["marathon", "attica"], flightDur=2.6),
   callouts=top("ONE THEORY · SAIL FOR PHALERON", "red"), sfx=SW(0))
sc(2, ai("horses_loading"), label=DRAMA)
sc(2, m("beach", "beach", [ships(0, sailOn="splitting", n=6), unit("pcamp", "CAVALRY BOARDING?", "red", 0.2, pulse=True), PPH(0.4)], tilt=30), callouts=low("THEORY · NOT PROVEN"))
sc(2, ai("dawn_omens"), label=DRAMA, sfx=WIND(0))
sc(2, m("marathon", "plain", [blue_a([[23.948, 38.128], [23.958, 38.124], [23.966, 38.121]], 0.3), GPH(0.9)], flight=["marathon", "plain"], flightDur=2.4, tilt=30),
   callouts=top("DAWN · THE GREEKS DESCEND"), sfx=SW(0))
next_act()

# ===== ACT 5 · EIGHT STADES AT A RUN =====
MID.append(nid())
sc(3, ranks([8] * 6, [4] * 12, title="THE PROBLEM", labels=[lab(0.5, 0.2, "PERSIAN LINE: LONGER", "red", on="longer"), lab(0.5, 0.6, "WRAPPED AROUND BOTH ENDS", "dark", on="wrap")]),
   pauseBefore=0.5, chapter={"num": "ACT 5", "title": "EIGHT STADES AT A RUN"})
sc(5, ranks(G_THIN, [4] * 12, title="BREAKING THE RULES", labels=[lab(0.5, 0.6, "THIN CENTER", "red", on="thinned"), lab(0.15, 0.6, "STRONG WING", "blue", on="wings"),
                                                                    lab(0.85, 0.6, "STRONG WING", "blue", on="wings")]))
sc(3, m("plain", "plain", [GPH(0), badge([23.973, 38.111], "CALLIMACHUS", "#1f5fbf", on="right"), badge([23.962, 38.131], "PLATAEANS", "#1f5fbf", on="Plataeans")], tilt=32))
sc(3, text("THEMISTOCLES · ARISTIDES", "dark", "in the thin center · according to Plutarch"))
sc(1, text("THE NEXT 20 YEARS", "yellow", "Salamis · Plataea · the Athenian empire"))
sc(2, m("plain", "plain", [GPH(0), PPH(0.2, text="PERSIANS & SAKA")], tilt=32))
sc(2, ai("saka_warriors"), label=DRAMA)
sc(2, m("plain", "plain", [GPH(0), PPH(0), line([[23.968, 38.121], [23.991, 38.128]], 0.3, "#ffffff"), badge("soros", "8 STADES ≈ 1 MILE", "#111", on="eight", dy=-60)], tilt=32))
sc(1, black("THEN CAME", "THE MOMENT"))
sc(2, black("THE GREEKS DID NOT WALK", "THEY RAN"), sfx=WIND(0))
sc(2, ph("chigi", pos="50% 50%", marks=[mk("SHIELD ≈ 3 FT ACROSS", 0.5, 0.2, "shield")]), label=plabel("chigi"))
sc(1, ph("helmet", pos="50% 45%", marks=[mk("BRONZE HELMET", 0.5, 0.82, "helmet")]), label=plabel("helmet"))
sc(1, text("50+ POUNDS", "red", "estimated weight of a hoplite's equipment"))
sc(3, ranks([5] * 12, title="THE SHIELD WALL", runOn="Running", labels=[lab(0.5, 0.28, "EACH SHIELD COVERS THE MAN ON THE LEFT", "dark", on="covered")]))
sc(3, ai("persians_watch"), label=DRAMA, callouts=low("“MADNESS”", "red", 1))
sc(3, reasons("WHY RUN?", [{"text": "Arrows fill the air", "on": "arrows"}, {"text": "Less time in the killing ground", "on": "faster"}]))
sc(2, m("plain", "plain", [PPH(0), GPH(0, run=55, runOn="run"), badge([23.98, 38.124], "INSIDE BOWSHOT", "#c9242c", on="bowshot", dy=-50)], tilt=32), sfx=PING(1.2))
sc(3, doc("HERODOTUS 6.112", ["First Greeks to charge at a run", "First to face Persian dress without fear"], "RECORD", "Herodotus · Histories", "Paraphrase"))
sc(1, ai("clash"), label=DRAMA, sfx=WIND(0))
sc(3, cmp("PERSIAN", "WICKER · LINEN", "GREEK", "BRONZE · WOOD", "red", "blue"))
sc(5, ranks(G_THIN, P_DEEP, title="THE CENTER", bendOn="broke", labels=[lab(0.5, 0.6, "THE CENTER BREAKS", "red", on="broke")]))
sc(1, black("THE OLD STORY", "REPEATING?"))
sc(3, m("plain", "plain", [GPH(0, bend=30, bendAt=0), PPH(0), swarm([[23.99, 38.135], [24.0, 38.137], [24.012, 38.132]], 1.0, 70, 0.4),
                           swarm([[23.993, 38.116], [24.004, 38.118], [24.012, 38.124]], 1.2, 70, 0.4)], tilt=32), callouts=top("THE WINGS WIN", "blue"))
sc(2, ai("wings_temptation"), label=DRAMA)
sc(3, checklist("EVERY INSTINCT SAID", [{"text": "Chase them", "on": "chase"}, {"text": "Kill them on the beach", "on": "Kill"}, {"text": "Take the loot", "on": "loot"}]))
sc(1, black("THEY", "DID NOT"))
sc(4, ranks(G_THIN, P_DEEP, title="THE TRAP", bendAt=0, wrapOn="turned", labels=[lab(0.5, 0.6, "THE WINGS TURN INWARD", "blue", on="turned")]))
sc(1, ai("wings_turn"), label=DRAMA)
sc(2, m("plain", "plain", [PPH(0), GPH(0, bend=30, bendAt=0, wrap=70, wrapAt=0.2), blue_a([[23.962, 38.131], [23.976, 38.136], [23.986, 38.132]], 0.6),
                           blue_a([[23.973, 38.111], [23.985, 38.111], [23.993, 38.117]], 0.8), LOCK("soros", 1.0, "DOUBLE ENVELOPMENT")], tilt=34), sfx=PING(1.2))
next_act()

# ===== ACT 6 · FIRE AT THE SHIPS =====
MID.append(nid())
sc(3, m("plain", "beach", [swarm([[23.985, 38.125], [24.0, 38.124], [24.012, 38.124]], 0.2, 150, 0.6), ships(0)], flight=["plain", "beach"], flightDur=2.4, tilt=32),
   pauseBefore=0.5, chapter={"num": "ACT 6", "title": "FIRE AT THE SHIPS"}, sfx=SW(0))
sc(3, m("beach", "beach", [zone(GMARSH, "GREAT MARSH", "#3fb6a8", 0), swarm([[24.0, 38.135], [24.012, 38.143], [24.022, 38.15]], 0.3, 90, 0.5)], tilt=32))
sc(3, ai("fire_at_ships"), label=DRAMA, sfx=SEA(0))
sc(3, ai("battle_at_ships"), label=DRAMA, callouts=top("CALLIMACHUS KILLED", "red", 1))
sc(2, ai("cynegirus"), label=DRAMA)
sc(2, text("AESCHYLUS", "dark", "his brother · the future playwright"))
sc(3, m("beach", "beach", [ships(0, sailOn="rest", n=12), badge([24.012, 38.119], "7 SHIPS CAPTURED", "#1f5fbf", on="seven")], tilt=30))
sc(3, ai("epizelus"), label=DRAMA)
sc(2, text("THE SHOCK OF COMBAT", "dark", "Herodotus 6.117 · the story of Epizelus"))
sc(4, bars("The dead · according to Herodotus", [{"label": "Persians", "value": 6400, "display": "≈6,400", "color": "red", "on": "six thousand"},
                                                 {"label": "Athenians", "value": 192, "display": "192", "color": "blue", "on": "ninety-two"}]),
   hook={"hud": [HUD("6,400", "Persian dead", "Herodotus", color="#FF3B30", on="six thousand"), HUD("192", "Athenian dead", "Herodotus", on="ninety-two")]})
sc(1, text("33 : 1", "red", "Persian dead for every Athenian"))
sc(3, reasons("THE NUMBERS", [{"text": "Persian figure may be rounded up", "on": "rounded"}, {"text": "Greek figure may be too low", "on": "too low"},
                              {"text": "Still a crushing defeat", "on": "crushing"}]))
sc(1, black("THE DAY", "WAS NOT OVER"))
sc(2, ai("shield_flash"), label=DRAMA)
sc(3, text("TREASON?", "red", "accusation never proved · Herodotus 6.115"))
sc(2, m("marathon", "attica", [red_a(FLEET_PH, 0.4), mark("sounion", "dark", on="Sounion")], flight=["marathon", "attica"], flightDur=2.6, tilt=18), sfx=SW(0))
sc(3, m("attica", "attica", [red_a(FLEET_PH, 0), LOCK("athens", 0.5, "ATHENS · NO ARMY")], tilt=18, hud=True), sfx=PING(0.8))
sc(1, black("ALMOST AS REMARKABLE", "AS THE BATTLE"))
sc(2, ai("march_back"), label=DRAMA)
sc(2, m("attica", "attica", [blue_a(BACK_M, 0.1), badge([23.84, 38.05], "≈26 MILES · SAME DAY", "#1f5fbf", on="twenty-six"), mark("athens", "blue", 0.6)], tilt=20))
sc(3, ai("phaleron_wait"), label=DRAMA)
sc(2, ai("datis_turn"), label=DRAMA)
sc(1, m("aegean", "aegean", [red_a(HOME, 0.1)], tilt=12), callouts=low("BACK TO ASIA"))
sc(2, m("greece", "greece", [blue_a(SPARTA_M, 0.1), mark("sparta", "dark", 0)], tilt=14), callouts=top("2,000 SPARTANS"))
sc(1, text("TOO LATE", "red"))
sc(3, ai("spartans_view"), label=DRAMA)
next_act()

# ===== ACT 7 · THE ANSWER =====
sc(3, black("THE DEAD", "STAYED AT MARATHON"), pauseBefore=0.5, chapter={"num": "ACT 7", "title": "THE ANSWER"})
sc(2, ph("soros", marks=[mk("THE SOROS", 0.5, 0.16, "mound")]), label=plabel("soros"))
sc(2, ph("soros_old", marks=[mk("≈30 FEET HIGH", 0.5, 0.2, "thirty")]), label=plabel("soros_old"))
sc(1, ph("plataean"), label=plabel("plataean"))
sc(1, text("192 HEROES", "yellow", "honored with a hero cult"))
sc(1, ph("stoa"), label=plabel("stoa"))
sc(3, doc("EPITAPH OF AESCHYLUS", ["No word of his plays", "Only: he fought at Marathon", "The long-haired Mede knew it"], "MARATHON", "Ancient Life of Aeschylus",
          "Paraphrase"))
sc(3, ai("runner_rejoice"), label=DRAMA, callouts=top("LEGEND"))
sc(3, cmp("THE LEGEND", "RUNNER TO ATHENS", "HERODOTUS", "RUNNER TO SPARTA", "dark", "blue"))
sc(3, ai("olympics_1896"), label=DRAMA, callouts=top("1896 · ATHENS"))
sc(2, black(" "), hook={"question": {"text": QUESTION, "on": "How did", "kicker": "■ THE ANSWER ■"}})
sc(2, text("NOT A MIRACLE", "yellow", "a chain of decisions"))
sc(3, m("marathon", "marathon", [zone(GMARSH, "MARSH"), zone(SMARSH, "MARSH"), unit("herakleion", "GREEK CAMP", "blue", 0.2)], tilt=32), callouts=top("1 · THE GROUND", "blue"))
sc(3, m("beach", "beach", [ships(0, sailOn="cavalry", n=6), PPH(0)], tilt=30), callouts=top("2 · THE TIMING", "blue"))
sc(2, ranks(G_THIN, P_DEEP, title="3 · THE RUN", runAt=0))
sc(2, cmp("WICKER · LINEN", "LIGHT", "BRONZE · SPEAR", "HEAVY", "red", "blue"), callouts=top("4 · THE ARMOR", "blue"))
sc(3, ranks(G_THIN, P_DEEP, title="5 · THE FORMATION", bendAt=0.3, wrapOn="wings"))
sc(2, ai("wings_turn"), label=DRAMA, callouts=top("6 · DISCIPLINE", "blue"))
sc(1, text("ONE MORE THING", "dark"))
sc(2, ai("pnyx_vote"), label=DRAMA, callouts=top("ATHENIAN DEMOCRACY · c. 508 BC", "blue"))
sc(2, checklist("WHY MARATHON WAS WON", [{"text": "The ground", "at": 0}, {"text": "The timing", "at": 0.1}, {"text": "The run", "at": 0.2}, {"text": "The armor", "at": 0.3},
                                          {"text": "The formation", "at": 0.4}, {"text": "Discipline", "at": 0.5}, {"text": "Free citizens", "on": "own city"}]))
sc(1, black("MARATHON DID NOT", "END THE WAR"))
sc(1, m("aegean", "aegean", [red_a(XERXES, 0.1, 1.4), mark("athens", "blue", 0.4)], tilt=12), callouts=top("480 BC · XERXES", "red"))
sc(1, ph("miltiades", pos="50% 35%"), label=plabel("miltiades"))
sc(2, ai("miltiades_paros"), label=DRAMA, callouts=top("489 BC · PAROS"))
sc(2, doc("VERDICT", ["Defendant: Miltiades", "Fine: 50 talents"], "GUILTY", "Athenian court · 489 BC", "Herodotus 6.136 · summary"))
sc(1, text("HIS SON PAID THE DEBT", "dark", "Cimon"))
sc(4, ai("marathon_dawn"), label=DRAMA)
sc(2, ai("servant_dinner"), label=DRAMA, callouts=low("“MASTER, REMEMBER THE ATHENIANS”", "dark", 1))
sc(1, ph("soros", pos="50% 60%"), label=plabel("soros"))
sc(2, {"type": "endcard", "title": "To the men who ran at Marathon", "q": pin("plain2")}, tail=1.0)
assert CUR["i"] == len(ACTS[6]), (CUR, len(ACTS[6]))
SOMBER_FROM = [s["id"] for s in S if s.get("chapter", {}).get("num") == "ACT 7"][0]

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
co = [s["visual"]["type"] for s in S if s["act"] == 1]
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
board = {"title": "They Charged at a Run: The Battle of Marathon (490 BC)", "subtitle": "How Greek farmers drove an empire into the sea · 490 BC",
         "lang": "en", "voice": "Srd5jY77m6kKijR9vy6R", "tempo": 1.02, "tts_mode": "act", "style": 2, "sfx_policy": "doc", "bgm_rel_db": -24, "sync_limit": 0.5,
         "target_sec": 1230, "midrolls": MID, "land": LAND, "places": P, "views": V, "music": music, "ai_images": AI, "scenes": S}
(HERE / "storyboard.json").write_text(json.dumps(board, ensure_ascii=False, indent=1), encoding="utf-8")
say = lambda l: l if isinstance(l, str) else l["say"]
types = collections.Counter(s["visual"]["type"] for s in S)
print("scenes", len(S), "chars", sum(len(say(l)) for s in S for l in s["lines"]), "mid", MID, "chap", [sid(i) for i in chap],
      "ai", len(AI), "pins", len(PINS), dict(types))
