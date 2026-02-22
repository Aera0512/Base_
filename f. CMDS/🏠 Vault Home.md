---
cssclass: dashboard
---
ㅌ

## 📅 Today
- **Date:** `= date(today)`
- **Quick Links:**
  - [[Inbox]]
  - [[Important]]
  - [[b. Dairy]]
  - [[d. Templates]]

---

## 📝 최근 노트
```dataview
LIST
FROM ""
WHERE !contains(file.path, "Templates") AND !contains(file.path, ".trash")
SORT file.mtime DESC
LIMIT 12
```

---

## 📚 공부 태그 노트
```dataview
LIST
FROM ""
WHERE contains(file.tags, "공부") OR contains(file.tags, "study")
SORT file.mtime DESC
LIMIT 10
```

---

## 🗂️ 주요 섹션
- [[Inbox]]
- [[Important]]
- [[a. Obsidian]]
- [[b. Dairy]]
- [[c. Attached file]]
- [[d. Templates]]
- [[e. Canvases]]
- [[f. CMDS]]

---

## 🔎 검색 힌트
- 최근 파일: 위 Dataview 자동 목록
- 태그: #공부 / #study

> 필요하면 추가 섹션(프로젝트, 영역, 리소스)을 더 붙일 수 있어.
