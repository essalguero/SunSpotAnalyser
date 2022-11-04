import sqlite3
from flask import Flask, request, jsonify

from db import DB
from grid import Grid

app = Flask(__name__)


def _init():
    db = DB("grids.db")

    db.execute_query("SELECT name FROM sqlite_master WHERE type='table' AND name='grid'")

    # db.close_connection()

    print("_init executed")


@app.route("/test/", methods=['GET'])
def test():
    db = DB("test.db")

    data = db.execute_query("SELECT name FROM sqlite_master")

    print(data)

    # db.close_connection()

    return {'data': data} if data is not None else {}, 200


@app.route("/info/", methods=['GET'])
def info():
    return {'version': '0.0.1'}


@app.route("/sun-spot-analyser-api/grid", methods=['POST'])
def submit_grid():
    data = request.get_json()
    size = data.get('size', 0)
    values = data.get('values', '')
    print("{0}: {1}".format(size, values))

    db = DB("grids.db")

    grid = Grid(size, values)

    db_id = {'id': db.insert_grid(grid)}

    return jsonify(db_id)


@app.route("/sun-spot-analyser-api/scores", methods=['GET'])
def get_scores_for_grid():
    id = request.args.get('id', default=0, type=int)

    db = DB("grids.db")

    grid = db.get_grid(id)

    if grid:
        return jsonify(dict(scores=grid.scores))
    else:
        return jsonify(scores=None)


@app.route("/", methods=['GET'])
def main():
    return "hello World!!"


if __name__ == '__main__':
    app.run(debug=True)
