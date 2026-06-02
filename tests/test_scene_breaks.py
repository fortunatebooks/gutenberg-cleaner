from pathlib import Path

from gutenberg_cleaner.scene_breaks import normalize_scene_breaks

FIXTURES = Path(__file__).parent / "fixtures"


def test_normalize_scene_break_variants_and_dedupe():
    cleaned, changed = normalize_scene_breaks(
        (FIXTURES / "ornamental_breaks.md").read_text(encoding="utf-8")
    )

    assert changed == 2
    assert cleaned.count("***") == 2
    assert "— — —" not in cleaned
    assert "* * *" not in cleaned
    assert "•••" not in cleaned
