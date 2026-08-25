<%*
const titleDate = tp.file.title.match(/^(\d{4}-\d{2}-\d{2})/)?.[1];
const titleMoment = moment(titleDate, 'YYYY-MM-DD', true);
const currentMoment = titleMoment.isValid()
  ? titleMoment
  : moment(tp.date.now('YYYY-MM-DD'), 'YYYY-MM-DD', true);
const noteDate = currentMoment.format('YYYY-MM-DD');
const dayOfWeek = ['일', '월', '화', '수', '목', '금', '토'][currentMoment.day()];
const sourcePath = tp.file.path(true);
if (sourcePath.startsWith('나머지/정리 대기/')) {
  await tp.file.move(`정리/계획과 회고/다이어리/1. Daily/${noteDate}(${dayOfWeek})`);
}
-%>
---
date_daily: <% noteDate %>
achievement:
emotion: '<% tp.system.suggester(["😊 행복", "😌 평온", "🔥 열정", "🤔 복잡", "😰 불안", "😔 우울", "😤 짜증", "🥱 피곤"], ["😊 행복", "😌 평온", "🔥 열정", "🤔 복잡", "😰 불안", "😔 우울", "😤 짜증", "🥱 피곤"]) %>'
important_date: false
tags:
  - daily
  - 이룸다이어리
---

# <% currentMoment.format('YYYY년 MM월 DD일') %> · <% dayOfWeek %>요일

> [!nav] 네비게이션
> **[[<% currentMoment.format('YYYY') %>|<% currentMoment.format('YYYY년') %>]]** · **[[<% currentMoment.format('YYYY-MM') %>|<% currentMoment.format('MM월') %>]]** · **[[<% currentMoment.format('gggg-[W]ww') %>|<% currentMoment.format('ww') %>주차]]**
>
> ◀ [[<% currentMoment.clone().subtract(1, 'days').format('YYYY-MM-DD(ddd)') %>|어제]] · **오늘** · [[<% currentMoment.clone().add(1, 'days').format('YYYY-MM-DD(ddd)') %>|내일]] ▶

> [!quote] 오늘의 문장
> <% tp.web.daily_quote() %>

<%*
const yesterday = currentMoment.clone().subtract(1, 'days');
const yesterdayFile = tp.file.find_tfile(yesterday.format('YYYY-MM-DD(ddd)'));
if (yesterdayFile) {
  const content = await app.vault.read(yesterdayFile);
  const lines = content.split('\n');
  let collecting = false;
  const reflectionLines = [];

  for (const line of lines) {
    if (line.includes('[!reflection]')) {
      collecting = true;
      continue;
    }
    if (collecting && line.startsWith('>')) {
      const text = line.replace(/^>\s?/, '').trim();
      if (text) reflectionLines.push(text);
    } else if (collecting) {
      break;
    }
  }

  if (reflectionLines.length > 0) {
    tR += `> [!tip] 어제 남긴 오늘의 다짐 · ${yesterday.format('MM/DD')}\n`;
    reflectionLines.forEach(line => { tR += `> ${line}\n`; });
  }
}
-%>

---

## 오늘의 방향

<!-- agent:morning-direction:start -->
> 오늘 무엇을 지키면 충분한가?
>
<!-- agent:morning-direction:end -->

## 오늘의 할 일

사분면: `#사분면/1_중요긴급` · `#사분면/2_중요비긴급` · `#사분면/3_비중요비긴급` · `#사분면/4_비중요긴급`  
카테고리 예시: `#카테고리/일` · `#카테고리/운동` · `#카테고리/계획` · `#카테고리/휴식`

<!-- notion-sync:start -->
- [ ] 
<!-- notion-sync:end -->

### Dream

```tasks
not done
path includes Dream
path does not include template
short mode
limit 5
```

### 아이젠하워 매트릭스

> [!danger] 1사분면 · 중요하고 긴급
> ```dataviewjs
> const text = await dv.io.load(dv.current().file.path);
> const area = (text.match(/<!-- notion-sync:start -->([\s\S]*?)<!-- notion-sync:end -->/) || [,''])[1];
> const tasks = area.split('\n').filter(line => /^\s*- \[[ xX/-]\]/.test(line) && line.includes('#사분면/1_중요긴급'));
> if (!tasks.length) dv.paragraph('*항목 없음*');
> else tasks.forEach(line => dv.paragraph(line.replace(/\s+#(?:사분면|카테고리)\/[^\s]+/g, '').replace(/\s*<!--.*?-->\s*$/, '')));
> ```

> [!tip] 2사분면 · 중요하고 긴급하지 않음
> ```dataviewjs
> const text = await dv.io.load(dv.current().file.path);
> const area = (text.match(/<!-- notion-sync:start -->([\s\S]*?)<!-- notion-sync:end -->/) || [,''])[1];
> const tasks = area.split('\n').filter(line => /^\s*- \[[ xX/-]\]/.test(line) && line.includes('#사분면/2_중요비긴급'));
> if (!tasks.length) dv.paragraph('*항목 없음*');
> else tasks.forEach(line => dv.paragraph(line.replace(/\s+#(?:사분면|카테고리)\/[^\s]+/g, '').replace(/\s*<!--.*?-->\s*$/, '')));
> ```

> [!example] 3사분면 · 중요하지도 긴급하지도 않음
> ```dataviewjs
> const text = await dv.io.load(dv.current().file.path);
> const area = (text.match(/<!-- notion-sync:start -->([\s\S]*?)<!-- notion-sync:end -->/) || [,''])[1];
> const tasks = area.split('\n').filter(line => /^\s*- \[[ xX/-]\]/.test(line) && line.includes('#사분면/3_비중요비긴급'));
> if (!tasks.length) dv.paragraph('*항목 없음*');
> else tasks.forEach(line => dv.paragraph(line.replace(/\s+#(?:사분면|카테고리)\/[^\s]+/g, '').replace(/\s*<!--.*?-->\s*$/, '')));
> ```

> [!warning] 4사분면 · 중요하지 않지만 긴급
> ```dataviewjs
> const text = await dv.io.load(dv.current().file.path);
> const area = (text.match(/<!-- notion-sync:start -->([\s\S]*?)<!-- notion-sync:end -->/) || [,''])[1];
> const tasks = area.split('\n').filter(line => /^\s*- \[[ xX/-]\]/.test(line) && line.includes('#사분면/4_비중요긴급'));
> if (!tasks.length) dv.paragraph('*항목 없음*');
> else tasks.forEach(line => dv.paragraph(line.replace(/\s+#(?:사분면|카테고리)\/[^\s]+/g, '').replace(/\s*<!--.*?-->\s*$/, '')));
> ```

> [!info]- 아침 에이전트
> Claudian에서 `/daily-start`를 실행한다. 에이전트는 계획안을 먼저 제시하며, 승인받기 전에는 노트나 Notion 일정을 수정하지 않는다.

## 시간별 기록

<!-- agent:day-plan:start -->

| 시간 | 계획 | 실제 |
|:---:|---|---|
| 06:00 |  |  |
| 07:00 |  |  |
| 08:00 |  |  |
| 09:00 |  |  |
| 10:00 |  |  |
| 11:00 |  |  |
| 12:00 |  |  |
| 13:00 |  |  |
| 14:00 |  |  |
| 15:00 |  |  |
| 16:00 |  |  |
| 17:00 |  |  |
| 18:00 |  |  |
| 19:00 |  |  |
| 20:00 |  |  |
| 21:00 |  |  |
| 22:00 |  |  |
| 23:00 |  |  |

<!-- agent:day-plan:end -->

## Quick Note

- 

---

# 상세 기록

## 노력 포인트

[Numbers 기록 열기](file:///Users/aera/Desktop/Spread%20sheet/%EC%98%AC%EB%B0%94%EB%A5%B8%20%EC%8A%B5%EA%B4%80.numbers)

1. 오늘 의도적으로 노력한 것:
2. 기존 점수:
3. 오늘의 점수:
4. 총합과 짧은 메모:

## 습관 추적

### 수면

- 잠든 시간:
- 기상 시간:
- 총 수면 시간:
- 일어난 뒤의 상태:

### 직접 추가

- [ ]

## 자유 기록



## 일기



---

# 하루 마감

## 오늘의 한 줄

<!-- agent:closing-line:start -->
>
<!-- agent:closing-line:end -->

## 회고 초안

<!-- agent:closing-review:start -->
- 확인된 진전:
- 실제 방해 요인:
<!-- agent:closing-review:end -->

> [!reflection] 내일의 다짐
> <!-- agent:next-commitment:start -->
>
> <!-- agent:next-commitment:end -->

> [!info]- 저녁 에이전트
> Claudian에서 `/daily-close`를 실행한다. 작성된 기록만 근거로 회고안을 먼저 제시하며, 승인받기 전에는 노트를 수정하지 않는다.

## 오늘의 달성률

```dataviewjs
const text = await dv.io.load(dv.current().file.path);
const area = (text.match(/<!-- notion-sync:start -->([\s\S]*?)<!-- notion-sync:end -->/) || [,''])[1];
const tasks = area.match(/^\s*- \[[ xX/-]\]\s+\S.*$/gm) || [];
const done = tasks.filter(line => /^\s*- \[[xX]\]/.test(line)).length;
const total = tasks.length;
const pct = total ? Math.round(done / total * 100) : 0;
const filled = Math.round(pct / 5);
dv.paragraph(`**${done} / ${total}** 완료 · **${pct}%** \`${'█'.repeat(filled)}${'░'.repeat(20 - filled)}\``);
```

## 오늘 완료한 일

```tasks
done today
path does not include template
short mode
```

## 오늘 작성한 노트

```dataview
LIST
FROM ""
WHERE file.cday = date("<% currentMoment.format('YYYY-MM-DD') %>")
SORT file.ctime DESC
```

## 오늘 수정한 노트

```dataview
LIST
FROM ""
WHERE file.mday = date("<% currentMoment.format('YYYY-MM-DD') %>") AND file.cday != date("<% currentMoment.format('YYYY-MM-DD') %>")
SORT file.mtime DESC
```

## 마무리 체크

- [ ] 오늘의 할 일을 점검했다
- [ ] 계획과 실제를 기록했다
- [ ] 오늘의 한 줄과 내일의 다짐을 적었다
- [ ] Properties의 `achievement`를 입력했다
