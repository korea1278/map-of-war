"""목소리 비교 샘플 (2026-11-19 추가): 같은 다큐 문장 하나를 여러 목소리·설정으로 몇 초씩 만들어 voice_samples/에 저장.
지금 목소리(Srd5)는 저음 갈라짐(지지직)이 있어 대체 후보를 귀로 비교하려는 용도. 비용: 샘플당 약 90자.
후보 = 지금 목소리 설정 변형 + Minho + 일레븐랩스 공유 라이브러리의 한국어 남성 나레이션 인기 목소리 몇 개(자동 검색)."""
import json, os, re, sys
from pathlib import Path
import requests

KEY = os.environ.get("ELEVENLABS_API_KEY") or sys.exit("ELEVENLABS_API_KEY 비어 있음")
H = {"xi-api-key": KEY}
API = "https://api.elevenlabs.io/v1"
OUT = Path("voice_samples"); OUT.mkdir(exist_ok=True)
N_SHARED = int(os.environ.get("N_SHARED") or 5)
TEXT = os.environ.get("TEXT") or (
    "기원전 사백구십 년 구월. 아테네 북쪽 마라톤 평원에서 청동 갑옷을 입은 농민 만 명이 "
    "세계 최대 제국의 군대와 마주 섰습니다. 그들에게는 기병도 궁수도 없었거든요.")
BASE = {"stability": 0.55, "similarity_boost": 0.78, "style": 0.0, "use_speaker_boost": True}

try:
    sub = requests.get(f"{API}/user/subscription", headers=H, timeout=30).json()
    print(f"남은 글자 크레딧: {sub.get('character_limit', 0) - sub.get('character_count', 0)} / 목소리 칸 {sub.get('voice_slots_used')}/{sub.get('voice_limit')}")
except Exception as e:
    print("구독 정보 확인 실패:", e)

mine = {v["voice_id"]: v for v in requests.get(f"{API}/voices", headers=H, timeout=30).json().get("voices", [])}
print("내 목소리:", ", ".join(f"{v['name']}({k})" for k, v in mine.items()))

cands = [
    {"tag": "01_지금목소리_기본", "voice": "Srd5jY77m6kKijR9vy6R", "model": "eleven_multilingual_v2", "set": BASE},
    {"tag": "02_지금목소리_안정성075", "voice": "Srd5jY77m6kKijR9vy6R", "model": "eleven_multilingual_v2", "set": {**BASE, "stability": 0.75}},
    {"tag": "03_지금목소리_turbo25", "voice": "Srd5jY77m6kKijR9vy6R", "model": "eleven_turbo_v2_5", "set": BASE},
    {"tag": "04_민호_격전의지도", "voice": "U1cJYS4EdbaHmfR7YzHd", "model": "eleven_multilingual_v2", "set": BASE},
]

# 공유 라이브러리: 한국어 남성 — 나레이션·교육용 우선, 많이 쓰인 순
seen, shared = set(c["voice"] for c in cands), []
for params in ({"use_cases": "narrative_story"}, {"use_cases": "informative_educational"}, {}):
    try:
        r = requests.get(f"{API}/shared-voices", headers=H, timeout=30,
                         params={"language": "ko", "gender": "male", "page_size": 40, "sort": "usage_character_count_1y", **params})
        vs = r.json().get("voices", [])
    except Exception as e:
        print("공유 목소리 검색 실패:", e); vs = []
    for v in vs:
        if v["voice_id"] in seen: continue
        if (v.get("age") or "") == "young": continue  # 다큐용이라 젊은 목소리 제외
        seen.add(v["voice_id"]); shared.append(v)
print(f"공유 라이브러리 후보 {len(shared)}개")
for v in shared[:20]:
    print(" -", v["name"], v["voice_id"], v.get("age"), v.get("use_case"), (v.get("description") or "")[:80].replace("\n", " "))

def tts(c):
    body = {"text": TEXT, "model_id": c["model"], "voice_settings": c["set"]}
    return requests.post(f"{API}/text-to-speech/{c['voice']}", params={"output_format": "mp3_44100_128"},
                         headers={**H, "Content-Type": "application/json"}, json=body, timeout=120)

n = 5
for v in shared:
    if n >= 5 + N_SHARED: break
    name = re.sub(r"[^0-9A-Za-z가-힣]+", "", v["name"])[:20] or "voice"
    cands.append({"tag": f"{n:02d}_{name}", "voice": v["voice_id"], "model": "eleven_multilingual_v2", "set": BASE,
                  "owner": v.get("public_owner_id"), "desc": (v.get("description") or "")[:200], "name": v["name"]})
    n += 1

report = []
for c in cands:
    r = tts(c)
    if r.status_code != 200 and c.get("owner"):
        # 공유 목소리는 내 목소리 목록에 추가해야 쓸 수 있는 경우가 있음 (목소리 칸 1개 사용)
        a = requests.post(f"{API}/voices/add/{c['owner']}/{c['voice']}", headers={**H, "Content-Type": "application/json"},
                          json={"new_name": c.get("name", c["tag"])}, timeout=60)
        print("  추가 시도", c["tag"], a.status_code, a.text[:150])
        if a.status_code == 200:
            c["voice"] = a.json().get("voice_id", c["voice"]); c["added"] = True
            r = tts(c)
    ok = r.status_code == 200 and r.headers.get("content-type", "").startswith("audio")
    if ok:
        (OUT / f"{c['tag']}.mp3").write_bytes(r.content)
    print(("성공 " if ok else f"실패 {r.status_code} {r.text[:200]} ") + c["tag"])
    report.append({k: c.get(k) for k in ("tag", "voice", "model", "set", "name", "desc", "added")} | {"ok": ok})

(OUT / "list.json").write_text(json.dumps({"text": TEXT, "samples": report}, ensure_ascii=False, indent=1))
if not any(x["ok"] for x in report): sys.exit("샘플을 하나도 못 만듦")
