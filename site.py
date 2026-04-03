import json

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/opovo")
def get_opovo():
    with open("data/artigos_opovo.json", "r") as f:
        data = json.load(f)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
