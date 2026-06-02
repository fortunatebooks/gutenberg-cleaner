"""Clean public-domain source texts into reusable manuscript formats."""

from gutenberg_cleaner.cleaner import CleanupResult, clean_text
from gutenberg_cleaner.reports import CleanupReport

__all__ = ["CleanupReport", "CleanupResult", "clean_text"]
__version__ = "0.1.0"
