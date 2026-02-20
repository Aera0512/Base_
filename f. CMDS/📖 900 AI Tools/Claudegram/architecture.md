---
title: 아키텍처
tags: [claudegram, architecture, code, technical, security]
created: 2026-02-20
updated: 2026-02-20
---

# 아키텍처

> Claudegram의 코드 구조, 핵심 모듈, 데이터 흐름, 보안 모델에 대한 기술 심화 노트입니다.

## 목차
- [[#소스 디렉토리 구조]]
- [[#핵심 모듈]]
- [[#데이터 흐름]]
- [[#세션 생명주기]]
- [[#보안 모델]]

---

## 소스 디렉토리 구조

```
src/
├── bot/           # Grammy 봇 설정 및 핸들러
│   ├── handlers/  # 명령어, 메시지, 음성, 사진 핸들러
│   └── auth/      # 인증 미들웨어
├── claude/        # Agent SDK 통합
│   ├── session/   # 세션 관리
│   ├── queue/     # 요청 큐
│   └── parser/    # 명령어 파서
├── telegram/      # 메시지 전송 계층
│   ├── sender/    # 스트리밍/청킹 전송
│   ├── markdown/  # MarkdownV2 변환
│   └── telegraph/ # Telegraph Instant View
├── tts/           # TTS 제공자 라우팅
├── audio/         # 음성 변환 유틸리티
├── reddit/        # Reddit 비디오 다운로드 파이프라인
├── medium/        # Freedium 기사 페처
└── utils/         # 유틸리티 함수
    ├── download   # 다운로드 헬퍼
    ├── sanitize   # 살균 처리
    ├── file-type  # 파일 타입 검증
    └── url-guard  # URL 검증
```

## 핵심 모듈

### `bot/` — Grammy 봇 계층
Telegram Bot API와의 인터페이스를 담당합니다.

- **Grammy 프레임워크** 기반 봇 인스턴스 생성
- **인증 미들웨어:** `TELEGRAM_USER_ID` 화이트리스트로 접근 제어
- **핸들러 라우팅:** 명령어(`/command`), 일반 메시지, 음성 메모, 사진 업로드를 각각의 핸들러로 분배

### `claude/` — Agent SDK 통합
Anthropic의 Claude Agent SDK와의 연동을 담당합니다.

- **세션 관리:** 세션 생성, 이어하기(resume), 초기화(clear)
- **요청 큐:** 동시 요청 처리 및 순서 보장
- **명령어 파서:** Telegram 명령어를 Claude 에이전트 지시문으로 변환
- **도구 접근:** Bash, Read, Write, Edit, Glob, Grep 등 시스템 도구 제공

### `telegram/` — 메시지 전송 계층
Claude의 응답을 Telegram에 최적화하여 전달합니다.

- **스트리밍 전송:** 실시간으로 응답을 업데이트하며 출력
- **스마트 청킹:** Telegram 메시지 길이 제한에 맞춰 자동 분할
- **MarkdownV2 변환:** Claude 출력을 Telegram MarkdownV2 형식으로 변환
- **Telegraph Instant View:** 긴 응답이나 테이블을 Telegraph 페이지로 생성
- **중복 제거:** 동일 메시지 재전송 방지

### `tts/` — 텍스트 음성 변환
OpenAI TTS API를 사용한 음성 응답을 담당합니다.

- 13가지 음성 선택 가능 (alloy, ash, ballad, cedar, coral 등)
- 사용자별 TTS 설정 저장
- 음성 응답 자동 전송 훅

### `reddit/` — Reddit 연동
Reddit 콘텐츠 가져오기 및 비디오 처리를 담당합니다.

- `redditfetch.py` 기반 게시물 수집
- DASH 매니페스트 + ffmpeg 비디오 다운로드
- 50MB 초과 비디오 자동 압축
- 대용량 스레드 JSON 내보내기

### `medium/` — Medium 연동
Freedium 미러를 통한 유료 기사 접근을 담당합니다.

- 순수 TypeScript 구현 (Python/Playwright 불필요)
- Telegraph Instant View 또는 Markdown 저장 지원

### `utils/` — 유틸리티
공통 보안 및 헬퍼 함수 모음입니다.

- `download` — 파일 다운로드 헬퍼, URL 프로토콜 검증
- `sanitize` — 경로 살균, 에러 메시지 살균
- `file-type` — 이미지 파일 유효성 검증
- `url-guard` — URL 안전성 검증

## 데이터 흐름

사용자 메시지가 처리되는 전체 흐름입니다:

```
1. 사용자가 Telegram에서 메시지 전송
           │
2. Grammy Bot이 메시지 수신
           │
3. 인증 미들웨어가 사용자 ID 확인
           │ (미인증 → 무시)
           │ (인증됨 → 계속)
           ▼
4. 핸들러 라우팅
   ├─ /command → 명령어 핸들러
   ├─ 텍스트 → 메시지 핸들러
   ├─ 음성 → 음성 핸들러 (Groq Whisper 변환)
   └─ 사진 → 사진 핸들러
           │
5. Claude Agent SDK에 쿼리 전송
           │
6. 에이전트가 도구 사용하여 작업 수행
   (Bash, Read, Write, Edit 등)
           │
7. 스트리밍 응답 생성
           │
8. Telegram 전송 계층에서 포맷팅
   ├─ MarkdownV2 변환
   ├─ 스마트 청킹
   └─ Telegraph (선택적)
           │
9. 사용자에게 응답 전달
```

## 세션 생명주기

```
생성 (Create)
  │ /start 또는 첫 메시지
  ▼
활성 (Active)
  │ 메시지 송수신, 도구 실행
  │ /continue로 중단된 세션 이어하기
  ▼
이어하기 (Resume)
  │ /resume <session-id>
  │ 이전 세션 컨텍스트 복원
  ▼
초기화 (Clear)
  │ /clear
  │ 세션 컨텍스트 삭제
  ▼
종료
```

> [!tip] 세션 관련 명령어
> 세션 관리 명령어 전체 목록은 [[commands-and-features#세션 명령어|명령어 및 기능]]에서 확인하세요.

## 보안 모델

Claudegram은 외부 입력을 처리할 때 여러 보안 계층을 적용합니다.

### URL 검증
- `isValidProtocol()` — 허용된 프로토콜만 통과 (http, https)
- SSRF(Server-Side Request Forgery) 방어

### 경로 살균
- `sanitizePath()` — 경로 탐색 공격 방지
- 작업 디렉토리 외부 접근 차단

### 에러 살균
- `sanitizeError()` — 에러 메시지에서 민감 정보 제거
- 토큰, API 키 등이 로그에 노출되지 않도록 처리

### 파일 검증
- `isValidImageFile()` — 이미지 파일 매직 바이트 검증
- 악성 파일 업로드 방지

### 워크스페이스 가드
- 에이전트 작업 범위를 지정된 디렉토리로 제한
- 시스템 파일 접근 차단

> [!warning] 보안 원칙
> 외부 입력(URL, 파일, 사용자 텍스트)은 항상 검증 후 처리합니다. 프로세스 인수에 토큰이나 시크릿을 포함하지 마세요. curl 등의 도구 사용 시 stdin을 통해 전달합니다.

---

## 관련 노트
- [[index|Claudegram 개요]] — 프로젝트 소개
- [[setup-and-config|설치 및 설정]] — 환경 구성 및 보안 설정
- [[commands-and-features|명령어 및 기능]] — 코드가 구현하는 명령어

---

> [!info] 출처
> 내부 요약 — Claudegram 프로젝트 소스 코드 구조 기반
