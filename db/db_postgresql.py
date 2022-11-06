import json
from grid.grid import Grid

import psycopg2


class DBPostgresql:

    def __init__(self, db_hostname: str, db_name: str, db_username: str, db_password: str, db_port: str):
        """
        Class to operate with the postgreSql database

        :param db_hostname:
        :param db_name:
        :param db_username:
        :param db_password:
        :param db_port:
        """

        self.connection = psycopg2.connect(
            host=db_hostname,
            database=db_name,
            user=db_username,
            password=db_password,
            port=db_port)

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

            data = cursor.fetchone()[0]

        return data

    def _execute_delete_query(self, query: str) -> list:
        """
        Execute a query passed as a parameter
        :param query: Query to be performed to the database
        :return: Last id created with the insert
        """
        with self:
            cursor = self.connection.cursor()

            cursor.execute(query)

            try:
                data = cursor.fetchone()
            except TypeError as e:
                data = None

        return data

    def insert_grid(self, grid: Grid) -> int:
        """
        Inserts a grid in the database, including the score of the positions
        :param grid:
        :return: id of the grid inserted in the DB
        """

        scores_json = json.dumps(dict(scores=grid.scores))
        query = """INSERT INTO grid (size, grid_values, scores) 
        VALUES ({0}, '{1}', '{2}') RETURNING ID""".format(grid.size, grid.values, scores_json)

        data = self._execute_insert_query(query)

        return data

    def get_grid(self, db_id: int) -> Grid:
        """
        Obtain grid from the database
        :param db_id: id of the grid to be retrived from the database
        :return: Grid stored in the database
        """

        query = """SELECT size, grid_values, scores
        FROM grid
        WHERE id = {0}""".format(db_id)

        data = self._execute_query(query)

        if len(data) > 0:
            grid = Grid(data[0][0], data[0][1], data[0][2]['scores'])
        else:
            grid = None

        return grid

    def delete_grid(self, db_id: int) -> Grid:
        """
        Delete specified grid from the database
        :param db_id: id of the grid to be deleted from the database
        :return: Grid deleted from the database
        """

        query = """DELETE FROM grid
        WHERE id = {0}
        RETURNING size, grid_values, scores""".format(db_id)

        data = self._execute_delete_query(query)

        if data and len(data) > 0:
            grid = Grid(data[0], data[1], data[2]['scores'])
        else:
            grid = None

        return grid

if __name__ == '__main__':
    db = DBPostgresql('localhost', 'database', 'username', 'secret', '6432')

    data = db.delete_grid(20)

    print(data)

    db.close_connection()

    print(db)
