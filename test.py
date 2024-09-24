import unittest
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


if __name__ == '__main__':
    unittest.main()