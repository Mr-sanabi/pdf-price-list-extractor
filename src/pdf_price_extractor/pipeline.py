"""Coordinate the extraction pipeline from PDF input to exported output."""

from pdf_price_extractor.table_extractor import extract_table_from_page
from pdf_price_extractor.normalizer import normalize_records
from pdf_price_extractor.exporter import export_records


def run_pipeline(
        pdf_path,
        output_path,
        page_number,
        column_boundaries,
    ):

    rows = extract_table_from_page(pdf_path, page_number, column_boundaries)
    accepted, rejected = normalize_records(rows)
    export_records(accepted, output_path)

    return accepted, rejected