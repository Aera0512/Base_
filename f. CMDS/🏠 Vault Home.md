# 🏠 Vault Home

이 페이지는 Vault 전체의 메인 허브입니다.

## 핵심 허브
```dataview
LIST FROM "f. CMDS"
WHERE contains(file.name, "Hub - ")
SORT file.name ASC
```

## 최근 업데이트 노트
```dataview
TABLE file.folder AS Folder
FROM "f. CMDS"
WHERE !contains(file.name, "Hub - ") AND file.name != "🏠 Vault Home"
SORT file.mtime DESC
LIMIT 40
```

## 연결성 대시보드
- [[📊 Vault 연결성 대시보드]]
