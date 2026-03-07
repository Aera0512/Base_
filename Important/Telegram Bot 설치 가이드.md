---
type: guide
tags:
  - automation
  - telegram
  - n8n
  - setup
created: '2026-03-07'
---
# Telegram Bot + 자동 노트 생성 시스템 설치 가이드

## 아키텍처

```
[텔레그램 봇] → [VPS n8n: 메시지 수집] → [Obsidian 큐 (Git 동기화)]
                                                    ↓
[텔레그램] ←→ [VPS n8n: 밤 10시 요약/질문] ← (cron 22:00 Sydney)
                      ↓ (유저 응답)
              [큐에 결정사항 기록 + git push]
                      ↓
              [Cowork 스케줄 태스크 22:05]
                      ↓
              [yt-to-note / book-to-note / pdf 실행]
                      ↓
              [텔레그램 완료 알림]
```

---

## Step 1: VPS에서 설치 스크립트 실행

모든 파일을 VPS에 복사한 후:

```bash
# 파일 복사 (로컬에서)
scp -r /Users/aera/Obsidian-photo-to-Anki/telegram-bot-setup/ root@212.47.67.161:/root/

# VPS 접속
ssh root@212.47.67.161

# 설치 실행
cd /root/telegram-bot-setup
chmod +x install-n8n.sh
bash install-n8n.sh
```

---

## Step 2: n8n에서 Telegram Bot Credential 설정

1. 브라우저에서 `http://212.47.67.161:5678` 접속
2. 로그인: `admin` / `n8n-telegram-bot-2026`
3. **Settings → Credentials → Add Credential**
4. "Telegram" 검색 → "Telegram Bot API" 선택
5. **Access Token** 입력
6. **Name**: `Telegram Bot`으로 설정
7. Save

---

## Step 3: 텔레그램 Chat ID 확인

봇에게 아무 메시지를 보낸 후:

```bash
curl -s "https://api.telegram.org/bot<TOKEN>/getUpdates" | python3 -m json.tool
```

응답에서 `"chat": {"id": 123456789}` 값을 찾아 메모.

---

## Step 4: 워크플로우 import & Chat ID 설정

### 워크플로우 1: Telegram Queue Collector
1. n8n UI → **Workflows → Import from File**
2. `workflow-1-telegram-collector.json` 선택
3. Telegram 노드들의 credential을 Step 2에서 만든 것으로 연결
4. **Activate** 토글 켜기

### 워크플로우 2: Nightly Queue Summary
1. `workflow-2-nightly-summary.json` import
2. **"Send Summary"** 노드와 **"Process Confirmation"** 노드의 `chatId` 값을 Step 3에서 확인한 Chat ID로 변경
3. Telegram 노드들의 credential 연결
4. **Activate** 토글 켜기

---

## Step 5: Cowork 스케줄 태스크 등록

**Cowork 일반 세션**(스케줄 태스크 세션이 아닌)에서:

> "scheduled-task-prompt.md 파일 내용대로 스케줄 태스크를 만들어줘. 매일 22:05에 실행되게."

또는 직접:

> "/schedule telegram-queue-processor 매일 22:05"

---

## Step 6: 테스트

1. **수집 테스트**: 텔레그램 봇에 YouTube 링크 전송 → "✅ 추가됨" 응답 확인
2. **큐 확인**: Obsidian에서 `Inbox/telegram-queue.md` 열어 항목 추가 확인
3. **요약 테스트**: n8n에서 워크플로우 2 수동 실행 → 텔레그램 요약 메시지 수신
4. **응답 테스트**: "all note" 응답 → 큐에 `status: ready` 반영 확인
5. **처리 테스트**: Cowork 스케줄 태스크 수동 실행 → 노트/PDF 생성 확인

---

## 사용법

### 하루 중: 텔레그램으로 수집
- 🎬 YouTube 링크 → 자동 감지
- 📚 일반 텍스트 → 주제로 분류
- `/clear` → 큐 초기화

### 밤 10시: 자동 요약 수신
- 수집된 항목 목록 텔레그램으로 수신
- "1,3 note" / "2 pdf" / "all note" / "skip" 으로 응답

### 밤 10:05: 자동 처리
- Cowork가 yt-to-note / book-to-note 실행 → 완료 알림

---

## 트러블슈팅

| 문제 | 해결 |
|------|------|
| 봇이 응답 안 함 | n8n 컨테이너 상태 확인: `docker logs n8n` |
| 큐 동기화 안 됨 | VPS에서 git pull/push 확인 |
| 밤 10시 메시지 안 옴 | n8n 타임존 확인 (Australia/Sydney) |
| Cowork 처리 안 됨 | Cowork 앱 실행 + Obsidian 실행 필요 |
| Git 충돌 | VPS: `cd vault && git pull --rebase` |
