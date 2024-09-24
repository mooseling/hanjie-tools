import unittest
from puzzle import Puzzle
from utils import copy_side_clues
from square import Square

class UtilsTest(unittest.TestCase):
    def test_copy_side_clues(self) -> None:
        side_clues = [
            [1, 2, 3],
            [4, 5],
            [6],
            [7, 8, 9, 10]
        ]

        copied_side_clues = copy_side_clues(side_clues)

        self.assertEqual(side_clues, copied_side_clues)
        self.assertFalse(side_clues is copied_side_clues)
        self.assertFalse(side_clues[0] is copied_side_clues[0])
        self.assertFalse(side_clues[1] is copied_side_clues[1])
        self.assertFalse(side_clues[2] is copied_side_clues[2])
        self.assertFalse(side_clues[3] is copied_side_clues[3])

class SquareTest(unittest.TestCase):
    def test_getters(self) -> None:
        self.assertEqual(Square.UNKNOWN.get_grid_char(), ' ')
        self.assertEqual(Square.UNKNOWN.get_fiendly_string(), 'unknown')
        self.assertEqual(Square.FILLED.get_grid_char(), '#')
        self.assertEqual(Square.FILLED.get_fiendly_string(), 'filled')
        self.assertEqual(Square.KNOWN_BLANK.get_grid_char(), '/')
        self.assertEqual(Square.KNOWN_BLANK.get_fiendly_string(), 'blank')

class PuzzleTest(unittest.TestCase):
    def test_init(self) -> None:
        row_clues = [[1, 2], [3, 4], [5], [5], [1, 1]]
        column_clues = [[1, 2], [3], [3], [1, 1, 1], [5], [5], [4], [2]]

        puzzle = Puzzle(5, 8, row_clues, column_clues)

        self.assertEqual(len(puzzle.rows), 5)
        for row in puzzle.rows:
            self.assertEqual(len(row), 8)

        self.assertEqual(puzzle.row_clues, row_clues)
        self.assertFalse(puzzle.row_clues is row_clues) # check this list is copied, not referencing the original
        self.assertEqual(puzzle.column_clues, column_clues)
        self.assertFalse(puzzle.column_clues is column_clues)


if __name__ == '__main__':
    unittest.main()
