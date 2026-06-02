from gutenberg_cleaner.boilerplate import detect_metadata, strip_project_gutenberg_boilerplate


def test_strip_project_gutenberg_boilerplate_with_start_and_end_markers():
    text = (
        "# The Project Gutenberg eBook of Pride and Prejudice\n\n"
        "This ebook is for the use of anyone anywhere.\n\n"
        "*** START OF THE PROJECT GUTENBERG EBOOK PRIDE AND PREJUDICE ***\n\n"
        "# Chapter 1\n\n"
        "It is a truth universally acknowledged.\n\n"
        "*** END OF THE PROJECT GUTENBERG EBOOK PRIDE AND PREJUDICE ***\n\n"
        "End boilerplate text."
    )

    cleaned, modified = strip_project_gutenberg_boilerplate(text)

    assert modified is True
    assert "Project Gutenberg eBook" not in cleaned
    assert "START OF THE PROJECT GUTENBERG" not in cleaned
    assert "END OF THE PROJECT GUTENBERG" not in cleaned
    assert "# Chapter 1" in cleaned
    assert "It is a truth universally acknowledged." in cleaned
    assert "End boilerplate text." not in cleaned


def test_strip_project_gutenberg_boilerplate_is_conservative_without_markers():
    text = (
        "# Foreword\n\n"
        "We discuss Project Gutenberg as a historical archive in this essay.\n\n"
        "# Chapter 1\n\n"
        "Normal content."
    )
    cleaned, modified = strip_project_gutenberg_boilerplate(text)

    assert modified is False
    assert cleaned == text


def test_detect_metadata_from_gutenberg_header():
    title, author = detect_metadata("Title: My Book\nAuthor: Ada Writer\n")

    assert title == "My Book"
    assert author == "Ada Writer"
