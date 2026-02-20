---
title: 외부 연동
tags: [claudegram, integrations, reddit, medium, voice, tts, telegraph]
created: 2026-02-20
updated: 2026-02-20
---

# 외부 연동

> Claudegram이 연동하는 외부 서비스(Reddit, Medium, 음성 인식, TTS, Telegraph)에 대한 상세 가이드입니다.

## 목차
- [[#Reddit 연동]]
- [[#Medium 연동]]
- [[#음성 인식 Groq Whisper]]
- [[#텍스트 음성 변환 OpenAI TTS]]
- [[#Telegraph 출력]]

---

## Reddit 연동

Reddit 게시물, 서브레딧, 사용자 프로필을 가져오고 비디오를 다운로드합니다.

### 기본 사용

```
/reddit <Reddit URL>      # 게시물, 서브레딧, 사용자 프로필 가져오기
/vreddit <Reddit URL>     # 비디오 다운로드
```

### 동작 방식

| 기능 | 설명 |
|------|------|
| 게시물 가져오기 | `redditfetch.py`를 통해 게시물 내용 수집 |
| 비디오 다운로드 | DASH 매니페스트 파싱 + ffmpeg 결합 |
| 자동 압축 | 50MB 초과 비디오 자동 압축 |
| 대용량 스레드 | 큰 스레드는 JSON 파일로 내보내기 |

### 환경 변수

| 변수명 | 설명 | 필수 |
|--------|------|------|
| `REDDITFETCH_PATH` | `redditfetch.py` 스크립트 경로 | Yes |
| `REDDIT_VIDEO_MAX_SIZE_MB` | 최대 비디오 크기 (MB) | No |

### 비디오 처리 파이프라인

```
Reddit URL 입력
    │
    ▼
DASH 매니페스트 파싱
    │
    ▼
비디오 + 오디오 스트림 다운로드
    │
    ▼
ffmpeg로 결합
    │
    ▼
크기 확인 (> 50MB?)
    ├─ Yes → 자동 압축
    └─ No → 그대로 전송
    │
    ▼
Telegram으로 전송
```

> [!warning] 주의
> ffmpeg가 시스템에 설치되어 있어야 비디오 다운로드가 동작합니다.

---

## Medium 연동

Freedium 미러를 통해 Medium 유료 기사를 무료로 읽을 수 있습니다.

### 기본 사용

```
/medium <Medium URL>      # 유료 기사 가져오기
```

### 동작 방식

| 기능 | 설명 |
|------|------|
| 기사 가져오기 | Freedium 미러 서버를 통해 기사 내용 수집 |
| 출력 형식 | Telegraph Instant View, Markdown 저장, 또는 둘 다 |
| 구현 방식 | 순수 TypeScript (Python/Playwright 불필요) |

### 환경 변수

| 변수명 | 설명 | 필수 |
|--------|------|------|
| `FREEDIUM_HOST` | Freedium 미러 호스트 주소 | No (기본값 있음) |
| `MEDIUM_TIMEOUT_MS` | 요청 타임아웃 (밀리초) | No |

### 출력 옵션

1. **Telegraph Instant View** — 깔끔한 웹 페이지로 즉시 보기
2. **Markdown 저장** — 로컬 파일로 저장
3. **복합** — 둘 다 생성

> [!tip] Telegraph 토글
> `/telegraph` 명령어로 Telegraph 출력을 켜고 끌 수 있습니다.

---

## 음성 인식 (Groq Whisper)

Groq의 Whisper API를 사용하여 음성 메모를 텍스트로 변환합니다.

### 기본 사용

```
# 자동 변환: 음성 메모를 전송하면 자동으로 텍스트 변환
# 수동 변환:
/transcribe                # 음성 메모에 답장하여 수동 변환
```

### 동작 방식

1. 사용자가 Telegram에서 음성 메모 전송
2. Claudegram이 음성 파일 다운로드
3. Groq Whisper API로 변환 요청
4. 변환된 텍스트를 Claude에 전달
5. Claude가 텍스트 기반으로 응답

### 환경 변수

| 변수명 | 설명 | 필수 |
|--------|------|------|
| `GROQ_API_KEY` | Groq API 키 | Yes |
| `GROQ_TRANSCRIBE_PATH` | 변환 스크립트 경로 | No |

> [!info] 핸즈프리 워크플로우
> 음성 입력과 TTS 출력을 결합한 핸즈프리 워크플로우는 [[workflows#워크플로우 3 음성 기반 상호작용|활용 워크플로우]]를 참고하세요.

---

## 텍스트 음성 변환 (OpenAI TTS)

OpenAI의 TTS API를 사용하여 Claude의 응답을 음성으로 변환합니다.

### 기본 사용

```
/tts                       # TTS 켜기/끄기 토글
/tts nova                  # 음성을 'nova'로 변경
```

### 사용 가능한 음성

| 음성 | 특성 |
|------|------|
| alloy | 중성적, 균형 잡힌 |
| ash | 차분한 |
| ballad | 부드러운 |
| cedar | 따뜻한 |
| coral | 자연스러운 |
| echo | 깊은 |
| fable | 이야기체 |
| marin | 밝은 |
| nova | 에너지 넘치는 |
| onyx | 낮은 |
| sage | 지적인 |
| shimmer | 경쾌한 |
| verse | 다목적 |

### 환경 변수

| 변수명 | 설명 | 필수 |
|--------|------|------|
| `OPENAI_API_KEY` | OpenAI API 키 | Yes |
| `TTS_VOICE` | 기본 음성 | No (기본: alloy) |
| `TTS_MODEL` | TTS 모델 | No |

### 동작 흐름

```
Claude 텍스트 응답
    │
    ▼
TTS 활성화 확인
    │ (비활성 → 텍스트만 전송)
    │ (활성 → 계속)
    ▼
OpenAI TTS API 호출
    │
    ▼
음성 파일 생성 (OGG)
    │
    ▼
Telegram 음성 메시지로 전송
```

---

## Telegraph 출력

긴 응답이나 복잡한 테이블을 Telegraph Instant View 페이지로 생성합니다.

### 기본 사용

```
/telegraph                 # Telegraph 출력 켜기/끄기 토글
```

### 활용 시나리오

| 시나리오 | 설명 |
|----------|------|
| 긴 코드 출력 | Telegram 메시지 길이 제한 초과 시 |
| 복잡한 테이블 | Telegram에서 포맷이 깨지는 경우 |
| 레포트 형식 | 깔끔한 웹 페이지로 보고서 생성 |
| Medium 기사 | `/medium` 결과를 Instant View로 표시 |

### 특징
- Telegram 내에서 바로 열리는 Instant View 지원
- 마크다운 렌더링이 깔끔하게 적용
- 링크 클릭 한 번으로 즉시 확인 가능

---

## 관련 노트
- [[index|Claudegram 개요]] — 프로젝트 소개
- [[setup-and-config|설치 및 설정]] — 연동별 환경 변수 설정
- [[commands-and-features|명령어 및 기능]] — 연동 관련 명령어
- [[workflows|활용 워크플로우]] — 연동을 활용한 실전 워크플로우

---

> [!info] 출처
> 내부 요약 — Claudegram `src/reddit/`, `src/medium/`, `src/tts/`, `src/audio/`, `src/telegram/telegraph/` 소스 코드 기반
