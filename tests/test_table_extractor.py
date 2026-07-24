from pdf_price_extractor.table_extractor import group_words_into_rows
from pdf_price_extractor.pdf_reader import extract_page_words
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def test_group_words_into_rows():
    words = [
        (100, 50, 140, 60, "Desk", 0, 0, 0),
        (200, 51, 240, 61, "Lamp", 0, 0, 1),
        (300, 80, 345, 90, "Price", 0, 1, 0),
    ]
    result = group_words_into_rows(words, y_tolerance=3)
    first_row_texts = [word[4] for word in result[0]]
    second_row_texts = [word[4] for word in result[1]]

    assert len(result) == 2
    assert first_row_texts == ["Desk", "Lamp"]
    assert second_row_texts == ["Price"]

def test_group_words_into_rows_from_pdf():
    pdf_path = FIXTURES_DIR / "sample.pdf"
    words = extract_page_words(pdf_path, 0)
    rows = group_words_into_rows(words, y_tolerance=3)
    row_texts = [
        " ".join(word[4] for word in row)
        for row in rows
    ]
    assert "SKU PRODUCT DIMENSIONS WEIGHT POWER PRICE" in row_texts
    assert "LMP-1001 Kanso Desk Lamp 42 x 18 x 55 cm 2.4 kg 12 W PLN 349.00" in row_texts
    assert "Page 1" in row_texts