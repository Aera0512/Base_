# Obsidian-to-PDF 변환 가이드

## 개요
Obsidian 마크다운 노트를 아이패드 학습용 PDF로 변환하는 CLI 도구.

## 빠른 사용법

### Claude Code에서 (스킬)
```
/obs2pdf "파일경로"
```

### 터미널에서 직접
```bash
# 라이트 테마 (Catppuccin Latte)
node ~/Obsidian-to-pdf/dist/cli.js "파일경로" -t latte

# 다크 테마 (Catppuccin Frappé)
node ~/Obsidian-to-pdf/dist/cli.js "파일경로" -t frappe

# HTML 디버그 파일도 함께 저장
node ~/Obsidian-to-pdf/dist/cli.js "파일경로" --debug
```

### 예시
```bash
node ~/Obsidian-to-pdf/dist/cli.js ~/Desktop/Base_/"English Grammar/Present Perfect.md" -t latte
```

## 디자인 사양

| 항목 | 설정 |
|------|------|
| 페이지 크기 | iPad 11" 가로 (10.5" × 7.5") |
| 폰트 | Inter + Noto Sans KR + JetBrains Mono |
| 팔레트 | Catppuccin Latte (라이트) / Frappé (다크) |
| 여백 | 0.75in (필기 공간 확보) |
| 레이아웃 | 문법설명=1컬럼, 예문=2컬럼 |
| 페이지 분리 | h2(##)마다 새 페이지 |

## 지원하는 Obsidian 문법

### Callout (핵심 기능)
- `> [!note]- 해석` → 연한 sapphire 배경 (해석용)
- `> [!success]- 정답` → 연한 green 배경 (정답용)
- `> [!warning] 주의` → yellow 배경
- `> [!danger] 핵심 규칙` → red 배경
- `> [!tip]` → mauve 배경
- 접힌 callout(`-`)은 opacity 낮춤 → 자가 테스트에 최적

### 기타
- `![[file.mp3]]` → 🎧 아이콘으로 표시
- `[[노트링크]]` → 텍스트로 변환
- YAML 프론트매터 → 자동 제거
- 마크다운 테이블 → 깔끔한 표

## 출력 위치
- PDF는 입력 `.md` 파일과 같은 폴더에 생성
- 파일명: `{원본이름}-{테마}.pdf`

## 프로젝트 경로
- 소스코드: `~/Obsidian-to-pdf/`
- Obsidian 볼트: `~/Desktop/Base_/`

## 향후 확장 예정
- [ ] YT-to-Note 형식 지원 (프론트매터, 타임스탬프)
- [ ] Book-to-Note 형식 지원 (챕터, 멀티파트)
- [ ] 범용 Obsidian 노트 지원 (위키링크, Mermaid)
