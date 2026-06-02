from pathlib import Path

from gutenberg_cleaner import clean_text

FIXTURES = Path(__file__).parent / "fixtures"


def test_clean_text_runs_full_pipeline():
    result = clean_text((FIXTURES / "gutenberg_sample.txt").read_text(encoding="utf-8"))

    assert result.report.title == "Example Book"
    assert result.report.author == "Ada Writer"
    assert result.report.boilerplate_removed is True
    assert result.report.toc_removed is True
    assert result.report.headings_normalized == 2
    assert result.report.scene_breaks_normalized == 1
    assert result.report.word_count_after < result.report.word_count_before
    assert "CONTENTS" not in result.markdown
    assert "chapter-1.xhtml" not in result.markdown
    assert "# CHAPTER I" in result.markdown
    assert "***" in result.markdown


def test_clean_text_adds_title_when_no_heading_exists():
    result = clean_text("A short body only.", title="Manual Title", author="Manual Author")

    assert result.markdown.startswith("# Manual Title\n\n_by Manual Author_")
    assert result.report.heading_levels["h1"] == 1
