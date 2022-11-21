import os
from flask import Flask, request, jsonify
from flask_jsonrpc import JSONRPC

from db.db_postgresql import DBPostgresql


from grid.grid import Grid

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

# postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user="postgres",
#                                                          password="pass@#29",
#                                                          host="127.0.0.1",
#                                                          port="5432",
#                                                          database="postgres_db")

dbpostgresql_pool = [DBPostgresql(os.getenv('DB_HOSTNAME'), os.getenv('DB_NAME'), os.getenv('DB_USERNAME'),
                                  os.getenv('DB_PASSWORD'), os.getenv('DB_PORT')) for i in range(1, 20)]


@app.route("/sun-spot-analyser-api/grid", methods=['POST'])
def submit_grid():
    """
    Sends a grid to be stored in the database.

    Parameters to be sent as json
        size: how big is the side of the square matrix
        values: list containing the values of a size*size grid

    :return: id in the database of the grid sent
    """

    data = request.get_json()
    size = data.get('size', 0)
    values = data.get('values', '')

    return submit_grid(size, values)


@jsonrpc.method('App.submit_grid')
def submit_grid(size: int, values: str):
    """
    Sends a grid to be stored in the database.

    Parameters to be sent as json
        size: how big is the side of the square matrix
        values: list containing the values of a size*size grid

    :return: id in the database of the grid sent
    """

    # db = DBPostgresql(os.getenv('DB_HOSTNAME'), os.getenv('DB_NAME'), os.getenv('DB_USERNAME'),
    #                   os.getenv('DB_PASSWORD'), os.getenv('DB_PORT'))

    db = dbpostgresql_pool.pop()

    grid = Grid(size, values)

    db_id = {'id': db.insert_grid(grid)}

    dbpostgresql_pool.append(db)

    return jsonify(db_id)


@app.route("/sun-spot-analyser-api/scores", methods=['GET'])
# @jsonrpc.method('get_scores_for_grid')
def get_scores_for_grid():
    """
    Function to obtain the scores of the grid. The method should receive the id of the grid

    :return: The scores calculated for the grid
    """
    db_id = request.args.get('id', default=0, type=int)

    # db = DBPostgresql(os.getenv('DB_HOSTNAME'), os.getenv('DB_NAME'), os.getenv('DB_USERNAME'),
    #                   os.getenv('DB_PASSWORD'), os.getenv('DB_PORT'))

    db = dbpostgresql_pool.pop()

    grid = db.get_grid(db_id)

    dbpostgresql_pool.append(db)

    if grid:
        return jsonify(scores=grid.scores)
    else:
        return jsonify(scores=None)


@app.route("/sun-spot-analyser-api/scores_sorted", methods=['GET'])
# @jsonrpc.method('App.get_top_scores_for_grid')
def get_top_scores_for_grid():
    """
    Get the biggest values from the list of scores

    Parameters to be sent:
        db_id: id of the grid in the database
        number_items: number of elements to be returned

    :return: A list containing 'number_values' grid positions including its score.
             The list is sorted in descending score order
    """

    db_id = request.args.get('id', default=0, type=int)
    number_items = request.args.get('number_items', default=0, type=int)

    # db = DBPostgresql(os.getenv('DB_HOSTNAME'), os.getenv('DB_NAME'), os.getenv('DB_USERNAME'),
    #                   os.getenv('DB_PASSWORD'), os.getenv('DB_PORT'))

    db = dbpostgresql_pool.pop()

    grid = db.get_grid(db_id)

    dbpostgresql_pool.append(db)

    if grid:
        sorted_list = grid.get_biggest_values(number_items)
        return jsonify(sorted_list)
    else:
        return jsonify(scores=None)


@app.route("/sun-spot-analyser-api/delete", methods=['DELETE'])
# @jsonrpc.method('App.delete_grid')
def delete_grid():
    """
    Deletes the grid from the database. The id of the grid must be provided

    :return: The grid deleted from the database
    """
    db_id = request.args.get('id', default=0, type=int)

    # db = DBPostgresql(os.getenv('DB_HOSTNAME'), os.getenv('DB_NAME'), os.getenv('DB_USERNAME'),
    #                   os.getenv('DB_PASSWORD'), os.getenv('DB_PORT'))

    db = dbpostgresql_pool.pop()

    grid = db.delete_grid(db_id)

    dbpostgresql_pool.append(db)

    if grid:
        grid_dict = dict(size=grid.size,
                         values=grid.values,
                         scores=grid.scores['scores'])
        return jsonify(grid_dict)
    else:
        return jsonify(scores=None)


@app.route("/", methods=['GET'])
# @jsonrpc.method('app.main')
def main():
    return """Welcome to the sun-spot-analyser-api
    
    Available operations are:
        "/sun-spot-analyser-api/delete", methods=['DELETE']
        "/sun-spot-analyser-api/scores_sorted", methods=['GET']
        "/sun-spot-analyser-api/scores", methods=['GET']
        "/sun-spot-analyser-api/grid", methods=['POST']
        "/sun-spot-analyser-api/info/", methods=['GET']
    """


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
