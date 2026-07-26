"""Export accepted and rejected records to CSV or Excel."""

import csv

def export_to_csv(records, output_path):
    if not records:
        return
    
    fields = [
        "sku",
        "product",
        "dimensions",
        "weight",
        "power",
        "price_raw",
        "currency",
        "price",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)
        