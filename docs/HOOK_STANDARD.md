# Map of War 초반 후킹 표준 (첫 60초 · 영문 롱폼)

> 2026-11-18 `war-docu`에서 이식. 원본은 war-docu EP29 대전(`ep29-daejeon`)에 처음 적용된 후킹 구조와 `remotion/Hook.tsx` 부품이다.
> ⚠️ war-docu 코드·대본은 `docs/HOOK_STANDARD.md`를 참조하지만, 이식 시점(2026-11-18 커밋 `e8ef7627`)에 war-docu 저장소에는 이 문서도, 이식 지시서에 적힌 `docs/HOOK_ANALYSIS_JIDOSA.md`도 커밋돼 있지 않았다. 그래서 이 문서는 EP29 대본(`episodes/ep29-daejeon/script.md`)·`Hook.tsx`·이식 지시서 요약으로 다시 정리한 것이다. 원본 분석 문서가 war-docu에 올라오면 이 문서에 합칠 것.
> 적용: **`ep09` 이후 모든 영문 롱폼** (`ep08-chosin`은 제외). `docs/LONGFORM_STANDARD.md`와 함께 지킨다. 화면 문구·대사는 100% 영어.

## 1. 첫 60초 구조 — 모순 누적형 콜드 오프닝

| 구간 | 할 일 | 화면 부품 |
|---|---|---|
| 0~10초 **사건 직격** | 배경 설명·연도 나열 없이 가장 극적인 순간으로 바로 시작 (날짜·장소 한 줄 + 주인공의 행동) | 3D 전술 지도 비행 또는 재연 그림 · `LeftStatHud`로 핵심 수치 카운트업 |
| 10~40초 **모순 3단 누적** | 앵글 후보 3개(갈등형 → 숫자형 → 질문형)를 순서대로 쌓는다. 각 단은 "**A였다. 그런데도 B였다.**" 형태의 모순 한 쌍 | `LeftStatHud` 카드 순차 교체(병력·손실·일수) · `troops` 병력 대열 대비 |
| 40~50초 **`X` 마크 반전** | 시청자가 믿을 통념("누가 봐도 참패")을 한 줄로 말한 뒤 "정말 그랬을까?"로 뒤집는다 | `NegationOverlay` — 통념 키워드 위 붉은 X (`xOn`으로 말하는 순간) |
| 50~60초 **중앙 질문 카드** | 영상 전체가 답할 핵심 질문 1문장 + "이야기는 ~에서 시작한다"로 1막 연결 | `CoreQuestionCard` — 화면이 어두워지고 중앙 종이 카드 |

- 예시 (war-docu EP29 콜드 오프닝을 영어 틀로): *"July 20, 1950. Taejon."* → *"They destroyed ten enemy tanks. Yet the city fell in a single day."* → *"The general stayed to fight. Yet he vanished on the road out."* → *"By any measure it was a disaster. **Or was it?**"* → 질문 카드 *"How did a defeat that cost a general save South Korea?"*
- 숫자는 사료로 확인된 것만. 콜드 오프닝의 숫자·질문은 **본편 어느 막에서 회수하는지 script.md 머리에 `회수 표시`로 적는다** (EP29: 핵심 질문 → 7막, 전차 10대 → 5막, 36일 → 6막)
- 대본 머리에 앵글 후보 3개를 적고, 제목·썸네일 카피·질문 카드가 같은 앵글을 쓰게 한다

## 2. 화면 부품 사용법 (`remotion/Hook.tsx`)

장면에 `"hook"` 필드를 넣으면 `Video.tsx`가 `HookOverlays`(HUD·X·질문 카드)를 그 장면 위에 얹는다. 시각은 모두 `"at"`(초) 대신 `"on": "<대사 속 단어>"`로 지정 가능 (`timeline.py`가 `on→at`, `untilOn→until`, `xOn→xAt` 변환).

```jsonc
"hook": {
  "hud": [   // 좌측 상단 반투명 다크 카드 — 큰 볼드 수치(숫자면 0.9초 카운트업) + 2줄 설명, 순차 교체
    { "big": "3,933", "sub": "U.S. troops in Taejon", "sub2": "24th Infantry Division", "on": "three thousand" },
    { "big": "1,150", "sub": "killed, wounded or missing", "color": "#FF3B30", "on": "eleven hundred" }
  ],
  "neg": { "text": "A TOTAL DEFEAT", "on": "disaster", "xOn": "Or was it" },          // 통념 키워드 + 붉은 X
  "question": { "text": "How did a defeat that cost a general|save South Korea?", "on": "How did", "kicker": "■ THE QUESTION ■" }
}
```

- `question.kicker`를 비우면 영문 보드(`lang: "en"`)에서는 `■ THE QUESTION ■`가 자동으로 들어간다
- **병력 대비 `troops`** (`visual.type`): `{ "type": "troops", "n": 31, "cols": 8, "side": "us"|"nk"|"kr"|"cn", "vs": { "n": 90, "side": "nk", "cols": 15 }, "keep": 1, "keepAt": 4.2, "fadeLabel": "...", "title": "...", "march": true }` — 3D 아이소메트릭 미니어처 대열, `keep`/`keepAt`로 "31명 → 1명" 강조
- 1차 사료 하이라이트: `document` 카드(요점 2~4줄 + 도장/붉은 X), 사진 `tag`(좌상단 출처·연도) + `marks`(`on`에 맞춰 뜨는 노랑/빨강 강조 라벨) — `Stage.tsx`·`Visuals.tsx`
- 모든 부품은 frame 기반 결정론 (`Date.now`·`setTimeout`·`Math.random` 금지)

## 3. 4~6초 시각 레이어 교차

- 첫 60초는 **4~6초마다** 화면 레이어가 바뀌어야 한다: 3D 지도 비행 → HUD 수치 → 병력 대열 → 사료 사진 강조 → X 반전 → 질문 카드 순으로 서로 다른 종류를 교차 (같은 종류 연속 2회 금지)
- 본편도 3~5초마다 장면 전환 또는 `on` 팝업(숫자·라벨·말풍선) 하나 — `CLAUDE.md` '연출 스타일 v2'
- 미리보기(`previews/<ep>/sheet_*.jpg`) 확인 때 첫 1분을 따로 점검: 위 4구간 · 4~6초 교차 · X/질문 카드 타이밍

## 4. 썸네일 v2와 한 묶음

콜드 오프닝의 앵글이 썸네일 카피가 된다 — `CLAUDE.md` '썸네일 표준 v2' 참고 (고정 인물 사진 폐기 · 에피소드 고유 전술 비주얼 Full-Bleed · 하단 다크 비네팅 · 대형 2줄 카피).
