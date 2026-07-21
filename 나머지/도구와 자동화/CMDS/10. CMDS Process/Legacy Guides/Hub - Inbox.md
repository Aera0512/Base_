# Hub - Inbox

상위: [[나머지/도구와 자동화/CMDS/10. CMDS Process/Legacy Guides/CMDS Home]]

## 주요 폴더
- `00. Inbox/01. Daily Notes`
- `00. Inbox/02. Weekly Notes`
- `00. Inbox/03. Claude Code`
- `00. Inbox/06. GenAI Chats`

## Dataview (최근 Inbox 노트)
```dataview
LIST FROM "f. CMDS/00. Inbox"
SORT file.mtime DESC
LIMIT 30
```
