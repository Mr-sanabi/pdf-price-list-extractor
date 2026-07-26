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
    amount_text = amount_text.replace(",", "")
    float_price = float(amount_text)
    return currency, float_price

def is_valid_record(record):
    cleaned_sku = clean_text(record["sku"])
    cleaned_product = clean_text(record["product"])
    cleaned_price = clean_text(record["price_raw"])
    if not cleaned_sku or not cleaned_product or not cleaned_price:
        return False
    
    return True

def split_records(records):
    accepted = []
    rejected = []
    for record in records:
        valid = is_valid_record(record)
        if valid:
            accepted.append(record)
        else:
            rejected.append(record)

    return accepted, rejected


def normalize_record(row):
    record = row_to_record(row)
    for key, value in record.items():
        record[key] = clean_text(value)
        
    currency, price = parse_price(record["price_raw"])

    record["currency"] = currency
    record["price"] = price

    return record

def normalize_records(rows):
    normalized_records = []
    for row in rows:
        normalized_row = normalize_record(row)
        normalized_records.append(normalized_row)

    accepted, rejected = split_records(normalized_records)

    return accepted, rejected