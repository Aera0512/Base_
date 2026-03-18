---
tags:
  - project
  - writing-coach
  - prd
  - claude-cowork
  - english-learning
created: '2026-03-18'
version: '0.2'
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
> **최종 수정**: 2026-03-18 | 버전: 0.2

---

## 1. 문제 정의 & 근거

### 해결하려는 문제

한국어 화자가 영어 에세이 실력을 향상시키려 할 때 3가지 핵심 문제가 존재한다:

- **단절된 학습 루프**: 어휘 학습(Anki), 글쓰기 연습, 교정 피드백이 별도 도구에서 이루어져 연결이 끊김. 배운 어휘를 글쓰기에 활용하는 전이(transfer)가 일어나지 않음
- **일방적 교정**: 기존 도구(Grammarly, LanguageTool)는 교정본만 제공하고 끝남. 학습자가 직접 수정하는 과정이 없어 동일 실수를 반복. 연구에 따르면 "힌트를 받고 직접 고치는 것"이 교정본을 읽기만 하는 것보다 2-3배 효과적
- **개인화 부재**: 한국어 L1 간섭 패턴(관사 누락, 시제 혼용, 전치사 직역)을 특별히 추적하는 도구가 없음. 매번 같은 유형의 실수를 처음 보는 것처럼 교정받음

### 교육학적 근거

- 인지 부하 이론(Sweller, 1988): 모든 피드백을 동시에 제공하면 학습 효과 저하 — 점진적 교정이 최적
- 간격 반복 + 글쓰기 통합(Nation, 2001): 실제 오류에서 추출한 SRS 카드가 일반 단어장보다 높은 retention rate
- L1 간섭 체계(Swan & Smith, 2001): 한국어 화자의 예측 가능한 오류 패턴을 우선 교정하면 학습 효율 극대화
- CEFR 기반 평가: 레벨별 비교를 통해 학습자가 현재 위치와 목표를 시각적으로 파악

---

## 2. 목표 & 성공 지표

### 핵심 목표

- 어휘 학습 → 글쓰기 → 교정 → SRS 카드의 완전 자동화 파이프라인 제공
- 3라운드 점진적 교정으로 학습자가 직접 수정하며 배우는 사이클 구축
- 세션 간 오류 추적으로 개인화된 피드백 누적

### 측정 가능한 성공 지표

| 지표 | 목표 | 측정 방법 |
|------|------|----------|
| 어휘 활용률 | 제공 어휘의 25%+ 에세이에 사용 | 세션 노트의 vocabulary_usage_rate |
| L1 간섭 검출율 | 한국어 특유 오류 90%+ 검출 | 수동 검토 대비 비교 (eval 시) |
| 오류 감소 추세 | 5세션 후 반복 오류 30%+ 감소 | error-profile의 last_5_sessions 추이 |
| 레벨별 리라이트 차별성 | 4레벨 간 명확한 차이 존재 | eval 시 질적 평가 |
| 전체 워크플로우 완료율 | Phase A~H 정상 완료 95%+ | 스킬 실행 로그 |

---

## 3. 범위 & 트레이드오프

### 범위 안 (v1)

- 에세이 형식 글쓰기 (의견/논증형)
- 주제별 어휘 생성 + Anki 카드 자동 생성 (obsidian-to-anki 연동)
- 3라운드 점진적 교정 (Grammar → Clarity → Style)
- 한국어 L1 간섭 특화 교정
- 4레벨 비교 리라이트 (A2-B1 / B1-B2 / B2-C1 / C1-C2)
- Obsidian 기반 오류 프로필 누적 추적
- 오류 기반 Anki 카드 자동 생성

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

---

## 4. 맥락 & 기술 스택

### 기존 인프라 연동

| 구성요소 | 선택 | 역할 |
|---------|------|------|
| AI 엔진 | Claude (Cowork 내장) | 어휘 생성, 교정, 레벨별 리라이트 |
| 어휘 카드 | obsidian-to-anki 스킬 | CTP-English, CTP-Cloze 카드 생성 |
| 오류 추적 | Obsidian MCP | 프론트매터 기반 오류 프로필 관리 |
| 웹 검색 | Claude 내장 | 주제별 어휘 리서치 |

### 사전 조건

- Obsidian MCP 연결 확인
- AnkiConnect 실행 상태 확인 (localhost:8765)
- Obsidian 볼트에 writing-coach/ 폴더 존재

---

## 5. 기능 요구사항

### REQ-1: 주제 선정 & 어휘 생성

**입력**: 사용자 지정 주제 또는 "추천해줘" 요청

**처리**:
- 주제 추천 시: 시사/사회 이슈와 개인 관심사를 번갈아 추천. 난이도(B2 적정 / C1 도전) 표시
- 주제 확정 후 3가지 카테고리 어휘 생성:
  - 주제별 핵심 어휘 (8-10개): 콜로케이션 포함
  - 에세이 연결어/표현 (5-7개): 담화 표지, 의견 표현
  - B2-C1 고급 어휘 (3-5개): 현재 수준보다 한 단계 높은 어휘
- 각 어휘에 예문, 콜로케이션, 한국어 의미, IPA 발음 포함
- 에세이 구조 가이드 제공 (서론-본론-결론 + 주제에 맞는 논증 전략)

**출력**: 어휘 리스트 + 에세이 가이드라인

**수락 기준**:
- Given 주제 "climate change"가 선정되었을 때
- When 어휘 생성이 완료되면
- Then 최소 16개 어휘가 3카테고리로 분류되어 있고, 각 어휘에 예문과 콜로케이션이 포함되어 있어야 함

### REQ-2: Anki 플래시카드 자동 생성

**입력**: REQ-1에서 생성된 어휘 리스트

**처리**:
- obsidian-to-anki 스킬 호출하여 CTP-English 카드 생성
- 덱 이름: Obsidian::English::Writing-Coach::{주제명}
- 필드 완성: Word, Phonetic, POS, POS_Class, Meaning_KR, Meaning_EN, Example_EN, Example_KR, Synonyms, Frequency, Deck_Tag, Tags

**출력**: Anki에 추가된 플래시카드

**수락 기준**:
- Given 16개 이상의 어휘 리스트가 있을 때
- When obsidian-to-anki 스킬이 실행되면
- Then 모든 어휘가 CTP-English 카드로 생성되고, 중복 카드는 skip 처리됨

### REQ-3: 에세이 작성 안내 & 대기

**입력**: 사용자의 글쓰기 준비 신호

**처리**:
- 제공 어휘 중 최소 5개 이상 활용하도록 안내
- 목표 단어 수 제안: 기본 200-300 단어 (사용자 조절 가능)
- 선택적 시간 제한 모드: 시험 대비 시 25분
- 사용자가 에세이 완성하여 제출할 때까지 대기

**출력**: 작성 가이드라인 메시지

**수락 기준**:
- Given 어휘가 제공된 상태에서
- When 사용자에게 작성 안내를 하면
- Then 목표 단어 수, 활용 어휘 수, 에세이 구조가 명시되고 압박 없이 동기 부여함

### REQ-4: Round 1 교정 — Grammar & Mechanics

**입력**: 사용자가 작성한 에세이 원문

**처리**:
- 한국어 L1 간섭 오류 우선 검출:
  - 관사 (a/the) 누락 또는 오용
  - 주어-동사 수 일치 오류
  - 단복수형 혼동
  - 시제 일관성 위반
  - 전치사 오용 (한국어 직역)
  - 직역 표현 (Konglish 패턴)
- 일반 문법 오류: 철자, 구두점, 문장 구조
- 각 오류에 대해:
  - 원문 위치 표시 (인용 + 교정)
  - 왜 틀렸는지 간결한 설명 (한국어)
  - 교정 제안 (대안 2-3개)
  - L1 간섭 오류는 한국어 간섭 태그 표시

**출력 형식 예시**:

```
[원문] "I think environment is very important issue."
[교정] "I think **the** environment is a very important issue."
[유형] 🇰🇷 한국어 간섭 — 관사 누락
[설명] 한국어에는 관사가 없어서 빠뜨리기 쉽습니다. "the environment"은 
       일반적으로 알려진 개념을 지칭하므로 정관사 the가 필요하고, 
       "issue"는 처음 언급하는 셀 수 있는 명사이므로 부정관사 a가 필요합니다.
```

**수락 기준**:
- Given 사용자의 에세이가 제출되었을 때
- When Round 1 교정이 완료되면
- Then 문법 오류 90%+ 검출, L1 간섭 오류에 한국어 간섭 태그 명시, 각 오류에 원문/교정/유형/설명 포함

### REQ-5: Round 2 교정 — Clarity & Coherence

**입력**: Round 1 피드백 반영하여 수정된 에세이

**처리**:
- 문장 수준: 모호한 표현, 불필요한 반복, 어색한 구조
- 단락 수준: 주제문(topic sentence) 존재 여부, 뒷받침 문장의 관련성
- 글 전체 수준: 서론-본론-결론 구조, 논리 흐름, 전환(transition) 자연스러움
- 각 피드백에:
  - 구체적 위치와 이유
  - 개선 방향 제안 (답을 주는 것이 아니라 방향 제시)
  - 활용 가능한 연결어/표현 제안

**출력 형식 예시**:

```
[단락 2] 주제문이 불명확합니다.
[현재] "There are many things about technology."
[문제] 이 문장은 너무 일반적이어서 이 단락이 구체적으로 무엇을 주장하는지 
      알 수 없습니다.
[방향] 이 단락에서 기술의 어떤 측면을 논의하는지 명시해보세요. 
      예: "Technology has transformed how we communicate, but this 
      convenience comes at a social cost."
[활용 표현] "however", "on the other hand", "this suggests that"
```

**수락 기준**:
- Given Round 1 수정본이 제출되었을 때
- When Round 2 교정이 완료되면
- Then 구조적 피드백이 문장/단락/전체 수준별로 제공되고, 각 피드백에 방향 제안이 포함됨

### REQ-6: Round 3 교정 — Style & Sophistication + 레벨별 비교

**입력**: Round 2 피드백 반영하여 수정된 에세이

**처리**:
- 어휘 다양성: 반복 단어 지적 + 대체어 제안
- 레지스터 적절성: 에세이 격식 수준 확인
- 세련된 표현: 단순 표현 → 고급 표현 업그레이드 제안
- 수사적 기법: 강조, 대비, 예시 등 적절한 기법 제안
- 4레벨 비교 리라이트:
  - 초급 (A2-B1): 같은 내용을 초급 수준으로
  - 중급 (B1-B2): 중급 수준 버전
  - 중상급 (B2-C1): 사용자의 목표 수준 (최종본과 비교)
  - 상급 (C1-C2): 원어민 수준의 세련된 버전
- 각 레벨 간 차이 설명: 무엇이 레벨을 나누는지

**출력**: 스타일 피드백 + 4레벨 비교 리라이트 + 레벨 간 차이 분석

**수락 기준**:
- Given Round 2 수정본이 제출되었을 때
- When Round 3 교정이 완료되면
- Then 4레벨 리라이트가 각각 동일 내용에 대해 명확히 다른 수준으로 작성되고, 레벨 간 차이가 구체적으로 설명됨

### REQ-7: 오류 프로필 관리

**입력**: 각 라운드에서 검출된 오류 데이터

**처리**:
- Obsidian writing-coach/error-profile.md에 누적 오류 기록 관리
- 오류 유형별 분류 & 빈도 추적 (L1 간섭 / 문법 / 구조 / 스타일)
- 다음 세션 시작 시 프로필을 읽어서 맞춤 가이드:
  - 반복 오류 우선 경고 (예: "최근 3회 세션에서 관사 오류 12회")
  - 개선 추세 표시 (예: "시제 오류 지난달 대비 40% 감소")
- 세션별 기록: writing-coach/sessions/YYMMDD-{주제}.md

**수락 기준**:
- Given 교정 세션이 완료되었을 때
- When 오류 프로필이 업데이트되면
- Then error-profile.md의 프론트매터에 오류 유형별 count, trend, last_5_sessions가 정확히 반영되고, 다음 세션 시작 시 이전 데이터가 참조됨

### REQ-8: 오류 기반 Anki 카드 생성

**입력**: 교정 과정에서 발견된 반복적 오류

**처리**:
- CTP-Cloze 카드: 교정된 문장을 Cloze 변환
  - 예: "The government {{c1::has}} implemented new policies."
- CTP-Knowledge 카드: 문법 규칙 Q&A
  - 예: Q: "셀 수 없는 추상 명사 앞에 관사는?" A: "일반적 개념일 때 무관사, 특정할 때 the"
- 덱: Obsidian::English::Writing-Coach::Error-Cards

**수락 기준**:
- Given 교정에서 반복 오류가 3회+ 발견되었을 때
- When 오류 카드 생성이 실행되면
- Then 오류 패턴당 1-2장의 Cloze/Knowledge 카드가 생성되고, 중복 검사 통과

---

## 6. 에이전트 행동 경계

### Always (항상 수행)

- 세션 시작 시 error-profile.md 로드 시도 (없으면 새로 생성)
- L1 간섭 오류에 한국어 간섭 태그 표시
- 교정 시 원문/교정/유형/설명 4요소 포함
- 사용자가 수정본을 제출할 때까지 다음 라운드 진행하지 않음
- 세션 종료 시 error-profile.md 업데이트 및 세션 노트 저장

### Ask (사용자에게 확인)

- 주제 추천 시: "이 주제로 할까요?"
- 어휘 리스트 완성 후: "이 어휘들로 진행할까요? 추가/변경할 단어 있나요?"
- Round 3 완료 후: "오류 기반 Anki 카드도 만들까요?"
- 시간 제한 모드 적용 여부

### Never (절대 금지)

- 사용자 대신 에세이를 써주는 것
- 사용자가 수정하기 전에 다음 라운드로 넘어가는 것
- Round 1에서 스타일/구조 피드백을 섞는 것 (라운드 순서 엄수)
- 교정 없이 "잘 썼습니다"만 하는 것 (항상 개선점 제시)
- 오류 프로필을 사용자 확인 없이 삭제하는 것

---

## 7. 워크플로우 상세 흐름

```
[시작] 사용자: "글쓰기 연습하자" / "writing practice"
  ↓
[Phase A] 오류 프로필 로드
  → error-profile.md 읽기 (없으면 새로 생성)
  → "지난번 관사 오류 5회, 시제 오류 3회. 오늘 포커스: 관사"
  ↓
[Phase B] 주제 선정
  → 사용자 지정 또는 AI 추천 (시사+개인 관심사 번갈아)
  → 사용자 확인: "이 주제로 할까요?"
  ↓
[Phase C] 어휘 제공 + Anki 카드 생성
  → 주제 어휘(8-10) + 연결어(5-7) + 고급 어휘(3-5)
  → 사용자 확인: "어휘 리스트 괜찮나요?"
  → obsidian-to-anki 스킬로 CTP-English 카드 생성
  ↓
[Phase D] 에세이 작성 (사용자)
  → 목표: 200-300 단어, 제공 어휘 5개+ 활용
  → 사용자가 완성 후 제출
  ↓
[Phase E] Round 1: Grammar & Mechanics
  → L1 간섭 우선 + 일반 문법
  → [검증] 각 오류에 원문/교정/유형/설명 포함 확인
  → 사용자 수정 후 재제출
  ↓
[Phase F] Round 2: Clarity & Coherence
  → 문장/단락/전체 구조
  → [검증] 각 피드백에 방향 제안 포함 확인
  → 사용자 수정 후 재제출
  ↓
[Phase G] Round 3: Style & Sophistication
  → 어휘 다양성 + 레지스터 + 4레벨 비교 리라이트
  → [검증] 4레벨 리라이트 간 차별성 확인
  ↓
[Phase H] 세션 마무리
  → 오류 프로필 업데이트 (error-profile.md)
  → 세션 기록 저장 (sessions/YYMMDD-주제.md)
  → 사용자 확인: "오류 기반 Anki 카드도 만들까요?"
  → 다음 세션 추천 포커스 제안
```

---

## 8. 데이터 스키마

### Obsidian 저장 구조

```
writing-coach/
  error-profile.md          # 누적 오류 프로필
  sessions/
    260318-climate-change.md
    260320-remote-work.md
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
  tense: { count: 15, trend: "decreasing", last_5: [4, 3, 3, 2, 2] }
  preposition: { count: 11, trend: "stable", last_5: [3, 2, 2, 2, 2] }
  literal_translation: { count: 6, trend: "decreasing", last_5: [2, 1, 1, 1, 1] }
grammar_errors:
  punctuation: { count: 5, trend: "stable" }
  plural: { count: 7, trend: "decreasing" }
structure_errors:
  topic_sentence: { count: 4, trend: "improving" }
  transition: { count: 6, trend: "stable" }
style_notes:
  vocabulary_diversity: "improving"
  register_awareness: "needs work"
focus_areas: ["articles", "preposition", "transition"]
```

### 세션 노트 프론트매터

```yaml
type: writing-session
date: 2026-03-18
topic: "Climate Change and Individual Responsibility"
topic_type: social-issue
word_count: 267
vocabulary_used: ["sustainable", "carbon footprint", "moreover", "mitigate"]
vocabulary_provided: 18
vocabulary_usage_rate: 0.22
round1_errors: { articles: 3, tense: 2, preposition: 1 }
round2_feedback: ["weak topic sentence in body 2", "transition between para 2-3"]
round3_level: "solid B2, approaching C1 in vocabulary"
overall_impression: "B2+"
```

---

## 9. 리스크 & 완화 전략

| 리스크 | 영향 | 완화 전략 |
|--------|------|----------|
| AnkiConnect 미실행 | REQ-2, REQ-8 실패 | 세션 시작 시 연결 확인. 실패 시 어휘 리스트만 텍스트로 제공하고, 카드 생성은 나중에 수행 |
| 오류 프로필 파일 손상 | REQ-7 데이터 손실 | 업데이트 전 이전 상태 백업 (프론트매터 diff 확인) |
| 교정 라운드에서 컨텍스트 초과 | 긴 에세이 + 3라운드 피드백으로 토큰 초과 | 각 라운드에서 이전 피드백은 요약만 유지, 현재 라운드에 집중 |
| L1 간섭 오진(false positive) | 학습자 혼란 | 오류 설명에 확신도 표시, 모호한 경우 "이것이 더 자연스럽습니다" 톤 사용 |
| obsidian-to-anki 스킬 변경 | 카드 생성 실패 | 카드 생성을 별도 단계로 분리, 메인 교정 흐름과 독립적 실행 |

---

## 10. 참고 자료

### 교육학적 근거
- 인지 부하 이론 (Sweller, 1988)
- 간격 반복 + 글쓰기 통합 효과 (Nation, 2001)
- L1 간섭 연구 (Swan & Smith, 2001)

### 기존 도구 분석
- LanguageTool — 오픈소스 문법 교정
- Harper — 로컬 기반 문법 검사
- WriteHERE — AI 글쓰기 에이전트
- Writing Tools — 시스템 전역 AI 글쓰기 도구

### 연동
- obsidian-to-anki 스킬: CTP-English, CTP-Cloze, CTP-Knowledge 카드 타입

---

## 관련 문서

- [[AI 프로젝트 기획-실행 파이프라인 (pipeline-full)]]
- [[AI 소형 프로젝트 빠른 가이드 (pipeline-quick)]]
- [[CLAUDE-template]]
