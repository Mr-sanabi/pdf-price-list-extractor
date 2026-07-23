"""Tests for pdf_reader."""


from pathlib import Path

import pytest

from pdf_price_extractor.pdf_reader import get_page_count, extract_page_text


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_get_page_count():
    pdf_path = FIXTURES_DIR / "sample.pdf"

    assert get_page_count(pdf_path) == 2


def test_get_page_count_missing_file():
    pdf_path = FIXTURES_DIR / "missing.pdf"

    with pytest.raises(FileNotFoundError):
        get_page_count(pdf_path)


def test_extract_page_text():
    pdf_path = FIXTURES_DIR / "sample.pdf"

    text = extract_page_text(pdf_path, page_number=0)
    assert isinstance(text, str)
    assert "Kanso Desk Lamp" in text
    assert "Page 2" not in text