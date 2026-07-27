import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract a price table from PDF")
    parser.add_argument("pdf_path", type=str, help="Path to the PDF file")
    parser.add_argument("output_path", type=str, help="Path to the output_path")
    parser.add_argument(
        "--page",
        type=int,
        default=0,
        help="Page number to process",
    )
    parser.add_argument(
        "--columns",
        type=int,
        nargs="+",
        required=True,
        help="Column boundaries"
    )
    return parser