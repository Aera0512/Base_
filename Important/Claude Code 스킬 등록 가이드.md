# Claude Code 스킬(커맨드) 등록 가이드

## 문제

Obsidian 볼트의 `.claude/skills/`에 스킬을 만들어도 Claude Code가 인식하지 못함.
Claude Code는 **`.claude/commands/`** 디렉토리에서 슬래시 커맨드를 찾기 때문.

## 구조 차이

| 위치 | 용도 | 인식 범위 |
|------|------|----------|
| `~/.claude/commands/` | 유저 레벨 커맨드 | 어디서든 사용 가능 |
| `{프로젝트}/.claude/commands/` | 프로젝트 레벨 커맨드 | 해당 폴더에서 claude 실행 시만 |
| `.claude/skills/` | Cowork 스킬 전용 | Claude Code에서 인식 안 됨 |

## 해결: 원라인 복사 명령어

터미널에서 아래 명령어를 실행하면 볼트의 모든 스킬을 유저 레벨 커맨드로 등록합니다.

### 전체 스킬 일괄 등록

```bash
VAULT="$HOME/Desktop/Base_" && mkdir -p ~/.claude/commands && for skill in "$VAULT"/.claude/skills/*/SKILL.md; do name=$(basename "$(dirname "$skill")"); cp "$VAULT/.claude/commands/$name.md" ~/.claude/commands/ 2>/dev/null || cp "$skill" ~/.claude/commands/"$name.md"; done && echo "등록 완료: $(ls ~/.claude/commands/*.md | wc -l)개 커맨드"
```

### 개별 스킬 등록

```bash
# {스킬명} 부분만 바꿔서 사용
mkdir -p ~/.claude/commands && cp "$HOME/Desktop/Base_/.claude/commands/{스킬명}.md" ~/.claude/commands/
```

### 현재 등록된 커맨드 확인

```bash
ls ~/.claude/commands/
```

## 새 스킬 만들 때 체크리스트

1. `.claude/skills/{스킬명}/SKILL.md` — 스킬 본체 + references/ (Cowork용)
2. `.claude/commands/{스킬명}.md` — Claude Code 커맨드 파일 (SKILL.md 내용 복사, 참조 경로를 `.claude/skills/{스킬명}/references/`로 수정)
3. 터미널에서 개별 등록 명령어 실행
4. Claude Code 재시작 후 `/{스킬명}` 으로 확인

## 참고

- 레퍼런스 파일(프롬프트, 스키마 등)은 `.claude/skills/{스킬명}/references/`에 그대로 둠
- 커맨드 파일에서 참조 경로만 절대경로(`.claude/skills/...`)로 맞추면 Claude Code가 실행 중 자동으로 읽음
- Claude Code를 **볼트 루트에서 실행**하면 프로젝트 레벨(`.claude/commands/`)도 자동 인식됨
