---
tags:
  - project
  - writing-coach
  - prd
  - claude-cowork
  - english-learning
created: '2026-03-18'
version: '0.5'
aliases:
  - Writing Coach PRD
pipeline: pipeline-full
phase: 3-PRD
---
# Writing Coach PRD

> **프로젝트명**: Writing Coach — 영어 에세이 글쓰기 코치 에이전트
>
> **목적**: 주제별 어휘 학습 → 에세이 작성 → 3라운드 점진적 교정 → 오류 추적의 완전 자동화 파이프라인으로 영어 글쓰기 실력을 체계적으로 향상시킨다
>
> **아키텍처**: Claude Cowork 스킬 (obsidian-to-anki 스킬 연동)
>
> **파이프라인**: pipeline-full (중형)
>
> **최종 수정**: 2026-03-18 | 버전: 0.3 (1차 검토 반영)\n\n---

## 1. 문제 정의 & 근거

### 해결하려는 문제

한국어 화자가 영어 에세이 실력을 향상시키려 할 때 3가지 핵심 문제가 존재한다:

- **단절된 학습 루프**: 어휘 학습(Anki), 글쓰기 연습, 교정 피드백이 별도 도구에서 이루어져 연결이 끊김. 배운 어휘를 글쓰기에 활용하는 전이(transfer)가 일어나지 않음
- **일방적 교정**: 기존 도구(Grammarly, LanguageTool)는 교정본만 제공하고 끝남. 학습자가 직접 수정하는 과정이 없어 동일 실수를 반복. 연구에 따르면 \"힌트를 받고 직접 고치는 것\"이 교정본을 읽기만 하는 것보다 2-3배 효과적
- **개인화 부재**: 한국어 L1 간섭 패턴(관사 누락, 시제 혼용, 전치사 직역)을 특별히 추적하는 도구가 없음. 매번 같은 유형의 실수를 처음 보는 것처럼 교정받음
- **입력(모방) 학습 부재**: 좋은 글을 읽고 그 표현을 흡수하는 과정이 글쓰기 연습과 분리되어 있음. "역번역" 방법(원문 → 한국어 번역 → 학습자가 영작 → 원문과 비교)이 교육학적으로 검증되었지만, 이를 체계적으로 지원하는 도구가 없음

### 교육학적 근거

- 인지 부하 이론(Sweller, 1988): 모든 피드백을 동시에 제공하면 학습 효과 저하 — 점진적 교정이 최적
- 간격 반복 + 글쓰기 통합(Nation, 2001): 실제 오류에서 추출한 SRS 카드가 일반 단어장보다 높은 retention rate
- L1 간섭 체계(Swan & Smith, 2001): 한국어 화자의 예측 가능한 오류 패턴을 우선 교정하면 학습 효율 극대화
- CEFR 기반 평가: 레벨별 비교를 통해 학습자가 현재 위치와 목표를 시각적으로 파악
- 역번역(Back-translation) 학습법(Beiler, 2020): 번역 → 영작 → 원문 비교의 과정에서 "이해"와 "생산" 사이의 갭이 드러나고, 원문과 비교할 때 "왜 원문이 더 좋은지" 분석하는 "reasoned noticing"이 표면적 교정보다 효과적
- Guided noticing 연구(2025): 자유 비교보다 구문/어휘/연결어 카테고리별 가이디드 비교가 학습 효과 훨씬 높음

---

## 2. 목표 & 성공 지표

### 핵심 목표

- 어휘 학습 → 글쓰기 → 교정 → SRS 카드의 완전 자동화 파이프라인 제공
- 3라운드 점진적 교정으로 학습자가 직접 수정하며 배우는 사이클 구축
- 세션 간 오류 추적으로 개인화된 피드백 누적

### 측정 가능한 성공 지표

| 지표 | 목표 | 측정 방법 |
|------|------|----------|
| 어휘 활용률 | 제공 어휘의 25%+ 에세이에 사용 | count(사용된 제공 어휘) / count(전체 제공 어휘). 동일 어휘 복수 사용은 1회로 계산 |
| L1 간섭 검출율 | 한국어 특유 오류 80%+ 검출 | eval 단계에서 원어민/고급자가 에세이를 독립 교정한 결과와 비교 |
| 오류 감소 추세 | 5세션 후 반복 오류 유형당 30%+ 감소 | error-profile의 last_5 배열 첫 값 대비 마지막 값 비교 |
| 레벨별 리라이트 차별성 | 4레벨 간 어휘 수준, 문장 복잡도, 연결어 사용이 단계적으로 상승 | eval 시 레벨별 평균 문장 길이, 고급 어휘 비율, 종속절 비율로 정량 비교 |
| 오류 프로필 참조율 | 다음 세션 시작 시 이전 오류 데이터가 100% 반영 | Phase A에서 focus_areas 기반 가이드가 출력되는지 확인 |

---

## 3. 범위 & 트레이드오프

### 범위 안 (v1)

**두 가지 모드** (세션 시작 시 선택):

- **Mode A — 자유 글쓰기**: 주제별 어휘 생성 → 에세이 직접 작성 → 3라운드 점진적 교정. 본인의 생각을 영어로 표현하는 "출력 능력" 훈련
- **Mode B — 역번역 연습**: 수준 맞는 모범문 제공(원문+한국어 번역) → 한국어 번역만 보고 영작 → 원문과 가이디드 비교 → 차이점 분석 교정. 좋은 표현을 흡수하는 "입력+모방 능력" 훈련

**공통 기능**:
- 한국어 L1 간섭 특화 교정 (6개 유형)
- Obsidian 기반 오류 프로필 누적 추적 (두 모드 공유)
- 오류 기반 Anki 카드 자동 생성
- 4레벨 비교 리라이트 (Mode A의 Round 3에서)

### 범위 밖 (v2 이후)

- 음성 입력/출력
- 실시간 타이핑 중 교정 (완성 후 제출 방식만)
- IELTS/TOEFL 밴드 스코어 자동 채점
- 다른 글쓰기 장르 (이메일, 보고서, 창작)
- 여러 사용자 프로필 관리
- 문법 규칙 체계적 커리큘럼

### 핵심 가정

- 사용자는 Upper-intermediate(B2-C1) 수준의 한국어 L1 화자
- Anki 데스크탑 + AnkiConnect 플러그인이 설치되어 있음
- Obsidian MCP가 연결되어 있음
- 사용자는 주 2-3회 에세이 연습 세션을 수행

### 기술적 제약

- 에세이 길이: 200-500 단어. Cowork 세션의 컨텍스트(200K 토큰)에서 3라운드 풀 피드백 + 4레벨 리라이트가 충분히 수용 가능하므로, 품질을 위해 이전 라운드 피드백도 전체 유지
- 품질 우선 원칙: 토큰 효율보다 피드백 품질을 우선한다. 이전 라운드의 피드백을 요약하지 않고 전체를 컨텍스트에 유지하여 후속 라운드의 교정 품질을 극대화
- error-profile.md 프론트매터는 YAML 호환 구조 유지 (중첩 2단계까지)
- obsidian-to-anki 스킬이 사용하는 CTP-English 노트 타입의 필드를 그대로 활용

---

## 4. 맥락 & 기술 스택

### 기존 인프라 연동

| 구성요소 | 선택 | 역할 | 의존성 |
|---------|------|------|--------|
| AI 엔진 | Claude (Cowork 내장) | 어휘 생성, 교정, 레벨별 리라이트 | 없음 (기본 내장) |
| 어휘 카드 | AnkiConnect API 직접 호출 | CTP-English, CTP-Cloze, CTP-Knowledge 카드 생성. obsidian-to-anki 스킬의 카드 CSS/필드 설계를 공유하되, API 호출은 Writing Coach가 직접 수행 | AnkiConnect (localhost:8765), Anki 데스크탑 실행 |
| 오류 추적 | Obsidian MCP (mcp__obsidian) | 프론트매터 기반 오류 프로필 읽기/쓰기 | Obsidian MCP 연결 |
| 웹 검색 | Claude 내장 | 주제별 어휘 리서치 | 없음 (기본 내장) |

### 사전 조건 확인 순서

1. Obsidian MCP 연결 확인 (mcp__obsidian__read_note 호출 가능 여부)
2. AnkiConnect 실행 확인 (localhost:8765 응답 여부) — 실패 시 카드 생성 건너뛰고 교정 흐름 진행
3. writing-coach/ 폴더 존재 확인 — 없으면 자동 생성

---

## 5. 기능 요구사항

### L1 간섭 오류 분류 체계

REQ-4, REQ-7, REQ-8에서 공통으로 사용하는 6가지 L1 간섭 오류 유형:

| ID | 유형 | 프로필 키 | 설명 | 예시 |
|----|------|----------|------|------|
| L1-1 | 관사 누락/오용 | articles | a/the 누락 또는 잘못된 사용 | \"I like music\" → \"I like the music\" (특정 맥락) |
| L1-2 | 주어-동사 수 일치 | subject_verb | 단수/복수 주어와 동사 불일치 | \"He go\" → \"He goes\" |
| L1-3 | 단복수형 혼동 | plural | 셀 수 있는 명사의 복수형 누락 | \"many student\" → \"many students\" |
| L1-4 | 시제 일관성 | tense | 문단 내 시제 혼용 | 과거 서술 중 갑자기 현재형 |
| L1-5 | 전치사 오용 | preposition | 한국어 조사를 영어 전치사로 직역 | \"go to home\" → \"go home\" |
| L1-6 | 직역 표현 | literal_translation | 한국어 문장 구조/표현의 직역 | \"I'm very interest\" → \"I'm very interested\" |

### 어휘 카테고리 정의

| 카테고리 | CEFR 기준 | 개수 | 설명 |
|---------|----------|------|------|
| 주제별 핵심 어휘 | B1-B2 | 8-10개 | 해당 주제를 논의하는 데 필수적인 어휘. 대부분의 에세이에 자연스럽게 쓸 수 있는 수준 |
| 에세이 연결어/표현 | B2 | 5-7개 | 담화 표지, 의견 표현, 전환 표현. 에세이 구조를 만드는 기능어 |
| 고급 어휘 | C1 | 3-5개 | Oxford 5000 기준 C1 레벨 이상. 사용하면 글의 수준이 올라가는 어휘 |

### REQ-1: 주제 선정 & 어휘 생성

**입력**: 사용자 지정 주제 또는 \"추천해줘\" 요청

**처리**:
- 주제 추천 시: 시사/사회 이슈와 개인 관심사를 번갈아 추천. 난이도 표시 (B2 적정 / C1 도전)
- 주제 확정 후 3가지 카테고리 어휘 생성 (위 어휘 카테고리 정의 참조)
- 각 어휘에 예문, 콜로케이션, 한국어 의미, IPA 발음 포함
- 에세이 구조 가이드 제공 (서론-본론-결론 + 주제에 맞는 논증 전략)

**출력**: 어휘 리스트 + 에세이 가이드라인

**수락 기준**:
- Given 주제가 선정되었을 때
- When 어휘 생성이 완료되면
- Then 최소 16개 어휘가 3카테고리로 분류되어 있고, 각 어휘에 예문과 콜로케이션이 포함되며, 고급 어휘는 Oxford 5000 C1+ 수준임

### REQ-2: Anki 플래시카드 자동 생성

**입력**: REQ-1에서 생성된 어휘 리스트

**처리**:
- AnkiConnect API(localhost:8765)를 직접 호출하여 CTP-English 카드 생성
  - obsidian-to-anki 스킬을 호출하는 것이 아니라, 동일한 노트 타입과 CSS를 공유하면서 API를 직접 사용
  - obsidian-to-anki의 references/card-css.md와 references/anki-helper.md를 레퍼런스로 참조
- 덱 이름 규칙: Obsidian::English::Writing-Coach::{주제명}
- 필드 매핑: Word, Phonetic, POS, POS_Class, Meaning_KR, Meaning_EN, Example_EN, Example_KR, Synonyms, Frequency, Deck_Tag, Tags
- 중복 검사: addNote의 allowDuplicate: false 옵션 사용

**출력**: Anki에 추가된 플래시카드

**폴백**: AnkiConnect 미연결 시 어휘 리스트를 Obsidian 노트로 저장 (writing-coach/vocab/YYMMDD-{주제}.md)하고, 나중에 일괄 카드 생성 가능

**수락 기준**:
- Given 16개 이상의 어휘 리스트가 있을 때
- When obsidian-to-anki 스킬이 실행되면
- Then 모든 어휘가 CTP-English 카드로 생성되고, 중복 카드는 skip 처리되며, 생성된 카드 수가 보고됨

### REQ-3: 에세이 작성 안내 & 대기

**입력**: 사용자의 글쓰기 준비 신호

**처리**:
- 제공 어휘 중 최소 5개 이상 활용하도록 안내
- 목표 단어 수 제안: 기본 200-500 단어 (자유롭게 조절)
- 50 단어 미만 제출 시: "좀 더 써볼까요? 100 단어 이상이면 효과적인 피드백이 가능합니다" 안내
- 선택적 시간 제한 모드: 사용자에게 \"시간 제한 모드를 켤까요? (25분)\" 확인
- 사용자가 에세이 완성하여 제출할 때까지 대기

**출력**: 작성 가이드라인 메시지

**수락 기준**:
- Given 어휘가 제공된 상태에서
- When 사용자에게 작성 안내를 하면
- Then 메시지에 (1) 목표 단어 수, (2) 활용 어휘 수 최소치, (3) 에세이 구조 리마인더, (4) 시간 제한 옵션이 포함되어 있음

### REQ-4: Round 1 교정 — Grammar & Mechanics

**입력**: 사용자가 작성한 에세이 원문

**처리**:
- L1 간섭 오류 분류 체계(L1-1 ~ L1-6)에 따라 우선 검출
- 일반 문법 오류: 철자, 구두점, 문장 구조
- 각 오류에 대해 4요소 포함: 원문/교정/유형/설명
- L1 간섭 오류는 한국어 간섭 태그 표시
- 오류 10개 이상 시 중요도 순으로 상위 10개 표시 후 나머지는 요약

**출력 구조** (오류가 여러 개일 때):

```
--- Round 1 교정: Grammar & Mechanics ---
오류 총 {N}개 발견 (L1 간섭 {M}개 / 일반 문법 {K}개)

[1/N]
[원문] "I think environment is very important issue."
[교정] "I think **the** environment is **a** very important issue."
[유형] L1 간섭 — 관사 누락
[설명] 한국어에는 관사가 없어서 빠뜨리기 쉽습니다...

[2/N]
...

---
Round 1 요약: 관사 오류 3회, 시제 오류 2회, 전치사 1회
위 교정을 참고하여 에세이를 수정한 뒤 다시 보내주세요.
```

**수락 기준**:
- Given 사용자의 에세이(200-500 단어)가 제출되었을 때
- When Round 1 교정이 완료되면
- Then (1) 총 오류 수 + L1/일반 분류가 상단에 표시되고, (2) 각 오류에 원문/교정/유형/설명 4요소가 포함되며, (3) 하단에 오류 유형별 빈도 요약이 있고, (4) 사용자에게 수정 후 재제출을 안내함

### REQ-5: Round 2 교정 — Clarity & Coherence

**입력**: Round 1 피드백 반영하여 수정된 에세이

**처리**:
- 문장 수준: 모호한 표현, 불필요한 반복, 어색한 구조
- 단락 수준: 주제문(topic sentence) 존재 여부, 뒷받침 문장의 관련성
- 글 전체 수준: 서론-본론-결론 구조, 논리 흐름, 전환(transition)
- 각 피드백에: 구체적 위치, 이유, 개선 방향(답이 아닌 힌트), 활용 가능한 표현
- Round 1에서 아직 남아있는 문법 오류는 간략히 언급만 (Round 2 초점은 구조)

**출력 구조**:

```
--- Round 2 교정: Clarity & Coherence ---

[글 전체] 구조 평가
- 서론: 주제 제시 있음 / 입장 표명 불명확
- 본론 1: ...
- 본론 2: ...
- 결론: ...

[단락 2] 주제문이 불명확합니다.
[현재] "There are many things about technology."
[문제] 너무 일반적 — 이 단락의 주장을 특정할 수 없음
[방향] 기술의 어떤 측면을 논의하는지 명시해보세요.
[활용 표현] "however", "on the other hand", "this suggests that"
```

**수락 기준**:
- Given Round 1 수정본이 제출되었을 때
- When Round 2 교정이 완료되면
- Then (1) 글 전체 구조 평가가 먼저 나오고, (2) 문장/단락별 피드백에 방향 제안이 포함되며, (3) 문법 피드백은 최소화됨

### REQ-6: Round 3 교정 — Style & Sophistication + 레벨별 비교

**입력**: Round 2 피드백 반영하여 수정된 에세이

**처리**:
- 어휘 다양성: 반복 단어 지적 + 대체어 제안
- 레지스터 적절성: 에세이 격식 수준 확인
- 세련된 표현: 단순 표현 → 고급 표현 업그레이드 제안
- 수사적 기법: 강조, 대비, 예시 등 제안
- 4레벨 비교 리라이트 (에세이의 핵심 단락 1개를 대상으로):
  - 초급 (A2-B1): 단문 위주, 기본 어휘, 최소한의 연결어
  - 중급 (B1-B2): 복문 등장, 주제 어휘 사용, 기본 연결어
  - 중상급 (B2-C1): 다양한 문장 구조, 콜로케이션, 논리적 전환
  - 상급 (C1-C2): 수사적 기법, 뉘앙스 표현, 원어민 수준 자연스러움

**4레벨 비교 예시** (본론 1단락 대상):

```
[초급 A2-B1]
Technology is good. It helps people. We can talk to friends easily.
→ 특징: 단문, 기본 어휘(good, help), 연결어 없음

[중급 B1-B2]
Technology has many advantages. For example, it allows people
to communicate with friends more easily than before.
→ 특징: 복문 등장, "for example" 연결어, "communicate" 대체어

[중상급 B2-C1]
Technological advancements have significantly transformed
interpersonal communication, enabling instantaneous global
connectivity that was inconceivable a generation ago.
→ 특징: 명사구 복잡도 증가, 콜로케이션("significantly transformed"),
  분사구문("enabling")

[상급 C1-C2]
The relentless march of technological innovation has fundamentally
reshaped the very fabric of human communication, collapsing
geographical barriers and forging connections that transcend
traditional boundaries of time and space.
→ 특징: 은유("fabric of communication"), 병렬구조("collapsing...
  forging"), 추상적 어휘("transcend")
```

**수락 기준**:
- Given Round 2 수정본이 제출되었을 때
- When Round 3 교정이 완료되면
- Then (1) 스타일 피드백에 구체적 대체어 제안 포함, (2) 4레벨 리라이트가 동일 내용에 대해 작성되고, (3) 각 레벨의 특징이 어휘 수준/문장 복잡도/연결어 관점에서 설명됨

### REQ-7: 오류 프로필 관리

**입력**: 각 라운드에서 검출된 오류 데이터

**초기화 로직** (첫 세션 또는 파일 없을 때):
- writing-coach/error-profile.md 파일 존재 여부 확인
- 없으면 빈 프로필 생성 (all counts = 0, last_5 = [], total_sessions = 0)
- 있으면 기존 프론트매터 로드

**업데이트 로직**:
- 이번 세션의 오류를 유형별로 집계
- 각 유형의 count에 이번 세션 오류 수 누적
- last_5 배열에 이번 세션 오류 수 push (5개 초과 시 가장 오래된 것 제거)
  - last_5의 의미: 최근 5개 세션에서 해당 유형이 각각 몇 회 발생했는지
- trend 계산: last_5의 앞 2개 평균 vs 뒤 2개 평균 비교
  - 뒤가 30%+ 감소 → \"decreasing\"
  - 뒤가 30%+ 증가 → \"increasing\"
  - 그 외 → \"stable\"
- focus_areas: 가장 빈도 높은 상위 3개 오류 유형 자동 선정
- total_sessions += 1

**다음 세션 가이드 생성**:
- focus_areas의 오류 유형별로 최근 빈도 + 추세를 자연어로 안내
- 개선된 유형은 긍정 피드백으로 동기 부여

**세션 기록**: writing-coach/sessions/YYMMDD-{주제 영문 kebab-case}.md

**수락 기준**:
- Given 교정 세션이 완료되었을 때
- When 오류 프로필이 업데이트되면
- Then (1) error-profile.md의 count/last_5/trend/focus_areas가 갱신되고, (2) 세션 노트가 sessions/ 폴더에 저장되며, (3) 다음 세션 시작 시 focus_areas 기반 가이드가 출력됨

### REQ-8: 오류 기반 Anki 카드 생성

**입력**: 교정 과정에서 발견된 오류

**트리거 조건**: 동일 오류 유형이 이번 세션에서 2회 이상 발생하거나, error-profile의 last_5에서 3세션 연속 등장한 유형

**처리**:
- CTP-Cloze 카드: 교정된 문장을 Cloze 변환 (오류 포인트를 빈칸으로)
- CTP-Knowledge 카드: 해당 오류 유형의 문법 규칙 Q&A
- 덱: Obsidian::English::Writing-Coach::Error-Cards
- 중복 검사: findNotes로 동일 Word/Sentence 확인 후 skip

**폴백**: AnkiConnect 미연결 시 Obsidian 노트로 저장 (writing-coach/error-cards/YYMMDD.md)

**수락 기준**:
- Given 트리거 조건을 만족하는 오류가 있을 때
- When 사용자가 \"오류 카드도 만들까요?\"에 동의하면
- Then 오류 패턴당 1-2장의 Cloze/Knowledge 카드가 생성되고, 중복 검사 통과

---

## 5B. 역번역 모드 (Mode B) 요구사항

### REQ-9: 모드 선택

**입력**: 세션 시작 시 사용자의 모드 선택

**처리**:
- Phase A(오류 프로필 로드) 완료 후, 모드 선택지 제공:
  - "자유 글쓰기" — 본인 생각을 직접 영작 (Mode A, 기존 Phase B-H)
  - "역번역 연습" — 모범문 기반 번역 연습 (Mode B, Phase B2-H2)
- 사용자가 선택하면 해당 모드의 Phase로 분기

**수락 기준**:
- Given 세션이 시작되었을 때
- When 오류 프로필 로드 후 모드 선택지가 제시되면
- Then 두 모드의 차이점이 한 줄씩 설명되고, 사용자가 선택 후 해당 흐름으로 진입함

### REQ-10: 모범문 선정 & 제공

**입력**: 사용자 지정 주제 또는 "추천해줘" 요청

**처리**:
1. 주제 확정 (Mode A와 동일한 주제 추천 로직 사용)
2. 모범문 확보 (우선순위):
   - **1순위: 웹 검색**으로 해당 주제의 B2-C1 수준 영어 에세이/기사 단락 검색. British Council, Linguapress, Cambridge Write & Improve 등 신뢰 출처 우선
   - **2순위: AI 생성** — 적절한 실제 텍스트를 찾지 못하면, B2-C1 수준에 맞게 모범문을 직접 작성
3. 모범문 기준:
   - 길이: 100-200 단어 (1-2 단락)
   - 수준: B2-C1 — 정량 기준:
     - Oxford 5000 C1+ 어휘: 100단어당 최대 2개 (3개 이상이면 너무 어려움)
     - 관용구/숙어: 150단어당 최대 1개 (역번역에 부적합하므로 최소화)
     - 종속절: 텍스트 전체에 최소 3개 이상
     - 평균 문장 길이: 15-20 단어
   - 장르: 의견/논증형 에세이 단락
   - AI 생성 시 품질 검증: 생성 후 "자연스럽게 읽히는가?" 자체 검토. 어색하면 재생성. 그래도 부적절하면 model_text_quality: "low" 태그하고 사용자에게 "AI 생성 텍스트입니다. 실제 원어민 글과 비교해보는 것도 좋습니다" 안내
4. 제공 형식:
   - **한국어 번역본만** 먼저 제공 (원문은 이 시점에서 보여주지 않음)
   - 번역은 자연스러운 한국어 (직역 아닌 의역)
   - "이 한국어 내용을 영어로 써보세요"라고 안내

**출력**: 한국어 번역본 + 작성 안내

**수락 기준**:
- Given 주제가 선정되었을 때
- When 모범문이 확보되면
- Then (1) 100-200 단어 분량의 B2-C1 수준 원문이 확보되고, (2) 자연스러운 한국어 번역이 제공되며, (3) 원문은 아직 사용자에게 보여주지 않음

### REQ-11: 역번역 작성 & 원문 비교

**입력**: 사용자가 한국어 번역을 보고 작성한 영문

**처리**:
1. 사용자의 영문 제출 받기
2. 원문 공개: "여기가 원문입니다" 하고 원문을 보여줌
3. **가이디드 비교 테이블** 제공 — 3가지 카테고리로 체계적 비교:

```
--- 원문 비교 분석 ---

### 1. 구문 (Syntax)
| 내 표현 | 원문 표현 | 차이점 | 원문이 더 나은 이유 |
|---------|----------|--------|-------------------|
| "I think technology is good for communication" | "Technology has fundamentally reshaped interpersonal communication" | 주어 전환 + 명사화 | 주관적 "I think" 제거, 동사 "reshaped"가 더 구체적 |

### 2. 어휘 (Vocabulary)
| 내 단어 선택 | 원문 단어 선택 | 뉘앙스 차이 |
|------------|-------------|-----------|
| good | fundamentally | 정도 부사로 강조 |
| talk | interpersonal communication | 명사화로 격식 수준 상승 |

### 3. 연결 & 흐름 (Cohesion)
| 내 연결 방식 | 원문 연결 방식 | 효과 |
|------------|-------------|------|
| "And also..." | 분사구문 "enabling..." | 접속사 없이 자연스럽게 연결 |
```

4. 각 주요 차이점에 대해 **왜 원문이 더 효과적인지** 설명 (reasoned noticing)
5. L1 간섭으로 인한 차이는 L1 태그 표시. 이 오류들이 error-profile 업데이트 대상
6. 비교 테이블 분량 가이드: 구문 1-2개, 어휘 2-3개, 연결 1개를 우선 선정하여 핵심에 집중
7. 유사도 높은 경우 처리: 사용자 글이 원문과 80%+ 겹치면, "원문과 매우 가깝습니다! 같은 내용을 다른 방식으로 표현해보는 것도 좋은 연습입니다" 안내 + 대안 표현 2-3개 제시

**출력**: 원문 + 가이디드 비교 테이블 + 차이점 분석

**수락 기준**:
- Given 사용자의 역번역이 제출되었을 때
- When 원문과 비교 분석이 완료되면
- Then (1) 구문/어휘/연결 3카테고리 비교 테이블이 제공되고, (2) 각 차이점에 "왜 원문이 더 나은지" 설명이 포함되며, (3) L1 간섭 패턴은 별도 태그

### REQ-12: 역번역 후 수정 & 세션 마무리

**입력**: 비교 분석을 본 사용자

**처리**:
1. "비교를 참고하여 글을 수정해보세요" 안내
2. 사용자가 수정본 제출
3. 수정본과 원문의 재비교 — 개선된 부분 강조
4. 이번 세션의 핵심 배움 정리:
   - "이번에 배운 표현 TOP 3" (원문에서 가져온 표현)
   - "L1 간섭으로 놓친 포인트" (있을 경우)
5. 오류 프로필 업데이트 (REQ-7과 동일한 로직)
6. 세션 노트 저장 (mode: "back-translation" 표시)
7. 배운 표현 Anki 카드 생성 제안:
   - 원문의 좋은 표현을 CTP-Cloze 카드로 변환
   - 예: "Technology has {{c1::fundamentally reshaped}} interpersonal communication."

**수락 기준**:
- Given 비교 분석 후 사용자가 수정본을 제출했을 때
- When 세션이 마무리되면
- Then (1) 수정본의 개선점이 강조되고, (2) "배운 표현 TOP 3"이 정리되며, (3) 오류 프로필이 업데이트되고, (4) Anki 카드 생성이 제안됨

### REQ-13: 배운 표현 Anki 카드 생성 (Mode B 전용)

**입력**: Phase H2에서 정리된 "배운 표현 TOP 3"

**트리거**: 사용자가 "카드로 만들까요?"에 동의

**처리**:
- "배운 표현 TOP 3"에서 카드 생성 (사용자가 원하면 추가 가능)
- 카드 타입: CTP-Cloze
  - Sentence: 원문에서 해당 표현이 포함된 전체 문장, 표현 부분을 Cloze 처리
  - 예: "Technology has {{c1::fundamentally reshaped}} interpersonal communication."
  - Translation: 한국어 번역
- 덱: Obsidian::English::Writing-Coach::Learned-Expressions
- 중복 검사: findNotes로 동일 Sentence 확인 후 skip
- error-profile 연동: 배운 표현이 L1 오류 교정과 관련된 경우 (예: 전치사 패턴 교정) 태그에 error-correction-L1-{n} 추가

**수락 기준**:
- Given "배운 표현 TOP 3"이 정리되어 있을 때
- When 사용자가 카드 생성에 동의하면
- Then 표현당 1장의 CTP-Cloze 카드가 생성되고, 중복은 skip, L1 관련 태그 포함

---

## 6. 에이전트 행동 경계

### Always (항상 수행)

- 세션 시작 시 error-profile.md 로드 시도 (없으면 빈 프로필로 초기화)
- L1 간섭 오류에 한국어 간섭 태그 + 유형 ID(L1-1~L1-6) 표시
- 교정 시 원문/교정/유형/설명 4요소 포함
- 사용자가 수정본을 제출할 때까지 다음 라운드 진행하지 않음
- 세션 종료 시 error-profile.md 업데이트 및 세션 노트 저장
- 격려적이고 건설적인 톤 유지 (\"이건 틀렸습니다\" 대신 \"이렇게 하면 더 자연스럽습니다\")

### Ask (사용자에게 확인)

- 주제 추천 시: \"이 주제로 할까요?\"
- 어휘 리스트 완성 후: \"이 어휘들로 진행할까요? 추가/변경할 단어 있나요?\"
- Phase D 시작 시: \"시간 제한 모드를 켤까요? (25분)\"
- Round 3 완료 후: \"오류 기반 Anki 카드도 만들까요?\"
- 사용자가 중간에 그만두고 싶을 때: 현재까지의 오류만 프로필에 저장할지 확인
- 사용자가 Round 2/3 건너뛰기 요청 시: "Round 2를 건너뛸까요? 구조 피드백 없이 스타일로 넘어갑니다."
- Mode B에서 모범문 확인: "이 모범문으로 연습할까요? 다른 걸 찾아볼까요?"
- Mode B 세션 마무리 시: "배운 표현을 Anki 카드로 만들까요?"

### Never (절대 금지)

- 사용자 대신 에세이를 써주는 것
- 사용자가 수정하기 전에 다음 라운드로 넘어가는 것
- Round 1에서 스타일/구조 피드백을 섞는 것 (라운드 순서 엄수)
- 교정 없이 \"잘 썼습니다\"만 하는 것 (항상 최소 1개 개선점 제시)
- 오류 프로필을 사용자 확인 없이 삭제하는 것
- 확신이 없는 교정을 단정적으로 표현하는 것
- Mode B에서 원문을 사용자가 영작하기 전에 보여주는 것 (반드시 한국어 번역만 먼저)
- Mode B에서 관용구/숙어가 과도한 텍스트를 모범문으로 선택하는 것 (역번역에 부적합)

---

## 7. 워크플로우 상세 흐름

### 아키텍처 참고

이 스킬은 Cowork의 대화형 세션 안에서 작동한다. 스킬이 로드되면 Phase A-H가 하나의 대화 세션 내에서 자연스럽게 이어진다. 사용자가 메시지를 보내고, 스킬이 응답하고, 사용자가 수정본을 보내고... 이 과정이 한 세션 안에서 반복된다. 별도의 상태 관리 메커니즘이 필요하지 않으며, 대화 컨텍스트가 자연스럽게 상태를 유지한다.

200K 토큰 컨텍스트에서 500단어 에세이 + 3라운드 풀 피드백은 전체 합쳐도 15K 토큰 미만이므로, 이전 라운드의 피드백을 요약하지 않고 전체 유지한다. 이를 통해 후속 라운드에서 이전 교정 사항을 참조하여 더 정확하고 일관된 피드백을 제공한다. 오류 프로필과 세션 기록은 Obsidian에 저장하여 세션 간 영속성을 보장한다.

### 모드 분기

```
[시작] 사용자: "글쓰기 연습하자" / "writing practice"
  |
  v
[Phase A] 사전 조건 확인 + 오류 프로필 로드
  |
  v
[모드 선택] "어떤 연습을 할까요?"
  ├── "자유 글쓰기" → Mode A (Phase B → C → D → E → F → G → H)
  └── "역번역 연습" → Mode B (Phase B2 → C2 → D2 → E2 → H2)
```

### Mode A: 자유 글쓰기 세션 흐름

```
[시작] 사용자: "자유 글쓰기" 선택
  |
  v
[Phase A] 사전 조건 확인 + 오류 프로필 로드
  → Obsidian MCP 연결 확인
  → AnkiConnect 연결 확인 (실패 시 카드 생성 건너뛰기 플래그 설정)
  → error-profile.md 읽기 (없으면 빈 프로필 초기화)
  → focus_areas 기반 가이드: "지난번 관사 오류 5회. 오늘 포커스: 관사"
  |
  v
[Phase B] 주제 선정
  → 사용자 지정 또는 AI 추천 (시사+개인 관심사 번갈아)
  → 사용자 확인: "이 주제로 할까요?"
  |
  v
[Phase C] 어휘 제공 + Anki 카드 생성
  → 3카테고리 어휘 생성 (주제 8-10 + 연결어 5-7 + 고급 3-5)
  → 사용자 확인: "어휘 리스트 괜찮나요?"
  → AnkiConnect 가능 시: obsidian-to-anki 스킬로 카드 생성
  → 불가 시: Obsidian 노트로 저장
  |
  v
[Phase D] 에세이 작성 (사용자)
  → 안내: 목표 200-500 단어, 어휘 5개+ 활용
  → 시간 제한 모드 확인 (선택)
  → 사용자가 완성 후 제출
  |
  v
[Phase E] Round 1: Grammar & Mechanics
  → L1 간섭 우선 + 일반 문법 (오류 분류 체계 L1-1~L1-6 적용)
  → 출력: 오류 총수 + 개별 교정 + 유형별 요약
  → 사용자 수정 후 재제출
  |
  v
[Phase F] Round 2: Clarity & Coherence
  → 글 전체 구조 평가 + 단락/문장별 피드백
  → 이전 Round 1 피드백 전체 유지 (품질 우선)
  → 사용자 수정 후 재제출
  |
  v
[Phase G] Round 3: Style & Sophistication
  → 스타일 피드백 + 4레벨 비교 리라이트 (핵심 단락 1개)
  → 이전 Round 1-2 피드백 전체 유지 (품질 우선)
  |
  v
[Phase H] 세션 마무리
  → error-profile.md 업데이트 (업데이트 로직 적용)
  → 세션 기록 저장 (sessions/YYMMDD-주제.md)
  → 사용자 확인: "오류 기반 Anki 카드도 만들까요?"
  → 다음 세션 추천 포커스 제안
```

### Mode B: 역번역 연습 세션 흐름

```
[시작] 사용자: "역번역 연습" 선택
  |
  v
[Phase B2] 주제 선정 (Mode A와 동일한 추천 로직)
  → 사용자 확인: "이 주제로 할까요?"
  |
  v
[Phase C2] 모범문 확보 + 한국어 번역 제공
  → 웹 검색 우선, 없으면 AI 생성 (100-200 단어, B2-C1)
  → 한국어 번역만 먼저 제공 (원문은 숨김)
  → "이 내용을 영어로 써보세요"
  |
  v
[Phase D2] 역번역 작성 (사용자)
  → 한국어 번역만 보고 영어로 작성
  → 사용자가 완성 후 제출
  |
  v
[Phase E2] 원문 공개 + 가이디드 비교
  → 원문 공개
  → 3카테고리 비교 테이블 (구문/어휘/연결)
  → 각 차이점에 "왜 원문이 더 좋은지" 설명
  → L1 간섭 패턴 태그
  → 사용자 수정 후 재제출
  |
  v
[Phase F2] 수정본 재비교 + 개선점 강조
  → 수정으로 개선된 부분 칭찬
  → 아직 남은 차이점 안내
  |
  v
[Phase H2] 세션 마무리
  → "배운 표현 TOP 3" 정리
  → 오류 프로필 업데이트 (Mode A와 동일한 프로필 공유)
  → 세션 기록 저장 (mode: "back-translation")
  → "배운 표현을 Anki 카드로 만들까요?"
```

### 중도 종료 처리

사용자가 Phase D~G 중간에 그만두고 싶을 때:
- 현재까지 수집된 오류 데이터로 error-profile.md 부분 업데이트
- 세션 노트에 status: \"incomplete\" 표시
- 나중에 이어서 할 수 있도록 안내

### 다중 세션 연결

```
[세션 1] Phase A~H 완료 → error-profile 업데이트
   |
   | (시간 경과)
   |
[세션 2] Phase A에서 세션 1 오류 프로필 로드 → 맞춤 가이드 → Phase B~H
   |
   | (시간 경과)
   |
[세션 N] Phase A에서 N-1 세션까지의 누적 프로필 로드 → 추세 분석 → ...
```

---

## 8. 데이터 스키마

### Obsidian 저장 구조

```
writing-coach/
  error-profile.md
  sessions/
    260318-climate-change.md
    260320-remote-work.md
  vocab/                        (AnkiConnect 폴백 시)
    260318-climate-change.md
  error-cards/                  (AnkiConnect 폴백 시)
    260318.md
```

### error-profile.md 프론트매터

```yaml
type: writing-coach-profile
last_updated: 2026-03-18
total_sessions: 12
current_level: upper-intermediate
l1_errors:
  articles: { count: 23, trend: "decreasing", last_5: [5, 4, 3, 3, 2] }
  subject_verb: { count: 8, trend: "stable", last_5: [2, 1, 2, 2, 1] }
  plural: { count: 7, trend: "decreasing", last_5: [2, 2, 1, 1, 1] }
  tense: { count: 15, trend: "decreasing", last_5: [4, 3, 3, 2, 2] }
  preposition: { count: 11, trend: "stable", last_5: [3, 2, 2, 2, 2] }
  literal_translation: { count: 6, trend: "decreasing", last_5: [2, 1, 1, 1, 1] }
grammar_errors:
  punctuation: { count: 5, trend: "stable", last_5: [1, 1, 1, 1, 1] }
  sentence_structure: { count: 3, trend: "stable", last_5: [1, 0, 1, 0, 1] }
structure_errors:
  topic_sentence: { count: 4, trend: "improving", last_5: [2, 1, 1, 0, 0] }
  transition: { count: 6, trend: "stable", last_5: [2, 1, 1, 1, 1] }
style_notes:
  vocabulary_diversity: "improving"
  register_awareness: "needs work"
focus_areas: ["articles", "preposition", "transition"]
```

- last_5 배열의 각 값 = 해당 세션에서 그 오류 유형이 발생한 횟수
- 배열 순서 = 가장 오래된 세션 → 가장 최근 세션 (왼쪽 = 과거, 오른쪽 = 최근)
- trend 계산: last_5[0:2] 평균 vs last_5[3:5] 평균 비교 (30%+ 변화 기준)

### 세션 노트 프론트매터

```yaml
type: writing-session
date: 2026-03-18
topic: "Climate Change and Individual Responsibility"
topic_type: social-issue       # social-issue | personal-interest
status: complete               # complete | incomplete
word_count: 267
vocabulary_provided: 18
vocabulary_used: ["sustainable", "carbon footprint", "moreover", "mitigate"]
vocabulary_usage_rate: 0.22    # count(사용된 제공 어휘) / count(전체 제공 어휘)
round1_errors:
  articles: 3
  tense: 2
  preposition: 1
round2_feedback: ["weak topic sentence in body 2", "transition between para 2-3"]
round3_highlights: ["vocabulary diversity improved", "register mostly appropriate"]
anki_cards_created: 4          # 이번 세션에서 생성된 오류 카드 수
mode: free-writing             # free-writing | back-translation
```

### 역번역 세션 노트 프론트매터 (Mode B)

```yaml
type: writing-session
date: 2026-03-19
topic: "The Role of Technology in Education"
topic_type: social-issue
status: complete
mode: back-translation
model_text_source: "web-search"   # web-search | ai-generated
model_text_word_count: 156
user_word_count: 142
syntax_gaps: 3                    # 구문 차이 수
vocabulary_gaps: 5                # 어휘 차이 수
cohesion_gaps: 2                  # 연결 차이 수
l1_interference_found: 2          # 비교에서 발견된 L1 간섭 수
revision_improvement:             # 수정 전후 갭 추적
  syntax_before: 3
  syntax_after: 1
  vocabulary_before: 5
  vocabulary_after: 2
  cohesion_before: 2
  cohesion_after: 1
learned_expressions:
  - expr: "fundamentally reshaped"
    pos: verb-phrase
    source: "Technology has fundamentally reshaped..."
    anki_created: true
  - expr: "precipitated a decline"
    pos: verb-phrase
    source: "Social media has precipitated a decline..."
    anki_created: true
  - expr: "becomes indispensable"
    pos: verb-phrase
    source: "Digital literacy becomes indispensable..."
    anki_created: false
l1_errors_found:                  # 비교에서 발견된 L1 오류 (프로필 업데이트용)
  articles: 2
  preposition: 1
anki_cards_created: 2
```

---

## 9. 리스크 & 완화 전략

| 리스크 | 영향 | 확률 | 완화 전략 |
|--------|------|------|----------|
| AnkiConnect 미실행 | REQ-2, REQ-8 카드 생성 불가 | 중 | Phase A에서 연결 확인. 실패 시 Obsidian 노트 폴백으로 교정 흐름은 정상 진행 |
| error-profile.md 손상/형식 오류 | REQ-7 데이터 손실 | 하 | 업데이트 전 read로 현재 상태 확인 + YAML 파싱 실패 시 빈 프로필로 재시작하고 사용자에게 알림 |
| 3라운드 피드백으로 컨텍스트 누적 | 후반 라운드 품질 저하 가능성 | 하 | 200K 컨텍스트에서 500단어 에세이 + 3라운드 풀 피드백은 충분히 수용. 이전 라운드 피드백 전체 유지하여 품질 극대화 |
| L1 간섭 오진(false positive) | 학습자 혼란 | 중 | 확신도 낮은 교정은 \"~하면 더 자연스럽습니다\" 톤 사용, 단정적 표현 금지 |
| obsidian-to-anki 스킬 인터페이스 변경 | 카드 생성 실패 | 하 | 카드 생성을 별도 Phase로 분리, 메인 교정 흐름과 독립. 에러 시 사용자에게 수동 생성 안내 |
| 사용자 중도 종료 | 오류 데이터 유실 | 중 | 중도 종료 시에도 현재까지 데이터로 부분 업데이트 수행 |

---

## 10. 참고 자료

### 교육학적 근거
- 인지 부하 이론 (Sweller, 1988) — 점진적 피드백의 이론적 근거
- 간격 반복 + 글쓰기 통합 효과 (Nation, 2001) — 어휘 retention 연구
- L1 간섭 연구 (Swan & Smith, 2001) — 한국어 화자 영어 오류 체계
- 역번역 학습법 (Beiler, 2020) — 번역이 외국어 학습의 촉매로 작용
- Guided noticing 연구 (2025) — 구조화된 비교가 자유 비교보다 효과적
- Parallel text 학습법 — 이중 언어 텍스트를 통한 패턴 인식 촉진

### 기존 도구 분석
- LanguageTool — 오픈소스 문법 교정
- Harper — 로컬 기반 문법 검사
- WriteHERE — AI 글쓰기 에이전트 (재귀적 글쓰기 계획)

### 연동 스킬
- obsidian-to-anki: CTP-English, CTP-Cloze, CTP-Knowledge 카드 타입
- Anki 덱 네이밍: Obsidian::English::{note_title} 패턴

---

## 관련 문서

- [[나머지/도구와 자동화/CMDS/📖 400 Methodologies/AI 프로젝트 기획-실행 파이프라인 (pipeline-full)]]
- [[나머지/도구와 자동화/CMDS/📖 400 Methodologies/AI 소형 프로젝트 빠른 가이드 (pipeline-quick)]]
- [[나머지/시스템/템플릿/CLAUDE-template]]
