# PDF Price List Extractor

A Python 3.11+ CLI that extracts a six-column product table from a text-based PDF page and saves accepted rows to CSV or Excel.

## Run

```bash
python -m pip install -e .
python -m pdf_price_extractor.cli tests/fixtures/sample.pdf data/output/products.csv --page 0 --columns 170 350 470 550 630
```

Change the output extension to `.xlsx` for Excel. `--page` is zero-based.
The five `--columns` values are PDF X coordinates tuned for the sample, not universal settings.

Source order: `SKU`, `PRODUCT`, `DIMENSIONS`, `WEIGHT`, `POWER`, `PRICE`. Use `--header` with exactly six names to match different headers; the field order stays fixed.
Output fields: `sku`, `product`, `dimensions`, `weight`, `power`, `price_raw`, `currency`, `price`.

## Limits

Text PDFs only, no OCR. One page per command, manually configured column boundaries, fixed product schema. Price parsing expects a currency token followed by a number. Rejected rows are counted but not exported separately.
Use `python -m pdf_price_extractor.cli --help` for options.

## Tests

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```
