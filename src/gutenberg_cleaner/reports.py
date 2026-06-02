"""Report models for Gutenberg Cleaner."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class CleanupReport:
    """Machine-readable summary of one cleanup run."""

    title: str | None = None
    author: str | None = None
    boilerplate_removed: bool = False
    toc_removed: bool = False
    headings_normalized: int = 0
    scene_breaks_normalized: int = 0
    word_count_before: int = 0
    word_count_after: int = 0
    heading_levels: dict[str, int] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""
        return asdict(self)
