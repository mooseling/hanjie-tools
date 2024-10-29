import math
from puzzle import Puzzle
from square import Square


def visualise_puzzle(puzzle:Puzzle) -> str:
    column_headers = get_column_headers(puzzle)
    return column_headers + '\n'.join([get_row_header(row_index) + visualise_row(row, row_index) for row_index, row in enumerate(puzzle._row_squares)])


def visualise_row(row_squares:list[Square], row_index: int) -> str:
    row_str = ''

    for square_index, square in enumerate(row_squares):
        if square == Square.UNKNOWN:
            if square_index % 5 == 4:
                row_str += '|'
            elif row_index % 5 == 4:
                row_str += '_'
            else:
                row_str += square.get_grid_char()
        else:
            row_str += square.get_grid_char()

    return row_str


def get_row_header(row_index: int) -> str:
    return str(row_index).rjust(2) + '|'


def get_column_headers(puzzle: Puzzle) -> str:
    column_count = len(puzzle._row_squares[0])
    max_digit_count = math.ceil(math.log10(column_count))
    header_digit_strs = ['   '] * max_digit_count

    for column_index in range(column_count):
        column_label = str(column_index).rjust(max_digit_count)
        for digit_index in range(max_digit_count):
            header_digit_strs[digit_index] += column_label[digit_index]

    header_str = '\n'.join(header_digit_strs)
    return header_str + '\n' + '   ' + '_' * column_count + '\n'
