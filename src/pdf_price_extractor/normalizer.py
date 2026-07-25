"""Normalize prices, currencies, dimensions, and measurement units."""

def row_to_record(row):
    keys = [
        "sku",
        "product",
        "dimensions",
        "weight",
        "power",
        "price_raw",
    ]

    return dict(zip(keys, row))

def clean_text(value):

    splited_value = value.split()
    clean_value = " ".join(splited_value)

    return clean_value