from pdf_price_extractor.table_extractor import group_words_into_rows

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