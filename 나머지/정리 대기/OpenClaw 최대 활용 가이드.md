---
tags: [ai-agent, automation, openclaw, self-hosted, productivity, security, integration]
created: 2026-02-26
type: research
source:
  - https://docs.openclaw.ai/start/getting-started
  - https://docs.openclaw.ai/tools/skills
  - https://open-claw.bot/docs/gateway/security/
  - https://codingapple.com/blog/openclaw-install/
  - https://wikidocs.net/325469
  - https://jangwook.net/en/blog/en/openclaw-advanced-usage/
  - https://cybersecuritynews.com/openclaw-2026-2-23-released/
  - https://vpncentral.com/openclaw-2026-2-23-hardens-security-while-adding-claude-opus-4-6-support/
  - https://github.com/openclaw/openclaw/releases
  - https://lilys.ai/ko/notes/openclaw-20260202/openclaw-automations-wild-builds
  - https://rentamac.io/openclaw-vs-claude/
  - https://www.datacamp.com/blog/openclaw-vs-claude-code
quality_score: 0
reviewed: false
related: []
---

# OpenClaw 최대 활용 가이드

> [!abstract] 핵심 요약
> OpenClaw는 사용자 컴퓨터에서 24/7 실행되는 오픈소스 AI 에이전트 플랫폼입니다. 메신저를 통해 명령을 받아 파일 관리, 이메일 전송, 코드 배포, 웹 자동화 등 실제 작업을 자율적으로 수행합니다. 2026년 2월 기준 GitHub 스타 200,000개 이상을 기록하며 가장 빠르게 성장 중입니다. 무료 오픈소스이나 AI 모델 API 비용은 별도입니다.

---

## 핵심 개념

**OpenClaw**는 오픈소스 자율형 AI 에이전트 플랫폼으로, 다음과 같은 특징을 가집니다:

- **자율 실행**: 사용자의 컴퓨터에서 독립적으로 실행되며 지속적인 모니터링과 작업 수행
- **메신저 기반 제어**: Telegram 등 메신저를 통해 자연어로 명령하고 결과 수신
- **실제 작업 수행**: 파일 관리, 이메일 전송, 코드 배포, 웹 자동화, CRM 구축 등
- **확장 가능**: Skills(자연어 API 통합)와 Plugins(TypeScript 심층 확장)로 기능 확장
- **지속 메모리**: 작업 컨텍스트를 기억하며 장기간 자동화 실행
- **오픈소스 & 프라이버시**: 로컬 실행으로 데이터 통제 가능

**2026년 최신 버전 v2026.2.23 주요 기능**:
- Claude Opus 4.6 지원
- Heartbeat(메일/일정/웹페이지 모니터링)
- Discord V2 통합
- 보안 강화(SSRF 보호, 자격증명 자동 삭제)
- 중첩 서브에이전트
- Mistral/Moonshot 프로바이더 추가

## 설정 가이드

### 1단계: 플랫폼별 설치

**Windows (PowerShell 관리자 모드)**:
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

**macOS / Linux**:
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

Node.js 22+ 버전이 자동으로 설치됩니다.

### 2단계: 온보딩 마법사 실행

```bash
openclaw onboard
```

이 명령을 통해 다음을 설정합니다:
- **AI 모델 선택**: Claude Opus 4.6(코딩 추천), Gemini(무료 체험), Ollama(로컬/비용 제로)
- **메신저 연동**: Telegram BotFather를 통한 봇 생성 및 토큰 입력
- **로컬 GPU**: 사용 가능 시 자동 감지 및 활성화

### 3단계: Gateway 실행

```bash
openclaw gateway
```

실행 후 대시보드 접속: `http://127.0.0.1:18789/`

### 4단계: 보안 강화 (필수)

설치 즉시 보안 감사 실행:
```bash
openclaw security audit --fix
```

파일 권한 강화:
```bash
chmod 700 ~/.openclaw
chmod 600 ~/.openclaw/openclaw.json
```

**중요 보안 취약점**: CVE-2026-25253(CVSS 8.8점) - API 키가 평문으로 저장되는 문제. 최신 버전으로 업데이트 필수.

### 5단계: 설정 파일 편집

`~/.openclaw/openclaw.json` (JSON5 형식) 주요 설정:

```json
{
  "gateway": {
    "bind": "loopback"  // 외부 접근 차단
  },
  "dmPolicy": "pairing",  // 보안 DM 모드
  "tools": {
    "allow": ["file", "web", "email"]  // 화이트리스트
  },
  "sandbox": {
    "mode": "all"  // 모든 작업 샌드박스화
  },
  "logging": {
    "redactSensitive": "tools"  // 민감 정보 로깅 제외
  }
}
```

### 6단계: Skills 설치

ClawHub(clawhub.com)에서 필요한 Skills 설치:

```bash
clawhub install <skill-slug>
```

**Skills 우선순위** (3단계):
1. Workspace (프로젝트별 로컬 skills)
2. 관리형 (ClawHub 설치)
3. 번들 (내장 기본 skills)

### 7단계: 문제 해결

설치 중 문제 발생 시:
```bash
openclaw doctor
```

자동으로 일반적인 설정 문제를 진단하고 수정합니다.

### 8단계: Workspace 파일 작성 (선택)

프로젝트 루트에 다음 파일 생성으로 에이전트 동작 커스터마이징:
- `AGENTS.md`: 멀티에이전트 역할 정의
- `SOUL.md`: 에이전트 성격/응답 스타일
- `HEARTBEAT.md`: 정기 실행 작업 정의

### 9단계: 메신저에서 테스트

Telegram 봇에 메시지 전송:
```
오늘 날씨 알려줘
```

응답이 오면 설정 완료!

### 10단계: 고급 설정 (선택)

- **Cron 자동화**: 시간 기반 작업 예약
- **Webhook 통합**: n8n/Make/GitHub Actions 연동
- **MCP 서버**: PostgreSQL/Notion 등 데이터베이스 통합
- **Tailscale Serve**: 원격 접근 보안 터널

## 활용 팁

**보안**:
- 설치 즉시 `openclaw security audit --fix` 실행
- `dmPolicy='pairing'` 필수 설정
- `sandbox.mode='all'` 활성화
- API 키 평문 저장 주의 (CVE-2026-25253)
- `gateway.bind='loopback'` 유지
- `tools.allow` 화이트리스트 설정
- 정기 업데이트 적용

**AI 모델 선택**:
- 코딩 작업: Claude Opus 4.6 (최고 성능)
- 무료 체험: Gemini (Google AI Studio)
- 비용 제로: Ollama (로컬 실행, 성능 낮음)

**효율성**:
- 메신저 연동이 실전에서 가장 편리
- ClawHub에서 필요한 skills만 설치 (보안 리뷰 필수)
- Workspace 파일(AGENTS.md/SOUL.md/HEARTBEAT.md) 작성으로 커스터마이징
- Cron 자동화로 생산성 극대화
- 에이전트 결과 교차 검증

**비용 관리**:
- API 비용 모니터링 (OpenClaw는 무료, AI 모델 API는 유료)
- 로컬 Ollama 사용 시 API 비용 제로

## 고급 활용

### Cron 작업
시간 기반 자동 실행:
```json
{
  "heartbeat": {
    "schedule": "0 9 * * *",  // 매일 9시
    "tasks": ["이메일 요약", "일정 확인"]
  }
}
```

### Webhook 통합
외부 서비스와 연동:
- **n8n**: 워크플로 자동화
- **Make**: 앱 통합 자동화
- **GitHub Actions**: 코드 배포 자동화

### 멀티에이전트 아키텍처
권한별 전문 에이전트 구성:
```markdown
# AGENTS.md
- **Finance Agent**: 회계 처리 전용, 제한된 파일 접근
- **Dev Agent**: 코드 배포, GitHub 접근
- **Content Agent**: 콘텐츠 스크랩 및 벡터화
```

### MCP 서버 통합
데이터베이스 직접 연동:
- PostgreSQL: 데이터 쿼리 및 분석
- Notion: 노트 자동 생성 및 업데이트

### CDP 브라우저 자동화
Chrome DevTools Protocol로 웹 브라우저 제어:
- 로그인 자동화
- 데이터 스크랩
- UI 테스트

### Skills 우선순위 활용
프로젝트별 Workspace skills로 전역 설정 오버라이드:
```
프로젝트/
  .openclaw/
    skills/
      custom-skill/
        SKILL.md
```

### 환경 변수 주입
```bash
export OPENCLAW_HOME=/custom/path
export OPENCLAW_LOG_LEVEL=debug
openclaw gateway
```

### Heartbeat 모니터링
메일/일정/웹페이지 변화 자동 감지 및 알림:
```markdown
# HEARTBEAT.md
- 매시간 Gmail 신규 메일 확인
- 매일 9시 캘린더 일정 요약
- 특정 웹페이지 변경 감지 시 알림
```

### Discord V2 통합
Discord 서버에서 명령 실행 및 결과 수신

### 중첩 서브에이전트
복잡한 작업을 계층적 에이전트로 분해:
```
Main Agent
  ├─ Research Agent
  ├─ Data Processing Agent
  │   └─ Validation Subagent
  └─ Reporting Agent
```

### 에이전트별 파라미터
각 에이전트에 다른 AI 모델/설정 적용 가능

## 상세 분석

### 설치 및 초기 설정
OpenClaw 설치는 플랫폼별 스크립트 하나로 완료됩니다. Windows는 PowerShell 관리자 모드에서 `iwr -useb https://openclaw.ai/install.ps1 | iex`, macOS/Linux는 `curl -fsSL https://openclaw.ai/install.sh | bash`를 실행합니다. Node.js 22+ 버전이 자동으로 설치되며, `openclaw onboard` 명령으로 온보딩 마법사가 시작됩니다. 여기서 AI 모델(Claude Opus 4.6/Gemini/Ollama), 메신저 연동(Telegram BotFather), 로컬 GPU 설정을 진행합니다. 실행은 `openclaw gateway`로 시작하며 대시보드는 http://127.0.0.1:18789/에서 확인합니다. 문제 발생 시 `openclaw doctor`로 진단합니다.

### Skills와 Plugins
**Skills**는 자연어 기반 API 통합을 제공하며 SKILL.md 파일로 정의됩니다. **Plugins**는 TypeScript로 작성된 심층 확장 기능입니다. ClawHub(clawhub.com)에서 `clawhub install <slug>` 명령으로 설치하며, 3단계 우선순위가 적용됩니다: Workspace(프로젝트별) > 관리형(ClawHub) > 번들(내장). 설정은 `~/.openclaw/openclaw.json`에서 관리합니다. 보안상 third-party 코드는 반드시 리뷰 후 설치해야 합니다.

### 보안 강화
즉시 실행해야 할 보안 조치: `openclaw security audit --fix`, `chmod 700 ~/.openclaw`, `chmod 600 openclaw.json`. **CVE-2026-25253(CVSS 8.8점)** 취약점은 API 키가 평문으로 저장되는 문제로, 최신 버전 업데이트가 필수입니다. 주요 설정: `gateway.bind='loopback'`(외부 접근 차단), `dmPolicy='pairing'`(보안 DM 모드), `tools.allow` 화이트리스트, `sandbox.mode='all'`(모든 작업 샌드박스화), `logging.redactSensitive='tools'`(민감 정보 로깅 제외). 원격 접근 시 Tailscale Serve 권장.

### 실전 활용 사례
OpenClaw는 다양한 실전 시나리오에서 활용됩니다:
- **이메일/일정 자동화**: Gmail + Calendar 통합으로 일정 자동 정리
- **CRM 구축**: Gmail + Calendar + Fathom 연동으로 고객 관리 자동화
- **콘텐츠 스크랩**: 웹 데이터 수집 후 벡터화하여 검색 가능하게 저장
- **브랜드 모니터링**: 수동 3시간 작업을 자동화로 전환
- **브라우저 자동화**: CDP로 로그인, 데이터 입력, UI 테스트 자동화
- **Cron 작업**: 정기 실행 작업 스케줄링
- **Webhook 통합**: n8n/Make/GitHub Actions 연동
- **멀티에이전트**: 권한별 전문 에이전트 구성
- **MCP 서버**: PostgreSQL/Notion 직접 통합
- **보안 카메라**: AI 기반 감시 및 알림

### 2026 최신 기능
**v2026.2.23** 주요 업데이트:
- **보안 강화**: SSRF 보호, 자격증명 자동 삭제
- **Claude Opus 4.6 지원**: 최신 AI 모델 통합
- **Heartbeat**: 메일/일정/웹페이지 모니터링 자동화
- **Discord V2**: 개선된 Discord 통합
- **멀티미디어**: Moonshot 비디오 처리
- **중첩 서브에이전트**: 복잡한 작업 계층화
- **에이전트별 파라미터**: 개별 에이전트 설정 가능
- **Mistral/Moonshot 프로바이더**: 새로운 AI 모델 지원

GitHub 스타 200,000개 이상을 기록하며 가장 빠르게 성장하는 오픈소스 AI 에이전트 플랫폼입니다.

### Claude Desktop 도구 비교
- **OpenClaw**: 24/7 범용 자동화, 메신저 기반, 무료 오픈소스, 지속 메모리, 일상 자동화 우위
- **Claude Code**: 코딩 특화, 터미널 통합, 구독 기반, 코드 리팩토링 우위
- **Claude Cowork**: 일반 사용자용 데스크톱 앱

목적에 따라 선택: 일상 업무 자동화는 OpenClaw, 개발 작업은 Claude Code가 적합합니다.

### 고급 자동화 설정
**Cron**: 시간 기반 자동 실행 (예: 매일 9시 이메일 요약)
**Webhook**: n8n/Make/GitHub Actions 연동으로 외부 이벤트 트리거
**Workspace 파일**: AGENTS.md(에이전트 역할), SOUL.md(응답 스타일), HEARTBEAT.md(정기 작업)
**MCP 서버**: PostgreSQL/Notion 등 데이터베이스 직접 통합
**CDP 브라우저 자동화**: Chrome DevTools Protocol로 웹 제어
**멀티에이전트**: 권한별 전문 에이전트 구성 (Finance Agent, Dev Agent 등)
**환경변수**: OPENCLAW_HOME 등으로 경로 커스터마이징
**Skills 우선순위**: Workspace > 관리형 > 번들

설정 파일 `~/.openclaw/openclaw.json`은 JSON5 형식으로 주석 사용 가능합니다.

## 연결 고리

- [[Claude Code]] - 코딩 특화 AI 에이전트, OpenClaw와 목적별 비교
- [[Claude Cowork]] - 일반 사용자용 데스크톱 AI 앱
- [[ClawHub]] - OpenClaw Skills/Plugins 마켓플레이스
- [[MCP]] - Model Context Protocol, 데이터베이스 통합 표준
- [[n8n]] - 워크플로 자동화 플랫폼, Webhook 연동
- [[Make]] - 앱 통합 자동화 서비스
- [[Ollama]] - 로컬 LLM 실행 플랫폼, 비용 제로 옵션
- [[Telegram BotFather]] - Telegram 봇 생성 및 토큰 발급
- [[Tailscale]] - 보안 원격 접근 터널
- [[Docker]] - 샌드박스 컨테이너 실행
- [[CDP]] - Chrome DevTools Protocol, 브라우저 자동화
- [[GitHub Actions]] - CI/CD 파이프라인, Webhook 연동
- [[Google AI Studio]] - Gemini API 무료 체험
- [[OpenRouter]] - 통합 AI 모델 API
- [[Fathom]] - 회의 요약 서비스, CRM 연동
- [[Notion]] - MCP 서버 통합 대상
- [[PostgreSQL]] - MCP 서버 통합 데이터베이스

## 추가 탐구 필요

- [ ] 한국어 공식 문서 부족 - 커뮤니티 기여 또는 번역 프로젝트 확인
- [ ] Windows 네이티브 상세 정보 - Windows 전용 최적화 설정
- [ ] 비용 예측 도구 - AI 모델 API 사용량 기반 비용 추정
- [ ] GUI 설정 도구 - 터미널 대신 그래픽 인터페이스 설정
- [ ] Skills 보안 검증 - 자동화된 보안 스캔 도구
- [ ] 백업/복구 가이드 - 설정 및 데이터 백업 전략
- [ ] 성능 벤치마크 - 다양한 AI 모델 성능 비교
- [ ] 멀티 플랫폼 동기화 - 여러 기기 간 설정 동기화
- [ ] 엔터프라이즈 기능 - 팀 협업 및 관리 기능
- [ ] 모바일 앱 - 스마트폰에서 OpenClaw 제어

## 출처

1. [Getting Started - OpenClaw Official Docs](https://docs.openclaw.ai/start/getting-started) — high
2. [Skills - OpenClaw Official Docs](https://docs.openclaw.ai/tools/skills) — high
3. [Security Guide](https://open-claw.bot/docs/gateway/security/) — high
4. [코딩애플 가이드](https://codingapple.com/blog/openclaw-install/) — high
5. [위키독스 가이드](https://wikidocs.net/325469) — high
6. [고급 활용 가이드](https://jangwook.net/en/blog/en/openclaw-advanced-usage/) — high
7. [v2026.2.23 보안 업데이트](https://cybersecuritynews.com/openclaw-2026-2-23-released/) — high
8. [Claude Opus 4.6 지원](https://vpncentral.com/openclaw-2026-2-23-hardens-security-while-adding-claude-opus-4-6-support/) — high
9. [GitHub Releases](https://github.com/openclaw/openclaw/releases) — high
10. [자동화 사례 13가지](https://lilys.ai/ko/notes/openclaw-20260202/openclaw-automations-wild-builds) — high
11. [OpenClaw vs Claude](https://rentamac.io/openclaw-vs-claude/) — high
12. [DataCamp 비교](https://www.datacamp.com/blog/openclaw-vs-claude-code) — high
13. [나무위키](https://namu.wiki/w/OpenClaw) — medium
14. [Brunch 활용법](https://brunch.co.kr/@teumlab/52) — medium
15. [TILNOTE 사용법](https://tilnote.io/en/pages/697e2e0cf998ea5a6490a077) — medium
