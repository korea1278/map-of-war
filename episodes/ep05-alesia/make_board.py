# EP05 (한국어 《격전의 세계사》) 알레시아 공방전 (기원전 52) 스토리보드 생성기 — 첫 생성용(기록). 나레이션은 script.md 문장을 순서대로 그대로 가져온다.
# ⚠️ storyboard.json을 손으로 고친 뒤에는 다시 돌리지 말 것 (수정 사항이 덮어써짐)
# 표준: 지도사 방식(look archive · sub_style dark · map_tone day · date/clock/legend · clip · 지도 60%↑ · 글자 카드 25%↓)
#       + DocuKit(research.md · src · globe · punch · counters · stamp) + 승현 eleven_v3 · tempo 1.0 · max_pause 0.65 + 롱폼·후킹 표준
# 막 번호: Act 1 = 콜드 오프닝(0~60초), Act 2~7 = 본편 → 장면 "act" 1~7 = act1.mp3~act7.mp3
# 전장: 알레시아(몽 오수아) 둘레 안쪽 포위선(11로마마일 ≈ 16km)·바깥 포위선(14로마마일 ≈ 21km)은 타원으로 모식화 (실제 선은 지형을 따라 굽음)
# 몽 레아(북서쪽 진영)·카이사르 지휘소(남쪽 플라비니 언덕)·구원군 진영(서남쪽 언덕) 좌표는 개략 — 학설·추정
# 재연 그림은 실사풍 시네마틱 재연(지도사 표준 4-5항) — 얼굴이 알아보이지 않게, 글자 없음
import collections
import json
import math
import pathlib
import re

HERE = pathlib.Path(__file__).parent
EP = HERE.name
raw = (HERE / "script.md").read_text(encoding="utf-8")
ACTS = []
for a in raw.split("\n## ")[1:]:
    body = [l for l in a.split("\n")[1:] if l and not l.startswith((">", "#"))]
    ACTS.append([s for l in body for s in re.split(r"(?<=[.?])\s+", l.strip()) if s])

# 자막 표기(숫자) ← 낭독 문장(단어) — 긴 것부터 (사용자 지시: 자막 숫자는 숫자로)
SUBS = [
    ("기원전 오십이년 구월", "기원전 52년 9월"), ("기원전 오십이년", "기원전 52년"), ("기원전 사십육년", "기원전 46년"),
    ("천팔백육십일년", "1861년"), ("천구백구십일년", "1991년"), ("천구백여 년", "1,900여 년"), ("이천 년", "2천 년"),
    ("팔만 명", "8만 명"), ("칠만 명", "7만 명"), ("육만에서 칠만 명", "6만에서 7만 명"), ("정예 육만 명", "정예 6만 명"),
    ("이십오만 명", "25만 명"), ("삼십만 명", "30만 명"), ("이십오만이라던", "25만이라던"), ("밖에서 이십오만", "밖에서 25만"), ("안에서 팔만", "안에서 8만"),
    ("약 사만 명", "약 4만 명"), ("팔백 명", "800명"), ("약 삼천 명", "약 3천 명"), ("약 칠백 명", "약 700명"), ("마흔여섯 명", "46명"),
    ("만 이천 명씩", "1만 2천 명씩"), ("기병 팔천 명", "기병 8천 명"), ("스무 곳", "20곳"), ("스물세 개", "23개"), ("일흔네 개", "74개"),
    ("서른아홉 개", "39개"), ("여섯 개 대대", "6개 대대"), ("일곱 개 대대", "7개 대대"), ("두 군단", "2개 군단"),
    ("십일 마일", "11마일"), ("십사 마일", "14마일"), ("삼 마일", "3마일"), ("약 십육 킬로미터", "약 16km"), ("약 이십일 킬로미터", "약 21km"), ("약 삼십칠 킬로미터", "약 37km"),
    ("이십 피트", "20피트"), ("사백 피트", "400피트"), ("십오 피트", "15피트"), ("십이 피트", "12피트"), ("팔십 피트", "80피트"), ("삼 피트", "3피트"), ("육 피트", "6피트"), ("사 인치", "4인치"),
    ("삼십일 치", "30일 치"), ("삼십일이", "30일이"), ("육 점 육 미터", "6.6m"), ("나폴레옹 삼세", "나폴레옹 3세"),
    ("여섯 해", "6년"), ("다섯 배", "5배"), ("다섯 줄", "5줄"), ("여덟 줄", "8줄"), ("두 줄", "2줄"),
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


def ai(img, kb="in", lower=None, **kw):
    v = {"type": "ai", "img": img, "kb": kb}
    if lower:
        v["lower"] = lower
    v.update(kw)
    return v


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


def punch(t, sub=None, color=None):
    v = {"type": "punch", "text": t}
    if sub:
        v["sub"] = sub
    if color:
        v["color"] = color
    return v


def cmp(lt, lb, rt, rb, lc="blue", rc="red"):
    return {"type": "compare", "left": {"title": lt, "big": lb, "icon": "none", "color": lc}, "right": {"title": rt, "big": rb, "icon": "none", "color": rc, "at": 0.6}}


def bars(note, items):
    return {"type": "bars", "note": note, "items": items}


def checklist(title, items):
    return {"type": "checklist", "title": title, "items": items}


def ranks(profile, vs=None, title=None, labels=None, **kw):
    """정면 전열 대열 (Hook.tsx PhalanxTroops) — profile: 열마다 대열 깊이 · gr = 앞쪽(파랑 계열) · pe = 상대(빨강 계열)"""
    v = {"type": "troops", "side": "gr", "profile": profile}
    if vs:
        v["vs"] = {"side": "pe", "profile": vs}
    if title:
        v["title"] = title
    if labels:
        v["labels"] = labels
    v.update(kw)
    return v


def globe(fr, to, route, pins, on=None, dur=4, **kw):
    v = {"type": "globe", "from": fr, "to": to, "route": route, "pins": pins, "dur": dur}
    if on:
        v["on"] = on
    v.update(kw)
    return v


def cnt(to, unit, label, on=None, at=None, frm=0, fmt=None, dur=1.6):
    d = {"from": frm, "to": to, "unit": unit, "label": label, "dur": dur}
    if fmt:
        d["fmt"] = fmt
    if on:
        d["on"] = on
    else:
        d["at"] = at if at is not None else 0.3
    return d


# 사진: 위키미디어 공용 파일명을 웹 검색으로 확인한 것만 (2026-11-26)
PH = {
    "caesar": ("File:Retrato de Julio César (26724093101).jpg",
               "카이사르 생전에 만들어진 것으로 보는 투스쿨룸 초상 · 토리노 고고학박물관", ("투스쿨룸 초상", "기원전 1세기")),
    "coin": ("File:Vercingetorix statère MAN.jpg",
             "베르킨게토릭스의 이름이 새겨진 아르베르니족 금화 · 프랑스 국립고고학박물관", ("아르베르니족 금화", "기원전 1세기")),
    "gergovia": ("File:Plateau de Gergovie au soleil couchant.jpg",
                 "오늘날의 게르고비아 고원 · 프랑스 퓌드돔", ("게르고비아 고원", "오늘날")),
    "motte_siege": ("File:Motte Le siège d'Alésia.jpg",
                    "알레시아 포위전 · 앙리 폴 모트 · 스뮈르 학술협회 소장", ("앙리 폴 모트", "1888년 무렵")),
    "panorama": ("File:Alise-Sainte-Reine panorama du site d'Alésia (1).jpg",
                 "몽 오수아의 알레시아 유적과 둘레 언덕 · 알리즈생트렌", ("알레시아 유적", "오늘날")),
    "rampart": ("File:Reconstruction of the rampart of the contravallation, Alesia (7700412514).jpg",
                "다시 세운 로마군 흙벽과 망루 · 뮈제오파르크 알레시아", ("복원한 포위선", "오늘날")),
    "traps": ("File:Reconstruction of the rampart and obstacles and traps of the circumvallation, Alesia (7700311088).jpg",
              "다시 만든 함정 구덩이와 뾰족한 가지 · 뮈제오파르크 알레시아", ("복원한 함정", "오늘날")),
    "ditches": ("File:Reconstruction of obstacles and traps of the contravallation, Alesia (7700232060).jpg",
                "다시 판 두 줄 도랑 · 앞 도랑에는 물을 채웠다 · 뮈제오파르크 알레시아", ("복원한 도랑", "오늘날")),
    "museo": ("File:Muséoparc d'Alésia fortifications.JPG",
              "복원한 포위선과 방어 장애물 · 뮈제오파르크 알레시아", ("복원한 포위선", "오늘날")),
    "royer": ("File:Lionel Royer - Vercingetorix Throwing down His Weapons at the feet of Julius Caesar.jpg",
              "카이사르의 발 앞에 무기를 던지는 베르킨게토릭스 · 리오넬 루아예 · 크로자티에 박물관", ("리오넬 루아예", "1899")),
    "motte_surr": ("File:Vercingétorix se rend à César 1886 HPMotte.jpg",
                   "카이사르에게 항복하는 베르킨게토릭스 · 앙리 폴 모트", ("앙리 폴 모트", "1886")),
    "site": ("File:Alise-Sainte-Reine - Site archéologique d'Alésia - 01.jpg",
             "몽 오수아 위 알레시아 발굴 유적 · 알리즈생트렌", ("알레시아 발굴 유적", "오늘날")),
    "plan": ("File:Plan du siège d’Alésia en 52 avant notre ère.jpg",
             "발굴로 확인한 알레시아 포위선 도면 · 뮈리엘 고트로프", ("알레시아 포위 도면", "오늘날")),
    "statue": ("File:Alise-Sainte-Reine statue Vercingetorix par Millet large.jpg",
               "몽 오수아의 베르킨게토릭스 동상 · 에메 미예 · 높이 6.6m", ("베르킨게토릭스 동상", "1865")),
    "statue_t": ("File:Vercingétorix Alésia.jpg",
                 "베르킨게토릭스 동상 · 나폴레옹 3세가 세움", ("베르킨게토릭스 동상", "1865")),
}


def pin(key):
    sid = nid()
    PINS[f"{sid}-photo#0"] = PH[key][0]
    return f"{sid}-photo"


def ph(key, pos=None, marks=None, **kw):
    v = {"type": "photo", "kb": "in", "q": pin(key), "tag": f"{PH[key][2][0]} · {PH[key][2][1]}"}
    if pos:
        v["pos"] = pos
    if marks:
        v["marks"] = marks
    v.update(kw)
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

# ===== 좌표 (경도, 위도) =====
C0 = (4.497, 47.539)          # 알레시아 언덕(몽 오수아) 한가운데
KX, KY = 1 / 75.2, 1 / 111.2  # km → 도 (위도 47.5도)


def ell(a, b, n=56, c=C0, start=0.0, end=360.0):
    out = []
    for i in range(n + 1):
        t = math.radians(start + (end - start) * i / n)
        out.append([round(c[0] + a * KX * math.cos(t), 5), round(c[1] + b * KY * math.sin(t), 5)])
    return out


def on_ell(a, b, deg, c=C0):
    t = math.radians(deg)
    return [round(c[0] + a * KX * math.cos(t), 5), round(c[1] + b * KY * math.sin(t), 5)]


IN_A, IN_B = 3.0, 2.1    # 안쪽 포위선 둘레 약 16km
OUT_A, OUT_B = 3.9, 2.75  # 바깥 포위선 둘레 약 21km
INNER = ell(IN_A, IN_B)
OUTER = ell(OUT_A, OUT_B)
TOWN = ell(1.1, 0.42, 32)
P = {
    # --- 갈리아 전역 ---
    "rome": [12.48, 41.9, "로마"], "italy": [10.9, 44.6, "이탈리아 · 갈리아 키살피나"], "province": [4.6, 43.75, "로마 속주"],
    "cevennes": [3.75, 44.45, "세벤산맥"], "arverni": [3.0, 45.55, "아르베르니족"], "gergovia": [3.15, 45.71, "게르고비아"],
    "avaricum": [2.4, 47.08, "아바리쿰"], "bituriges": [2.1, 46.75, "비투리게스족"], "bibracte": [4.04, 46.92, "비브락테 · 하이두이족"],
    "alesia": [4.5, 47.54, "알레시아"], "rhine": [7.7, 48.9, "라인강"], "lingones": [5.25, 47.62, "링고네스족 땅"],
    "senones": [3.28, 48.2, "세노네스족"], "sequani": [6.0, 47.24, "세콰니족"], "britannia": [-1.2, 51.0, "브리타니아"],
    "lemovices": [1.26, 45.83, "레모비케스족"], "carrhae": [39.03, 36.87, "카레"],
    # --- 알레시아 둘레 (개략) ---
    "town": [4.497, 47.539, "알레시아 · 만두비족의 도시"], "gcamp": [4.513, 47.541, "갈리아군 진영"],
    "plain": [4.462, 47.537, "서쪽 들판 · 약 3마일"], "rea": [4.465, 47.563, "몽 레아"], "ncamp": [4.468, 47.557, "북쪽 진영 · 2개 군단"],
    "bussy": [4.508, 47.566, "북쪽 언덕"], "flavigny": [4.518, 47.517, "플라비니 언덕"], "post": [4.512, 47.521, "카이사르의 지휘소"],
    "relief": [4.425, 47.522, "구원군 진영"], "gate_w": [4.484, 47.538, "서쪽 성문"], "steep": [4.522, 47.531, "가파른 비탈"],
    "behind_rea": [4.452, 47.574, "언덕 뒤"], "oze": [4.53, 47.551, "오즈강"], "ozerain": [4.53, 47.528, "오즈랭강"],
    "ring_s": on_ell((IN_A + OUT_A) / 2, (IN_B + OUT_B) / 2, 270), "ring_n": on_ell((IN_A + OUT_A) / 2, (IN_B + OUT_B) / 2, 100),
    "in_w": on_ell(IN_A, IN_B, 180), "out_w": on_ell(OUT_A, OUT_B, 180), "in_e": on_ell(IN_A, IN_B, 0), "out_e": on_ell(OUT_A, OUT_B, 0),
    "in_s": on_ell(IN_A, IN_B, 285), "between": [4.468, 47.548, "두 군대 사이"],
}
for k in ("ring_s", "ring_n", "in_w", "out_w", "in_e", "out_e", "in_s"):
    P[k] = P[k] + [""]
V = {
    "europe": {"center": [8.5, 45.6], "span": 20.0}, "gaul": {"center": [3.3, 46.7], "span": 11.5},
    "approach": {"center": [4.85, 47.58], "span": 1.3}, "auxois": {"center": [4.5, 47.545], "span": 0.42},
    "siege": {"center": [4.494, 47.540], "span": 0.135}, "north": {"center": [4.474, 47.555], "span": 0.06},
    "plain": {"center": [4.462, 47.537], "span": 0.055}, "south": {"center": [4.508, 47.526], "span": 0.06},
}
LAND = {"home": ["250"], "foreign": ["724", "380", "756", "276", "56", "442", "528", "826", "40", "20", "492"]}

# --- 강 (개략) ---
OZE = [[4.575, 47.556], [4.548, 47.551], [4.52, 47.549], [4.495, 47.547], [4.472, 47.543], [4.452, 47.539]]
OZERAIN = [[4.575, 47.522], [4.548, 47.526], [4.52, 47.529], [4.495, 47.531], [4.472, 47.533], [4.452, 47.537]]
BRENNE = [[4.443, 47.585], [4.447, 47.562], [4.451, 47.538], [4.455, 47.515], [4.46, 47.495]]
RIV = lambda at=0: [{"k": "line", "path": p, "color": "#5aa0d8", "glow": False, "at": at} for p in (OZE, OZERAIN, BRENNE)]
# --- 갈리아 원정로 (개략) ---
ITALY_BACK = [[11.2, 44.5], [7.6, 44.8], [5.0, 43.9], [4.4, 43.85]]
CEVENNES = [[4.4, 43.85], [3.75, 44.45], [3.1, 45.4]]
TO_AVAR = [[3.1, 45.4], [3.6, 46.4], [2.4, 47.08]]
TO_GERG = [[2.4, 47.08], [3.0, 46.3], [3.15, 45.71]]
RETREAT = [[3.6, 46.6], [4.6, 47.3], [5.25, 47.62]]
TO_ALESIA = [[5.25, 47.62], [4.9, 47.6], [4.5, 47.54]]
# --- 알레시아 둘레 화살표 (모식) ---
SORTIE = [[[4.497, 47.539], [4.47, 47.57], [4.43, 47.6]], [[4.497, 47.539], [4.54, 47.575], [4.58, 47.6]], [[4.497, 47.539], [4.53, 47.505], [4.58, 47.49]]]
RELIEF_IN = [[4.38, 47.48], [4.405, 47.505], [4.425, 47.522]]
NIGHT_HIT = [[4.425, 47.522], [4.438, 47.531], [4.445, 47.537]]
INSIDE_W = [[4.487, 47.539], [4.47, 47.538], [4.459, 47.538]]
BACK_IN = [[4.459, 47.538], [4.475, 47.539], [4.488, 47.539]]
RETIRE = [[4.445, 47.535], [4.432, 47.528], [4.42, 47.52]]
FLANK_N = [[4.425, 47.522], [4.41, 47.555], [4.44, 47.58], [4.452, 47.574]]
DOWN_REA = [[4.455, 47.572], [4.462, 47.565], [4.467, 47.559]]
LAB = [[4.512, 47.521], [4.49, 47.53], [4.475, 47.545], [4.469, 47.554]]
TO_STEEP = [[4.505, 47.537], [4.515, 47.533], [4.524, 47.531]]
BRUTUS = [[4.512, 47.521], [4.52, 47.526], [4.523, 47.53]]
CAESAR_N = [[4.523, 47.53], [4.505, 47.523], [4.48, 47.533], [4.47, 47.55], [4.468, 47.556]]
CAV_OUT = [[4.512, 47.521], [4.47, 47.5], [4.42, 47.51], [4.405, 47.545], [4.43, 47.575], [4.452, 47.57]]
FLEE_N = [[4.462, 47.562], [4.448, 47.575], [4.43, 47.585]]
SCATTER = [[[4.425, 47.522], [4.38, 47.5]], [[4.425, 47.522], [4.4, 47.56]], [[4.425, 47.522], [4.43, 47.47]]]
SHORT = [[4.512, 47.521], [4.49, 47.522], [4.47, 47.528], [4.458, 47.538]]
LONG = [[4.425, 47.522], [4.39, 47.55], [4.42, 47.585], [4.465, 47.59], [4.52, 47.585]]
TO_ROME = [[4.5, 47.54], [6.5, 45.5], [9.0, 44.4], [12.48, 41.9]]
TO_CARRHAE = [[4.5, 47.54], [12.48, 41.9], [23.7, 38.0], [35.5, 36.9], [39.03, 36.87]]

LOCK = lambda p, at=0.3, text=None, on=None: dict({"k": "lock", "p": p, "text": text if text is not None else P[p][2]}, **({"on": on} if on else {"at": at}))
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
zone = lambda path, text=None, at=0, on=None, color="#d8b46a": dict({"k": "zone", "path": path, "color": color}, **({"text": text} if text else {}), **({"on": on} if on else {"at": at}))
top = lambda t, s="yellow", at=0: [{"text": t, "style": s, "at": at, "pos": "top"}]
SW = lambda at=0: [{"id": "whoosh", "at": at}]
PING = lambda at=0.6: [{"id": "ping", "at": at}]
WIND = lambda at=0: [{"id": "wind", "at": at}]
FAR = lambda at=0: [{"id": "artillery_far", "at": at, "db": -32}]
HUD = lambda big, sub=None, sub2=None, at=0.0, color=None, on=None: dict({"big": big, "count": False}, **({"sub": sub} if sub else {}), **({"sub2": sub2} if sub2 else {}),
                                                                         **({"on": on} if on else {"at": at}), **({"color": color} if color else {}))
CLIP = lambda source, t, on=None, at=0.3, pos=None, rec=True: dict({"source": source, "text": t, "recreated": rec}, **({"on": on} if on else {"at": at}), **({"pos": pos} if pos else {}))

IN_L = lambda at=0, on=None: line(INNER, at, "#ffd400", on)
OUT_L = lambda at=0, on=None: line(OUTER, at, "#ff8a3d", on)
TOWN_Z = lambda at=0: zone(TOWN, None, at, color="#6f8fd8")
BASE = lambda: RIV() + [TOWN_Z()]
WALLS = lambda: BASE() + [IN_L(), OUT_L()]
RING_UNITS = lambda at=0.2: [mark(on_ell((IN_A + OUT_A) / 2, (IN_B + OUT_B) / 2, d), "red", at) for d in range(0, 360, 30)]
FORTS = [mark(on_ell(IN_A, IN_B, d * 360 / 23 + 8), "red", 0.15 + 0.06 * d) for d in range(23)]
LEG_GAUL = [{"icon": "ally", "text": "로마군 · 카이사르", "color": "#c9242c"}, {"icon": "enemy", "text": "갈리아 연합 · 베르킨게토릭스", "color": "#1f5fbf"}]
LEG_SIEGE = [{"icon": "ally", "text": "로마군", "color": "#c9242c"}, {"icon": "enemy", "text": "갈리아군", "color": "#1f5fbf"},
             {"icon": "line", "text": "안쪽 포위선 · 약 16km", "color": "#ffd400"}, {"icon": "line", "text": "바깥 포위선 · 약 21km", "color": "#ff8a3d"}]
LEG_CIVIL = LEG_SIEGE[:2] + [{"icon": "civil", "text": "쫓겨난 만두비족"}]

QUESTION = "안에서도 밖에서도 포위당한\n카이사르는 어떻게\n이 싸움을 이겼을까"
SIEGE = lambda items, tilt=34, **kw: m("siege", "siege", WALLS() + items, tilt=tilt, **kw)
SIEGE1 = lambda items, tilt=34, **kw: m("siege", "siege", BASE() + [IN_L()] + items, tilt=tilt, **kw)
NORTH = lambda items, tilt=36, **kw: m("north", "north", WALLS() + items, tilt=tilt, **kw)
GAUL = lambda items, tilt=14, **kw: m("gaul", "gaul", items, tilt=tilt, **kw)

# ===== 제1막 · 콜드 오프닝 (0~10초 사건 직격 → 모순 3단 → X 반전 → 중앙 질문 카드 → 타이틀) =====
# 레이어 교차: 3D 비행 → 사료(초상) → 3D 두 겹 벽 → 병력 대열 → 지도 HUD → 재연 그림 → 병력 대열 → 복원 사진 → 지도(벽 그리기) → X → 질문 카드 → 타이틀
sc(2, m("gaul", "siege", BASE() + [LOCK("town", 1.6, "알레시아 언덕")], flight=["gaul", "auxois", "siege"], flightDur=4.6, hud=True, tilt=30),
   date="기원전 52. 9", legend=LEG_SIEGE, scale="1 km",
   hook={"hud": [HUD("기원전 52년 9월", "알레시아 · 몽 오수아", "갈리아 한가운데 · 오늘날 프랑스 부르고뉴")]}, sfx=SW(0) + PING(1.6), src=[30])
sc(1, ph("caesar", pos="50% 30%", marks=[mk("율리우스 카이사르", 0.5, 0.12, "카이사르는")]), label=plabel("caesar"))
sc(1, SIEGE([badge("town", "포위한 쪽", "#c9242c", dy=-90, at=0.1), blue_a(RELIEF_IN, on="둘러싸여", w=1.2), badge("relief", "그런데 포위당한 쪽", "#1f5fbf", on="둘러싸여", dy=70)], tilt=34), sfx=PING(1.2))
sc(1, ranks([7, 7, 7, 7, 7, 7, 7, 7], [5] * 7, title="성 안의 갈리아군"),
   hook={"hud": [HUD("8만", "성 안의 갈리아군", "카이사르의 기록 · 7권 71장", color="#1f5fbf", on="팔만")]}, src=[11])
sc(1, SIEGE(RING_UNITS(0.2)), hook={"hud": [HUD("6만~7만", "로마군 (추정)", "오늘날 학자들의 추정", color="#FF3B30", on="칠만")]}, src=[33, 16])
sc(1, ai("relief_hills"), label=DRAMA, hook={"hud": [HUD("25만", "바깥의 구원군 보병", "카이사르의 기록 · 7권 76장", color="#1f5fbf", on="이십오만")]}, src=[17])
sc(1, ranks([9] * 14, [4] * 5, title="카이사르의 숫자대로라면", labels=[{"text": "약 5배", "x": 0.5, "y": 0.45, "color": "red", "on": "다섯"}]), src=[11, 17, 33])
sc(2, ph("rampart", pos="50% 55%", marks=[mk("도망 대신 벽", 0.5, 0.12, "벽을")]), label=plabel("rampart"))
sc(1, m("siege", "siege", BASE() + [IN_L(on="안쪽으로"), OUT_L(on="바깥쪽으로")], tilt=36), sfx=PING(1.8))
sc(2, black("독 안에 든 쥐?", "정말 그랬을까"), hook={"neg": {"text": "독 안에 든 쥐", "on": "독", "xOn": "그랬을까요"}})
sc(1, SIEGE([], tilt=30), hook={"question": {"text": QUESTION, "at": 0.02}})
sc(1, {"type": "titlecard", "title": "안팎이 모두 적", "sub": "알레시아 공방전 · 기원전 52년", "at": 0, "q": pin("motte_siege")}, flash=True)
next_act()

# ===== 제2막 · 기원전 52년 겨울 =====
sc(2, GAUL([LOCK("alesia", 0.8, "갈리아")]), chapter={"num": "제2막", "title": "기원전 52년 겨울"}, date="기원전 52. 겨울", legend=LEG_GAUL, scale="100 km", sfx=SW(0), src=[1])
sc(2, GAUL([mark(p, "red", 0.2 + 0.25 * i) for i, p in enumerate(["province", "bibracte", "senones", "lingones", "avaricum"])] + [badge("alesia", "기원전 58년부터 · 갈리아 전쟁", "#c9242c", on="여섯", dy=-70)]), src=[1])
sc(1, m("gaul", "europe", [LOCK("italy", on="이탈리아에")], flight=["gaul", "europe"], flightDur=2.2, tilt=12))
sc(1, GAUL([LOCK("arverni", on="아르베르니족에서")]), sfx=PING(1.4))
sc(1, ph("coin", pos="50% 50%", marks=[mk("베르킨게토릭스", 0.5, 0.1, "베르킨게토릭스")]), label=plabel("coin"), src=[1])
sc(2, ai("exile", lower={"date": "기원전 53년 무렵", "title": "도시에서 쫓겨난 젊은이", "sub": "아버지 켈틸루스는 왕이 되려 했다는 이유로 죽임을 당했다"}), label=DRAMA, src=[1])
sc(2, GAUL([unit("gergovia", "게르고비아", "blue", 0.1, pulse=True), badge("gergovia", "왕으로 추대", "#1f5fbf", on="추대됩니다", dy=-70)]
           + [blue_a([P[k][:2], [3.15, 45.71]], on="처음으로") for k in ("avaricum", "lemovices", "senones")]))
sc(1, globe([11.5, 44.0], [3.5, 45.0], ITALY_BACK + CEVENNES[1:], [{"ll": [11.2, 44.5], "text": "갈리아 키살피나"}, {"ll": [3.1, 45.4], "text": "아르베르니족 땅", "on": "돌아왔습니다"}],
            on="돌아왔습니다", dur=3.2))
sc(2, ai("snow_pass", lower={"date": "기원전 52년 겨울", "title": "눈 덮인 세벤산맥", "sub": "로마 병사들이 눈을 치우며 산을 넘었다 · 7권 8장"}), label=DRAMA, sfx=WIND(0), src=[2])
sc(1, GAUL([red_a(CEVENNES, 0.2, 1.2), badge("cevennes", "아무도 오지 못한다고 믿은 길", "#c9242c", on="믿었던", dy=-70)], tilt=16))
sc(2, GAUL([mark("arverni", "red", 0), unit("avaricum", "베르킨게토릭스", "blue", 0.2), badge("bituriges", "정면 승부를 피하다", "#1f5fbf", on="정면으로", dy=70)]))
sc(2, ai("scorched", lower={"date": "기원전 52년 봄", "title": "스스로 불태운 마을", "sub": "로마군이 먹을 것을 찾지 못하게"}), label=DRAMA, src=[3])
sc(1, GAUL([zone([[1.3, 46.4], [2.9, 46.4], [2.9, 47.5], [1.3, 47.5]], "비투리게스족 땅", 0, color="#d0702a"), badge("bituriges", "하루에 도시 20곳 넘게", "#c9242c", on="하루", dy=70)],
           counters=[cnt(20, "곳 넘게", "하루에 불탄 도시", on="스무")]), src=[3])
sc(2, GAUL([LOCK("avaricum", on="아바리쿰만은"), badge("avaricum", "가장 아름다운 도시", "#111", on="아름다우니", dy=-70)], tilt=16))
sc(2, ai("avaricum_rain", lower={"date": "기원전 52년 봄", "title": "아바리쿰 함락", "sub": "비가 쏟아지던 날 로마군이 성벽을 넘었다"}), label=DRAMA, sfx=FAR(0))
sc(1, GAUL([mark("avaricum", "red", 0), LOCK("avaricum", 0.1, "아바리쿰")],
           counters=[cnt(40000, "명", "성 안에 있던 사람 (카이사르)", on="사만"), cnt(800, "명", "살아서 빠져나간 사람", on="팔백")]), src=[4, 5])
sc(2, GAUL([blue_a([P[k][:2], [3.15, 45.71]], on="더") for k in ("senones", "lemovices", "bibracte", "bituriges")] + [unit("gergovia", "베르킨게토릭스", "blue", 0.1, pulse=True)]))
sc(2, ph("gergovia", pos="50% 55%", marks=[mk("게르고비아 · 높은 언덕 위의 도시", 0.5, 0.14, "높은")]), label=plabel("gergovia"), date="기원전 52. 늦봄", src=[6])
sc(2, ai("gergovia_charge", lower={"date": "기원전 52년 늦봄", "title": "게르고비아 성벽 아래", "sub": "물러나라는 나팔을 듣지 못한 병사들"}), label=DRAMA, sfx=FAR(0), src=[7])
sc(1, GAUL([red_a(TO_GERG, 0), clash("gergovia", 0.2), badge("gergovia", "로마군의 패배", "#1f5fbf", on="백인대장", dy=-70)],
           counters=[cnt(46, "명", "쓰러진 백인대장", on="마흔여섯"), cnt(700, "명", "쓰러진 병사 (약)", on="칠백")]), src=[6, 7])
sc(1, punch("카이사르가 졌다", "직접 이끈 싸움에서 좀처럼 없던 패배"), src=[7])
sc(2, GAUL([zone([[3.4, 46.4], [4.7, 46.4], [4.7, 47.3], [3.4, 47.3]], "하이두이족", 0, color="#1f5fbf"), badge("bibracte", "가장 오랜 동맹이 등을 돌리다", "#1f5fbf", on="등을", dy=70)]), sfx=PING(1.0))
sc(1, GAUL([dash_r(RETREAT, on="물러나기"), LOCK("province", on="속주")], tilt=16))
sc(3, ai("cavalry_oath", lower={"date": "기원전 52년 여름", "title": "갈리아 기병 대장들의 맹세", "sub": "카이사르 『갈리아 전기』 7권 66장"}), label=DRAMA,
   clip=CLIP("카이사르 『갈리아 전기』 7권 66장", "로마군 행렬을 [[두 번]] 꿰뚫지 못한 자는\n집에도 가족에게도 돌아가지 않는다", on="맹세했다고", pos="right"), src=[34])
sc(2, GAUL([LOCK("rhine", on="라인강"), dash_r([[7.7, 48.9], [6.2, 48.2], [5.25, 47.62]], on="게르만")]))
sc(1, m("approach", "approach", [unit("lingones", "게르만 기병", "red", 0.1, pulse=True), badge("lingones", "장교들의 말을 내주다", "#c9242c", on="장교들의", dy=-70)], tilt=26), src=[8])
sc(2, m("approach", "approach", [unit("lingones", "로마군 행렬", "red", 0), swarm([[5.0, 47.75], [5.15, 47.68], [5.25, 47.62]], 0.1, 100, 0.5, "#1f5fbf"),
                                 red_a([[5.35, 47.55], [5.25, 47.66], [5.05, 47.75]], on="밀어냈습니다", w=1.2), clash([5.18, 47.67], on="무너졌고")],
        tilt=28, counters=[cnt(3000, "명", "쓰러진 갈리아 후위 (약)", on="삼천")]), sfx=FAR(0), src=[8, 9])
sc(2, m("approach", "auxois", [blue_a(TO_ALESIA, 0.2, 1.1), LOCK("town", on="알레시아였습니다", text="알레시아")], flight=["approach", "auxois"], flightDur=2.6, tilt=28), sfx=SW(0))
next_act()

# ===== 제3막 · 16킬로미터 =====
MID = [nid()]
sc(2, m("auxois", "siege", BASE() + [LOCK("town", 0.8, "알레시아")] + [badge(k, P[k][2], "#2a5d8f", on="두 줄기", dy=-50) for k in ("oze", "ozerain")],
        flight=["auxois", "siege"], flightDur=2.6, tilt=32), pauseBefore=0.5, chapter={"num": "제3막", "title": "16킬로미터"},
   date="기원전 52. 여름", legend=LEG_SIEGE[:2], scale="1 km", sfx=SW(0), src=[9])
sc(2, m("siege", "siege", BASE() + [zone([[4.44, 47.528], [4.475, 47.528], [4.475, 47.548], [4.44, 47.548]], "서쪽 들판 · 약 3마일", on="들판이", color="#d8b46a"),
                                    badge("rea", "언덕", "#111", on="언덕들이", dy=-40), badge("bussy", "언덕", "#111", on="언덕들이", dy=-40), badge("flavigny", "언덕", "#111", on="언덕들이", dy=40)], tilt=32), src=[9])
sc(1, m("siege", "siege", BASE() + [unit("town", "갈리아군", "blue", 0.1, pulse=True), unit("gcamp", "갈리아군 진영", "blue", 0.4)], tilt=34,
        counters=[cnt(80000, "명", "성 안의 갈리아군 (카이사르)", on="팔만")]), src=[11])
sc(2, ai("steep_hill", lower={"date": "기원전 52년 여름", "title": "알레시아 언덕", "sub": "정면으로 오르면 로마군이 먼저 쓰러질 비탈"}), label=DRAMA)
sc(1, m("siege", "siege", BASE() + [IN_L(on="벽으로")], tilt=34), sfx=PING(1.2))
sc(2, SIEGE1([badge("ring_s", "11로마마일 ≈ 약 16km", "#111", on="십일", dy=60)], counters=[cnt(16, "km", "안쪽 포위선 둘레 (약)", on="십육")]), src=[10])
sc(1, SIEGE1(FORTS + [unit("post", "로마 진영", "red", 0.2), unit("ncamp", "로마 진영", "red", 0.4)], counters=[cnt(23, "개", "보루", on="스물세")]), src=[10])
sc(2, m("plain", "plain", BASE() + [IN_L(), swarm([[4.475, 47.545], [4.462, 47.538], [4.452, 47.532]], 0.1, 100, 0.5, "#1f5fbf"),
                                    red_a([[4.445, 47.53], [4.462, 47.538], [4.478, 47.541]], on="게르만", w=1.3), clash([4.465, 47.538], on="몰아붙였죠")], tilt=36), sfx=FAR(0), src=[9])
sc(3, m("siege", "auxois", BASE() + [IN_L()] + [dash_b(p, on="내보냈죠") for p in SORTIE], flight=["siege", "auxois"], flightDur=2.4, tilt=30, tone="night"),
   clock="밤", src=[11])
sc(2, SIEGE1([unit("town", "갈리아군 8만", "blue", 0.1)], counters=[cnt(30, "일", "성 안 곡식 · 아껴 먹어도", on="삼십일")]), clock="", src=[11])
sc(2, punch("시간과의 싸움", "구원군이 오기 전에 벽을 끝내라"))
sc(2, ph("ditches", pos="50% 55%", marks=[mk("깊이 20피트 도랑", 0.5, 0.12, "이십")]), label=plabel("ditches"), src=[11])
sc(2, doc("카이사르의 공사 기록", ["언덕 쪽 · 깊이 20피트 도랑", "400피트 뒤 · 너비 15피트 도랑 2줄", "안쪽 도랑에는 강물"], "7권 72장", "『갈리아 전기』"), src=[11])
sc(2, ph("rampart", pos="50% 50%", marks=[mk("흙벽 + 울타리 · 12피트", 0.36, 0.14, "흙벽과"), mk("망루 · 80피트마다", 0.7, 0.14, "망루가")]), label=plabel("rampart"), src=[11])
sc(2, SIEGE1([mark(on_ell(IN_A, IN_B, d), "red", 0.2) for d in range(0, 360, 60)] + [badge("in_s", "지킬 병사보다 긴 벽", "#c9242c", on="훨씬", dy=60)]))
sc(1, ai("stakes", lower={"date": "기원전 52년 여름", "title": "사람 대신 땅이 지키다", "sub": "뾰족하게 깎은 가지를 박는 로마 병사들"}), label=DRAMA)
sc(2, ph("traps", pos="50% 55%", marks=[mk("묘비석 · 5줄", 0.5, 0.12, "묘비석이라")]), label=plabel("traps"), src=[12])
sc(2, ai("lilia", lower={"date": "기원전 52년 여름", "title": "백합", "sub": "깊이 3피트 구덩이 · 바닥에 말뚝 · 땅 위로 4인치"}), label=DRAMA, src=[12])
sc(2, ph("museo", pos="50% 55%", marks=[mk("잔가지로 덮은 함정", 0.5, 0.12, "감췄습니다"), mk("백합", 0.5, 0.22, "백합이라고", "red")]), label=plabel("museo"), src=[12])
sc(2, checklist("사람 대신 땅이 지킨다", [{"text": "묘비석 · 뾰족한 가지 5줄", "at": 0.1}, {"text": "백합 · 말뚝 구덩이 8줄", "at": 0.6}, {"text": "박차 · 쇠갈고리 말뚝", "on": "박차라고"}]), src=[12])
sc(2, m("siege", "siege", BASE() + [IN_L(), OUT_L(on="바깥쪽을")], tilt=32), sfx=PING(1.6))
sc(2, SIEGE([badge("ring_n", "14로마마일 ≈ 약 21km", "#111", on="십사", dy=-60)], counters=[cnt(21, "km", "바깥 포위선 둘레 (약)", on="이십일")]), legend=LEG_SIEGE, src=[13])
sc(1, SIEGE(RING_UNITS(0.1) + [zone(OUTER, None, 0, color="#c9242c")], counters=[cnt(70000, "명", "두 벽 사이의 로마군 (추정 6만~7만)", on="칠만")]), src=[33])
sc(1, SIEGE([blue_a([[4.497, 47.539], [4.475, 47.539]], 0.1), blue_a(RELIEF_IN, 0.2), badge("between", "포위한 쪽이 갇히다", "#c9242c", on="가둔", dy=-60)]), sfx=PING(1.0))
sc(1, ai("granary", lower={"date": "기원전 52년 여름", "title": "30일 치 곡식과 말 먹이", "sub": "두 벽 안에 쌓아 둔 로마군의 식량"}), label=DRAMA, src=[13])
next_act()

# ===== 제4막 · 30일 =====
sc(3, SIEGE([unit("town", "갈리아군", "blue", 0.1)], tilt=32, counters=[cnt(30, "일", "포위가 시작된 뒤", on="삼십일이")]), pauseBefore=0.5,
   chapter={"num": "제4막", "title": "30일"}, date="기원전 52. 9", sfx=SW(0), src=[14])
sc(2, ai("council", lower={"date": "기원전 52년 9월", "title": "알레시아 안의 회의", "sub": "항복할 것인가 뛰쳐나갈 것인가"}), label=DRAMA, src=[14])
sc(2, SIEGE([LOCK("town", on="크리토그나투스가", text="크리토그나투스")], clip=CLIP("카이사르 『갈리아 전기』 7권 77장", "뛰쳐나가는 건 [[용기가 아니라]]\n굶주림을 못 참는 약함이다", on="뛰쳐나가는")), src=[14])
sc(2, black("끔찍한 제안", "싸울 수 없는 사람들의 몸으로"), src=[14])
sc(2, SIEGE([LOCK("town", 0.2, "알레시아")], clip=CLIP("카이사르 『갈리아 전기』 7권 77장", "[[유례없이 잔인한]] 말\n※ 이 연설은 카이사르의 글에만 남아 있다", on="유례없이")), src=[14])
sc(2, SIEGE([blue_a(INSIDE_W[:2] + [[4.465, 47.538]], on="성 밖으로")], tilt=34))
sc(2, ai("mandubii", lower={"date": "기원전 52년 9월", "title": "쫓겨난 만두비족", "sub": "알레시아의 원래 주인 · 아내와 아이들과 함께"}), label=DRAMA, src=[15])
sc(2, m("plain", "plain", WALLS() + [mark("between", "#e0a526", 0.1, "만두비족"), badge("in_w", "노예로라도 받아 달라", "#111", on="노예로", dy=-60)], tilt=38),
   legend=LEG_CIVIL, src=[15])
sc(2, ai("guards", lower={"date": "기원전 52년 9월", "title": "벽 위의 경비병", "sub": "카이사르는 아무도 받아들이지 않았다 · 7권 78장"}), label=DRAMA, src=[15])
sc(1, m("plain", "plain", WALLS() + [mark("between", "#e0a526", 0), badge("between", "돌아갈 곳이 없다", "#111", on="돌아갈", dy=-60)], tilt=38))
sc(2, m("plain", "plain", WALLS() + [mark("between", "#e0a526", 0), badge("between", "두 군대 사이의 땅", "#111", on="두 군대", dy=60)], tilt=38),
   clip=CLIP("카이사르 『갈리아 전기』 7권 78장", "그 뒤의 일은 [[적지 않았다]]", on="적지", rec=False), src=[15, 16])
sc(1, black("가장 먼저", "쓰러진 사람들"))
sc(2, m("siege", "gaul", [mark("alesia", "red", 0)] + [blue_a([P[k][:2], [4.04, 46.92]], on="모이고") for k in ("senones", "sequani", "arverni", "lemovices", "bituriges", "britannia")],
        flight=["siege", "auxois", "gaul"], flightDur=2.8, tilt=14), legend=LEG_GAUL, scale="100 km", sfx=SW(0), src=[17])
sc(1, GAUL([LOCK("senones", on="세노네스족과"), LOCK("sequani", on="세콰니족"), badge("senones", "1만 2천 명씩", "#1f5fbf", on="만 이천", dy=-70)]), src=[17])
sc(1, GAUL([unit("bibracte", "구원군 집결", "blue", 0.1, pulse=True)], counters=[cnt(8000, "명", "기병", on="팔천"), cnt(250000, "명", "보병 (약 · 카이사르)", on="이십오만")]), src=[17, 18])
sc(3, bars("구원군 보병 · 기록마다 다르고 오늘날엔 훨씬 적었다고 봄", [{"label": "카이사르 (7권 76장)", "value": 250000, "display": "약 25만", "color": "blue", "at": 0.2},
                                    {"label": "플루타르코스", "value": 300000, "display": "30만", "color": "blue", "on": "플루타르코스는"},
                                    ]), src=[17, 25])
sc(3, GAUL([LOCK("britannia", on="코미우스"), dash_r([[1.6, 50.7], [-0.5, 51.0]], on="브리타니아"), badge("britannia", "카이사르를 도왔던 코미우스", "#1f5fbf", on="충실히", dy=70)], tilt=12), src=[22])
sc(1, ph("coin", pos="50% 50%", marks=[mk("사촌 베르카시벨라우누스", 0.5, 0.1, "사촌")]), label=plabel("coin"), src=[22])
sc(3, ranks([9] * 14, [4] * 5, title="안에서 8만 · 밖에서 25만", labels=[{"text": "누가 버틸 수 있나", "x": 0.5, "y": 0.45, "color": "red", "on": "누가"}]),
   hook={"hud": [HUD("33만 대 6만~7만", "카이사르의 숫자대로라면", "갈리아 안팎 대 로마군 (추정)", color="#1f5fbf", on="팔만")]}, src=[11, 17, 33])
sc(2, m("gaul", "siege", WALLS() + [swarm(RELIEF_IN, 0.3, 140, 0.6, "#1f5fbf"), LOCK("relief", on="나타났습니다"), badge("town", "부둥켜안고 기뻐하다", "#1f5fbf", on="기뻐했다고", dy=-80)],
        flight=["gaul", "auxois", "siege"], flightDur=2.6, tilt=34), legend=LEG_SIEGE, scale="1 km", src=[19])
next_act()

# ===== 제5막 · 25만 =====
MID.append(nid())
sc(2, m("plain", "plain", WALLS() + [swarm([[4.425, 47.522], [4.438, 47.53], [4.447, 47.537]], 0.1, 160, 0.7, "#1f5fbf"), LOCK("plain", on="들판을", text="서쪽 들판")], tilt=38),
   pauseBefore=0.5, chapter={"num": "제5막", "title": "25만"}, sfx=SW(0), src=[19])
sc(1, ai("archers", lower={"date": "구원군 도착 다음 날", "title": "기병 사이의 궁수들", "sub": "카이사르 『갈리아 전기』 7권 80장"}), label=DRAMA, src=[19])
sc(1, SIEGE([blue_a(INSIDE_W, on="베르킨게토릭스도"), badge("in_w", "첫 도랑을 메우다", "#1f5fbf", on="메우기", dy=60)]))
sc(2, SIEGE(RING_UNITS(0.1) + [badge("ring_s", "등을 맞댄 로마군", "#c9242c", on="등을", dy=60)]), sfx=PING(1.4))
sc(3, m("plain", "plain", WALLS() + [swarm([[4.43, 47.525], [4.442, 47.532]], 0, 140, 0.6, "#1f5fbf"), unit("out_w", "로마 기병", "red", 0.1), clash([4.44, 47.533], on="정오부터", size=1.2)], tilt=38),
   clock="정오", sfx=FAR(0), src=[19])
sc(1, m("plain", "plain", WALLS() + [red_a([[4.448, 47.545], [4.438, 47.535], [4.43, 47.526]], on="돌격했습니다", w=1.5), clash([4.437, 47.533], 0.4, 1.3)], tilt=38),
   clock="해 질 녘", src=[19])
sc(2, ai("german_charge", lower={"date": "구원군 도착 다음 날", "title": "게르만 기병의 돌격", "sub": "무너진 기병 사이로 드러난 궁수들"}), label=DRAMA, src=[19])
sc(1, SIEGE([dash_b(BACK_IN, on="돌아갔습니다")]), src=[19])
sc(2, ai("hurdles", lower={"date": "하루 뒤", "title": "나뭇가지 다발 · 사다리 · 갈고리", "sub": "구원군이 밤 공격을 준비하다"}), label=DRAMA, src=[20])
sc(1, m("plain", "plain", WALLS() + [dash_b(NIGHT_HIT, on="다가갔습니다")], tilt=38, tone="night"), clock="한밤", src=[20])
sc(3, SIEGE([blue_a(NIGHT_HIT, 0, 1.2), blue_a(INSIDE_W, on="나팔을", w=1.2), badge("relief", "함성 = 신호", "#1f5fbf", on="함성을", dy=70)], tone="night"), sfx=PING(2.2), src=[20])
sc(2, ai("night_wall", lower={"date": "한밤", "title": "들판 쪽 벽의 밤 싸움", "sub": "돌과 화살 · 투석기와 쌓아 둔 돌"}), label=DRAMA, sfx=FAR(0), src=[20])
sc(2, punch("어둠은 로마 편", "보이지 않는 함정"))
sc(2, ph("traps", pos="50% 60%", marks=[mk("백합 구덩이", 0.4, 0.14, "백합"), mk("박차 말뚝", 0.66, 0.14, "박차", "red")]), label=plabel("traps"), src=[20])
sc(1, ph("rampart", pos="60% 45%", marks=[mk("망루", 0.62, 0.14, "망루에서")]), label=plabel("rampart"))
sc(1, SIEGE([red_a(SHORT, on="안토니우스와", w=1.2), badge("post", "안토니우스", "#c9242c", on="안토니우스와", dy=-60), badge("ring_n", "트레보니우스", "#c9242c", on="트레보니우스는", dy=-60)], tone="night"), src=[20])
sc(2, SIEGE([dash_b(RETIRE, on="물러났습니다"), LOCK("ncamp", on="로마 진영이", text="높은 언덕의 로마 진영")]), clock="새벽", src=[20])
sc(2, SIEGE([dash_b(BACK_IN, on="돌아갔습니다"), badge("in_w", "벽에 닿지도 못하다", "#1f5fbf", on="닿지도", dy=60)]), src=[20])
sc(1, SIEGE([mark("plain", "blue", 0), mark("in_w", "blue", 0)], stamp={"text": "두 번 실패", "on": "실패했습니다", "x": 0.5, "y": 0.42, "rot": -8}), clock="")
sc(3, SIEGE([blue_a(NIGHT_HIT, 0.2), blue_a(INSIDE_W, on="박자를"), badge("between", "안과 밖 · 박자가 안 맞았다", "#1f5fbf", on="박자를", dy=-70)]), sfx=PING(2.4))
next_act()

# ===== 제6막 · 정오 =====
MID.append(nid())
sc(2, SIEGE([{"k": "radar", "p": "town", "at": 0.1}, LOCK("rea", on="약점을", text="약점")], tilt=32), pauseBefore=0.5, chapter={"num": "제6막", "title": "정오"}, sfx=SW(0) + PING(1.6), src=[21])
sc(2, m("siege", "north", WALLS() + [LOCK("rea", on="몽 레아라고")], flight=["siege", "north"], flightDur=2.0, tilt=36), src=[21])
sc(2, NORTH([zone([[4.452, 47.572], [4.478, 47.572], [4.478, 47.562], [4.452, 47.562]], "벽 밖에 남은 언덕", on="넓어", color="#8a7a5a"), unit("ncamp", "북쪽 진영", "red", 0.2), badge("ncamp", "비탈 아래 불리한 자리", "#c9242c", on="불리한", dy=60)]), src=[21])
sc(1, NORTH([unit("ncamp", "레기누스 · 레빌루스", "red", 0), badge("ncamp", "2개 군단뿐", "#c9242c", on="두 군단뿐이었습니다", dy=60)]), sfx=PING(1.0), src=[21])
sc(2, m("north", "siege", WALLS() + [unit("relief", "정예 6만", "blue", 0.2, pulse=True), badge("relief", "베르카시벨라우누스", "#1f5fbf", on="베르카시벨라우누스가", dy=70)],
        flight=["north", "siege"], flightDur=1.6, tilt=32, counters=[cnt(60000, "명", "북쪽으로 보낸 정예", on="육만")]), src=[21, 22])
sc(2, SIEGE([dash_b(FLANK_N, on="밤에"), LOCK("behind_rea", on="언덕 뒤에", text="언덕 뒤")], tone="night"), clock="밤 → 새벽", src=[21])
sc(1, ai("rea_descent", lower={"date": "마지막 날", "title": "정오의 비탈", "sub": "몽 레아에서 내려오는 갈리아 정예"}), label=DRAMA, clock="정오", sfx=FAR(0), src=[21])
sc(1, SIEGE([blue_a(DOWN_REA, 0, 1.3), swarm([[4.43, 47.525], [4.444, 47.534]], 0.2, 120, 0.6, "#1f5fbf"), blue_a(NIGHT_HIT, on="기병은")]), src=[21])
sc(2, SIEGE([blue_a(DOWN_REA, 0), blue_a(INSIDE_W, on="베르킨게토릭스도", w=1.2), badge("in_w", "갈고리 · 사다리 · 공성 방패", "#1f5fbf", on="갈고리와", dy=60)]), src=[21])
sc(1, SIEGE([clash(p, on="한꺼번에", size=0.9) for p in ("ncamp", "in_w", "out_w", "steep")]), sfx=FAR(0))
sc(2, SIEGE(RING_UNITS(0) + [clash("ncamp", 0, 0.9), clash("out_w", 0, 0.9)], counters=[cnt(37, "km", "로마군이 지킨 벽 (16 + 21 · 약)", on="삼십칠")]), src=[10, 13])
sc(2, SIEGE([clash("ncamp", 0), clash("out_w", 0)], clip=CLIP("카이사르 『갈리아 전기』 7권 84장", "등 뒤의 [[함성]]이 가장 두려웠다\n내 목숨이 남의 용기에 달렸으니", on="함성이")), src=[23])
sc(2, m("south", "south", WALLS() + [LOCK("post", on="높은 곳에", text="카이사르의 지휘소 (추정)"), red_a([[4.512, 47.521], [4.49, 47.524]], on="사람을"), red_a([[4.512, 47.521], [4.525, 47.53]], on="사람을")], tilt=38), src=[23])
sc(1, SIEGE([zone(OUTER, None, 0, color="#c9242c"), red_a(SHORT, 0.2, 1.2), badge("ring_s", "지름길 = 두 벽 사이", "#c9242c", on="지름길", dy=60)]), sfx=PING(1.4))
sc(3, NORTH([blue_a(DOWN_REA, 0, 1.3), zone([[4.46, 47.558], [4.474, 47.558], [4.474, 47.553], [4.46, 47.553]], "메워진 함정", on="흙을", color="#1f5fbf"), clash("ncamp", on="방패를", size=1.2)]),
   sfx=FAR(0), src=[23])
sc(2, m("north", "siege", WALLS() + [red_a(LAB, on="라비에누스에게", w=1.2), badge("ncamp", "라비에누스 · 6개 대대", "#c9242c", on="여섯", dy=60)], flight=["north", "siege"], flightDur=1.6, tilt=34), src=[23])
sc(3, SIEGE([blue_a(TO_STEEP, on="가파른", w=1.2), LOCK("steep", on="가파른", text="가파른 비탈 · 함정이 적다"), clash("steep", on="뜯어냈습니다")]), src=[23])
sc(3, m("south", "south", WALLS() + [red_a(BRUTUS, on="브루투스에게"), badge("steep", "브루투스 · 6개 대대", "#c9242c", on="브루투스에게", dy=-60),
                                    badge("in_s", "파비우스 · 7개 대대", "#c9242c", on="파비우스에게", dy=60), LOCK("post", on="카이사르 자신이", text="카이사르")], tilt=38), sfx=PING(2.2), src=[23])
sc(2, SIEGE([red_a(CAESAR_N, on="북쪽 언덕으로", w=1.3), badge("ncamp", "라비에누스 · 39개 대대", "#c9242c", on="서른아홉", dy=60)]), src=[23])
sc(3, ai("caesar_cloak", lower={"date": "마지막 날 오후", "title": "멀리서도 알아본 겉옷", "sub": "흔히 붉은 망토로 전해진다 · 7권 88장"}), label=DRAMA, src=[23])
sc(3, NORTH([blue_a(DOWN_REA, 0, 1.2), red_a(CAESAR_N[-3:], 0.1, 1.2), clash("ncamp", on="함성이", size=1.4)]), sfx=FAR(0), src=[23])
sc(2, NORTH([red_a(CAV_OUT, on="등 뒤에", w=1.4), badge("behind_rea", "바깥으로 돌아온 로마 기병", "#c9242c", on="돌려보낸", dy=-60)]), sfx=PING(1.2), src=[23])
sc(2, NORTH([red_a(CAV_OUT[-3:], 0, 1.3), red_a(CAESAR_N[-3:], 0, 1.3), dash_b(FLEE_N, on="달아났습니다")]), src=[23])
sc(2, NORTH([dash_b(FLEE_N, 0), badge("rea", "세둘루스 전사", "#1f5fbf", on="세둘루스가", dy=-60), badge("behind_rea", "베르카시벨라우누스 생포", "#1f5fbf", on="사로잡혔죠", dy=60)],
            counters=[cnt(74, "개", "카이사르 앞에 놓인 갈리아 군기", on="일흔네")]), src=[23])
sc(1, SIEGE([dash_b(BACK_IN, on="물러났습니다")]), src=[24])
sc(2, m("siege", "auxois", WALLS() + [dash_b(p, on="흩어졌습니다") for p in SCATTER] + [badge("relief", "사라진 구원군", "#1f5fbf", on="사라졌죠", dy=70)],
        flight=["siege", "auxois"], flightDur=2.2, tilt=30, tone="night"), clock="그날 밤", src=[24])
next_act()

# ===== 제7막 · 답 =====
sc(3, SIEGE([LOCK("town", 0.4, "베르킨게토릭스")], clip=CLIP("카이사르 『갈리아 전기』 7권 89장", "나는 [[모두의 자유]]를 위해\n이 전쟁을 시작했다", on="모두의")), pauseBefore=0.5,
   chapter={"num": "제7막", "title": "답"}, clock="다음 날", sfx=SW(0), src=[24])
sc(2, m("south", "south", WALLS() + [LOCK("post", on="앉아", text="진영 앞의 카이사르")], tilt=38), src=[24])
sc(3, ph("royer", pos="50% 50%", marks=[mk("베르킨게토릭스", 0.3, 0.14, "베르킨게토릭스는"), mk("카이사르", 0.75, 0.14, "카이사르의 둘레를", "red")]), label=plabel("royer"), src=[25])
sc(1, ph("motte_surr", pos="50% 45%", marks=[mk("끝까지 한마디도 없이", 0.5, 0.12, "한마디도")]), label=plabel("motte_surr"), src=[25])
sc(3, SIEGE([unit("town", "무기를 내려놓다", "blue", 0.1), badge("post", "포로 · 병사 한 사람에 한 명", "#c9242c", on="한 사람씩", dy=-60), badge("in_w", "하이두이·아르베르니는 남겨 두다", "#1f5fbf", on="하이두이족과", dy=60)]), src=[24])
sc(2, globe([4.5, 47.5], [12.0, 42.5], TO_ROME, [{"ll": [4.5, 47.54], "text": "알레시아"}, {"ll": [12.48, 41.9], "text": "로마 · 기원전 46년 처형", "on": "사십육년"}], on="로마로", dur=3.4), src=[26])
sc(2, SIEGE([], tilt=30), hook={"question": {"text": QUESTION, "on": "어떻게", "kicker": "■ 답 ■"}})
sc(3, SIEGE([IN_L(0.1), OUT_L(0.3), badge("between", "감옥이 아니라 성", "#c9242c", on="성이었죠", dy=-60)]), sfx=PING(1.6))
sc(2, ph("traps", pos="50% 50%", marks=[mk("구덩이 하나 · 말뚝 하나", 0.5, 0.12, "구덩이")]), label=plabel("traps"))
sc(3, SIEGE([red_a(SHORT, on="짧은 길로", w=1.3), blue_a(LONG, on="바깥 둘레를", w=1.0), badge("ring_s", "안쪽의 짧은 길", "#c9242c", on="짧은", dy=60), badge("relief", "바깥의 먼 길", "#1f5fbf", on="크게", dy=70)]), src=[23])
sc(3, SIEGE([unit("town", "굶주린 성", "blue", 0.1), blue_a(INSIDE_W, on="서두르게"), blue_a(NIGHT_HIT, on="바로 그 벽")], counters=[cnt(30, "일 넘게", "곡식이 떨어진 성", on="굶주림이")]), src=[11, 14])
sc(2, cmp("숫자가 많았던 쪽", "갈리아", "하나로 움직인 쪽", "로마군", "blue", "red"))
sc(1, GAUL([mark(k, "blue", 0.1 + 0.15 * i) for i, k in enumerate(["arverni", "bibracte", "senones", "sequani", "lemovices", "bituriges"])] + [badge("alesia", "끝내 하나가 되지 못한 갈리아", "#1f5fbf", on="하나가", dy=-70)]),
   date="", legend=LEG_GAUL, scale="100 km")
sc(2, ph("site", pos="50% 55%", marks=[mk("1861 · 나폴레옹 3세의 발굴", 0.5, 0.12, "나폴레옹")]), label=plabel("site"), date="1861", src=[27, 28])
sc(2, ph("plan", pos="50% 50%", marks=[mk("카이사르가 적은 그 도랑", 0.5, 0.1, "도랑들이"), mk("1991~1997 프랑스·독일 공동 발굴", 0.5, 0.2, "천구백구십일년부터는", "red")]), label=plabel("plan"), date="1991", src=[30, 31])
sc(2, ph("statue", pos="50% 40%", marks=[mk("높이 6.6m", 0.5, 0.12, "육 점 육"), mk("나폴레옹 3세를 닮은 얼굴", 0.5, 0.22, "닮게", "red")]), label=plabel("statue"), date="", src=[28, 29])
sc(3, ph("statue_t", pos="50% 35%"), label=plabel("statue_t"), clip=CLIP("동상 받침돌 · 1865", "하나로 뭉친 갈리아는\n[[온 세상]]과도 맞설 수 있다", on="받침돌에는", pos="right"), src=[27])
sc(2, globe([4.5, 47.5], [36.0, 38.0], TO_CARRHAE, [{"ll": [4.5, 47.54], "text": "알레시아"}, {"ll": [39.03, 36.87], "text": "카레 · 기원전 53년", "on": "카레"}], on="사막입니다", dur=3.6))
sc(1, {"type": "endcard", "title": "알레시아의 두 벽 앞에서 쓰러진 모든 이들을 기억하며", "q": pin("panorama")}, tail=1.0)
assert CUR["i"] == len(ACTS[6]), (CUR, len(ACTS[6]))

# ===== 재연 그림 — 실사풍 시네마틱 재연 (지도사 표준 4-5항 · Cloudflare FLUX 무료 엔진) =====
RE = "Cinematic photorealistic historical reenactment, 52 BC Roman Gaul, muted desaturated film color, 35mm documentary still, "
ROM = "Roman legionaries in mail shirts, bronze helmets and red tunics with curved rectangular shields"
GAL = "Gallic Celtic warriors with long hair, moustaches, checked woollen cloaks, long swords and oval wooden shields"
END = ", people seen from behind or at a distance, faces not identifiable, leaving calm uncluttered darker area in the upper right, no text, no letters, no captions, no logos, no readable symbols."
AI = {
    "relief_hills": RE + "a vast Gallic relief army of tens of thousands spread over rolling green hills at dawn, seen from far away behind a Roman earthen rampart with wooden towers in the foreground" + END,
    "exile": RE + "a young Gallic nobleman in a dark cloak walking away from the wooden gate of a Celtic hilltop town, followed by a few poor ragged men, overcast winter day" + END,
    "snow_pass": RE + "a long column of " + ROM + " clearing deep snow with shovels to cross a high mountain pass in a winter blizzard" + END,
    "scorched": RE + "Gallic villagers setting fire to their own thatched farmhouses and grain stores, columns of black smoke over a flat winter countryside" + END,
    "avaricum_rain": RE + ROM + " climbing over a timber-laced stone Gallic town wall during a heavy rainstorm, siege towers in the mist" + END,
    "gergovia_charge": RE + ROM + " running up a steep slope toward a high Gallic hilltop town wall while Gallic defenders counterattack from above, chaos and dust" + END,
    "cavalry_oath": RE + "Gallic cavalry chieftains on horseback raising their swords together in a solemn oath around a camp fire at dusk" + END,
    "steep_hill": RE + "Roman officers on horseback on a low ridge looking up at a large flat-topped hill crowned with the timber ramparts of a Gallic town, two small rivers at its foot, late summer" + END,
    "stakes": RE + ROM + " hammering sharpened forked tree branches into a trench in long rows in front of an earthen rampart" + END,
    "lilia": RE + "close view of rows of cone-shaped pits dug in the ground, each with a sharpened fire-hardened wooden stake at the bottom, Roman soldiers covering them with brushwood" + END,
    "granary": RE + ROM + " stacking sacks of grain and bundles of hay inside a fortified Roman camp behind a palisade, late summer" + END,
    "council": RE + GAL + " arguing in a smoky dim wooden hall lit by torches, starving and exhausted" + END,
    "mandubii": RE + "Gallic families, women, children and old people walking out of the gate of a hilltop town carrying small bundles, toward distant Roman earthworks, grey sky" + END,
    "guards": RE + ROM + " standing guard on top of a wooden palisade and earthen rampart, looking down at a distant crowd of civilians in the field below" + END,
    "archers": RE + "Gallic cavalry filling a wide plain with light infantry and archers running between the horses, dust clouds, afternoon light" + END,
    "german_charge": RE + "a dense mass of Germanic horsemen in furs charging at full gallop across a plain into Gallic cavalry, dust and sunset light" + END,
    "hurdles": RE + GAL + " weaving brushwood hurdles and building long wooden ladders and grappling hooks in a large camp at dusk" + END,
    "night_wall": RE + "night battle at a Roman earthen rampart with wooden towers, torches, stones and arrows flying, Gallic warriors throwing brushwood bundles into a ditch" + END,
    "rea_descent": RE + "thousands of " + GAL + " rushing down a wide hillside at noon toward a Roman camp with a palisade, bright sunlight" + END,
    "caesar_cloak": RE + "a Roman general in a flowing scarlet red cloak on horseback seen from behind, leading fresh cohorts and cavalry along an earthen rampart toward a hill battle" + END,
    "thumb_bg": ("Cinematic photorealistic war painting, 16:9 wide aerial view of a flat-topped hill with a Gallic town in the center, surrounded by two concentric Roman earthen rampart rings with wooden towers, "
                 "Roman soldiers between the two rings, a huge Gallic army attacking the outer ring from the surrounding hills, warm golden late-summer light, full color, high contrast, "
                 "the upper part of the frame darker sky, no text, no letters, no logos."),
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
# 숫자가 들어간 문장은 src 필수 (DocuKit 2항)
NUMW = re.compile(r"[0-9]|만 명|천 명|백 명|마일|킬로미터|피트|인치|스무|마흔|일흔|서른|스물")
nosrc = [s["id"] for s in S if not s.get("src") and any(NUMW.search(disp(l)) for l in s["lines"]) and s["visual"]["type"] not in ("titlecard", "endcard")]
print("숫자 문장 src 없음:", nosrc)

ids = [s["id"] for s in S]
chap = [i for i, s in enumerate(S) if s.get("chapter")]
sid = lambda i: S[i]["id"]
music = [{"id": "drone", "from": "s001", "to": sid(chap[0] - 1), "volume": 0.2},
         {"id": "theme", "from": sid(chap[0]), "to": sid(chap[1] - 1), "volume": 0.16},
         {"id": "analysis", "from": sid(chap[1]), "to": sid(chap[2] - 1), "volume": 0.16},
         {"id": "somber", "from": sid(chap[2]), "to": sid(chap[3] - 1), "volume": 0.17},
         {"id": "tension", "from": sid(chap[3]), "to": sid(chap[4] - 1), "volume": 0.17},
         {"id": "march", "from": sid(chap[4]), "to": sid(chap[5] - 1), "volume": 0.16},
         {"id": "analysis", "from": sid(chap[5]), "to": ids[-1], "volume": 0.16}]
(HERE / "photo_pins.json").write_text(json.dumps(PINS, ensure_ascii=False, indent=1), encoding="utf-8")
# target_sec: 승현 eleven_v3 첫 편 — 샘플 추정 공백 포함 초당 약 6.3자 → 약 7,700자 ≈ 20:20 (첫 미리보기 실측으로 갱신)
board = {"title": "안팎이 모두 적: 알레시아 공방전", "subtitle": "포위하면서 포위당한 카이사르 · 기원전 52년",
         "lang": "ko", "sub_max": 28, "voice": "0mlAtfsvMzFpppUuNWkV", "tts_model": "eleven_v3", "tempo": 1.0, "max_pause": 0.65,
         "look": "archive", "sub_style": "dark", "map_tone": "day", "card_max": 0.25,
         "tts_mode": "act", "style": 2, "sfx_policy": "doc", "bgm_rel_db": -24, "sync_limit": 0.5,
         "target_sec": 1230, "midrolls": MID, "land": LAND, "places": P, "views": V, "music": music, "ai_images": AI, "scenes": S}
(HERE / "storyboard.json").write_text(json.dumps(board, ensure_ascii=False, indent=1), encoding="utf-8")
types = collections.Counter(s["visual"]["type"] for s in S)
CARD = {"text", "black", "document", "compare", "bars", "checklist", "reasons", "punch", "quotes"}
print("scenes", len(S), "chars", sum(len(say(l)) for s in S for l in s["lines"]), "mid", MID, "chap", [sid(i) for i in chap],
      "ai", len(AI), "pins", len(PINS), dict(types))
print("map %.0f%% · card %.0f%%" % (100 * types["map"] / len(S), 100 * sum(types[k] for k in CARD) / len(S)))
