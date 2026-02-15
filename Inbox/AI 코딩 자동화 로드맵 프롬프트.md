---
tags:
  - prompt-engineering
  - AI-coding
  - roadmap
  - automation
  - anki
  - english-learning
  - vocabulary
created: '2025-02-15'
status: active
project: 단어장 → Anki 자동화 에이전트
---
# 🔧 완전 자동화 셋업 가이드

## Antigravity에 프롬프트 붙여넣기 전에 할 것

### 1. AnkiConnect 애드온 설치 (2분)

AnkiConnect는 외부 프로그램(우리 Python 스크립트)이 Anki에 카드를 직접 넣을 수 있게 해주는 다리(bridge) 역할입니다.

1. Mac에서 **Anki** 앱 실행
2. 상단 메뉴 → **Tools** → **Add-ons**
3. **Get Add-ons...** 클릭
4. 코드 입력: `2055492159`
5. OK → Anki 재시작

확인 방법: 터미널에서 아래 입력

```bash
curl http://localhost:8765 -X POST -d '{"action":"version","version":6}'
```

`{"result":6,"error":null}` 이 나오면 성공!

### 2. Anthropic API 키 발급 (3분)

1. https://console.anthropic.com 가입
2. Settings → API Keys → Create Key
3. 키를 메모장에 복사해두기 (sk-ant-로 시작하는 긴 문자열)

---

## Antigravity에 프롬프트 붙여넣은 후에 할 것

AI가 코드를 다 만들면 아래 순서로 진행:

### 3. 설치 실행

Antigravity 터미널에서:

```bash
chmod +x install.sh
./install.sh
```

### 4. API 키 입력

```bash
# .env 파일을 열어서 키 입력
# Antigravity의 파일 탐색기에서 .env를 클릭해도 됨
```

.env 내용:

```
ANTHROPIC_API_KEY=sk-ant-여기에-복사한-키-붙여넣기
```

### 5. 테스트 실행

```bash
./start.sh
```

→ "👀 iCloud 폴더 감시 시작..." 메시지가 나오면 성공

→ iPhone이나 Mac에서 단어장 사진을 iCloud Drive > anki-agent > input 폴더에 넣어보기

→ 잠시 후 Anki에 카드가 추가되고 macOS 알림이 뜨면 완성!

---

## iPhone 바로가기 설정 (사진 찍기 → 자동 저장)

이걸 설정하면 홈화면 버튼 한 번으로 촬영 → 저장이 됩니다.

### iPhone에서:

1. **바로가기** 앱 열기
2. 우측 상단 **+** 탭
3. 아래 단계를 순서대로 추가:

```
동작 1: "카메라로 사진 찍기"
  → 검색: "사진 찍기" → "카메라로 사진 찍기" 선택

동작 2: "파일 저장"
  → 검색: "파일 저장" → "파일 저장" 선택
  → 저장 위치: iCloud Drive > anki-agent > input
  → "저장 위치 묻기" 끄기 (OFF로!)
```

4. 바로가기 이름: **"📸 단어장 촬영"**
5. 홈화면에 추가: 바로가기 설정(ⓘ) → "홈 화면에 추가"

### 사용법:

홈화면의 "📸 단어장 촬영" 아이콘 탭 → 카메라 열림 → 촬영 → iCloud 폴더에 자동 저장 → Mac에서 자동 처리 → Anki에 카드 추가됨

---

## Mac 시작 시 자동 실행 (선택사항)

Mac을 켤 때마다 자동으로 감시가 시작되게 하려면:

AI가 만든 `launchd/com.ankiagent.watcher.plist` 파일을 활용합니다.

```bash
# 자동 시작 등록
cp launchd/com.ankiagent.watcher.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.ankiagent.watcher.plist

# 자동 시작 해제하고 싶을 때
launchctl unload ~/Library/LaunchAgents/com.ankiagent.watcher.plist
```

---

## 전체 흐름 요약

```
[한 번만 설정]
AnkiConnect 설치 → API 키 발급 → Antigravity에서 코드 생성 → install.sh → .env 키 입력

[매일 사용]
iPhone "📸 단어장 촬영" 탭 → 사진 촬영 → 끝!

[자동으로 일어나는 일]
iCloud 동기화 → Mac watchdog 감지 → Vision API 추출 
→ AnkiConnect로 카드 추가 → Anki 동기화 → iPhone Anki 반영
```

### 주의사항

- Mac에서 **Anki 앱이 켜져있어야** AnkiConnect가 작동합니다
- Anki가 꺼져있으면 .apkg 백업 파일로 저장됩니다 (나중에 수동 임포트)
- AnkiMobile에 자동 반영되려면 Anki 데스크톱에서 동기화가 필요합니다 (스크립트가 자동으로 동기화 요청을 보냄)
- iPhone에서 AnkiMobile도 가끔 열어서 동기화해줘야 최신 카드가 내려옴