---
tags:
  - guide
  - AI
---

# 🤖 AI 가이드 - Edit 사용

> **이 노트를 프롬프트에 태그하세요!**

---

## ⚠️ 필수 규칙 - MCP 도구 문제

**MCP Obsidian 쓰기 도구는 실제로 파일을 생성/수정하지 못합니다.**

### 🔍 문제 상황
- MCP 도구 (`mcp__obsidian__write_note`, `mcp__obsidian__patch_note`)는 **"성공"이라고 응답**함
- MCP `list_directory`에서도 파일이 **보이는 것처럼 보임**
- **하지만 실제 파일 시스템에는 파일이 생성/수정되지 않음** ❌

### ✅ 해결 방법
**반드시 Claude Code의 기본 Write/Edit 도구를 사용하세요:**

| ❌ 사용 금지 (작동 안 함) | ✅ 반드시 사용 (실제로 작동함) |
|-------------|---------------|
| `mcp__obsidian__write_note` | `Write` - 새 파일 생성 / 전체 덮어쓰기 |
| `mcp__obsidian__patch_note` | `Edit` - 부분 수정 (권장) |

### 💡 핵심
- **Write/Edit 도구**는 실제 파일 시스템에 직접 쓰기를 수행합니다
- 파일 생성 후 `ls` 명령어로 실제 생성되었는지 확인 가능
- MCP 도구는 읽기(`read_note`, `search_notes` 등)는 정상 작동

---

## 📝 Edit 도구 사용법

```
Edit 도구 파라미터:
- file_path: 절대 경로 사용
- old_string: 바꿀 기존 텍스트 (정확히 일치해야 함)
- new_string: 새로운 텍스트
```

**예시:**
- 파일 경로: `/Users/aera/Documents/Obsidian/Yesung_Obsidian/노트경로.md`
- 테이블에 행 추가할 때: 기존 행 포함해서 old_string 지정 → 새 행 추가된 new_string으로 교체

---

## 📌 "단어 및 표현 정리해줘" 워크플로우

1. [[영어 LC]]의 **Expressions** 섹션 내용 → [[영어 표현 모음]]으로 옮기기
2. [[영어 LC]]의 **Words** 섹션 내용 → [[영어 단어 모음]]으로 옮기기
3. 옮긴 후 [[영어 LC]]의 해당 행은 비우거나 삭제

**반드시 Edit 도구로 수정할 것!**
