---
tags:
  - project
  - writing-coach-web
  - prd
  - web-app
created: '2026-03-19'
version: '0.3'
aliases:
  - Writing Coach Web PRD
pipeline: pipeline-full
phase: 3-PRD
---
# Writing Coach Web PRD

> **프로젝트명**: Writing Coach Web — 영어 글쓰기 코치 웹앱
>
> **목적**: 기존 Writing Coach 스킬의 핵심 기능(3라운드 교정 + 역번역 + L1 간섭 추적)을 브라우저에서 독립 실행할 수 있는 웹앱으로 구현한다. 터미널 없이 브라우저만으로 글쓰기 연습이 가능하게 한다.
>
> **아키텍처**: Vanilla HTML/Tailwind/JS + Vercel Serverless (Claude API 프록시)
>
> **파이프라인**: pipeline-full (중형)
>
> **최종 수정**: 2026-03-19 | 버전: 0.1

---

## 1. 문제 정의 & 근거

### 해결하려는 문제

기존 Writing Coach 스킬은 Claude Code/Cowork 터미널에서만 사용 가능하다. 이로 인해:

- **접근성**: 터미널을 열고, 스킬을 트리거하고, 텍스트를 복붙하는 과정이 번거로움
- **시각적 피드백**: 터미널에서는 인라인 하이라이트, 색상 코딩, 비교 테이블 등 시각적 피드백이 제한적
- **세션 연속성**: 터미널 세션이 닫히면 컨텍스트가 사라짐. 에세이 초안과 피드백 이력을 별도로 관리해야 함
- **즉시성**: 글쓰기 연습을 하고 싶을 때 브라우저만 열면 바로 시작할 수 있어야 함

### 핵심 가치

터미널 기반 스킬의 교육학적 설계(3라운드 교정, L1 간섭 추적, 역번역)를 그대로 유지하면서, 웹 인터페이스의 시각적 장점을 활용하여 학습 경험을 향상시킨다.

---

## 2. 목표 & 성공 지표

### 핵심 목표

- 브라우저에서 바로 글쓰기 연습 시작 가능 (터미널 불필요)
- 기존 스킬의 2가지 모드(자유 글쓰기 + 역번역) 완전 구현
- 오류 프로필의 시각적 대시보드 (추이 그래프, 패턴 분석)
- 세션 데이터 브라우저에 영속 저장 (LocalStorage)

### 성공 지표

| 지표 | 목표 | 측정 방법 |
|------|------|----------|
| 세션 시작까지 시간 | 5초 이내 (페이지 로드 → 모드 선택) | 타이머 측정 |
| 전체 워크플로우 완료 | Mode A 8 Phase, Mode B 6 Phase 정상 완료 | 기능 테스트 |
| 피드백 응답 시간 | Claude API 응답 10초 이내 (스트리밍 시작) | API latency 측정 |
| 오류 프로필 영속성 | 브라우저 재시작 후에도 데이터 유지 | LocalStorage 검증 |
| 모바일 대응 | 태블릿 이상에서 사용 가능 | 반응형 테스트 |

---

## 3. 범위 & 트레이드오프

### 범위 안 (v1)

- Mode A (자유 글쓰기): 주제 선정 → 어휘 제공 → 에세이 작성 → 3라운드 교정 → 세션 저장
- Mode B (역번역): 모범문 제공 → 한국어 번역 → 영작 → 가이디드 비교 → 세션 저장
- L1 간섭 6유형 분류 + 태깅 (L1-1 ~ L1-6)
- 오류 프로필 대시보드 (누적 오류, 추세, 포커스 영역)
- LocalStorage 기반 데이터 저장 (에세이, 피드백, 오류 프로필)
- Claude API 스트리밍 응답
- Vercel 배포 (무료 티어)

### 범위 밖 (v2 이후)

- Mode B (역번역 연습) — v2에서 별도 스프린트
- 대시보드 추세 차트 (Chart.js) — v1은 숫자 요약만
- 반응형 모바일 레이아웃 — v1은 데스크탑 우선
- Anki 연동 (CORS 제약) — 내보내기 기능만 v1
- Obsidian 연동
- 사용자 인증/로그인 (개인용)
- 오프라인 모드

### 핵심 가정

- 사용자 1명 (개인용)
- Anthropic API 키 보유
- 인터넷 연결 필수 (Claude API 호출)
- 데스크탑/태블릿 브라우저 사용 (모바일 폰은 보조)

### 기술적 제약

- Claude API는 브라우저에서 직접 호출 불가 (CORS) → Vercel Serverless Function으로 프록시
- LocalStorage 5MB 제한 → 에세이 100+ 세션 충분히 수용 가능 (세션당 ~10KB)
- Vercel 무료 티어: 100GB 대역폭/월, serverless function 100GB-hours/월

---

## 4. 기술 스택

| 구성요소 | 선택 | 이유 |
|---------|------|------|
| 프론트엔드 | Vanilla HTML + Tailwind CSS + JS | 빌드 불필요, 의존성 최소, 개인용에 최적 |
| 백엔드 | Vercel Serverless Functions (Node.js) | Claude API 키 보호, 무료, 배포 간편 |
| AI | Claude API (claude-sonnet-4-6) | 교정 품질 최적, 스트리밍 지원 |
| 저장 | LocalStorage (JSON) | 개인용, 5MB 충분, 별도 DB 불필요 |
| 스타일링 | Tailwind CSS (CDN) | 빌드 불필요, 유틸리티 클래스 |
| 배포 | Vercel | 무료, Git 연동, env 변수로 API 키 관리 |
| 코드 관리 | GitHub private repo | 버전 관리 + Vercel 자동 배포 |
| JSON 검증 | zod (런타임 스키마 검증) | Claude 응답 파싱 안정성 보장 |
| 차트 | Chart.js (CDN) | 대시보드 오류 추세 그래프 |

### 프로젝트 구조

```
writing-coach-web/
├── index.html                 # 메인 SPA
├── css/
│   └── custom.css             # Tailwind 보완 커스텀 스타일
├── js/
│   ├── app.js                 # 앱 라우팅 + 상태 관리
│   ├── api.js                 # Claude API 호출 (fetch → /api/chat)
│   ├── storage.js             # LocalStorage CRUD
│   ├── ui.js                  # UI 렌더링 헬퍼
│   ├── mode-a.js              # 자유 글쓰기 모드 로직
│   ├── mode-b.js              # 역번역 모드 로직
│   └── dashboard.js           # 오류 프로필 대시보드
├── api/
│   └── chat.js                # Vercel Serverless Function (Claude 프록시)
├── prompts/
│   ├── system-mode-a.md       # Mode A 시스템 프롬프트
│   └── system-mode-b.md       # Mode B 시스템 프롬프트
├── .env.local                 # ANTHROPIC_API_KEY (gitignore)
├── vercel.json                # Vercel 설정
└── package.json               # 최소 의존성 (anthropic SDK만)
```

---

## 5. 기능 요구사항

### REQ-W1: 메인 화면 + 모드 선택

**처리**:
- 앱 로드 시 오류 프로필 존재 여부 확인 (LocalStorage)
- 첫 방문: 환영 메시지 + 워크플로우 설명
- 재방문: 오류 프로필 요약 + 포커스 영역 표시
- 모드 선택: "자유 글쓰기" / "역번역 연습" / "대시보드" 3버튼

**수락 기준**:
- Given 앱이 로드되었을 때
- When 메인 화면이 표시되면
- Then 5초 이내에 모드 선택이 가능하고, 이전 오류 프로필이 있으면 요약이 표시됨

### REQ-W2: 자유 글쓰기 모드 (Mode A)

기존 스킬의 Phase B~H를 웹 UI로 구현. 각 Phase가 화면 전환(또는 섹션 확장)으로 진행.

**Phase B (주제 선정)**:
- AI 추천 주제 2-3개 표시 (버튼) + 직접 입력 필드
- 주제 선택 시 다음 Phase로

**Phase C (어휘 제공)**:
- Claude API 호출하여 3카테고리 어휘 생성
- 카드 형태로 표시 (단어, 발음, 뜻, 예문)
- "이 어휘로 시작" 버튼

**Phase D (에세이 작성)**:
- 큰 텍스트 에디터 (textarea)
- 실시간 단어 수 카운트
- 제공 어휘가 사이드바에 표시 (참고용)
- "제출" 버튼

**Phase E (Round 1: 문법)**:
- Claude API 호출 (시스템 프롬프트에 L1 분류 체계 포함)
- 응답을 파싱하여 오류별 카드로 표시
- 각 오류: 원문(빨간 하이라이트) → 교정(초록 하이라이트) + 유형 태그 + 설명
- L1 태그는 시각적으로 구분 (별도 뱃지)
- "수정 후 재제출" 버튼 → 에디터로 돌아감

**Phase F (Round 2: 구조)**:
- Claude API 호출 (구조/명확성 초점)
- 글 전체 구조 평가 + 단락별 피드백 카드
- "수정 후 재제출" 버튼

**Phase G (Round 3: 스타일 + 4레벨 비교)**:
- Claude API 호출 (스타일 + 리라이트)
- 스타일 피드백 + 4레벨 탭 (A2-B1 / B1-B2 / B2-C1 / C1-C2)
- 각 레벨 탭 클릭 시 해당 수준의 리라이트 표시

**Phase H (마무리)**:
- 오류 프로필 자동 업데이트 (LocalStorage)
- 세션 요약: 오류 유형별 집계 + 개선 포인트
- "새 세션 시작" / "대시보드" 버튼

**수락 기준**:
- Given 사용자가 Mode A를 선택했을 때
- When Phase B~H를 순서대로 진행하면
- Then 각 Phase에서 Claude API 응답이 구조화된 UI로 표시되고, 에세이와 피드백 전체가 LocalStorage에 저장됨

### REQ-W3: 역번역 모드 (Mode B)

**Phase B2 (모범문 선정)**:
- Claude API로 주제+수준에 맞는 모범문 생성 (100-200 단어)
- 모범문 미리보기는 보여주지 않음

**Phase C2 (한국어 번역 제공)**:
- 한국어 번역만 화면에 표시
- 원문은 숨김 (JS로 저장만, 표시 안 함)
- "읽었으면 영작 시작" 버튼

**Phase D2 (영작)**:
- 왼쪽: 한국어 번역 (읽기 전용)
- 오른쪽: 영작 에디터
- 단어 수 카운트

**Phase E2 (가이디드 비교)**:
- 원문 공개
- 3카테고리 비교 테이블 (구문/어휘/연결)
- 사이드바이사이드 뷰: 내 글 vs 원문
- 차이점 하이라이트

**Phase H2 (마무리)**:
- "배운 표현 TOP 3" 카드
- 오류 프로필 업데이트
- 세션 저장

### REQ-W4: 오류 프로필 대시보드

- L1 오류 유형별 누적 횟수 바 차트
- 최근 5세션 추세 라인 차트 (각 오류 유형별)
- 현재 포커스 영역 강조 표시
- 세션 히스토리 리스트 (날짜, 주제, 모드, 오류 수)
- 세션 클릭 시 상세 보기 (에세이 원문 + 피드백)

**수락 기준**:
- Given 3회 이상의 세션 데이터가 있을 때
- When 대시보드를 열면
- Then 오류 추세 그래프 + 포커스 영역 + 세션 히스토리가 표시됨

### REQ-W5: Claude API 프록시 (Serverless Function)

**엔드포인트**: POST /api/chat

**인증**:
- Vercel 환경 변수에 APP_SECRET 설정
- 프론트엔드가 요청 시 Authorization: Bearer {APP_SECRET} 헤더 포함
- Serverless Function에서 헤더 검증 후 진행
- CORS: Access-Control-Allow-Origin을 배포 도메인으로 제한

**요청 형식**:
```json
{
  "messages": [{"role": "user", "content": "..."}],
  "mode": "a",
  "phase": "E"
}
```

**처리**:
- mode와 phase에 따라 서버 측에서 시스템 프롬프트 선택 (클라이언트가 아닌 서버에서 관리)
- Claude API 호출 (claude-sonnet-4-6, stream: true)
- SSE로 스트리밍 응답 반환

**스트리밍 전략**:
- 전체 응답을 받은 후 JSON 파싱하여 반환 (스트리밍은 Claude ↔ 서버 간에만)
- 서버 → 클라이언트: 완성된 JSON 응답 1회 전송
- 이유: JSON 구조화 응답을 스트리밍 중간에 파싱하면 불안정. 서버에서 전체 수집 후 검증하여 전송하는 것이 안정적
- 클라이언트에서는 로딩 인디케이터 표시 (10-20초 예상)

**JSON 응답 검증**:
- 서버에서 Claude 응답을 JSON.parse 후 zod 스키마로 검증
- 검증 실패 시: { "error": "parsing_failed", "rawText": "..." } 반환 → 프론트엔드에서 마크다운으로 폴백 표시
- 검증 성공 시: 구조화된 JSON 반환

**시스템 프롬프트 관리**:
- 시스템 프롬프트는 서버 측 prompts/ 폴더에 저장 (클라이언트에 노출 안 됨)
- Mode A 각 Phase별 시스템 프롬프트 (L1 분류 체계, JSON 출력 스키마 포함)
- Mode B 각 Phase별 시스템 프롬프트 (모범문 기준, 비교 테이블 JSON 스키마 포함)

**대화 컨텍스트 관리**:
- 각 Phase에서 Claude에 보내는 내용은 선택적 컨텍스트:
  - Phase E (Round 1): 시스템 프롬프트 + 에세이 원문
  - Phase F (Round 2): 시스템 프롬프트 + 수정된 에세이 + "Round 1에서 발견된 L1 오류 유형 요약" (전체 피드백 아님)
  - Phase G (Round 3): 시스템 프롬프트 + 최종 수정 에세이 + "Round 1-2 오류 요약" (한 줄씩)
- 전체 피드백 이력은 LocalStorage에만 저장 (사용자 참조용)
- 이유: 토큰 절약 + 각 라운드 독립성 유지

**오류 프로필 집계 규칙**:
- Round 1에서 발견된 원본 오류 수를 기록 (수정 여부와 무관)
- 이유: "이 유형의 오류를 얼마나 자주 하는가"를 추적하는 것이 목적

**에러 처리**:
- Claude API 타임아웃 (45초): 504 반환 + "응답 시간 초과. 다시 시도해주세요."
- Claude API 5xx: 502 반환 + 재시도 버튼
- 인증 실패: 401 반환
- 최대 재시도: 3회 (exponential backoff: 2s → 4s → 8s)

**수락 기준**:
- Given 유효한 API 키와 APP_SECRET이 환경 변수에 설정되어 있을 때
- When 프론트엔드에서 /api/chat을 호출하면
- Then 인증 검증 → Claude 호출 → JSON 검증 → 구조화된 응답 반환. API 키와 시스템 프롬프트가 클라이언트에 노출되지 않음

### REQ-W6: 세션 상태 관리 + 페이지 새로고침 복구

**세션 상태 객체**:
```json
{
  "sessionId": "260319-social-media",
  "mode": "a",
  "currentPhase": "E",
  "topic": "Social Media Impact",
  "vocabulary": [...],
  "essays": {
    "original": "...",
    "afterRound1": null,
    "afterRound2": null,
    "final": null
  },
  "feedback": {
    "round1": null,
    "round2": null,
    "round3": null
  },
  "conversationHistory": [...]
}
```

**상태 관리 규칙**:
- 매 Phase 전환 시 LocalStorage에 currentSession 자동 저장
- 페이지 새로고침/닫기 시: 현재 세션 상태가 유지됨
- 앱 재로드 시: currentSession이 존재하면 복구 UI 표시 — "진행 중인 세션이 있습니다: Social Media (Round 1 교정 중). 이어하기 / 새 세션 시작"
- Phase 가드: Phase F 진입은 Phase E 완료 + 사용자 수정본 제출이 필요

**수락 기준**:
- Given Phase E 진행 중 페이지가 새로고침되었을 때
- When 앱이 다시 로드되면
- Then 복구 UI가 표시되고, "이어하기" 선택 시 Phase E의 피드백과 에세이가 복원됨

### REQ-W7: 데이터 저장 (LocalStorage)

**저장 구조**:
```json
{
  "errorProfile": {
    "totalSessions": 12,
    "l1Errors": { "articles": { "count": 23, "last5": [5,4,3,3,2] }, ... },
    "focusAreas": ["articles", "preposition"]
  },
  "sessions": [
    {
      "id": "260319-social-media",
      "date": "2026-03-19",
      "mode": "free-writing",
      "topic": "Social Media Impact",
      "essays": { "original": "...", "r1": "...", "r2": "...", "final": "..." },
      "feedback": { "round1": "...", "round2": "...", "round3": "..." },
      "errors": { "articles": 3, "tense": 2 }
    }
  ],
  "settings": {
    "apiKey": null  // 키는 Vercel env에만 저장, 브라우저에는 저장 안 함
  }
}
```

**수락 기준**:
- Given 세션이 완료되었을 때
- When LocalStorage에 저장되면
- Then 브라우저 재시작 후에도 모든 데이터가 유지되고, 대시보드에서 조회 가능

---

## 6. UI 레이아웃

### 전체 구조

```
┌────────────────────────────────────────────────────┐
│  [로고]  Writing Coach       [대시보드] [새 세션]    │  ← 헤더
├────────────────────────────────────────────────────┤
│                                                    │
│  ┌──────────────────┐  ┌───────────────────────┐  │
│  │                  │  │                       │  │
│  │   에디터 영역     │  │   피드백 영역          │  │
│  │   (왼쪽 패널)     │  │   (오른쪽 패널)        │  │
│  │                  │  │                       │  │
│  │  - 에세이 작성    │  │  - 교정 카드           │  │
│  │  - 한국어 번역    │  │  - 비교 테이블         │  │
│  │  - 수정본 작성    │  │  - 4레벨 리라이트      │  │
│  │                  │  │  - 배운 표현           │  │
│  └──────────────────┘  └───────────────────────┘  │
│                                                    │
├────────────────────────────────────────────────────┤
│  Phase: [B] [C] [D] [E] [F] [G] [H]  단어 수: 267 │  ← 풋터
└────────────────────────────────────────────────────┘
```

### 핵심 UI 패턴

- **Split Panel**: 왼쪽(에디터) + 오른쪽(피드백). 모든 Phase에서 일관된 구조
- **Phase 스테퍼**: 하단에 현재 Phase 위치 표시 (진행 바)
- **오류 카드**: 원문(빨강) → 교정(초록) + 유형 뱃지 + 설명 접힘/펼침
- **4레벨 탭**: Round 3에서 A2-B1 / B1-B2 / B2-C1 / C1-C2 탭 전환
- **비교 뷰**: Mode B에서 좌(내 글) / 우(원문) 사이드바이사이드 + 차이 하이라이트

---

## 7. 에이전트 행동 경계 (시스템 프롬프트 규칙)

기존 스킬의 Always/Ask/Never 경계를 시스템 프롬프트에 임베딩:

- **Always**: L1 태그, 4요소 포맷, 라운드 순서 엄수, 격려적 톤
- **Never**: 에세이 대필, 라운드 혼합, 원문 조기 공개 (Mode B)
- **Format**: 응답을 JSON 구조로 반환하도록 시스템 프롬프트에 명시 → 프론트엔드에서 파싱하여 UI 렌더링

### Claude 응답 JSON 형식 (Mode A Round 1 예시)

```json
{
  "phase": "E",
  "totalErrors": 12,
  "l1Count": 8,
  "generalCount": 4,
  "errors": [
    {
      "id": 1,
      "original": "I think environment is very important issue.",
      "correction": "I think **the** environment is **a** very important issue.",
      "type": "L1-1",
      "typeName": "관사 누락",
      "explanation": "한국어에는 관사가 없어서..."
    }
  ],
  "summary": { "articles": 3, "tense": 2, "preposition": 1 },
  "encouragement": "관사 패턴을 잘 인식하고 계세요. 다음 수정에서 집중해보세요!"
}
```

---

## 8. 에러 처리 + UX 상태

### 로딩 상태
- Claude API 호출 중: "피드백 생성 중..." 메시지 + 스피너 + 예상 시간 (10-20초)
- 에세이 분석 중 단계별 표시: "문법 검사 중... → L1 패턴 분석 중... → 피드백 정리 중..."

### 에러 UI
- 네트워크 실패: "인터넷 연결을 확인해주세요. 에세이는 안전하게 저장되어 있습니다." + 재시도 버튼
- API 타임아웃: "응답이 늦어지고 있습니다. 다시 시도할까요?" + 재시도 버튼
- JSON 파싱 실패: 폴백으로 마크다운 텍스트 표시 + "정확한 형식으로 다시 요청" 옵션
- LocalStorage 용량 초과: "저장 공간이 부족합니다. 오래된 세션을 내보내고 삭제할까요?" + 내보내기 버튼

### 내보내기 기능
- 대시보드에서 "JSON 내보내기" 버튼
- 전체 데이터 (오류 프로필 + 모든 세션) → writing-coach-export-YYMMDD.json 다운로드
- Obsidian에 수동 임포트 가능한 형식

### 기타 UX
- 다크 모드 토글 (Tailwind dark: 클래스, preference를 LocalStorage에 저장)
- 키보드 단축키: Cmd/Ctrl+Enter (제출), Esc (취소)

---

## 9. 리스크 & 완화 전략

| 리스크 | 영향 | 완화 전략 |
|--------|------|----------|
| Claude API 응답이 JSON 형식을 따르지 않음 | UI 파싱 실패 | 시스템 프롬프트에 JSON 스키마 명시 + 파싱 실패 시 raw text 폴백 표시 |
| LocalStorage 5MB 초과 | 데이터 손실 | 오래된 세션(30일+) 자동 아카이브/삭제 옵션 |
| Vercel 무료 티어 한도 초과 | 서비스 중단 | 월 사용량 모니터링, 초과 시 로컬호스트 모드 전환 |
| 모바일 화면에서 Split Panel 비좁음 | UX 저하 | 태블릿 이하에서는 탭 전환 방식으로 변경 |
| API 키 노출 | 보안 | Vercel env 변수 사용, 클라이언트 코드에 절대 포함 안 함 |

---

## 9. 구현 우선순위

| 순서 | 기능 | 예상 난이도 |
|------|------|-----------|
| 1 | Vercel 프로젝트 + API 프록시 (/api/chat) | 하 |
| 2 | 메인 화면 + 모드 선택 | 하 |
| 3 | Mode A: Phase D (에디터) + Phase E (Round 1) | 중 |
| 4 | Mode A: Phase F (Round 2) + Phase G (Round 3 + 4레벨 탭) | 중 |
| 5 | Mode A: Phase B-C (주제/어휘) + Phase H (마무리) | 하 |
| 6 | LocalStorage 저장/로드 + 오류 프로필 관리 | 중 |
| 7 | 대시보드 (차트 + 세션 히스토리) | 중 |
| 8 | Mode B: 역번역 전체 플로우 | 중 |
| 9 | 반응형 (태블릿 대응) | 하 |

---

## 10. 참고 자료

### 경쟁 분석
- Write & Improve (Cambridge) — 점진적 피드백 공개 UX
- Grammarly — WebSocket 기반 실시간 교정
- Ludwig.guru — 300M 문장 DB 기반 네이티브 용례 검색

### 기술 참고
- Anthropic Messages API + Streaming
- Vercel Serverless Functions
- Tailwind CSS (CDN 모드)
- LocalStorage API

### 기존 프로젝트 연동
- [[Writing Coach PRD]] — 원본 스킬 PRD (교육학적 설계 기반)
- [[나머지/도구와 자동화/CMDS/📖 400 Methodologies/AI 프로젝트 기획-실행 파이프라인 (pipeline-full)]]

---

## 관련 문서

- [[Writing Coach PRD]]
- [[Writing Coach 사용 가이드]]
- [[나머지/도구와 자동화/CMDS/📖 400 Methodologies/AI 프로젝트 기획-실행 파이프라인 (pipeline-full)]]
