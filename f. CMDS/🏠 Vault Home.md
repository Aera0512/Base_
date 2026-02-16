# 🏠 Vault Home

CMDS 메인 허브 (한눈에 보기)

## 시작
- [[00. START HERE]]
- [[10. CMDS Process/01. Hub Navigator|Hub Navigator]]

## 핵심 허브 7개
- [[00. Inbox/Hub - 00. Inbox|Inbox]]
- [[20. Literature Notes/Hub - 20. Literature Notes|Literature Notes]]
- [[30. Permanent Notes/Hub - 30. Permanent Notes|Permanent Notes]]
- [[40. Docs/Hub - 40. Docs|Docs]]
- [[70. Collections/Hub - 70. Collections|Collections]]
- [[80. References/Hub - 80. References|References]]
- [[90. Settings/Hub - 90. Settings|Settings]]

## 연결성 관리
- [[10. CMDS Process/📊 Vault 연결성 대시보드]]
- [[10. CMDS Process/연결 지도 - CMDS]]

## 최근 업데이트 (자동)
```dataview
TABLE file.folder AS Folder
FROM "f. CMDS"
WHERE !contains(file.name, "Hub - ") AND file.name != "🏠 Vault Home" AND file.name != "00. START HERE"
SORT file.mtime DESC
LIMIT 25
```
