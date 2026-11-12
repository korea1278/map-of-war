# Map of War (`map-of-war`) 영문 롱폼 영구 제작 표준 규칙

> 적용: **다음 에피소드(`ep09` 이후)부터 제작하는 모든 영문 롱폼**. 완성된 `ep08-chosin`은 건드리지 않는다(API 재호출 금지). 2026-11-13 사용자 지시로 등록.

1. 소통 및 에셋 언어 분리 원칙 (Language Separation)
   - 클로드와의 모든 대화, 진행 상황 보고, 오류 안내는 반드시 **한국어**로 작성할 것.
   - 실제 영상에 들어가는 모든 결과물(7막 나레이션 대본, 자막 JSON, 썸네일 카피, 유튜브 제목/설명)은 **100% 영문(US/Western Military History 다큐멘터리 톤)**으로 생성할 것.

2. 오디오 막(Act) 단위 통파일 생성 원칙 (Strict Act-by-Act Single MP3)
   - 문장이나 자막 줄 단위로 쪼개서 ElevenLabs API를 호출하는 행위 전면 금지 (문장 끝음 단절 및 디지털 팝 노이즈 원천 차단).
   - 반드시 **1개 막(Act) 전체 영문 텍스트를 1회의 API 호출로 단일 통파일(`act1.mp3` ~ `act7.mp3`)**로 추출하여 문단 단위의 자연스러운 호흡과 억양을 유지할 것.
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

---
## 구현 메모 (Claude용 · 엔진 현황과의 차이)
- 2번: 이미 구현됨 — 보드 `"tts_mode": "act"` + 장면별 `"act": n` → `pipeline/tts.py main_acts()`가 막마다 1회 호출해 `public/ep/<ep>/tts/acts/act<n>.mp3` 저장 후 글자 타임스탬프로 장면 분할
- 3번: **구현 완료 (2026-11-13, war-docu와 같은 엔진 코드)** — 보드 최상단 `"sfx_policy": "doc"` + `"bgm_rel_db": -24`. `pipeline/timeline.py doc_sfx()`가 금지 효과음(`boom`·`hit`·`artillery`(근거리)·`mg`·`drum`·`pop`) 삭제, 콜아웃 자동 pop 제거, 막 전환(`chapter`)마다 `whoosh` 스윕 1회 자동, 같은 효과음 15초 쿨다운, 볼륨은 나레이션 대비 dB(`whoosh`·`ping` -26 / `artillery_far`·`wind`·`tank` -30 / `water`·`birds` -32, cue `"db"`로 -24~-32 조정). 효과음·BGM LUFS는 `public/sfx/loudness.json`·`public/bgm/loudness.json`. 레이더 핑 `public/sfx/ping.mp3`(ffmpeg 합성, 비용 0). 장면에 넣을 것: 3D 비행 `whoosh`, 클라이맥스 `artillery_far`·`wind`, 핵심 록온 `ping`. 적용 사례: war-docu `episodes/ep26-seungho/storyboard.json`
- 4번: 자막 싱크 허용 오차를 ±0.5초로 — `pipeline/check_sync.py` 기준(현재 ±1.0초)을 영문 보드에서 0.5로 강화
