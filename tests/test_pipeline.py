from pathlib import Path

import pytest

from pdf_price_extractor.pipeline import run_pipeline
import pdf_price_extractor.pipeline as pipeline_module

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def test_run_pipeline_exports_normalized_records(tmp_path):
    pdf_path = FIXTURES_DIR / "sample.pdf"
    output_path = tmp_path / "products.csv"

    accepted, rejected = run_pipeline(
        pdf_path=pdf_path,
        output_path=output_path,
        page_number=0,
        column_boundaries=[170, 350, 470, 550, 630]
    )

    assert len(accepted) == 5
    assert len(rejected) == 0
    assert output_path.exists()

def test_run_pipeline_passes_expected_header(monkeypatch, tmp_path):
    custom_header = [
        "ITEM",
        "DESCRIPTION",
        "SIZE",
        "MASS",
        "WATTAGE",
        "COST",
    ]

    received = {}

    def fake_extract_table_from_page(
        pdf_path,
        page_number,
        column_boundaries,
        expected_header=None,
    ):
        received["expected_header"] = expected_header
        return []

    monkeypatch.setattr(
        pipeline_module,
        "extract_table_from_page",
        fake_extract_table_from_page,
    )

    pdf_path = FIXTURES_DIR / "sample.pdf"
    output_path = tmp_path / "output.xlsx"

    pipeline_module.run_pipeline(
        pdf_path,
        output_path,
        page_number=0,
        column_boundaries=[170, 350, 470, 550, 630],
        expected_header=custom_header,
    )

    assert received["expected_header"] == custom_header


def test_run_pipeline_rejects_incompatible_table_schema(tmp_path):
    pdf_path = FIXTURES_DIR / "sample.pdf"
    output_path = tmp_path / "output.csv"

    with pytest.raises(ValueError, match="Exactly 5 column boundaries"):
        run_pipeline(
            pdf_path,
            output_path,
            page_number=0,
            column_boundaries=[100, 200, 300, 400],
        )

    with pytest.raises(ValueError, match="exactly 6 names"):
        run_pipeline(
            pdf_path,
            output_path,
            page_number=0,
            column_boundaries=[100, 200, 300, 400, 500],
            expected_header=["ITEM", "DESCRIPTION", "UNIT", "PACK", "PRICE"],
        )
