# Review Control Tower Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Obsidian 학습 노트의 복습 스케줄을 자동 관리하는 로컬 웹 대시보드 구축

**Architecture:** FastAPI 백엔드가 Obsidian vault의 frontmatter를 읽고 쓰며, Next.js 프론트엔드가 SWR로 데이터를 fetching. Optimistic Locking(MD5 hash)으로 동시 수정 충돌 방지.

**Tech Stack:** Python 3.10+, FastAPI, python-frontmatter, Next.js 14 (App Router), SWR, shadcn/ui, Tailwind CSS

**PRD Reference:** `/Users/aera/Desktop/Base_/.omc/PRD_Review_Control_Tower.md`

---

## File Structure

### Backend (`/Users/aera/Desktop/Base_/.scripts/review-control-tower/backend/`)

```
backend/
├── main.py                      # FastAPI app entry point
├── requirements.txt             # Python dependencies
├── config.py                    # Configuration (vault path, ports)
├── routers/
│   ├── __init__.py
│   ├── reviews.py               # /api/reviews/* endpoints
│   ├── anki.py                  # /api/anki/* endpoints
│   └── health.py                # /api/health endpoint
├── services/
│   ├── __init__.py
│   ├── vault_scanner.py         # Scan vault for review notes
│   ├── frontmatter_service.py   # Read/update frontmatter
│   ├── spaced_repetition.py     # Calculate next review date
│   └── anki_connect.py          # AnkiConnect integration
├── models/
│   ├── __init__.py
│   └── review_note.py           # Pydantic models
├── utils/
│   ├── __init__.py
│   ├── normalizer.py            # normalize_review_array()
│   └── hash.py                  # Content hash utilities
└── tests/
    ├── __init__.py
    ├── test_vault_scanner.py
    ├── test_frontmatter_service.py
    ├── test_spaced_repetition.py
    ├── test_normalizer.py
    └── test_api.py
```

### Frontend (`/Users/aera/Desktop/Base_/.scripts/review-control-tower/frontend/`)

```
frontend/
├── package.json
├── next.config.js
├── tailwind.config.js
├── tsconfig.json
├── app/
│   ├── layout.tsx               # Root layout with providers
│   ├── page.tsx                 # Dashboard page
│   └── globals.css              # Tailwind imports
├── components/
│   ├── ui/                      # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   └── badge.tsx
│   ├── stats-card.tsx           # Stats display card
│   ├── review-card.tsx          # Individual review note card
│   ├── review-list.tsx          # List of review cards
│   ├── confidence-modal.tsx     # Confidence selection modal
│   └── anki-status.tsx          # Anki connection status
├── lib/
│   ├── api.ts                   # API client functions
│   ├── types.ts                 # TypeScript types
│   └── utils.ts                 # Utility functions
└── hooks/
    ├── use-reviews.ts           # SWR hook for reviews
    └── use-anki.ts              # SWR hook for Anki status
```

---

## Task 1: Project Setup

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/config.py`
- Create: `backend/main.py`
- Create: `frontend/package.json`

### Steps

- [ ] **Step 1.1: Create project directories**

```bash
mkdir -p /Users/aera/Desktop/Base_/.scripts/review-control-tower/{backend,frontend}
mkdir -p /Users/aera/Desktop/Base_/.scripts/review-control-tower/backend/{routers,services,models,utils,tests}
touch /Users/aera/Desktop/Base_/.scripts/review-control-tower/backend/{routers,services,models,utils,tests}/__init__.py
```

- [ ] **Step 1.2: Create backend requirements.txt**

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-frontmatter==1.1.0
httpx==0.26.0
pydantic==2.6.0
pytest==8.0.0
pytest-asyncio==0.23.0
```

- [ ] **Step 1.3: Create backend config.py**

```python
from pathlib import Path

# Obsidian Vault Configuration
VAULT_PATH = Path("/Users/aera/Desktop/Base_")

# Review target directories (relative to vault)
REVIEW_DIRS = [
    "0. Ai agent/Yt-to-Note",
    "Book-to-Note",
]

# Review target types
REVIEW_TYPES = ["yt-note", "book-note", "concept"]

# AnkiConnect
ANKI_CONNECT_URL = "http://localhost:8765"
ANKI_TIMEOUT = 2.0

# Allowed frontmatter fields for update
ALLOWED_UPDATE_FIELDS = {"review", "confidence", "next_review", "review_phase", "difficulty"}
```

- [ ] **Step 1.4: Create minimal backend main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Review Control Tower API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
```

- [ ] **Step 1.5: Verify backend starts**

Run: `cd /Users/aera/Desktop/Base_/.scripts/review-control-tower/backend && pip install -r requirements.txt && uvicorn main:app --reload --port 8000`
Expected: Server starts on http://localhost:8000

- [ ] **Step 1.6: Initialize frontend with Next.js**

```bash
cd /Users/aera/Desktop/Base_/.scripts/review-control-tower
npx create-next-app@14 frontend --typescript --tailwind --eslint --app --src-dir=false --import-alias="@/*"
```

- [ ] **Step 1.7: Install frontend dependencies**

```bash
cd /Users/aera/Desktop/Base_/.scripts/review-control-tower/frontend
npm install swr
npx shadcn@latest init -y
npx shadcn@latest add button card dialog badge
```

- [ ] **Step 1.8: Commit initial setup**

```bash
cd /Users/aera/Desktop/Base_/.scripts/review-control-tower
git init
git add .
git commit -m "chore: initial project setup with FastAPI and Next.js"
```

---

## Task 2: Review Array Normalizer

**Files:**
- Create: `backend/utils/normalizer.py`
- Create: `backend/tests/test_normalizer.py`

### Steps

- [ ] **Step 2.1: Write failing tests for normalizer**

```python
# backend/tests/test_normalizer.py
import pytest
from utils.normalizer import normalize_review_array

class TestNormalizeReviewArray:
    def test_none_returns_three_nulls(self):
        result = normalize_review_array(None)
        assert result == [None, None, None]

    def test_empty_list_padded_to_three(self):
        result = normalize_review_array([])
        assert result == [None, None, None]

    def test_partial_list_padded(self):
        result = normalize_review_array(["2026-03-01"])
        assert result == ["2026-03-01", None, None]

    def test_full_list_preserved(self):
        result = normalize_review_array(["2026-01-01", "2026-02-01", "2026-03-01"])
        assert result == ["2026-01-01", "2026-02-01", "2026-03-01"]

    def test_string_converted_to_list(self):
        result = normalize_review_array("2026-03-01")
        assert result == ["2026-03-01", None, None]

    def test_null_string_converted_to_none(self):
        result = normalize_review_array(["2026-03-01", "null", None])
        assert result == ["2026-03-01", None, None]

    def test_empty_string_converted_to_none(self):
        result = normalize_review_array(["2026-03-01", "", None])
        assert result == ["2026-03-01", None, None]
```

- [ ] **Step 2.2: Run tests to verify they fail**

Run: `cd /Users/aera/Desktop/Base_/.scripts/review-control-tower/backend && python -m pytest tests/test_normalizer.py -v`
Expected: FAIL with "ModuleNotFoundError" or "ImportError"

- [ ] **Step 2.3: Implement normalizer**

```python
# backend/utils/normalizer.py
from typing import Any, List, Optional
import logging

logger = logging.getLogger(__name__)

def normalize_review_array(review_value: Any, min_length: int = 3) -> List[Optional[str]]:
    """
    Normalize review field to consistent list format.

    Args:
        review_value: Raw value from frontmatter
        min_length: Minimum array length (default 3 for 3-phase review)

    Returns:
        Normalized list with None for empty slots
    """
    # Case 1: None or missing
    if review_value is None:
        return [None] * min_length

    # Case 2: Already a list
    if isinstance(review_value, list):
        result = list(review_value)
        # Pad if too short
        while len(result) < min_length:
            result.append(None)
        # Convert 'null' strings and empty strings to None
        return [None if v in (None, 'null', '') else v for v in result]

    # Case 3: Single string (legacy format)
    if isinstance(review_value, str):
        if review_value in ('null', ''):
            return [None] * min_length
        return [review_value] + [None] * (min_length - 1)

    # Case 4: Unexpected type
    logger.warning(f'Unexpected review format: {type(review_value)} - {review_value}')
    return [None] * min_length
```

- [ ] **Step 2.4: Run tests to verify they pass**

Run: `cd /Users/aera/Desktop/Base_/.scripts/review-control-tower/backend && python -m pytest tests/test_normalizer.py -v`
Expected: All 7 tests PASS

- [ ] **Step 2.5: Commit**

```bash
git add backend/utils/normalizer.py backend/tests/test_normalizer.py
git commit -m "feat: add review array normalizer with edge case handling"
```

---

## Task 3: Spaced Repetition Calculator

**Files:**
- Create: `backend/services/spaced_repetition.py`
- Create: `backend/tests/test_spaced_repetition.py`

### Steps

- [ ] **Step 3.1: Write failing tests**

```python
# backend/tests/test_spaced_repetition.py
import pytest
from datetime import date
from services.spaced_repetition import calculate_next_review, get_base_interval, get_confidence_multiplier

class TestGetBaseInterval:
    def test_phase_0_returns_1(self):
        assert get_base_interval(0) == 1

    def test_phase_1_returns_7(self):
        assert get_base_interval(1) == 7

    def test_phase_2_returns_30(self):
        assert get_base_interval(2) == 30

    def test_phase_3_plus_returns_30(self):
        assert get_base_interval(3) == 30
        assert get_base_interval(5) == 30

class TestGetConfidenceMultiplier:
    def test_confidence_1_returns_0_5(self):
        assert get_confidence_multiplier(1) == 0.5

    def test_confidence_3_returns_1_0(self):
        assert get_confidence_multiplier(3) == 1.0

    def test_confidence_5_returns_1_5(self):
        assert get_confidence_multiplier(5) == 1.5

    def test_invalid_confidence_returns_1_0(self):
        assert get_confidence_multiplier(None) == 1.0
        assert get_confidence_multiplier(0) == 1.0
        assert get_confidence_multiplier(6) == 1.0

class TestCalculateNextReview:
    def test_phase_0_confidence_3(self):
        # Base: 1 day, Multiplier: 1.0 = 1 day
        result = calculate_next_review(
            review_phase=0,
            confidence=3,
            from_date=date(2026, 3, 19)
        )
        assert result == date(2026, 3, 20)

    def test_phase_1_confidence_5(self):
        # Base: 7 days, Multiplier: 1.5 = 10.5 -> 11 days
        result = calculate_next_review(
            review_phase=1,
            confidence=5,
            from_date=date(2026, 3, 19)
        )
        assert result == date(2026, 3, 30)

    def test_phase_2_confidence_1(self):
        # Base: 30 days, Multiplier: 0.5 = 15 days
        result = calculate_next_review(
            review_phase=2,
            confidence=1,
            from_date=date(2026, 3, 19)
        )
        assert result == date(2026, 4, 3)
```

- [ ] **Step 3.2: Run tests to verify they fail**

Run: `cd /Users/aera/Desktop/Base_/.scripts/review-control-tower/backend && python -m pytest tests/test_spaced_repetition.py -v`
Expected: FAIL

- [ ] **Step 3.3: Implement spaced repetition calculator**

```python
# backend/services/spaced_repetition.py
from datetime import date, timedelta
from typing import Optional

# Base intervals by review phase
BASE_INTERVALS = {
    0: 1,   # Phase 0 -> 1: 1 day
    1: 7,   # Phase 1 -> 2: 7 days
    2: 30,  # Phase 2 -> 3: 30 days
}
DEFAULT_INTERVAL = 30  # Phase 3+

# Confidence multipliers
CONFIDENCE_MULTIPLIERS = {
    1: 0.5,
    2: 0.75,
    3: 1.0,
    4: 1.25,
    5: 1.5,
}
DEFAULT_MULTIPLIER = 1.0

MAX_INTERVAL = 365  # Maximum days until next review


def get_base_interval(review_phase: int) -> int:
    """Get base interval for given review phase."""
    return BASE_INTERVALS.get(review_phase, DEFAULT_INTERVAL)


def get_confidence_multiplier(confidence: Optional[int]) -> float:
    """Get multiplier for given confidence level."""
    if confidence is None or confidence not in CONFIDENCE_MULTIPLIERS:
        return DEFAULT_MULTIPLIER
    return CONFIDENCE_MULTIPLIERS[confidence]


def calculate_next_review(
    review_phase: int,
    confidence: int,
    from_date: Optional[date] = None
) -> date:
    """
    Calculate the next review date based on spaced repetition algorithm.

    Args:
        review_phase: Current review phase (0, 1, 2, 3+)
        confidence: User's confidence rating (1-5)
        from_date: Base date for calculation (default: today)

    Returns:
        Next review date
    """
    if from_date is None:
        from_date = date.today()

    base_interval = get_base_interval(review_phase)
    multiplier = get_confidence_multiplier(confidence)

    interval = round(base_interval * multiplier)
    interval = max(1, min(interval, MAX_INTERVAL))  # Clamp to 1-365

    return from_date + timedelta(days=interval)
```

- [ ] **Step 3.4: Run tests to verify they pass**

Run: `cd /Users/aera/Desktop/Base_/.scripts/review-control-tower/backend && python -m pytest tests/test_spaced_repetition.py -v`
Expected: All 10 tests PASS

- [ ] **Step 3.5: Commit**

```bash
git add backend/services/spaced_repetition.py backend/tests/test_spaced_repetition.py
git commit -m "feat: add spaced repetition calculator with confidence multipliers"
```

---

## Task 4: Frontmatter Service

**Files:**
- Create: `backend/utils/hash.py`
- Create: `backend/models/review_note.py`
- Create: `backend/services/frontmatter_service.py`
- Create: `backend/tests/test_frontmatter_service.py`

### Steps

- [ ] **Step 4.1: Create hash utility**

```python
# backend/utils/hash.py
import hashlib
from pathlib import Path

def compute_content_hash(file_path: Path) -> str:
    """Compute MD5 hash of file content."""
    content = file_path.read_bytes()
    return hashlib.md5(content).hexdigest()
```

- [ ] **Step 4.2: Create Pydantic models**

```python
# backend/models/review_note.py
from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import date

class ReviewNote(BaseModel):
    path: str
    title: str
    type: Literal["yt-note", "book-note", "concept"]
    review: List[Optional[str]]
    review_phase: int
    next_review: Optional[str]
    confidence: Optional[int]
    difficulty: int = 3
    content_hash: str
    uri: str
    overdue_days: int = 0

class ReviewCompleteRequest(BaseModel):
    confidence: int
    content_hash: str

class ReviewCompleteResponse(BaseModel):
    success: bool
    updated_fields: dict
    next_review_date: str
```

- [ ] **Step 4.3: Write failing test for frontmatter service**

```python
# backend/tests/test_frontmatter_service.py
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from services.frontmatter_service import FrontmatterService
from models.review_note import ReviewNote

class TestFrontmatterService:
    @pytest.fixture
    def service(self):
        return FrontmatterService(vault_path=Path("/tmp/test_vault"))

    def test_parse_frontmatter_extracts_fields(self, service):
        content = """---
type: yt-note
review:
  - null
  - null
  - null
confidence: null
---
# Test Note
"""
        result = service.parse_frontmatter(content)
        assert result["type"] == "yt-note"
        assert result["review"] == [None, None, None]

    def test_build_obsidian_uri(self, service):
        uri = service.build_obsidian_uri("0. Ai agent/Yt-to-Note/test.md")
        assert uri.startswith("obsidian://open?vault=Base_&file=")
        assert "test" in uri
```

- [ ] **Step 4.4: Run tests to verify they fail**

Run: `cd /Users/aera/Desktop/Base_/.scripts/review-control-tower/backend && python -m pytest tests/test_frontmatter_service.py -v`
Expected: FAIL

- [ ] **Step 4.5: Implement frontmatter service**

```python
# backend/services/frontmatter_service.py
import frontmatter
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import date
from urllib.parse import quote

from config import VAULT_PATH, ALLOWED_UPDATE_FIELDS
from utils.normalizer import normalize_review_array
from utils.hash import compute_content_hash
from models.review_note import ReviewNote

class FrontmatterService:
    def __init__(self, vault_path: Path = VAULT_PATH):
        self.vault_path = vault_path
        self.vault_name = "Base_"

    def parse_frontmatter(self, content: str) -> Dict[str, Any]:
        """Parse frontmatter from markdown content."""
        post = frontmatter.loads(content)
        return dict(post.metadata)

    def read_note(self, relative_path: str) -> Optional[Dict[str, Any]]:
        """Read a note and return its frontmatter and metadata."""
        file_path = self.vault_path / relative_path
        if not file_path.exists():
            return None

        post = frontmatter.load(file_path)
        content_hash = compute_content_hash(file_path)

        metadata = dict(post.metadata)
        metadata["_content_hash"] = content_hash
        metadata["_path"] = relative_path

        return metadata

    def build_review_note(self, relative_path: str, metadata: Dict[str, Any]) -> ReviewNote:
        """Build ReviewNote from metadata."""
        review = normalize_review_array(metadata.get("review"))
        review_phase = metadata.get("review_phase", self._infer_review_phase(review))
        next_review = metadata.get("next_review")

        # Calculate overdue days
        overdue_days = 0
        if next_review:
            try:
                next_date = date.fromisoformat(next_review)
                overdue_days = (date.today() - next_date).days
            except ValueError:
                pass

        return ReviewNote(
            path=relative_path,
            title=metadata.get("title", Path(relative_path).stem),
            type=metadata.get("type", "concept"),
            review=review,
            review_phase=review_phase,
            next_review=next_review,
            confidence=metadata.get("confidence"),
            difficulty=metadata.get("difficulty", 3),
            content_hash=metadata.get("_content_hash", ""),
            uri=self.build_obsidian_uri(relative_path),
            overdue_days=max(0, overdue_days),
        )

    def _infer_review_phase(self, review: List[Optional[str]]) -> int:
        """Infer review phase from review array."""
        for i, val in enumerate(review):
            if val is None:
                return i
        return len(review)  # All slots filled

    def build_obsidian_uri(self, relative_path: str) -> str:
        """Build Obsidian URI for a note."""
        # Remove .md extension
        file_path = relative_path.rsplit('.md', 1)[0]
        encoded_path = quote(file_path, safe='')
        return f"obsidian://open?vault={self.vault_name}&file={encoded_path}"

    def update_note(
        self,
        relative_path: str,
        updates: Dict[str, Any],
        expected_hash: str
    ) -> Dict[str, Any]:
        """
        Update frontmatter fields with optimistic locking.

        Raises:
            FileNotFoundError: If note doesn't exist
            ValueError: If content hash doesn't match (concurrent modification)
        """
        file_path = self.vault_path / relative_path
        if not file_path.exists():
            raise FileNotFoundError(f"Note not found: {relative_path}")

        # Check content hash for optimistic locking
        current_hash = compute_content_hash(file_path)
        if current_hash != expected_hash:
            raise ValueError("Content modified externally. Please refresh.")

        # Load and update
        post = frontmatter.load(file_path)

        updated_fields = {}
        for key, value in updates.items():
            if key in ALLOWED_UPDATE_FIELDS:
                post.metadata[key] = value
                updated_fields[key] = value

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))

        return updated_fields
```

- [ ] **Step 4.6: Run tests to verify they pass**

Run: `cd /Users/aera/Desktop/Base_/.scripts/review-control-tower/backend && python -m pytest tests/test_frontmatter_service.py -v`
Expected: All tests PASS

- [ ] **Step 4.7: Commit**

```bash
git add backend/utils/hash.py backend/models/review_note.py backend/services/frontmatter_service.py backend/tests/test_frontmatter_service.py
git commit -m "feat: add frontmatter service with optimistic locking"
```

---

## Task 5: Vault Scanner Service

**Files:**
- Create: `backend/services/vault_scanner.py`
- Create: `backend/tests/test_vault_scanner.py`

### Steps

- [ ] **Step 5.1: Write failing test**

```python
# backend/tests/test_vault_scanner.py
import pytest
from pathlib import Path
from services.vault_scanner import VaultScanner

class TestVaultScanner:
    def test_scan_returns_review_notes_only(self):
        # This test requires actual vault access
        scanner = VaultScanner()
        notes = scanner.scan_for_review_notes()

        # All notes should have valid types
        for note in notes:
            assert note.type in ["yt-note", "book-note", "concept"]

        # Should return ReviewNote objects
        assert all(hasattr(n, 'path') for n in notes)
        assert all(hasattr(n, 'review') for n in notes)
```

- [ ] **Step 5.2: Implement vault scanner**

```python
# backend/services/vault_scanner.py
from pathlib import Path
from typing import List
from datetime import date

from config import VAULT_PATH, REVIEW_DIRS, REVIEW_TYPES
from services.frontmatter_service import FrontmatterService
from models.review_note import ReviewNote

class VaultScanner:
    def __init__(self, vault_path: Path = VAULT_PATH):
        self.vault_path = vault_path
        self.frontmatter_service = FrontmatterService(vault_path)

    def scan_for_review_notes(self) -> List[ReviewNote]:
        """Scan vault for notes that need review."""
        review_notes = []

        for dir_name in REVIEW_DIRS:
            dir_path = self.vault_path / dir_name
            if not dir_path.exists():
                continue

            for md_file in dir_path.glob("**/*.md"):
                relative_path = str(md_file.relative_to(self.vault_path))
                note = self._process_note(relative_path)
                if note:
                    review_notes.append(note)

        return review_notes

    def _process_note(self, relative_path: str) -> ReviewNote | None:
        """Process a single note and return ReviewNote if eligible."""
        metadata = self.frontmatter_service.read_note(relative_path)
        if not metadata:
            return None

        note_type = metadata.get("type")
        if note_type not in REVIEW_TYPES:
            return None

        # Check if note has review field (concept might not have it)
        if note_type == "concept" and "review" not in metadata:
            return None

        return self.frontmatter_service.build_review_note(relative_path, metadata)

    def get_due_notes(self) -> List[ReviewNote]:
        """Get notes that are due for review today."""
        all_notes = self.scan_for_review_notes()
        due_notes = []

        today = date.today()

        for note in all_notes:
            if self._is_due(note, today):
                due_notes.append(note)

        # Sort by overdue days (descending) - most overdue first
        due_notes.sort(key=lambda n: n.overdue_days, reverse=True)

        return due_notes

    def _is_due(self, note: ReviewNote, today: date) -> bool:
        """Check if a note is due for review."""
        # If next_review is set and it's today or earlier
        if note.next_review:
            try:
                next_date = date.fromisoformat(note.next_review)
                return next_date <= today
            except ValueError:
                pass

        # If review array has null slots (never reviewed or partial)
        for i, val in enumerate(note.review):
            if val is None and i == note.review_phase:
                return True

        return False
```

- [ ] **Step 5.3: Run tests**

Run: `cd /Users/aera/Desktop/Base_/.scripts/review-control-tower/backend && python -m pytest tests/test_vault_scanner.py -v`
Expected: PASS

- [ ] **Step 5.4: Commit**

```bash
git add backend/services/vault_scanner.py backend/tests/test_vault_scanner.py
git commit -m "feat: add vault scanner for review note discovery"
```

---

## Task 6: AnkiConnect Service

**Files:**
- Create: `backend/services/anki_connect.py`
- Create: `backend/tests/test_anki_connect.py`

### Steps

- [ ] **Step 6.1: Write test with mock**

```python
# backend/tests/test_anki_connect.py
import pytest
from unittest.mock import patch, MagicMock
from services.anki_connect import AnkiConnectService

class TestAnkiConnectService:
    @pytest.fixture
    def service(self):
        return AnkiConnectService()

    @patch('services.anki_connect.httpx.post')
    def test_get_due_count_success(self, mock_post, service):
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": ["1", "2", "3"], "error": None}
        mock_post.return_value = mock_response

        result = service.get_due_count()
        assert result == {"due_count": 3, "status": "online"}

    @patch('services.anki_connect.httpx.post')
    def test_get_due_count_offline(self, mock_post, service):
        mock_post.side_effect = Exception("Connection refused")

        result = service.get_due_count()
        assert result == {"due_count": 0, "status": "offline"}
```

- [ ] **Step 6.2: Implement AnkiConnect service**

```python
# backend/services/anki_connect.py
import httpx
from typing import Dict, Any

from config import ANKI_CONNECT_URL, ANKI_TIMEOUT

class AnkiConnectService:
    def __init__(self, url: str = ANKI_CONNECT_URL, timeout: float = ANKI_TIMEOUT):
        self.url = url
        self.timeout = timeout

    def _invoke(self, action: str, params: Dict[str, Any] = None) -> Any:
        """Invoke AnkiConnect action."""
        payload = {
            "action": action,
            "version": 6,
        }
        if params:
            payload["params"] = params

        response = httpx.post(self.url, json=payload, timeout=self.timeout)
        result = response.json()

        if result.get("error"):
            raise Exception(result["error"])

        return result.get("result")

    def get_due_count(self) -> Dict[str, Any]:
        """Get count of due cards from Anki."""
        try:
            cards = self._invoke("findCards", {"query": "is:due"})
            return {
                "due_count": len(cards) if cards else 0,
                "status": "online"
            }
        except Exception:
            return {
                "due_count": 0,
                "status": "offline"
            }

    def is_available(self) -> bool:
        """Check if AnkiConnect is available."""
        try:
            self._invoke("version")
            return True
        except Exception:
            return False
```

- [ ] **Step 6.3: Run tests**

Run: `cd /Users/aera/Desktop/Base_/.scripts/review-control-tower/backend && python -m pytest tests/test_anki_connect.py -v`
Expected: PASS

- [ ] **Step 6.4: Commit**

```bash
git add backend/services/anki_connect.py backend/tests/test_anki_connect.py
git commit -m "feat: add AnkiConnect service with graceful degradation"
```

---

## Task 7: API Routers

**Files:**
- Create: `backend/routers/reviews.py`
- Create: `backend/routers/anki.py`
- Create: `backend/routers/health.py`
- Modify: `backend/main.py`

### Steps

- [ ] **Step 7.1: Create reviews router**

```python
# backend/routers/reviews.py
from fastapi import APIRouter, HTTPException
from typing import List
from datetime import date

from services.vault_scanner import VaultScanner
from services.frontmatter_service import FrontmatterService
from services.spaced_repetition import calculate_next_review
from models.review_note import ReviewNote, ReviewCompleteRequest, ReviewCompleteResponse
from utils.normalizer import normalize_review_array

router = APIRouter(prefix="/api/reviews", tags=["reviews"])

scanner = VaultScanner()
frontmatter_service = FrontmatterService()


@router.get("/due", response_model=dict)
async def get_due_reviews():
    """Get all notes due for review today."""
    notes = scanner.get_due_notes()

    return {
        "notes": [note.model_dump() for note in notes],
        "total_count": len(notes),
        "overdue_count": sum(1 for n in notes if n.overdue_days > 0)
    }


@router.post("/{path:path}/complete", response_model=ReviewCompleteResponse)
async def complete_review(path: str, request: ReviewCompleteRequest):
    """Mark a note as reviewed and update frontmatter."""
    # Validate confidence
    if request.confidence < 1 or request.confidence > 5:
        raise HTTPException(status_code=422, detail="Confidence must be between 1 and 5")

    # Read current note
    metadata = frontmatter_service.read_note(path)
    if not metadata:
        raise HTTPException(status_code=404, detail=f"Note not found: {path}")

    # Get current state
    review = normalize_review_array(metadata.get("review"))
    review_phase = metadata.get("review_phase", 0)

    # Update review array
    if review_phase < len(review):
        review[review_phase] = date.today().isoformat()

    # Calculate next review date
    next_review_date = calculate_next_review(
        review_phase=review_phase,
        confidence=request.confidence
    )

    # Prepare updates
    updates = {
        "review": review,
        "confidence": request.confidence,
        "review_phase": review_phase + 1,
        "next_review": next_review_date.isoformat(),
    }

    try:
        updated_fields = frontmatter_service.update_note(
            path,
            updates,
            request.content_hash
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return ReviewCompleteResponse(
        success=True,
        updated_fields=updated_fields,
        next_review_date=next_review_date.isoformat()
    )
```

- [ ] **Step 7.2: Create anki router**

```python
# backend/routers/anki.py
from fastapi import APIRouter
from services.anki_connect import AnkiConnectService

router = APIRouter(prefix="/api/anki", tags=["anki"])

anki_service = AnkiConnectService()


@router.get("/due")
async def get_anki_due():
    """Get Anki due card count."""
    return anki_service.get_due_count()
```

- [ ] **Step 7.3: Create health router**

```python
# backend/routers/health.py
from fastapi import APIRouter
from datetime import datetime
from pathlib import Path

from config import VAULT_PATH
from services.anki_connect import AnkiConnectService

router = APIRouter(prefix="/api", tags=["health"])

anki_service = AnkiConnectService()


@router.get("/health")
async def health_check():
    """Check service health status."""
    vault_accessible = Path(VAULT_PATH).exists()
    anki_available = anki_service.is_available()

    return {
        "status": "healthy" if vault_accessible else "degraded",
        "vault_path": str(VAULT_PATH),
        "vault_accessible": vault_accessible,
        "anki_status": "online" if anki_available else "offline",
        "timestamp": datetime.now().isoformat()
    }
```

- [ ] **Step 7.4: Update main.py to include routers**

```python
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import reviews, anki, health

app = FastAPI(title="Review Control Tower API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(reviews.router)
app.include_router(anki.router)
app.include_router(health.router)
```

- [ ] **Step 7.5: Test API endpoints manually**

Run: `cd /Users/aera/Desktop/Base_/.scripts/review-control-tower/backend && uvicorn main:app --reload --port 8000`

Test endpoints:
```bash
curl http://localhost:8000/api/health
curl http://localhost:8000/api/reviews/due
curl http://localhost:8000/api/anki/due
```

Expected: JSON responses

- [ ] **Step 7.6: Commit**

```bash
git add backend/routers/ backend/main.py
git commit -m "feat: add API routers for reviews, anki, and health"
```

---

## Task 8: Frontend API Client

**Files:**
- Create: `frontend/lib/types.ts`
- Create: `frontend/lib/api.ts`

### Steps

- [ ] **Step 8.1: Create TypeScript types**

```typescript
// frontend/lib/types.ts
export interface ReviewNote {
  path: string;
  title: string;
  type: "yt-note" | "book-note" | "concept";
  review: (string | null)[];
  review_phase: number;
  next_review: string | null;
  confidence: number | null;
  difficulty: number;
  content_hash: string;
  uri: string;
  overdue_days: number;
}

export interface DueReviewsResponse {
  notes: ReviewNote[];
  total_count: number;
  overdue_count: number;
}

export interface AnkiStatusResponse {
  due_count: number;
  status: "online" | "offline";
}

export interface ReviewCompleteRequest {
  confidence: number;
  content_hash: string;
}

export interface ReviewCompleteResponse {
  success: boolean;
  updated_fields: Record<string, unknown>;
  next_review_date: string;
}

export interface HealthResponse {
  status: "healthy" | "degraded";
  vault_path: string;
  vault_accessible: boolean;
  anki_status: "online" | "offline";
  timestamp: string;
}
```

- [ ] **Step 8.2: Create API client**

```typescript
// frontend/lib/api.ts
import type {
  DueReviewsResponse,
  AnkiStatusResponse,
  ReviewCompleteRequest,
  ReviewCompleteResponse,
  HealthResponse,
} from "./types";

const API_BASE = "http://localhost:8000/api";

async function fetchApi<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

export const api = {
  getDueReviews: () => fetchApi<DueReviewsResponse>("/reviews/due"),

  completeReview: (path: string, data: ReviewCompleteRequest) =>
    fetchApi<ReviewCompleteResponse>(`/reviews/${encodeURIComponent(path)}/complete`, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  getAnkiStatus: () => fetchApi<AnkiStatusResponse>("/anki/due"),

  getHealth: () => fetchApi<HealthResponse>("/health"),
};
```

- [ ] **Step 8.3: Commit**

```bash
git add frontend/lib/
git commit -m "feat: add frontend API client and TypeScript types"
```

---

## Task 9: Frontend SWR Hooks

**Files:**
- Create: `frontend/hooks/use-reviews.ts`
- Create: `frontend/hooks/use-anki.ts`

### Steps

- [ ] **Step 9.1: Create reviews hook**

```typescript
// frontend/hooks/use-reviews.ts
import useSWR from "swr";
import { api } from "@/lib/api";
import type { DueReviewsResponse, ReviewCompleteRequest } from "@/lib/types";

export function useReviews() {
  const { data, error, isLoading, mutate } = useSWR<DueReviewsResponse>(
    "/reviews/due",
    () => api.getDueReviews(),
    {
      refreshInterval: 30000, // Refresh every 30 seconds
      revalidateOnFocus: true,
    }
  );

  const completeReview = async (path: string, request: ReviewCompleteRequest) => {
    try {
      const result = await api.completeReview(path, request);
      // Optimistically remove the note from the list
      await mutate(
        (current) => {
          if (!current) return current;
          return {
            ...current,
            notes: current.notes.filter((n) => n.path !== path),
            total_count: current.total_count - 1,
            overdue_count: Math.max(0, current.overdue_count - 1),
          };
        },
        { revalidate: false }
      );
      return result;
    } catch (error) {
      // Revalidate on error to get fresh data
      await mutate();
      throw error;
    }
  };

  return {
    notes: data?.notes ?? [],
    totalCount: data?.total_count ?? 0,
    overdueCount: data?.overdue_count ?? 0,
    isLoading,
    isError: !!error,
    error,
    refresh: () => mutate(),
    completeReview,
  };
}
```

- [ ] **Step 9.2: Create anki hook**

```typescript
// frontend/hooks/use-anki.ts
import useSWR from "swr";
import { api } from "@/lib/api";
import type { AnkiStatusResponse } from "@/lib/types";

export function useAnki() {
  const { data, error, isLoading } = useSWR<AnkiStatusResponse>(
    "/anki/due",
    () => api.getAnkiStatus(),
    {
      refreshInterval: 60000, // Refresh every minute
      revalidateOnFocus: true,
    }
  );

  return {
    dueCount: data?.due_count ?? 0,
    status: data?.status ?? "offline",
    isLoading,
    isError: !!error,
    isOffline: data?.status === "offline",
  };
}
```

- [ ] **Step 9.3: Commit**

```bash
git add frontend/hooks/
git commit -m "feat: add SWR hooks for reviews and anki data"
```

---

## Task 10: Frontend UI Components

**Files:**
- Create: `frontend/components/stats-card.tsx`
- Create: `frontend/components/review-card.tsx`
- Create: `frontend/components/review-list.tsx`
- Create: `frontend/components/confidence-modal.tsx`

### Steps

- [ ] **Step 10.1: Create stats card component**

```typescript
// frontend/components/stats-card.tsx
import { Card, CardContent } from "@/components/ui/card";

interface StatsCardProps {
  icon: string;
  label: string;
  value: number | string;
  variant?: "default" | "success" | "warning" | "danger";
}

const variantStyles = {
  default: "bg-white border-gray-200",
  success: "bg-green-50 border-green-200",
  warning: "bg-orange-50 border-orange-200",
  danger: "bg-red-50 border-red-200",
};

export function StatsCard({
  icon,
  label,
  value,
  variant = "default",
}: StatsCardProps) {
  return (
    <Card className={`${variantStyles[variant]} border`}>
      <CardContent className="p-4">
        <div className="flex items-center gap-3">
          <span className="text-2xl">{icon}</span>
          <div>
            <p className="text-sm text-gray-500">{label}</p>
            <p className="text-2xl font-bold">{value}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
```

- [ ] **Step 10.2: Create review card component**

```typescript
// frontend/components/review-card.tsx
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import type { ReviewNote } from "@/lib/types";

interface ReviewCardProps {
  note: ReviewNote;
  onComplete: () => void;
  isLoading?: boolean;
}

const typeIcons = {
  "yt-note": "📺",
  "book-note": "📚",
  concept: "💡",
};

export function ReviewCard({ note, onComplete, isLoading }: ReviewCardProps) {
  const overdueBadgeVariant =
    note.overdue_days > 7
      ? "destructive"
      : note.overdue_days > 0
      ? "secondary"
      : "outline";

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardContent className="p-4">
        <div className="flex items-start justify-between gap-2">
          <div className="flex items-center gap-2">
            <span className="text-xl">{typeIcons[note.type]}</span>
            <h3 className="font-medium line-clamp-2">{note.title}</h3>
          </div>
          {note.overdue_days > 0 && (
            <Badge variant={overdueBadgeVariant}>
              ⏰ {note.overdue_days}d
            </Badge>
          )}
        </div>
        <div className="mt-2 text-sm text-gray-500">
          Phase {note.review_phase + 1} · Confidence{" "}
          {note.confidence ?? "N/A"}
        </div>
      </CardContent>
      <CardFooter className="p-4 pt-0 gap-2">
        <Button onClick={onComplete} disabled={isLoading} className="flex-1">
          {isLoading ? "처리 중..." : "복습 완료"}
        </Button>
        <Button variant="outline" asChild>
          <a href={note.uri} target="_blank" rel="noopener noreferrer">
            Open
          </a>
        </Button>
      </CardFooter>
    </Card>
  );
}
```

- [ ] **Step 10.3: Create confidence modal component**

```typescript
// frontend/components/confidence-modal.tsx
"use client";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

interface ConfidenceModalProps {
  open: boolean;
  onClose: () => void;
  onSelect: (confidence: number) => void;
  isLoading?: boolean;
}

const confidenceLevels = [
  { value: 1, label: "1", description: "전혀 기억 안남" },
  { value: 2, label: "2", description: "거의 기억 안남" },
  { value: 3, label: "3", description: "보통" },
  { value: 4, label: "4", description: "잘 기억남" },
  { value: 5, label: "5", description: "완벽히 기억" },
];

export function ConfidenceModal({
  open,
  onClose,
  onSelect,
  isLoading,
}: ConfidenceModalProps) {
  return (
    <Dialog open={open} onOpenChange={(o) => !o && onClose()}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>복습 난이도는 어땠나요?</DialogTitle>
        </DialogHeader>
        <div className="grid grid-cols-5 gap-2 py-4">
          {confidenceLevels.map((level) => (
            <Button
              key={level.value}
              variant="outline"
              className="flex flex-col h-auto py-3"
              onClick={() => onSelect(level.value)}
              disabled={isLoading}
            >
              <span className="text-lg font-bold">{level.label}</span>
              <span className="text-xs text-gray-500 mt-1">
                {level.description}
              </span>
            </Button>
          ))}
        </div>
      </DialogContent>
    </Dialog>
  );
}
```

- [ ] **Step 10.4: Create review list component**

```typescript
// frontend/components/review-list.tsx
"use client";

import { useState } from "react";
import { ReviewCard } from "./review-card";
import { ConfidenceModal } from "./confidence-modal";
import { useReviews } from "@/hooks/use-reviews";
import type { ReviewNote } from "@/lib/types";

export function ReviewList() {
  const { notes, isLoading, isError, completeReview } = useReviews();
  const [selectedNote, setSelectedNote] = useState<ReviewNote | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleComplete = (note: ReviewNote) => {
    setSelectedNote(note);
  };

  const handleConfidenceSelect = async (confidence: number) => {
    if (!selectedNote) return;

    setIsSubmitting(true);
    try {
      await completeReview(selectedNote.path, {
        confidence,
        content_hash: selectedNote.content_hash,
      });
      setSelectedNote(null);
    } catch (error) {
      console.error("Failed to complete review:", error);
      alert(error instanceof Error ? error.message : "복습 완료 실패");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[...Array(3)].map((_, i) => (
          <div
            key={i}
            className="h-32 bg-gray-100 animate-pulse rounded-lg"
          />
        ))}
      </div>
    );
  }

  if (isError) {
    return (
      <div className="text-center py-8 text-red-500">
        데이터를 불러오는 데 실패했습니다.
      </div>
    );
  }

  if (notes.length === 0) {
    return (
      <div className="text-center py-12">
        <span className="text-4xl">🎉</span>
        <p className="mt-4 text-gray-500">오늘 복습할 노트가 없습니다!</p>
      </div>
    );
  }

  return (
    <>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {notes.map((note) => (
          <ReviewCard
            key={note.path}
            note={note}
            onComplete={() => handleComplete(note)}
            isLoading={isSubmitting && selectedNote?.path === note.path}
          />
        ))}
      </div>

      <ConfidenceModal
        open={!!selectedNote}
        onClose={() => setSelectedNote(null)}
        onSelect={handleConfidenceSelect}
        isLoading={isSubmitting}
      />
    </>
  );
}
```

- [ ] **Step 10.5: Commit**

```bash
git add frontend/components/
git commit -m "feat: add UI components for dashboard"
```

---

## Task 11: Frontend Dashboard Page

**Files:**
- Modify: `frontend/app/page.tsx`
- Modify: `frontend/app/layout.tsx`

### Steps

- [ ] **Step 11.1: Update layout**

```typescript
// frontend/app/layout.tsx
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "복습 관제탑",
  description: "Obsidian 학습 노트 복습 스케줄 관리",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
```

- [ ] **Step 11.2: Create dashboard page**

```typescript
// frontend/app/page.tsx
"use client";

import { StatsCard } from "@/components/stats-card";
import { ReviewList } from "@/components/review-list";
import { useReviews } from "@/hooks/use-reviews";
import { useAnki } from "@/hooks/use-anki";

export default function DashboardPage() {
  const { totalCount, overdueCount, notes } = useReviews();
  const { dueCount, isOffline } = useAnki();

  const completedToday = totalCount > 0 ? notes.filter(
    (n) => n.overdue_days === 0 && n.review_phase > 0
  ).length : 0;

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            📊 복습 관제탑
          </h1>
          <p className="text-gray-500 mt-1">
            오늘의 복습 현황을 확인하세요
          </p>
        </header>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <StatsCard
            icon="🎯"
            label="오늘 복습"
            value={totalCount}
          />
          <StatsCard
            icon="✅"
            label="완료"
            value={completedToday}
            variant="success"
          />
          <StatsCard
            icon="⏰"
            label="밀림"
            value={overdueCount}
            variant={overdueCount > 0 ? "danger" : "default"}
          />
          <StatsCard
            icon="📇"
            label={isOffline ? "Anki (Offline)" : "Anki Due"}
            value={isOffline ? "-" : dueCount}
            variant={isOffline ? "warning" : "default"}
          />
        </div>

        {/* Review List */}
        <section>
          <h2 className="text-xl font-semibold mb-4">
            📝 오늘의 복습 ({totalCount})
          </h2>
          <ReviewList />
        </section>
      </div>
    </main>
  );
}
```

- [ ] **Step 11.3: Verify frontend runs**

Run: `cd /Users/aera/Desktop/Base_/.scripts/review-control-tower/frontend && npm run dev`
Expected: Dashboard loads at http://localhost:3000

- [ ] **Step 11.4: Commit**

```bash
git add frontend/app/
git commit -m "feat: add dashboard page with stats and review list"
```

---

## Task 12: Integration Testing

**Files:**
- Create: `backend/tests/test_api.py`

### Steps

- [ ] **Step 12.1: Write API integration tests**

```python
# backend/tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestHealthEndpoint:
    def test_health_returns_status(self):
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "vault_accessible" in data

class TestReviewsEndpoint:
    def test_get_due_reviews_returns_list(self):
        response = client.get("/api/reviews/due")
        assert response.status_code == 200
        data = response.json()
        assert "notes" in data
        assert "total_count" in data
        assert isinstance(data["notes"], list)

class TestAnkiEndpoint:
    def test_get_anki_due_returns_status(self):
        response = client.get("/api/anki/due")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] in ["online", "offline"]
```

- [ ] **Step 12.2: Run all tests**

Run: `cd /Users/aera/Desktop/Base_/.scripts/review-control-tower/backend && python -m pytest tests/ -v`
Expected: All tests PASS

- [ ] **Step 12.3: End-to-end manual test**

1. Start backend: `uvicorn main:app --reload --port 8000`
2. Start frontend: `npm run dev`
3. Open http://localhost:3000
4. Verify:
   - [ ] Stats cards show data
   - [ ] Review notes are listed
   - [ ] "복습 완료" button opens modal
   - [ ] Selecting confidence updates the note
   - [ ] Note disappears from list after completion
   - [ ] Anki status shows online/offline

- [ ] **Step 12.4: Final commit**

```bash
git add .
git commit -m "feat: complete Review Control Tower MVP

- Backend: FastAPI with vault scanner, frontmatter service, spaced repetition
- Frontend: Next.js dashboard with SWR, shadcn/ui components
- Features: Due reviews, completion tracking, Anki integration
- Safety: Optimistic locking, review array normalization"
```

---

## Task 13: Startup Scripts

**Files:**
- Create: `start.sh`
- Create: `README.md`

### Steps

- [ ] **Step 13.1: Create startup script**

```bash
#!/bin/bash
# start.sh - Start Review Control Tower

PROJECT_DIR="/Users/aera/Desktop/Base_/.scripts/review-control-tower"

# Start backend
echo "Starting backend..."
cd "$PROJECT_DIR/backend"
source venv/bin/activate 2>/dev/null || python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt -q
uvicorn main:app --port 8000 &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend..."
cd "$PROJECT_DIR/frontend"
npm install -q
npm run dev &
FRONTEND_PID=$!

echo "✅ Review Control Tower started!"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop"

# Cleanup on exit
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
```

- [ ] **Step 13.2: Create README**

```markdown
# 복습 관제탑 (Review Control Tower)

Obsidian 학습 노트의 복습 스케줄을 자동 관리하는 로컬 웹 대시보드.

## Quick Start

```bash
cd /Users/aera/Desktop/Base_/.scripts/review-control-tower
chmod +x start.sh
./start.sh
```

Open http://localhost:3000

## Requirements

- Python 3.10+
- Node.js 18+
- Anki Desktop (optional, for Anki integration)

## Features

- 📋 오늘 복습할 노트 자동 식별
- ✅ 원클릭 복습 완료 기록
- 📊 복습 현황 대시보드
- 📇 Anki Due 카드 통합

## Tech Stack

- Backend: FastAPI + python-frontmatter
- Frontend: Next.js 14 + SWR + shadcn/ui
```

- [ ] **Step 13.3: Final commit**

```bash
chmod +x start.sh
git add start.sh README.md
git commit -m "docs: add startup script and README"
```

---

## Summary

| Task | Description | Estimated Time |
|------|-------------|----------------|
| 1 | Project Setup | 15 min |
| 2 | Review Array Normalizer | 10 min |
| 3 | Spaced Repetition Calculator | 10 min |
| 4 | Frontmatter Service | 15 min |
| 5 | Vault Scanner Service | 10 min |
| 6 | AnkiConnect Service | 10 min |
| 7 | API Routers | 15 min |
| 8 | Frontend API Client | 10 min |
| 9 | Frontend SWR Hooks | 10 min |
| 10 | Frontend UI Components | 20 min |
| 11 | Frontend Dashboard Page | 15 min |
| 12 | Integration Testing | 15 min |
| 13 | Startup Scripts | 5 min |

**Total: ~2.5 hours**
