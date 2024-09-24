from common_types import Line, SideClues
from utils import copy_side_clues
from square import Square


class Puzzle:
    rows: list[Line]
    row_clues: SideClues
    column_clues: SideClues


    def __init__(self, num_rows: int, num_columns: int, row_clues: SideClues, column_clues: SideClues) -> None:
        self.row_clues = copy_side_clues(row_clues)
        self.column_clues = copy_side_clues(column_clues)

        self.rows = [[Square.UNKNOWN] * num_columns] * num_rows

    
    def get_row(self, row_index: int) -> Line:
        return self.rows[row_index]
    

    def get_column(self, column_index: int) -> Line:
        return [row[column_index] for row in self.rows]