---
tags:
  - project
  - routine
  - environment
  - skill
  - neuroscience
  - claude-cowork
created: '2026-03-07'
version: '0.1'
aliases:
  - 루틴-환경 스킬 PRD
pipeline: pipeline-quick
phase: 4-implement
---
# Routine & Environment Skills PRD

> **프로젝트명**: 루틴 최적화 & 환경 설계 스킬
> **목적**: 뇌과학 기반으로 일일 루틴을 최적화하고, 습관/목표 달성을 위한 환경을 강제적으로 설계하는 Cowork 스킬 2종 개발
> **아키텍처**: Claude Cowork 스킬
> **파이프라인**: pipeline-quick (소형)
> **최종 수정**: 2026-03-07 | 버전: 0.1 (초안)

---

## 스킬 개요

| 항목 | routine-optimizer | environment-architect |
|------|-------------------|----------------------|
| **목적** | 일일 스케줄 뇌과학적 최적화 | 습관/목표 달성 환경 강제 설계 |
| **핵심 MCP** | Google Calendar, Gmail | WebSearch |
| **선택 MCP** | Notion | Google Calendar |
| **작동 모드** | 3가지 (분석/Rize/재조정) | 단일 (목적 입력 → 설계 출력) |
| **출력 형식** | 개선안 선택지 | 환경 변경 체크리스트 |
| **상세 문서** | [[나머지/도구와 자동화/CMDS/📦 500 Projects/Routine-Environment-Skills/routine-optimizer-SKILL]] | [[나머지/도구와 자동화/CMDS/📦 500 Projects/Routine-Environment-Skills/environment-architect-SKILL]] |
| **레퍼런스** | [[나머지/도구와 자동화/CMDS/📦 500 Projects/Routine-Environment-Skills/neuroscience-framework]] | [[나머지/도구와 자동화/CMDS/📦 500 Projects/Routine-Environment-Skills/base-framework]] |

---

## 필수 연결

- [x] Google Calendar MCP (Notion Calendar 연동됨)
- [ ] Gmail MCP (Rize 리포트 검색용)
- [ ] Notion MCP (선택적)

---

## 개발 현황

| 단계 | 상태 | 비고 |
|------|------|------|
| 뇌과학 리서치 | ✅ 완료 | 루틴 + 환경 설계 모두 |
| SKILL.md 작성 | ✅ 완료 | 초안 v0.1 |
| 레퍼런스 파일 작성 | ✅ 완료 | neuroscience-framework + base-framework |
| 테스트 실행 (iteration-1) | ✅ 완료 | 3개 테스트 케이스 |
| 그레이딩 | ✅ 완료 | 모든 assertion 통과 |
| 피드백 & 개선 | 🔄 진행 중 | 사용자 피드백 대기 |
| 패키징 & 설치 | ⬜ 대기 | |

---

## 테스트 결과 (iteration-1)

| 테스트 | with_skill | without_skill |
|--------|-----------|---------------|
| Rize 리포트 분석 | 5/5 ✅ | 5/5 ✅ |
| 캘린더 루틴 검토 | 6/6 ✅ | 6/6 ✅ |
| 실행력 환경 설계 | 9/9 ✅ | 9/9 ✅ |

> 정량적으로 모두 통과. 질적 비교 및 상세 분석은 [[나머지/도구와 자동화/AI Agent/REA/쓸데 없는 파일/eval-results-iteration-1]] 참고. (REA 폴더에 저장)

---

## 관련 문서

- [[나머지/도구와 자동화/CMDS/📖 400 Methodologies/AI 소형 프로젝트 빠른 가이드 (pipeline-quick)]]
- [[나머지/도구와 자동화/CMDS/📖 400 Methodologies/AI 프로젝트 기획-실행 파이프라인 (pipeline-full)]]
- [[나머지/시스템/템플릿/CLAUDE-template]]
