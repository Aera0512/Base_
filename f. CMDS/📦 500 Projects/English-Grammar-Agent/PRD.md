---
tags:
  - project
  - prd
  - english-learning
  - cowork-skill
created: '2026-03-05'
version: '1.1'
status: approved
---
# English Grammar Learning Agent — PRD

> **프로젝트 유형**: 중형 (Cowork 스킬)
> **목적**: 영어 문법 토픽 입력 → 심화 개념 설명 → 예문 150개 → 오디오 → 퀴즈 → 스피킹 연습 → 유튜브 추천까지 자동 생성
> **실행 환경**: Cowork Skill (Claude Code로 개발)
> **출력**: Obsidian 볼트 직접 쓰기 (CLI, not MCP)
> **TTS**: Kokoro-82M (기본) + edge-tts (폴백)
> **버전**: 1.1
> **작성일**: 2026-03-05

---

## 변경 이력

| 날짜 | 버전 | 변경 내용 |
|------|------|----------|
| 2026-03-05 | 1.0 | 초안 작성 |
| 2026-03-05 | 1.1 | TTS 변경 (edge-tts → Kokoro+edge-tts 폴백), 출력 CLI로 변경, 유튜브 추천 추가, 리서치 반영 |

---

> ℹ️ 상세 PRD, 리서치 결과, CLAUDE.md는 프로젝트 폴더 `Grammer_generater/` 참고
> - `docs/PRD.md` — 전체 PRD
> - `docs/research.md` — TTS 비교, 오픈소스 조사
> - `CLAUDE.md` — Claude Code 프로젝트 컨텍스트

---

## 핵심 요약

### 파이프라인
```
입력: "Present Perfect"
  │
  ├─ [1] 웹 리서치 (3회+, 교차검증)
  ├─ [2] 개념서 작성 (한국어, 8개 섹션)
  ├─ [3] 예문 150개 (초50/중50/고50, 10상황 균등분배)
  ├─ [4] TTS 오디오 3개 (Kokoro / edge-tts 폴백)
  ├─ [5] 빈칸 퀴즈 20문제 (초7/중7/고6)
  ├─ [6] 스피킹 연습 (영어어순 한국어 20 + 자연 한국어 20 + 상황 5)
  ├─ [7] 유튜브 추천 (한국인 유튜버 3~5개)
  └─ [8] Obsidian 출력
```

### 기술 스택
| 항목 | 선택 |
|------|------|
| TTS 기본 | Kokoro-82M (CPU, 82M params, Apache 2.0) |
| TTS 폴백 | edge-tts (MS Neural, 무료) |
| 오디오 | pydub + ffmpeg |
| 출력 | Obsidian 볼트 CLI 직접 쓰기 |
| 환경 | 8GB RAM, CPU only |

### 출력 구조
```
English Grammar/
├── audio/
│   ├── {topic}-beginner.mp3
│   ├── {topic}-intermediate.mp3
│   └── {topic}-advanced.mp3
└── {Topic}.md
```
