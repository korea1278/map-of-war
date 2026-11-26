# map-of-war — 한국어 전쟁사 다큐 《격전의 세계사》 제작 운영 규칙 (SOP)

> ## 🔄 2026-11-18 사용자 지시: **이 저장소는 한국어 채널 '격전의 세계사'로 전환** (이전 '영문판 전용' 규칙 폐기)
> - 영상 에셋(대본·나레이션·자막·화면 문구·질문 카드·썸네일 카피·제목·설명·태그)은 **100% 한국어**. 사용자와의 대화도 한국어
> - 대본 문체는 격전의 지도(war-docu) 한국어 편과 같게: 낭독용 순수 텍스트, 숫자는 한글 발음(자막은 `SUBS`로 숫자), 괄호 지문·한자·영문·쉼표 없음, "~습니다/~죠/~거든요" 다큐 톤. 보드 `"lang": "ko"`, `"sub_max": 28`
> - 목소리는 **ElevenLabs 창욱 `ZJCNdZEjYwkOElxugmW2`** (2026-11-19 교체 · eleven_multilingual_v2 · stability 0.55 · similarity 0.78 · style 0.0). 예전 `Srd5jY77m6kKijR9vy6R`은 아주 낮은 저음(평균 85Hz)이라 헤드셋에서 목소리마다 '지지직' 갈라짐이 들려 폐기 — 설정(안정성 0.75·turbo 모델)을 바꿔도 그대로였음. EP01 마라톤만 Srd5로 완성됨. 목소리 비교는 Actions '목소리 비교 샘플'(`voice-test.yml`, 브랜치 `voice-test`)
> - **썸네일 배경은 컬러** (2026-11-19 사용자 지시 · 흑백 금지 · EP01·EP02도 컬러로 다시 렌더). 썸네일 카피도 한국어 (`PAROHO_V2` → thumb 모드 `thumbnails/<ep>_ko_A.png`·`_ko_A2.png`, `thumbnails/<ep>/thumb_a.png`·`thumb_b.png`)
> - 아래 본문에 남아 있는 '영문·영어' 표현은 참고용 `ep08-chosin`(영문, 건드리지 않음) 시절 기록이다. 새 편은 위 한국어 규칙이 우선
> - 한국 전쟁(6·25) 위주의 '격전의 지도'는 계속 `korea1278/war-docu`에서 만든다. 이 저장소는 로드맵 `docs/EPISODE_ROADMAP_50.md`의 세계 전쟁사 50편

- 사용자는 PC방에서 작업한다. 로컬 설치를 요구하지 말고 모든 렌더링은 GitHub Actions에서 한다.
- 엔진 코드(pipeline·remotion·workflows)는 `war-docu`에서 복사해 왔다. 두 저장소는 자동 동기화되지 않으므로, `war-docu`의 엔진 개선이 필요하면 그때 옮겨 온다.

> ## ⚠️ 필수: [`docs/LONGFORM_STANDARD.md`](docs/LONGFORM_STANDARD.md) 영구 제작 표준 준수 (2026-11-13 사용자 지시 · **`ep01`부터 모든 영문 롱폼** · 참고용 `ep08-chosin`은 제외·API 재호출 금지)
> 새 에피소드 작업 전에 이 문서를 먼저 읽고 따른다. 아래 규칙과 충돌하면 그 문서가 우선. 핵심 요약:
> 1. **언어** — (2026-11-18 전환) 대화·보고와 영상 에셋 모두 한국어 (참고용 `ep08-chosin`만 영문)
> 2. **막(Act) 단위 통 MP3** — 문장·줄 단위 ElevenLabs 호출 금지, 막 1개 = 1회 호출 = `act1.mp3`~`act7.mp3` (`tts_mode: "act"`). 괄호 지문 금지, 쉼표 과다 금지
> 3. **절제된 다큐 효과음** (2026-11-13 수정 — 전면 삭제 취소) — '꽝' 폭발·타격음과 UI Pop 금지, 같은 소리 15초 쿨다운. 막 전환·3D 비행 때 묵직한 스윕 1회, 클라이맥스에만 먼 포성·바람 앰비언스(-28~-32dB), 핵심 록온 때 레이더 핑 1회. BGM은 나레이션 대비 -22~-26dB, 효과음은 -24~-32dB (`"sfx_policy": "doc"`, `"bgm_rel_db": -24`)
> 4. **결정론 렌더** — `Date.now()`·`setTimeout` 금지, `frame/30` 기반. MapView 3D 비행·진격선·스웜·전술 HUD 유지. 자막 싱크는 막 통 MP3 실제 파형 기준 ±0.5초 이내
> 5. **초반 60초 모순 누적 후킹** (2026-11-18 war-docu에서 이식 · [`docs/HOOK_STANDARD.md`](docs/HOOK_STANDARD.md)) — 사건 직격 → 모순 3단 누적 → `X` 마크 반전 → 중앙 질문 카드. 장면 `"hook"` 필드(`hud`·`neg`·`question`) + `troops` 병력 대열
> 6. **4~6초 단위 시각 레이어 교차** — 첫 60초는 4~6초마다 다른 종류의 화면(지도 비행·HUD·병력 대열·사료 강조·X·질문 카드), 같은 종류 연속 금지
> 7. **GitHub Actions 비대기 실행** — dispatch 후 `gh run watch`·폴링으로 기다리지 않는다. dispatch 확인 즉시 "컴퓨터를 꺼도 된다" 안내를 첫 줄에 내고 완료 확인은 `send_later` 예약. 엔진·문서만 바꾸는 작업은 렌더를 돌리지 않고 push 후 종료

## ★★★★ '지도사' 방식 화면·목소리 표준 (2026-11-24 사용자 지시 · war-docu·map-of-war 공통 · 다음 신규 편부터 · 필수 참조 `docs/REFERENCE_JIDOSA_121.md`)
> 사용자가 레퍼런스 영상(지도사 「김신조 일행은 왜 못 잡았을까? 지도로 보는 1·21 사태」)을 주며 "무엇이 다른지 분석해서 고쳐 달라", "일레븐랩스 목소리가 너무 부자연스럽다"고 함. 실측 비교: 레퍼런스 지도 약 65~70%·글자 카드 약 5% / 우리 EP33 지도 32%·글자 카드 37%
- 보드 최상단 기본값: `"look": "archive"`, `"sub_style": "dark"`, `"map_tone": "day"`, `"tts_model"`(비교 샘플로 고른 모델), `"tempo": 1.0`, `"max_pause": 0.65`, `"card_max": 0.25`
- 장면: `date`·`clock`(왼쪽 위 작전 시계 판, 다음 장면으로 이어짐) · `legend`·`scale`(오른쪽 위 범례, 지도만) · `visual.tone: "night"` · `visual.lower`(사진·그림 하단 제목) · `clip`(지도 위 사료 인용 카드, `[[형광펜]]`, `orig` 원문)
- **지도 60% 이상 · 글자 카드 25% 이하** (timeline.py가 비율 출력·초과 경고), 숫자·이유·인용은 지도 위에 얹고 같은 지도를 이어 쓴다. 장 제목은 시간·숫자로
- 재연 그림은 실사풍 시네마틱 재연이 기본(볼 캐릭터는 stage에만) — 프롬프트 예시는 docs 4-5항
- 목소리: 배속 끔 + 쉼 0.65초, 모델은 **비교 샘플에서 귀로 고른 쪽**(`tts_model`). ⚠️ v3가 늘 낫지는 않다 — 2026-11-24 샘플 22개 실측에서 민호는 v3가 오히려 높낮이 폭이 12→4반음으로 평평해졌고, 창욱·수현·승현·훈민은 v3에서 쉼이 자연스러워짐. 샘플 기록: map-of-war 브랜치 `voice-test`. 목소리를 바꿀 때는 map-of-war Actions '목소리 비교 샘플'(`voice-test.yml`, 입력 `extra`=이름:ID 목록, `models`=eleven_v3,eleven_multilingual_v2)로 귀로 고른 뒤 보드 `voice`만 바꾼다 (비교용으로 추가한 공유 목소리는 끝나면 자동 삭제)
- 켜지 않은 예전 편은 렌더 결과가 바뀌지 않는다 (TTS 서명도 그대로라 재생성 없음)
- ★ **채널 목소리 확정 (2026-11-24 사용자 선택: "승현으로 가자")** — ElevenLabs **승현 `0mlAtfsvMzFpppUuNWkV`**(공유 라이브러리, 따뜻한 전문가 톤 중년 남성) · `"tts_model": "eleven_v3"`(stability 0.5 · similarity 0.78) · `"tempo": 1.0` · `"max_pause": 0.65`. war-docu·map-of-war **다음 신규 편부터** 보드 `"voice"`에 이 ID. 이미 만든 편(민호·창욱)은 다시 만들지 않는다. 새 목소리라 첫 편 미리보기에서 말 속도를 실측해 분량 환산을 갱신할 것 (그 전 추정: 샘플 기준 공백 포함 약 6.3자/초 → 20분 30초 ≈ 7,800자). API가 공유 목소리를 거부하면(404 등) 일레븐랩스 웹에서 승현을 내 목소리에 추가
- ★ **레퍼런스 화면을 그대로 베끼지 말 것 (2026-11-24 사용자 지시: "비슷하게는 찬성, 똑같이 하면 표절")** — 아이디어(늘 보이는 날짜·시각, 범례, 낮/밤 지도, 지도 위 인용)만 쓰고 모양은 채널 고유: 날짜는 왼쪽 위 짙은 반투명 '작전 시계' 판 한 줄(노란 세로 막대 · 흰 고딕 날짜 · 노란 시각), 범례는 짙은 유리판 + 노란 윗줄, 사진 하단 제목은 노란 세로 막대 + 고딕 제목, 강조 카드는 왼쪽 노란 막대. 레퍼런스의 큰 명조 날짜·빨간 시각 칩·미색 종이 범례·노란 날짜 칩 하단 제목은 쓰지 않는다

## ★★★★★ 다큐 설명 영상 스킬 표준 'DocuKit' (2026-11-26 사용자 지시 · war-docu·map-of-war 공통 · 다음 신규 편부터 · 필수 참조 [`docs/DOCU_SKILL_STANDARD.md`](docs/DOCU_SKILL_STANDARD.md))
> 사용자가 튜토리얼 영상(Claude '다큐 설명 영상' 스킬로 포클랜드 3분 다큐 제작)을 주며 "분석해서 스킬 적용, 대본·화면 퀄리티 업데이트" → 9가지 전부 적용. 엔진은 우리 쪽이 앞서 있어 그대로, 모양은 베끼지 않고 채널 고유 디자인으로
- **대본 전 리서치 브리프** `episodes/<ep>/research.md` — 연표 · [번호] 출처(실제로 열어 본 것만) · **숫자 충돌**(출처끼리 다른 숫자와 대본 표현) · 앵글 후보
- **비트 시트·자료 체크리스트** — 장면 `"src": [1,3]`(숫자 문장은 필수) · `"need": {what, required, fallback}`(사용자 제공 자료) → `python3 pipeline/plan_sheet.py <ep>` → `beats.md`·`assets.md` (0원, 세션). ⚠️ 0개 목표, 사용자 제공 자료는 이때 한 번에 요청
- **목소리 ↔ 대본 대조** `pipeline/asr_check.py` — 미리보기 때 Actions가 자동 실행(Whisper turbo 무료 받아쓰기, 약 3~5분, 경고만) → `logs/asr_check_<ep>.txt`의 빠짐·덧붙음·바뀜(3글자 이상)을 미리보기 확인 때 같이 본다
- **새 화면** (`remotion/DocuKit.tsx` 두 저장소 같은 파일): `globe`(지구본 원정 항로 + 거리 카운터 · zoom) · `weapon`(무기 실루엣 sub/ship/carrier/jet/plane/tank/galley/cannon/missile + 어뢰·미사일·화살·포탄 발사) · `punch`(초단타 반전 한 줄 + 노란 밑줄, 한 편 2~4번) · 어느 화면에나 `visual.counters`(오른쪽 위 숫자·시간 카운터 판)·`visual.stamp`(객체: 도장 쾅) · 지도 아이템 `ring`(km 반지름 구역·사거리 원) · 인용 카드 `clip.recreated`(원문 재구성 표시)
- globe·weapon은 한 편에 각 3~6장면 정도 — 늘 지도가 주인공(지도 60%↑ 기준 유지)

## ★ 무료 오픈소스 화질·입체 업그레이드 (2026-11-24 사용자 지시 · war-docu·map-of-war 공통 · 추가 비용 0원)
> 모두 자동이라 새 편에서 따로 켤 필요 없음. 어느 단계가 실패해도 렌더는 예전 방식으로 계속된다
1. **사진 화질 개선 — Real-ESRGAN `realesr-general-x4v3`(BSD-3)**: `pipeline/enhance.py`가 긴 변 1600px 미만 사료 사진(`photos/`)만 4배로 키워 `public/fx/<ep>/photos_<이름>.hd.jpg`로 저장(원본은 그대로, 흑백 사진은 흑백 유지). torch 없이 onnxruntime — 공식 .pth를 스크립트가 직접 ONNX로 바꿈
2. **2.5D 입체 사진 — Depth Anything V2 Small(Apache-2.0)**: 사진·재연 그림마다 깊이 지도 `public/fx/<ep>/<폴더>_<이름>.depth.png`를 만들고, `remotion/ui.tsx` `KenBurns`(→ `DepthCanvas`)가 캔버스에서 픽셀마다 깊이만큼 다르게 밀어 가까운 사람·물체가 배경보다 더 움직이게 함(켄번즈 in/out = 깊이 돌리, left/right/up = 깊이 패럴랙스). 잘라 붙이는 레이어 방식은 배경에 번진 자국이 생겨 폐기 — 와핑 방식이라 구멍 없음
   - ⚠️ **Base/Large/Giant 모델은 CC-BY-NC(비상업)라 절대 쓰지 말 것** — Small만
   - 렌더 비용: 깊이 장면 1프레임당 약 0.2초 추가(20분 편 전체 약 5~10분)
   - 끄기: 보드 `"fx": false`(전부) · `"parallax": false`(입체만) · `"upscale": false`(화질만) · 장면 `visual.parallax: false`(그 장면만 — 글자 많은 문서 사진 등 휘면 어색한 장면)
3. **핸드헬드 미세 흔들림 — `@remotion/noise`(MIT)**: 모든 사진·그림 켄번즈에 최대 ±0.35%의 아주 느린 손떨림(frame 기반 결정론)
4. **한국어 자막 줄바꿈 — kiwipiepy(형태소 분석)**: `timeline.py` `split_phrase`가 글자 규칙 위에 형태소로 확실한 경우만 보정 — 꾸미는 말(지친·모인·그·두) 뒤·'A와 B' 나열·명사+명사(부대·지명) 사이는 끊지 않고, 이음말(~고·~며·~는데·~아서) 뒤에서 끊음. 설치 실패 시 예전 규칙 그대로
5. **썸네일 배경 컬러 복원 — DDColor-tiny(Apache-2.0, map-of-war 전용)**: thumb 모드에서 `pipeline/colorize.py`가 `PAROHO_V2` 배경이 흑백 사료 사진이면 색을 입혀 `public/ep/<ep>/thumbcolor/<폴더>_<이름>.jpg`로 저장 → `ParohoV2Thumb`가 있으면 자동 사용. 끄기: 항목에 `colorize: false` 또는 `gray: true`. ⚠️ AI가 추측한 색이라 군복·깃발 색이 틀릴 수 있음 → 썸네일 PNG를 직접 열어 확인. 모델은 Hugging Face(edgetools/ddcolor)에서 받음 — 세션에선 접속 불가라 Actions에서만 동작(첫 실행 때 로그 "[colorize]" 확인)
6. **썸네일 누끼 — BiRefNet(`birefnet-general-lite`, MIT)** 우선 → 실패하면 isnet → u2net → 흰 배경 알파 (`ai_images.py cutout`, 별도 프로세스라 메모리 부족으로 죽어도 다음 모델로). ⚠️ BRIA RMBG는 비상업 라이선스라 쓰지 말 것. 캐릭터(`chars.py`)는 예전대로 rembg 금지
- 결과 `public/fx/`·모델 `.cache/models/`는 `.gitignore`(저장소 용량 보호) → Actions 캐시(`fx-v1-`)로 재사용, 캐시가 없으면 다시 계산(무료). Actions 단계 "사진 화질 개선 + 2.5D 깊이 지도"는 사진·그림 단계 바로 뒤, 나레이션 앞
- 세션에서 확인: `cd pipeline && python3 enhance.py <ep> && python3 timeline.py <ep>` → 번들 → `remotion still`(Hugging Face·pytorch 서버는 세션에서 막혀 있고 모델은 GitHub 릴리스에서 받음)

## 제작 이력

> ⚠️ **이 채널의 정식 에피소드는 아직 0편이다 (2026-11-18 사용자 확인).** 첫 편은 `ep01`부터 시작하고, 기획은 [`docs/EPISODE_ROADMAP_50.md`](docs/EPISODE_ROADMAP_50.md)의 EP01~EP50 순서를 따른다. 아래 `ep08-chosin`은 war-docu에서 분리할 때 함께 가져온 **참고용** 편(번호 체계에 포함하지 않음, 업로드된 정식 편 아님)이다.

| EP | id | 나레이션 | 결과 | 메모 |
|---|---|---|---|---|
| 01 달려서 덮쳤다: 마라톤 전투 (기원전 490) · 7막(1막=콜드 오프닝) · **한국어** | `ep01-marathon` | 약 10,000자 · 181장면 · target_sec 1697 · **본 렌더 28:18 · -15.2 LUFS · 1.74GB · 자막 381/381 · 싱크 ±0.5초 통과 · 릴리스 `ep01-marathon-20261118-0415`** | 처음엔 영문으로 만들었다가 사용자 지시로 한국어 전환(영문 미리보기는 TTS 전에 취소), 한국어 미리보기 28:17 (2026-11-18, 목표 20:30보다 7분 47초 김 → 사용자 결정: 대본 그대로 28분 본 렌더, target_sec 1697). 미리보기 뒤 수정: `marathon` 뷰 중심·범위(작은 늪·산 라벨이 화면 밖), s005 강조 라벨 위치, s047 그림(돌에 '490 BC' 글자)은 프롬프트를 되돌리고 파일에서 글자 부분만 지움(서명 유지·재생성 0). **2026-11-18 본 렌더 1차 실패**: 그 그림 하나를 다시 그리려다 Gemini 선불 크레딧 소진(402)으로 '재연 일러스트' 단계에서 전체 중단 → `ai_images.py`에 대체 경로 추가 | 격전의 지도 EP29 실측 8,632자 = 20:30 (Minho) — 이번 편은 약 10,000자라 새 내레이터 속도에 따라 23분 안팎 예상, 미리보기 실측 뒤 분량 판단. 한반도 밖 첫 전장 — 보드 `land`(그리스+주변국 ISO) · 래스터 `aegean_sea`·`attica_sea`·`marathon_zoom_sea`. 새 부품: 지도 `phalanx`·`zone`·`ships`, `troops` `profile` 정면 전열(gr/pe). stage 미사용. 미드롤 `s042`·`s096`·`s125`, 사진 17장 핀, AI 44장. 확인 안 된 사실 `episodes/ep01-marathon/unverified_facts.md`. 썸네일 v2 한국어 카피(달려서 덮쳤다 / 제국이 도망쳤다 · A2 기병도 궁수도 없이 / 어떻게 이겼을까?) |
| 02 대함대를 꾀었다: 살라미스 해전 (기원전 480) · 7막(1막=콜드 오프닝) · **한국어 · 창욱 첫 편** | `ep02-salamis` | 8,274자 · 151장면 · target_sec 1225 · **본 렌더 20:17 · -15.0 LUFS · 1.25GB · 자막 431줄 · 릴리스 `ep02-salamis-20261118-1951`** | 1차 미리보기 6,755자 = 16:39 → 2~6막에 1,519자 보강(아토스 운하·에피알테스·아리스테이데스 도편·지팡이 일화·아이기나 매복 등, 1·7막 TTS 유지) → 20:17. 해협 함선 좌표를 키노수라곶·프시탈레이아 밖 물 위로 수정, 헬레스폰토스용 `north` 뷰. Cloudflare 무료 한도(두 저장소 공용 1만 뉴런) 소진으로 새 그림 3장 빈 화면·충각 그림이 숫양 뿔로 → 문서 카드·올림피아스 사진으로 교체 | 새 래스터 `salamis_zoom_sea`(z13, 해안이 계단처럼 거칠게 보임 — 다음 해전 편은 z14 고려). 지도 `ships` color 파랑(그리스)·빨강(페르시아). 미드롤 `s034`·`s080`·`s100`. 사진 21장 핀, AI 28장. 확인 안 된 사실 `episodes/ep02-salamis/unverified_facts.md`. 썸네일 v3 카피(“페르시아 시점”에서 본 그리스 함대의 덫 / 아테네를 불태운 대함대가 / 좁은 해협에서 무너진 이유 · A2 좁은 해협으로 / 대함대를 꾀었다) |
| 03 단 한 번의 돌격: 가우가멜라 전투 (기원전 331) · 7막(1막=콜드 오프닝) · **한국어 · 창욱** | `ep03-gaugamela` | 8,079자 · 152장면 · target_sec 1230 · **본 렌더 19:59 · -15.0 LUFS · 1.23GB · 자막 419줄 · 싱크 ±0.5초 통과 · 릴리스 `ep03-gaugamela-20261124-0820`** | 미리보기 1차 실패: 4막 마지막 장면 s084의 마지막 글자 끝 시각이 막 끝 무음까지 늘어나 싱크 검사 0.93초 오탐 → `tts`·`tts_fast/s084.json` `ends[-1]`만 보정(재생성 0). 2차 미리보기에서 전장(field) 지도가 남북으로 길어 화면 밖으로 잘림 → 전장 위도를 0.45배 압축·span 0.2·중심 36.511, `zone()` 인자 순서 버그로 평지가 청록색 → 수정, 넓은 지도 중심 조정 | 새 래스터 `neareast_sea`(z6, 목록 맨 앞=맨 아래)·`mesopotamia`(z8)·`nineveh`(z11)·`gaugamela_zoom`(z14). 전장 좌표는 모식(마케도니아 서쪽·정면 동쪽 → 오른쪽=남쪽). 미드롤 `s040`·`s085`·`s108`. 사진 22장 핀, AI 20장(Cloudflare 정상). 확인 안 된 사실 `episodes/ep03-gaugamela/unverified_facts.md`. 썸네일 v3(“페르시아 시점”에서 본 알렉산드로스의 돌격 / 직접 고른 전장에서 / 대왕이 먼저 도망친 이유 · A2 단 한 번의 돌격 / 대왕이 도망쳤다) |
| 04 일부러 밀렸다: 칸나이 전투 (기원전 216) · 7막(1막=콜드 오프닝) · **한국어 · 창욱** | `ep04-cannae` | 약 8,250자 · 167장면 · target_sec 1221 · **본 렌더 20:21 · -15.1 LUFS · 1.26GB · 자막 416줄 · 릴리스 `ep04-cannae-20261124-1215`** | 미리보기 20:21 한 번에 통과(사진 18·그림 15 정상). 미리보기 뒤 수정: 전장 뷰 span 0.09→0.13(양 끝 기병 라벨 잘림)·진영 좌표 화면 안으로, `carthage`·`westmed_n`·`north_it`·`apulia_s` 뷰 추가(라벨 잘림), 라벨 겹침 dy 조정, 포위 움직임 강화(로마 run 110 · 카르타고 bend ±45/70 · wrap 110), 트럼불 그림 pos | 새 래스터 `westmed_sea`(z6)·`italy_sea`(z8)·`apulia_sea`(z11)·`cannae_zoom`(z14). 전장 모식(로마 북쪽·정면 남쪽·오른쪽 끝=강). 지도 `phalanx` bend 음수=불룩한 초승달. 미드롤 `s042`·`s090`·`s114`. 확인 안 된 사실 `episodes/ep04-cannae/unverified_facts.md`. 썸네일 v4(칸나이 \| 기원전 216 · [2배 가까운] 로마군이 / 하루 만에 {갇힌} 이유 · A2 한니발의 덫 · 일부러 {밀려} 주고 / 통째로 포위했다) |
| 08 Battle of Chosin Reservoir (1950): The 17-Day March Out of Frozen Hell · 7막 | `ep08-chosin` | 3,175단어 · 약 18,000자 · 92장면 · target_sec 1230 | 미리보기 20:18 (war-docu에서 실행, 2026-11-12, 3,149단어) → 7막 s87에 2문장 보강(+약 12초) · s63 어두운 코르세어 사진을 근접 항공 지원 사진으로 교체 | 지시서 2,600~2,900단어는 실측 환산 18:50이라 러닝타임 우선 보강. 미드롤 `s31`·`s56`·`s80`, CTA1 3막 끝 `s43`, CTA2 7막 끝 `s91`. 그림 9장은 war-docu EP06 `jangjin`에서 복사(파일·서명) + 새 그림 14장, 사진 26장 war-docu 검증 핀. 지형 `yudam_zoom`(z13)·`funchilin_zoom`(z14). 고지 1282·1240·1403·1081·헬파이어 밸리 좌표 개략 |

**분량 환산 — 창욱 1.02배속 실측 (2026-11-19 EP02 본 렌더)**: 8,274자(151장면) = 20:17 → 초당 약 6.8자 (샘플 비교 때 예상과 달리 Srd5보다 빠름). **20분 30초 ≈ 약 8,350자**, 22분 ≈ 약 9,000자. 6,755자는 16:39였음

**분량 환산 — 한국어 Srd5jY77m6kKijR9vy6R 1.02배속 실측 (2026-11-18 EP01 미리보기)**: 10,000자(181장면) = 28:17 → 초당 약 5.9자. 20분 30초를 맞추려면 약 7,200~7,300자. (격전의 지도 Minho는 8,632자 = 20:30으로 이보다 약 20% 빠름)

**분량 환산 (영문 Adam 1.02배속 실측 — 새 내레이터는 말 속도가 다를 수 있으니 ep01 미리보기 실측으로 갱신할 것)**: 3,045단어(18,130자) = 20:16 · 17,824자 = 20:18 (92장면). 20분 30초를 맞추려면 약 18,000자 / 3,180단어.

## ★ 기획 원칙 — 앵글 전환 & 도입부 1분 (2026-11-12 사용자 지시 · 유튜브 피드백 반영 · 다음 편부터 war-docu·map-of-war 공통 영구 적용)
1. **소재를 풀어내는 앵글 전환** — 전투명에 기대지 말고 **인간적 갈등 · 극적인 숫자 · 미스터리 질문**으로 포장한다
   - 제목·썸네일 카피·첫 문장은 '구체적 상황 묘사'로: "235고지 전투"(X) → "물도 탄약도 끊긴 영국군 700명이 버틴 사흘"(O)
   - 전투명은 검색용으로 제목 뒤쪽(콜론·괄호)이나 설명글·태그로 보낸다
   - 대본을 쓰기 전에 앵글 후보 3개(갈등형·숫자형·질문형)를 먼저 뽑고, 가장 강한 것을 제목·썸네일·훅에 일관되게 쓴다. 숫자는 사료로 확인된 것만
2. **도입부 1분 몰입감** — 영상 시작 직후 60초 안에 **결말의 긴박한 복선이나 질문**을 먼저 던진다 (긴 시청 시간이 조회수의 핵심)
   - 0~10초: 가장 극적인 순간(절정·결말 직전)으로 바로 시작 — 배경 설명·연도 나열로 시작 금지
   - 10~45초: "어떻게 / 왜 ~했을까?" 핵심 질문 + 끝까지 보면 답이 나온다는 약속, 결말을 암시하되 다 밝히지 않음
   - 45~60초: 타이틀 카드 → 그다음부터 시간 순 배경 설명
   - 도입부에서 던진 질문은 본편 후반에 반드시 명시적으로 회수한다 (회수 장면을 대본에 표시)
   - 미리보기 확인 때 첫 1분(장면 시트 앞부분)이 위 구조인지 따로 점검한다

## ★ 연출 스타일 v2 — 레퍼런스 '강뉴부대' 영상 방식 (2026-11-12 사용자 지시 · 다음 편부터 war-docu·map-of-war 공통 · EP08 영문 장진호는 제외)
- 스토리보드 최상단에 **`"style": 2`** 를 꼭 켠다 (켜지 않은 기존 편은 예전 방식 그대로 렌더됨)
- **뜻 단위 자막 (엔진 `timeline.py` `split_phrase`)**: 글자 수 균등 분할 대신 쉼표·문장 끝·이음말(~고/~는데/~지만, and/but/which)에서 우선 끊고, 사람·부대·지명 이름 안, 숫자+단위, '~의' 뒤, 보조 용언(~고 있다, ~지 않다)은 끊지 않는다. 한 줄 최대 한국어 21자·영어 44자(+3자 여유). 숫자로 바꿔 쓴 자막(t≠say)도 단어 대응(`disp2say`)으로 실제 발음 시각에 맞춘다
- **단어 동기 표시 (`"on": "단어"`)**: 콜아웃·말풍선(bubbles)·지도 아이템(items)·효과음(sfx)·`visuals`·`hudCta` 어디에나 `"at"` 대신 `"on": "포로 0명"`처럼 대사 속 단어를 적으면 그 단어를 **말하는 순간** 나타난다 (`untilOn`·`takenOn`도 가능). 대사(say 또는 자막 t)에 없는 단어면 `logs/errors.txt`에 경고
  - 쓰는 곳: 핵심 숫자("9,500km", "포로 0명", "단 1개국"), 연도·날짜("1935년"), 사건명("이탈리아의 침공"), 이름을 부르는 순서대로 국기·부대·지명 하나씩 강조, 효과음
- **대본 쓰는 법 (레퍼런스 분석)**
  1. **한 문장 = 자막 한 줄 = 화면 변화 하나**. 문장은 자막 한 줄(한국어 21자·영어 44자) 안팎으로 짧게, 긴 문장은 쉼표로 뜻 단위를 나눠 쓴다
  2. **3~5초마다 화면에 뭔가 바뀐다** — 장면 전환, 또는 같은 장면 안에서 `on`으로 숫자·라벨·하이라이트·말풍선이 뜬다 (레퍼런스: 첫 5분 컷 57번 ≈ 5초당 1번). 20분 편은 장면 약 180~220개
  3. **질문 → 짧은 답 → 반응**: "그런데 이 목록에 좀 뜻밖의 나라가 하나 끼어 있습니다" → "바로 아프리카의 에티오피아" → 캐릭터 반응 말풍선("어? 여긴..?", "도와주세요!!"). 어려운 개념은 생활 비유로("보험 증서", "보험료 납부")
  4. 문서·조약·신문은 `document` 카드로 요점 2~4줄 + 도장/붉은 X, 목록·이유는 체크리스트·번호 카드로 하나씩 `on`에 맞춰 띄우고 지워 나간다
  5. 사료 사진은 좌상단 작은 출처 라벨 + 말하는 순간 뜨는 노란/빨간 강조 라벨

## ☑ 화면 업그레이드 2단계 + 초반 후킹 부품 + 썸네일 v2 — war-docu에서 이식 완료 (2026-11-18, war-docu `e8ef7627` 기준)
- `remotion/Stage.tsx`(stage·flatmap·flaggrid·checklist·reasons·PhotoTag/PhotoMarks·국기 SVG·캐릭터 face/prop/anim), `remotion/Hook.tsx`(LeftStatHud·NegationOverlay·CoreQuestionCard·TroopsV), 이를 쓰는 `Video.tsx`·`Visuals.tsx`·`MapView.tsx`(plane)·`theme.ts`·`Root.tsx`, `pipeline/timeline.py`(checkOn·xOn·hook·chars·sub_max)·`check_sync.py`(sync_limit)·`geo.py`·`chars.py`, `public/ui/paper.jpg`, **캐릭터 `public/chars/`**(파일 복사 — 다시 생성 금지, `make-chars.yml` 실행 금지)
- 사용법·필드는 war-docu `CLAUDE.md`의 '화면 업그레이드 2단계' 절과 war-docu `episodes/ep26-seungho/make_board.py` 헬퍼(C·pop·stage·flat·fpin·route·reasons·checklist) 참고. 영문 화면 문구(말풍선·카드·HUD·질문 카드)는 영어로 (`question.kicker` 기본값은 영문 보드에서 `■ THE QUESTION ■`)
- 새 나라 캐릭터는 SVG 볼 자동 대체(0원)

## ☑ 한반도 밖 전장 · 고대 전투 부품 (2026-11-18 EP01 마라톤에서 추가 · 이후 편 공통)
- **육지 마스크**: 보드 최상단 `"land": {"home": ["300"], "foreign": ["792", ...]}` (world-atlas ISO 숫자 코드). 없으면 예전 한반도 기본값. 보이는 나라만 넣을 것(러시아 643처럼 큰 나라는 렌더가 느려짐)
- **지형 래스터**: `pipeline/geo.py` `RASTERS`에 권역 추가(Actions `geo.py auto`가 새 권역만 생성). 바다는 `{"sea": True, "seeds": [...]}`, 근접 지도 장면은 `demSea: true`(make_board `m()`가 ZOOM 뷰에 자동)
- **지도 아이템**: `phalanx` `{path:[왼끝,오른끝], depth:[열마다 두께], face:±1(정면), px, color, run/runOn, bend/bendOn(가운데 후퇴), wrap/wrapOn(양익 포위), text}` · `zone` `{path:[다각형], color, text}` · `ships` `{pts, rot, dx, dy, sailOn, n}`
- **정면 전열 대열**: `troops` + `profile:[열마다 깊이]`, `side:"gr"|"pe"`, `vs:{side, profile}`, `runOn`·`bendOn`·`wrapOn`(상대의 얕은 날개 열은 wrap 때 패주해 사라짐). 라벨 `labels[].y`는 0.52 이하로(하단 자막 영역 피하기)
- 질문 카드 줄바꿈은 `\n` (`|` 아님). 사진 `tag`는 문자열

## ★★★★ 썸네일 표준 v5 'TV 우선 · 질문과 감정' (2026-11-26 사용자 지시 · war-docu·map-of-war 공통 · 다음 신규 편부터 · **아래 v4보다 우선** · 필수 참조 [`docs/THUMB_STANDARD_V5.md`](docs/THUMB_STANDARD_V5.md))
> 사용자가 썸네일 강의 영상(「give me 9 minutes, I'll make your thumbnails 81% better」)을 주며 "이런 조건에 맞게 나오게" → 6가지 조언 전부 반영. v4 디자인(태그·2줄·`[빨강]` `{노랑}`·box2)은 유지하고 위치·주인공·시안 수를 바꿈
- **TV 50% 테스트**: TV 홈·추천은 썸네일 위쪽 절반만 보임 → PAROHO_V2 항목에 **`tv: true`** = 태그 + 큰 글자 2줄을 **위쪽 46% 안**으로 (v4는 아래라 TV에서 사라짐). 주인공은 가운데~아래 가운데로 `bgPos`
- **썸네일 혼자 질문·감정을 만들 것** (제목에 기대지 말 것) — 항목에 `why: {q, e}` 기록, 문구 공식 5가지(질문형·단정 반전형·인물 감정형·숫자 대비형·미스터리형)
- **주인공 한눈에**: `focus` {x,y,rx,ry}(주변 어둡게) · `cut`(배경과 같은 크기 누끼 + 흰 테두리 — `pipeline/thumb_cut.py`, ⚠️ 주인공이 하나로 뚜렷한 사진만, 군중엔 금지) · `label` 이름표(위쪽 절반에)
- **겹침 금지** (2026-11-26 사용자 지시 "이름표와 썸네일 글자가 겹치면 불편 — 앞으로 안 나오게"): `HitThumb`가 label·note·bubble을 큰 글자·태그·서로와 겹치지 않게 자동으로 옮김(28px 간격, TV 가운데 선에 걸치지 않게) — 점검 시트로 최종 확인
- **군더더기 빼기**: note·bubble·화살표는 그 자체가 질문·감정을 만들 때만
- **시안 여러 개**: `alts: [...]` → A2·A3·… (줄 끝 `// ALTS:<ep> n=<개수>`), **최소 4개(A+3)·서로 다른 공식** → 유튜브 '테스트 및 비교' 3개 선택
- **점검 시트** `thumbnails/<ep>_check.jpg` (thumb 모드 자동 · `pipeline/thumb_check.py`): 원본 · TV 보기(위 절반만) · 휴대폰 홈 · 추천 목록 크기 — 전달 전에 직접 열어 확인
- **참고 10~15개·5가지 출처** (우리 잘된 편 · 남의 잘된 영상 · 같은 형식 다른 분야 · 저장해 둔 썸네일 · 유튜브 밖) → 편마다 `episodes/<ep>/thumb_plan.md`에 작동 원리 기록, 참고 서랍 [`docs/THUMB_REFERENCES.md`](docs/THUMB_REFERENCES.md)에 쌓기. 베끼지 말고 '어떻게'만

## ★★★ 썸네일 표준 v4 = '조회수 레퍼런스' 공식 (2026-11-24 사용자 지시 · war-docu·map-of-war 공통 · 이후 모든 신규 롱폼 A안 — 아래 v3보다 우선)
> 사용자가 조회수 잘 나온 남의 썸네일 5장(낙동강 '트럭 300대가/30대만 남았다' · '아마존강에 다리가 없는 이유' · 러일전쟁 · 73 이스팅 · 6.25 전쟁 전날)을 가져와 "지금 썸네일이 마음에 안 든다"며 이 방식으로 바꾸게 함
- 구현: `remotion/HitThumb.tsx`(두 저장소 같은 파일). `PAROHO_V2` 항목에 **`tag`가 있으면** `ParohoV2Thumb`가 v4로 렌더 (없으면 예전 v3 그대로 — 기존 편 영향 없음). 기준 결과물: war-docu `thumbnails/ep33-seobuksan_ko_A.png`·`_A2.png`, map-of-war `thumbnails/ep04-cannae_ko_A.png`·`_A2.png`
- 화면 구성 (1920×1080)
  1. 배경: 대본 핵심 장면 사진/재연 그림 Full-Bleed. 흑백·컬러는 저장소 기본 그대로(war-docu 흑백, map-of-war 컬러). **사람·피사체가 화면 위쪽 절반에 있는 사진**을 고를 것 — 아래 절반은 글자가 덮음 (EP33은 피사체가 아래에 있던 s061 대신 s123 곡사포반으로 교체)
  2. **왼쪽 위 태그 박스 `tag`** — 레퍼런스를 베끼지 말고 **대본에 맞게 매번 창작**: "장소 | 연월"(마산 서북산 | 1950.8), "사건 | 핵심 숫자"(서북산 혈전 | 45일), "작전·인물명"(한니발의 덫). `|`는 가는 구분선으로 표시. 색 `tagStyle`은 편 분위기로 고른다 — `red`(빨강 바탕·흰 글자: 위기·비극) · `cream`(미색 바탕·검은 글자: 전술 분석) · `black`(검정 바탕·흰 글자, `|` 뒤 노랑: 미스터리) · `yellow`(노랑 바탕: 의외의 사실) · `white`. A와 A2는 태그 문구·색을 다르게
  3. **하단 큰 글자 2줄** (`line1`·`line2`) — Pretendard Black, 굵은 검정 외곽선(7.5%)+그림자, 기본 흰색, **단어 단위 강조색 표기: `[빨강]` `{노랑}`** (예: `"부산 [턱밑]까지 와서"` / `"산 하나 {못 넘은} 이유"`). 한 줄에 강조 1~2곳, 숫자·핵심어만. 두 줄 같은 크기로 긴 줄이 가로를 채움(상한 210px, 최소 120px). **솔리드 블랙 바닥판 없음** — 사진 위에 글자, 글자 뒤만 어둡게 그라데이션
  4. `box2: true`(또는 색 문자열) — 2줄째를 빨간 박스 위 흰 글자로 (73 이스팅 레퍼런스 방식, 질문형·반전형에 어울림)
  5. 선택: 말풍선 `bubble: {text, x, y, to:[꼬리 끝 x,y], size}` (아마존강 '큰일납니다' 방식 — 등장인물의 한마디), `align`(left 기본·center·right — 피사체 반대쪽), `size`(글자 크기 직접), `note`(사진 설명 라벨 — 사람 위를 가리키지 말 것)
  6. **오른쪽 아래 재생시간 표시 없음**, 위 가운데 검은 박스(v3 `top`)는 v4에서 쓰지 않음
- **카피 공식 (대본에서 도출)**: Line 1 = [구체적 숫자·상황·불리한 전제] / Line 2 = [충격적 결과] + "~한 이유" 또는 단정형("~했다"). 줄당 5~10자. 숫자·사실은 대본에서 확인된 것만 (예: 칸나이는 8만 6천 vs 5만이라 '2배'가 아니라 '2배 가까운')
- 등록 예:
  ```
  "ep33-seobuksan": { bg: "ep/ep33-seobuksan/photos/s123_photo_0.jpg", bgPos: "50% 62%",
    tag: "마산 서북산 | 1950.8", tagStyle: "red", line1: "부산 [턱밑]까지 와서", line2: "산 하나 {못 넘은} 이유",
    alt: { tag: "서북산 혈전 | 45일", tagStyle: "cream", line1: "주인이 [19번] 바뀐", line2: "바위산의 비밀", box2: true } }, // ALTS:ep33-seobuksan
  ```
- 절차는 v3와 같음: 등록 → Actions `mode=thumb` 또는 세션 `npx remotion still … Thumbnail` → PNG를 직접 열어 확인(글자가 얼굴 안 가림·넘침 없음·태그와 피사체 안 겹침)

## ★★ 썸네일 표준 v3 = 레퍼런스 '베트콩 시점' 공식 (2026-11-18 사용자 지시 · war-docu·map-of-war 공통 · **2026-11-24부터 위 v4로 대체 — EP29~33·세계사 EP01~03 기록용** · 아래 v2·v5보다 우선)
- 구현: `remotion/Thumbnail.tsx` `PAROHO_V2` 표(이름 그대로) → `ParohoV2Thumb`가 새 디자인으로 렌더. 기준 결과물: war-docu `thumbnails/ep29-daejeon_ko_A.png`, map-of-war `thumbnails/ep01-marathon_ko_A.png`
- 화면 구성 (1920×1080)
  1. **배경 = 그 편 대본의 핵심 장면 사진, 전체 화면 컬러** — ⚠️ **2026-11-19 사용자 지시: map-of-war(격전의 세계사)는 흑백 말고 컬러** (`gray` 기본 false, war-docu는 흑백 그대로). 사료 사진이 있으면 장면 사진을 그대로 지정 `bg: "ep/<ep>/photos/sNNN_photo_0.jpg"`(스카우트 핀으로 받은 사진 — 추가 비용 0), 없으면(고대 등) 재연 그림 `ep/<ep>/ai/thumb_bg.jpg`. 어두우면 `bgFilter`로 밝기 보정
  2. **최상단 가운데 검은 라운드 박스 한 줄 `top`** — “ ” 안은 노랑 `#FFD83A`, 나머지 흰색 (44~66px 자동)
  3. **사진 설명 흰 라벨 + 휘어진 흰 화살표 `note`** `{text, x, y(라벨 중심), to:[x,y](가리킬 곳)}` — **라벨과 화살표는 사람(얼굴·몸) 위를 지나가지 않게**: 라벨은 하늘·안개·빈 땅 같은 빈 공간에 두고, 화살표는 짧게(200~350px) 빈 공간을 지나 대상의 가장자리를 가리킨다 (2026-11-18 사용자 수정)
  4. **하단 솔리드 블랙 바닥판**(사진이 위로 260px 페이드) 위 2줄 — Line 1 흰색(얇은 검정 외곽선) / Line 2 빨강 `#FF2B2B`
  5. **글자 크기**: 실측 글꼴 폭으로 좌우 56px 여백 안(1808px)을 꽉 채움. Line 2 상한 210px, Line 1 상한 200px·Line 2의 94% 이하, 최소 110px. **줄당 9~13자(띄어쓰기 포함)** 가 레퍼런스처럼 두 줄이 가로를 꽉 채우는 길이 — 짧으면 글자가 과하게 커지고 길면 작아짐
  6. **재생시간 배지 여백 없음, 시간 표시도 넣지 않음** (2026-11-18 사용자 지시)
- **카피 공식 (대본에서 도출)**: `top` = “[상대편·적] 시점”에서 본 [주인공]의 [사건] / Line 1 = [강한 상대·불리한 전제] / Line 2 = [의외의 결과] + "~한 이유". 숫자·사실은 대본에서 확인된 것만. `alt`(A2)에는 다른 앵글 카피
- 절차: 대본·사진 핀 확정 → `PAROHO_V2`에 한 줄(`bg`·`bgPos`·`top`·`line1`·`line2`·`note`·`alt` + 줄 끝 `// ALTS:<ep>`) → Actions `mode=thumb` 또는 세션에서 `npx remotion still … Thumbnail` → PNG를 직접 열어 확인(라벨이 얼굴 안 가림, 글자 넘침 없음)

## ★ 썸네일 표준 v2 (2026-11-18 war-docu에서 이식 · `ep01`부터 영문 A안 기본 · 참고용 `ep08-chosin`은 기존 공식 유지)
- **고정 인물 흑백 사진 폐기** (반복 기시감·CTR 저하) → **에피소드 고유 전술 비주얼을 배경 전체(Full-Bleed)로** (결정적 전황 재연 그림 `ep/<ep>/ai/thumb_bg.jpg` 또는 3D 지형)
- **하단 다크 비네팅** + 가장자리 비네트, **고대비 2줄 핵심 카피** — 기존 대비 2.5~3배(최대 340px, 최소 120px), 실측 폭으로 좌 60px~우측 재생시간 배지 여백 200px 안을 꽉 채움, 검은 외곽선 7% + 그림자. Line 1 흰색 / Line 2 머스터드 옐로 `#FFD400`(`color2`로 변경 가능). 영문 글꼴 Montserrat Black
- 선택: 좌상단 붉은 배지(`badge`, 예: `"JULY 20, 1950"`), 타깃 링(`targets`)·화살표(`arrows`)
- 등록: `remotion/Thumbnail.tsx`의 `PAROHO_V2` 표에 `"<ep>": { bg, bgPos, line1, line2, badge, alt: { line1, line2 } }` 추가 + 줄 끝에 `// ALTS:<ep>` → Actions `mode=thumb`가 `thumbnails/<ep>_en_A.png`·`_en_A2.png`를 1920×1080으로 렌더
- 카피는 줄당 2~4단어 영어, 콜드 오프닝 앵글(갈등·숫자·질문)과 같은 프레임. 렌더 후 PNG를 직접 열어 확인, 1.9MB 넘으면 JPG 자동 생성

## ★ 캐릭터 반복 방지 규칙 (2026-11-12 사용자 지시 · EP26 다음 편부터 · war-docu·map-of-war 공통 · 추가 비용 0원)
> 캐릭터 42장(`public/chars/`)은 계속 재사용하되, 매 편 같은 장면처럼 보이지 않게 아래를 지킨다. 전부 코드로 처리 — 그림을 새로 생성하지 말 것
1. **표정 덧그리기** — 같은 캐릭터 그림 위에 SVG로 표정을 얹는다: 화난 눈썹·땀방울·눈물·놀란 입·반짝 눈·식은땀 줄 (stage `chars[].face`: angry·sweat·tears·shock·smug·worried 등). 아직 없으면 다음 편 작업 때 `Stage.tsx`에 먼저 구현
2. **소품 씌우기** — 시대·인물에 맞는 소품을 SVG로 얹는다: 군모·철모·장교모·왕관·안경·훈장·담배 파이프·서류 가방 (`chars[].prop`)
3. **움직임** — 말하는 캐릭터는 통통 튀기, 고개 갸웃, 부들부들 떨기, 화면 밖에서 걸어 들어오기·나가기, 눈 깜빡임 (`chars[].anim`: bounce·tilt·shake·enter·exit)
4. **사용 규칙**
   - 캐릭터 무대(`stage`)는 전체 장면의 **25% 이하**
   - 같은 나라·같은 포즈 조합을 **연달아 두 장면** 쓰지 않는다. 한 편 안에서 같은 조합이 3번 넘게 나오지 않게 (좌우 뒤집기·위치·크기·표정·소품으로 반드시 변화)
   - 스토리보드 생성기에서 위 두 조건을 자동 검사해 어기면 경고(가능하면 assert)
   - 말풍선 문구는 매번 그 장면 대사에 맞춰 새로 쓴다 (편마다 같은 문구 재사용 금지)

## 1. 제작 순서

1. **대본** — `episodes/<ep>/script.md` (파일로). `## ACT n · 제목 [mm:ss–mm:ss]` 머리글로 막을 나눈다
   - **괄호 지문 금지** (`(pause)` 등), **쉼표 최소화** (ElevenLabs 호흡 끊김·팝 노이즈 방지)
   - 숫자는 낭독용 단어로 쓴다 (`November twenty-seventh`, `Hill twelve-eighty-two`). 자막은 생성기 `SUBS` 표가 숫자로 바꿔 보여 준다 (`November 27`, `Hill 1282`)
   - 문장은 `.`/`?`에서 나뉜다 — `Oliver P. Smith`처럼 약자 마침표는 쓰지 말 것 (문장이 쪼개짐)
   - 사실은 웹 검색으로 확인, 확정 못 한 것(발언 원문·좌표·수치)은 목록으로 남겨 전달 때 알린다
2. **스토리보드** — `episodes/<ep>/make_board.py`로 script.md 문장을 순서대로 장면에 배정해 `storyboard.json` 생성 (형식은 `episodes/ep08-chosin/`)
   - 보드 상단: `"lang": "en"`, `"voice": "0mlAtfsvMzFpppUuNWkV"`(승현, 2026-11-24~), `"tts_model": "eleven_v3"`, `"tempo": 1.0`, `"max_pause": 0.65`, **`"tts_mode": "act"`**, `"midrolls"`, `target_sec`, `"style": 2`, `"sfx_policy": "doc"`, `"bgm_rel_db": -24`, **`"sync_limit": 0.5`**(ep01~). 콜드 오프닝 장면에는 `"hook"` (docs/HOOK_STANDARD.md)
   - 장면마다 `"act": n` — **막 단위 TTS**: 막마다 일레븐랩스 1회 호출 → `public/ep/<ep>/tts/acts/act<n>.mp3` (지시서의 act1~act7 통 MP3) → `tts.py`가 글자 타임스탬프로 장면별 mp3·json으로 잘라 자막 싱크를 맞춘다. 문장 단위 생성 금지
   - 막 하나의 문장을 바꾸면 **그 막 전체가 다시 생성**된다(크레딧 약 2,500자). 수정은 막 단위로 모아서
   - 지도: `flight`(카메라 비행), `hud: true`(전술 HUD) + **`temp: "-40°F"`(HUD 온도 표시, EP08 추가)**, `tilt`, 아이템 `swarm`·`obj`·`clash`·`lock`·`shock`·`radar`·`badge`·`line`·`unit`·`arrow`
   - 사진: 장면별 `q: "<장면id>-photo"` + `photo_pins.json`에 `File:` 핀. **핀이 없으면 장면 id로 자동 검색돼 엉뚱한 사진이 들어온다** — 사진 장면마다 핀 필수
   - 그림: countryball 반실사 스타일 + "leaving calm uncluttered dark background area …, absolutely no speech bubbles … no text" 문구 필수. 미 해병 = 성조기 볼, 중공군 = 오성홍기 볼
   - 손으로 고친 뒤에는 생성기를 다시 돌리지 말 것
3. **커밋 → 미리보기** — Actions "영상 만들기" `episode=<ep>`, `mode=preview`, `english=false`
   - REST로 실행: `gh api -X POST repos/korea1278/map-of-war/actions/workflows/make-video.yml/dispatches -f ref=main -f 'inputs[episode]=<ep>' -f 'inputs[mode]=preview' -f 'inputs[english]=false'`
   - 끝나면 `git pull` 후 `previews/<ep>/sheet_*.jpg` 전부 육안 확인 (지도 자막·라벨 겹침·사진 라벨·어두운 사진), `logs/midroll_<ep>.txt`(러닝타임·목차·광고 위치), `logs/errors.txt`
4. **본 렌더** — 같은 명령에 `mode=full`
   - dispatch 직후 사용자 답변 **맨 첫 줄**에:
     ```
     ## 🛑 [안내] GitHub Actions 렌더링이 서버에 안착했습니다. 이제 피시방 컴퓨터를 끄셔도 됩니다!
     - 실행된 워크플로우: <에피소드명>
     - 진행 상태: In progress (클라우드 연산 중)
     ```
   - dispatch 직후 `send_later`로 확인 예약(20분 장편 약 2시간 10분~3시간). "끝나면 말씀해 주세요"로 미루지 말 것
5. **검증** — Releases MP4를 REST로 받아 길이(목표 ±10초), 음량 -15 LUFS ±1(`ffmpeg -af ebur128`), 지도 장면 프레임 포함 샘플 프레임 육안 확인, SRT·`logs/sync_check_<ep>.txt`·`logs/subs_check_<ep>.txt`
6. **썸네일** — **`ep01`부터는 위 '썸네일 표준 v2'** (`PAROHO_V2` 등록 → `mode=thumb`). 아래는 참고용 `ep08-chosin`에 쓴 예전 공식(영문): 좌측 3D 설산 작전 지도 + 우측 인물 흑백 누끼(`thumb_subject`) · 상단 인용 레드 `#FF3B30` · Line 1 흰색 100px · Line 2 옐로 `#FFE500` 112px · 우측 하단 재생시간 배지 여백 200px. 렌더 후 PNG를 직접 열어 확인, 1.9MB 넘으면 JPG
7. **전달** (한 번에) — Releases 링크, SRT, 썸네일, **영문** 제목 후보 3개·설명글(목차 타임스탬프는 SRT 실제 시각, 채널명·인사말 없이, 참고 자료·재연 일러스트 고지)·태그, 카테고리 Education, 확인 안 된 사실 목록. 설명은 한국어로

## 2. 고정 규격

| 항목 | 값 |
|---|---|
| 해상도 / 인코딩 | 1920×1080, 30fps, H.264 8Mbps, AAC 192k (20분 약 1.2GB) |
| 음량 | 렌더 후 `loudnorm` -15 LUFS |
| 나레이션 | **2026-11-24~ 신규 편 승현 `0mlAtfsvMzFpppUuNWkV` · eleven_v3 · 배속 없음** / (EP02~04) 창욱 `ZJCNdZEjYwkOElxugmW2` (2026-11-19~ 기본 · 이전 Srd5는 EP01만 · `eleven_multilingual_v2` · stability 0.55 · similarity_boost 0.78 · style 0.0), 1.02배속, `tts_mode: act` — 참고용 `ep08-chosin`만 예전 Adam `pNInz6obpgDQGcFmaJgB` 유지(API 재호출 금지) |
| 하단 자막 | Roboto Condensed 64px · 한 줄 44자 · 루트 글로벌 오버레이(z 9999)에서만 |
| 제목 글꼴 | Oswald |
| BGM | `public/bgm/` 공용 6곡 고정 (drone·theme·tension·march·analysis·somber), Music API 호출 금지 |
| 사진 표기 | 우상단 출처(영어 자동 변환) + 내용 라벨(연월), AI 그림은 "Dramatization" |
| 유튜브 카테고리 | Education |

자막 무결성(지도 장면 자막 누락 방지 구조)·카드 줄바꿈 원칙은 war-docu와 같다 — `remotion/ui.tsx`의 `GlobalSubtitleOverlay`, `MapView` 틸트 컨테이너 `overflow: hidden`, `pipeline/check_subs.py`·`check_sync.py`가 렌더 전 자동 검사.

## 3. 저장소 구조
- `episodes/<ep>/` script.md · make_board.py · storyboard.json · photo_pins.json
- `pipeline/` tts(막 단위 포함) · tighten · photos · ai_images · sfx · geo · timeline(+SRT) · preview · check_subs · check_sync · midroll
- `remotion/` 영상 컴포넌트 · `public/` geo·bgm·sfx·fonts·ui(공용) + ep/<ep>/ · `previews/` · `thumbnails/` · `logs/`
- 결과: Releases `<ep>-<날짜>` 태그에 MP4·SRT

## 4. 주의
- **이미지 크레딧 소진 대비 (2026-11-18 EP01 본 렌더 실패 후 추가)**: `ai_images.py`는 크레딧·권한 오류(402·429·RESOURCE_EXHAUSTED 등)를 만나면 같은 엔진을 재시도하지 않고 ① 예전 그림 파일이 있으면 그대로 사용 ② 없으면 무료 pollinations로 대체 ③ 그것도 안 되면 어두운 자리 표시 그림으로 렌더를 계속하고 `logs/errors.txt`에 남긴다 → 렌더 뒤 errors.txt의 '대체'·'자리 표시' 줄을 꼭 확인해 사용자에게 알릴 것
- **본 렌더 직전에는 그림 프롬프트를 바꾸지 말 것** — 프롬프트 한 글자만 바뀌어도 서명이 달라져 유료 재생성이 일어난다. 그림 속 글자 같은 작은 문제는 `public/ep/<ep>/ai/<이름>.jpg` 파일을 직접 손보면 서명이 그대로라 재생성되지 않는다
- Gemini 선불 크레딧은 AI Studio(https://ai.studio/projects)에서 충전·확인. 크레딧이 없으면 새 에피소드의 새 그림은 pollinations(무료, 화풍 다름)로 그려진다
- **GitHub Secrets 필요**: `ELEVENLABS_API_KEY`, `GEMINI_API_KEY` (선택: `CF_ACCOUNT_ID`, `CF_API_TOKEN`). 대화에 키를 적지 말 것
- Actions 실행 중에는 재료 파일(`public/ep`, `episodes`, `previews`)을 push 하지 말 것
- 이 세션 환경에서는 ElevenLabs·Gemini·위키미디어 직접 접속 불가 → 해당 작업은 Actions에서. `gh`는 REST(`gh api`)만
- 새 에피소드가 war-docu의 그림·사진을 재사용하려면, war-docu에서 파일(`public/ep/<src>/ai/*.jpg`)과 `ai.json` 서명·프롬프트를 이 저장소로 복사해 온다(재생성 비용 0). 사진은 `photo_pins.json`에 같은 `File:` 이름만 적으면 Actions가 다시 받는다
