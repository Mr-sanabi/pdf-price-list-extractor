<p align="center">
  <img src="assets/readme/banner.png" alt="PDF Price List Extractor — PDF to structured CSV and XLSX data" width="100%">
</p>

<p align="center">
  Extract product tables from text-based PDF price lists, normalize the records, and export clean CSV or Excel files.
</p>

<p align="center">
  <img alt="Python 3.11+" src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white">
  <img alt="PyMuPDF" src="https://img.shields.io/badge/PDF-PyMuPDF-00A98F">
  <img alt="CSV and XLSX export" src="https://img.shields.io/badge/Export-CSV%20%7C%20XLSX-217346">
  <img alt="35 tests" src="https://img.shields.io/badge/Tests-35%20passing-2EA44F">
</p>

## What it does

```text
PDF page → words → rows → columns → normalized records → CSV / XLSX
```

- Reads positioned words from a PDF page with PyMuPDF.
- Reconstructs table rows using vertical coordinates.
- Splits each row into six columns using configurable X-coordinate boundaries.
- Cleans whitespace and separates currency from numeric price.
- Validates required fields and reports accepted/rejected counts.
- Exports accepted records to `.csv` or `.xlsx`.

## Quick start

Requires Python 3.11 or newer.

```bash
git clone https://github.com/Mr-sanabi/pdf-price-list-extractor.git
cd pdf-price-list-extractor
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Install the project:

```bash
pip install -e .
```

## Usage

```bash
python -m pdf_price_extractor.cli INPUT.pdf OUTPUT.csv \
  --page 0 \
  --columns X1 X2 X3 X4 X5
```

Run the included sample:

```bash
python -m pdf_price_extractor.cli \
  tests/fixtures/sample.pdf \
  output/products.csv \
  --page 0 \
  --columns 170 350 470 550 630
```

Successful output:

```text
Exported: 5
Rejected: 0
```

Change the destination extension to export Excel:

```bash
python -m pdf_price_extractor.cli \
  tests/fixtures/sample.pdf \
  output/products.xlsx \
  --columns 170 350 470 550 630
```

### Choosing column boundaries

`--columns` accepts five X-coordinate boundaries that divide a row into the six expected fields:

```text
SKU | PRODUCT | DIMENSIONS | WEIGHT | POWER | PRICE
```

The values are PDF coordinates, so they depend on the layout of each price list. The sample coordinates above are tuned for `tests/fixtures/sample.pdf`.

## Output

| Field | Example |
|---|---|
| `sku` | `LMP-1001` |
| `product` | `Kanso Desk Lamp` |
| `dimensions` | `42 x 18 x 55 cm` |
| `weight` | `2.4 kg` |
| `power` | `12 W` |
| `price_raw` | `PLN 349.00` |
| `currency` | `PLN` |
| `price` | `349.0` |

## Current scope

The extractor currently targets text-based PDFs with one table layout and the six-column schema shown above.

- One page is processed per command.
- Scanned/image-only PDFs require OCR and are not supported yet.
- Column boundaries must be provided for the source layout.
- Accepted records are exported; rejected records are counted but not written to a separate file.

## Development

Install development dependencies and run the full test suite:

```bash
pip install -e ".[dev]"
pytest -v
```

The suite covers PDF reading, row and column extraction, normalization, CSV/XLSX export, the complete pipeline, CLI parsing, and CLI error handling.

## Built with

[PyMuPDF](https://pymupdf.readthedocs.io/) · [openpyxl](https://openpyxl.readthedocs.io/) · [pytest](https://docs.pytest.org/)
