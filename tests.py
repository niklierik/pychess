import unittest
from actors.board import Board

BOARD_WIDTH = 8
BOARD_HEIGHT = 8


class TestBoardTiles(unittest.TestCase):
    def _actual_test_of_tiles(self, board, names):
        for x in range(0, BOARD_WIDTH):
            for y in range(0, BOARD_HEIGHT):
                index = board.index(x, y)
                self.assertIsNotNone(index)
                tile = board.tile(index)
                self.assertIsNotNone(tile)
                self.assertEqual(tile.__str__(), names[index])

    def test_tiles_naming(self):
        board = Board(None)
        names = [""] * (BOARD_WIDTH * BOARD_HEIGHT)
        files = ["a", "b", "c", "d", "e", "f", "g", "h"]
        for x in range(0, BOARD_WIDTH):
            for y in range(0, BOARD_HEIGHT):
                rank = f"{8 - y}"
                index = board.index(x, y)
                self.assertIsNotNone(index)
                names[index] = f"{files[x]}{rank}"  # type: ignore
        self._actual_test_of_tiles(board, names)
        # flip the board
        board.perspective = board.perspective.opposite()
        names.reverse()
        self._actual_test_of_tiles(board, names)


if __name__ == "__main__":
    unittest.main()
