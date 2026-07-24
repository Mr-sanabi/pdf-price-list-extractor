from pdf_price_extractor.table_extractor import group_words_into_rows, split_row_into_columns
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

def test_split_row_into_columns():
    row = [
        (105, 100, 160, 110, "LMP-1001", 0, 0, 0),
        (190, 100, 225, 110, "Kanso", 0, 0, 1),
        (230, 100, 260, 110, "Desk", 0, 0, 2),
        (265, 100, 300, 110, "Lamp", 0, 0, 3),
        (374, 100, 390, 110, "42", 0, 0, 4),
        (400, 100, 410, 110, "x", 0, 0, 5),
        (490, 100, 510, 110, "2.4", 0, 0, 6),
        (520, 100, 535, 110, "kg", 0, 0, 7),
        (575, 100, 590, 110, "12", 0, 0, 8),
        (600, 100, 615, 110, "W", 0, 0, 9),
        (652, 100, 675, 110, "PLN", 0, 0, 10),
        (690, 100, 730, 110, "349.00", 0, 0, 11),
    ]
    result = split_row_into_columns(row, [170, 350, 470, 550, 630])
    assert result == [
        "LMP-1001",
        "Kanso Desk Lamp",
        "42 x",
        "2.4 kg",
        "12 W",
        "PLN 349.00",
    ]