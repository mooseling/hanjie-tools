from common_types import Line, SideClues
from line_algorithms import LineChanges
from utils import copy_side_clues
from square import Square


class Puzzle:
    rows: list[Line]
    row_clues: SideClues
    column_clues: SideClues


    def __init__(self, num_rows: int, num_columns: int, row_clues: SideClues, column_clues: SideClues) -> None:
        self.row_clues = copy_side_clues(row_clues)
        self.column_clues = copy_side_clues(column_clues)

        # don't use [[] * c] * r, this will make all the rows be the same list
        self.rows = [[Square.UNKNOWN] * num_columns for x in range(num_rows)]

    
    def get_row(self, row_index: int) -> Line:
        return self.rows[row_index]
    

    def get_column(self, column_index: int) -> Line:
        return [row[column_index] for row in self.rows]
    

    def apply_row_changes(self, changes: LineChanges, row_index: int) -> None:
        for column_index, new_value in enumerate(changes):
            if new_value != Square.UNKNOWN:
                self.set_cell(row_index, column_index, new_value)


    def apply_column_changes(self, changes: LineChanges, column_index: int) -> None:
        for row_index, new_value in enumerate(changes):
            if new_value != Square.UNKNOWN:
                self.set_cell(row_index, column_index, new_value)


    def set_cell(self, row_index: int, column_index: int, new_value: Square) -> None:
        self.rows[row_index][column_index] = new_value
