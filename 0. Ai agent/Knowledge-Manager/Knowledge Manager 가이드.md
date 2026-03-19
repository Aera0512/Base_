# Knowledge Manager 가이드

> Claude Code용 종합 지식 관리 에이전트. 다양한 소스에서 콘텐츠를 수집하고, Zettelkasten 원칙에 따라 분석하여 Obsidian에 저장한다.

---

## 주요 기능

| 기능 | 설명 |
|------|------|
| **웹페이지 정리** | URL에서 핵심 내용 추출 + 노트 생성 |
| **PDF 처리** | PDF → Markdown 변환 + OCR 지원 |
| **YouTube 자막** | 영상 자막 추출 + 분석 + 노트 생성 |
| **SNS 정리** | Threads/Instagram 포스트 수집 |
| **PPT 생성** | AI 이미지 기반 슬라이드 생성 |

---

## 사용법

### 기본 명령어

```
# 웹 아티클 정리
/knowledge-manager https://example.com/article

# PDF 파일 처리
/knowledge-manager /path/to/document.pdf

# YouTube 영상 자막 정리
/knowledge-manager https://youtube.com/watch?v=XXX

# Threads 포스트 정리
/knowledge-manager https://threads.net/@user/post/123
```

### 모바일/Remote 버전 (`/knowledge-manager-m`)

키워드 기반 자동 프리셋으로 빠르게 실행:

```
# 빠른 요약
/knowledge-manager-m https://example.com 요약해줘

# 상세 분석
/knowledge-manager-m https://example.com 꼼꼼히

# 기본 정리
/knowledge-manager-m https://example.com
```

### 키워드 프리셋

| 키워드 | 상세 수준 | 노트 분할 |
|--------|-----------|-----------|
| `요약해줘` | 요약 | 단일 노트 |
| `꼼꼼히` | 상세 | 원자적 분할 |
| `기본` | 상세 | 3-tier 계층 |
| (키워드 없음) | 상세 | 3-tier 계층 |

---

## PPT/슬라이드 생성

```
# 콘텐츠에서 PPT 생성
/knowledge-manager https://example.com PPT로 만들어줘

# 스타일 지정
/knowledge-manager content.md sketch-notes 스타일로 슬라이드 생성
```

### 스타일 옵션

| 스타일 | 용도 |
|--------|------|
| `sketch-notes` | 교육/튜토리얼, 강의 |
| `blueprint` | 기술 문서, 아키텍처 |
| `corporate` | 비즈니스, 투자 발표 |
| `minimal` | 심플한 발표 |
| `chalkboard` | 교육 콘텐츠 |
| `notion` | SaaS 대시보드, B2B |

---

## 저장 구조

노트는 Obsidian vault에 Zettelkasten 스타일로 저장됨:

```
Base_/
├── Zettelkasten/
│   └── AI-연구/
│       └── MCP 프로토콜 개요 - 2026-03-19.md
├── Research/
└── Threads/
```

---

## 설정 파일

설정 파일 위치: `~/km-config.json`

### 주요 설정

```json
{
  "storage": {
    "primary": "obsidian",
    "obsidian": {
      "vaultPath": "/Users/aera/Desktop/Base_",
      "defaultFolder": "Zettelkasten"
    }
  },
  "youtube": {
    "preferredLanguage": "ko",
    "fallbackLanguage": "en"
  },
  "defaults": {
    "detailLevel": 2,
    "noteStructure": 2
  }
}
```

### 상세 수준 (`detailLevel`)
- `1` = 간략
- `2` = 보통 (기본)
- `3` = 상세

### 노트 구조 (`noteStructure`)
- `1` = 단일 노트
- `2` = 챕터별 분리 (기본)
- `3` = 3-Tier 계층
- `4` = 완전 원자화

---

## 요구사항

### 필수
- Claude Code
- Node.js 18+
- Playwright MCP 서버

### Playwright MCP 설치

```bash
claude mcp add playwright -- npx -y @anthropic-ai/mcp-playwright
```

### YouTube 자막 (선택)

```bash
pip install youtube-transcript-api yt-dlp
```

### PDF/OCR 처리 (선택)

```bash
pip install marker-pdf pytesseract pdf2image pdfplumber
```

---

## 문제 해결

### MCP 서버 상태 확인

```bash
claude mcp list
```

### 설정 파일 위치

| 환경 | 경로 |
|------|------|
| Claude Code CLI | `~/km-config.json` |
| 프로젝트별 | 프로젝트 폴더의 `km-config.json` |

---

## 관련 링크

- [GitHub 저장소](https://github.com/treylom/knowledge-manager)
- [Claude Code](https://claude.ai/claude-code)
- [MCP Protocol](https://modelcontextprotocol.io/)

---

#ai-agent #knowledge-management #claude-code #zettelkasten
