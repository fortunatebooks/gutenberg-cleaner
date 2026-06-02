"""Project Gutenberg boilerplate detection and removal."""

from __future__ import annotations

import re

START_RE = re.compile(r"\*{0,3}\s*start of (?:the|this) project gutenberg", re.IGNORECASE)
END_RE = re.compile(r"\*{0,3}\s*end of (?:the|this) project gutenberg", re.IGNORECASE)
TITLE_RE = re.compile(r"^\s*Title:\s*(?P<value>.+?)\s*$", re.IGNORECASE | re.MULTILINE)
AUTHOR_RE = re.compile(r"^\s*Author:\s*(?P<value>.+?)\s*$", re.IGNORECASE | re.MULTILINE)
EBOOK_TITLE_RE = re.compile(
    r"Project Gutenberg (?:eBook|EBook|e-text) of (?P<value>.+?)(?:, by|\n|$)", re.IGNORECASE
)


def detect_metadata(text: str) -> tuple[str | None, str | None]:
    """Best-effort title/author detection from public-domain source headers."""
    title_match = TITLE_RE.search(text) or EBOOK_TITLE_RE.search(text)
    author_match = AUTHOR_RE.search(text)
    title = _clean_metadata_value(title_match.group("value")) if title_match else None
    author = _clean_metadata_value(author_match.group("value")) if author_match else None
    return title, author


def strip_project_gutenberg_boilerplate(text: str) -> tuple[str, bool]:
    """Remove explicit Project Gutenberg header/footer blocks conservatively.

    The cleaner strips only when START/END markers are present. Plain mentions of
    Project Gutenberg in essays, notes, or bibliographies are preserved.
    """
    if not text:
        return text, False

    lines = text.splitlines()
    start_idx = None
    end_idx = None

    for index, line in enumerate(lines):
        if start_idx is None and START_RE.search(line):
            start_idx = index
            continue
        if end_idx is None and END_RE.search(line):
            end_idx = index

    if start_idx is not None and end_idx is not None and start_idx < end_idx:
        stripped = lines[start_idx + 1 : end_idx]
    elif start_idx is not None:
        stripped = lines[start_idx + 1 :]
    elif end_idx is not None:
        stripped = lines[:end_idx]
    else:
        return text, False

    while stripped and _is_rule_line(stripped[0]):
        stripped = stripped[1:]
    while stripped and _is_rule_line(stripped[-1]):
        stripped = stripped[:-1]

    return "\n".join(stripped).strip(), True


def _is_rule_line(line: str) -> bool:
    return bool(re.fullmatch(r"\s*[*_\-–—]{3,}\s*", line))


def _clean_metadata_value(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip(" .,*#")
