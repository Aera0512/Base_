---
tags:
  - project
  - prd
  - english-learning
  - cowork-skill
created: '2026-03-05'
updated: '2026-03-06'
version: '3.0'
status: approved
---
# English Grammar Learning Agent — PRD

> **프로젝트 유형**: 중형 (Cowork 스킬)
> **목적**: 영어 문법 토픽 입력 → 심화 개념 설명 → 예문 120개 → 오디오 → 다층 연습 102문제 → 복습 워크북까지 자동 생성
> **실행 환경**: Cowork Skill (Claude Code로 개발)
> **출력**: Obsidian 볼트 직접 쓰기 (CLI)
> **TTS**: Kokoro-82M (기본) + edge-tts (폴백)
> **버전**: 3.0
> **작성일**: 2026-03-06

---

## 변경 이력

| 날짜 | 버전 | 변경 내용 |
|------|------|----------|
| 2026-03-05 | 1.0 | 초안 작성 |
| 2026-03-05 | 1.1 | TTS 변경, 출력 CLI로 변경, 유튜브 추천 추가 |
| 2026-03-05 | 1.2 | ultrathink/brainstorm 추가, 퀴즈 50, 스피킹 50+50 |
| 2026-03-06 | 3.0 | 뇌과학 기반 전면 재설계: 예문 120, 다층 연습 8유형 102문제, Fill the Gap 추가, 복습 워크북 추가 |

---

> ℹ️ 상세 PRD, 리서치 결과, CLAUDE.md는 프로젝트 폴더 `Grammer_generater/` 참고
> - `docs/PRD.md` — 전체 PRD (v3.0)
> - `docs/research.md` — TTS 비교, 오픈소스 조사
> - `CLAUDE.md` — Claude Code 프로젝트 컨텍스트

---

## 설계 근거

6개 학습 이론 기반: DeKeyser Skill Acquisition, Nation Four Strands, Cognitive Load Theory, Interleaving, Retrieval Practice, Krashen i+1

## 파이프라인
```
입력: "Present Perfect"
  │
  ├─ [1] 🧠 웹 리서치 (3회+, ultrathink 교차검증)
  ├─ [2] 개념서 작성 (한국어, 8개 섹션)
  ├─ [3] 💡🧠 예문 120개 (brainstorm 설계 → ultrathink 생성)
  ├─ [4] TTS 오디오 3개 (Kokoro / edge-tts 폴백)
  ├─ [5] 🧠 다층 연습 102문제 (8가지 유형)
  ├─ [6] 유튜브 추천 (한국인 유튜버 3~5개)
  ├─ [7] 복습 워크북 생성
  └─ [8] Obsidian 출력 (메인 노트 + 복습 워크북 + 오디오)
```

## 수량 요약

| 구분 | 항목 | 수량 |
|------|------|------|
| 입력 | 예문 (초40/중40/고40) | 120 |
| 인식 | 빈칸18 + 오류교정12 | 30 |
| 재구성 | 문장변환10 + 어순배열10 | 20 |
| 생산 | FtG 25 + 스피킹A 12 + 스피킹B 12 | 49 |
| 적용 | 프리토킹 | 3 |
| 복습 | 워크북 자가테스트 | 10 |
| 오디오 | TTS MP3 | 3파일 |
| **전체** | | **~232** |

## 출력 구조
```
English Grammar/
├── audio/
│   ├── {topic}-beginner.mp3
│   ├── {topic}-intermediate.mp3
│   └── {topic}-advanced.mp3
├── {Topic}.md          ← 메인 학습 노트 (13개 섹션)
└── {Topic}-Review.md   ← 복습 전용 워크북 (5개 섹션)
```

## 기술 스택
| 항목 | 선택 |
|------|------|
| TTS 기본 | Kokoro-82M (CPU, 82M params, Apache 2.0) |
| TTS 폴백 | edge-tts (MS Neural, 무료) |
| 오디오 | pydub + ffmpeg |
| 출력 | Obsidian 볼트 CLI 직접 쓰기 |
| 환경 | 8GB RAM, CPU only |
