# YT-to-Note: YouTube 학습 노트 에이전트

유튜브 영상 URL을 받아서 구조화된 학습 노트를 자동 생성하고, 보충자료와 기존 지식을 연결하여 옵시디언 볼트에 저장합니다.

## 파이프라인 개요

```
URL 수신 → 메타데이터 추출 → 장르 판별 → 자막 추출+분석 (서브에이전트) → 노트 생성 → 보충자료 수집 → 내부 링크 생성 → 옵시디언 저장
```

---

## Step 1: 입력 수집

사용자로부터 다음을 수집하세요:

**필수:**
- YouTube URL (하나)

**선택 (자동 감지 실패 시 요청):**
- 장르 힌트: tech / knowledge / english
- 시청일 (기본값: 오늘)

## Step 2: 메타데이터 추출

### VIDEO_ID 추출

URL에서 VIDEO_ID를 파싱하세요:
- `youtube.com/watch?v=VIDEO_ID` → `v=` 뒤 11자 (`&` 전까지)
- `youtu.be/VIDEO_ID` → 슬래시 뒤 11자
- `youtube.com/embed/VIDEO_ID` → `embed/` 뒤 11자

### 영상 정보 수집

WebFetch로 YouTube oEmbed API 호출:
```
URL: https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={VIDEO_ID}&format=json
```
→ `title`, `author_name` 추출

실패 시 WebSearch로 `site:youtube.com {VIDEO_ID}` 검색하여 제목/채널명을 수집하세요.

## Step 3: 자막 추출 + 1차 분석 (서브에이전트)

### 자막 추출 폴백 체인

순서대로 시도하세요. 성공하면 다음 단계로:

1. `get_transcript(url, lang="ko", include_timestamps=true)`
2. `get_transcript(url, lang="ko", include_timestamps=false)` — 토큰 초과 시
3. `get_transcript(url, lang="en", include_timestamps=true)` — 한국어 없을 시
4. `get_transcript(url, lang="en", include_timestamps=false)` — 토큰 초과 시
5. 모두 실패 → 사용자에게 "자막 없음" 알림 후 중단

timestamps=false로 폴백한 경우, 구간 가이드의 시간은 "(추정)" 표시.

### 장르 자동 판별

자막 앞 500자 + 제목 + 채널명을 기반으로 판별:

| 장르 | 시그널 |
|------|--------|
| **tech** | 코드, API, 프레임워크, CLI, 아키텍처, 함수, GitHub, 데이터베이스, 서버 |
| **knowledge** | 연구, 심리학, 경제, 역사, 과학, 통계, 논문, 자기계발, 건강 |
| **english** | 문법, grammar, 발음, 표현, 영어회화, TOEIC, 뉘앙스, 원어민, 패턴 |

확신도 70% 미만이면 사용자에게 확인하세요.

### 서브에이전트 분석

**20분 이하 영상**: 서브에이전트 없이 직접 처리 가능
**20분 이상 영상**: Task 도구로 서브에이전트 실행

서브에이전트에게 다음을 요청하세요:

> 자막 전문을 분석하여 JSON 형태의 중간 결과물을 생성하세요.
>
> 1. **챕터 분절**: 주제 전환 기준으로 2~5개 챕터, 각 챕터에 제목/시작초/종료초/난이도(🟢🟡🔴)
> 2. **챕터별 분석**: 핵심 주장/개념, 근거/사례(구체적 수치 보존), 용어, 코드(tech), 패턴/예문(english), 비유, 흔한 실수
> 3. **전체 분석**: 한 줄 핵심, 4~6문장 개요, 마인드맵 구조, 암기 포인트(★ 중요도), 용어 사전, 종합 정리, 셀프테스트 질문

서브에이전트 결과물은 JSON 형태로 반환받으세요. 상세 JSON 스키마는 `.claude/skills/yt-to-note/references/sub-agent-schema.md`를 참조.

## Step 4: 노트 생성

장르에 따라 해당 프롬프트 참조 파일을 읽고 노트를 생성하세요:

| 장르 | 참조 파일 | 템플릿 |
|------|----------|--------|
| tech | `.claude/skills/yt-to-note/references/prompt-tech.md` | `d. Templates/YT-Note-Tech-Template.md` |
| knowledge | `.claude/skills/yt-to-note/references/prompt-knowledge.md` | `d. Templates/YT-Note-Knowledge-Template.md` |
| english | `.claude/skills/yt-to-note/references/prompt-english.md` | `d. Templates/YT-Note-English-Template.md` |

### 핵심 작성 원칙

1. **재구성, 단순 요약 금지**: 학습 가능한 구조로 변환
2. **밀도 우선**: 모든 문장에 정보, 빈 말 없이
3. **연결 강조**: 챕터 간 "왜 이 순서인지" 명시적 연결
4. **구체성 보존**: 연구 수치, 사례 디테일, 코드 원문 최대한 보존
5. **학습 과학 내장**: 비유(Feynman), 시각화(Mermaid), 인출 연습(셀프테스트)

### 형식 규칙

- **OFM**: `[[]]` 내부 링크, `> [!warning]` callout, Mermaid 다이어그램
- **iframe**: 전체 영상 `<iframe src="https://www.youtube.com/embed/{VIDEO_ID}">`, 구간 재생 `?start={초}&end={초}`
- **난이도**: `🟢 기초` `🟡 중급` `🔴 심화`
- **목차**: `[[#섹션명]]` 링크
- **분량**: 본문 8,000~15,000자

### 금지 사항

- ❌ "이 영상에서는~" 같은 메타 서술
- ❌ 영상에 없는 내용 추가 (환각)
- ❌ 빈 문장, 불필요한 연결어

## Step 5: 보충자료 수집

노트의 핵심 용어/개념 중 최대 8개를 선정하여 WebSearch로 검색:

| 장르 | 검색 우선순위 |
|------|-------------|
| tech | 공식문서 → 튜토리얼 → 심화 아티클 |
| knowledge | 원본 연구/논문 → 도서 → 관련 강연 |
| english | 문법서/사전 → 연습 사이트 → 유사 콘텐츠 |

결과를 필터링하여 **보충자료 섹션** (2~5개)과 **용어 사전 보강**에 반영하세요. 각 자료에 "이 노트의 어떤 부분을 보완하는지"를 명시.

## Step 6: 내부 링크 생성

`mcp__obsidian__search_notes`로 볼트 내 관련 노트를 검색하세요:

1. **용어 사전**: 각 용어로 검색 → 관련 노트 발견 시 `[[노트명]]` 추가
2. **"내 생각 & 연결"**: 핵심 주제로 검색 → 관련 노트 2~3개 연결, 연결 이유 기재
3. **본문**: 기존 노트의 주제가 언급되면 자연스럽게 `[[]]` 링크

**규칙**: 볼트에 실제 존재하는 노트만 링크. 빈 링크 금지. 한 노트당 2~10개.

## Step 7: 옵시디언 저장

### 파일명 생성

```
YT-{genre}-{YYMMDD}-{제목축약}.md
```
- 제목축약: 핵심 키워드 2~4개, 하이픈 연결, 30자 이내

### 프론트매터 조립

```yaml
---
type: yt-note
genre: {tech|knowledge|english}
source: "[{제목}]({URL})"
channel: "{채널명}"
video_id: "{VIDEO_ID}"
date_watched: {YYYY-MM-DD}
date_created: {오늘 날짜}
subtitle_lang: {ko|en}
tags:
  - yt-note
  - {장르}
  - {주제 태그 3~5개}
review:
  - null
  - null
  - null
confidence: null
status: processed
version: "7.0"
---
```

### 저장

1. **중복 체크**: `mcp__obsidian__get_notes_info`로 파일 존재 여부 확인
   - 존재 시 → 사용자에게 덮어쓰기 확인
2. **저장**: `mcp__obsidian__write_note(path="Yt-to-Note/{파일명}.md", content, frontmatter)`
3. **검증**: `mcp__obsidian__read_note`로 저장 확인

### 결과 보고

사용자에게 다음을 보고하세요:
- 저장된 노트 경로와 링크
- 연결된 내부 링크 목록
- 보충자료 요약
- 다음 복습 일정 안내 (+1일, +7일, +30일)

---

## 에러 핸들링

| 에러 | 대응 |
|------|------|
| 자막 없음 | "이 영상에는 자막이 없습니다" → 중단 |
| MCP 연결 실패 | "YouTube Transcript MCP가 연결되어 있는지 확인해주세요" |
| Obsidian MCP 실패 | "Obsidian이 실행 중인지 확인해주세요" |
| 토큰 초과 | timestamps off로 재시도 → 그래도 초과 시 사용자에게 경고 |
| 중복 파일명 | 사용자 확인 후 덮어쓰기 또는 번호 추가 |
| 장르 불확실 | 사용자에게 선택 요청 |

---

## 참조 파일

| 파일 | 내용 | 언제 읽는가 |
|------|------|-----------|
| `.claude/skills/yt-to-note/references/prompt-tech.md` | tech 노트 생성 상세 프롬프트 | Step 4에서 genre=tech일 때 |
| `.claude/skills/yt-to-note/references/prompt-knowledge.md` | knowledge 노트 생성 상세 프롬프트 | Step 4에서 genre=knowledge일 때 |
| `.claude/skills/yt-to-note/references/prompt-english.md` | english 노트 생성 상세 프롬프트 | Step 4에서 genre=english일 때 |
| `.claude/skills/yt-to-note/references/sub-agent-schema.md` | 서브에이전트 JSON 스키마 | Step 3에서 서브에이전트 호출 시 |
