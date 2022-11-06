import os
from flask import Flask, request, jsonify

from db.db_postgresql import DBPostgresql

from grid.grid import Grid

app = Flask(__name__)


@app.route("/test/", methods=['GET'])
def test():
    """
    Method to check that the app is running and DB is reachable

    :return: current date
    """

    db = DBPostgresql(os.getenv('DB_HOSTNAME'), os.getenv('DB_NAME'), os.getenv('DB_USERNAME'),
                      os.getenv('DB_PASSWORD'), os.getenv('DB_PORT'))

    data = db.execute_query("SELECT current_date")

    return {'data': data} if data is not None else {}, 200


@app.route("/sun-spot-analyser-api/grid", methods=['POST'])
def submit_grid():
    """
    Sends a grid to be stored in the database.

    Parameters to be sent as json
        size: how big is the side of the square matrix
        values: list containing the values of a size*size grid

    :return: id in the database of the sent grid
    """

    data = request.get_json()
    size = data.get('size', 0)
    values = data.get('values', '')

    db = DBPostgresql(os.getenv('DB_HOSTNAME'), os.getenv('DB_NAME'), os.getenv('DB_USERNAME'),
                      os.getenv('DB_PASSWORD'), os.getenv('DB_PORT'))

    grid = Grid(size, values)

    db_id = {'id': db.insert_grid(grid)}

    return jsonify(db_id)


@app.route("/sun-spot-analyser-api/scores", methods=['GET'])
def get_scores_for_grid():
    """
    Function to obtain the scores of the grid. The method should receive the id of the grid

    :return: The scores calculated for the grid
    """
    db_id = request.args.get('id', default=0, type=int)

    db = DBPostgresql(os.getenv('DB_HOSTNAME'), os.getenv('DB_NAME'), os.getenv('DB_USERNAME'),
                      os.getenv('DB_PASSWORD'), os.getenv('DB_PORT'))

    grid = db.get_grid(db_id)

    if grid:
        return jsonify(scores=grid.scores)
    else:
        return jsonify(scores=None)


@app.route("/sun-spot-analyser-api/scores_sorted", methods=['GET'])
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

    db = DBPostgresql(os.getenv('DB_HOSTNAME'), os.getenv('DB_NAME'), os.getenv('DB_USERNAME'),
                      os.getenv('DB_PASSWORD'), os.getenv('DB_PORT'))

    grid = db.get_grid(db_id)

    if grid:
        sorted_list = grid.get_biggest_values(number_items)
        return jsonify(sorted_list)
    else:
        return jsonify(scores=None)


@app.route("/sun-spot-analyser-api/delete", methods=['DELETE'])
def delete_grid():
    """
    Deletes the grid from the database. The id of the grid must be provided

    :return: The grid deleted from the database
    """
    db_id = request.args.get('id', default=0, type=int)

    db = DBPostgresql(os.getenv('DB_HOSTNAME'), os.getenv('DB_NAME'), os.getenv('DB_USERNAME'),
                      os.getenv('DB_PASSWORD'), os.getenv('DB_PORT'))

    grid = db.delete_grid(db_id)

    if grid:
        grid_dict = dict(size=grid.size,
                         values=grid.values,
                         scores=grid.scores['scores'])
        return jsonify(grid_dict)
    else:
        return jsonify(scores=None)


@app.route("/", methods=['GET'])
def main():
    return """Welcome to the sun-spot-analyser-api
    
    Available operations are:
        "/sun-spot-analyser-api/delete", methods=['DELETE']
        "/sun-spot-analyser-api/scores_sorted", methods=['GET']
        "/sun-spot-analyser-api/scores", methods=['GET']
        "/sun-spot-analyser-api/grid", methods=['POST']
        "/sun-spot-analyser-api/info/", methods=['GET']
        "/test/", methods=['GET']
    """


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
