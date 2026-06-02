import json
from pathlib import Path

from gutenberg_cleaner.cli import main

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
