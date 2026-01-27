---
type: moc
aliases:
  - CMDS Guide
  - Standards
  - Conventions
author:
  - "[[구요한]]"
date created: 2025-01-19
date modified: 2025-01-19
tags:
  - CMDS
  - guide
  - standards
CMDS:
index:
status:
---

# 🏛 CMDS Guide

**Operational Standards & Conventions for the CMDS System**

This guide ensures consistency and quality across your knowledge base.

---

## 📋 Required Properties (v2.0)

Every note MUST include these 5 core properties:

```yaml
---
type: note
aliases: []
author:
  - "[[구요한]]"
date created: YYYY-MM-DD
date modified: YYYY-MM-DD
tags: []
---
```

### Core Properties Explained

#### 1. `type:` (Required)
Note type/category. Common types:
- `note` - General notes
- `terminology` - Term definitions
- `meeting` - Meeting notes
- `people` - People profiles
- `curriculum` - Course curriculum
- `moc` - Map of Content
- `CMDS` - CMDS index pages

#### 2. `aliases:` (Required)
Alternative names for the note. Array format:
```yaml
aliases:
  - Alternative Name
  - Another Name
```
Empty is OK: `aliases: []`

#### 3. `author:` (Required)
Author(s) with wikilinks. Array format:
```yaml
author:
  - "[[구요한]]"
  - "[[Co-author Name]]"
```
⚠️ **CRITICAL**: Wikilinks MUST be quoted in YAML!

#### 4. `date created:` (Required)
Creation date in ISO 8601 format:
```yaml
date created: 2025-01-19
```
**Always use**: `YYYY-MM-DD` format

#### 5. `tags:` (Required)
Relevant tags. Array format:
```yaml
tags:
  - AI시대
  - 생산성
  - PKM
```
Empty is OK: `tags: []`

### Optional Properties

#### CMDS Reference
```yaml
CMDS: "[[📖 200 Literature]]"
```
Links to relevant CMDS category.

#### Index Reference
```yaml
index: "[[🏷 Meeting Notes]]"
```
Links to index/MOC page.

#### Status
```yaml
status: inProgress
```
Standard values:
- `unread` - Not yet read
- `reading` - Currently reading
- `inProgress` - Work in progress
- `completed` - Finished
- `archived` - Archived

#### Custom Properties (camelCase)
Use camelCase for compound words:
```yaml
totalPage: 350
myRate: 4.5
startReadDate: 2025-01-15
```

---

## 🎨 YAML Frontmatter Rules

### Critical Indentation Rule
⚠️ **YAML frontmatter uses 2 SPACES (NOT tabs)**

✅ **CORRECT**:
```yaml
---
author:
  - "[[구요한]]"    # ← 2 spaces
tags:
  - PKM           # ← 2 spaces
---
```

❌ **WRONG**:
```yaml
---
author:
	- "[[구요한]]"    # ← TAB - WRONG!
---
```

### Wikilinks Must Be Quoted
✅ **CORRECT**:
```yaml
CMDS: "[[📖 200 Literature]]"
organization: "[[SK Innovation]]"
```

❌ **WRONG**:
```yaml
CMDS: [[📖 200 Literature]]      # Missing quotes!
organization: [[SK Innovation]]   # Missing quotes!
```

### Array Format
Use hyphen + space for arrays:
```yaml
author:
  - "[[구요한]]"
  - "[[공동저자]]"

tags:
  - AI
  - 생산성
```

---

## 📝 Markdown Body Rules

### Critical Indentation Rule
⚠️ **Markdown body uses TAB (NOT spaces)**

✅ **CORRECT**:
```markdown
- First level item
	- Second level (TAB)
		- Third level (TAB TAB)
```

❌ **WRONG**:
```markdown
- First level item
  - Second level (spaces) - WRONG!
    - Third level (spaces) - WRONG!
```

### Wikilinks
Use `[[double brackets]]` for internal links:
```markdown
See [[📖 200 Literature]] for more details.
Related to [[구요한]]'s research.
```

**NOT** markdown links:
```markdown
❌ See [200 Literature](200%20Literature.md)  # Wrong!
✅ See [[📖 200 Literature]]                    # Correct!
```

---

## 🗂️ File Naming Conventions

### General Notes
```
Descriptive Title.md
```
Examples:
- `Zettelkasten Method.md`
- `Second Brain Overview.md`
- `AI in Education.md`

### Dated Notes
```
YYYY-MM-DD-description.md
```
Examples:
- `2025-01-19-daily-note.md`
- `2025-01-19-team-meeting.md`
- `2025-01-19-research-summary.md`

### CMDS Categories
```
📖 N00 Category Name/
```
Examples:
- `📖 100 Themes/`
- `📖 200 Literature/`
- `📚 620 Generative AI/`

### Special Prefixes
Use emoji prefixes for special note types:
- `🏛` - Main hub/guide notes
- `📖` - 1st level CMDS (100-900)
- `📚` - 2nd level CMDS (N01-N99)
- `🏷` - Index pages
- `📎` - Web clips
- `📦` - Reviews

---

## 🔗 Linking Best Practices

### Link Liberally
Create connections between related notes:
```markdown
This concept relates to [[Zettelkasten Method]] and 
builds on [[Second Brain Overview]].

See also: [[구요한]]'s work on [[PKM Systems]].
```

### Link Types

**Basic link**:
```markdown
[[Note Name]]
```

**Link with alias**:
```markdown
[[Note Name|Custom Display Text]]
```

**Link to heading**:
```markdown
[[Note Name#Heading]]
```

**Link to block**:
```markdown
[[Note Name^block-id]]
```

**Embed note**:
```markdown
![[Note Name]]
```

**Embed image**:
```markdown
![[image.png]]
```

---

## 📁 File Organization

### Where to Put New Notes

**Capture Phase**:
1. Start in `00. Inbox/` - capture quickly without overthinking
2. Add to appropriate subfolder if obvious:
   - Daily thoughts → `01. Daily Notes/`
   - Code from Claude → `03. Claude Code/`
   - Web clips → `07. Clippings/`

**Processing Phase**:
1. Review inbox regularly (daily/weekly)
2. Add proper frontmatter
3. Create connections
4. Move to appropriate CMDS category:
   - Ideas/terms → `📖 100 Themes/`
   - Book notes → `📖 200 Literature/`
   - Data → `📖 300 Data/`
   - Methods → `📖 400 Methodologies/`
   - Tool docs → `📖 500 Products/`
   - Expertise → `📖 600 Specialties/`
   - Creative work → `📖 700 Creatives/`
   - Final outputs → `📖 800 Outputs/`
   - Operations → `📖 900 Divisions/`

**Refinement Phase**:
- Extract core insights → `30. Permanent Notes/`
- Create MOCs for related topics
- Build knowledge graph through links

---

## 🎯 Note Types & Templates

### Basic Note
**Use**: General-purpose notes
**Template**: `Template_00. Basic Note.md`
**Location**: Any CMDS category

### Daily Note
**Use**: Daily journal entries
**Template**: `Template_01. Daily Note.md`
**Location**: `00. Inbox/01. Daily Notes/`
**Format**: `YYYY-MM-DD.md`

### Meeting Minutes
**Use**: Meeting notes and action items
**Template**: `Template_05. Meeting Minutes.md`
**Location**: `70. Collections/74. Meetings/`

### People Profile
**Use**: Contact and relationship tracking
**Template**: `Template_51. People.md`
**Location**: `70. Collections/71. People/`

### Map of Content (MOC)
**Use**: Navigation and topic organization
**Template**: `Template_90. CMDS MOC.md`
**Location**: Any CMDS category or Collections

---

## 🏗️ CMDS Hierarchy

### Three Levels

**Level 1: Main Categories** (9 categories)
```
🏛 Top (Home/Guide)
📖 100-900 (Main CMDS Categories)
```

**Level 2: Subcategories** (Expandable)
```
📚 N01-N99 (Subcategories)
```
Examples:
- `📚 610 Knowledge Management`
- `📚 620 Generative AI`
- `📚 630 Second Brain`

**Level 3: Individual Notes** (No icon)
```
Regular note names
```
Examples:
- `Zettelkasten Method`
- `AI Prompt Engineering`
- `Meeting - 2025-01-19`

---

## 🎨 Style & Formatting

### Headers
Use ATX-style headers with proper hierarchy:
```markdown
# Main Title (H1 - once per note)
## Section (H2)
### Subsection (H3)
#### Detail (H4)
```

### Lists
Use tabs for indentation in markdown body:
```markdown
- First level
	- Second level (TAB)
		- Third level (TAB TAB)
```

### Code Blocks
Include language for syntax highlighting:
````markdown
```python
def hello_world():
    print("Hello, World!")
```
````

### Callouts
Use Obsidian callout syntax:
```markdown
> [!note] Note
> This is a note callout.

> [!warning] Warning
> This is a warning callout.

> [!tip] Tip
> This is a tip callout.
```

---

## 🔄 Workflow Patterns

### Capture → Process → Connect → Output

**1. Capture (00. Inbox/)**
```markdown
Quick note in inbox with minimal formatting
```

**2. Process (Add Properties)**
```yaml
---
type: note
aliases: []
author:
  - "[[구요한]]"
date created: 2025-01-19
date modified: 2025-01-19
tags:
  - relevant-tag
---
```

**3. Connect (Add Links)**
```markdown
Related to [[Other Note]] and builds on [[Previous Concept]].
```

**4. Move to CMDS Category**
```
00. Inbox/ → 📖 Appropriate Category/
```

**5. Refine (Optional)**
```
Extract core insight → 30. Permanent Notes/
```

---

## ✅ Quality Checklist

Before finalizing a note, verify:

- [ ] Has all 5 required properties
- [ ] Dates in YYYY-MM-DD format
- [ ] Author with quoted wikilinks
- [ ] YAML uses 2 spaces (not tabs)
- [ ] Markdown body uses tabs (not spaces)
- [ ] At least 2-3 outgoing links
- [ ] Clear, descriptive title
- [ ] Proper CMDS category
- [ ] Tags are relevant and consistent

---

## 🚨 Common Mistakes to Avoid

### 1. Wrong Indentation
❌ Tabs in YAML frontmatter
❌ Spaces in markdown body
✅ 2 spaces in YAML, tabs in markdown

### 2. Unquoted Wikilinks in YAML
❌ `CMDS: [[200 Literature]]`
✅ `CMDS: "[[200 Literature]]"`

### 3. Wrong Date Format
❌ `date created: 01/19/2025`
❌ `date created: 2025.01.19`
✅ `date created: 2025-01-19`

### 4. Missing Required Properties
Every note needs: type, aliases, author, date created, tags

### 5. Broken Links
Use exact note names in wikilinks (case-sensitive!)

---

## 📚 References

- [[CLAUDE]] - Technical implementation details
- [[CMDS]] - System philosophy and context
- [[🏛 CMDS Head Quarter]] - Navigation hub

---

*Last updated: 2025-01-19*
*Guide version: 2.0*
