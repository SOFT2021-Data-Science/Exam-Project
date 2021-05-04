from flask import Flask
from utils.aliases import RESOURCES_DIR
from logic.basic import basic_sdg
import os

app = Flask(__name__)


@app.route("/")
def index():
    return "This is the backend for the dsc project"


# E.g. http://localhost:5000/basic/2002&2012
@app.route("/basic/<int:min>&<int:max>")
def sdg_basic_route(min, max):
    if min > max:
        return "400 - Minimum value is larger than max"
    try:
        basic_sdg(min, max)
        return "ok"
    except Exception as e:
        if bool(os.getenv('DEBUG')):
            return f"500 - {e}"
        return 500


if __name__ == "__main__":
    os.environ['DEBUG'] = "True"
    app.run(host="127.0.0.1", debug=True)
