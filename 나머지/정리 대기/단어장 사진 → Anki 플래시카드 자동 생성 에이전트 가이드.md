---
created: '2026-02-15'
tags:
  - 프로젝트
  - 자동화
  - Anki
  - 영어학습
status: 진행예정
---
# 📸 단어장 사진 → Anki 플래시카드 자동 생성 에이전트 만들기

> **대상**: 코딩 경험 없는 초보자 | **환경**: macOS + iPhone | **난이도**: ⭐⭐ (바이브 코딩)
> **최종 목표**: 단어장 사진을 찍으면 → AI가 자동으로 Anki 플래시카드(.apkg)를 만들어주는 시스템

---

## 🗺️ 전체 로드맵

```
📸 사진 촬영 → 🤖 AI가 텍스트 추출 → 📊 단어 정리 → 🃏 Anki 카드 생성 → 📱 iPhone에서 복습
   (iPhone)      (Vision API)        (JSON 변환)    (genanki)         (AnkiMobile)
```

**핵심 3단계**: 눈(OCR/Vision) → 뇌(LLM 처리) → 손(genanki)

---

## 🧰 도구 총정리

### 1. Google Antigravity — 메인 개발 환경
- Google의 에이전트 기반 AI IDE (2025.11 출시)
- 🆓 퍼블릭 프리뷰 완전 무료
- Gemini 3 Pro 기반, Claude Sonnet 4.5도 선택 가능
- antigravity.google에서 다운로드

### 2. Claude Code — 보조 디버깅 도구
- 터미널 기반 AI 코딩 어시스턴트
- Claude Pro $20/월 필요
- `npm install -g @anthropic-ai/claude-code`

### 3. OpenAI Codex — 대안 도구
- 클라우드 기반 코딩 에이전트
- ChatGPT Plus $20/월 필요
- GitHub 연동 후 병렬 작업 가능

### 4. 추가 필수 도구
- Python 3 + genanki (🆓)
- OpenAI API (종량제 ~$1-3/월)
- Anki macOS (🆓) + AnkiMobile ($24.99 1회)

---

자세한 가이드는 다운로드 파일 참고.

#프로젝트 #자동화 #Anki #영어학습 #AI에이전트
