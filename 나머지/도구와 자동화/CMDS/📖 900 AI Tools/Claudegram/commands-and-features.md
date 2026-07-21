---
title: 명령어 및 기능
tags: [claudegram, commands, features, reference]
created: 2026-02-20
updated: 2026-02-20
---

# 명령어 및 기능

> Claudegram의 모든 봇 명령어와 사용자 기능에 대한 전체 레퍼런스입니다.

## 목차
- [[#세션 명령어]]
- [[#에이전트 모드 명령어]]
- [[#콘텐츠 명령어]]
- [[#음성 및 TTS 명령어]]
- [[#유틸리티 명령어]]
- [[#주요 기능]]

---

## 세션 명령어

세션을 생성하고 관리하는 명령어입니다.

| 명령어 | 설명 |
|--------|------|
| `/start` | 봇 시작 및 새 세션 생성 |
| `/project <경로>` | 작업 디렉토리 설정 |
| `/newproject <경로>` | 새 프로젝트 세션 생성 (격리된 워크스페이스) |
| `/clear` | 현재 세션 컨텍스트 초기화 |
| `/status` | 현재 세션 상태 확인 (모델, 디렉토리, 토큰 등) |
| `/sessions` | 모든 활성 세션 목록 표시 |
| `/resume <id>` | 이전 세션으로 복원 |
| `/continue` | 중단된 세션 이어하기 |

> [!tip] 멀티 세션 활용
> 여러 프로젝트를 동시에 관리하는 방법은 [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/workflows#워크플로우 4 멀티 세션 프로젝트 관리|활용 워크플로우]]를 참고하세요.

## 에이전트 모드 명령어

Claude 에이전트의 동작 모드를 전환하는 명령어입니다.

| 명령어 | 설명 |
|--------|------|
| `/plan` | 계획 모드 — 복잡한 작업을 단계별로 계획 |
| `/explore` | 탐색 모드 — 코드베이스 질문 및 탐색 |
| `/loop` | 루프 모드 — 반복 작업 수행 |
| `/model <모델명>` | 모델 전환 (sonnet / opus / haiku) |
| `/mode <모드>` | 에이전트 모드 전환 |

### 모델 선택 가이드

| 모델 | 특성 | 추천 용도 |
|------|------|-----------|
| **Haiku** | 빠르고 가벼움 | 간단한 질문, 빠른 응답 |
| **Sonnet** | 균형 잡힌 성능 | 일반 개발 작업 (기본값) |
| **Opus** | 최고 성능 | 복잡한 추론, 대규모 리팩토링 |

## 콘텐츠 명령어

외부 콘텐츠를 가져오고 처리하는 명령어입니다.

| 명령어 | 설명 |
|--------|------|
| `/reddit <URL>` | Reddit 게시물, 서브레딧, 사용자 프로필 가져오기 |
| `/vreddit <URL>` | Reddit 비디오 다운로드 |
| `/medium <URL>` | Medium 유료 기사 읽기 (Freedium 우회) |
| `/file <경로>` | 로컬 파일 내용 전송 |
| `/telegraph` | Telegraph Instant View 출력 토글 |

> [!info] 연동 상세
> 각 연동 서비스의 상세 설정과 동작 방식은 [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/integrations|외부 연동]] 노트를 참고하세요.

## 음성 및 TTS 명령어

음성 인식과 텍스트 음성 변환 관련 명령어입니다.

| 명령어 | 설명 |
|--------|------|
| `/tts` | TTS(텍스트 음성 변환) 토글 |
| `/tts <음성>` | TTS 음성 변경 (예: `/tts nova`) |
| `/transcribe` | 음성 메모 수동 변환 |
| 음성 메모 전송 | 자동 변환 후 Claude에 전달 |

### 사용 가능한 TTS 음성

alloy, ash, ballad, cedar, coral, echo, fable, marin, nova, onyx, sage, shimmer, verse (총 13종)

> [!tip] 음성 워크플로우
> 핸즈프리 사용 방법은 [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/workflows#워크플로우 3 음성 기반 상호작용|활용 워크플로우]]에서 확인하세요.

## 유틸리티 명령어

봇 상태 확인 및 관리 명령어입니다.

| 명령어 | 설명 |
|--------|------|
| `/ping` | 봇 응답 확인 (연결 테스트) |
| `/context` | 현재 컨텍스트 토큰 사용량 확인 |
| `/botstatus` | 봇 시스템 상태 확인 |
| `/restartbot` | 봇 프로세스 재시작 |
| `/cancel` | 진행 중인 요청 취소 |
| `/commands` | 사용 가능한 명령어 목록 표시 |

## 주요 기능

### Claude Code 에이전트
Claudegram의 핵심은 완전한 Claude Code 에이전트입니다. 다음 도구에 접근할 수 있습니다:

- **Bash** — 셸 명령 실행
- **Read** — 파일 읽기
- **Write** — 파일 생성
- **Edit** — 파일 편집
- **Glob** — 파일 검색 (패턴 매칭)
- **Grep** — 파일 내용 검색

### 스트리밍 응답
Claude의 응답이 실시간으로 Telegram 메시지에 업데이트됩니다. 긴 작업도 진행 상황을 실시간으로 확인할 수 있습니다.

### 리치 출력 형식
- **MarkdownV2** — Telegram 네이티브 마크다운 포맷팅
- **Telegraph Instant View** — 긴 응답이나 테이블을 깔끔한 웹 페이지로 제공
- **스마트 청킹** — Telegram 메시지 길이 제한(4096자)에 맞춰 자동 분할
- **ForceReply** — 특정 상황에서 사용자 답장 유도
- **인라인 키보드** — 버튼 기반 상호작용

### 이미지 업로드
사진을 Telegram 채팅에 전송하면 Claude에 자동으로 전달됩니다. 스크린샷 분석, 디자인 리뷰 등에 활용할 수 있습니다.

> [!tip] 실전 활용
> 이 명령어들을 조합한 실전 워크플로우는 [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/workflows|활용 워크플로우]] 노트를 참고하세요.

---

## 관련 노트
- [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/index|Claudegram 개요]] — 프로젝트 소개
- [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/integrations|외부 연동]] — 명령어가 사용하는 연동 서비스
- [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/architecture|아키텍처]] — 명령어를 구현하는 코드 구조
- [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/workflows|활용 워크플로우]] — 명령어 조합 활용법

---

> [!info] 출처
> 내부 요약 — Claudegram `src/bot/handlers/command.handler.ts` 기반
