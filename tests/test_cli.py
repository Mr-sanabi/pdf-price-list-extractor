import sys

from pdf_price_extractor.cli import build_parser, main

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