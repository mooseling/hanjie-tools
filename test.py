import unittest
from puzzle import Puzzle
from utils import copySideClues
from square import Square

class UtilsTest(unittest.TestCase):
    def test_copySideClues(self) -> None:
        sideClues = [
            [1, 2, 3],
            [4, 5],
            [6],
            [7, 8, 9, 10]
        ]

        copiedSideClues = copySideClues(sideClues)

        self.assertEqual(sideClues, copiedSideClues)
        self.assertFalse(sideClues is copiedSideClues)
        self.assertFalse(sideClues[0] is copiedSideClues[0])
        self.assertFalse(sideClues[1] is copiedSideClues[1])
        self.assertFalse(sideClues[2] is copiedSideClues[2])
        self.assertFalse(sideClues[3] is copiedSideClues[3])

class SquareTest(unittest.TestCase):
    def test_getters(self) -> None:
        self.assertEqual(Square.UNKNOWN.getGridChar(), ' ')
        self.assertEqual(Square.UNKNOWN.getFriendlyString(), 'unknown')
        self.assertEqual(Square.FILLED.getGridChar(), '#')
        self.assertEqual(Square.FILLED.getFriendlyString(), 'filled')
        self.assertEqual(Square.BLANK.getGridChar(), '/')
        self.assertEqual(Square.BLANK.getFriendlyString(), 'blank')

class PuzzleTest(unittest.TestCase):
    def test_init(self) -> None:
        rowClues = [[1, 2], [3, 4], [5], [5], [1, 1]]
        columnClues = [[1, 2], [3], [3], [1, 1, 1], [5], [5], [4], [2]]

        puzzle = Puzzle(5, 8, rowClues, columnClues)

        self.assertEqual(len(puzzle.rows), 5)
        for row in puzzle.rows:
          self.assertEqual(len(row), 8)

        self.assertEqual(puzzle.rowClues, rowClues)
        self.assertFalse(puzzle.rowClues is rowClues) # check this list is copied, not referencing the original
        self.assertEqual(puzzle.columnClues, columnClues)
        self.assertFalse(puzzle.columnClues is columnClues)


if __name__ == '__main__':
    unittest.main()
