# 📊 Vault 연결성 대시보드

상위: [[나머지/도구와 자동화/CMDS/🏠 Vault Home]]

## 고립 노트 (Inlinks = 0)
```dataview
TABLE file.folder AS Folder
FROM "f. CMDS"
WHERE length(file.inlinks) = 0 AND !contains(file.name, "Hub - ") AND file.name != "🏠 Vault Home"
SORT file.mtime DESC
```

## 연결 부족 노트 (Outlinks < 2)
```dataview
TABLE length(file.outlinks) AS Outlinks, file.folder AS Folder
FROM "f. CMDS"
WHERE length(file.outlinks) < 2 AND !contains(file.name, "Hub - ") AND file.name != "🏠 Vault Home"
SORT file.mtime DESC
```

## 허브 미연결 의심 노트
```dataview
TABLE file.folder AS Folder
FROM "f. CMDS"
WHERE !contains(file.content, "허브:") AND !contains(file.name, "Hub - ") AND file.name != "🏠 Vault Home"
SORT file.mtime DESC
```
