"""Tests for normalizer."""

from pdf_price_extractor.normalizer import row_to_record, clean_text, parse_price, is_valid_record, split_records

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


def test_parse_price():
    result = parse_price("PLN 349.00")

    assert result == ("PLN", 349.00)
    assert isinstance(result[0], str)
    assert isinstance(result[1], float)


def test_is_valid_record():
    valid_record = {
        "sku": "LMP-1001",
        "product": "Kanso Desk Lamp",
        "dimensions": "42 x 18 x 55 cm",
        "weight": "2.4 kg",
        "power": "12 W",
        "price_raw": "PLN 349.00",
    }

    invalid_record = valid_record.copy()
    invalid_record["sku"] = "   "

    assert is_valid_record(valid_record) is True
    assert is_valid_record(invalid_record) is False


def test_split_records():
    valid_record = {
        "sku": "LMP-1001",
        "product": "Kanso Desk Lamp",
        "dimensions": "42 x 18 x 55 cm",
        "weight": "2.4 kg",
        "power": "12 W",
        "price_raw": "PLN 349.00",
    }

    invalid_record = valid_record.copy()
    invalid_record["sku"] = "   "
    accepted, rejected = split_records([valid_record, invalid_record])

    assert accepted == [valid_record]
    assert rejected == [invalid_record]