from pathlib import Path

from gutenberg_cleaner.toc import remove_toc_artifacts

FIXTURES = Path(__file__).parent / "fixtures"


def test_remove_toc_artifacts():
    cleaned, modified = remove_toc_artifacts(
        (FIXTURES / "messy_toc.md").read_text(encoding="utf-8")
    )

    assert modified is True
    assert "Table of Contents" not in cleaned
    assert "chapter1.xhtml" not in cleaned
    assert "Chapter Three ........ 30" not in cleaned
    assert "Body text survives." in cleaned
    assert "# Chapter Two" in cleaned
