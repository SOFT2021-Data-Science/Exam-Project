from flask import Flask
from utils.aliases import RESOURCES_DIR
from logic.basic import basic_sdg

app = Flask(__name__)


@app.route("/")
def index():
    return "stuff works"


@app.route("/stuff")
def stuff_route():
    basic_sdg()
    return "ok"

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)