"""Table-of-contents artifact removal."""

from __future__ import annotations

import re

TOC_HEADING_RE = re.compile(r"^\s*#{0,6}\s*(contents|table of contents)\s*$", re.IGNORECASE)
TOC_LINK_RE = re.compile(r"\[[^\]]+\]\((?:#|[^)]*\.x?html)[^)]*\)", re.IGNORECASE)
RAW_XHTML_RE = re.compile(r"\b[^\s)]+\.x?html(?:#[\w.:-]+)?\b", re.IGNORECASE)
DOTTED_PAGE_RE = re.compile(r"^\s*\S.{2,}?\.{3,}\s*\d+\s*$")


def remove_toc_artifacts(text: str) -> tuple[str, bool]:
    """Remove obvious copied/generated TOC blocks and link artifacts."""
    lines = text.splitlines()
    output: list[str] = []
    in_toc_block = False
    toc_lines_seen = 0
    modified = False

    for line in lines:
        stripped = line.strip()
        if TOC_HEADING_RE.match(stripped):
            in_toc_block = True
            toc_lines_seen = 0
            modified = True
            continue

        if in_toc_block:
            if not stripped:
                toc_lines_seen += 1
                if toc_lines_seen <= 1:
                    continue
                in_toc_block = False
                output.append(line)
                continue
            if _looks_like_toc_entry(stripped):
                modified = True
                toc_lines_seen += 1
                continue
            in_toc_block = False

        if _looks_like_raw_toc_artifact(stripped):
            modified = True
            continue
        output.append(line)

    return "\n".join(output), modified


def _looks_like_toc_entry(line: str) -> bool:
    return bool(
        TOC_LINK_RE.search(line)
        or RAW_XHTML_RE.search(line)
        or DOTTED_PAGE_RE.match(line)
        or re.match(r"^(?:[-*]|\d+[.)])\s+(chapter|part|book|prologue|epilogue)\b", line, re.I)
    )


def _looks_like_raw_toc_artifact(line: str) -> bool:
    if not line:
        return False
    return bool(TOC_LINK_RE.search(line) or RAW_XHTML_RE.fullmatch(line))
