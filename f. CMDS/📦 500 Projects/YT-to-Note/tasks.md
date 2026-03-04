---
tags:
  - project
  - yt-to-note
  - tasks
created: '2026-03-04'
version: '2.0'
aliases:
  - YT-to-Note Tasks
---
# YT-to-Note 태스크 분해

> **PRD**: [[PRD]]
> **파이프라인**: pipeline-full Phase 4
> **최종 수정**: 2026-03-04

---

## 실행 순서

```
Task 1+2 (병렬) → Task 3+6 (병렬) → Task 4 → Task 5 → Task 7 → Task 8
```

---

## Task 1: 환경 설정 (사전 조건) ✅
- **복잡도**: 낮음 | **의존성**: 없음 | **상태**: 완료
- [x] YouTube Transcript MCP 서버 연결 확인/설치 (`@fabriqa.ai/youtube-transcript-mcp`)
- [x] Obsidian CLI 활성화 확인 (로컬 설치 완료)
- [x] kepano/obsidian-skills 내용 검토 (`obsidian-markdown`, `json-canvas` 설치됨)
- [ ] Note Linker 플러그인 설치 확인 (v2에서 처리)
- [x] Perplexity/Gemini MCP → 스킵, Claude 웹 검색으로 대체

## Task 2: 노트 템플릿 설계 ✅
- **복잡도**: 중간 | **의존성**: 없음 | **상태**: 완료 (v7.0)
- [x] 기술/개발 템플릿 마크다운 구조 확정 → `d. Templates/YT-Note-Tech-Template.md` (v7.0)
- [x] 지식/교양 템플릿 마크다운 구조 확정 → `d. Templates/YT-Note-Knowledge-Template.md` (v7.0)
- [x] 영어 학습 템플릿 마크다운 구조 확정 → `d. Templates/YT-Note-English-Template.md` (v3.0)
- [x] 프론트매터 스키마 확정
- [x] 저장 경로 규칙 확정: `f. CMDS/20. Literature Notes/YT-{genre}-{YYMMDD}-{제목축약}.md`
- [x] Obsidian Flavored Markdown 규칙 반영

## Task 3: 자막 추출 + 1차 분석 로직 ✅
- **복잡도**: 중간 | **의존성**: Task 1 | **상태**: 완료
- [x] YouTube Transcript MCP 호출 로직 (폴백 체인: ko→en, timestamps on→off)
- [x] 영상 메타데이터 추출 (oEmbed API + WebSearch 폴백)
- [x] 장르 자동 판별 프롬프트 설계 (tech/knowledge/english, 70% 확신도 기준)
- [x] 서브에이전트 패턴 구현 (자막 → JSON 중간 결과물)
- **산출물**: `logic/transcript-extraction.md`

## Task 4: 노트 생성 프롬프트 설계 ⭐ 핵심 ✅
- **복잡도**: 높음 | **의존성**: Task 2, 3 | **상태**: 완료
- [x] 기술/개발 노트 생성 프롬프트 작성
- [x] 지식/교양 노트 생성 프롬프트 작성
- [x] 영어 학습 노트 생성 프롬프트 작성
- [x] 공통 후처리 규칙 (품질 체크리스트 10항목)
- **산출물**: `logic/note-generation-prompts.md`, `.claude/skills/yt-to-note/references/prompt-*.md`

## Task 5: 보충자료 수집 로직 ✅
- **복잡도**: 중간 | **의존성**: Task 4 | **상태**: 완료
- [x] 핵심 개념/용어 추출 로직 (최대 8개)
- [x] 웹 검색 보충자료 수집 (장르별 검색 전략)
- [x] 용어 사전 보강 로직 (웹 크로스체크)
- [x] 보충자료를 노트에 통합하는 포맷
- **산출물**: `logic/supplementary-research.md`

## Task 6: 옵시디언 저장 + 내부 링크 ✅
- **복잡도**: 중간 | **의존성**: Task 1, 2 | **상태**: 완료
- [x] Obsidian MCP로 노트 저장 로직 (중복 체크 → 저장 → 검증)
- [x] 기존 볼트 노트 검색 → 내부 링크 생성 로직 (3개 위치)
- [x] 프론트매터 자동 생성
- [x] 에러 핸들링 (경로 없음, 중복 파일명, MCP 실패 등)
- **산출물**: `logic/obsidian-save.md`

## Task 7: Cowork 스킬 통합 & 패키징 ✅
- **복잡도**: 중간 | **의존성**: Task 3, 4, 5, 6 | **상태**: 완료
- [x] SKILL.md 작성 (7단계 파이프라인)
- [x] references/ 폴더: prompt-tech.md, prompt-knowledge.md, prompt-english.md, sub-agent-schema.md
- [x] 에러 핸들링 + 폴백 로직 통합
- [x] 엣지 케이스 처리 문서화
- **산출물**: `.claude/skills/yt-to-note/SKILL.md` + `references/` (4개 파일)

## Task 8: 테스트 & 품질 검증 ✅
- **복잡도**: 중간 | **의존성**: Task 7 | **상태**: 완료 (부분)
- [x] 모의 데이터로 tech 노트 E2E 테스트
- [x] 옵시디언 저장 + 프론트매터 검증 성공
- [x] 테스트 노트: `f. CMDS/20. Literature Notes/YT-tech-260304-React-Server-Components.md`
- [ ] 실제 YouTube Transcript MCP 연동 테스트 (Claude Code 세션에서 수행 필요)
- [ ] knowledge/english 장르 테스트 (동일 파이프라인이므로 Claude Code에서 진행)
- [ ] 내부 링크 정확도 확인 (볼트 내 관련 노트와 연결)
