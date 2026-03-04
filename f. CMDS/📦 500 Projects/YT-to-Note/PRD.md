---
tags:
  - project
  - yt-to-note
  - prd
  - claude-cowork
created: '2026-03-04'
version: '1.0'
aliases:
  - YT-to-Note PRD
pipeline: pipeline-full
phase: 3-PRD
---
# YT-to-Note PRD

> **프로젝트명**: YT-to-Note — 유튜브 학습 노트 에이전트
>
> **목적**: 유튜브 영상을 구조화된 학습 노트로 자동 변환하고, 보충자료와 기존 지식을 연결하여 옵시디언 볼트에 축적한다
>
> **아키텍처**: Claude 네이티브 (Cowork 스킬)
>
> **파이프라인**: pipeline-full (중형)
>
> **최종 수정**: 2026-03-04 | 버전: 1.0

---

## Phase 1 요약

| 항목 | 확정 내용 |
|------|----------|
| **What** | 유튜브 링크 → 구조화된 학습 노트 자동 생성 에이전트 |
| **Why** | 영상 학습 효율 극대화, 지식을 옵시디언에 체계적 축적 |
| **Who** | 1인 사용 (본인) |
| **Where** | Claude Cowork 스킬 → 옵시디언 볼트 저장 |
| **When** | 주 7~10개 영상 처리 |
| **How** | MCP로 자막 추출 → AI 분석 (장르별 템플릿) → 보충자료 검색 → 옵시디언 CLI로 저장 |

---

## 기술 스택

| 구성요소 | 선택 | 비고 |
|---------|------|------|
| 자막 추출 | **YouTube Transcript MCP** (hancengiz 또는 ergut) | 언어 선택/폴백, 타임스탬프 on/off, 서브에이전트 가이드 포함 |
| AI 분석 | Claude (Cowork 내장) | 멀티스텝 추론, 웹 검색 |
| 보충자료 검색 | Claude 웹 검색 + **Perplexity MCP** (선택) | Perplexity 연결 시 검색 품질 향상 |
| 옵시디언 CLI 사용 | **kepano/obsidian-skills** 내장 | 옵시디언 창시자 제작, CLI/Markdown/Bases 스킬 |
| 내부 링크 | Claude 1차 생성 + **Note Linker 플러그인** 후처리 | 볼트 전체 스캔으로 누락 링크 보완 |
| 실행 방식 | Cowork 스킬 (온디맨드) | 링크 붙여넣기 → 실행 |
| 컨텍스트 관리 | 서브에이전트 패턴 | 자막 처리를 별도 컨텍스트에서 수행 |

### 사전 조건

- [ ] YouTube Transcript MCP 서버 연결
- [ ] kepano/obsidian-skills 설치 (또는 스킬에 내장)
- [ ] Obsidian CLI 활성화 (설정 → General → CLI)
- [ ] Note Linker 플러그인 설치
- [ ] (선택) Perplexity MCP 서버 연결 + API 키

---

## 기능 요구사항

### REQ-1: 유튜브 자막 추출

- **입력**: 유튜브 URL (단일 또는 복수)
- **처리**: YouTube Transcript MCP로 자막 추출. 한국어 우선, 없으면 영어 자막 추출 후 분석 시 한국어로 처리. 타임스탬프 off 모드로 토큰 절약 (60분 기준 ~19k tokens)
- **출력**: 전체 자막 텍스트 + 영상 메타데이터 (제목, 채널명, 설명)
- **수락 기준**: 자막이 있는 영상에서 95% 이상 정상 추출. 자막 없는 영상은 사용자에게 알림 후 중단
- **컨텍스트 관리**: 서브에이전트에서 자막 추출 + 1차 구조화를 수행하여 메인 세션 컨텍스트 보존

### REQ-2: 장르 판별 & 템플릿 선택

- **입력**: 추출된 자막 + 영상 메타데이터
- **처리**: 콘텐츠 분석으로 장르 자동 판별 (기술/개발 vs 지식/교양)
- **출력**: 선택된 템플릿 유형
- **수락 기준**: 90% 이상 정확한 장르 분류. 애매한 경우 사용자에게 확인

#### 기술/개발 템플릿 포함 요소
- 핵심 개념 정리 (개념 → 설명 → 예시 구조)
- 코드/명령어 블록
- 실습 체크리스트
- 관련 공식문서 링크
- 기술 용어 사전

#### 지식/교양 템플릿 포함 요소
- 핵심 논점/주장 구조화
- 근거/사례 정리
- 시간순 또는 논리순 흐름도
- 비판적 사고 질문
- 전문 용어 사전

### REQ-3: 구조화된 학습 노트 생성

- **입력**: 자막 텍스트 + 선택된 템플릿
- **처리**: AI가 자막을 분석하여 템플릿에 맞는 구조화된 노트 생성. Obsidian Flavored Markdown 사용 (kepano/obsidian-skills 기반)
- **출력**: 마크다운 학습 노트 (프론트매터 포함)
- **수락 기준**: 영상의 핵심 내용 90% 이상 포함. 단순 요약이 아닌 학습 가능한 구조

### REQ-4: 보충자료 수집 & 통합

- **입력**: 노트 내 핵심 개념/용어
- **처리**:
  - Perplexity MCP 연결 시: `perplexity_ask`로 검색 (우선)
  - 미연결 시: Claude 내장 웹 검색으로 폴백
  - 전문 용어 사전 생성
- **출력**: 노트 하단에 보충자료 섹션 (링크 + 요약) + 용어 사전 섹션
- **수락 기준**: 핵심 개념당 최소 1개 이상 신뢰할 수 있는 보충 출처. 전문 용어는 모두 정의 포함

### REQ-5: 옵시디언 저장 & 내부 링크 연결

- **입력**: 완성된 노트
- **처리**:
  1. Obsidian CLI로 지정 경로에 노트 저장 (kepano/obsidian-skills CLI 스킬 기반)
  2. Claude가 기존 볼트 노트를 검색하여 관련 노트와 `[[내부 링크]]` 1차 생성
  3. Note Linker 플러그인이 후처리로 누락 링크 보완
- **출력**: 옵시디언 볼트 내 지정 경로에 저장된 노트 (프론트매터 + 내부 링크 포함)
- **수락 기준**: 지정 경로에 정상 저장. 관련 기존 노트가 있으면 최소 1개 이상 링크. 프론트매터에 태그/소스URL/날짜 포함

### REQ-6: 컨텍스트 관리 (서브에이전트 패턴)

- **입력**: 긴 자막 텍스트 (60분+ 영상)
- **처리**: 자막 분석을 서브에이전트에 위임하여 메인 세션 컨텍스트 오버플로 방지
- **출력**: 구조화된 중간 결과물 (메인 세션에서 노트 완성에 사용)
- **수락 기준**: 2시간 이상 영상도 컨텍스트 오버플로 없이 처리 가능

---

## 프론트매터 스키마

```yaml
---
type: yt-note
genre: tech | knowledge  # 자동 판별
source: "[영상 제목](유튜브 URL)"
channel: "채널명"
date_watched: YYYY-MM-DD
date_created: YYYY-MM-DD
tags:
  - yt-note
  - [장르 태그]
  - [주제 태그들]
status: processed
---
```

---

## 저장 경로 규칙

```
[볼트 루트]/
  └── [사용자 지정 폴더]/
      └── YT-[장르]-[YYMMDD]-[영상제목 축약].md
```

> 구체적인 폴더 경로는 구현 시 사용자 확인 후 확정

---

## 안 하는 것 (v1)

- 영상 파일(로컬) STT → v2
- 시각 정보(슬라이드/화면) 분석 → v2
- 배치 자동 처리 (스케줄 태스크) → v2
- Anki/플래시카드 생성 → v2
- 노트 품질 자동 평가 → v2
- 복수 영상 한 번에 처리 → v2

---

## 참고 자료 & 오픈소스

### 직접 도입
- [hancengiz/youtube-transcript-mcp](https://github.com/hancengiz/youtube-transcript-mcp) — YouTube 자막 MCP
- [ergut/youtube-transcript-mcp](https://github.com/ergut/youtube-transcript-mcp) — 리모트 대안 (제로 셋업)
- [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) — 옵시디언 공식 에이전트 스킬
- [Obsidian Note Linker](https://github.com/AlexW00/obsidian-note-linker) — 내부 링크 자동 매칭

### 설계 패턴 참고
- [BayramAnnakov/notebooklm-youtube-skill](https://github.com/BayramAnnakov/notebooklm-youtube-skill) — 영상→리서치→결과물 파이프라인 패턴
- [ZanderRuss/obsidian-claude](https://github.com/ZanderRuss/obsidian-claude) — 리서치 에이전트 오케스트레이션
- [ballred/obsidian-claude-pkm](https://github.com/ballred/obsidian-claude-pkm) — PKM 스타터킷

---

## 관련 문서

- [[AI 소형 프로젝트 빠른 가이드 (pipeline-quick)]]
- [[AI 프로젝트 기획-실행 파이프라인 (pipeline-full)]]
- [[CLAUDE-template]]
