# Contributing

Thanks for helping improve Gutenberg Cleaner.

## Local setup

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
pytest
ruff check .
```

## Good issues and pull requests

The best contribution is a small fixture plus a regression test:

1. Add a minimal input under `tests/fixtures/`.
2. Add or update a focused `tests/test_*.py` assertion.
3. Keep cleanup deterministic and local-only.
4. Avoid adding heavyweight dependencies unless the feature cannot reasonably be
   implemented with the standard library.

## Scope boundaries

Please do not add web app code, hosted service assumptions, account flows, or
default network calls. This project should remain a small reusable public-domain
text cleanup utility.
