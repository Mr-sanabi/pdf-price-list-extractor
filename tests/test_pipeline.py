from pathlib import Path

from pdf_price_extractor.pipeline import run_pipeline

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