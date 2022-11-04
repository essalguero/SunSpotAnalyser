import sqlite3


class DB:

    def __init__(self):
        """Check if the tables exists or if it has to be created"""
        self.connection = sqlite3.connect("grids.db")

        sql_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='grid'"

        cursor = self.connection.cursor()

        cursor.execute(sql_query)

        try:
            data = cursor.fetchone()[0]
        except TypeError as e:
            print("Table not found: grid")
            data = None

        if not data:
            # Create table
            sql_query = """CREATE TABLE grid (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                grid TEXT NOT NULL, 
                scores TEXT)"""

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

    def execute_query(self, query):
        """
        Execute a query passed as a parameter

        :param query:
        :return:
        """
        with self:
            cursor = self.connection.cursor()

            cursor.execute(query)

            data = cursor.fetchone()[0]

    def close_connection(self):
        try:
            self.connection.close()
        except Exception as e:
            print(e)

    def _rollback_transaction(self):
        self.connection.rollback()

    def _commit_transaction(self):
        self.connection.commit()
