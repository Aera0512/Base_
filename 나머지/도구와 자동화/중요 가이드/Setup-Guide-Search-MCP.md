---
type: guide
date_created: 2026-03-07
tags:
  - setup
  - mcp
  - infrastructure
  - guide
status: active
---

# 검색 MCP 인프라 설정 가이드

book-to-note / yt-to-note 스킬의 검색·추론 품질 강화를 위한 설정 가이드.

---

## 아키텍처 개요

```mermaid
graph LR
    subgraph Local[로컬 Mac]
        CC[Claude Code<br/>Opus ultrathink]
        CC --> S[MCP: searxng]
        CC --> J[MCP: jina]
        CC --> D[MCP: ddg]
        CC --> OB[MCP: obsidian]
        CC --> YT[MCP: youtube-transcript]
    end

    subgraph VPS[VPS 4GB]
        SX[SearXNG :8080<br/>~512MB RAM]
    end

    subgraph Cloud[클라우드 무료]
        JA[Jina AI API<br/>500 RPM]
    end

    S -->|HTTP| SX
    J -->|HTTPS| JA
```

### 검색 폴백 체인

```
검색: SearXNG → DuckDuckGo → WebSearch (Claude 내장)
전문 읽기: Jina read_url() → DDG fetch_content() → WebFetch (Claude 내장)
```

---

## 설정 항목 체크리스트

- [ ] **Step 1**: VPS에 SearXNG 설치
- [ ] **Step 2**: Jina API 키 발급
- [ ] **Step 3**: uvx 설치 (로컬)
- [ ] **Step 4**: mcp.json에 VPS IP 입력
- [ ] **Step 5**: JINA_API_KEY 환경변수 설정
- [ ] **Step 6**: 연결 테스트

---

## Step 1: VPS에 SearXNG 설치

### 1-1. SSH 접속

```bash
ssh user@YOUR_VPS_IP
```

### 1-2. Docker Compose 설정

```bash
mkdir -p ~/searxng && cd ~/searxng

cat > docker-compose.yml << 'EOF'
services:
  searxng:
    image: searxng/searxng:latest
    ports:
      - "8080:8080"
    volumes:
      - ./searxng:/etc/searxng:rw
    environment:
      - SEARXNG_SECRET=GENERATE_RANDOM_HEX
    restart: unless-stopped
EOF
```

> [!warning] `SEARXNG_SECRET` 값 변경
> `openssl rand -hex 32` 로 생성한 랜덤 hex 값으로 교체하세요.

### 1-3. SearXNG 설정 파일 생성

```bash
mkdir -p searxng

cat > searxng/settings.yml << 'EOF'
use_default_settings: true
server:
  limiter: false
  image_proxy: false
search:
  formats:
    - html
    - json
engines:
  - name: google
    disabled: true  # Google 차단 회피 — Bing+DDG+Brave로 충분
EOF
```

### 1-4. 실행

```bash
docker compose up -d
```

### 1-5. 방화벽 확인

```bash
# UFW 사용 시
sudo ufw allow 8080/tcp

# 또는 iptables
sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
```

> [!tip] 보안 강화 (선택)
> 특정 IP만 허용하려면:
> ```bash
> sudo ufw allow from YOUR_LOCAL_IP to any port 8080
> ```

### 1-6. 동작 확인

```bash
curl "http://localhost:8080/search?q=test&format=json" | head -c 200
```

JSON 응답이 오면 성공.

---

## Step 2: Jina API 키 발급

1. https://jina.ai/api-dashboard/ 접속
2. 회원가입 (무료)
3. API Key 발급

> [!info] Jina 무료 티어
> - 500 RPM (분당 요청)
> - 10M 토큰/월
> - 비용: $0

---

## Step 3: uvx 설치 (로컬 Mac)

`uvx`는 `uv` 패키지 매니저의 실행 도구입니다. SearXNG MCP와 DuckDuckGo MCP 실행에 필요합니다.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

설치 확인:
```bash
uvx --version
```

---

## Step 4: mcp.json에 VPS IP 입력

파일 위치: `~/.claude/mcp.json`

`VPS_IP` 부분을 실제 VPS IP 주소로 교체:

```json
"searxng": {
  "command": "uvx",
  "args": ["mcp-searxng"],
  "env": {
    "SEARXNG_URL": "http://123.456.789.0:8080"  // ← 여기 교체
  }
}
```

---

## Step 5: JINA_API_KEY 환경변수 설정

### 방법 A: 쉘 프로필에 추가 (권장)

```bash
# ~/.zshrc 또는 ~/.bashrc에 추가
echo 'export JINA_API_KEY="jina_xxxxxxxxxxxxxxxx"' >> ~/.zshrc
source ~/.zshrc
```

### 방법 B: mcp.json에 직접 입력

```json
"jina": {
  "type": "http",
  "url": "https://mcp.jina.ai/v1?exclude_tags=parallel,utility",
  "headers": {
    "Authorization": "Bearer jina_xxxxxxxxxxxxxxxx"  // ← 직접 입력
  }
}
```

> [!warning] 방법 B 주의
> API 키가 파일에 평문으로 저장됩니다. 보안이 중요하면 방법 A를 사용하세요.

---

## Step 6: 연결 테스트

### 6-1. SearXNG 원격 접속 테스트 (로컬에서)

```bash
curl "http://YOUR_VPS_IP:8080/search?q=test&format=json" | head -c 200
```

### 6-2. Claude Code MCP 연결 확인

Claude Code를 재시작한 후:

```bash
claude mcp list
```

다음 6개가 모두 표시되어야 합니다:
- `context7`
- `obsidian`
- `nano-banana`
- `searxng` ← 신규
- `jina` ← 신규
- `ddg` ← 신규

### 6-3. 기능 테스트

Claude Code에서 다음을 실행하여 검증:

**book-to-note 테스트:**
```
/book-to-note Atomic Habits
```
- SearXNG 검색이 동작하는지 확인
- Jina Reader로 서평 페이지 전문을 읽어오는지 확인
- 서브에이전트가 `source_reliability` 필드를 포함한 JSON 반환하는지 확인
- Step 5.5 품질 자가검증이 실행되는지 확인

**yt-to-note 테스트:**
```
/yt-to-note [인기 knowledge 영상 URL]
```
- Step 3.5 배경 지식 검색이 실행되는지 확인
- 보충자료가 Jina Reader로 전문 읽기되는지 확인

### 6-4. 폴백 테스트

SearXNG Docker를 중단하고 스킬 실행:

```bash
# VPS에서
docker compose -f ~/searxng/docker-compose.yml stop
```

→ DuckDuckGo MCP로 자동 폴백되는지 확인

---

## 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| `searxng` MCP 연결 실패 | VPS 방화벽 또는 Docker 미실행 | `docker compose up -d` 재실행, 방화벽 확인 |
| `jina` MCP 인증 실패 | API 키 미설정 또는 만료 | `JINA_API_KEY` 환경변수 확인 |
| `ddg` MCP 실행 실패 | `uvx` 미설치 | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| 검색 결과 비어있음 | SearXNG 엔진 설정 문제 | `searxng/settings.yml`에서 엔진 활성화 확인 |
| Jina `read_url()` 타임아웃 | 대상 사이트 차단 | DDG `fetch_content()` 폴백 자동 작동 |

---

## 변경된 스킬 요약

### book-to-note 변경점
- **Step 2**: WebSearch 5~6회 → 3단계 적응적 심층 검색 (SearXNG + Jina Reader)
- **Step 4**: 서브에이전트에 Ultra Think 추론 지시 + 출처 신뢰도 평가
- **Step 5.5**: 품질 자가검증 체크리스트 (신규)
- **Step 6**: Jina `read_url()`로 보충자료 전문 읽기

### yt-to-note 변경점
- **Step 3**: 서브에이전트에 Ultra Think 추론 지시
- **Step 3.5**: 배경 지식 보강 검색 (신규) — 영상 내용의 정확성 검증
- **Step 5**: Jina `read_url()`로 보충자료 전문 읽기

### 공통
- 검색 폴백 체인: SearXNG → DuckDuckGo → WebSearch
- 전문 읽기 폴백: Jina → DDG → WebFetch
- 비용: **$0** (모두 무료 또는 셀프호스팅)
