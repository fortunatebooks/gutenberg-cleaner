"""Heading detection and normalization."""

from __future__ import annotations

import re
from collections import Counter

CHAPTER_WORDS = (
    "chapter",
    "prologue",
    "epilogue",
    "part",
    "book",
    "section",
    "volume",
    "introduction",
    "preface",
)
ROMAN = r"[IVXLCDM]+"
NUMBER_WORD = r"[A-Z][A-Z\- ]{0,30}"
CHAPTER_RE = re.compile(
    rf"^(?P<label>{'|'.join(CHAPTER_WORDS)})(?:\s+(?:\d+|{ROMAN}|{NUMBER_WORD}))?(?:[.:\-–—].*)?$",
    re.IGNORECASE,
)
NUMERIC_RE = re.compile(r"^(?:\d{1,3}|[ivxlcdm]{1,8})$", re.IGNORECASE)


def normalize_headings(text: str) -> tuple[str, int, dict[str, int]]:
    """Promote obvious standalone chapter labels to Markdown headings."""
    lines = text.splitlines()
    changed = 0

    for index, line in enumerate(lines):
        stripped = _strip_inline_emphasis(line.strip())
        if not stripped or line.lstrip().startswith("#"):
            continue
        if _looks_like_heading(stripped, lines, index):
            lines[index] = f"# {stripped}"
            changed += 1

    normalized = _fix_markdown_heading_spacing("\n".join(lines))
    return normalized, changed, count_heading_levels(normalized)


def count_heading_levels(text: str) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+\S", line.strip())
        if match:
            counts[f"h{len(match.group(1))}"] += 1
    return dict(sorted(counts.items()))


def _looks_like_heading(stripped: str, lines: list[str], index: int) -> bool:
    if len(stripped) > 90:
        return False
    if CHAPTER_RE.match(stripped):
        return True
    if NUMERIC_RE.match(stripped) and _has_prose_after(lines, index + 1):
        return True
    if stripped.isupper() and 3 <= len(stripped) <= 70 and _has_blank_context(lines, index):
        lowered = stripped.lower()
        return not any(word in lowered for word in ("project gutenberg", "license", "copyright"))
    return False


def _has_blank_context(lines: list[str], index: int) -> bool:
    previous_blank = index == 0 or not lines[index - 1].strip()
    next_blank = index + 1 >= len(lines) or not lines[index + 1].strip()
    return previous_blank and next_blank


def _has_prose_after(lines: list[str], start: int) -> bool:
    words = 0
    for line in lines[start : start + 12]:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#") or NUMERIC_RE.match(stripped):
            break
        words += len(stripped.split())
        if words >= 25:
            return True
    return False


def _strip_inline_emphasis(text: str) -> str:
    return re.sub(r"^(?:\*\*|__|\*|_)(.*?)(?:\*\*|__|\*|_)$", r"\1", text).strip()


def _fix_markdown_heading_spacing(text: str) -> str:
    return re.sub(r"^(#{1,6})([^#\s].*)$", r"\1 \2", text, flags=re.MULTILINE)
