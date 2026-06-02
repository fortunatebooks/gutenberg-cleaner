"""Scene-break normalization helpers."""

from __future__ import annotations

import re

ORNAMENTAL_WORDS = re.compile(
    r"^(?:\[?\s*)?(?:ornament|decoration|divider|separator|scene\s*break|section\s*break)(?:\s*\]?)$",
    re.IGNORECASE,
)


def normalize_scene_breaks(text: str) -> tuple[str, int]:
    """Normalize common ornamental scene breaks to a single ``***`` marker."""
    changed = 0
    output = []
    previous_was_break = False

    for line in text.splitlines():
        if is_scene_break_line(line):
            if not previous_was_break:
                output.append("***")
                changed += 1
            previous_was_break = True
            continue

        output.append(line.rstrip())
        if line.strip():
            previous_was_break = False

    return "\n".join(output), changed


def is_scene_break_line(line: str) -> bool:
    """Return True for standalone textual scene-break ornaments."""
    stripped = line.strip()
    if not stripped:
        return False
    if stripped in {"***", "* * *", "---", "- - -", "___", "_ _ _"}:
        return True
    if re.fullmatch(r"(?:\*\s*){3,}", stripped):
        return True
    if re.fullmatch(r"(?:[-–—]\s*){3,}", stripped):
        return True
    if re.fullmatch(r"(?:[•·]\s*){3,}", stripped):
        return True
    if re.fullmatch(r"(?:[~#◇◆❦✦✧]\s*){2,}", stripped):
        return True
    return bool(ORNAMENTAL_WORDS.fullmatch(stripped))
