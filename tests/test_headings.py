from gutenberg_cleaner.headings import count_heading_levels, normalize_headings


def test_normalize_chapter_headings():
    text = (
        "CHAPTER ONE\n\n"
        "A paragraph with plenty of words after the heading.\n\n"
        "Chapter Two\n\n"
        "More text."
    )

    cleaned, changed, levels = normalize_headings(text)

    assert changed == 2
    assert "# CHAPTER ONE" in cleaned
    assert "# Chapter Two" in cleaned
    assert levels == {"h1": 2}


def test_count_heading_levels():
    assert count_heading_levels("# One\n\n## Two\n\n### Three") == {"h1": 1, "h2": 1, "h3": 1}
