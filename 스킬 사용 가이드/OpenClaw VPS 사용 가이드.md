---
tags:
  - guide
  - openclaw
  - vps
  - workflow
  - important
created: '2026-03-05'
aliases:
  - VPS 가이드
  - OpenClaw 사용법
---
ㅑㅡㅔ
# OpenClaw VPS 사용 가이드

> VPS에서 Claude Code로 YT-to-Note / Book-to-Note 스킬을 사용하는 방법
> **최종 수정**: 2026-03-05

---

## 한 줄 요약

맥북이 꺼져 있어도, VPS에 SSH 접속해서 Claude Code를 실행하면 학습 노트가 자동으로 볼트에 동기화된다.

---

## 사전 조건

| 항목 | 상태 |
|------|------|
| OpenClaw VPS | 가동 중 |
| Claude Code | VPS에 설치됨 |
| 볼트 git sync | 양방향 자동 동기화 설정됨 |
| YouTube Transcript MCP | 아래에서 확인 |

---

## 초기 설정 (최초 1회)

### 1. YouTube Transcript MCP 확인

```bash
claude mcp list
```

없으면 설치:
```bash
claude mcp add --scope user youtube-transcript npx @fabriqa.ai/youtube-transcript-mcp@latest
```

### 2. 볼트 루트에서 Claude Code 실행 확인

```bash
cd ~/Desktop/Base_   # 또는 볼트가 동기화된 경로
claude
```

실행 후 슬래시 커맨드 인식 확인:
```
/yt-to-note
/book-to-note
```

> [!tip] 볼트 루트에서 실행해야 `.claude/commands/`가 프로젝트 레벨로 인식된다.
> 유저 레벨(`~/.claude/commands/`)에도 복사해두면 어디서든 사용 가능.

### 3. 유저 레벨 커맨드 등록 (선택)

볼트 폴더 밖에서도 쓰고 싶으면:
```bash
mkdir -p ~/.claude/commands && cp ~/Desktop/Base_/.claude/commands/*.md ~/.claude/commands/
```

---

## 사용법

### YT-to-Note

```bash
claude
```

```
/yt-to-note
이 영상 노트 만들어줘: https://www.youtube.com/watch?v=VIDEO_ID
```

또는 슬래시 커맨드 없이:
```
이 영상 tech 노트로 정리해줘: https://youtu.be/VIDEO_ID
```

### Book-to-Note

```
/book-to-note
아토믹 해빗 책 노트 만들어줘
```

또는:
```
제임스 클리어의 아토믹 해빗 knowledge 노트로 정리해줘
```

### 결과 확인

노트가 볼트에 저장되면 git sync가 로컬 맥북으로 자동 동기화.
맥북에서 Obsidian 열면 바로 확인 가능.

---

## VPS vs 로컬 차이점

| 항목 | 로컬 (Cowork) | VPS (Claude Code) |
|------|:---:|:---:|
| YT-to-Note | ⭕ | ⭕ |
| Book-to-Note | ⭕ | ⭕ |
| Anki 카드 생성 | ⭕ | ❌ (AnkiConnect 필요) |
| Obsidian MCP | ⭕ | ❌ (파일 직접 R/W) |
| 스케줄 태스크 | ⭕ | cron으로 대체 가능 |
| 오프라인 맥북 | ❌ | ⭕ |

### VPS에서 안 되는 것

- **Anki 카드 생성**: AnkiConnect가 Anki GUI 앱 필요 → VPS에서 불가
- **Obsidian MCP 호출**: Obsidian 앱이 없으므로 `mcp__obsidian__*` 사용 불가

### VPS에서의 대체 동작

Claude Code는 Obsidian MCP 대신 **파일을 직접 읽고 쓴다**:
- 노트 읽기: `cat`, `Read` 도구로 .md 파일 직접 읽기
- 노트 쓰기: 파일 시스템에 직접 .md 파일 생성
- 노트 검색: `grep`, `Grep` 도구로 볼트 내 검색
- 내부 링크: 파일 목록 기반으로 `[[]]` 링크 생성

스킬이 `mcp__obsidian__read_note`를 호출하면 Claude Code가 알아서 파일 직접 읽기로 대체한다.

---

## 팁

### tmux로 백그라운드 실행

SSH 끊겨도 세션 유지:
```bash
tmux new -s claude
claude
# 작업 진행...
# Ctrl+B → D 로 detach
```

다시 연결:
```bash
tmux attach -t claude
```

### 여러 영상 한 번에 처리

```
다음 영상들 전부 노트로 만들어줘:
1. https://youtu.be/VIDEO_ID_1
2. https://youtu.be/VIDEO_ID_2
3. https://youtu.be/VIDEO_ID_3
```

### git sync 수동 트리거

자동 동기화가 늦을 때:
```bash
cd ~/Desktop/Base_ && git add -A && git commit -m "VPS: 노트 생성" && git push
```

---

## 관련 문서

- [[자동화 에이전트 통합 사용 가이드]] — 전체 에이전트 마스터 가이드
- [[YT-to-Note 사용 가이드]] — 유튜브 노트 상세
- [[Book-to-Note 사용 가이드]] — 도서 노트 상세
- [[Claude Code 스킬 등록 가이드]] — 커맨드 등록 방법
