# 🎬 YouTube to Note

유튜브 영상을 마크다운 노트로 변환하는 도구입니다.

## ✨ 기능

- 유튜브 영상 메타데이터 추출 (제목, 채널, 조회수 등)
- 자막 자동 추출 (한국어/영어/일본어 지원)
- Obsidian 호환 마크다운 노트 생성
- 타임스탬프가 포함된 자막

## 📦 설치

```bash
# 프로젝트 디렉토리로 이동
cd "/Users/aera/Desktop/Base_/0. Ai agent/Yt-to-Note"

# 의존성 설치
pip install -r requirements.txt
```

## 🚀 사용법

### 기본 사용

```bash
python yt_to_note.py https://www.youtube.com/watch?v=VIDEO_ID
```

### 출력 디렉토리 지정

```bash
python yt_to_note.py https://youtu.be/VIDEO_ID -o ./notes
```

### 자막 언어 우선순위 설정

```bash
python yt_to_note.py VIDEO_URL --lang ko en ja
```

## 📝 생성되는 노트 구조

```markdown
---
title: "영상 제목"
source: YouTube
video_id: xxx
channel: "채널명"
...
---

# 영상 제목

## 📺 영상 정보
(메타데이터 테이블)

## 📝 내 정리 노트
(정리 공간)

## 📄 자막 전문
(타임스탬프 포함 자막)
```

## 🔧 요구사항

- Python 3.8+
- youtube-transcript-api
- yt-dlp

## 📜 라이선스

MIT License
