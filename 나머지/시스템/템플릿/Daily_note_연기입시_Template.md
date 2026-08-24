---
date_daily: <% tp.file.title.slice(0,10) %>
note_type: daily-audition
condition: '<% tp.system.suggester(["5 — 아주 좋음", "4 — 좋음", "3 — 보통", "2 — 좋지 않음", "1 — 회복 우선"], [5, 4, 3, 2, 1]) %>'
emotion: '<% tp.system.suggester(["😊 행복", "😌 평온", "🔥 열정", "🤔 복잡", "😰 불안", "😔 우울", "😤 짜증", "🥱 피곤"], ["😊 행복", "😌 평온", "🔥 열정", "🤔 복잡", "😰 불안", "😔 우울", "😤 짜증", "🥱 피곤"]) %>'
target_school:
exam_date:
tags:
  - daily
  - 입시/연기
---

<%*
const currentMoment = moment(tp.file.title, "YYYY-MM-DD");
const dayOfWeek = ['일', '월', '화', '수', '목', '금', '토'][currentMoment.day()];
-%>

# 🎭 <% currentMoment.format('YYYY년 MM월 DD일') %> (<% dayOfWeek %>요일)

> [!nav] 📍 네비게이션
> **[[<% currentMoment.format('YYYY') %>|<% currentMoment.format('YYYY년') %>]]** · **[[<% currentMoment.format('YYYY-MM') %>|<% currentMoment.format('MM월') %>]]** · **[[<% currentMoment.format('gggg-[W]ww') %>|<% currentMoment.format('ww') %>주차]]**
>
> ◀ [[<% currentMoment.clone().subtract(1, 'days').format('YYYY-MM-DD(ddd)') %>|어제]] · **오늘** · [[<% currentMoment.clone().add(1, 'days').format('YYYY-MM-DD(ddd)') %>|내일]] ▶

<%*
const yesterday = currentMoment.clone().subtract(1, 'days');
const yesterdayFile = tp.file.find_tfile(yesterday.format('YYYY-MM-DD(ddd)'));
if (yesterdayFile) {
  const content = await app.vault.read(yesterdayFile);
  const lines = content.split('\n');
  let collecting = false;
  const nextLines = [];

  for (const line of lines) {
    if (line.includes('[!next]')) {
      collecting = true;
      continue;
    }
    if (collecting && line.startsWith('>')) {
      const text = line.replace(/^>\s?/, '').trim();
      if (text) nextLines.push(text);
    } else if (collecting) {
      break;
    }
  }

  if (nextLines.length > 0) {
    tR += `> [!tip] 어제 남긴 오늘의 첫 과제 (${yesterday.format('MM/DD')})\n`;
    nextLines.forEach(line => { tR += `> ${line}\n`; });
  }
}
-%>

---

## 🌅 시작 전 체크인

| 항목 | 기록 |
|---|---|
| 수면 | 취침:  / 기상:  / 총:  시간 |
| 몸 상태 | 1–5:  / 통증·긴장:  |
| 목 상태 | 1–5:  / 쉰 소리·이물감:  |
| 집중·감정 | 1–5:  / 지금 마음:  |
| 오늘의 가용 시간 |  시간  분 |

> [!warning] 회복 기준
> 날카로운 통증, 갑작스러운 음역 상실, 심한 쉰 목소리, 어지러움이 있으면 강도를 낮추거나 중단한다.

## 🎯 오늘의 한 가지

> [!abstract] 오늘 반드시 남길 변화
> **집중할 한 가지:**  
> **성공 기준:** 영상·녹음·결과에서 무엇이 보이거나 들리면 성공인가?  
> **외부 초점:** 오늘 상대·공간에 어떤 변화를 일으킬 것인가?  
> **내려놓을 습관 하나:**

## ✅ 오늘의 우선순위

> 태그 기준: `#q1` 중요·긴급 · `#q2` 중요·비긴급 · `#q3` 비중요·비긴급 · `#q4` 비중요·긴급

- [ ] 가장 중요한 일 #q2
- [ ] 반드시 처리할 일 #q1
- [ ] 여유가 있으면 할 일

### 진행 중인 입시 과제

```tasks
not done
filter by function task.file.tags.some(tag => tag.includes("입시") || tag.includes("연기"))
filter by function !task.file.folder.toLowerCase().includes("template")
sort by priority
short mode
limit 8
```

## 🗓️ 오늘의 훈련 설계

| 순서 | 영역 | 오늘의 과제 | 시간 | 완료 | 증거 링크 |
|:---:|---|---|---:|:---:|---|
| 1 | 몸·목소리 준비 |  |  분 | ☐ |  |
| 2 | 자유 연기 / 지정 연기 |  |  분 | ☐ |  |
| 3 | 당일 대사 / 즉흥 |  |  분 | ☐ |  |
| 4 | 보컬 / 무용 / 특기 |  |  분 | ☐ |  |
| 5 | 학교별 공략 / 질의응답 |  |  분 | ☐ |  |
| 6 | 작품 읽기 / 분석 |  |  분 | ☐ |  |

> [!info] 훈련 원칙
> 각 블록은 `무도움 기준 시도 → 한 요소 수정 → 실전처럼 한 번 → 증거 기록` 순서로 진행한다.

## ⏱️ DAY PLANNER

| 시간 | 계획 | 실제 |
|:---:|---|---|
| 08:00 | 기상·아침 루틴 |  |
| 09:00 |  |  |
| 10:00 |  |  |
| 11:00 |  |  |
| 12:00 | 점심·회복 |  |
| 13:00 |  |  |
| 14:00 |  |  |
| 15:00 |  |  |
| 16:00 |  |  |
| 17:00 |  |  |
| 18:00 | 저녁·회복 |  |
| 19:00 |  |  |
| 20:00 |  |  |
| 21:00 |  |  |
| 22:00 | 피드백·정리 |  |
| 23:00 | 하루 마무리 |  |

---

# 🎬 훈련 기록

## 1. 기준 시도

- 오늘 첫 시도에서 실제로 보인 것:
- 설명하거나 꾸며낸 순간:
- 상대·공간과 연결된 순간:
- 몸·목소리에서 느낀 것:

## 2. 시도와 수정

| 시도 | 바꾼 단 한 가지 | 보이거나 들린 사실 | 다음 수정 |
|:---:|---|---|---|
| 기준 | 도움 없이 전체 |  |  |
| 수정 1 |  |  |  |
| 수정 2 |  |  |  |
| 실전 | 멈추지 않고 한 번에 |  |  |

## 3. 영역별 핵심 관찰

### 🎭 연기

- 상대와 관계:
- 지금 원하는 것과 행동 동사:
- 자극을 실제로 받은 순간:
- 계획한 억양·표정·버릇이 나온 순간:

### 🎤 보컬·발성

- 호흡·음정·리듬:
- 가사와 말의 전달:
- 목에 부담을 준 조건 / 편하게 만든 조건:

### 💃 움직임·무용

- 중심·호흡·힘의 방향:
- 시선·공간·전환:
- 통증 또는 강도를 조절한 지점:

### 🏫 학교별 공략·질의응답

- 학교·전형 단계:
- 오늘 확인한 평가 기준:
- 질문과 내 답의 핵심:
- 입장부터 퇴장까지 가장 불안정했던 순간:

## 4. 영상·녹음 피드백

| 관찰 항목 | 확인된 사실 | 다음에 할 구체적인 행동 |
|---|---|---|
| 상대·외부 초점 |  |  |
| 목적·행동 변화 |  |  |
| 말·호흡·여운 |  |  |
| 몸·시선·공간 |  |  |
| 고유성·매력 |  |  |
| 실수 뒤 회복 |  |  |

- 영상·녹음 링크:
- 오늘 가장 좋아진 3–10초:
- 그 변화가 생긴 조건:

## 📚 오늘의 인풋

- 읽거나 본 작품·자료:
- 기억에 남은 장면·문장:
- 내 연기에 실험해볼 한 가지:

## 📝 Quick Note

> [!note]- 떠오른 생각·대사·아이디어
>

---

# 🌙 마감 회고

## 오늘의 증거

> [!success] 잘했다/못했다 대신 관찰 가능한 변화
> **전보다 달라진 한 가지:**  
> **오늘 지킨 약속:**  
> **아직 불안정한 한 가지:**

## 오늘의 한 줄

> [!quote] 오늘을 한 문장으로 표현한다면?
>

## 내일의 첫 과제

> [!next] 내일 시작하자마자 할 구체적인 행동
>

## 오늘의 달성률

```dataviewjs
const content = await dv.io.load(dv.current().file.path);
const beforeReview = content.split("# 🌙 마감 회고")[0];
const total = (beforeReview.match(/- \[.\]/g) || []).length;
const done = (beforeReview.match(/- \[[xX]\]/g) || []).length;
const pct = total ? Math.round((done / total) * 100) : 0;
const filled = Math.round(pct / 5);
dv.paragraph(`**${done} / ${total}** 완료 · **${pct}%** \`${'█'.repeat(filled)}${'░'.repeat(20 - filled)}\``);
```

## 오늘 작성한 연습 기록

```dataview
LIST
FROM #연기/연습기록
WHERE file.cday = date("<% currentMoment.format('YYYY-MM-DD') %>")
SORT file.ctime DESC
```

## 마무리 체크

- [ ] 영상 또는 녹음을 다시 확인했다
- [ ] 오늘의 증거를 적었다
- [ ] 내일의 첫 과제를 하나만 남겼다
- [ ] 몸·목 상태를 확인하고 회복했다

> [!success] 오늘 하루도 수고했어.
> 완벽한 하루보다, 재현 가능한 변화 하나를 남긴 하루.
