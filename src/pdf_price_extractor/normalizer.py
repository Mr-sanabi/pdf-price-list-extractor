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
    