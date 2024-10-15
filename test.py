import unittest
from block_utils import get_limits
from data_classes import CluedBlock, Line
from puzzle import Puzzle
from utils import index_of, index_of_any
from square import Square


class UtilsTest(unittest.TestCase):

    def test_index_of(self) -> None:
        line = [Square.UNKNOWN, Square.UNKNOWN, Square.UNKNOWN, Square.FILLED, Square.KNOWN_BLANK, Square.UNKNOWN]
        self.assertEqual(index_of(line, Square.UNKNOWN), 0)
        self.assertEqual(index_of(line, Square.FILLED), 3)
        self.assertEqual(index_of(line, Square.KNOWN_BLANK), 4)
        self.assertEqual(index_of(line, Square.UNKNOWN, 0), 0)
        self.assertEqual(index_of(line, Square.UNKNOWN, 3), 5)

    def test_index_of_any(self) -> None:
        line = [Square.UNKNOWN, Square.UNKNOWN, Square.UNKNOWN, Square.FILLED, Square.KNOWN_BLANK, Square.UNKNOWN]
        self.assertEqual(index_of_any(line, [Square.FILLED, Square.KNOWN_BLANK]), 3)
        self.assertEqual(index_of_any(line, [Square.KNOWN_BLANK, Square.FILLED]), 3)
        self.assertEqual(index_of_any(line, [Square.UNKNOWN, Square.FILLED, Square.KNOWN_BLANK]), 0)
        self.assertEqual(index_of_any(line, []), -1)

        int_list = [0, 1, 2, 3, 4]
        self.assertEqual(index_of_any(int_list, [2, 3]), 2)
        self.assertEqual(index_of_any(int_list, [5, 6]), -1)
        self.assertEqual(index_of_any(int_list, [5]), -1)


class SquareTest(unittest.TestCase):
    def test_getters(self) -> None:
        self.assertEqual(Square.UNKNOWN.get_grid_char(), ' ')
        self.assertEqual(Square.UNKNOWN.get_fiendly_string(), 'unknown')
        self.assertEqual(Square.FILLED.get_grid_char(), '#')
        self.assertEqual(Square.FILLED.get_fiendly_string(), 'filled')
        self.assertEqual(Square.KNOWN_BLANK.get_grid_char(), '⋅')
        self.assertEqual(Square.KNOWN_BLANK.get_fiendly_string(), 'blank')


class PuzzleTest(unittest.TestCase):
    def test_init(self) -> None:
        row_clues = [[1, 2], [3, 4], [5], [5], [1, 1]]
        column_clues = [[1, 2], [3], [3], [1, 1, 1], [5], [5], [4], [2]]

        puzzle = Puzzle(5, 8, row_clues, column_clues)

        self.assertEqual(len(puzzle.get_rows()), 5)
        self.assertEqual(len(puzzle.get_columns()), 8)

        for row_index, row in enumerate(puzzle.get_rows()):
            self.assertEqual(row.squares, [Square.UNKNOWN] * 8)
            for clue_index, clued_block in enumerate(row.clued_blocks):
                self.assertEqual(row_clues[row_index][clue_index], clued_block.length)

        for column_index, column in enumerate(puzzle.get_columns()):
            self.assertEqual(column.squares, [Square.UNKNOWN] * 5)
            for clue_index, clued_block in enumerate(column.clued_blocks):
                self.assertEqual(column_clues[column_index][clue_index], clued_block.length)


class BlockUtilsTest(unittest.TestCase):
    def test_get_limits(self) -> None:
        clued_block_1 = CluedBlock(3)
        clued_block_2 = CluedBlock(5)
        line_with_2_wiggle_room = Line([clued_block_1, clued_block_2], [Square.UNKNOWN] * 11)
        self.assertEqual(get_limits(clued_block_1, line_with_2_wiggle_room), (0, 4))
        self.assertEqual(get_limits(clued_block_2, line_with_2_wiggle_room), (4, 10))

        clued_block_3 = CluedBlock(3)
        clued_block_4 = CluedBlock(3)
        line_with_1_wiggle_room = Line([clued_block_3, clued_block_4], [Square.UNKNOWN] * 8)
        self.assertEqual(get_limits(clued_block_3, line_with_1_wiggle_room), (0, 3))
        self.assertEqual(get_limits(clued_block_4, line_with_1_wiggle_room), (4, 7))


if __name__ == '__main__':
    unittest.main(exit=False)
