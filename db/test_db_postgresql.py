import unittest
import os

import psycopg2
from psycopg2 import connect, extensions, InterfaceError
import json

from db_postgresql import DBPostgresql
from grid.grid import Grid


class TestDBPostgresql(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ['DB_NAME'] = 'database'
        os.environ['DB_HOSTNAME'] = 'localhost'
        os.environ['DB_USERNAME'] = 'username'
        os.environ['DB_PASSWORD'] = 'secret'
        os.environ['DB_PORT'] = '6432'


    def setUp(self) -> None:
        self.db = DBPostgresql(os.getenv('DB_HOSTNAME'), os.getenv('DB_NAME'), os.getenv('DB_USERNAME'),
                               os.getenv('DB_PASSWORD'), os.getenv('DB_PORT'))
        autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
        self.db.connection.set_isolation_level(autocommit)

        cursor = self.db.connection.cursor()
        sql_query = 'DROP TABLE IF EXISTS grid'
        cursor.execute(sql_query)

        sql_query = 'DROP SEQUENCE IF EXISTS grid_id_seq'
        cursor.execute(sql_query)

        sql_query = "CREATE SEQUENCE grid_id_seq START 1;"
        cursor.execute(sql_query)

        sql_query = """CREATE TABLE IF NOT EXISTS grid( 
        id INT PRIMARY KEY NOT NULL DEFAULT nextval('grid_id_seq'),
        size INT NOT NULL,
        grid_values VARCHAR NOT NULL,
        scores JSONB);"""
        cursor.execute(sql_query)

        self.grid_01 = Grid(1, '1')
        self.grid_02 = Grid(2, '1, 2, 3, 4')
        self.grid_03 = Grid(3, '4, 2, 3, 2, 2, 1, 3, 2, 1')

        self.grid_01_scores = {"scores": [{"score": 1, "x": 0, "y": 0}]}

        self.grid_02_scores = {"scores": [{"score": 10, "x": 0, "y": 0}, {"score": 10, "x": 0, "y": 1},
                                          {"score": 10, "x": 1, "y": 0}, {"score": 10, "x": 1, "y": 1}]}

        self.grid_03_scores = {"scores": [{"score": 10, "x": 0, "y": 0}, {"score": 14, "x": 0, "y": 1},
                                          {"score": 8, "x": 0, "y": 2}, {"score": 15, "x": 1, "y": 0},
                                          {"score": 20, "x": 1, "y": 1}, {"score": 11, "x": 1, "y": 2},
                                          {"score": 9, "x": 2, "y": 0}, {"score": 11, "x": 2, "y": 1},
                                          {"score": 6, "x": 2, "y": 2}]}

    def tearDown(self) -> None:
        if not self.db.connection.closed:
            cursor = self.db.connection.cursor()
            sql_query = 'DROP TABLE IF EXISTS grid'
            cursor.execute(sql_query)

            sql_query = "DROP SEQUENCE IF EXISTS grid_id_seq"
            cursor.execute(sql_query)

            self.db.close_connection()

    @classmethod
    def tearDownClass(cls) -> None:
        db = DBPostgresql(os.getenv('DB_HOSTNAME'), os.getenv('DB_NAME'), os.getenv('DB_USERNAME'),
                               os.getenv('DB_PASSWORD'), os.getenv('DB_PORT'))
        autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
        db.connection.set_isolation_level(autocommit)
        cursor = db.connection.cursor()
        sql_query = "CREATE SEQUENCE IF NOT EXISTS grid_id_seq START 1;"
        cursor.execute(sql_query)

        sql_query = """CREATE TABLE IF NOT EXISTS grid( 
                id INT PRIMARY KEY NOT NULL DEFAULT nextval('grid_id_seq'),
                size INT NOT NULL,
                grid_values VARCHAR NOT NULL,
                scores JSONB);"""
        cursor.execute(sql_query)

    def test_connection(self):
        self.assertIsNotNone(self.db.connection)

    def test_close_connection(self):
        self.db.close_connection()

        query = """SELECT count(*) FROM grid"""
        with self.assertRaises(InterfaceError):
            self.db._execute_query(query)[0][0]

    def test_execute_query(self):
        query = """SELECT count(*) from grid"""

        data = self.db._execute_query(query)[0][0]
        self.assertIsNotNone(data)
        self.assertEqual(data, 0)

        self.db.insert_grid(self.grid_01)
        self.db.insert_grid(self.grid_01)

        data = self.db._execute_query(query)[0][0]
        self.assertIsNotNone(data)
        self.assertGreaterEqual(data, 2)

        query = """SELECT max(id) from grid"""
        data = self.db._execute_query(query)[0][0]
        self.assertIsNotNone(data)
        self.assertGreaterEqual(data, 2)

        # Delete sentence raises exception as Delete is not returning any value
        with self.assertRaises(psycopg2.ProgrammingError):
            query = """DELETE from grid where id = 1"""
            data = self.db._execute_query(query)

        query = """SELECT count(*) FROM grid"""
        data = self.db._execute_query(query)[0][0]
        self.assertIsNotNone(data)
        self.assertGreaterEqual(data, 1)

    def test_execute_insert_query(self):
        scores_json = json.dumps(dict(scores=self.grid_02.scores))
        query = """INSERT INTO grid (size, grid_values, scores) 
        VALUES ({0}, '{1}', '{2}') RETURNING ID""".format(self.grid_02.size, self.grid_02.values, scores_json)

        data = self.db._execute_insert_query(query)
        self.assertIsNotNone(data)
        self.assertEqual(1, data)

        scores_json = json.dumps(dict(scores=self.grid_01.scores))
        query = """INSERT INTO grid (size, grid_values, scores) 
        VALUES ({0}, '{1}', '{2}') RETURNING ID""".format(self.grid_01.size, self.grid_01.values, scores_json)

        data = self.db._execute_insert_query(query)
        self.assertIsNotNone(data)
        self.assertEqual(2, data)

        scores_json = json.dumps(dict(scores=self.grid_03.scores))
        query = """INSERT INTO grid (size, grid_values, scores) 
                VALUES ({0}, '{1}', '{2}') RETURNING ID""".format(self.grid_03.size, self.grid_03.values, scores_json)

        data = self.db._execute_insert_query(query)
        self.assertIsNotNone(data)
        self.assertEqual(3, data)

    def test_insert_and_get_grid(self):
        data_01 = self.db.insert_grid(self.grid_01)
        data_02 = self.db.insert_grid(self.grid_02)
        data_03 = self.db.insert_grid(self.grid_03)

        scores_02 = self.db.get_grid(data_02)
        self.assertListEqual(scores_02.scores, self.grid_02_scores['scores'])

        scores_03 = self.db.get_grid(data_03)
        self.assertListEqual(scores_03.scores, self.grid_03_scores['scores'])

        scores_01 = self.db.get_grid(data_01)
        self.assertListEqual(scores_01.scores, self.grid_01_scores['scores'])


if __name__ == '__main__':
    unittest.main()

