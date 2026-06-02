"""Command-line interface for Gutenberg Cleaner."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from gutenberg_cleaner import __version__
from gutenberg_cleaner.cleaner import clean_text
from gutenberg_cleaner.converters import write_outputs


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "clean":
        return _clean_command(args)
    if args.command == "inspect":
        return _inspect_command(args)
    parser.print_help()
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gutenberg-cleaner",
        description="Clean public-domain texts into tidy Markdown, HTML, EPUB, and optional DOCX.",
    )
    parser.add_argument("--version", action="version", version=f"gutenberg-cleaner {__version__}")
    subparsers = parser.add_subparsers(dest="command")

    clean = subparsers.add_parser("clean", help="Clean a manuscript and write output files.")
    clean.add_argument("input", type=Path, help="Input .txt or .md manuscript.")
    clean.add_argument("--title", help="Override detected title.")
    clean.add_argument("--author", help="Override detected author.")
    clean.add_argument(
        "--formats",
        default="md,json",
        help="Comma-separated formats: md,json,html,epub,docx.",
    )
    clean.add_argument("--out", type=Path, help="Output file path for single-format runs.")
    clean.add_argument("--out-dir", type=Path, help="Directory for generated files.")

    inspect = subparsers.add_parser(
        "inspect",
        help="Print the cleanup report without writing files.",
    )
    inspect.add_argument("input", type=Path, help="Input .txt or .md manuscript.")
    inspect.add_argument("--title", help="Override detected title.")
    inspect.add_argument("--author", help="Override detected author.")
    return parser


def _clean_command(args: argparse.Namespace) -> int:
    raw = args.input.read_text(encoding="utf-8")
    result = clean_text(raw, title=args.title, author=args.author)
    formats = [part.strip() for part in args.formats.split(",") if part.strip()]
    output_base = _output_base(args.input, args.out, args.out_dir, formats)
    paths = write_outputs(
        result.markdown,
        output_base=output_base,
        formats=formats,
        title=result.report.title,
        author=result.report.author,
        report=result.report,
    )
    for fmt, path in paths.items():
        print(f"{fmt}: {path}")
    return 0


def _inspect_command(args: argparse.Namespace) -> int:
    raw = args.input.read_text(encoding="utf-8")
    result = clean_text(raw, title=args.title, author=args.author)
    print(json.dumps(result.report.to_dict(), indent=2, ensure_ascii=False))
    return 0


def _output_base(
    input_path: Path,
    out: Path | None,
    out_dir: Path | None,
    formats: list[str],
) -> Path:
    if out and out_dir:
        raise SystemExit("Use either --out or --out-dir, not both.")
    if out:
        if len(formats) == 1:
            return out.with_suffix("")
        raise SystemExit("--out is only valid when one output format is requested.")
    directory = out_dir or input_path.parent
    return directory / input_path.stem


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
