from re import sub
from flask import Flask, render_template_string, send_file
from flask_cors import CORS, cross_origin
import os

from utils.aliases import OUT_DIR
from utils.misc import check_debug
from utils.logging import create_and_updatelog
from utils.file_handling import generate_file_name, IMAGE_FORMAT, file_name_exists
from logic.sdg import sdg_linear_regression
from service.abstract_instructions import AbstractInstruction


app = Flask(__name__)
CORS(app)
app.config["CORS_HEADERS"] = "*"

for subclass in AbstractInstruction.__subclasses__():
    subclass = subclass()
    url = f"/instructions/{subclass.dataset_name}"
    app.add_url_rule(url, f"{subclass.dataset_name}", subclass.get_instruction)

# Should contain swagger like structure
# E.g.http://localhost:5000/
@cross_origin()
@app.route("/")
def index():
    return "This is the backend for the dsc project"


# E.g. http://localhost:5000/sdg/preview/region=Africa&gender=male
@cross_origin()
@app.route("/sdg/preview/region=<string:region>&gender=<string:gender>")
def sdg_linear_regression_preview(region, gender):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"

    # File name is false if a file with the same name already exists.
    file_name = generate_file_name("sdg_linear_regression", region, gender)
    if not file_name_exists(file_name):
        sdg_linear_regression(region, gender, preview=True, file_name=file_name)
    try:
        return send_file(f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}")
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)


# E.g. http://localhost:5000/sdg/template/region=Africa&gender=male
@cross_origin()
@app.route("/sdg/template/region=<string:region>&gender=<string:gender>")
def sdg_linear_regression_template(region, gender):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"
    try:
        img = sdg_linear_regression(region, gender, preview=False)
        return render_template_string(img)
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)


if __name__ == "__main__":
    os.environ["DEBUG"] = "True"
    app.run(host="127.0.0.1", debug=True)
