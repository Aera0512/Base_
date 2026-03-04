---
tags:
  - project
  - book-to-note
  - schema
created: '2026-03-04'
---

# 서브에이전트 중간 결과물 JSON 스키마

서브에이전트는 웹 검색으로 수집된 도서 정보를 분석하여 다음 JSON 구조를 반환해야 합니다.

## 서브에이전트 프롬프트

```
당신은 도서의 핵심 내용을 분석하여 구조화된 학습 노트의 재료를 만드는 분석가입니다.

## 입력
- 책 제목: {{title}}
- 저자: {{author}}
- 장르: {{genre}}
- 수집된 정보: (아래 첨부)

## 임무

1. **파트 분절**: 책의 실제 Part/Chapter 구조를 따라 3~6개 파트로 나누세요.
   - 원서의 Part/Chapter 구조를 최대한 반영 (임의 재구성 금지)
   - 각 파트에 원서 대응 범위를 명시 (예: "1장~3장")
   - 난이도 라벨 부여: 🟢 기초 / 🟡 중급 / 🔴 심화

2. **파트별 핵심 분석**: 각 파트에 대해:
   - **핵심 질문** 3~5개 (Cornell Cue Column용: 이 파트를 읽고 답할 수 있어야 하는 질문)
   - 핵심 주장/개념을 1~2문장으로 요약
   - 뒷받침 근거/사례를 가능한 구체적으로 (수치, 연구자명 보존)
   - 핵심 용어 목록 (용어 → 한 줄 정의)
   - [tech] 코드/아키텍처 패턴이 있다면 원문 그대로 보존
   - [selfhelp] 실천 방법/프레임워크가 있다면 단계별로 정리
   - 저자가 사용한 비유가 있다면 기록 (Feynman Technique용)
   - 흔한 오해/주의사항이 있다면 기록
   - **한 줄 요약** (Cornell Summary: 파트 전체를 한 문장으로 압축)

3. **전체 분석**:
   - 한 줄 핵심 (20자 내외)
   - 4~6문장 개요
   - 마인드맵 구조: root → branch → leaf
   - 암기 포인트: ★★★(3점), ★★☆(2점), ★☆☆(1점) 중요도
   - 전체 용어 사전
   - 종합 정리 (모든 챕터를 관통하는 서사)
   - 셀프 테스트 질문 5~7개

수집된 웹 검색 결과에서만 정보를 추출하세요. 확인되지 않은 내용을 추가하지 마세요.
```

## JSON 스키마

```json
{
  "title": "책 제목",
  "original_title": "원서 제목 (번역서인 경우)",
  "author": "저자명",
  "genre": "tech|knowledge|selfhelp",
  "year": 2024,
  "pages": 300,

  "one_liner": "한 줄 핵심 (20자 내외)",
  "overview": "4~6문장 개요. 저자 배경, 핵심 질문, 책의 위치(분야 내 중요도) 포함.",

  "mindmap": {
    "root": "핵심 주제",
    "branches": [
      {
        "label": "챕터/논점 주제",
        "children": ["하위 개념 1", "하위 개념 2"]
      }
    ]
  },

  "key_points": [
    {
      "importance": 3,
      "concept": "핵심 개념/논점",
      "summary": "한 줄 요약",
      "anchor": "기억 고리 (비유/키워드)"
    }
  ],

  "chapters": [
    {
      "number": 1,
      "title": "챕터 제목",
      "difficulty": "🟢 기초",
      "book_chapters": "원서 1~3장 해당",
      "content": {
        "background": "배경/문제 상황 서술 (3~5문장 분량의 재료)",
        "main_argument": "핵심 주장/개념 상세 서술 (5~10문장 분량의 재료)",
        "evidence": [
          "근거 1: 구체적 연구/데이터/사례 (수치 보존)",
          "근거 2: ..."
        ],
        "examples": [
          "구체적 사례 서술 (인물, 기업, 상황, 결과)"
        ],
        "analogy": "저자가 사용한 비유 또는 적절한 비유 제안",
        "code_blocks": [
          "// tech 장르만: 코드 원문 보존\nconst example = 'code';"
        ],
        "frameworks": [
          {
            "name": "selfhelp 장르만: 프레임워크/모델명",
            "steps": ["1단계: ...", "2단계: ...", "3단계: ..."],
            "when_to_use": "적용 상황"
          }
        ],
        "action_items": [
          "selfhelp 장르만: 구체적 실천 항목"
        ],
        "common_misconceptions": [
          {
            "wrong": "흔한 오해/잘못된 믿음",
            "correct": "실제/올바른 이해",
            "why": "왜 오해하는가"
          }
        ],
        "terms": [
          {"term": "용어", "definition": "한 줄 정의"}
        ]
      }
    }
  ],

  "glossary": [
    {
      "term": "용어",
      "definition": "한 줄 정의",
      "context": "이 책에서의 사용 맥락"
    }
  ],

  "synthesis": "종합 정리: 모든 챕터를 관통하는 큰 그림 서술",
  "critical_view": "비판적 시각 (knowledge 장르): 전제의 한계, 근거의 약점 등",
  "practical_view": "실천적 시각 (selfhelp 장르): 적용 가능성, 현실적 한계",
  "flowchart_description": "Mermaid 플로우차트로 변환할 전체 흐름 서술",

  "self_test_questions": [
    "Q: 셀프 테스트 질문 1",
    "Q: 셀프 테스트 질문 2",
    "Q: 셀프 테스트 질문 3",
    "Q: 셀프 테스트 질문 4",
    "Q: 셀프 테스트 질문 5"
  ],

  "related_books": [
    {
      "title": "관련 도서 제목",
      "author": "저자",
      "relation": "보완/반론/심화/전제"
    }
  ]
}
```

## 장르별 필수/선택 필드

| 필드 | tech | knowledge | selfhelp |
|------|:----:|:---------:|:--------:|
| code_blocks | ✅ | - | - |
| frameworks | - | - | ✅ |
| action_items | - | - | ✅ |
| common_misconceptions | ✅ | ✅ | ✅ |
| critical_view | - | ✅ | - |
| practical_view | - | - | ✅ |
| evidence | ✅ | ✅ | ✅ |
| examples | ✅ | ✅ | ✅ |
| analogy | ✅ | ✅ | ✅ |
| related_books | ✅ | ✅ | ✅ |
