"""Temporary experiments for inspecting PDF text, blocks, and word coordinates."""

from pathlib import Path

import pymupdf


pdf_path = Path("sample.pdf")

with pymupdf.open(pdf_path) as document:
    print(f"Pages: {len(document)}")

    page = document[2 - 1]

    print(f"Page width: {page.rect.width}")
    print(f"Page height: {page.rect.height}")

    words = page.get_text("words", sort=True)

    lines = {}
    for word in words:
        x0, y0, x1, y1, text, block_no, line_no, word_no = word

        line_y = round(y0)

        if line_y not in lines:
            lines[line_y] = []

        lines[line_y].append((x0, text))

        for line_y in sorted(lines):
            line_words = lines[line_y]
            line_words = sorted(line_words, key=lambda item: item[0])
            line_text = " ".join(text for x0, text in line_words)
            print(line_y, line_text)
