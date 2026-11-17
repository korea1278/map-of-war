# 격전의 세계사 (`map-of-war`) 롱폼 영구 제작 표준 규칙

> 🔄 2026-11-18 사용자 지시로 한국어 채널로 전환 — 아래 1번 언어 규칙은 '대화·에셋 모두 한국어'로 바뀌었다. 나머지 규칙은 그대로

> 적용: **`ep01`부터 제작하는 모든 영문 롱폼** (이 채널의 정식 편은 `ep01`부터 시작 — 2026-11-18 사용자 확인). war-docu에서 함께 들어온 참고용 `ep08-chosin`은 건드리지 않는다(API 재호출 금지). 2026-11-13 사용자 지시로 등록.

1. 소통 및 에셋 언어 분리 원칙 (Language Separation)
   - 클로드와의 모든 대화, 진행 상황 보고, 오류 안내는 반드시 **한국어**로 작성할 것.
   - 실제 영상에 들어가는 모든 결과물(7막 나레이션 대본, 자막 JSON, 썸네일 카피, 유튜브 제목/설명)은 **100% 한국어 다큐멘터리 톤**으로 생성할 것 (2026-11-18 전환 · 참고용 ep08-chosin만 영문).

2. 오디오 막(Act) 단위 통파일 생성 원칙 (Strict Act-by-Act Single MP3)
   - 문장이나 자막 줄 단위로 쪼개서 ElevenLabs API를 호출하는 행위 전면 금지 (문장 끝음 단절 및 디지털 팝 노이즈 원천 차단).
   - 반드시 **1개 막(Act) 전체 영문 텍스트를 1회의 API 호출로 단일 통파일(`act1.mp3` ~ `act7.mp3`)**로 추출하여 문단 단위의 자연스러운 호흡과 억양을 유지할 것.
   - 기본 내레이터 (2026-11-18 교체): ElevenLabs Voice ID **`Srd5jY77m6kKijR9vy6R`**, `model_id` `eleven_multilingual_v2`, `stability` 0.55 · `similarity_boost` 0.78 · `style` 0.0 (차분하고 또박또박한 다큐 톤, 과장된 억양 방지). 믹싱 밸런스는 나레이션 0dB · BGM -24dB 그대로. 참고용 `ep08-chosin`은 예전 Adam 유지
   - 대본 정제 규칙:
     * `(dramatically)`, `(pause)` 등 **괄호 연출 지문 전면 금지** (순수 낭독 텍스트만 작성).
     * TTS 엔진이 부자연스럽게 숨을 멈추지 않도록 **불필요한 쉼표(`,`) 과다 사용 금지**.

3. 절제된 다큐멘터리 SFX 믹싱 기준 (2026-11-13 사용자 수정 지시 — 이전 '효과음 전면 금지'를 대체. 전면 삭제는 영상이 지나치게 건조해짐 · war-docu와 동일)
   1) 절대 금지할 효과음 (Ban)
      - **갑작스럽고 과장된 저음 폭발/타격음('꽝' 하는 Loud Boom, Heavy Slam SFX) 금지.**
      - 캐릭터(컨트리볼), 말풍선, 텍스트 박스, 체크리스트가 뜰 때마다 반복 재생되는 **가벼운 UI `Pop` 효과음 전면 금지.**
      - 동일 효과음이 15초 이내에 연속으로 중복 재생되는 현상 금지 (쿨다운 최소 15초 이상 적용).
   2) 적절히 살려서 배치할 효과음 (Allow & Mix)
      - **전술 지도 및 장면 전환:** 막(Act)이 바뀌거나 3D 카메라가 주요 고지·전장으로 크게 이동(Flythrough)할 때만 차분하고 묵직한 저음 스윕(Subtle Cinematic Whoosh/Sweep)을 절제하여 1회 사용.
      - **전장 현장감 앰비언스(Ambience):** 대규모 포격전, 돌파전, 고지 사투 등 클라이맥스 장면에 한해 나레이션을 방해하지 않는 선에서 은은한 배경 현장음(먼 포성 울림, 바람 소리, 무전 교신 노이즈 등)을 아주 낮게(`-28dB ~ -32dB`) 깔아 몰입감 부여.
      - **전술 HUD 포인트:** 적 포위망이 완성되거나 핵심 타깃 록온 링이 활성화될 때만 절제된 레이더 비프(Radar Ping) 효과음 1회 허용.
   3) 전체 오디오 밸런스 기준
      - 메인 성우 나레이션: `0dB` (기준)
      - 다큐멘터리 BGM: `-22dB ~ -26dB`
      - 절제된 포인트 SFX / 현장 앰비언스: `-24dB ~ -32dB` (절대 나레이션 목소리를 덮거나 놀라게 하지 않는 수준)

4. Remotion 렌더링 및 전술 지형 연출 표준
   - 시간 함수(`Date.now()`, `setTimeout`) 사용 금지, 철저히 `frame / 30` 기반 결정론적 프레임 제어(Deterministic Rendering) 엄수.
   - `MapView` 3D 지형 비행(`CatmullRomCurve3`), SVG Path 스트로크 진격선 및 파티클 스웜, 밀리터리 Tactical HUD 오버레이 표준 유지.
   - 자막 싱크는 통으로 추출된 `act1.mp3` ~ `act7.mp3`의 실제 음파 파형에 맞춰 동기화할 것 (오차 ±0.5초 이내).

5. 초반 60초 모순 누적 후킹 구조 (2026-11-18 war-docu EP29에서 이식 · 상세는 [`docs/HOOK_STANDARD.md`](HOOK_STANDARD.md))
   - **사건 직격(0~10초) → 모순 3단 누적(10~40초, "A였다. 그런데도 B였다." × 3) → `X` 마크 반전(통념 부정 + "Or was it?") → 중앙 핵심 질문 카드(50~60초)** 순서를 지킬 것.
   - 앵글 후보 3개(갈등형·숫자형·질문형)를 모순 3단에 순서대로 쓰고, 핵심 질문은 본편 후반에 명시적으로 회수(대본 머리에 `회수 표시`).
   - 화면 부품: `LeftStatHud`(좌측 수치 HUD) · `NegationOverlay`(붉은 X) · `CoreQuestionCard`(중앙 질문 카드) · `troops`(병력 대비 대열) — 장면 `"hook"` 필드.

6. 4~6초 단위 시각 레이어 교차
   - 첫 60초는 4~6초마다 서로 다른 종류의 화면 레이어(3D 지도 비행 · HUD 수치 · 병력 대열 · 사료 사진 강조 · X 반전 · 질문 카드)로 교차하고, 같은 종류를 2회 연속 쓰지 않는다. 본편은 3~5초마다 장면 전환 또는 `on` 팝업 1개.

7. GitHub Actions 비대기(Non-Blocking) 실행 원칙
   - 렌더링(`make-video.yml`) dispatch 후 **세션 안에서 `gh run watch`·폴링으로 완료를 기다리지 않는다.** dispatch 성공을 확인하면 즉시 사용자에게 "컴퓨터를 꺼도 된다" 안내를 맨 첫 줄로 출력하고, 완료 확인은 `send_later` 예약으로 넘긴다 (사용자는 PC방에서 작업 — 대기 시간이 곧 비용).
   - 엔진·문서만 바꾸는 작업(이번 이식처럼)은 렌더 워크플로를 실행하지 않고 push 후 바로 종료한다.

---
## 구현 메모 (Claude용 · 엔진 현황과의 차이)
- 2번: 이미 구현됨 — 보드 `"tts_mode": "act"` + 장면별 `"act": n` → `pipeline/tts.py main_acts()`가 막마다 1회 호출해 `public/ep/<ep>/tts/acts/act<n>.mp3` 저장 후 글자 타임스탬프로 장면 분할
- 3번: **구현 완료 (2026-11-13, war-docu와 같은 엔진 코드)** — 보드 최상단 `"sfx_policy": "doc"` + `"bgm_rel_db": -24`. `pipeline/timeline.py doc_sfx()`가 금지 효과음(`boom`·`hit`·`artillery`(근거리)·`mg`·`drum`·`pop`) 삭제, 콜아웃 자동 pop 제거, 막 전환(`chapter`)마다 `whoosh` 스윕 1회 자동, 같은 효과음 15초 쿨다운, 볼륨은 나레이션 대비 dB(`whoosh`·`ping` -26 / `artillery_far`·`wind`·`tank` -30 / `water`·`birds` -32, cue `"db"`로 -24~-32 조정). 효과음·BGM LUFS는 `public/sfx/loudness.json`·`public/bgm/loudness.json`. 레이더 핑 `public/sfx/ping.mp3`(ffmpeg 합성, 비용 0). 장면에 넣을 것: 3D 비행 `whoosh`, 클라이맥스 `artillery_far`·`wind`, 핵심 록온 `ping`. 적용 사례: war-docu `episodes/ep26-seungho/storyboard.json`
- 4번: **구현 완료 (2026-11-18 war-docu에서 이식)** — 보드 최상단 `"sync_limit": 0.5`를 넣으면 `pipeline/check_sync.py`가 ±0.5초로 검사 (없으면 예전 ±1.0초). 영문 자막 한 줄은 44자 고정(`sub_max`는 한국어 보드 전용)
- 5·6번: **구현 완료 (2026-11-18 war-docu EP29 `e8ef7627`에서 이식)** — `remotion/Hook.tsx`(HookOverlays·TroopsV), `Video.tsx`(장면 `hook` 있으면 오버레이), `Visuals.tsx`(`troops`), `timeline.py`(장면 `hook` 통과 · `xOn`/`checkOn` 변환). 사용법은 `docs/HOOK_STANDARD.md`
- 화면 업그레이드 2단계(`Stage.tsx` stage·flatmap·flaggrid·checklist·reasons·PhotoTag/PhotoMarks · 캐릭터 face/prop/anim)·`public/chars/` 44장·`public/ui/paper.jpg`도 같은 날 이식 완료
