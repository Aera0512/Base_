---
tags:
  - AI
  - Claude
  - 에이전트
  - 오케스트레이션
  - 자동화
  - 옵시디언
created: '2026-02-25'
type: system-design
related:
  - Claude 실전 워크플로우
  - 프롬프트 엔지니어링 완전 정복 가이드
---

# Research Agent Orchestration — 심층 조사 → 가공 → 저장 → 검토 자동화 시스템

> [!abstract] 시스템 목적
> 학습/연구 자료를 **심층 조사 → 구조화 가공 → 옵시디언 저장 → 자동 검토 → 개선**하는 4-에이전트 팀 오케스트레이션. [[나머지/정리 대기/Claude 실전 워크플로우]]의 서브에이전트 패턴을 실전 시스템으로 확장한 것이다.

---

## 시스템 아키텍처

```
┌─────────────────────────────────────────────────────┐
│                  🎯 Orchestrator                     │
│            (작업 분배 & 품질 게이트)                   │
└─────┬──────────┬──────────┬──────────┬──────────────┘
      │          │          │          │
      ▼          ▼          ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ 🔍       │ │ 📝       │ │ 🗄️       │ │ 🔎       │
│Researcher│→│Processor │→│ Storer   │→│ Reviewer │
│심층 조사  │ │구조화 가공│ │옵시디언   │ │품질 검토  │
│          │ │          │ │저장      │ │& 개선    │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
      ▲                                      │
      └──────── 개선 필요 시 재조사 ────────────┘
```

### 에이전트별 역할 정의

**1. Researcher (심층 조사 에이전트)**
- 역할: 주어진 주제에 대해 다각도로 심층 조사
- 전략: Step-Back → 넓은 탐색 → 핵심 집중 → 상충 정보 교차 검증
- 출력: 구조화된 원시 조사 데이터 (출처 포함)

**2. Processor (가공 에이전트)**
- 역할: 원시 데이터를 옵시디언 노트 형식으로 가공
- 전략: 피라미드 구조, 핵심 우선, Zettelkasten 원칙 적용
- 출력: frontmatter + 본문 + 내부 링크 + 태그가 완비된 마크다운

**3. Storer (저장 에이전트)**
- 역할: 가공된 노트를 옵시디언 볼트의 적절한 위치에 저장
- 전략: 기존 볼트 구조 분석 → 최적 경로 결정 → 관련 노트 링크
- 출력: 옵시디언에 저장된 노트 + 양방향 링크

**4. Reviewer (검토 에이전트)**
- 역할: 저장된 노트의 품질을 평가하고 개선점 제시
- 전략: 6가지 품질 기준 (정확성, 완성도, 구조, 연결성, 실용성, 출처) 평가
- 출력: 품질 점수 (1-10) + 구체적 개선 제안

---

## 실행 흐름 (Flow)

### Phase 1: 조사 계획 수립
```
Orchestrator:
  1. 사용자 입력에서 핵심 주제와 범위 파악
  2. Step-Back: "이 주제를 이해하려면 먼저 무엇을 알아야 하는가?"
  3. 조사 계획 수립 (핵심 질문 3-5개)
  4. Researcher에게 전달
```

### Phase 2: 심층 조사
```
Researcher:
  1. 핵심 질문별 웹 서치 (최소 3개 소스)
  2. 상충 정보 교차 검증
  3. "확실한 것 / 가능성 높은 것 / 추가 확인 필요" 분류
  4. 출처와 함께 구조화된 데이터 반환
```

### Phase 3: 가공 및 저장
```
Processor:
  1. 조사 결과를 옵시디언 노트 구조로 변환
  2. frontmatter 생성 (tags, created, type, related, source)
  3. 핵심 요약 → 상세 분석 → 실전 적용 → 출처 순서
  4. 기존 노트와의 링크 포인트 식별

Storer:
  1. 볼트 구조 분석하여 최적 저장 경로 결정
  2. 노트 저장
  3. 관련 기존 노트에 역방향 링크 추가 (선택적)
```

### Phase 4: 품질 검토 & 개선
```
Reviewer:
  1. 6가지 기준으로 평가:
     - 정확성: 사실 관계가 맞는가? (출처 대조)
     - 완성도: 핵심 질문에 모두 답했는가?
     - 구조: 정보 계층이 논리적인가?
     - 연결성: 다른 지식과 어떻게 연결되는가?
     - 실용성: 내가 이걸 보고 실제로 활용할 수 있는가?
     - 출처: 신뢰할 수 있는 출처가 충분한가?
  
  2. 종합 점수 산출 (1-10)
  
  3. 분기:
     - 8점 이상 → 완료, 최종 저장
     - 6-7점 → Processor에게 개선 지시 (구조/표현 문제)
     - 5점 이하 → Researcher에게 재조사 지시 (내용 부족)
```

---

## 옵시디언 노트 템플릿

### 생성되는 노트 구조
```yaml
---
tags: [주제태그1, 주제태그2, 분류태그]
created: 2026-02-25
type: research  # research | concept | guide | reference
source: [출처 URL 목록]
quality_score: 8
reviewed: true
related: [관련 노트1, 관련 노트2]
---
```

```markdown
# [주제 제목]

> [!abstract] 핵심 요약
> [3-5줄 핵심 요약 — 이것만 읽어도 주제를 파악할 수 있도록]

---

## 핵심 개념

[주제의 핵심을 설명하는 본문]

## 상세 분석

### [하위 주제 1]
[상세 내용]

### [하위 주제 2]
[상세 내용]

## 실전 적용

[이 지식을 실제로 어떻게 활용할 수 있는지]

## 연결 고리

- [[관련 노트 1]] — [어떤 관계인지]
- [[관련 노트 2]] — [어떤 관계인지]

## 추가 탐구 필요

- [ ] [아직 확인하지 못한 것 1]
- [ ] [아직 확인하지 못한 것 2]

## 출처

1. [출처 제목](URL) — [핵심 인용 한 줄]
2. [출처 제목](URL) — [핵심 인용 한 줄]
```

---

## 구현: Python 오케스트레이션 코드 (v2)

> [!info] 구현 방식
> Claude API (Anthropic SDK)를 사용하는 Python 스크립트. 각 에이전트는 독립적인 API 호출로 구현되어 **컨텍스트 분리**가 보장된다.
> 
> **v2 주요 변경:**
> - Brave Search / Tavily 웹 검색 API 실제 연동
> - 옵시디언 Local REST API 직접 연동 (파일시스템 fallback 포함)
> - 관련 노트 검색 → 자동 `[[링크]]` 연결
> - 검색 출처 자동 수집 및 기록
> 
> 코드 파일: `research_orchestration_v2.py`

### 아키텍처 구성요소

```
┌──────────────────────────────────────────────────────────┐
│                  research_orchestration_v2.py              │
├──────────────────────────────────────────────────────────┤
│ SearchEngine (추상)                                       │
│   ├─ BraveSearchEngine   — Brave Search API (월 2,000 무료)│
│   ├─ TavilySearchEngine  — Tavily API (월 1,000 무료)     │
│   └─ FallbackSearchEngine — Claude 내장 지식 기반          │
├──────────────────────────────────────────────────────────┤
│ ObsidianClient                                            │
│   ├─ REST API 모드  — Local REST API 플러그인              │
│   └─ Filesystem 모드 — 직접 파일 읽기/쓰기 (fallback)      │
├──────────────────────────────────────────────────────────┤
│ Agents: Researcher → Processor → Storer → Reviewer        │
│         └─ Improver (품질 미달 시)                         │
├──────────────────────────────────────────────────────────┤
│ Utilities: call_claude, parse_json_response, clean_markdown│
└──────────────────────────────────────────────────────────┘
```

### 환경변수 설정

```bash
# 필수
export ANTHROPIC_API_KEY="sk-ant-..."

# 웹 검색 (둘 중 하나 이상 권장)
export BRAVE_API_KEY="BSA..."      # https://brave.com/search/api/
export TAVILY_API_KEY="tvly-..."   # https://tavily.com/

# 옵시디언 REST API (선택 — 없으면 파일시스템 사용)
export OBSIDIAN_REST_API_KEY="..."  # Local REST API 플러그인 설정에서 확인
```

### 필수 플러그인 (옵시디언)

| 플러그인 | 용도 | 필수 여부 |
|---------|------|----------|
| **Local REST API** | REST API로 노트 읽기/쓰기/검색 | 권장 (없으면 파일시스템 fallback) |

---

## MCP / Skills 리소스 디렉토리

> [!tip] MCP & Skills 찾기
> 아래 리소스에서 추가 MCP 서버와 Skills를 찾아 시스템을 확장할 수 있다.

### MCP (Model Context Protocol) 서버

| 이름 | URL | 설명 |
|------|-----|------|
| **Official MCP Registry** | modelcontextprotocol.io | Anthropic 공식 MCP 서버 목록 |
| **awesome-mcp-servers** | github.com/punkpeye/awesome-mcp-servers | 커뮤니티 최대 MCP 목록 (6k+ stars) |
| **PulseMCP** | pulsemcp.com | MCP 서버 검색/디렉토리 |
| **MCP.so** | mcp.so | MCP 서버 마켓플레이스 |
| **Smithery** | smithery.ai | MCP 서버 레지스트리 |

### 이 시스템에 유용한 MCP 서버들

| MCP 서버 | 용도 | 연동 상태 |
|----------|------|----------|
| **Brave Search** | 웹 검색 (월 2,000 무료) | ✅ v2 직접 API 연동 |
| **Tavily** | AI 에이전트 최적화 검색 (월 1,000 무료) | ✅ v2 직접 API 연동 |
| **Obsidian MCP** | 옵시디언 볼트 접근 | ✅ REST API 연동 |
| **mcp-omnisearch** | 멀티 검색 엔진 통합 | 🔲 확장 후보 |
| **Exa Search** | 의미 기반 검색 | 🔲 확장 후보 |

### Claude Code Skills 리소스

| 이름 | URL | 설명 |
|------|-----|------|
| **Skills Directory** | claude.com/skills | 공식 Skills 탐색 |
| **claude-skill-registry** | GitHub | 커뮤니티 스킬 레지스트리 |
| **awesome-claude-skills** | GitHub | 스킬 큐레이션 목록 |

---

## 사용법

### 기본 실행
```bash
python research_orchestration_v2.py "프롬프트 엔지니어링의 최신 트렌드" --depth deep
```

### 옵션
```
--depth          조사 깊이: quick (빠른 요약) | standard (기본) | deep (심층)
--vault          옵시디언 볼트 경로 (기본: ~/Desktop/Base_)
--folder         저장할 폴더 (기본: Inbox)
--search-engine  검색 엔진: auto (자동 선택) | brave | tavily
--no-review      자동 검토 비활성화
--max-improve    개선 루프 최대 횟수 (기본: 2)
--model          기본 에이전트 모델 (기본: claude-sonnet-4-5)
--reviewer-model 검토 에이전트 모델 (기본: claude-opus-4-6)
```

### Cowork 모드에서 직접 실행
이 오케스트레이션은 Cowork에서도 수동으로 실행할 수 있다:
1. 조사할 주제를 Claude에게 전달
2. "심층 조사 → 옵시디언 저장 → 검토 개선 오케스트레이션을 실행해줘"
3. Claude가 각 에이전트 역할을 순차적으로 수행

---

## 실전 사용 시나리오

### 시나리오 1: 빠른 개념 정리
```bash
python research_orchestration_v2.py "Zettelkasten 방법론" --depth quick --no-review
```
→ 3-5분 내 핵심 개념 노트 생성, 검토 없이 빠르게 저장

### 시나리오 2: 학습 자료 심층 정리
```bash
python research_orchestration_v2.py "트랜스포머 아키텍처의 어텐션 메커니즘" --depth deep
```
→ 심층 조사 + 자동 검토 2회 + 8점 이상 될 때까지 개선

### 시나리오 3: 특정 폴더에 분류 저장
```bash
python research_orchestration_v2.py "RAG 파이프라인 설계 패턴" --depth deep --folder "AI/Research" --search-engine tavily
```
→ 볼트 내 AI/Research 폴더에 저장 (없으면 자동 생성)

### 시나리오 4: Cowork 모드에서 직접 실행
Cowork에서 이 오케스트레이션을 수동으로도 활용할 수 있다:
```
"에이전트 오케스트레이션 방식으로 [주제]에 대해 
심층 조사하고 옵시디언에 저장해줘.
조사 → 가공 → 저장 → 검토 → 개선 순서로 진행해줘."
```

### 확장 로드맵

**Phase 1 ✅ (완료)**: Claude API 기반 독립 실행 스크립트
- ✅ 4-에이전트 팀 오케스트레이션
- ✅ 자동 품질 검토 루프
- ✅ 옵시디언 직접 저장

**Phase 2 ✅ (v2 완료)**: 웹 검색 & MCP 연동
- ✅ Brave Search API 연동 (월 2,000회 무료)
- ✅ Tavily Search API 연동 (월 1,000회 무료, AI 에이전트 최적화)
- ✅ 옵시디언 Local REST API 연동 (파일시스템 fallback 포함)
- ✅ 관련 노트 자동 검색 → `[[링크]]` 연결
- ✅ 검색 출처 자동 수집/기록

**Phase 3 (추후)**: n8n 자동화 연동
- Webhook으로 주제 입력 → 자동 실행
- 스케줄링 (매주 특정 주제 자동 조사)
- Slack/Telegram 알림 연동

**Phase 4 (추후)**: 지식 그래프 자동화
- 옵시디언 그래프 분석 → 빈 연결 자동 탐지
- 관련 주제 자동 추천 → 연쇄 조사
- Exa/Omnisearch MCP 연동으로 의미 기반 검색 확장

---

## 설계 원칙 ([[나머지/정리 대기/Claude 실전 워크플로우]] 기반)

1. **컨텍스트 분리**: 각 에이전트가 독립 컨텍스트에서 작업 → 메인 컨텍스트 보호
2. **품질 게이트**: Reviewer가 기준 미달 시 루프백 → 자동 품질 보장
3. **점진적 개선**: 최대 2회 개선 루프 후 강제 종료 → 무한 루프 방지
4. **자산화**: 모든 결과가 옵시디언에 구조화되어 저장 → 지식 축적
5. **컨텍스트 경제학**: 각 에이전트에 필요한 최소한의 정보만 전달
