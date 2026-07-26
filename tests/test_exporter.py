from pdf_price_extractor.exporter import export_to_csv
import csv

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