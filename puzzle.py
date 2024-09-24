from utils import SideClues, copySideClues
from square import Square


type Line = list[Square]


class Puzzle:
    rows: list[Line]
    rowClues: SideClues
    columnClues: SideClues


    def __init__(self, numRows: int, numColumns: int, rowClues: SideClues, columnClues: SideClues) -> None:
        self.rowClues = copySideClues(rowClues)
        self.columnClues = copySideClues(columnClues)

        self.rows = [[Square.UNKNOWN] * numColumns] * numRows

    
    def getRow(self, rowIndex: int) -> Line:
        return self.rows[rowIndex]
    

    def getColumn(self, columnIndex: int) -> Line:
        return [row[columnIndex] for row in self.rows]