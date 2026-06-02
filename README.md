# Gutenberg Cleaner

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Gutenberg Cleaner** is a tiny, deterministic command-line toolkit for turning
Project Gutenberg and other public-domain source texts into tidy Markdown,
HTML, EPUB, and optional DOCX manuscripts.

It is built for educators, archivists, indie publishers, ebook makers, and
accessibility projects that need reusable public-domain texts without manually
removing boilerplate, table-of-contents debris, odd scene breaks, and heading
inconsistencies.

```bash
pipx install gutenberg-cleaner

gutenberg-cleaner clean pride-and-prejudice.txt \
  --title "Pride and Prejudice" \
  --author "Jane Austen" \
  --formats md,html,epub,json \
  --out-dir dist/
```

> This open source package is intentionally **local-only by default**. It does
> not call APIs, send manuscripts over the network, or require any hosted
> service.

---

## What it cleans

Gutenberg Cleaner focuses on predictable cleanup steps that are easy to inspect
and regression-test:

- Removes Project Gutenberg header/footer boilerplate when explicit START/END
  markers are present.
- Detects title and author metadata from common Gutenberg headers.
- Normalizes chapter-like lines into Markdown headings.
- Converts ornamental scene breaks (`* * *`, em-dash rules, bullets, divider
  labels, etc.) into a consistent `***` marker.
- Removes copied/generated table-of-contents artifacts such as XHTML fragment
  links and dotted page lists.
- Tidies extra whitespace and common OCR-style artifacts.
- Produces a machine-readable cleanup report with word counts, heading levels,
  removed sections, and warnings.

## Before and after

**Input**

```text
The Project Gutenberg eBook of Example Book
Title: Example Book
Author: Ada Writer

*** START OF THE PROJECT GUTENBERG EBOOK EXAMPLE BOOK ***

CONTENTS
Chapter I ........ 1
chapter-1.xhtml#id

CHAPTER I

A paragraph from the book.

* * *

CHAPTER II

Another paragraph.

*** END OF THE PROJECT GUTENBERG EBOOK EXAMPLE BOOK ***
```

**Output Markdown**

```md
# CHAPTER I

A paragraph from the book.

***

# CHAPTER II

Another paragraph.
```

**Report**

```json
{
  "title": "Example Book",
  "author": "Ada Writer",
  "boilerplate_removed": true,
  "toc_removed": true,
  "headings_normalized": 2,
  "scene_breaks_normalized": 1,
  "word_count_before": 49,
  "word_count_after": 12,
  "heading_levels": {"h1": 2},
  "warnings": []
}
```

---

## Installation

### From a fresh clone

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
```

### Development install

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
```

### Optional DOCX output

Markdown, JSON report, HTML, and EPUB output use only the Python standard
library. DOCX output is optional:

```bash
python -m pip install -e '.[docx]'
# or, if the package is installed with pipx:
pipx inject gutenberg-cleaner python-docx
```

---

## CLI usage

### Clean to Markdown and report JSON

```bash
gutenberg-cleaner clean examples/gutenberg_sample.txt --out-dir dist/
```

By default this writes:

```text
dist/gutenberg_sample.md
dist/gutenberg_sample.report.json
```

### Generate multiple formats

```bash
gutenberg-cleaner clean examples/gutenberg_sample.txt \
  --formats md,html,epub,json \
  --out-dir dist/
```

### Generate one exact output file

```bash
gutenberg-cleaner clean input.txt --formats md --out clean.md
```

### Inspect only

```bash
gutenberg-cleaner inspect examples/gutenberg_sample.txt
```

---

## Python API

```python
from gutenberg_cleaner import clean_text

raw = """*** START OF THE PROJECT GUTENBERG EBOOK DEMO ***
CHAPTER I

It was a bright cold day.
*** END OF THE PROJECT GUTENBERG EBOOK DEMO ***
"""

result = clean_text(raw, title="Demo")
print(result.markdown)
print(result.report.to_dict())
```

---

## Cleanup philosophy

Gutenberg Cleaner is conservative where accidental deletion would be costly and
opinionated where publishing conventions are clear:

- **Boilerplate removal requires explicit markers.** A normal essay that merely
  mentions Project Gutenberg is preserved.
- **Markdown is the canonical output.** DOCX/EPUB are convenience exports built
  from the cleaned Markdown.
- **Every behavior should have a fixture.** Formatting bugs become small public
  regression tests.
- **No silent service coupling.** The package has no web app, database, cloud
  storage, account, or network-service dependencies.

---

## Repository layout

```text
src/gutenberg_cleaner/
  boilerplate.py    # Gutenberg marker stripping and metadata detection
  cleaner.py        # high-level clean_text API
  cli.py            # argparse CLI
  converters.py     # Markdown/HTML/EPUB/optional DOCX writers
  headings.py       # heading normalization
  reports.py        # cleanup report dataclass
  scene_breaks.py   # ornamental break normalization
  toc.py            # TOC artifact removal
tests/
  fixtures/         # small public-domain-style fixtures
  test_*.py         # regression tests
examples/
  gutenberg_sample.txt
```

---

## Development

```bash
python -m pip install -e '.[dev]'
ruff check .
pytest
python -m build
```

The CI workflow runs linting, tests, and package builds on pull requests.

## Roadmap

- More Gutenberg marker variants and public fixture coverage.
- Better language-agnostic chapter structure scoring.
- Optional validation against EPUBCheck when installed locally.
- More export checks for generated EPUB and DOCX files.

## Contributing

Bug reports with small source snippets are welcome. Please include:

1. The smallest input text that reproduces the issue.
2. The output you expected.
3. Your command and Python version.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full development workflow.

## License

MIT. See [LICENSE](LICENSE).

## Public-domain source note

Project Gutenberg texts can have specific trademark and redistribution terms.
This tool helps remove boilerplate for downstream manuscripts, but users are
responsible for complying with the terms of the source text they use.
