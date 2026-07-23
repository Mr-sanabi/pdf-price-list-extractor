"""Tests for pdf_reader."""


from pathlib import Path

import pytest

from pdf_price_extractor.pdf_reader import get_page_count


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_get_page_count():
    pdf_path = FIXTURES_DIR / "sample.pdf"

    assert get_page_count(pdf_path) == 2


def test_get_page_count_missing_file():
    pdf_path = FIXTURES_DIR / "missing.pdf"

    with pytest.raises(FileNotFoundError):
        get_page_count(pdf_path)