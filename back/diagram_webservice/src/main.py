from flask import Flask, render_template_string, send_file
from flask_cors import CORS, cross_origin
import os

from utils.aliases import OUT_DIR
from utils.misc import check_debug
from utils.file_handling import generate_file_name, IMAGE_FORMAT, file_name_exists
from logic.basic import basic_sdg
from logic.mpld3_check import mpld3_check

from utils.aliases import OUT_DIR
from utils.misc import check_debug
from utils.file_handling import generate_file_name, IMAGE_FORMAT
from logic.basic import basic_sdg
from logic.sdg_linear_regression import sdg_linear_regression
from logic.mpld3_check import mpld3_check


app = Flask(__name__)
CORS(app)
app.config["CORS_HEADERS"] = "*"


# Should contain swagger like structure
# E.g.http://localhost:5000/
@cross_origin()
@app.route("/")
def index():
    return "This is the backend for the dsc project"


# Just for testing
# E.g. http://localhost:5000/mpld3check
@cross_origin()
@app.route("/mpld3check")
def mpld3_check_stuff():
    mpld3_check()
    return "ok"


# Preview route. For sending image to frontend.
# E.g. http://localhost:5000/basic/preview/min=2002&max=2012
@cross_origin()
@app.route("/basic/preview/min=<int:min>&max=<int:max>")
def sdg_basic_route_preview(min, max):
    if min > max:
        return "400 - Minimum value is larger than max"
    try:
        # File name is false if a file with the same name already exists.

        file_name = generate_file_name("sdg_basic", region, gender)
        if not file_name_exists(file_name):
            basic_sdg(min, max, preview=True, file_name=file_name)
        try:
            return send_file(f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}")
        except Exception as e:
            return e
    except Exception as e:
        check_debug(e)


# Template route. Rendering mpld3 template string.
# E.g. http://localhost:5000/basic/template/min=2002&max=2012
@cross_origin()
@app.route("/basic/template/min=<int:min>&max=<int:max>")
def sdg_basic_route_template(min, max):
    if min > max:
        return "400 - Minimum value is larger than max"
    try:
        img = basic_sdg(min, max, preview=False)
        return render_template_string(img)
    except Exception as e:
        check_debug(e)


# E.g. http://localhost:5000/sdg/preview/region=Africa&gender=Male
@cross_origin()
@app.route("/sdg/preview/region=<string:region>&gender=<string:gender>")
def sdg_linear_regression_preview(region, gender):
    if gender not in ["both", "male", "female"]:
        return "400"
        # File name is false if a file with the same name already exists.
    file_name = generate_file_name("sdg_linear_regression", region, gender)
    if not file_name_exists(file_name):
        sdg_linear_regression(region, gender, preview=True, file_name=file_name)
    try:
        return send_file(f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}")
    except Exception as e:
        check_debug(e)


# E.g. http://localhost:5000/sdg/template/region=Africa&gender=Male
@cross_origin()
@app.route("/sdg/template/region=<string:region>&gender=<string:gender>")
def sdg_linear_regression_template(region, gender):
    if gender not in ["both", "male", "female"]:
        return "400"
    try:
        img = sdg_linear_regression(min, max, region, gender, preview=False)
        return render_template_string(img)
    except Exception as e:
        check_debug(e)


if __name__ == "__main__":
    os.environ["DEBUG"] = "True"
    app.run(host="127.0.0.1", debug=True)
