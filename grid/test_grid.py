import unittest

from grid import Grid


class TestGrid(unittest.TestCase):

    def setUp(self):
        self.grid_01 = Grid(1, '1')
        self.grid_02 = Grid(2, '1, 2, 3, 4')
        self.grid_03 = Grid(3, '4, 2, 3, 2, 2, 1, 3, 2, 1')

        self.grid_01_scores = [{"score": 1, "x": 0, "y": 0}]

        self.grid_02_scores = [{"score": 10, "x": 0, "y": 0}, {"score": 10, "x": 0, "y": 1},
                               {"score": 10, "x": 1, "y": 0}, {"score": 10, "x": 1, "y": 1}]

        self.grid_03_scores = [{"score": 10, "x": 0, "y": 0}, {"score": 14, "x": 0, "y": 1},
                               {"score": 8, "x": 0, "y": 2}, {"score": 15, "x": 1, "y": 0},
                               {"score": 20, "x": 1, "y": 1}, {"score": 11, "x": 1, "y": 2},
                               {"score": 9, "x": 2, "y": 0}, {"score": 11, "x": 2, "y": 1},
                               {"score": 6, "x": 2, "y": 2}]

    def test_create_grid(self):
        with self.assertRaises(ValueError):
            grid_01 = Grid(0, '')

        with self.assertRaises(ValueError):
            grid_02 = Grid(-2, '')

        with self.assertRaises(ValueError):
            grid_03 = Grid(1, '')

        with self.assertRaises(ValueError):
            grid_04 = Grid(1, '1, 2')

        grid_05 = Grid(1, '1')
        self.assertListEqual(grid_05.scores, self.grid_01_scores)

        grid_06 = Grid(2, '1, 2, 3, 4')
        self.assertListEqual(grid_06.scores, self.grid_02_scores)

        grid_07 = Grid(3, '4, 2, 3, 2, 2, 1, 3, 2, 1')
        self.assertListEqual(grid_07.scores, self.grid_03_scores)


if __name__ == '__main__':
    unittest.main()
