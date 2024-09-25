import math
from common_types import Line
from puzzle import Puzzle


def visualise_puzzle(puzzle:Puzzle) -> str:
    column_headers = get_column_headers(puzzle)
    return column_headers + '\n'.join([get_row_header(row_index) + visualise_row(row) for row_index, row in enumerate(puzzle.rows)])


def visualise_row(row:Line) -> str:
    return ''.join([cell.get_grid_char() for cell in row])


def get_row_header(row_index) -> str:
    return str(row_index + 1).rjust(2) + '|'


def get_column_headers(puzzle: Puzzle) -> str:
    row_count = len(puzzle.rows[0])
    column_count = len(puzzle.rows)
    max_digit_count = math.ceil(math.log10(row_count))
    header_digit_strs = ['   '] * max_digit_count

    for column_index in range(column_count):
        column_label = str(column_index + 1).rjust(max_digit_count)
        for digit_index in range(max_digit_count):
            header_digit_strs[digit_index] += column_label[digit_index]

    header_str = '\n'.join(header_digit_strs)
    return header_str + '\n' + '   ' + '_' * column_count + '\n'
