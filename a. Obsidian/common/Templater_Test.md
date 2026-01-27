## 노트 생성 날짜
<% tp.file.creation_date("YYYY년 MM월 DD일 HH:mm") %>
<% tp.file.creation_date("YYYY-MM-DD a HH:mm") %>


## 노트 제목
<% tp.file.title %>
<% tp.file.title.slice(9) %>
<% tp.file.title.slice(0, 9) %>

## 노트 저장 폴더, 경로
<% tp.file.folder() %>
<% tp.file.path() %>

## tp_date
<% tp.date.now("YYYY-MM-DD") %>
<% tp.date.tomorrow("YYYY-MM-DD") %>
<% tp.date.yesterday("YYYY-MM-DD") %>
일 [[<% tp.date.weekday("YYYY-MM-DD", 0) %>]]
월 <% tp.date.weekday("YYYY-MM-DD", 1) %>
화 <% tp.date.weekday("YYYY-MM-DD", 2) %>
수 <% tp.date.weekday("YYYY-MM-DD", 3) %>
목 <% tp.date.weekday("YYYY-MM-DD", 4) %>
금 <% tp.date.weekday("YYYY-MM-DD", 5) %>
토 <% tp.date.weekday("YYYY-MM-DD", 6) %>

## tp_system

### 클립보드
<% tp.system.clipboard() %>

### 드롭다운 메뉴
<% tp.system.suggester(
["별 5개", "별 4개", "별 3개", "별 2개", "별 1개"], 
["별점 : *****", "별점 : ****", "별점 : ***", "별점 : **", "별점 : *"]
) %>

### 텍스트 필드
<% tp.system.prompt("오늘의 기분은?", "오늘의 기분은 : ") %>