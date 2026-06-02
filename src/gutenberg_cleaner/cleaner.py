"""High-level public API for deterministic manuscript cleanup."""

from __future__ import annotations

import re
from dataclasses import dataclass

from gutenberg_cleaner.boilerplate import detect_metadata, strip_project_gutenberg_boilerplate
from gutenberg_cleaner.headings import normalize_headings
from gutenberg_cleaner.reports import CleanupReport
from gutenberg_cleaner.scene_breaks import normalize_scene_breaks
from gutenberg_cleaner.toc import remove_toc_artifacts


@dataclass
class CleanupResult:
    """Cleaned manuscript plus a machine-readable cleanup report."""

    markdown: str
    report: CleanupReport


def clean_text(
    raw_text: str,
    *,
    title: str | None = None,
    author: str | None = None,
) -> CleanupResult:
    """Clean a Project Gutenberg/public-domain text into tidy Markdown.

    The function is deterministic and local-only: it does not call an API, send
    data over the network, or require hosted services.
    """
    normalized = _normalize_newlines(raw_text)
    detected_title, detected_author = detect_metadata(normalized)
    report = CleanupReport(
        title=title or detected_title,
        author=author or detected_author,
        word_count_before=count_words(normalized),
    )

    cleaned, report.boilerplate_removed = strip_project_gutenberg_boilerplate(normalized)
    cleaned, report.toc_removed = remove_toc_artifacts(cleaned)
    cleaned, report.scene_breaks_normalized = normalize_scene_breaks(cleaned)
    cleaned, report.headings_normalized, report.heading_levels = normalize_headings(cleaned)
    cleaned = _clean_ocr_artifacts(cleaned)
    cleaned = _normalize_paragraph_spacing(cleaned)

    if report.title and not cleaned.lstrip().startswith("# "):
        byline = f"\n\n_by {report.author}_" if report.author else ""
        cleaned = f"# {report.title}{byline}\n\n{cleaned}".strip()
        report.heading_levels = {
            **report.heading_levels,
            "h1": report.heading_levels.get("h1", 0) + 1,
        }

    report.word_count_after = count_words(cleaned)
    _add_warnings(report, cleaned)
    return CleanupResult(markdown=cleaned, report=report)


def count_words(text: str) -> int:
    """Count prose-like words while ignoring Markdown punctuation."""
    return len(re.findall(r"\b[\w’'-]+\b", text, flags=re.UNICODE))


def _normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _clean_ocr_artifacts(text: str) -> str:
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    text = re.sub(r"(?<=\w)-\n(?=\w)", "", text)
    text = re.sub(r"\n{2,}\s*Page \d+\s*\n{2,}", "\n\n", text, flags=re.IGNORECASE)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text


def _normalize_paragraph_spacing(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines).strip() + "\n"


def _add_warnings(report: CleanupReport, markdown: str) -> None:
    if not report.boilerplate_removed and "Project Gutenberg" in markdown:
        report.warnings.append(
            "Project Gutenberg is mentioned, but no explicit START/END marker was stripped."
        )
    if not report.heading_levels:
        report.warnings.append("No Markdown headings were detected after cleanup.")
    if report.word_count_after == 0:
        report.warnings.append("Cleaned manuscript is empty.")
