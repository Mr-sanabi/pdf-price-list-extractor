"""Extract table-like data from PDF pages."""

from pdf_price_extractor.pdf_reader import extract_page_words

def group_words_into_rows(words, y_tolerance=3):
    if not words:
        return []

    sorted_words = sorted(words, key=lambda word: word[1])


    rows = []
    current_row = []
    current_y = None


    for word in sorted_words:
        word_y = word[1]

        if not current_row:
            current_row.append(word)
            current_y = word_y

        elif abs(word_y - current_y) <= y_tolerance:
            current_row.append(word)

        else:
            sorted_x = sorted(current_row, key=lambda word: word[0])
            rows.append(sorted_x)
            current_row = [word]
            current_y = word_y

    last_sorted = sorted(current_row, key=lambda word: word[0])
    rows.append(last_sorted)
    return rows


def split_row_into_columns(row, column_boundaries):
    columns = [[] for _ in range(len(column_boundaries) + 1)]

    for word in row:
        word_x = word[0]
        word_text = word[4]
        column_index = 0

        for boundary in column_boundaries:
            if word_x < boundary:
                break

            column_index += 1

        columns[column_index].append(word_text)

    return [" ".join(column) for column in columns]


def extract_table_rows(rows, column_boundaries):
    table_rows = []
    header_found = False
    expected_header = [
        "SKU",
        "PRODUCT",
        "DIMENSIONS",
        "WEIGHT",
        "POWER",
        "PRICE",
    ]

    for row in rows:
        columns = split_row_into_columns(row, column_boundaries)

        if not header_found:
            if columns == expected_header:
                header_found = True

            continue

        if columns[0] and columns[5]:
            table_rows.append(columns)

    return table_rows


def extract_table_from_page(
    pdf_path,
    page_number,
    column_boundaries,
    y_tolerance=3,
):
    words = extract_page_words(pdf_path, page_number)
    rows = group_words_into_rows(words, y_tolerance)
    table_rows = extract_table_rows(rows, column_boundaries)
    return table_rows