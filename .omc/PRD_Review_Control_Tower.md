# PRD: 복습 관제탑 (Review Control Tower)

**Version**: 1.0
**Status**: Draft
**Last Updated**: 2026-03-19
**Owner**: Product Manager (Athena)
**Target Release**: Phase 1 (MVP)

---

## 1. Executive Summary

복습 관제탑은 Obsidian 학습 노트의 복습 스케줄을 자동 관리하고 추적하는 로컬 웹 대시보드입니다. Spaced Repetition 알고리즘을 기반으로 3,600개 이상의 노트 중 복습이 필요한 노트를 자동으로 식별하고, 원클릭 복습 완료 기록을 통해 학습 지속성을 지원합니다.

**Core Value Proposition**: "오늘 뭘 복습해야 하는지" 고민하는 시간을 0으로 만들고, 복습 기록을 자동화하여 학습 지속성을 높입니다.

**Key Metrics**:
- 일일 복습 완료율 80% 달성 (현재 수동 관리 시 ~30% 추정)
- 복습 관리 오버헤드 5분/일 → 30초/일로 단축
- 밀린 복습 수 0개 유지

---

## 2. Problem Statement

### Current Situation
학습자는 YouTube 강의, 책, 개념 노트를 Obsidian에 작성하지만, 복습 스케줄을 수동으로 관리하거나 Anki에 의존하고 있습니다. 복습이 밀리면 어떤 노트부터 복습해야 할지 파악하기 어렵고, 복습 완료 후 frontmatter를 수동으로 업데이트하는 것은 번거롭고 오류가 발생하기 쉽습니다.

### User Persona
**Name**: 시스템 학습자 (Systematic Learner)
**Role**: 지식 노동자, 개발자, 평생 학습자
**Characteristics**:
- Obsidian에 학습 노트를 체계적으로 작성
- Spaced Repetition의 가치를 이해하지만 실천이 어려움
- 복습 관리에 소비하는 시간을 최소화하고 싶음
- 모바일에서도 복습 현황을 확인하고 싶음

**Jobs to be Done (JTBD)**:
> "학습 내용을 장기 기억으로 전환하기 위해, 오늘 복습해야 할 노트를 자동으로 파악하고, 복습 완료를 빠르게 기록하며, 복습 진행 상황을 시각적으로 추적하고 싶다."

### Pain Points
1. **Discovery Problem**: 3,600개 노트 중 오늘 복습할 노트를 수동으로 찾는 데 5분+ 소요
2. **Recording Overhead**: 복습 후 frontmatter를 수동으로 편집하는 데 노트당 30초 소요
3. **Visibility Gap**: 밀린 복습 수를 파악하려면 vault 전체를 검색해야 함
4. **Consistency Challenge**: Anki due 카드와 Obsidian 복습 노트를 별도로 확인해야 함

### Value Hypothesis
**IF** 오늘 복습할 노트 목록을 자동으로 제시하고, 원클릭으로 복습 완료를 기록하며, 복습 현황을 시각적으로 표시한다면,
**THEN** 일일 복습 완료율이 30% → 80%로 증가하고, 복습 관리 시간이 5분 → 30초로 단축될 것이다,
**BECAUSE** 인지 부하(어떤 노트를 복습할지 고민)와 기록 마찰(수동 frontmatter 편집)이 제거되기 때문이다.

### Evidence
- **Quantitative**: Obsidian vault에 ~3,600개 노트, 복습 대상 추정 ~30개/일
- **User Feedback**: "밀린 복습이 쌓이면 어디서부터 시작해야 할지 막막함" (사용자 인터뷰)
- **Confidence Level**: **HIGH** (사용자가 직접 요청, 명확한 pain point)

---

## 3. Goals & Non-Goals

### Goals (Phase 1)
1. **Automation**: 복습 대상 노트를 매일 자동으로 식별하고 정렬
2. **Low Friction**: 복습 완료 기록을 2클릭(버튼 + confidence 선택)으로 완료
3. **Visibility**: 복습 현황(오늘 할 일, 밀린 복습, 완료 수)을 한눈에 파악
4. **Reliability**: Obsidian frontmatter 수정 시 데이터 손실 0%
5. **Accessibility**: 모바일 브라우저에서도 사용 가능

### Non-Goals (Explicitly OUT of Scope)
- ❌ Notion 학습 태스크 통합 (Phase 2로 연기)
- ❌ 외부 접근/클라우드 배포 (localhost only)
- ❌ 복습 내용 편집 기능 (Obsidian에서만 편집)
- ❌ 노트 생성/삭제 (Read + Update only)
- ❌ 복습 알림/리마인더 (별도 시스템으로 구현 예정)
- ❌ 복습 히스토리 상세 분석 (Phase 2로 연기)
- ❌ 멀티 유저 지원 (단일 사용자 전용)
- ❌ 복습 노트 필터링/검색 (Phase 1에서는 단순 정렬만)

---

## 4. User Stories

### Epic 1: 복습 계획 확인
**As a** 학습자,
**I want to** 오늘 복습해야 할 노트 목록을 자동으로 확인하고,
**So that** 복습 계획을 세우는 시간을 절약할 수 있다.

- **US-1.1**: 사용자는 대시보드를 열면 오늘 복습 예정 노트 목록을 본다
- **US-1.2**: 사용자는 각 노트의 타입(yt-note/book-note), 복습 단계, 밀린 일수를 본다
- **US-1.3**: 사용자는 밀린 일수 순으로 정렬된 목록을 본다
- **US-1.4**: 사용자는 노트 제목을 클릭하여 Obsidian에서 해당 노트를 연다

### Epic 2: 복습 완료 기록
**As a** 학습자,
**I want to** 복습 완료를 원클릭으로 기록하고,
**So that** frontmatter를 수동으로 편집하는 수고를 덜 수 있다.

- **US-2.1**: 사용자는 "복습 완료" 버튼을 클릭한다
- **US-2.2**: 사용자는 confidence (1-5)를 선택한다
- **US-2.3**: 시스템은 frontmatter를 자동으로 업데이트하고 다음 복습일을 계산한다
- **US-2.4**: 사용자는 완료된 노트가 목록에서 사라지는 것을 본다

### Epic 3: 복습 현황 모니터링
**As a** 학습자,
**I want to** 복습 진행 상황을 시각적으로 추적하고,
**So that** 복습 습관을 유지할 동기를 얻을 수 있다.

- **US-3.1**: 사용자는 총 복습 대상 노트 수를 본다
- **US-3.2**: 사용자는 오늘 복습 완료한 노트 수를 본다
- **US-3.3**: 사용자는 밀린 복습 수를 본다
- **US-3.4**: 사용자는 Anki due 카드 수를 함께 본다

### Epic 4: Anki 통합
**As a** 학습자,
**I want to** Anki due 카드 수를 대시보드에서 확인하고,
**So that** Obsidian 복습과 Anki 복습을 한 곳에서 관리할 수 있다.

- **US-4.1**: 사용자는 Anki가 실행 중일 때 due 카드 수를 본다
- **US-4.2**: 사용자는 Anki가 꺼져 있을 때 "Anki: Offline" 배지를 본다
- **US-4.3**: 시스템은 AnkiConnect 오류 시 gracefully 처리한다

---

## 5. Functional Requirements

### FR-1: 복습 대상 노트 자동 식별
- **FR-1.1**: 시스템은 vault의 모든 노트를 스캔한다
- **FR-1.2**: 시스템은 `type: yt-note | book-note | concept`인 노트만 필터링한다
- **FR-1.3**: 시스템은 `next_review ≤ today` 또는 `review[phase] = null`인 노트를 복습 대상으로 식별한다
- **FR-1.4**: 시스템은 밀린 일수를 계산한다 (`today - next_review`)
- **FR-1.5**: 시스템은 밀린 일수 내림차순으로 정렬한다

### FR-2: Obsidian URI 연동
- **FR-2.1**: 시스템은 각 노트의 Obsidian URI를 생성한다 (`obsidian://open?vault=Base_&file={path}`)
- **FR-2.2**: 사용자가 노트 제목을 클릭하면 Obsidian 앱에서 해당 노트가 열린다

### FR-3: 복습 완료 기록
- **FR-3.1**: 사용자가 "복습 완료" 버튼을 클릭하면 confidence 입력 모달이 표시된다
- **FR-3.2**: 사용자가 confidence (1-5)를 선택하면 시스템은 다음을 수행한다:
  - `review[current_phase] = today's date`
  - `confidence = user input`
  - `review_phase += 1`
  - `next_review = today + (base_interval × confidence_multiplier)`
- **FR-3.3**: 시스템은 frontmatter 업데이트 전 content hash를 검증한다 (Optimistic Locking)
- **FR-3.4**: 시스템은 frontmatter의 다른 필드를 절대 수정하지 않는다

### FR-4: Spaced Repetition 알고리즘
- **FR-4.1**: 시스템은 review_phase에 따라 base_interval을 결정한다:
  - Phase 0 → 1: +1일
  - Phase 1 → 2: +7일
  - Phase 2 → 3: +30일
  - Phase 3+: FSRS 근사 (현재는 +30일 고정)
- **FR-4.2**: 시스템은 confidence에 따라 multiplier를 적용한다:
  - 1: 0.5, 2: 0.75, 3: 1.0, 4: 1.25, 5: 1.5
- **FR-4.3**: 시스템은 `next_interval = base_interval × multiplier`를 계산한다

### FR-5: AnkiConnect 통합
- **FR-5.1**: 시스템은 AnkiConnect (localhost:8765)에 2초 timeout으로 요청한다
- **FR-5.2**: 시스템은 due 카드 수를 조회한다 (`findCards("is:due")`)
- **FR-5.3**: 시스템은 Anki 오프라인 시 에러를 무시하고 "Offline" 상태를 반환한다

### FR-6: 실시간 상태 업데이트
- **FR-6.1**: 프론트엔드는 SWR로 데이터를 캐싱하고 자동 갱신한다
- **FR-6.2**: 복습 완료 후 목록이 즉시 업데이트된다 (optimistic update)
- **FR-6.3**: 백엔드는 watchdog로 vault 변경을 감지하고 캐시를 무효화한다

### FR-7: 반응형 UI
- **FR-7.1**: 대시보드는 모바일 브라우저에서 사용 가능하다 (최소 320px width)
- **FR-7.2**: 카드 레이아웃은 화면 크기에 따라 1열(모바일) ~ 3열(데스크톱)로 조정된다
- **FR-7.3**: 터치 인터랙션을 지원한다

---

## 6. Technical Architecture

### System Overview
```
┌─────────────────┐
│  Next.js 14     │  Frontend (localhost:3000)
│  + SWR          │  - Dashboard UI
│  + shadcn/ui    │  - Review list
│  + Tailwind CSS │  - Completion modal
└────────┬────────┘
         │ HTTP REST API
         │
┌────────▼────────┐
│  FastAPI        │  Backend (localhost:8000)
│  + frontmatter  │  - Vault scanner
│  + watchdog     │  - Frontmatter updater
└────────┬────────┘
         │
    ┌────┼─────────────────┐
    │    │                 │
┌───▼────▼────┐    ┌──────▼──────┐
│ Obsidian    │    │ AnkiConnect │
│ Vault       │    │ (port 8765) │
│ (3,600 MD)  │    └─────────────┘
└─────────────┘
```

### Tech Stack
| Layer | Technology | Rationale |
|-------|------------|-----------|
| Frontend | Next.js 14 (App Router) | React framework with SSR, optimal DX |
| State Management | SWR | Auto-refresh, caching, optimistic updates |
| UI Components | shadcn/ui | Accessible, customizable, Tailwind-native |
| Styling | Tailwind CSS | Utility-first, responsive design |
| Backend | FastAPI | Fast, type-safe, auto-generated API docs |
| Frontmatter Parser | python-frontmatter | Robust YAML frontmatter handling |
| File Watcher | watchdog | Cross-platform file system monitoring |
| HTTP Client | fetch API | Built-in, no dependencies |

### Deployment
- **Frontend**: `npm run dev` on localhost:3000
- **Backend**: `uvicorn main:app --reload` on localhost:8000
- **Dependencies**: Node.js 18+, Python 3.10+, Anki Desktop (optional)
- **Cost**: $0 (no cloud services, no API keys)

---

## 7. API Specification

### Base URL
```
http://localhost:8000/api
```

### Endpoints

#### 1. GET /api/reviews/due
**Description**: 오늘 복습 예정 노트 목록 반환

**Response**:
```json
{
  "notes": [
    {
      "path": "yt-notes/딥러닝 기초.md",
      "title": "딥러닝 기초",
      "type": "yt-note",
      "review_phase": 1,
      "next_review": "2026-03-15",
      "overdue_days": 4,
      "confidence": 3,
      "uri": "obsidian://open?vault=Base_&file=yt-notes%2F딥러닝%20기초.md",
      "content_hash": "a1b2c3d4e5f6"
    }
  ],
  "total_count": 12,
  "overdue_count": 4
}
```

**Query Parameters**:
- `limit` (optional): 최대 결과 수 (기본값: 100)

**Error Codes**:
- `500`: Vault 스캔 실패

---

#### 2. POST /api/reviews/{path}/complete
**Description**: 복습 완료 기록 및 frontmatter 업데이트

**Path Parameters**:
- `path`: URL-encoded 노트 경로 (예: `yt-notes%2F딥러닝%20기초.md`)

**Request Body**:
```json
{
  "confidence": 4,
  "content_hash": "a1b2c3d4e5f6"
}
```

**Response**:
```json
{
  "success": true,
  "updated_fields": {
    "review": ["2026-01-15", "2026-03-19", null],
    "confidence": 4,
    "review_phase": 2,
    "next_review": "2026-04-18"
  },
  "next_review_date": "2026-04-18"
}
```

**Error Codes**:
- `404`: 노트를 찾을 수 없음
- `409`: Content hash 불일치 (Obsidian에서 동시 수정됨)
- `422`: 유효하지 않은 confidence 값 (1-5 범위 외)

---

#### 3. GET /api/anki/due
**Description**: Anki due 카드 수 조회

**Response**:
```json
{
  "due_count": 37,
  "status": "online"
}
```

**Offline Response**:
```json
{
  "due_count": 0,
  "status": "offline"
}
```

**Error Codes**:
- None (gracefully returns offline status)

---

#### 4. GET /api/health
**Description**: 서비스 상태 확인

**Response**:
```json
{
  "status": "healthy",
  "vault_path": "/Users/aera/Desktop/Base_",
  "vault_accessible": true,
  "anki_status": "online",
  "timestamp": "2026-03-19T10:30:00+11:00"
}
```

---

## 8. Data Models

### Frontmatter Schema
```yaml
# Required fields (for review notes)
type: "yt-note" | "book-note" | "concept"

# Review tracking (managed by system)
review: [date|null, date|null, date|null]  # review[0], review[1], review[2]
review_phase: 0 | 1 | 2 | 3                 # Current review stage
next_review: "YYYY-MM-DD" | null            # Next scheduled review date

# User input
confidence: 1 | 2 | 3 | 4 | 5 | null        # Last review confidence
difficulty: 1 | 2 | 3 | 4 | 5               # Intrinsic difficulty (default: 3)

# Other fields (read-only for Review Agent)
# ... (tags, aliases, created, etc. - preserved but never modified)
```

### Review Note Object (Backend)
```python
class ReviewNote:
    path: str                    # Relative path from vault root
    title: str                   # Extracted from frontmatter or filename
    type: Literal["yt-note", "book-note", "concept"]
    review: List[Optional[str]]  # Normalized to 3-element list
    review_phase: int            # 0, 1, 2, 3
    next_review: Optional[str]   # ISO date string
    confidence: Optional[int]    # 1-5
    difficulty: int              # 1-5 (default: 3)
    content_hash: str            # MD5 of full file content
    uri: str                     # Obsidian URI
```

### Spaced Repetition Config
```python
# Base intervals
REVIEW_INTERVALS = {
    0: 1,   # 1 day
    1: 7,   # 7 days
    2: 30,  # 30 days
    3: 30   # 30 days (FSRS placeholder)
}

# Confidence multipliers
CONFIDENCE_MULTIPLIERS = {
    1: 0.5,
    2: 0.75,
    3: 1.0,
    4: 1.25,
    5: 1.5
}
```

---

## 9. UI/UX Requirements

### Layout Structure
```
┌─────────────────────────────────────┐
│  📊 복습 관제탑                      │  Header
├─────────────────────────────────────┤
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐   │
│  │오늘 │ │완료 │ │밀림 │ │Anki │   │  Stats Cards
│  │ 12  │ │ 3   │ │ 4   │ │ 37  │   │
│  └─────┘ └─────┘ └─────┘ └─────┘   │
├─────────────────────────────────────┤
│  📝 오늘의 복습 (12)                 │  Section Title
│                                     │
│  ┌───────────────────────────────┐ │
│  │ 📺 딥러닝 기초              ⏰4d│ │  Review Card
│  │ Phase 1 · Confidence 3        │ │
│  │ [복습 완료] [Open in Obsidian]│ │
│  └───────────────────────────────┘ │
│  ┌───────────────────────────────┐ │
│  │ 📚 클린 코드               ⏰2d│ │
│  │ Phase 2 · Confidence 4        │ │
│  │ [복습 완료] [Open in Obsidian]│ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

### Component Specifications

#### 1. Stats Card
- **Purpose**: 복습 현황을 한눈에 파악
- **Content**:
  - Icon + Label + Number
  - 예: 🎯 오늘 복습: 12
- **States**:
  - Default: 흰색 배경, 회색 테두리
  - Anki Offline: "Offline" 배지 표시
- **Responsive**: 모바일에서 2×2 그리드, 데스크톱에서 4열

#### 2. Review Card
- **Purpose**: 복습 대상 노트 정보 표시 및 액션
- **Content**:
  - Title (클릭 시 Obsidian 열기)
  - Type emoji (📺 yt-note, 📚 book-note, 💡 concept)
  - Phase & Confidence
  - Overdue badge (빨강/주황/회색)
- **Actions**:
  - "복습 완료" 버튼 (primary)
  - "Open in Obsidian" 버튼 (secondary)
- **States**:
  - Default
  - Loading (복습 완료 처리 중)
  - Completed (fade out animation)

#### 3. Confidence Modal
- **Trigger**: "복습 완료" 버튼 클릭
- **Content**:
  - Title: "복습 난이도는 어땠나요?"
  - 5개 버튼: 1 (매우 어려움) ~ 5 (매우 쉬움)
- **Actions**:
  - 버튼 클릭 시 즉시 제출 및 모달 닫기
  - ESC 키로 취소

### Accessibility
- **Keyboard Navigation**: Tab으로 모든 인터랙션 가능
- **ARIA Labels**: 스크린 리더 지원
- **Color Contrast**: WCAG AA 준수 (최소 4.5:1)
- **Touch Targets**: 최소 44×44px

### Loading States
- **Initial Load**: Skeleton UI (shimmer effect)
- **Data Refresh**: 상단에 작은 spinner
- **Action Pending**: 버튼 disabled + spinner

### Error States
- **Network Error**: Toast notification + retry 버튼
- **Conflict Error (409)**: "다른 곳에서 수정됨. 새로고침 후 다시 시도하세요."
- **Empty State**: "🎉 오늘 복습할 노트가 없습니다!"

---

## 10. Success Metrics

### KPI Tree
```
Business Goal: 학습 지속성 향상
  |
  ├─ Leading Indicator: 일일 복습 완료율 ≥ 80%
  |    |
  |    ├─ User Behavior: 일일 대시보드 방문 횟수 ≥ 1회
  |    ├─ User Behavior: 평균 복습 완료 시간 ≤ 30초/노트
  |    └─ User Behavior: 복습 완료 클릭률 ≥ 70%
  |
  ├─ Leading Indicator: 밀린 복습 수 = 0
  |    |
  |    └─ User Behavior: 주간 복습 완료 노트 수 ≥ 목표 수
  |
  └─ Leading Indicator: 복습 관리 오버헤드 ≤ 30초/일
       |
       ├─ System Behavior: 복습 목록 로딩 시간 ≤ 500ms
       └─ System Behavior: Frontmatter 업데이트 성공률 = 100%
```

### Measurement Plan

| Metric | Current | Target | Measurement Method | Frequency |
|--------|---------|--------|-------------------|-----------|
| 일일 복습 완료율 | ~30% | 80% | (완료 수 / due 수) × 100 | 일일 |
| 복습 관리 시간 | 5분 | 30초 | 대시보드 오픈 ~ 마지막 클릭 | 세션별 |
| 밀린 복습 수 | 추정 10+ | 0 | overdue_count API | 일일 |
| Frontmatter 업데이트 성공률 | N/A | 100% | (성공 / 시도) × 100 | 실시간 |
| 대시보드 로딩 시간 | N/A | ≤ 500ms | Performance API | 세션별 |
| AnkiConnect 가용성 | N/A | ≥ 90% | health check API | 실시간 |

### Acceptance Criteria (Launch Readiness)
- [ ] 일일 복습 완료율 ≥ 60% (1주일 평균)
- [ ] Frontmatter 업데이트 성공률 = 100% (데이터 손실 0건)
- [ ] 대시보드 로딩 시간 ≤ 500ms (P95)
- [ ] 모바일 반응형 UI 테스트 통과 (iOS Safari, Android Chrome)
- [ ] Anki 오프라인 시 graceful degradation 확인

---

## 11. Timeline & Milestones

### Phase 1: MVP (Target: 2주)

| Milestone | Deliverables | Timeline | Dependencies |
|-----------|--------------|----------|--------------|
| **M1: Backend API** | - `/api/reviews/due` 구현<br>- `/api/reviews/{path}/complete` 구현<br>- Frontmatter 파싱 및 업데이트 로직<br>- Optimistic locking | Week 1 | Obsidian vault access |
| **M2: Frontend UI** | - Dashboard layout<br>- Review card component<br>- Confidence modal<br>- SWR integration | Week 1 | M1 API endpoints |
| **M3: Anki Integration** | - `/api/anki/due` 구현<br>- AnkiConnect 연동<br>- Offline handling | Week 2 | AnkiConnect installed |
| **M4: Testing & Polish** | - E2E 테스트<br>- 모바일 반응형 테스트<br>- 에러 핸들링 검증 | Week 2 | M1, M2, M3 |
| **M5: Launch** | - Production deployment<br>- User onboarding guide<br>- 1주일 모니터링 | Week 2 | M4 |

### Development Sequence
1. **Day 1-2**: Backend - Vault scanner, frontmatter parser, review algorithm
2. **Day 3-4**: Backend - API endpoints, optimistic locking, error handling
3. **Day 5-6**: Frontend - Dashboard layout, stats cards, review list
4. **Day 7-8**: Frontend - Confidence modal, Obsidian URI integration, SWR
5. **Day 9-10**: Integration - AnkiConnect, health check, E2E testing
6. **Day 11-12**: Polish - Responsive design, loading states, error states
7. **Day 13-14**: Testing & Launch - User testing, bug fixes, deployment

---

## 12. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation Strategy | Owner |
|------|------------|--------|---------------------|-------|
| **Concurrent Modification** (Obsidian + FastAPI 동시 수정) | HIGH | HIGH | Optimistic locking with content hash. 409 Conflict 시 사용자에게 새로고침 안내. | Backend Dev |
| **Frontmatter Corruption** (잘못된 YAML 파싱) | MEDIUM | CRITICAL | `python-frontmatter` 라이브러리 사용. 업데이트 전 백업 생성 (optional). 허용 필드 whitelist 엄격 적용. | Backend Dev |
| **AnkiConnect Downtime** | HIGH | LOW | 2초 timeout + try/except. "Offline" 상태로 graceful degradation. | Backend Dev |
| **Large Vault Performance** (3,600+ 노트 스캔) | MEDIUM | MEDIUM | 파일 시스템 캐싱 + watchdog로 변경 감지. 첫 스캔 후 증분 업데이트. | Backend Dev |
| **Review Array Edge Cases** (다양한 형식) | MEDIUM | MEDIUM | `normalize_review_array()` 함수로 모든 형식 처리 (null, [], 문자열 등). | Backend Dev |
| **Mobile Browser Compatibility** | LOW | MEDIUM | iOS Safari, Android Chrome 명시적 테스트. Tailwind responsive utilities 사용. | Frontend Dev |
| **User Drops Off** (복잡한 UI) | LOW | HIGH | 초기 사용자 테스팅 (5명+). 1클릭 복습 완료 UX 우선. | Product Manager |

### Assumptions Requiring Validation

| Assumption | Validation Method | Confidence |
|------------|-------------------|------------|
| 사용자는 매일 대시보드를 방문한다 | 1주일 사용 로그 분석 | MEDIUM |
| Confidence 입력이 부담스럽지 않다 | 사용자 피드백 수집 | MEDIUM |
| 밀린 일수 정렬이 최적의 우선순위다 | A/B 테스트 (밀린 일수 vs phase) | LOW |
| Obsidian URI가 모바일에서도 작동한다 | iOS/Android 실기기 테스트 | HIGH |

---

## 13. Future Considerations (Phase 2+)

### Deferred Features
1. **Notion 학습 태스크 통합**
   - Notion API로 "해야할일" DB의 학습 태스크 조회
   - Obsidian 복습 + Notion 태스크를 단일 뷰로 통합
   - Estimated Effort: 1주일

2. **복습 히스토리 상세 분석**
   - 주간/월간 복습 완료 트렌드 차트
   - Confidence 평균 추이
   - 가장 어려운 노트 top 10
   - Estimated Effort: 3일

3. **고급 Spaced Repetition 알고리즘**
   - FSRS (Free Spaced Repetition Scheduler) 완전 구현
   - Difficulty 자동 조정
   - Estimated Effort: 1주일

4. **복습 알림 시스템**
   - macOS Notification Center 통합
   - 모바일 푸시 알림 (Pushover/Telegram)
   - Estimated Effort: 3일

5. **노트 필터링/검색**
   - 타입별 필터 (yt-note/book-note/concept)
   - Phase별 필터
   - 키워드 검색
   - Estimated Effort: 2일

### Scalability Considerations
- **Vault Size**: 10,000+ 노트로 확장 시 인덱싱 최적화 필요
- **Multi-User**: 가족 공유 시나리오 (별도 vault 지원)
- **Cloud Sync**: iCloud/Dropbox와의 충돌 방지 메커니즘

### Technical Debt Prevention
- API versioning (`/api/v1/reviews/due`)
- Database migration strategy (현재는 frontmatter만 사용)
- Logging and monitoring (Sentry, Prometheus)

---

## Appendix A: Open Questions

1. **Q**: Confidence 입력 없이 복습 완료를 허용할 것인가?
   **A**: Phase 1에서는 필수 입력. Phase 2에서 "빠른 완료" 옵션 검토.

2. **Q**: Review phase 3 이후 간격을 어떻게 늘릴 것인가?
   **A**: Phase 1에서는 고정 30일. Phase 2에서 FSRS 구현.

3. **Q**: Obsidian vault가 iCloud에 있을 때 동기화 충돌을 어떻게 처리할 것인가?
   **A**: Content hash로 감지 후 409 Conflict 반환. 사용자가 수동 해결.

4. **Q**: 복습 완료 후 Obsidian에서 노트를 자동으로 열 것인가?
   **A**: Phase 1에서는 수동 클릭. Phase 2에서 "복습 후 자동 열기" 옵션 검토.

---

## Appendix B: Design System References

### Color Palette
| Purpose | Color | Hex |
|---------|-------|-----|
| Primary | Blue | #3B82F6 |
| Success | Green | #10B981 |
| Warning | Orange | #F59E0B |
| Danger | Red | #EF4444 |
| Neutral | Gray | #6B7280 |

### Typography
- **Font Family**: Inter (sans-serif)
- **Sizes**: 12px (caption), 14px (body), 16px (heading), 24px (title)

### Spacing Scale
- **4px**: XS (gap)
- **8px**: SM (padding)
- **16px**: MD (margin)
- **24px**: LG (section gap)

---

**Document Status**: ✅ Ready for Review
**Next Steps**:
1. Technical feasibility review with `architect` (Oracle)
2. Requirements gap analysis with `analyst` (Metis)
3. Implementation planning with `planner` (Prometheus)
