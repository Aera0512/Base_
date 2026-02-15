---
created: '2026-02-15'
status: 진행중
tags:
  - 프로젝트
  - 자동화
  - Anki
---
# Anki Agent - Antigravity 지시문 & 셋업 가이드

## 현재 진행 상태
- [x] Antigravity 설치
- [x] 프로젝트 폴더 열기
- [ ] AnkiConnect 애드온 설치 (코드: 2055492159)
- [ ] OpenAI API 키 발급
- [ ] Antigravity에 지시문 붙여넣기
- [ ] install.sh 실행
- [ ] .env 키 입력
- [ ] 테스트 실행
- [ ] iPhone 바로가기 설정

## 핵심 파일
- `antigravity-prompt.md` — Antigravity에 붙여넣을 전체 지시문
- `setup-guide.md` — 붙여넣기 전후로 해야 할 설정 가이드

## 완성 시 자동화 흐름
📸 iPhone 촬영 → ☁️ iCloud 동기화 → 🤖 자동 처리 → 🃏 Anki 카드 추가 → 📱 iPhone 복습

#프로젝트 #자동화 #Anki #영어학습 #진행중


---

## 📋 Antigravity에 붙여넣을 프롬프트 (OpenAI 버전)

아래 구분선 사이의 텍스트를 그대로 복사해서 Antigravity Agent 패널에 붙여넣기

---

한국어로 소통해줘.

다음 Python 프로젝트를 만들어줘. Plan Mode로 계획을 먼저 보여주고, 내가 승인하면 실행해.

## 프로젝트: 단어장 사진 → Anki 완전 자동 파이프라인

### 최종 목표:
iPhone에서 단어장 사진을 iCloud Drive 특정 폴더에 저장하면,
Mac에서 자동으로 감지 → AI가 단어 추출 → Anki에 카드 자동 추가.
사용자가 추가로 할 일이 전혀 없는 완전 자동화 시스템.

### 전체 아키텍처:
```
iPhone 사진 → iCloud Drive/anki-agent/input/ → Mac 동기화
→ watchdog 감지 → OpenAI GPT-4.1 Nano Vision API로 텍스트 추출
→ JSON 파싱 → AnkiConnect API로 Anki에 직접 카드 추가
→ 처리 완료 파일은 processed/ 폴더로 이동
→ macOS 알림으로 결과 통보
```

### 기술 스택:
- Python 3.11+
- openai (GPT-4.1 Nano Vision API - 사진 속 텍스트 추출)
- watchdog (폴더 감시 라이브러리)
- requests (AnkiConnect HTTP 요청)
- genanki (백업용 .apkg 파일 생성)
- python-dotenv (환경변수 관리)
- Pillow (이미지 전처리)

### 폴더 구조:
```
anki-agent/
├── main.py              # 메인 실행 - watchdog으로 폴더 감시 시작
├── watcher.py           # iCloud 폴더 감시 모듈
├── vision.py            # 사진 → 텍스트 추출 (OpenAI GPT-4.1 Nano Vision API)
├── parser.py            # 텍스트 → 구조화된 JSON 변환
├── anki_sync.py         # AnkiConnect API로 Anki에 카드 직접 추가
├── card_maker.py        # 백업용 .apkg 파일 생성 (genanki)
├── notifier.py          # macOS 알림 전송
├── config.py            # 설정값 관리
├── .env.example         # API 키 설정 예시
├── requirements.txt
├── install.sh           # 원클릭 설치 스크립트
├── start.sh             # 원클릭 실행 스크립트
├── launchd/             # macOS 자동 시작 설정
│   └── com.ankiagent.watcher.plist
├── logs/                # 처리 로그
└── README.md            # 설치/사용 가이드 (한국어)
```

### 각 모듈 상세 요구사항:

#### 1. config.py
```python
# iCloud Drive 경로 (macOS 기본 경로)
ICLOUD_INPUT = "~/Library/Mobile Documents/com~apple~CloudDocs/anki-agent/input"
ICLOUD_PROCESSED = "~/Library/Mobile Documents/com~apple~CloudDocs/anki-agent/processed"
LOCAL_BACKUP = "~/anki-agent/backup"

# AnkiConnect 설정
ANKICONNECT_URL = "http://localhost:8765"
ANKI_DECK_NAME = "영단어장"
ANKI_MODEL_NAME = "영단어 카드"

# 지원하는 이미지 확장자
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".heic"}
```

#### 2. watcher.py
- watchdog 라이브러리로 ICLOUD_INPUT 폴더를 실시간 감시
- 새 이미지 파일이 감지되면 처리 파이프라인 시작
- iCloud 동기화 중인 파일 처리 방지 (.icloud 확장자 무시)
- 파일이 완전히 동기화될 때까지 대기 (파일 크기 변화 체크, 2초 간격 3회)
- 중복 처리 방지 (이미 처리한 파일명 기록)

#### 3. vision.py
- OpenAI GPT-4.1 Nano Vision API 사용
- HEIC 파일은 Pillow로 JPEG 변환 후 처리
- 이미지를 base64로 인코딩하여 API에 전송
- 핵심 코드 구조:
```python
from openai import OpenAI
import base64

client = OpenAI()  # OPENAI_API_KEY 환경변수에서 자동 읽음

def extract_text_from_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")
    
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_data}"
                    }
                },
                {
                    "type": "text",
                    "text": """이 단어장/교재 사진에서 모든 영어 단어와 한국어 뜻을 추출해줘.

규칙:
1. 영단어의 발음기호를 IPA 형식으로 포함
2. 품사(n./v./adj./adv. 등) 포함
3. 자연스러운 예문 1개 생성 (TOEIC 600-700 수준)
4. 예문의 한국어 번역 포함
5. 읽기 어려운 부분은 [불확실]로 표시
6. 반드시 JSON 배열만 반환, 다른 텍스트 없이

JSON 형식:
[
    {
        "word": "영단어",
        "pos": "품사",
        "pronunciation": "/발음기호/",
        "meaning": "한국어 뜻",
        "example": "영어 예문",
        "example_kr": "예문 한국어 번역"
    }
]"""
                }
            ]
        }]
    )
    
    return response.choices[0].message.content
```
- API 에러 시 3회 재시도 (exponential backoff)

#### 4. parser.py
- vision.py에서 반환된 텍스트를 JSON으로 파싱
- JSON 유효성 검증 (필수 필드 체크)
- [불확실] 태그가 있는 항목은 별도 로그에 기록
- 중복 단어 필터링

#### 5. anki_sync.py (가장 중요!)
- AnkiConnect REST API (http://localhost:8765)를 통해 Anki에 직접 카드 추가
- 기능:
  a. Anki 실행 여부 확인 (AnkiConnect ping)
  b. 덱이 없으면 자동 생성
  c. 카드 노트 타입(모델)이 없으면 자동 생성
  d. 중복 카드 체크 (같은 단어가 이미 있으면 스킵)
  e. 카드 추가 후 자동 동기화 트리거

- 카드 디자인:
  앞면:
  ```html
  <div style="font-size:36px; text-align:center; font-weight:bold;">{{Word}}</div>
  <div style="font-size:16px; color:#888; text-align:center;">{{Pronunciation}}</div>
  <div style="font-size:12px; color:#aaa; text-align:center;">{{POS}}</div>
  ```

  뒷면:
  ```html
  {{FrontSide}}
  <hr>
  <div style="font-size:28px; text-align:center; color:#2196F3;">{{Meaning}}</div>
  <div style="font-size:16px; text-align:center; margin-top:15px; color:#555;">{{Example}}</div>
  <div style="font-size:14px; text-align:center; color:#888;">{{ExampleKR}}</div>
  ```

- AnkiConnect API 호출 예시:
  ```python
  requests.post("http://localhost:8765", json={
      "action": "addNote",
      "version": 6,
      "params": {
          "note": {
              "deckName": "영단어장",
              "modelName": "영단어 카드",
              "fields": {
                  "Word": "apple",
                  "Pronunciation": "/ˈæpəl/",
                  "POS": "n.",
                  "Meaning": "사과",
                  "Example": "I eat an apple every morning.",
                  "ExampleKR": "나는 매일 아침 사과를 먹는다."
              },
              "options": {"allowDuplicate": false},
              "tags": ["auto-generated"]
          }
      }
  })
  
  requests.post("http://localhost:8765", json={
      "action": "sync",
      "version": 6
  })
  ```

#### 6. card_maker.py
- genanki로 .apkg 백업 파일도 함께 생성
- AnkiConnect 실패 시 폴백(대체 방안)으로 사용
- backup/ 폴더에 날짜별 저장

#### 7. notifier.py
- macOS 네이티브 알림 사용 (osascript)
- 성공 시: "✅ 15개 단어 추가 완료! (사진: photo1.jpg)"
- 실패 시: "❌ 처리 실패: [에러 내용]"
- Anki 미실행 시: "⚠️ Anki가 꺼져있어서 .apkg로 저장했습니다"

#### 8. main.py
- 실행하면 watchdog 감시를 시작
- Ctrl+C로 종료 가능
- 시작 시 체크:
  a. iCloud 폴더 존재 확인, 없으면 자동 생성
  b. processed 폴더 확인, 없으면 자동 생성
  c. .env 파일의 API 키 확인
  d. AnkiConnect 연결 테스트 (실패해도 계속 진행, .apkg 모드로 전환)
- 처리 완료된 이미지는 processed/ 폴더로 이동
- 모든 활동을 logs/ 폴더에 날짜별 로그 파일로 기록

#### 9. install.sh
```bash
#!/bin/bash
echo "🚀 Anki Agent 설치 시작..."
python3 -m venv venv
source venv/bin/activate
pip install openai watchdog genanki Pillow python-dotenv requests pillow-heif
mkdir -p ~/Library/Mobile\ Documents/com~apple~CloudDocs/anki-agent/input
mkdir -p ~/Library/Mobile\ Documents/com~apple~CloudDocs/anki-agent/processed
mkdir -p backup logs
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  .env 파일에 OPENAI_API_KEY를 입력해주세요!"
fi
echo "✅ 설치 완료!"
echo ""
echo "다음 단계:"
echo "1. .env 파일에 OpenAI API 키 입력"
echo "2. Anki에 AnkiConnect 애드온 설치 (코드: 2055492159)"
echo "3. ./start.sh 로 실행"
```

#### 10. start.sh
```bash
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
echo "👀 iCloud 폴더 감시 시작... (종료: Ctrl+C)"
python3 main.py
```

#### 11. launchd/com.ankiagent.watcher.plist
- macOS launchd를 이용한 로그인 시 자동 시작 설정
- Mac을 켜면 자동으로 폴더 감시가 시작되도록
- 설치 방법도 README에 포함

#### 12. .env.example
```
OPENAI_API_KEY=sk-여기에-OpenAI-키-붙여넣기
```

### 중요 사항:
1. 모든 함수에 한국어 docstring(설명 주석) 달기
2. 에러 처리를 꼼꼼히 (네트워크 에러, API 에러, 파일 에러 등)
3. .env.example에 필요한 환경변수 명시
4. README.md에 상세한 한국어 설치/사용 가이드 작성
5. iCloud 동기화 지연 대응 (.icloud 파일 처리, 파일 완전성 체크)
6. HEIC(iPhone 기본 사진 형식) → JPEG 자동 변환
7. AnkiConnect 미연결 시에도 .apkg 파일로 저장하는 폴백 처리

이 계획을 먼저 보여주고, 내가 승인하면 구현을 시작해줘.

---

