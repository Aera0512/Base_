---
title: Claudegram 개요
tags: [claudegram, overview, index]
created: 2026-02-20
updated: 2026-02-20
---

# Claudegram 개요

> Claudegram은 Telegram을 통해 Claude AI 에이전트와 상호작용하는 오픈소스 개인 비서 봇입니다.

## 목차
- [[#Claudegram이란]]
- [[#핵심 아키텍처]]
- [[#주요 특징]]
- [[#기술 스택]]
- [[#프로젝트 정보]]

---

## Claudegram이란

Claudegram은 Anthropic의 Claude Agent SDK와 Grammy(Telegram Bot 프레임워크)를 결합하여 만든 **Telegram 기반 AI 개인 비서**입니다. 단순한 챗봇이 아니라, 로컬 머신에서 파일을 읽고 쓰고, 셸 명령을 실행하고, 코드를 편집할 수 있는 **자율 에이전트**입니다.

사용자는 Telegram 채팅 하나로 코드 개발, 콘텐츠 리서치, 음성 상호작용 등 다양한 작업을 수행할 수 있습니다.

## 핵심 아키텍처

```
Telegram 사용자
    │
    ▼
Grammy Bot (인증 미들웨어)
    │
    ▼
핸들러 라우팅 (명령어 / 메시지 / 음성 / 사진)
    │
    ▼
Claude Agent SDK (세션 관리, 요청 큐)
    │
    ▼
로컬 머신 (Bash, 파일 시스템, 도구 실행)
```

> [!tip] 자세한 기술 구조
> 코드 구조와 모듈 설명은 [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/architecture|아키텍처]] 노트를 참고하세요.

## 주요 특징

| 특징 | 설명 |
|------|------|
| **Claude 에이전트** | Bash, Read, Write, Edit, Glob, Grep 도구 접근 가능 |
| **세션 관리** | 세션 생성, 이어하기, 초기화 지원 |
| **스트리밍 응답** | 실시간 업데이트되는 응답 출력 |
| **모델 선택** | Sonnet / Opus / Haiku 전환 가능 |
| **이미지 업로드** | 사진 전송 시 Claude에 전달 |
| **음성 지원** | 음성 메모 자동 변환 + TTS 응답 |
| **콘텐츠 연동** | Reddit, Medium, Telegraph 연동 |
| **리치 출력** | MarkdownV2, Telegraph Instant View, 스마트 청킹 |

> [!info] 전체 명령어 목록
> [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/commands-and-features|명령어 및 기능]] 노트에서 모든 명령어를 확인할 수 있습니다.

## 기술 스택

| 구성 요소 | 기술 |
|-----------|------|
| 언어 | TypeScript |
| 런타임 | Node.js 18+ |
| 봇 프레임워크 | Grammy |
| AI 백엔드 | Anthropic Claude Agent SDK |
| 음성 인식 | Groq Whisper |
| TTS | OpenAI TTS API |
| 비디오 처리 | ffmpeg |
| 패키지 관리 | npm |

## 프로젝트 정보

- **라이선스:** 오픈소스
- **저장소:** GitHub (claudegram)
- **개발 언어:** TypeScript
- **플랫폼:** Telegram

---

## 관련 노트
- [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/setup-and-config|설치 및 설정]] — 환경 구성 및 첫 실행
- [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/architecture|아키텍처]] — 코드 구조 및 기술 설계
- [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/commands-and-features|명령어 및 기능]] — 전체 명령어 레퍼런스
- [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/integrations|외부 연동]] — Reddit, Medium, 음성 등 연동
- [[나머지/도구와 자동화/CMDS/📖 900 AI Tools/Claudegram/workflows|활용 워크플로우]] — 실전 활용 가이드

---

> [!info] 출처
> 내부 요약 — Claudegram 프로젝트 소스 코드 기반
