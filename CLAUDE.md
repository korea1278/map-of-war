# map-of-war — 영문 전쟁사 다큐 《Map of War》 제작 운영 규칙 (SOP)

**이 저장소는 영문판 전용**이다 (2026-11-12 사용자 지시로 한국어 채널 '격전의 지도' 저장소 `korea1278/war-docu`에서 분리).
- 영문판은 **사용자가 요청할 때만** 만든다. 한국어판은 `war-docu`에서 만들고 이 저장소에 넣지 않는다.
- 사용자와의 대화·설명은 **항상 한국어**. 영상 에셋(대본·오디오·자막·썸네일 문구·제목·설명·태그)은 **100% 영어** (미국 시청자 · 켄 번스 다큐 톤 · US Western Military History 스타일).
- 사용자는 PC방에서 작업한다. 로컬 설치를 요구하지 말고 모든 렌더링은 GitHub Actions에서 한다.
- 엔진 코드(pipeline·remotion·workflows)는 `war-docu`에서 복사해 왔다. 두 저장소는 자동 동기화되지 않으므로, `war-docu`의 엔진 개선이 영문판에 필요하면 그때 옮겨 온다.

## 제작 이력

| EP | id | 나레이션 | 결과 | 메모 |
|---|---|---|---|---|
| 08 Battle of Chosin Reservoir (1950): The 17-Day March Out of Frozen Hell · 7막 | `ep08-chosin` | 3,175단어 · 약 18,000자 · 92장면 · target_sec 1230 | 미리보기 20:18 (war-docu에서 실행, 2026-11-12, 3,149단어) → 7막 s87에 2문장 보강(+약 12초) · s63 어두운 코르세어 사진을 근접 항공 지원 사진으로 교체 | 지시서 2,600~2,900단어는 실측 환산 18:50이라 러닝타임 우선 보강. 미드롤 `s31`·`s56`·`s80`, CTA1 3막 끝 `s43`, CTA2 7막 끝 `s91`. 그림 9장은 war-docu EP06 `jangjin`에서 복사(파일·서명) + 새 그림 14장, 사진 26장 war-docu 검증 핀. 지형 `yudam_zoom`(z13)·`funchilin_zoom`(z14). 고지 1282·1240·1403·1081·헬파이어 밸리 좌표 개략 |

**분량 환산 (영문 Adam 1.02배속 실측)**: 3,045단어(18,130자) = 20:16 · 17,824자 = 20:18 (92장면). 20분 30초를 맞추려면 약 18,000자 / 3,180단어.

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

## ☐ 예정: 화면 업그레이드 2단계 — 레퍼런스 수준 디자인 통일 (2026-11-12 사용자 확정 · **다음 편 제작 때 먼저 구현**하고 시작 · war-docu·map-of-war 공통)
> 아직 구현 안 됨. 다음 새 에피소드 작업 지시가 오면 대본보다 먼저 아래를 만들고, 시험 장면을 레퍼런스('강뉴부대' 영상)와 나란히 비교한 이미지를 사용자에게 보여 준 뒤 진행한다.
1. **고정 캐릭터 라이브러리** `public/chars/<나라>_<포즈>.png` — 정장 차림 볼(countryball) 캐릭터, 플랫 2D, 투명 누끼(rembg). 나라: 한국·미국·중국·북한·영국·소련·UN(+에피소드별 추가), 포즈 6종(기본·애원·어깨 으쓱·경례·가리키기·놀람). 한 번 만들어 모든 편에서 재사용 (Gemini 약 48장 ≈ 2,600원). 같은 캐릭터가 계속 나와 화면 톤이 통일됨
2. **새 화면 `stage` (종이 무대)** — 구겨진 흰 종이 배경 위 캐릭터 1~3명 배치, 말풍선·아이콘·물음표·느낌표가 `on` 단어 타이밍에 팝업, 살짝 흔들리는 등장 애니메이션
3. **새 화면 `flatmap` (플랫 지도)** — 바다 청록·땅 베이지·국가 단색 칠하기, 거리 곡선 + 라벨("직선 약 9,500km"), 국기 핀. 세계·지역 개요 설명용 (전투 장면은 기존 3D 전술 지도 유지 — 채널 강점)
4. **설명 카드 3종** — `flaggrid`(국기 줄 세우기 + 이름 부를 때 하나씩 강조·"?" 칸), `checklist`(노란 체크가 하나씩), `reasons`(이유 1·2·3 번호 카드 + 붉은 X로 지우기). 배경은 어두운 석판 질감 (`document` 카드도 같은 톤으로)
5. 사료 사진: 좌상단 작은 출처·연도 라벨 + `on`에 맞춰 뜨는 노랑/빨강 강조 라벨

## 1. 제작 순서

1. **대본** — `episodes/<ep>/script.md` (파일로). `## ACT n · 제목 [mm:ss–mm:ss]` 머리글로 막을 나눈다
   - **괄호 지문 금지** (`(pause)` 등), **쉼표 최소화** (ElevenLabs 호흡 끊김·팝 노이즈 방지)
   - 숫자는 낭독용 단어로 쓴다 (`November twenty-seventh`, `Hill twelve-eighty-two`). 자막은 생성기 `SUBS` 표가 숫자로 바꿔 보여 준다 (`November 27`, `Hill 1282`)
   - 문장은 `.`/`?`에서 나뉜다 — `Oliver P. Smith`처럼 약자 마침표는 쓰지 말 것 (문장이 쪼개짐)
   - 사실은 웹 검색으로 확인, 확정 못 한 것(발언 원문·좌표·수치)은 목록으로 남겨 전달 때 알린다
2. **스토리보드** — `episodes/<ep>/make_board.py`로 script.md 문장을 순서대로 장면에 배정해 `storyboard.json` 생성 (형식은 `episodes/ep08-chosin/`)
   - 보드 상단: `"lang": "en"`, `"voice": "pNInz6obpgDQGcFmaJgB"`(Adam), `"tempo": 1.02`, **`"tts_mode": "act"`**, `"midrolls"`, `target_sec`
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
6. **썸네일** — EP08 지시서 공식(영문): 좌측 3D 설산 작전 지도 + 우측 인물 흑백 누끼(`thumb_subject`) · 상단 인용 레드 `#FF3B30` · Line 1 흰색 100px · Line 2 옐로 `#FFE500` 112px · 우측 하단 재생시간 배지 여백 200px. 렌더 후 PNG를 직접 열어 확인, 1.9MB 넘으면 JPG
7. **전달** (한 번에) — Releases 링크, SRT, 썸네일, **영문** 제목 후보 3개·설명글(목차 타임스탬프는 SRT 실제 시각, 채널명·인사말 없이, 참고 자료·재연 일러스트 고지)·태그, 카테고리 Education, 확인 안 된 사실 목록. 설명은 한국어로

## 2. 고정 규격

| 항목 | 값 |
|---|---|
| 해상도 / 인코딩 | 1920×1080, 30fps, H.264 8Mbps, AAC 192k (20분 약 1.2GB) |
| 음량 | 렌더 후 `loudnorm` -15 LUFS |
| 나레이션 | ElevenLabs 'Adam' `pNInz6obpgDQGcFmaJgB`, 1.02배속, `tts_mode: act` |
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
- **GitHub Secrets 필요**: `ELEVENLABS_API_KEY`, `GEMINI_API_KEY` (선택: `CF_ACCOUNT_ID`, `CF_API_TOKEN`). 대화에 키를 적지 말 것
- Actions 실행 중에는 재료 파일(`public/ep`, `episodes`, `previews`)을 push 하지 말 것
- 이 세션 환경에서는 ElevenLabs·Gemini·위키미디어 직접 접속 불가 → 해당 작업은 Actions에서. `gh`는 REST(`gh api`)만
- 새 에피소드가 war-docu의 그림·사진을 재사용하려면, war-docu에서 파일(`public/ep/<src>/ai/*.jpg`)과 `ai.json` 서명·프롬프트를 이 저장소로 복사해 온다(재생성 비용 0). 사진은 `photo_pins.json`에 같은 `File:` 이름만 적으면 Actions가 다시 받는다
