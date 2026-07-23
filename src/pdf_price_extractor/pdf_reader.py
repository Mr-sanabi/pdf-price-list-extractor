"""Read PDF documents and expose page-level text, blocks, and words."""

from pathlib import Path

import pymupdf

def get_page_count(pdf_path):
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")
    with pymupdf.open(path) as document:
        return document.page_count

