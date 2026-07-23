"""Read PDF documents and expose page-level text, blocks, and words."""

from pathlib import Path

import pymupdf

def get_page_count(pdf_path):
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")
    with pymupdf.open(path) as document:
        return document.page_count

def extract_page_text(pdf_path, page_number):
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")

    with pymupdf.open(pdf_path) as document:
        page = document.load_page(page_number)
        text = page.get_text()

        return text 

def extract_document_text(pdf_path):
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")

    result = []
    with pymupdf.open(pdf_path) as document:
        for page in document:
            text = page.get_text()
            result.append(text)

        return "\n".join(result)

