# Obsidian Notes Architecture Plan — Claudegram (OpenClaw Personal Assistant)

## Overview

This document defines the information architecture for Obsidian notes about Claudegram/OpenClaw as a personal assistant. The notes are written in Korean and designed for an Obsidian vault with rich backlinks, tags, and cross-references.

---

## 1. Topic Areas (6 Main Notes)

### Note 1: `index` — Claudegram 개요 (Overview / Table of Contents)
- **Purpose:** Entry point and master index for the entire vault
- **Content:**
  - What is Claudegram — one-paragraph summary
  - Architecture diagram (Telegram -> Grammy -> Claude Agent SDK -> Local Machine)
  - Quick navigation to all topic notes via backlinks
  - Key stats: tech stack, license, repository link
- **Links to:** All other notes
- **Tags:** `#claudegram` `#overview` `#index`

### Note 2: `setup-and-config` — 설치 및 설정 (Setup & Configuration)
- **Purpose:** Complete setup guide and configuration reference
- **Content:**
  - Prerequisites (Node.js 18+, Claude Code CLI, Telegram bot token, user ID)
  - Installation steps (clone, .env, npm install, npm run dev)
  - Environment variables reference table (Required / Core / Reddit / Medium / Voice & TTS)
  - Bot control script usage (claudegram-botctl.sh)
  - Development modes (dev vs prod, self-editing workflow)
  - Security configuration (user whitelist, permission modes, dangerous mode)
- **Links to:** `[[index]]`, `[[commands-and-features]]`, `[[integrations]]`
- **Tags:** `#setup` `#config` `#env` `#security`

### Note 3: `architecture` — 아키텍처 (Architecture & Code Structure)
- **Purpose:** Technical deep-dive into how Claudegram works
- **Content:**
  - Source directory tree with descriptions
  - Core modules:
    - `bot/` — Grammy bot setup, command/message/voice/photo handlers, auth middleware
    - `claude/` — Agent SDK integration, session management, request queue, command parser
    - `telegram/` — Message sender (streaming/chunking), MarkdownV2, Telegraph, deduplication
    - `tts/` — TTS provider routing, voice settings, voice reply hook
    - `audio/` — Transcription utilities
    - `reddit/` — Reddit video download & compression pipeline
    - `medium/` — Freedium article fetcher
    - `utils/` — Download, sanitize, file-type, URL guard, workspace guard
  - Data flow: User message -> auth middleware -> handler routing -> agent query -> streaming response
  - Session lifecycle: create -> resume -> clear
  - Security model: URL validation, path sanitization, error sanitization, workspace guard
- **Links to:** `[[index]]`, `[[setup-and-config]]`, `[[commands-and-features]]`
- **Tags:** `#architecture` `#code` `#technical` `#security`

### Note 4: `commands-and-features` — 명령어 및 기능 (Commands & Features)
- **Purpose:** Complete reference of all bot commands and user-facing features
- **Content:**
  - **Session commands:** /start, /project, /newproject, /clear, /status, /sessions, /resume, /continue
  - **Agent mode commands:** /plan, /explore, /loop, /model, /mode
  - **Content commands:** /reddit, /vreddit, /medium, /file, /telegraph
  - **Voice & TTS commands:** /tts, /transcribe, voice note auto-transcription
  - **Utility commands:** /ping, /context, /botstatus, /restartbot, /cancel, /commands
  - **Features overview:**
    - Full Claude Code agent with tool access (Bash, Read, Write, Edit, Glob, Grep)
    - Session resume across messages
    - Streaming responses with live-updating
    - Model picker (Sonnet / Opus / Haiku)
    - Image uploads with Claude notification
    - Rich output: MarkdownV2, Telegraph Instant View, smart chunking, ForceReply, inline keyboards
- **Links to:** `[[index]]`, `[[integrations]]`, `[[architecture]]`, `[[workflows]]`
- **Tags:** `#commands` `#features` `#reference`

### Note 5: `integrations` — 외부 연동 (External Integrations)
- **Purpose:** Detailed guide for each integration module
- **Content:**
  - **Reddit Integration:**
    - /reddit — posts, subreddits, user profiles via redditfetch.py
    - /vreddit — video download with DASH manifests + ffmpeg
    - Auto-compression for videos > 50 MB
    - Large threads auto-export to JSON
    - Config: REDDITFETCH_PATH, REDDIT_VIDEO_MAX_SIZE_MB, etc.
  - **Medium Integration:**
    - /medium — paywalled articles via Freedium mirror
    - Telegraph Instant View, Markdown save, or both
    - Pure TypeScript, no Python/Playwright
    - Config: FREEDIUM_HOST, MEDIUM_TIMEOUT_MS, etc.
  - **Voice Transcription (Groq Whisper):**
    - Voice note auto-transcription
    - /transcribe standalone command
    - Config: GROQ_API_KEY, GROQ_TRANSCRIBE_PATH
  - **Text-to-Speech (OpenAI TTS):**
    - /tts toggle and voice selection
    - 13 voices available (alloy, ash, ballad, cedar, coral, echo, fable, marin, nova, onyx, sage, shimmer, verse)
    - Config: OPENAI_API_KEY, TTS_VOICE, TTS_MODEL
  - **Telegraph Output:**
    - Instant View for long responses and tables
    - /telegraph toggle
- **Links to:** `[[index]]`, `[[setup-and-config]]`, `[[commands-and-features]]`
- **Tags:** `#integrations` `#reddit` `#medium` `#voice` `#tts` `#telegraph`

### Note 6: `workflows` — 활용 워크플로우 (Usage Workflows & Guides)
- **Purpose:** Practical workflows and use-case guides for personal assistant usage
- **Content:**
  - **Workflow 1: Code Development from Phone**
    1. /project to set working directory
    2. Send task description in natural language
    3. Claude reads files, edits code, runs tests
    4. Review streaming output in Telegram
    5. /continue to resume if interrupted
  - **Workflow 2: Content Research & Summarization**
    1. /reddit to fetch and summarize Reddit threads
    2. /medium to read paywalled articles
    3. Ask Claude to synthesize findings
  - **Workflow 3: Voice-Driven Interaction**
    1. Send voice note -> auto-transcribed -> Claude processes
    2. /tts enable for spoken responses
    3. Hands-free coding/research loop
  - **Workflow 4: Multi-Session Project Management**
    1. /newproject to create isolated workspaces
    2. /sessions to list all active sessions
    3. /resume to switch between projects
    4. /status to check current context
  - **Workflow 5: Self-Editing (Claudegram editing itself)**
    1. Use prod mode (no hot reload)
    2. Let Claude edit files
    3. Restart with botctl script
    4. /continue to restore session
  - **Tips & Best Practices:**
    - Use /plan for complex multi-step tasks
    - Use /explore for codebase questions
    - Use /loop for iterative tasks
    - Monitor tokens with /context
    - Use /model to switch between speed (Haiku) and capability (Opus)
- **Links to:** `[[index]]`, `[[commands-and-features]]`, `[[integrations]]`, `[[setup-and-config]]`
- **Tags:** `#workflows` `#guide` `#tips` `#personal-assistant`

---

## 2. Backlink Relationship Map

```
                    ┌─────────────┐
                    │   index     │
                    │   (개요)     │
                    └──────┬──────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
   ┌────────▼───────┐ ┌───▼────────┐ ┌──▼──────────────┐
   │ setup-and-     │ │ architecture│ │ commands-and-   │
   │ config         │ │             │ │ features        │
   │ (설치 및 설정)  │ │ (아키텍처)   │ │ (명령어 및 기능) │
   └───────┬────────┘ └──┬─────────┘ └──┬──────────────┘
           │             │              │
           │    ┌────────┴───┐     ┌────▼──────────┐
           │    │            │     │               │
           └────▶ integrations◀────┤ workflows     │
                │            │     │ (활용 워크플로우)│
                │ (외부 연동)  │     │               │
                └────────────┘     └───────────────┘
```

### Bidirectional Backlinks:
- `index` <-> all notes (hub-and-spoke)
- `setup-and-config` <-> `commands-and-features` (config enables features)
- `setup-and-config` <-> `integrations` (integration setup details)
- `architecture` <-> `commands-and-features` (code implements commands)
- `commands-and-features` <-> `integrations` (commands use integrations)
- `commands-and-features` <-> `workflows` (commands compose into workflows)
- `integrations` <-> `workflows` (integrations power workflows)

---

## 3. TOC Structure for `_index`

```markdown
# Claudegram — Personal AI Assistant Notes

## Navigation
- [[index|Claudegram 개요]]
  - [[setup-and-config|설치 및 설정]]
  - [[architecture|아키텍처]]
  - [[commands-and-features|명령어 및 기능]]
  - [[integrations|외부 연동]]
  - [[workflows|활용 워크플로우]]

## Quick Links
- [[commands-and-features#Session commands|세션 명령어]]
- [[commands-and-features#Agent mode commands|에이전트 모드]]
- [[integrations#Reddit Integration|Reddit 연동]]
- [[integrations#Medium Integration|Medium 연동]]
- [[integrations#Voice Transcription|음성 인식]]
- [[integrations#Text-to-Speech|텍스트 음성 변환]]
- [[workflows#Code Development from Phone|폰으로 코딩하기]]
- [[workflows#Voice-Driven Interaction|음성 기반 사용]]
```

---

## 4. Note Template

Each note should follow this template:

```markdown
---
title: [Korean Title]
tags: [tag1, tag2, tag3]
created: 2026-02-20
updated: 2026-02-20
---

# [Korean Title]

> [One-line summary in Korean]

## 목차 (Table of Contents)
- [[#Section 1]]
- [[#Section 2]]
- ...

---

## Section 1

[Content in Korean]

## Section 2

[Content in Korean]

---

## 관련 노트 (Related Notes)
- [[note-name|Display Name in Korean]]
- [[note-name|Display Name in Korean]]
```

### Template Rules:
1. YAML frontmatter with title, tags, and dates
2. Korean title as H1
3. Blockquote summary line
4. Table of contents with internal links
5. Content sections in Korean
6. Related notes section at bottom with `[[backlinks]]`
7. Use callouts for tips: `> [!tip]` and warnings: `> [!warning]`
8. Use code blocks for commands and configuration examples
9. Use tables for reference data (env vars, command lists)

---

## 5. Tag Taxonomy

| Tag | Purpose |
|-----|---------|
| `#claudegram` | Top-level project tag |
| `#overview` | Summary/intro content |
| `#setup` | Installation and setup |
| `#config` | Configuration and environment |
| `#security` | Security-related topics |
| `#architecture` | Code structure and design |
| `#technical` | Technical deep-dives |
| `#commands` | Bot commands |
| `#features` | User-facing features |
| `#reference` | Reference material |
| `#integrations` | External service integrations |
| `#reddit` | Reddit-specific |
| `#medium` | Medium-specific |
| `#voice` | Voice/audio features |
| `#tts` | Text-to-speech |
| `#telegraph` | Telegraph output |
| `#workflows` | Usage patterns |
| `#guide` | How-to guides |
| `#tips` | Tips and best practices |
| `#personal-assistant` | PA use cases |

---

## 6. File Structure

```
obsidian/
├── _index              # Master TOC and navigation
├── _research           # Research notes (from researcher)
├── _architecture       # This file (architecture plan)
├── index               # Claudegram 개요
├── setup-and-config    # 설치 및 설정
├── architecture        # 아키텍처
├── commands-and-features # 명령어 및 기능
├── integrations        # 외부 연동
└── workflows           # 활용 워크플로우
```

---

## 7. Design Decisions

1. **6 notes (not more):** Keeps the vault focused and navigable. Each note covers a distinct concern.
2. **Hub-and-spoke from index:** The overview note links to everything, making it the natural starting point in Obsidian graph view.
3. **Korean content, English filenames:** Filenames use English kebab-case for cross-platform compatibility; all content is in Korean.
4. **Workflows note as practical guide:** Goes beyond reference material to show real usage patterns for personal assistant scenarios.
5. **Rich backlinks at section level:** Allows linking to specific sections (e.g., `[[integrations#Reddit Integration]]`) for precise navigation.
6. **YAML frontmatter:** Enables Obsidian's metadata features (Dataview queries, tag filtering, date sorting).
7. **Consistent template:** Every note follows the same structure for predictability and readability.
