---
type: review-report
period: "2026-W16"
date_created: "2026-04-16"
tags: [review-report, weekly]
---

# 주간 복습 리포트 (2026-W16: 4/13 ~ 4/19)

> 생성 시점: 2026-04-16 (목, Sydney) · 주간 스케줄 자동 실행

## 요약
- 복습 완료: **0개 노트** (이번 주 내 `review[]` 슬롯에 기록된 날짜 없음)
- 미복습 누적: **4개 노트** (next_review ≤ 오늘 또는 1차 복습 미진행)
- 평균 confidence: **N/A** (이번 주 완료된 복습 없음)

## 과목별 분석
| 과목 | 복습 완료 | 미복습 | 평균 confidence |
|------|:---------:|:------:|:--------------:|
| english | 0 | 3 | N/A |
| tech | 0 | 1 | N/A |
| knowledge | 0 | 0 | N/A |
| selfhelp | 0 | 0 | N/A |
| **전체** | **0** | **4** | **N/A** |

## 이번 주 복습 완료 노트
_이번 주(4/13 ~ 4/19) 완료된 복습 기록이 없습니다._

## 밀린 복습 (누적 미복습)
1. **YT-tech-260304-React-Server-Components** (tech)
   - 1차 복습 미진행 · 학습일 2026-03-04 · **43일 밀림**
   - 규칙 적용: 30일 이상 → `review_phase = 0` 리셋 검토
   - 🔗 [Obsidian에서 열기](obsidian://open?vault=Base_&file=f.%20CMDS%2F20.%20Literature%20Notes%2FYT-tech-260304-React-Server-Components)
2. **YT-english-260321-극효율-영어단어-암기법** (english)
   - 1차 복습 미진행 · 학습일 2026-03-21 · **26일 밀림**
   - 규칙 적용: 7~30일 → `review_phase` 한 단계 되돌리기
   - 🔗 [Obsidian에서 열기](obsidian://open?vault=Base_&file=0.%20Ai%20agent%2FYt-to-Note%2FYT-english-260321-%EA%B7%B9%ED%9A%A8%EC%9C%A8-%EC%98%81%EC%96%B4%EB%8B%A8%EC%96%B4-%EC%95%94%EA%B8%B0%EB%B2%95)
3. **YT-english-250323-영어-리액션-70개-표현** (english)
   - 1차 복습 예정일 2026-03-24 · **23일 밀림**
   - 규칙 적용: 7~30일 → `review_phase` 한 단계 되돌리기
   - 🔗 [Obsidian에서 열기](obsidian://open?vault=Base_&file=Yt-to-Note%2FYT-english-250323-%EC%98%81%EC%96%B4-%EB%A6%AC%EC%95%A1%EC%85%98-70%EA%B0%9C-%ED%91%9C%ED%98%84)
4. **Past Perfect** (concept / english)
   - 1차 복습 예정일 2026-03-24 · **23일 밀림**
   - 규칙 적용: 7~30일 → `review_phase` 한 단계 되돌리기
   - 🔗 [Obsidian에서 열기](obsidian://open?vault=Base_&file=0.%20Ai%20agent%2FEnglish%20Grammar%2FPast%20Perfect)

## 다음 주 복습 예정 (4/20 ~ 4/26)
_다음 주에 `next_review`가 도래하는 노트가 없습니다._

다만, 다수의 노트가 `next_review: "2036-03-16"`으로 설정되어 있어 실제 장기 복습 스케줄 관점에서 비정상적으로 보입니다. 아래 "개선 포인트"에서 데이터 정합성 이슈를 다룹니다.

## 개선 포인트
- 🚨 **복습 루틴 재시동 필요**: 이번 주 완료된 복습이 0건입니다. Mode A 브리핑("오늘 뭐 복습해?")을 매일 한 번 열어 밀린 항목 Top 1만이라도 처리하는 것이 회복의 출발점입니다.
- ⚠️ **4개 노트 기한 초과** (23~43일): 밀린 일수에 따라 간격 반복 엔진 규칙을 적용합니다.
    - React-Server-Components (43일): `review_phase = 0`으로 리셋, `review = [null, null, null]`
    - 극효율-영어단어 / 영어-리액션 / Past Perfect (23~26일): `review_phase`를 한 단계 되돌림
- 📚 **과목 편중 주의**: 학습 노트 16개 중 english 계열이 12개(75%)로 쏠려 있습니다. tech(React Server Components)와 selfhelp(Passion/Flow, 블로그 자동화) 쪽은 1차 복습도 안 들어간 상태이니, 다음 주 슬롯을 의식적으로 배분해보세요.
- 🔧 **데이터 정합성 체크 필요**: 다수 노트의 `review[]`에 `["2026-01-01", "2026-01-08", "2026-02-08"]`이 일괄로 기록되어 있고 `next_review: "2036-03-16"`(10년 뒤)이 설정돼 있습니다. 실제 복습 기록이 아닌 마이그레이션/초기화 과정의 배치 값으로 추정되므로, 실제 복습 이력으로 재설정하는 것을 권장합니다. 이 상태가 유지되면 해당 노트들은 10년간 복습 대상에서 제외됩니다.
- 📅 **주간 리듬 제안**: 이번 주는 이미 4일이 지났으니 주말(4/18~4/19)에 밀린 4개를 1차 복습으로 해치우는 배치 처리를 추천합니다. 각 노트 10~15분씩, 총 약 60분이면 충분합니다.

## 참고
- 간격 반복 엔진 규칙: `spaced-repetition-engine.md` (1차: +1일, 2차: +7일×CM, 3차: +30일×CM, 4차+: FSRS)
- 밀림 처리: ≤7일 이어서 / 8~30일 한 단계 되돌림 / 30일+ 완전 리셋
