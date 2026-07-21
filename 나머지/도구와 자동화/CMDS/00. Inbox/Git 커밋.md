---
tags:
  - Git
  - Claude-Code
  - 개발
status: active
created: '2026-02-24'
---
# Git 커밋 — 프로젝트 세이브 포인트

## 최초 1번 (프로젝트 시작할 때)

```bash
cd ~/Claude_code/프로젝트폴더
git init
git add .
git commit -m "초기 세팅 완료"
```

## 작업 중간중간 (잘 되는 상태마다)

```bash
git add .
git commit -m "설명 메모"
```

## 망했을 때 되돌리기

```bash
# 마지막 커밋으로 전부 되돌리기
git checkout .

# 커밋 목록 보기
git log --oneline

# 특정 시점으로 되돌리기
git checkout abc1234
```

## 핵심

- Claude Code가 파일 직접 수정하니까 예상 못한 변경 발생 가능
- "잘 되는 상태"마다 커밋 = 게임 세이브
- 새 프로젝트 시작할 때 `git init` + 첫 커밋 습관화 (3초)
