"""Tests for normalizer."""

from pdf_price_extractor.normalizer import row_to_record, clean_text, parse_price, is_valid_record, split_records, normalize_record, normalize_records

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
    invalid_result1 = parse_price("$74.13")
    invalid_result2 = parse_price("$4,448.56")
    invalid_result3 = parse_price("€19.99")

    assert result == ("PLN", 349.00)
    assert isinstance(result[0], str)
    assert isinstance(result[1], float)
    assert invalid_result1 == ("$", 74.13)
    assert invalid_result2 == ("$", 4448.56)
    assert invalid_result3 == ("€", 19.99)


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


def test_normalize_record():
    row = [
        " LMP-1001 ",
        "  Kanso   Desk\nLamp ",
        "42 x 18 x 55 cm",
        "2.4 kg",
        "12 W",
        "PLN 349.00",
    ]

    result = normalize_record(row)

    assert result == {        
        "sku": "LMP-1001",
        "product": "Kanso Desk Lamp",
        "dimensions": "42 x 18 x 55 cm",
        "weight": "2.4 kg",
        "power": "12 W",
        "price_raw": "PLN 349.00",
        "currency": "PLN",
        "price": 349.0,
    }


def test_normalize_records():
    valid_row = [
        "LMP-1001",
        "Kanso Desk Lamp",
        "42 x 18 x 55 cm",
        "2.4 kg",
        "12 W",
        "PLN 349.00",
    ]

    invalid_row = valid_row.copy()
    invalid_row[0] = "   "

    na_row = valid_row.copy()
    na_row[-1] = "NA"

    defaulted_row = valid_row.copy()
    defaulted_row[-1] = "DEFAULTED"


    accepted, rejected = normalize_records([valid_row, na_row, defaulted_row])
    assert len(accepted) == 1
    assert len(rejected) == 2
    assert accepted[0]["currency"] == "PLN"
    assert accepted[0]["price"] == 349.0