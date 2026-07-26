from pdf_price_extractor.exporter import export_to_csv, export_to_excel, export_records
import csv
from openpyxl import load_workbook
import pytest

def test_export_to_csv(tmp_path):
    records = [
        {
            "sku": "LMP-1001",
            "product": "Kanso Desk Lamp",
            "dimensions": "42 x 18 x 55 cm",
            "weight": "2.4 kg",
            "power": "12 W",
            "price_raw": "PLN 349.00",
            "currency": "PLN",
            "price": 349.0,
        }
    ]  
    output_path = tmp_path / "products.csv"
    export_to_csv(records, output_path)
    assert output_path.exists()
    with open (output_path, "r",encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    assert len(rows) == 1
    assert rows[0]["sku"] == "LMP-1001"
    assert rows[0]["currency"] == "PLN"
    assert rows[0]["price"] == "349.0"


def test_export_to_excel(tmp_path):
    records = [
        {
            "sku": "LMP-1001",
            "product": "Kanso Desk Lamp",
            "dimensions": "42 x 18 x 55 cm",
            "weight": "2.4 kg",
            "power": "12 W",
            "price_raw": "PLN 349.00",
            "currency": "PLN",
            "price": 349.0,
        }
    ]  

    output_path = tmp_path / "products.xlsx"

    export_to_excel(records, output_path)

    assert output_path.exists()
    workbook = load_workbook(output_path)
    worksheet = workbook.active
    assert worksheet["A1"].value == "sku"
    assert worksheet["B1"].value == "product"
    assert worksheet["H1"].value == "price"
    assert worksheet["A2"].value == "LMP-1001"
    assert worksheet["B2"].value == "Kanso Desk Lamp"
    assert worksheet["G2"].value == "PLN"
    assert worksheet["H2"].value == 349.0


def test_export_records_to_csv(tmp_path):
    records = [
        {
            "sku": "LMP-1001",
            "product": "Kanso Desk Lamp",
            "dimensions": "42 x 18 x 55 cm",
            "weight": "2.4 kg",
            "power": "12 W",
            "price_raw": "PLN 349.00",
            "currency": "PLN",
            "price": 349.0,
        }
    ]

    output_path = tmp_path / "products.csv"

    export_records(records, output_path)

    assert output_path.exists()


def test_export_records_to_excel(tmp_path):
    records = [
        {
            "sku": "LMP-1001",
            "product": "Kanso Desk Lamp",
            "dimensions": "42 x 18 x 55 cm",
            "weight": "2.4 kg",
            "power": "12 W",
            "price_raw": "PLN 349.00",
            "currency": "PLN",
            "price": 349.0,
        }
    ]

    output_path = tmp_path / "products.xlsx"

    export_records(records, output_path)

    assert output_path.exists()

def test_export_records_unsupported_format(tmp_path):
    output_path = tmp_path / "products.txt"

    with pytest.raises(ValueError, match="Unsupported output format"):
        export_records([], output_path)


def test_export_records_creates_parent_directories(tmp_path):
    records = [
        {
            "sku": "LMP-1001",
            "product": "Kanso Desk Lamp",
            "dimensions": "42 x 18 x 55 cm",
            "weight": "2.4 kg",
            "power": "12 W",
            "price_raw": "PLN 349.00",
            "currency": "PLN",
            "price": 349.0,
        }
    ]

    output_path = tmp_path / "output" / "reports" / "products.csv"

    export_records(records, output_path)

    assert output_path.exists()
    assert output_path.parent.exists()


def test_export_records_does_not_create_file_for_empty_records(tmp_path):
    output_path = tmp_path / "output" / "products.csv"

    export_records([], output_path)

    assert not output_path.exists()    