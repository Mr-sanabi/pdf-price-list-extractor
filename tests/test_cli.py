import sys

from pdf_price_extractor.cli import build_parser, main
import pdf_price_extractor.cli as cli_module

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


def test_main_handles_missing_pdf(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "pdf-price-extractor",
            "missing.pdf",
            "products.csv",
            "--columns",
            "82",
            "177",
            "326",
            "450",
            "505",
        ],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error: PDF file not found: missing.pdf" in captured.err


def test_main_handles_unsupported_output_format(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "pdf-price-extractor",
            "tests/fixtures/sample.pdf",
            "products.txt",
            "--columns",
            "82",
            "177",
            "326",
            "450",
            "505",
        ],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Unsupported output format" in captured.err


def test_main_handles_nonexistent_page(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "pdf-price-extractor",
            "tests/fixtures/sample.pdf",
            "products.csv",
            "--page",
            "99",
            "--columns",
            "82",
            "177",
            "326",
            "450",
            "505",
        ],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error: Page 99 does not exist" in captured.err


def test_main_passes_custom_header(monkeypatch):
    received = {}

    def fake_run_pipeline(
        pdf_path,
        output_path,
        page_number,
        column_boundaries,
        expected_header=None,
    ):
        received["expected_header"] = expected_header
        return [], []

    monkeypatch.setattr(
        cli_module,
        "run_pipeline",
        fake_run_pipeline,
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "pdf-price-extractor",
            "input.pdf",
            "output.xlsx",
            "--columns",
            "100",
            "200",
            "300",
            "400",
            "500",
            "--header",
            "ITEM",
            "DESCRIPTION",
            "SIZE",
            "MASS",
            "WATTAGE",
            "COST",
        ],
    )


    exit_code = cli_module.main()

  
    assert exit_code == 0
    assert received["expected_header"] == [
        "ITEM",
        "DESCRIPTION",
        "SIZE",
        "MASS",
        "WATTAGE",
        "COST",
    ]


def test_main_rejects_incompatible_custom_header(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "pdf-price-extractor",
            "input.pdf",
            "output.csv",
            "--columns",
            "100",
            "200",
            "300",
            "400",
            "500",
            "--header",
            "ITEM",
            "DESCRIPTION",
            "UNIT",
            "PACK",
            "PRICE",
        ],
    )

    exit_code = cli_module.main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Custom headers must contain exactly 6 names" in captured.err
    assert captured.out == ""
