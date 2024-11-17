from data_classes import CluedBlock, Line
from square import Square


class Puzzle:
    _row_squares: list[list[Square]]
    row_clues: list[list[CluedBlock]]
    column_clues: list[list[CluedBlock]]


    def __init__(self, num_rows: int, num_columns: int, row_clues: list[list[int]], column_clues: list[list[int]]) -> None:
        self.row_clues = [[CluedBlock(length, index) for index, length in enumerate(line_clues)] for line_clues in row_clues]
        self.column_clues = [[CluedBlock(length, index) for index, length in enumerate(line_clues)] for line_clues in column_clues]

        # don't use [[] * c] * r, this will make all the rows be the same list
        self._row_squares = [[Square.UNKNOWN] * num_columns for _ in range(num_rows)]


    def get_rows(self) -> list[Line]:
        return [self.get_row(row_index) for row_index, _ in enumerate(self._row_squares)]

    def get_columns(self) -> list[Line]:
        return [self.get_column(column_index) for column_index, _ in enumerate(self._row_squares[0])]


    def get_row(self, row_index: int) -> Line:
        return Line(self.row_clues[row_index], self._row_squares[row_index], row_index, 'row', False)


    def get_column(self, column_index: int) -> Line:
        return Line(self.column_clues[column_index], self._get_column_squares(column_index), column_index, 'column', False)


    def apply_line_changes(self, changes: list[Square], *, row_index: int|None = None, column_index: int|None = None) -> None:
        if row_index != None and column_index != None:
            raise Exception('Only try to change one row or column at a time')
        
        if row_index != None:
            for square_index, new_value in enumerate(changes):
                if new_value != Square.UNKNOWN:
                    self._set_square(row_index, square_index, new_value)
        
        if column_index != None:
            for square_index, new_value in enumerate(changes):
                if new_value != Square.UNKNOWN:
                    self._set_square(square_index, column_index, new_value)


    def _set_square(self, row_index: int, column_index: int, new_value: Square) -> None:
        current_value = self._row_squares[row_index][column_index]
        if current_value != new_value and current_value != Square.UNKNOWN:
            raise Exception(f'Tried to overwrite a square with a different value ({current_value.get_grid_char()} -> {new_value.get_grid_char()}). Row {row_index}, column {column_index}')
        self._row_squares[row_index][column_index] = new_value


    def _get_column_squares(self, column_index: int) -> list[Square]:
        return [row[column_index] for row in self._row_squares]
