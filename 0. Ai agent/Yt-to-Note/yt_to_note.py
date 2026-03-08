#!/usr/bin/env python3
"""
YouTube to Note - 유튜브 영상을 마크다운 노트로 변환하는 도구
"""

import os
import re
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# 의존성 체크
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api.formatters import TextFormatter
except ImportError:
    print("❌ youtube-transcript-api가 설치되지 않았습니다.")
    print("   pip install youtube-transcript-api 로 설치해주세요.")
    sys.exit(1)

try:
    import yt_dlp
except ImportError:
    print("❌ yt-dlp가 설치되지 않았습니다.")
    print("   pip install yt-dlp 로 설치해주세요.")
    sys.exit(1)


def extract_video_id(url: str) -> str:
    """유튜브 URL에서 비디오 ID 추출"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/shorts\/([^&\n?#]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"유효한 YouTube URL이 아닙니다: {url}")


def get_video_info(video_id: str) -> dict:
    """yt-dlp를 사용해 비디오 메타데이터 가져오기"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }

    url = f"https://www.youtube.com/watch?v={video_id}"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            'title': info.get('title', 'Unknown Title'),
            'channel': info.get('uploader', 'Unknown Channel'),
            'channel_url': info.get('uploader_url', ''),
            'duration': info.get('duration', 0),
            'upload_date': info.get('upload_date', ''),
            'description': info.get('description', ''),
            'view_count': info.get('view_count', 0),
            'thumbnail': info.get('thumbnail', ''),
            'tags': info.get('tags', []),
        }


def get_transcript(video_id: str, languages: list = None) -> str:
    """유튜브 자막 가져오기"""
    if languages is None:
        languages = ['ko', 'en', 'ja']  # 기본 언어 우선순위

    try:
        # 사용 가능한 자막 목록 확인
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # 수동 자막 우선 시도
        try:
            transcript = transcript_list.find_manually_created_transcript(languages)
        except:
            # 자동 생성 자막 시도
            try:
                transcript = transcript_list.find_generated_transcript(languages)
            except:
                # 아무 자막이나 가져와서 번역 시도
                transcript = transcript_list.find_transcript(languages)

        # 자막 텍스트 추출
        transcript_data = transcript.fetch()

        # 타임스탬프와 함께 포맷팅
        formatted_lines = []
        for entry in transcript_data:
            timestamp = format_timestamp(entry['start'])
            text = entry['text'].strip()
            formatted_lines.append(f"[{timestamp}] {text}")

        return '\n'.join(formatted_lines)

    except Exception as e:
        return f"자막을 가져올 수 없습니다: {str(e)}"


def format_timestamp(seconds: float) -> str:
    """초를 HH:MM:SS 또는 MM:SS 형식으로 변환"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def format_duration(seconds: int) -> str:
    """영상 길이를 읽기 쉬운 형식으로 변환"""
    if seconds < 60:
        return f"{seconds}초"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}분 {secs}초"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}시간 {minutes}분"


def create_markdown_note(video_id: str, video_info: dict, transcript: str, output_dir: str = None) -> str:
    """마크다운 노트 생성"""

    # 파일명 생성 (특수문자 제거)
    safe_title = re.sub(r'[<>:"/\\|?*]', '', video_info['title'])
    safe_title = safe_title[:50]  # 파일명 길이 제한

    # 출력 디렉토리 설정
    if output_dir is None:
        output_dir = os.getcwd()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 날짜 포맷팅
    upload_date = video_info.get('upload_date', '')
    if upload_date:
        try:
            formatted_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
        except:
            formatted_date = upload_date
    else:
        formatted_date = "Unknown"

    # 마크다운 콘텐츠 생성
    md_content = f"""---
title: "{video_info['title']}"
source: YouTube
video_id: {video_id}
channel: "{video_info['channel']}"
upload_date: {formatted_date}
duration: {format_duration(video_info['duration'])}
created: {datetime.now().strftime('%Y-%m-%d %H:%M')}
tags: [youtube, video-note]
---

# {video_info['title']}

## 📺 영상 정보

| 항목 | 내용 |
|------|------|
| **채널** | [{video_info['channel']}]({video_info['channel_url']}) |
| **영상 길이** | {format_duration(video_info['duration'])} |
| **업로드일** | {formatted_date} |
| **조회수** | {video_info['view_count']:,}회 |
| **링크** | [YouTube에서 보기](https://www.youtube.com/watch?v={video_id}) |

![썸네일]({video_info['thumbnail']})

## 📝 내 정리 노트

> 여기에 핵심 내용을 정리하세요

### 핵심 포인트
-

### 인사이트
-

### 액션 아이템
- [ ]

---

## 📄 자막 전문

```
{transcript}
```

---

## 📋 영상 설명

{video_info['description'][:2000] if video_info['description'] else '설명 없음'}

"""

    # 파일 저장
    filename = f"{safe_title}.md"
    filepath = output_dir / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)

    return str(filepath)


def main():
    parser = argparse.ArgumentParser(
        description='YouTube 영상을 마크다운 노트로 변환합니다.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python yt_to_note.py https://www.youtube.com/watch?v=VIDEO_ID
  python yt_to_note.py https://youtu.be/VIDEO_ID -o ./notes
  python yt_to_note.py VIDEO_URL --lang ko en
        """
    )

    parser.add_argument('url', help='YouTube 영상 URL 또는 비디오 ID')
    parser.add_argument('-o', '--output', default='.', help='출력 디렉토리 (기본: 현재 디렉토리)')
    parser.add_argument('-l', '--lang', nargs='+', default=['ko', 'en', 'ja'],
                       help='자막 언어 우선순위 (기본: ko en ja)')

    args = parser.parse_args()

    print("🎬 YouTube to Note 변환 시작...\n")

    try:
        # 비디오 ID 추출
        video_id = extract_video_id(args.url) if 'youtube' in args.url or 'youtu.be' in args.url else args.url
        print(f"📌 비디오 ID: {video_id}")

        # 비디오 정보 가져오기
        print("📊 영상 정보 가져오는 중...")
        video_info = get_video_info(video_id)
        print(f"   제목: {video_info['title']}")
        print(f"   채널: {video_info['channel']}")
        print(f"   길이: {format_duration(video_info['duration'])}")

        # 자막 가져오기
        print("📝 자막 가져오는 중...")
        transcript = get_transcript(video_id, args.lang)
        if "자막을 가져올 수 없습니다" in transcript:
            print(f"   ⚠️ {transcript}")
        else:
            line_count = len(transcript.split('\n'))
            print(f"   ✅ 자막 {line_count}줄 가져옴")

        # 마크다운 생성
        print("📄 마크다운 노트 생성 중...")
        filepath = create_markdown_note(video_id, video_info, transcript, args.output)

        print(f"\n✅ 완료! 노트가 생성되었습니다:")
        print(f"   📁 {filepath}")

    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
