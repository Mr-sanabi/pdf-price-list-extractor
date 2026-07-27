from pdf_price_extractor.cli import build_parser

def test_build_parser():
    parser = build_parser()
    args = parser.parse_args([
        "sample.pdf",
        "products.csv",
        "--page",
        "2",
        "--columns",
        "50",
        "120",
        "250",
        "370",
    ])
    assert args.pdf_path == "sample.pdf"
    assert args.output_path == "products.csv"
    assert args.page == 2
    assert args.columns == [50, 120, 250, 370]


def test_build_parser_uses_default_page():
    parser = build_parser()

    args = parser.parse_args([
        "sample.pdf",
        "products.csv",
        "--columns",
        "50",
        "120",
        "250",
        "370",
    ])

    assert args.page == 0