import json
from pathlib import Path

import pytest

from gutenberg_cleaner.cli import _parse_formats, main

FIXTURES = Path(__file__).parent / "fixtures"


def test_cli_clean_writes_markdown_and_report(tmp_path):
    code = main([
        "clean",
        str(FIXTURES / "gutenberg_sample.txt"),
        "--formats",
        "md,json,html,epub",
        "--out-dir",
        str(tmp_path),
    ])

    assert code == 0
    assert (tmp_path / "gutenberg_sample.md").exists()
    assert (tmp_path / "gutenberg_sample.html").exists()
    assert (tmp_path / "gutenberg_sample.epub").exists()
    report = json.loads((tmp_path / "gutenberg_sample.report.json").read_text(encoding="utf-8"))
    assert report["boilerplate_removed"] is True


def test_cli_inspect_prints_report(capsys):
    code = main(["inspect", str(FIXTURES / "gutenberg_sample.txt")])

    assert code == 0
    captured = capsys.readouterr().out
    assert '"title": "Example Book"' in captured


def test_cli_normalizes_and_deduplicates_formats():
    assert _parse_formats(" MD, .json,md ") == ["md", "json"]


def test_cli_rejects_empty_formats():
    with pytest.raises(SystemExit, match="At least one output format"):
        _parse_formats(" , ")


def test_cli_rejects_unknown_formats():
    with pytest.raises(SystemExit, match="Unsupported output format: pdf"):
        _parse_formats("md,pdf")
