# OpenClaw Research Document

> Research compiled for Obsidian notes creation. Final deliverables will be in Korean.

---

## 1. Overview

**OpenClaw** (formerly Clawdbot, then Moltbot) is a free and open-source autonomous AI agent developed by Peter Steinberger (Austrian developer). It serves as a 24/7 personal AI assistant that runs locally on your own machine.

- **First released:** November 2025 (as "Clawdbot")
- **Renamed to "Moltbot":** January 27, 2026 (due to Anthropic trademark complaint)
- **Renamed to "OpenClaw":** January 30, 2026
- **GitHub stats (as of Feb 2, 2026):** 140,000+ stars, 20,000+ forks
- **Latest news (Feb 14, 2026):** Steinberger announced joining OpenAI; project moving to an open-source foundation
- **Tagline:** "Your own personal AI assistant. Any OS. Any Platform. The lobster way."

### What Makes It Different from Chatbots
Unlike ChatGPT or other standard chatbots, OpenClaw has "eyes and hands" -- it can browse the web, read/write files, and run shell commands autonomously. It is not just a conversational AI; it is an autonomous agent that takes action on your behalf.

---

## 2. Core Architecture

### Plugin System (4 Integration Types)
1. **Channels** -- messaging platform integrations (how users talk to the agent)
2. **Tools** -- agent capabilities (what the agent can do)
3. **Providers** -- AI model inference backends (the brain)
4. **Memory** -- search backends (how the agent remembers)

### How Plugins Work
- Plugin Loader scans `extensions/` workspace directory
- Discovers extensions by reading `package.json` manifest files
- Plugins can ship their own skills via `openclaw.plugin.json`
- Core stays lean; optional capability ships as plugins

### Model Support (Model-Agnostic)
- Integrates with external LLMs: Claude, DeepSeek, OpenAI GPT models
- Can run local models (Ollama) for zero-cost operation
- Privacy-focused: bring your own API keys or run entirely on local infrastructure

---

## 3. Memory System

OpenClaw's memory is a key differentiator. It avoids complex vector databases in favor of simple, editable local files.

### Two-Level Memory Architecture

#### Short-Term Memory (Daily Notes)
- **Location:** `memory/YYYY-MM-DD.md`
- **Purpose:** Raw running log of what happened each day
- **Content:** Messy context, everything that feels useful in the moment
- **Format:** Markdown files

#### Long-Term Memory (MEMORY.md)
- **Location:** `MEMORY.md` (root)
- **Purpose:** Curated, stable knowledge that stays true over time
- **Content:** User preferences, learned patterns, key facts
- **Privacy:** Only loaded in private sessions, never in group contexts

### Technical Details
- **Session logs:** `~/.openclaw/agents/<agentId>/sessions/*.jsonl`
- **Embedding cache:** SQLite at `~/.openclaw/memory/<agentId>.sqlite`
- **Search:** Cosine similarity with sqlite-vec extension + SQLite FTS5 (Full-Text Search)
- **Vector index:** Can build small vector index over `MEMORY.md` and `memory/*.md` for semantic queries
- **Reindexing:** SQLite caches chunk embeddings so unchanged text is not re-embedded

---

## 4. Heartbeat (Proactive Agent)

The "Heartbeat" feature is what makes OpenClaw truly assistant-like rather than just reactive.

- **What it does:** Allows the AI to wake up proactively and take initiative
- **Configuration:** Edit `HEARTBEAT.md` to change check-in schedule
- **Examples of proactive behavior:**
  - Cron job skill runs at 8:00 AM, checks local calendar, sends "Daily Briefing" via Telegram
  - Monitor inbox and alert about urgent emails
  - Periodically check schedule and prepare meeting materials in advance
  - Monitor specific webpage changes and notify immediately
  - Runs 24/7 without manual intervention

---

## 5. Skills & Extensibility

### What Are Skills?
- Modular extensions that grant the AI agent new abilities
- Use the `SKILL.md` standard format
- Allow interaction with external APIs, file management, code execution, complex automation

### ClawHub (Skills Marketplace)
- **URL:** https://clawhub.com
- **Stats (Feb 7, 2026):** 5,705+ community-built skills
- **CLI:** `clawdhub install <skill-name>`
- **Categories:** Web Browsing, Productivity, Development, Data Analysis
- **Self-building:** OpenClaw can write its own skills based on YouTube videos or user notes

### 100+ Preconfigured AgentSkills
- Execute shell commands
- Manage file systems
- Perform web automation
- GitHub integration
- Scheduled cron jobs
- Webhook triggers

### 20+ Bundled Extensions
- Messaging platforms
- Workflows
- Advanced features

---

## 6. Supported Channels (Messaging Platforms)

### Primary Channels
- WhatsApp
- Telegram
- Slack
- Discord
- Google Chat
- Signal
- iMessage
- Microsoft Teams
- WebChat

### Extension Channels
- BlueBubbles
- Matrix
- Zalo
- Zalo Personal

### Additional Capabilities
- Voice: speak and listen on macOS/iOS/Android
- Canvas: live Canvas rendering that users can control

---

## 7. Personal Assistant Use Cases

### Daily Life Management
- **Daily Briefing:** Automated morning briefing with calendar, email summary, weather, news
- **Calendar Management:** Timeblocking tasks based on importance, managing conflicts autonomously
- **Email Management:** Clear inbox, send emails, summarize urgent messages
- **Travel:** Check in for flights, suggest departure times based on traffic

### Productivity & Knowledge Management
- **Obsidian Integration:** Knows your Obsidian notes, can provide deeply personalized insights
- **Task Management:** Manage across Apple Notes, Apple Reminders, Things 3, Notion, Obsidian, Trello
- **All from one conversation:** Manage everything from a single WhatsApp or Telegram chat

### Web Automation
- Fill out forms
- Scrape data
- Navigate websites on your behalf
- Make restaurant reservations by phone
- Purchase tickets

### Smart Home & Health
- Control Philips Hue lights, Elgato devices
- Home Assistant integration
- Pull health data from wearables (WHOOP metrics, biomarker goals)
- Track daily health metrics

### Development & DevOps
- Automate debugging
- DevOps management
- Codebase management with GitHub integration
- Scheduled cron jobs and webhook triggers

### Advanced Use Cases (Early Adopters)
- Managing investment portfolios
- ClawWork project: "$10K earned in 7 Hours" using OpenClaw as AI coworker

---

## 8. Security Considerations

### Known Risks (CRITICAL)

#### Data Exfiltration
- 26% of analyzed agent skills contained vulnerabilities
- Tools facilitated active data exfiltration via curl commands to external servers
- Network calls executed silently without user awareness

#### Prompt Injection
- Skills conducted direct prompt injection to bypass safety guidelines
- External content (emails, web pages, skills) provided paths for adversarial prompts

#### Malicious Skills (ClawHavoc Campaign)
- Koi Security audit (early Feb 2026): 341 malicious skills identified on ClawHub
- ClawHavoc campaign: 335 infostealer packages deploying Atomic macOS Stealer, keyloggers, backdoors

#### Critical CVE
- **CVE-2026-25253:** Remote code execution (CVSS 8.8)
- Allowed attackers to hijack local instances via malicious links
- Could steal authentication tokens

### Cisco's Assessment
> "From a security perspective, OpenClaw is an absolute nightmare. It can run shell commands, read and write files, and execute scripts on your machine. Granting an AI agent high-level privileges enables it to do harmful things if misconfigured or if a user downloads a skill injected with malicious instructions."

### Best Practices for Security
1. **Reduce blast radius:** Use a read-only/tool-disabled reader agent to summarize untrusted content, then pass summary to main agent
2. **Lock down DMs:** Use pairing/allowlists for inbound direct messages
3. **Mention gating in groups:** Avoid "always-on" bots in public rooms
4. **Treat external content as hostile:** Links, attachments, pasted instructions = untrusted by default
5. **Use Cisco AI Skill Scanner:** Scan skills before installation for malware, data exfiltration, prompt injection
6. **VirusTotal integration:** OpenClaw now integrates VirusTotal scanning for ClawHub skills

---

## 9. Setup & Installation Summary

1. Run the installer command (auto-detects OS)
2. OpenClaw launches interactive terminal UI (TUI) for setup
3. Configure LLM provider (API key for Claude/OpenAI/DeepSeek, or local Ollama)
4. Connect messaging channels (Telegram, WhatsApp, etc.)
5. Configure memory system (MEMORY.md, daily notes)
6. Set up heartbeat schedule (HEARTBEAT.md)
7. Install skills from ClawHub as needed
8. Customize agent personality and preferences

---

## 10. Key Terminology

| Term | Meaning |
|------|---------|
| OpenClaw | The open-source AI personal assistant (formerly Clawdbot/Moltbot) |
| ClawHub | Public skills registry/marketplace for OpenClaw |
| SKILL.md | Standard format for defining skills |
| MEMORY.md | Long-term memory file (curated, stable) |
| HEARTBEAT.md | Proactive schedule configuration |
| AgentSkills | Preconfigured capabilities (100+) |
| Channels | Messaging platform integrations |
| Providers | LLM backends (Claude, GPT, DeepSeek, Ollama) |
| Peter Steinberger | Creator of OpenClaw |

---

## 11. Sources

- [OpenClaw Official Website](https://openclaw.ai/)
- [OpenClaw GitHub Repository](https://github.com/openclaw/openclaw)
- [OpenClaw Wikipedia](https://en.wikipedia.org/wiki/OpenClaw)
- [OpenClaw Documentation - Memory](https://docs.openclaw.ai/concepts/memory)
- [OpenClaw Documentation - Skills](https://docs.openclaw.ai/tools/skills)
- [OpenClaw Documentation - Security](https://docs.openclaw.ai/gateway/security)
- [ClawHub Skills Registry](https://github.com/openclaw/clawhub)
- [DigitalOcean - What is OpenClaw?](https://www.digitalocean.com/resources/articles/what-is-openclaw)
- [Cisco Blog - Security Nightmare](https://blogs.cisco.com/ai/personal-ai-agents-like-openclaw-are-a-security-nightmare)
- [Codecademy - OpenClaw Tutorial](https://www.codecademy.com/article/open-claw-tutorial-installation-to-first-chat-setup)
- [MacStories - Future of Personal AI](https://www.macstories.net/stories/clawdbot-showed-me-what-the-future-of-personal-ai-assistants-looks-like/)
- [OpenClaw Use Cases Directory (175+)](https://www.foxessellfaster.com/blog/openclaw-use-cases-directory-175-ways-to-use-your-ai-assistant-updated-daily/)
- [OpenClaw Memory Architecture Guide](https://zenvanriel.nl/ai-engineer-blog/openclaw-memory-architecture-guide/)
- [OpenClaw Mega Cheatsheet](https://moltfounders.com/openclaw-mega-cheatsheet)
- [ClawWork - OpenClaw as AI Coworker](https://github.com/HKUDS/ClawWork)
- [Awesome OpenClaw Skills](https://github.com/VoltAgent/awesome-openclaw-skills)
- [Giskard - OpenClaw Security Vulnerabilities](https://www.giskard.ai/knowledge/openclaw-security-vulnerabilities-include-data-leakage-and-prompt-injection-risks)
- [The Hacker News - VirusTotal Scanning Integration](https://thehackernews.com/2026/02/openclaw-integrates-virustotal-scanning.html)
- [Jose Casanova - Daily Intelligence Briefing](https://www.josecasanova.com/blog/openclaw-daily-intel-report)
