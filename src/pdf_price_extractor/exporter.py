"""Export accepted and rejected records to CSV or Excel."""

import csv
from openpyxl import Workbook
from pathlib import Path

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


def export_to_excel(records, output_path):
    if not records:
        return

    workbook = Workbook()
    worksheet = workbook.active
    fieldnames = [
        "sku",
        "product",
        "dimensions",
        "weight",
        "power",
        "price_raw",
        "currency",
        "price",
    ]
    worksheet.append(fieldnames)

    for record in records:
        row = [record[field] for field in fieldnames]
        worksheet.append(row)

    workbook.save(output_path)

def export_records(records, output_path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    suffix = path.suffix.lower()

    if suffix == ".csv":
        export_to_csv(records, output_path)

    elif suffix == ".xlsx":
        export_to_excel(records, output_path)

    else:
        raise ValueError(f"Unsupported output format: {suffix}")
    