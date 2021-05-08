from flask import Flask, render_template, render_template_string
from flask_cors import CORS, cross_origin
from utils.aliases import RESOURCES_DIR
from logic.basic import basic_sdg
from logic.mpld3_check import mpld3_check
import os

app = Flask(__name__)
#cors = CORS(app)
#app.config["CORS_HEADERS"] = "*"


#@cross_origin()
@app.route("/")
def index():
    return "This is the backend for the dsc project"

#@cross_origin()
@app.route("/mpld3check")
def mpld3_check_stuff():
    mpld3_check()
    return "ok"


# E.g. http://localhost:5000/basic/2002&2012
#@cross_origin()
@app.route("/basic/<int:min>&<int:max>")
def sdg_basic_route(min, max):
    if min > max:
        return "400 - Minimum value is larger than max"
    try:
        img = basic_sdg(min, max)
        return render_template_string(img)
        #return img
        #return {"msg":"ok"}
    except Exception as e:
        if bool(os.getenv("DEBUG")):
            return f"500 - {e}"
        return 500


if __name__ == "__main__":
    os.environ["DEBUG"] = "True"
    app.run(host="127.0.0.1", debug=True)
