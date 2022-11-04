import sqlite3
from flask import Flask, request

from db import DB

app = Flask(__name__)


def _init():
    db = DB()

    db.execute_query("SELECT name FROM sqlite_master WHERE type='table' AND name='grid'")

    # db.close_connection()

    print("_init executed")


@app.route("/test/", methods=['GET'])
def test():
    db = DB()

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
    values = data.get('values', 0)
    print("{0}: {1}".format(size, values))
    return {"id": 1}


@app.route("/sun-spot-analyser-api/scores", methods=['GET'])
def get_scores_for_grid():
    id = request.args.get('id', default=0, type=int)
    return {"scores": [{"x": 1, "y": 1, "score": 10}]}


@app.route("/", methods=['GET'])
def main():
    return "hello World!!"


if __name__ == '__main__':
    _init()
    app.run(debug=True)
