# """Extract table-like data from PDF pages."""

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