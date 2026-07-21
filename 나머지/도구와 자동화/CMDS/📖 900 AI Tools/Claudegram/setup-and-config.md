---
title: 설치 및 설정
tags: [claudegram, setup, config, env, security]
created: 2026-02-20
updated: 2026-02-20
---

# 설치 및 설정

> Claudegram을 처음 설치하고 실행하기 위한 전체 가이드입니다.

## 목차
- [[#사전 요구 사항]]
- [[#설치 단계]]
- [[#환경 변수 설정]]
- [[#봇 제어 스크립트]]
- [[#개발 모드]]
- [[#보안 설정]]

---

## 사전 요구 사항

Claudegram을 실행하려면 다음이 필요합니다:

| 요구 사항 | 설명 |
|-----------|------|
| Node.js 18+ | JavaScript 런타임 |
| Claude Code CLI | Anthropic의 CLI 도구 |
| Telegram Bot Token | @BotFather에서 발급 |
| Telegram User ID | 인증용 사용자 ID |
| Anthropic API Key | Claude API 접근 키 |

## 설치 단계

```bash
# 1. 저장소 클론
git clone <repository-url>
cd claudegram

# 2. 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 필수 값 입력

# 3. 의존성 설치
npm install

# 4. 개발 모드 실행
npm run dev
```

> [!warning] 주의
> `.env` 파일에 API 키와 토큰을 정확히 입력해야 봇이 정상 작동합니다.

## 환경 변수 설정

### 필수 변수

| 변수명 | 설명 |
|--------|------|
| `TELEGRAM_BOT_TOKEN` | Telegram 봇 토큰 |
| `TELEGRAM_USER_ID` | 허용된 사용자 ID (쉼표 구분) |
| `ANTHROPIC_API_KEY` | Claude API 키 |

### 핵심 설정

| 변수명 | 설명 | 기본값 |
|--------|------|--------|
| `CLAUDE_MODEL` | 사용할 Claude 모델 | `sonnet` |
| `MAX_TURNS` | 최대 에이전트 턴 수 | - |
| `PERMISSION_MODE` | 권한 모드 | `default` |
| `WORKSPACE_DIR` | 작업 디렉토리 | - |

### Reddit 연동

| 변수명 | 설명 |
|--------|------|
| `REDDITFETCH_PATH` | redditfetch.py 경로 |
| `REDDIT_VIDEO_MAX_SIZE_MB` | 최대 비디오 크기 (MB) |

### Medium 연동

| 변수명 | 설명 |
|--------|------|
| `FREEDIUM_HOST` | Freedium 미러 호스트 |
| `MEDIUM_TIMEOUT_MS` | 요청 타임아웃 (ms) |

### 음성 및 TTS

| 변수명 | 설명 |
|--------|------|
| `GROQ_API_KEY` | Groq API 키 (음성 인식용) |
| `GROQ_TRANSCRIBE_PATH` | 변환 스크립트 경로 |
| `OPENAI_API_KEY` | OpenAI API 키 (TTS용) |
| `TTS_VOICE` | TTS 음성 선택 |
| `TTS_MODEL` | TTS 모델 |

> [!tip] 연동 상세 설정
> 각 연동 서비스의 자세한 설정은 [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/integrations|외부 연동]] 노트를 참고하세요.

## 봇 제어 스크립트

`claudegram-botctl.sh` 스크립트를 사용하여 봇을 관리할 수 있습니다:

```bash
# 봇 시작
./claudegram-botctl.sh start

# 봇 중지
./claudegram-botctl.sh stop

# 봇 재시작
./claudegram-botctl.sh restart

# 상태 확인
./claudegram-botctl.sh status
```

## 개발 모드

### 개발 모드 (dev)
```bash
npm run dev
```
- 핫 리로드 지원
- 코드 변경 시 자동 재시작
- 일반 개발 작업에 적합

### 프로덕션 모드 (prod)
```bash
npm run start
```
- 핫 리로드 없음
- **자체 편집(self-editing)** 워크플로우에 필요
- 안정적인 운영 환경

> [!tip] 자체 편집 워크플로우
> Claudegram이 자기 자신의 코드를 편집하는 워크플로우는 [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/workflows#워크플로우 5 자체 편집 Claudegram이 스스로 코드 수정|활용 워크플로우]]에서 확인하세요.

## 보안 설정

### 사용자 화이트리스트
`TELEGRAM_USER_ID` 환경 변수에 허용된 사용자 ID를 쉼표로 구분하여 설정합니다. 등록되지 않은 사용자의 메시지는 무시됩니다.

### 권한 모드
`PERMISSION_MODE` 환경 변수로 Claude 에이전트의 권한 수준을 제어합니다:

| 모드 | 설명 |
|------|------|
| `default` | 기본 권한 (안전한 도구만 자동 허용) |
| `dangerous` | 확장 권한 (모든 도구 허용) |

> [!warning] 보안 주의
> `dangerous` 모드는 셸 명령 실행, 파일 수정 등 모든 작업을 자동 허용합니다. 신뢰할 수 있는 환경에서만 사용하세요.

### 보안 체크리스트
- [ ] URL 프로토콜 검증 (`isValidProtocol()`)
- [ ] 경로 살균 처리 (`sanitizePath()`)
- [ ] 에러 메시지 살균 (`sanitizeError()`)
- [ ] 파일 콘텐츠 검증 (`isValidImageFile()`)
- [ ] 프로세스 인수에 토큰/시크릿 미포함

> [!info] 아키텍처의 보안 모델
> 코드 수준의 보안 설계는 [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/architecture#보안 모델|아키텍처]] 노트를 참고하세요.

---

## 관련 노트
- [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/index|Claudegram 개요]] — 프로젝트 소개
- [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/commands-and-features|명령어 및 기능]] — 설정 후 사용 가능한 명령어
- [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/integrations|외부 연동]] — 연동 서비스별 상세 설정
- [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/architecture|아키텍처]] — 코드 구조 및 보안 모델

---

> [!info] 출처
> 내부 요약 — Claudegram 프로젝트 소스 코드 및 `.env.example` 기반
