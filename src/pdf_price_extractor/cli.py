import argparse
import sys

from pdf_price_extractor.pipeline import run_pipeline

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
    parser.add_argument(
        "--header",
        nargs="+",
        default=None,
        help="Expected table header names",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    pdf_path=args.pdf_path
    output_path=args.output_path
    page_number=args.page
    column_boundaries=args.columns
    expected_header=args.header
    try:
        accepted, rejected = run_pipeline(
            pdf_path,
            output_path,
            page_number,
            column_boundaries,
            expected_header=expected_header,
        )
    except FileNotFoundError:
        print(
            f"Error: PDF file not found: {pdf_path}", 
            file=sys.stderr
        )
        return 1

    except ValueError as error:
        print(
            f"Error: {error}", 
            file=sys.stderr
        )
        return 1

    except IndexError:
        print(
            f"Error: Page {page_number} does not exist", 
            file=sys.stderr
        )
        return 1

    print(f"Exported: {len(accepted)}")
    print(f"Rejected: {len(rejected)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())