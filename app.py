import sqlite3
from flask import Flask, request

app = Flask(__name__)


@app.route("/test/", methods=['GET'])
def test():
    con = sqlite3.connect("grids.db")

    cursor = con.cursor()

    cursor.execute("SELECT name FROM sqlite_master")
    data = cursor.fetchone()

    print(data)

    return data if data is not None else {}


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
    app.run(debug=True)
