---
title: 오픈 클로(Open WebUI)를 제대로 활용하는 방법 - 로컬과 VM
date: 2026-02-26
tags:
  - OpenWebUI
  - Docker
  - Ollama
  - LLM
  - self-hosting
  - RAG
status: research-note
confidence: high
---

# 오픈 클로(Open WebUI)를 제대로 활용하는 방법 — 로컬과 VM

> [!abstract] 요약
> Open WebUI는 Ollama 및 OpenAI 호환 API를 백엔드로 하는 자체 호스팅 AI 웹 인터페이스다. 로컬 설치는 Docker 한 줄 명령으로 가능하며 GPU 지원, CPU 전용, Ollama 번들 등 다양한 옵션이 있다. VM 배포 시 Ubuntu + Docker + Caddy 리버스 프록시 조합이 권장되며 HTTPS 자동화와 도메인 연결이 용이하다. RAG, 웹 검색, 이미지 생성, 파이프라인 등 고급 기능을 관리자 패널에서 설정할 수 있고, 다중 사용자 환경에서는 Redis + PostgreSQL 조합으로 성능과 안정성을 확보해야 한다.

---

## 1. 로컬 환경 설치

### Docker 설치 (권장)

```bash
# 기본 설치 (CPU)
docker run -d -p 3000:8080 \
  -v open-webui:/app/backend/data \
  --name open-webui \
  ghcr.io/open-webui/open-webui:main

# Nvidia GPU 지원
docker run -d -p 3000:8080 --gpus all \
  -v open-webui:/app/backend/data \
  --name open-webui \
  ghcr.io/open-webui/open-webui:cuda

# Ollama 번들 (단일 이미지)
docker run -d -p 3000:8080 \
  -v open-webui:/app/backend/data \
  --name open-webui \
  ghcr.io/open-webui/open-webui:ollama
```

### Python pip 설치

```bash
pip install open-webui
open-webui serve
```

### 최소 시스템 요구사항

| 항목 | 최소 | 권장 |
|------|------|------|
| RAM | 8GB | 16GB |
| 저장공간 | 10GB+ | - |

> [!tip] 첫 접속
> `http://localhost:3000` 접속 → 최초 접속 시 관리자 계정 생성
> Ollama 없이도 OpenAI API, Gemini 등 외부 API 연결로 독립 실행 가능

---

## 2. 핵심 기능과 설정

### 주요 기능 목록

| 기능 | 설명 |
|------|------|
| **멀티 모델 지원** | Ollama, OpenAI, Gemini 등 다양한 백엔드 동시 연결 |
| **RAG** | ChromaDB, Milvus, Qdrant 등 9가지 벡터 DB 지원 |
| **웹 검색 통합** | SearXNG, Brave, Google 등 15개+ 제공자 |
| **이미지 생성** | DALL-E, ComfyUI, AUTOMATIC1111 연동 |
| **파이프라인** | 커스텀 Python 함수로 입출력 처리 확장 |
| **관리자 패널** | 사용자/그룹 권한, LDAP 인증, SCIM 2.0 |

### 성능 최적화 팁

> [!important] 성능 설정
> - `ENABLE_REALTIME_CHAT_SAVE=False` 설정 권장
> - 다중 워커: Redis 세션 동기화 사용
> - DB: SQLite 대신 **PostgreSQL** 권장
> - 벡터 DB: 프로덕션에서는 **Milvus** 권장

---

## 3. VM 환경 Docker 배포

### Azure VM 기준 단계별 절차

1. **VM 생성**: Ubuntu Pro 24.04 (LLM 로컬 실행 시 디스크 용량 확대)
2. **SSH 접속 후 Docker 실행**:

```bash
docker run -d --name open-webui \
  --network=host \
  --add-host=host.docker.internal:host-gateway \
  -e PORT=8080 \
  -v open-webui:/app/backend/data \
  --restart always \
  ghcr.io/open-webui/open-webui:dev
```

3. **Caddy 리버스 프록시**: 도메인 연결 + 자동 HTTPS
4. **방화벽**: 포트 80/443 허용, 포트 8080 직접 접근 차단

> [!warning] 데이터 영속성
> 반드시 `-v open-webui:/app/backend/data` 볼륨 마운트 필요!
> Docker Compose로 ChromaDB, Ollama, OpenWebUI를 분리 운영 가능

---

## 4. 고급 기능 활용

### RAG (검색 증강 생성)

1. **Workspace > Knowledge > "+ Create a Knowledge Base"** 에서 지식베이스 생성
2. PDF, Word, Excel, PPT 등 문서 업로드
3. 채팅에서 **`#` 키**로 지식베이스 참조
4. URL 직접 입력으로 웹 콘텐츠 실시간 통합
5. 고급: 하이브리드 검색 + 리랭킹 지원

### 멀티모달 / 이미지 생성

- DALL-E, Gemini, ComfyUI, AUTOMATIC1111 연동
- **Native Tool Calling**으로 모델이 독립적으로 이미지 생성/정제

### 웹 검색

- **Native Function Calling** 사용 시 모델이 순차적 다중 검색 수행
- `fetch_url` 도구로 전체 페이지 읽기 → 심층 리서치

### 파이프라인 프레임워크

- **inlet 함수**: LLM 전송 전 사용자 입력 전처리
- **outlet 함수**: 모델 출력 후처리

---

## 5. 로컬 vs VM 비교

| 구분 | 로컬 배포 | VM 배포 |
|------|-----------|---------|
| **프라이버시** | 완전 보장 | 클라우드 의존 |
| **인터넷** | 오프라인 가능 | 필수 |
| **외부 접근** | 불가 | 가능 |
| **공유** | 개인 전용 | 팀 공유 가능 |
| **GPU** | 로컬 GPU 직접 활용 | 고사양 VM 필요 |
| **비용** | 전기세 | 클라우드 요금 |
| **가용성** | PC 켜야 사용 | 24/7 상시 가동 |
| **HTTPS** | 불필요 | Caddy/Nginx로 자동화 |
| **권장 DB** | SQLite 가능 | PostgreSQL + Redis |

### 권장 구성

> [!example] 로컬
> Ollama + Open WebUI 번들 Docker 이미지, GPU 있으면 `--gpus all`

> [!example] VM (다중 사용자)
> Ubuntu + Docker + Caddy + Redis + PostgreSQL

### 공통 권장사항

- 데이터 볼륨 마운트 필수: `-v open-webui:/app/backend/data`
- `--restart always` 옵션으로 자동 재시작
- 미사용 기능(이미지 생성, 코드 인터프리터 등) 비활성화 → 리소스 절약

---

## 연결 개념

- [[Ollama]] — 로컬 LLM 추론 엔진
- [[RAG (Retrieval-Augmented Generation)]]
- [[Docker]] / Docker Compose 컨테이너화
- [[LLM 프라이버시]] 및 자체 호스팅
- [[OpenAI API]] 호환 인터페이스
- 벡터 데이터베이스: [[ChromaDB]], [[Milvus]], [[Qdrant]]
- 역방향 프록시: [[Caddy]], [[Nginx]]

---

## 추가 탐구 과제

- [ ] Windows WSL2 기반 설치 세부 가이드
- [ ] Mac Apple Silicon (M1/M2/M3/M4) 최적화 설정
- [ ] Kubernetes/Helm 배포 상세 절차
- [ ] 기업 환경 LDAP/SSO 통합 설정
- [ ] 파이프라인 커스텀 개발 심화
- [ ] 비용 최적화를 위한 클라우드 VM 선택 기준

---

## 참고 자료

1. [Open WebUI 공식 문서 - Getting Started](https://docs.openwebui.com/getting-started/quick-start/)
2. [Open WebUI 핵심 기능 목록](https://docs.openwebui.com/features/)
3. [Open WebUI 성능 최적화 가이드](https://docs.openwebui.com/troubleshooting/performance/)
4. [Azure VM에 Open WebUI Docker 배포](https://techcommunity.microsoft.com/blog/educatordeveloperblog/deploy-open-web-ui-on-azure-vm-via-docker-a-step-by-step-guide-with-custom-domai/4387717)
5. [라이니즈 - Open WebUI 로컬 LLM 웹서비스 구축](https://www.lainyzine.com/ko/article/building-llm-web-service-with-open-webui/)
6. [Open WebUI 설치와 기본 세팅](https://whdrns2013.github.io/ai/20260113_004_install_openwebui/)
7. [Ultimate Local AI Setup Guide](https://www.robwillis.info/2025/05/ultimate-local-ai-setup-guide-ubuntu-ollama-open-webui/)
8. [Open WebUI RAG 튜토리얼](https://docs.openwebui.com/tutorials/tips/rag-tutorial/)
9. [Open WebUI GitHub](https://github.com/open-webui/open-webui)
