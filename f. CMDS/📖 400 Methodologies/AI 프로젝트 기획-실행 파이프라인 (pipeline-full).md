---
tags:
  - methodology
  - ai-workflow
  - pipeline
  - claude-code
  - task-master
created: '2026-03-04'
version: '4.0'
aliases:
  - pipeline-full
---
# AI 프로젝트 기획-실행 파이프라인 (중대형)

> **목적**: 아이디어 → 리서치 → 설계 → 실행 → 검증까지의 완전한 AI 네이티브 개발 워크플로우
>
> **대상**: 1주 이상 소요, 다중 파일/서비스, 복잡한 의존성이 있는 프로젝트
>
> **핵심 원칙**: "코드를 쓰기 전에 반드시 계획을 검토하라" — 계획과 실행의 분리가 품질을 결정한다
>
> **도구 스택**: Claude (기획 & 리서치) + Claude Code (개발) + Task Master (실행 관리)
>
> **최종 수정**: 2026-03-04 | 버전: 4.0

---

## 이 가이드를 쓸 때

아래 중 **하나라도 해당**되면 이 가이드가 필요하다:

- 외부 API/서비스가 3개 이상
- 수정/생성할 파일이 10개 이상
- 여러 사람이 협업
- DB 스키마 설계가 필요
- 프로젝트 기간이 1주 이상

**모두 해당하지 않는다면** → **[[AI 소형 프로젝트 빠른 가이드 (pipeline-quick)]]** 사용

### 프로젝트 규모별 적용

| 규모 | 예상 기간 | 적용 Phase | 예시 |
|------|-----------|-----------|------|
| **중형** (1~2주) | 1~2주 | Phase 0~6 전체 | 멀티 노드 에이전트, API 서버, 대시보드 |
| **대형** (1개월+) | 1개월+ | Phase 0~6 + 태그 분리 + 병렬 실행 | 풀스택 앱, 복합 자동화 시스템 |

---

## 파이프라인 전체 흐름

```
[Phase 0] 환경 설정 ─── CLAUDE.md + Task Master + MCP 연결
     ↓
[Phase 1] 탐색 & 아이디어 구체화 ─── Claude 대화 ←─────────┐
     ↓                                                     │
[Phase 2] 딥 리서치 → research.md ←──────────┐              │
     ↓                    ↑                  │              │
[Phase 3] PRD 작성 & 검증 ─┘(리서치 부족)     │              │
     ↓                                      │              │
[Phase 4] 태스크 분해 & 복잡도 분석            │              │
     ↓                                      │              │
[Phase 5] 반복 실행 ────────────────────────┘              │
     │    (중대 변경: 핵심 가정 무효화 시)                    │
     │    (경미/중간: Phase 4~5 내 조정)                     │
     ↓                                                     │
[Phase 6] 리뷰 & 회고 ───────────────────────────────────┘
              (다음 이터레이션/프로젝트)
```

### 피드백 루프 분류

모든 변경이 같은 수준은 아니다. 변경의 영향 범위에 따라 돌아갈 Phase가 다르다:

| 수준 | 트리거 | 돌아갈 Phase | 예시 |
|------|--------|-------------|------|
| **경미** (태스크 내) | 구현 중 세부사항 변경 | Phase 5 내 | API 파라미터 조정, 에러 핸들링 추가 |
| **중간** (태스크 간) | 기술적 발견으로 후속 태스크 영향 | Phase 4 재조정 | 라이브러리 제약으로 태스크 재분해 필요 |
| **중대** (방향 전환) | 핵심 가정 무효화 | Phase 2 또는 3 | API 폐지, 비용 10배 초과, 아키텍처 근본 변경 |

**판단 기준**: "이 변경이 앞으로의 태스크 3개 이상에 영향을 주는가?" → 예라면 중간 이상.

---

## Phase 0: 환경 설정 (최초 1회)

**목표**: AI가 프로젝트 맥락을 이해할 수 있는 기반 구축

이 단계를 건너뛰면 이후 모든 Phase의 품질이 떨어진다. CLAUDE.md 없이 Claude Code를 쓰는 것은 지도 없이 운전하는 것과 같다.

CLAUDE.md 범용 템플릿이 필요하면 → **[[CLAUDE-template]]** 참고

### Phase 0 진행 게이트
```
- [ ] CLAUDE.md가 프로젝트 루트에 존재하는가?
- [ ] Task Master가 초기화되어 있는가?
- [ ] MCP 연결이 확인되었는가?
→ 모두 충족 시 Phase 1 진행
```

### 0-1. CLAUDE.md 작성

프로젝트 루트에 `CLAUDE.md`를 만든다. Claude Code가 매 세션마다 자동으로 읽는 파일이다.

**작성 원칙**:
- Claude가 반복적으로 틀리는 것만 기록한다 — 포괄적인 매뉴얼이 아니다
- 150줄 이하를 유지한다 — 길어지면 Claude가 중요한 규칙을 놓칠 수 있다
- 서브 디렉토리별 추가 CLAUDE.md로 세분화 가능 (예: `/workflows/CLAUDE.md`)

**팁**: `claude /init` 명령으로 Claude가 코드베이스를 스캔해서 CLAUDE.md를 자동 생성할 수 있다. 이후 수동으로 다듬으면 된다.

### 0-2. Claude Code 확장 설정 (선택)

Claude Code는 CLAUDE.md 외에도 Hooks, Skills, Subagents로 확장할 수 있다. 모두 설정할 필요는 없고, 프로젝트에 맞게 선택한다.

**Hooks** — 특정 이벤트 시 자동으로 실행되는 셸 명령. 프롬프트와 달리 100% 실행이 보장된다.

```bash
# Claude에게 Hooks 생성 요청
"파일 수정 후 자동으로 eslint를 실행하는 Hook을 만들어줘"

# 또는 직접 설정
/hooks  # 대화형 설정
```

**Skills** — Claude Code에 도메인 지식을 제공하는 SKILL.md 파일. `.claude/skills/` 디렉토리에 저장한다.

**Subagents** — 별도 컨텍스트에서 독립 작업을 수행하는 특화 에이전트. 코드 리뷰, 문서 생성 등 반복 작업에 유용하다.

**언제 뭘 쓸까**:
- "매번 반드시 실행해야 하는 것" → Hooks
- "Claude가 잘 모르는 도메인 지식" → Skills
- "메인 컨텍스트를 오염시키지 않고 위임할 작업" → Subagents

### 0-3. Task Master 설치 & 모델 설정

```bash
npm install -g task-master-ai
cd your-project
task-master init
```

| 역할 | 용도 | 추천 모델 |
|------|------|----------|
| **Main** | 태스크 생성, 업데이트, 분석 | Claude Sonnet 4.5 또는 GPT-4o |
| **Research** | 최신 정보 조사 (Perplexity 연동) | Perplexity (sonar-pro) |
| **Fallback** | Main 실패 시 대체 | Claude Haiku 4.5 또는 GPT-4o-mini |

### 0-4. MCP 연결

```bash
claude mcp add task-master-ai \
  --env ANTHROPIC_API_KEY="your-key" \
  --env PERPLEXITY_API_KEY="your-key" \
  --env TASK_MASTER_TOOLS="standard" \
  -- npx -y task-master-ai@latest
```

| 모드 | 도구 수 | 토큰 | 추천 대상 |
|------|---------|------|----------|
| core | 7개 | ~6K | 대형 프로젝트, 토큰 절약 |
| standard | 15개 | ~12K | 일반 사용 (권장) |
| all | 36개 | ~21K | 태그, 리서치, metadata 등 전체 기능 필요 시 |

### 산출물

→ CLAUDE.md, Task Master 초기화, MCP 연결 완료

---

## Phase 1~6: 상세 내용

> 이 노트는 핵심 구조와 환경 설정을 담고 있습니다.
> Phase 1~6의 전체 상세 내용(대화 프레임워크, PRD 템플릿, 태스크 분해, 실행 사이클, 테스트/CI/CD, 디버깅, 회고 등)은 로컬 파일 `pipeline-full.md`를 참조하세요.

### Phase 1: 탐색 & 아이디어 구체화
What/Why/Who/Where/When/How를 확정한다. → 게이트: 한 문장씩 정의 완료

### Phase 2: 딥 리서치 → research.md
기술 리서치 → 경쟁 분석 → 리스크 분석 → 교차 검증. → 게이트: 기술 선택 근거 + 비용 추정 완료

### Phase 3: PRD 작성 & 검증
입력/처리/출력/수락 기준을 가진 REQ 단위로 작성. → 게이트: 크로스 체크 완료

### Phase 4: 태스크 분해 & 복잡도 분석
`parse-prd --auto` → 복잡도 분석 → 태그 분리. → 게이트: 의존성 검증 통과

### Phase 5: 반복 실행
Explore → Plan → Implement → Verify → Commit 사이클. 피드백 수준(경미/중간/중대)에 따라 돌아갈 Phase 결정.

### Phase 6: 리뷰 & 회고
PRD 대조 검증 → 프로세스 회고 → Obsidian CMDS 아카이빙 → CLAUDE.md 업데이트.

---

## 피해야 할 안티패턴

| 안티패턴 | 해결 |
|----------|------|
| PRD 없이 바로 코딩 | 최소한 간단한 PRD라도 작성 |
| Plan 없이 구현 요청 | 3파일 이상 수정 시 반드시 Plan 먼저 |
| CLAUDE.md 미작성 / 150줄 초과 | 작성 필수 + 핵심만 유지 |
| /compact 타이밍 잘못 | 세션 50% 시점에서 수동 /compact |
| 한 세션에서 전부 | 태스크당 새 세션 또는 /clear |
| 리서치 건너뛰기 | Phase 2를 충실히 수행 |

---

## 참고

- 소형 프로젝트 가이드: **[[AI 소형 프로젝트 빠른 가이드 (pipeline-quick)]]**
- CLAUDE.md 템플릿: **[[CLAUDE-template]]**
- [Claude Code 공식 Best Practices](https://code.claude.com/docs/en/best-practices)
- [Claude Code Subagents 문서](https://code.claude.com/docs/en/sub-agents)
- [Claude Task Master](https://github.com/eyaltoledano/claude-task-master)
- [Task Master 공식 문서](https://docs.task-master.dev/)
