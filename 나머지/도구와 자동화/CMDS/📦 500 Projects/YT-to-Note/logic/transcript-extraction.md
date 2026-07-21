---
tags:
  - project
  - yt-to-note
  - logic
  - task-3
created: '2026-03-04'
status: complete
---

# Task 3: 자막 추출 + 1차 분석 로직

> **상태**: 설계 완료
> **의존성**: Task 1 (환경 설정)
> **다음**: Task 4 (노트 생성 프롬프트)에서 이 로직을 호출

---

## 3-1. YouTube Transcript MCP 호출 로직

### 도구 스펙

| 항목 | 값 |
|------|-----|
| 패키지 | `@fabriqa.ai/youtube-transcript-mcp@latest` |
| 도구명 | `get_transcript` |
| 필수 파라미터 | `url` (YouTube URL) |
| 선택 파라미터 | `lang` (언어코드, 기본값: 영상 기본 언어), `include_timestamps` (기본값: true) |
| 토큰 제한 | MCP 레이어에서 25,000 토큰 응답 제한 |

### 호출 전략

**1단계: 타임스탬프 포함 추출 (기본)**

```
도구: get_transcript
파라미터:
  url: {{사용자 제공 YouTube URL}}
  lang: "ko"
  include_timestamps: true
```

- 타임스탬프가 있어야 챕터별 구간(start/end) 매핑이 가능
- 60분 이하 영상은 대부분 25k 토큰 내에서 처리 가능

**2단계: 토큰 초과 시 폴백**

```
도구: get_transcript
파라미터:
  url: {{URL}}
  lang: "ko"
  include_timestamps: false
```

- 타임스탬프 제거로 토큰 약 40% 절감
- 이 경우 구간 가이드 테이블의 시간은 "대략적 추정"으로 표시

**3단계: 한국어 자막 없을 시 폴백**

```
도구: get_transcript
파라미터:
  url: {{URL}}
  lang: "en"
  include_timestamps: true
```

- 영어 자막 추출 후, 노트 생성 시 한국어로 분석/작성
- 프론트매터에 `subtitle_lang: en` 추가

**4단계: 자막 없음**

- 사용자에게 알림: "이 영상에는 사용 가능한 자막이 없습니다."
- 처리 중단

### 폴백 체인 요약

```
ko(timestamps:on) → ko(timestamps:off) → en(timestamps:on) → en(timestamps:off) → 중단
```

---

## 3-2. 영상 메타데이터 추출

YouTube Transcript MCP는 자막만 반환하므로, 메타데이터는 **별도 경로**로 수집한다.

### 방법 1: 사용자 직접 입력 (기본)

스킬 실행 시 사용자에게 다음 정보를 요청:

```
필수:
- YouTube URL
- (자동 추출 실패 시) 영상 제목
- (자동 추출 시) 채널명

선택:
- 장르 힌트 (tech/knowledge/english)
- 시청일
```

### 방법 2: 웹 검색으로 메타데이터 보완

YouTube URL에서 VIDEO_ID를 추출한 뒤, 웹 검색으로 영상 정보를 수집:

```
1. URL에서 VIDEO_ID 추출
   - youtube.com/watch?v=VIDEO_ID
   - youtu.be/VIDEO_ID
   - youtube.com/embed/VIDEO_ID

2. 웹 검색: "site:youtube.com VIDEO_ID"
   → 제목, 채널명, 설명 추출

3. 또는 YouTube oEmbed API (무인증):
   https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=VIDEO_ID&format=json
   → title, author_name 반환
```

### VIDEO_ID 추출 로직

```
입력 URL 패턴:
- https://www.youtube.com/watch?v=dQw4w9WgXcQ
- https://youtu.be/dQw4w9WgXcQ
- https://www.youtube.com/embed/dQw4w9WgXcQ
- https://youtube.com/watch?v=dQw4w9WgXcQ&t=120

추출 규칙:
1. youtu.be/ → 슬래시 뒤 11자
2. watch?v= → v= 뒤 11자 (& 전까지)
3. embed/ → embed/ 뒤 11자
```

---

## 3-3. 장르 자동 판별 프롬프트

### 판별 기준

| 장르 | 키 시그널 |
|------|----------|
| **tech** | 코드, API, 프레임워크, 라이브러리, 터미널/CLI, 아키텍처, 디버깅, 배포, 프로그래밍 언어명, GitHub, 개발환경, 함수/변수, 데이터베이스, 서버 |
| **knowledge** | 연구결과, 심리학, 경제, 역사, 과학, 사회현상, 자기계발, 건강, 뇌과학, 통계, 논문, 전문가 인터뷰, 다큐멘터리 |
| **english** | 문법, grammar, 발음, pronunciation, 표현, expression, 영어회화, TOEIC, 영작, 뉘앙스, 원어민, native speaker, 패턴 영어 |

### 판별 프롬프트

```
다음 정보를 바탕으로 이 영상의 장르를 판별하세요.

[영상 제목]: {{title}}
[채널명]: {{channel}}
[자막 앞부분 500자]: {{transcript_preview}}

장르 옵션:
1. tech — 프로그래밍, 개발, IT 기술, 소프트웨어, 개발 도구
2. knowledge — 지식, 교양, 과학, 심리학, 경제, 자기계발, 건강
3. english — 영어 학습, 문법, 회화, 발음, 시험 영어

판별 규칙:
- 코드/명령어/API가 등장하면 → tech
- 영어 학습 관련 키워드가 주된 주제면 → english
- 그 외 지식/교양 콘텐츠 → knowledge
- 확신도가 70% 미만이면 → "uncertain" + 가장 가능성 높은 장르

출력 형식 (JSON):
{
  "genre": "tech" | "knowledge" | "english",
  "confidence": 0.0~1.0,
  "reason": "판별 근거 한 줄"
}
```

### 불확실한 경우 처리

confidence < 0.7일 때 사용자에게 확인:
```
영상 장르를 자동 판별한 결과:
- 추정 장르: {{genre}} (확신도: {{confidence}})
- 판별 근거: {{reason}}

이 장르로 진행할까요? 다른 장르를 선택하시겠습니까?
→ [tech] [knowledge] [english]
```

---

## 3-4. 서브에이전트 패턴 (컨텍스트 관리)

### 왜 서브에이전트가 필요한가

- 60분 영상 자막 ≈ 19,000 토큰 (타임스탬프 off)
- 자막 전체를 메인 세션에 넣으면 컨텍스트 압박
- 서브에이전트에서 자막 → 구조화된 중간 결과물로 압축 후, 메인 세션으로 반환

### 서브에이전트 워크플로

```
[메인 세션]
    │
    ├─ 1. 사용자로부터 YouTube URL 수신
    ├─ 2. VIDEO_ID 추출 + 메타데이터 수집
    ├─ 3. 장르 판별
    │
    ├─ 4. ★ 서브에이전트 호출 ★
    │     │
    │     ├─ YouTube Transcript MCP로 자막 추출
    │     ├─ 자막을 챕터 단위로 분절
    │     ├─ 각 챕터의 핵심 내용 구조화
    │     ├─ 타임스탬프 → 구간 매핑
    │     └─ 구조화된 중간 결과물(JSON) 반환
    │
    ├─ 5. 중간 결과물로 노트 생성 (Task 4 프롬프트)
    ├─ 6. 보충자료 수집 (Task 5)
    └─ 7. 옵시디언 저장 (Task 6)
```

### 서브에이전트 프롬프트 (자막 → 중간 결과물)

```
당신은 YouTube 영상 자막을 분석하여 구조화된 학습 노트의 재료를 만드는 분석가입니다.

## 입력
- 영상 제목: {{title}}
- 채널: {{channel}}
- 장르: {{genre}}
- 자막 전문: (아래 첨부)

## 임무

1. **챕터 분절**: 자막을 주제 전환 기준으로 2~5개 챕터로 나누세요.
   - 각 챕터에 제목을 붙이세요
   - 각 챕터의 시작/종료 타임스탬프를 기록하세요 (초 단위)

2. **챕터별 핵심 분석**: 각 챕터에 대해:
   - 핵심 주장/개념 (1~2문장)
   - 뒷받침 근거/사례 (구체적으로)
   - 핵심 용어 목록
   - 난이도 라벨 (🟢 기초 / 🟡 중급 / 🔴 심화)
   - [tech] 코드/명령어가 있다면 원문 보존
   - [english] 문법 규칙/패턴/예문이 있다면 원문 보존

3. **전체 분석**:
   - 한 줄 핵심 요약
   - 4~6문장 개요
   - 마인드맵 구조 (최상위 노드 → 챕터 → 하위 개념)
   - 암기 포인트 (★ 중요도 포함, 최대 6개)
   - 핵심 용어 사전 (용어 → 정의 → 맥락)

## 출력 형식

JSON 형식으로 반환하세요:

{
  "title": "영상 제목",
  "channel": "채널명",
  "genre": "tech|knowledge|english",
  "video_id": "VIDEO_ID",
  "one_liner": "한 줄 핵심",
  "overview": "4~6문장 개요",
  "mindmap": {
    "root": "핵심 주제",
    "branches": [
      {"label": "챕터1 주제", "children": ["하위1", "하위2"]},
      ...
    ]
  },
  "key_points": [
    {"importance": 3, "concept": "개념", "summary": "한 줄", "anchor": "기억 고리"},
    ...
  ],
  "chapters": [
    {
      "number": 1,
      "title": "챕터 제목",
      "difficulty": "🟢 기초",
      "start_seconds": 0,
      "end_seconds": 300,
      "content": {
        "background": "배경/문제 상황 서술",
        "main_argument": "핵심 주장/개념 상세 서술",
        "evidence": ["근거1 상세", "근거2 상세"],
        "examples": ["사례1 상세"],
        "analogy": "비유 설명",
        "code_blocks": ["코드 블록 (tech만)"],
        "patterns": ["패턴 구조 (english만)"],
        "example_sentences": ["예문 (english만)"],
        "common_mistakes": ["흔한 실수"],
        "terms": [{"term": "용어", "definition": "정의"}]
      }
    },
    ...
  ],
  "glossary": [
    {"term": "용어", "definition": "정의", "context": "이 영상에서의 맥락"}
  ],
  "synthesis": "종합 정리 서술",
  "critical_view": "비판적 시각 (knowledge만)",
  "self_test_questions": ["셀프 테스트 질문1", "질문2", ...]
}
```

### 토큰 관리

| 영상 길이 | 자막 토큰 (추정) | 전략 |
|-----------|-----------------|------|
| ~20분 | ~6k | 서브에이전트 없이 직접 처리 가능 |
| 20~60분 | 6k~19k | 서브에이전트 사용 권장 |
| 60~120분 | 19k~38k | 서브에이전트 필수 + timestamps off |
| 120분+ | 38k+ | 2회 분할 추출 또는 사용자에게 경고 |

### Cowork에서의 서브에이전트 구현

Cowork 환경에서는 `Task` 도구를 사용하여 서브에이전트를 실행:

```
도구: Task
파라미터:
  subagent_type: "general-purpose"
  description: "YouTube 자막 분석"
  prompt: |
    [서브에이전트 프롬프트 + 자막 데이터]
```

- 서브에이전트는 독립적 컨텍스트에서 실행
- 결과물(JSON)만 메인 세션으로 반환
- 메인 세션의 컨텍스트를 보존하면서 긴 자막 처리 가능

---

## 검증 기준

- [ ] 한국어 자막 있는 영상에서 정상 추출 확인
- [ ] 영어 자막만 있는 영상에서 폴백 동작 확인
- [ ] 자막 없는 영상에서 적절한 에러 메시지 확인
- [ ] 장르 판별 정확도 90% 이상 (영상 10개 테스트)
- [ ] 60분+ 영상에서 서브에이전트 패턴 정상 동작
- [ ] 중간 결과물(JSON)이 노트 생성에 충분한 정보 포함
