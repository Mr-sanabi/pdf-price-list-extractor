"""Tests for pdf_reader."""


from pathlib import Path

import pytest

from pdf_price_extractor.pdf_reader import get_page_count, extract_page_text, extract_document_text, extract_page_words


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


def test_extract_document_text():
    pdf_path = FIXTURES_DIR / "sample.pdf"

    result = extract_document_text(pdf_path)
    assert isinstance(result, str)
    assert "Page 1" in result
    assert "Page 2" in result
    assert "Kanso Desk Lamp" in result
    assert "Yuki Side Table" in result


def test_extract_page_words():
    pdf_path = FIXTURES_DIR / "sample.pdf"

    words = extract_page_words(pdf_path, 0)

    assert isinstance(words, list)
    assert len(words) > 0
    assert len(words[0]) == 8
    assert isinstance(words[0][4], str)
    assert any(word[4] == "Kanso" for word in words)


def test_extract_page_text_negative_page_number():
    pdf_path = FIXTURES_DIR / "sample.pdf"

    with pytest.raises(IndexError):
        extract_page_text(pdf_path, -1)


def test_extract_page_text_page_number_out_of_range():
    pdf_path = FIXTURES_DIR / "sample.pdf"

    with pytest.raises(IndexError):
        extract_page_text(pdf_path, 2)


def test_extract_page_words_negative_page_number():
    pdf_path = FIXTURES_DIR / "sample.pdf"

    with pytest.raises(IndexError):
        extract_page_words(pdf_path, -1)


def test_extract_page_words_page_number_out_of_range():
    pdf_path = FIXTURES_DIR / "sample.pdf"

    with pytest.raises(IndexError):
        extract_page_words(pdf_path, 2)