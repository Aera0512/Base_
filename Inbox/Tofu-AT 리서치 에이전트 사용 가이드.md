---
title: Tofu-AT 리서치 에이전트 사용 가이드
date: 2026-02-26
tags:
  - Claude-Code
  - Agent-Teams
  - tofu-at
  - workflow
  - automation
status: guide
---

# Tofu-AT 리서치 에이전트 사용 가이드

> [!abstract] 요약
> `/tofu-at`는 Claude Code의 Agent Teams 기능을 활용해 **리서치 → 노트 변환 → 저장 → 품질 리뷰** 파이프라인을 자동화하는 스킬이다. 어떤 주제든 입력하면 웹 리서치 → Obsidian 마크다운 노트 생성 → 품질 검증까지 원스톱으로 처리한다.

---

## 1. 기본 사용법

### 실행 명령

```
/tofu-at
```

Claude Code 채팅에서 위 명령을 입력하면 **인터랙티브 모드**가 시작된다.

### 실행 흐름

```
/tofu-at → 액션 선택 → 대상 파일 스캔 → 설정 → 팀 구성 확인 → 실행
```

| 단계 | 내용 | 사용자 입력 |
|------|------|-------------|
| STEP 0 | 라우팅 (첫 실행 여부 확인) | 자동 |
| STEP 1 | 액션 선택 | **스캔** 선택 (권장) |
| STEP 2-A | 규모·품질·게이트·실행 방식 | 표준/품질최적/표준게이트/즉시실행 |
| STEP 2-B | Ralph 루프·DA 설정 | ON/OFF 선택 |
| STEP 3 | 팀 구성 확인 | 확인 |
| STEP 4-5 | 템플릿 생성 (자동) | - |
| STEP 6 | 최종 확인 + 실행 | **즉시 실행** 선택 |
| STEP 7 | 팀 생성 + 워커 스폰 + 파이프라인 실행 | 토픽·깊이 입력 |
| STEP 8 | 검증 + 보고 | 자동 |
| STEP 9 | 재실행 명령 생성 | 선택 |

---

## 2. 리서치 파이프라인 구조

```
┌─────────────┐    ┌─────────────────┐    ┌──────────┐    ┌──────────────────┐
│ web-researcher│ → │ note-processor  │ → │  저장     │ → │ quality-reviewer │
│ (웹 리서치)   │    │ (노트 변환)      │    │ (Obsidian)│    │ (6차원 품질평가)  │
└─────────────┘    └─────────────────┘    └──────────┘    └──────────────────┘
```

### 각 에이전트 역할

| 에이전트 | 모델 | 역할 |
|----------|------|------|
| **Lead** (Main) | Opus 4.6 | 팀 관리, 파일 쓰기, 결과 통합 |
| **web-researcher** | Sonnet 4.6 | WebSearch + WebFetch로 주제 리서치 |
| **note-processor** | Sonnet 4.6 | 리서치 JSON → Obsidian 마크다운 변환 |
| **quality-reviewer** | Sonnet 4.6 | 6차원 품질 평가 (8.0 이상 PASS) |

### 품질 평가 6차원

1. **완성도** — 핵심 질문 전부 커버했는가
2. **정확도** — 사실 기반, 출처 검증
3. **구조** — Obsidian 기능 활용도 (콜아웃, 위키링크, YAML)
4. **가독성** — 테이블, 코드블록, 시각적 구분
5. **실행가능성** — 복붙 가능한 명령어, 단계별 절차
6. **출처 품질** — 공식 문서 비중, 신뢰도

---

## 3. 실행 예시

### 입력

```
/tofu-at
→ 스캔 선택
→ 대상: research_orchestration_v2.py
→ 토픽: "오픈 클로를 제대로 활용하는 방법 (로컬과 VM)"
→ 깊이: standard
```

### 산출물

| 파일 | 위치 |
|------|------|
| Obsidian 노트 | `~/Desktop/Base_/Inbox/{토픽명}.md` |
| 리서치 원본 | `.team-os/artifacts/RESEARCH_OUTPUT.json` |
| 팀 분석 보고서 | `.team-os/artifacts/TEAM_FINDINGS.md` |

---

## 4. 설정 옵션

### 규모 (agent_count)

| 규모 | 에이전트 수 | 용도 |
|------|------------|------|
| 소규모 (1-2) | 리드 + 1 워커 | 간단한 조사 |
| **표준 (3-5)** | 리드 + 3 워커 | 일반 리서치 (권장) |
| 대규모 (5+) | 리드 + 5+ 워커 | 심층 분석 |

### 품질 전략

| 전략 | 설명 |
|------|------|
| **품질최적 + 리드 Opus** | 리드 Opus, 워커 Sonnet (권장) |
| 비용절감 | 리드 Sonnet, 워커 Haiku |
| 올 Opus | 전원 Opus (고비용) |

### Ralph 루프 & Devil's Advocate

- **Ralph 루프**: 품질 미달 시 자동 개선 반복 (최대 5회)
- **Devil's Advocate**: 별도 에이전트가 반론 제기

> [!tip] 일반 리서치는 둘 다 OFF 권장
> 시간·비용 대비 효과가 표준 리서치에서는 크지 않음

---

## 5. 스캔 대상 파일

`/tofu-at`는 기존 Python/JS 워크플로우 파일을 분석해 Agent Teams로 변환한다.

### 지원 패턴

- **순차 파이프라인**: A → B → C → D
- **병렬 팬아웃**: A → [B, C, D] → E
- **리뷰 루프**: A → B → (품질 미달 시 A로 복귀)

### 현재 등록된 팀 (registry.yaml)

| team_id | 목적 |
|---------|------|
| `qa.spawn-template-audit.standard` | 프롬프트/스킬 파일 4관점 병렬 감사 |
| `custom.vocabsnap.enhance.standard` | VocabSnap 코드 품질 개선 |
| `analysis.obsidian-pdf.v1` | Obsidian→iPad PDF 변환기 분석 |

---

## 6. 알려진 이슈 & 해결책

### SendMessage 배달 실패

> [!warning] Agent Teams 이슈 #24771
> 워커 → 리드 SendMessage가 간헐적으로 전달되지 않는 문제.
> **해결책**: 워커가 파일에 결과를 Write → 리드가 Read로 수신

### 세션 끊김 / 컨텍스트 컴팩션

> [!warning] 장시간 실행 시 발생
> 컨텍스트 윈도우 초과 시 세션 컴팩션 발생, 워커 연결 유실 가능.
> **해결책**: 리드가 남은 작업 직접 수행으로 전환

### Sibling Tool Call 에러

> [!info] 병렬 도구 호출 시 간헐 발생
> **해결책**: 실패한 호출을 개별 순차 재시도 (CLAUDE.md 규칙)

---

## 7. 파일 구조

```
Tofu-at-generater/
├── .claude/
│   ├── skills/
│   │   ├── tofu-at-spawn-templates.md   # 스폰 프롬프트 템플릿
│   │   └── tofu-at-registry-schema.md   # YAML 스키마
│   └── settings.local.json              # Agent Teams 활성화
├── .team-os/
│   ├── registry.yaml                    # 팀 정의 레지스트리
│   ├── hooks/
│   │   ├── teammate-idle-gate.js        # 워커 유휴 훅
│   │   └── task-completed-gate.js       # 태스크 완료 훅
│   └── artifacts/
│       ├── RESEARCH_OUTPUT.json         # 리서치 원본
│       ├── TEAM_FINDINGS.md             # 팀 분석 보고서
│       ├── TEAM_PLAN.md                 # 팀 실행 계획
│       ├── TEAM_PROGRESS.md             # 진행 상황
│       └── TEAM_BULLETIN.md             # 팀 활동 로그
└── CLAUDE.md                            # 프로젝트 지침
```

---

## 연결 개념

- [[Claude Code]] — Anthropic CLI AI 도구
- [[Agent Teams]] — Claude Code 멀티 에이전트 기능
- [[Obsidian]] — 지식 관리 앱 (노트 저장 대상)
- [[RAG (Retrieval-Augmented Generation)]] — 리서치 결과 활용 가능

---

## 빠른 참조

```bash
# 기본 실행
/tofu-at

# 등록된 팀 재실행 (스캔 없이)
/tofu-at spawn qa.spawn-template-audit.standard --target <FILE>
/tofu-at spawn custom.vocabsnap.enhance.standard --target /Users/aera/VocabSnap
/tofu-at spawn analysis.obsidian-pdf.v1 --target /Users/aera/Obsidian_강의pdf변환
```
