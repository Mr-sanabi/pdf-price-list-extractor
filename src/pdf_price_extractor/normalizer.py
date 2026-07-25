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

def parse_price(price_raw):
    cleaned_price = clean_text(price_raw)
    currency, amount_text = cleaned_price.split(maxsplit=1)
    float_price = float(amount_text)
    return currency, float_price
