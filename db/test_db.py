import unittest
import os
import json
import sqlite3

from db import DB
from grid.grid import Grid

class TestDB(unittest.TestCase):

    def setUp(self) -> None:
        if os.path.exists('testing.db'):
            os.remove('testing.db')

        self.db = DB('testing.db')

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

    def test_connection(self):
        self.assertIsNotNone(self.db.connection)

    def test_close_connection(self):
        self.db.close_connection()

        query = """SELECT count(*) FROM grid"""
        with self.assertRaises(sqlite3.ProgrammingError):
            self.db._execute_query(query)[0][0]


    def tearDown(self) -> None:
        self.db.close_connection()
        os.remove('testing.db')

    def test_execute_query(self):
        query = """SELECT count(*) from grid"""

        data = self.db._execute_query(query)[0][0]
        self.assertIsNotNone(data)
        self.assertGreaterEqual(data, 0)

        self.db.insert_grid(self.grid_01)
        self.db.insert_grid(self.grid_01)

        data = self.db._execute_query(query)[0][0]
        self.assertIsNotNone(data)
        self.assertGreaterEqual(data, 2)

        query = """SELECT max(id) from grid"""
        data = self.db._execute_query(query)[0][0]
        self.assertIsNotNone(data)
        self.assertGreaterEqual(data, 2)

        query = """DELETE from grid where id = 1"""
        data = self.db._execute_query(query)
        self.assertIsNotNone(data)
        self.assertEqual(len(data), 0)

        query = """SELECT count(*) FROM grid"""
        data = self.db._execute_query(query)[0][0]
        self.assertIsNotNone(data)
        self.assertGreaterEqual(data, 1)

    def test_execute_insert_query(self):
        scores_json = json.dumps(self.grid_02.scores)
        query = """INSERT INTO grid (size, grid_values, scores) 
        VALUES ({0}, '{1}', '{2}')""".format(self.grid_02.size, self.grid_02.values, scores_json)

        data = self.db._execute_insert_query(query)
        self.assertIsNotNone(data)
        self.assertEqual(1, data)

        scores_json = json.dumps(self.grid_01.scores)
        query = """INSERT INTO grid (size, grid_values, scores) 
        VALUES ({0}, '{1}', '{2}')""".format(self.grid_01.size, self.grid_01.values, scores_json)

        data = self.db._execute_insert_query(query)
        self.assertIsNotNone(data)
        self.assertEqual(2, data)

        scores_json = json.dumps(self.grid_03.scores)
        query = """INSERT INTO grid (size, grid_values, scores) 
                VALUES ({0}, '{1}', '{2}')""".format(self.grid_03.size, self.grid_03.values, scores_json)

        data = self.db._execute_insert_query(query)
        self.assertIsNotNone(data)
        self.assertEqual(3, data)


    def test_insert_and_get_grid(self):
        data_01 = self.db.insert_grid(self.grid_01)
        data_02 = self.db.insert_grid(self.grid_02)
        data_03 = self.db.insert_grid(self.grid_03)

        scores_02 = self.db.get_grid(data_02)
        self.assertListEqual(scores_02.scores, self.grid_02_scores)

        scores_03 = self.db.get_grid(data_03)
        self.assertListEqual(scores_03.scores, self.grid_03_scores)

        scores_01 = self.db.get_grid(data_01)
        self.assertListEqual(scores_01.scores, self.grid_01_scores)


if __name__ == '__main__':
    unittest.main()

