import sqlite3
import json
from grid.grid import Grid


class DB:

    def __init__(self, db_name: str):
        """Check if the tables exists or if it has to be created"""
        self.connection = sqlite3.connect(db_name)

        sql_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='grid'"

        cursor = self.connection.cursor()

        cursor.execute(sql_query)

        try:
            data = cursor.fetchone()[0]
        except TypeError as e:
            data = None

        if not data:
            # Create table
            sql_query = """CREATE TABLE grid (id INTEGER PRIMARY KEY AUTOINCREMENT,
            size INT NOT NULL, grid_values TEXT NOT NULL, scores TEXT)"""

            cursor.execute(sql_query)

            self.connection.commit()

            sql_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='grid'"

            cursor.execute(sql_query)

            try:
                data = cursor.fetchone()[0]
            except TypeError as e:
                print("Not able to create the needed table: grid")

    def __enter__(self):
        """

        :return:
        """
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Created to use the context

        :param exc_type: Type of exception
        :param exc_val: Exception value
        :param exc_tb: Exception Traceback
        :return:
        """
        if exc_type is not None:
            self._rollback_transaction()
        else:
            self._commit_transaction()

    def __del__(self):
        self.close_connection()

    def close_connection(self):
        """
        Closes the connection to the database if the client does not do it

        """
        try:
            self.connection.close()
        except Exception as e:
            print(e)

    def _rollback_transaction(self):
        """
        makes a rollback of the current transaction

        """
        self.connection.rollback()

    def _commit_transaction(self):
        """
        Persist data in the database

        """
        self.connection.commit()

    def _execute_query(self, query: str) -> list:
        """
        Execute a query passed as a parameter

        :param query: Query to be performed to the database
        :return: All data retrived from the database
        """
        with self:
            cursor = self.connection.cursor()

            cursor.execute(query)

            data = cursor.fetchall()

        return data

    def _execute_insert_query(self, query: str) -> int:
        """
        Execute a query passed as a parameter

        :param query: Query to be performed to the database
        :return: Last id created with the insert
        """
        with self:
            cursor = self.connection.cursor()

            cursor.execute(query)

            data = cursor.lastrowid

        return data

    def insert_grid(self, grid: Grid) -> int:
        """

        :param grid:
        :return: id of the grid inserted in the DB
        """

        scores_json = json.dumps(grid.scores)

        query = """INSERT INTO grid (size, grid_values, scores) 
        VALUES ({0}, '{1}', '{2}')""".format(grid.size, grid.values, scores_json)

        data = self._execute_insert_query(query)

        return data

    def get_grid(self, id: int) -> Grid:
        """

        :param id: id of the grid to be retrived from the database
        :return: Grid stored in the database
        """

        query = """SELECT size, grid_values, scores
        FROM grid
        WHERE id = {0}""".format(id)

        data = self._execute_query(query)

        if len(data) > 0:
            grid = Grid(data[0][0], data[0][1], eval(data[0][2]))
        else:
            grid = None

        return grid
