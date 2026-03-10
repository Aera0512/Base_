# Obsidian-Notion Sync Plan

## Project: 양방향 실시간 동기화 시스템

### Tech Stack
- Python + notion-sdk-py + watchdog
- Team: 4 workers + Ralph + Codex review

### Team Distribution
| Worker | Scope | Files |
|--------|-------|-------|
| Worker-1 | Notion API | src/notion/ |
| Worker-2 | Obsidian Parser | src/obsidian/ |
| Worker-3 | Sync Engine | src/sync/ |
| Worker-4 | Realtime Watcher | watcher, main.py |

### Tag Mapping
- #q1 → Importance: High, Urgency: High
- #q2 → Importance: High, Urgency: Low
- #q3 → Importance: Low, Urgency: Low
- #q4 → Importance: Low, Urgency: High

### Project Location
`/Users/aera/Desktop/Base_/.scripts/obsidian-notion-sync/`

### Prerequisites
1. Create Notion Internal Integration
2. Get API Key
3. Connect Integration to TO-DO database
4. Update maxAgents: 3 → 4 in .omc-config.json

### Execute
```
/team 4:executor ralph "Obsidian-Notion 양방향 동기화 시스템 구축"
```
