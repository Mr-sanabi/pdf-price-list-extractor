"""Tests for normalizer."""

from pdf_price_extractor.normalizer import row_to_record, clean_text

def test_row_to_record():
    row = [
        "LMP-1001",
        "Kanso Desk Lamp",
        "42 x 18 x 55 cm",
        "2.4 kg",
        "12 W",
        "PLN 349.00",
    ]

    result = row_to_record(row)

    assert result == {
        "sku": "LMP-1001",
        "product": "Kanso Desk Lamp",
        "dimensions": "42 x 18 x 55 cm",
        "weight": "2.4 kg",
        "power": "12 W",
        "price_raw": "PLN 349.00",
    }


def test_clean_text():
    assert clean_text("  Kanso   Desk\nLamp  ") == "Kanso Desk Lamp"
    assert clean_text("\t42 x 18 x 55 cm\n") == "42 x 18 x 55 cm"
    assert clean_text("") == ""
