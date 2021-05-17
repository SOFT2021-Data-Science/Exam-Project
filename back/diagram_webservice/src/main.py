from flask import Flask, json, render_template_string, send_file, jsonify
from flask_cors import CORS, cross_origin
import os

from utils.aliases import OUT_DIR
from utils.misc import check_debug
from utils.file_handling import generate_file_name, IMAGE_FORMAT, file_name_exists
from logic.sdg import sdg_linear_regression
from logic.sdg import sdg_kmeans_cluster
from logic.sdg import sdg_kmeans_elbow
from logic.sdg import sdg_get_list_of_all_values_in_row_by_column_name

from logic.kaggle import kaggle_linear_regression
from logic.kaggle import kaggle_kmeans_cluster
from logic.kaggle import kaggle_kmeans_elbow
from logic.kaggle import kaggle_get_list_of_all_values_in_row_by_column_name

from utils.logging import create_and_updatelog


app = Flask(__name__)
CORS(app)
app.config["CORS_HEADERS"] = "*"


# Should contain swagger like structure
# E.g.http://localhost:5000/
@cross_origin()
@app.route("/")
def index():
    return "Hello World!"


# E.g. http://localhost:5000/sdg/row_values=who%20region
@app.route("/sdg/row_values=<string:row_values>")
def sdg_row_values(row_values):
    return jsonify(sdg_get_list_of_all_values_in_row_by_column_name(row_values))

# E.g. http://localhost:5000/sdg/linearregression/preview/region=Africa&gender=male
@cross_origin()
@app.route("/sdg/linearregression/preview/region=<string:region>&gender=<string:gender>")
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


# E.g. http://localhost:5000/sdg/linearregression/template/region=Africa&gender=male
@cross_origin()
@app.route("/sdg/linearregression/template/region=<string:region>&gender=<string:gender>")
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
        
   
# E.g. http://localhost:5000/sdg/kmeans/clustering/preview/region=Africa&gender=male&clusters=2
@cross_origin()
@app.route("/sdg/kmeans/clustering/preview/region=<string:region>&gender=<string:gender>&clusters=<int:clusters>")
def sdg_kmeans_clustering_preview(region, gender, clusters):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"

        # File name is false if a file with the same name already exists.
    file_name = generate_file_name("sdg_kmeans_clustering", region, gender, clusters)
    if not file_name_exists(file_name):
        sdg_kmeans_cluster(region, gender, clusters, preview=True, file_name=file_name)
    try:
        return send_file(f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}")
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)


# E.g. http://localhost:5000/sdg/kmeans/clustering/template/region=Africa&gender=male&clusters=2
@cross_origin()
@app.route("/sdg/kmeans/clustering/template/region=<string:region>&gender=<string:gender>&clusters=<int:clusters>")
def sdg_kmeans_clustering_template(region, gender, clusters):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"

    try:
        img = sdg_kmeans_cluster(region, gender, clusters, preview=False)
        return render_template_string(img)
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)


# E.g. http://localhost:5000/sdg/kmeans/elbow/preview/region=Africa&gender=male&clusters=5
@cross_origin()
@app.route("/sdg/kmeans/elbow/preview/region=<string:region>&gender=<string:gender>&clusters=<int:clusters>")
def sdg_kmeans_elbow_preview(region, gender, clusters):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"
    if clusters <= 1:
        create_and_updatelog("400")
        return "Max can not be less or equal to 1"

    # File name is false if a file with the same name already exists.
    file_name = generate_file_name("sdg_kmeans_elbow", region, gender, clusters)
    if not file_name_exists(file_name):
        sdg_kmeans_elbow(region, gender, clusters, preview=True, file_name=file_name)
    try:
        return send_file(f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}")
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)


# E.g. http://localhost:5000/sdg/kmeans/elbow/template/regio    n=Africa&gender=male&clusters=5
@cross_origin()
@app.route("/sdg/kmeans/elbow/template/region=<string:region>&gender=<string:gender>&clusters=<int:clusters>")
def sdg_kmeans_elbow_template(region, gender, clusters):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"
    if clusters <= 1:
        create_and_updatelog("400")
        return "Max can not be less or equal to 1"

    try:
        img = sdg_kmeans_elbow(region, gender, clusters, preview=False)
        return render_template_string(img)
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)



# ---- Kaggle ----- #

# E.g. http://localhost:5000/kaggle/row_values=country
@app.route("/kaggle/row_values=<string:row_values>")
def kaggle_row_values(row_values):
    return jsonify(kaggle_get_list_of_all_values_in_row_by_column_name(row_values))


# E.g. http://localhost:5000/kaggle/linearregression/preview/region=United_States&gender=male
@cross_origin()
@app.route("/kaggle/linearregression/preview/region=<string:region>&gender=<string:gender>")
def kaggle_linear_regression_preview(region, gender):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"

        # File name is false if a file with the same name already exists.
    file_name = generate_file_name("kaggle_linear_regression", region, gender)
    if not file_name_exists(file_name):
        kaggle_linear_regression(region, gender, preview=True, file_name=file_name)
    try:
        return send_file(f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}")
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)


# E.g. http://localhost:5000/kaggle/linearregression/template/region=United_States&gender=male
@cross_origin()
@app.route("/kaggle/linearregression/template/region=<string:region>&gender=<string:gender>")
def kaggle_linear_regression_template(region, gender):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"

    try:
        img = kaggle_linear_regression(region, gender, preview=False)
        return render_template_string(img)
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)


# E.g. http://localhost:5000/kaggle/kmeans/clustering/preview/region=United_States&gender=male&clusters=2
@cross_origin()
@app.route("/kaggle/kmeans/clustering/preview/region=<string:region>&gender=<string:gender>&clusters=<int:clusters>")
def kaggle_kmeans_clustering_preview(region, gender, clusters):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"

        # File name is false if a file with the same name already exists.
    file_name = generate_file_name("kaggle_kmeans_clustering", region, gender, clusters)
    if not file_name_exists(file_name):
        kaggle_kmeans_cluster(region, gender, clusters, preview=True, file_name=file_name)
    try:
        return send_file(f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}")
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)


# E.g. http://localhost:5000/kaggle/kmeans/clustering/template/region=United_States&gender=male&clusters=2
@cross_origin()
@app.route("/kaggle/kmeans/clustering/template/region=<string:region>&gender=<string:gender>&clusters=<int:clusters>")
def kaggle_kmeans_clustering_template(region, gender, clusters):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"

    try:
        img = kaggle_kmeans_cluster(region, gender, clusters, preview=False)
        return render_template_string(img)
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)


# E.g. http://localhost:5000/kaggle/kmeans/elbow/preview/region=United_States&gender=male&clusters=5
@cross_origin()
@app.route("/kaggle/kmeans/elbow/preview/region=<string:region>&gender=<string:gender>&clusters=<int:clusters>")
def kaggle_kmeans_elbow_preview(region, gender, clusters):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"
    if clusters <= 1:
        create_and_updatelog("400")
        return "Max can not be less or equal to 1"

    # File name is false if a file with the same name already exists.
    file_name = generate_file_name("kaggle_kmeans_elbow", region, gender, clusters)
    if not file_name_exists(file_name):
        kaggle_kmeans_elbow(region, gender, clusters, preview=True, file_name=file_name)
    try:
        return send_file(f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}")
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)


# E.g. http://localhost:5000/kaggle/kmeans/elbow/template/region=United_States&gender=male&clusters=5
@cross_origin()
@app.route("/kaggle/kmeans/elbow/template/region=<string:region>&gender=<string:gender>&clusters=<int:clusters>")
def kaggle_kmeans_elbow_template(region, gender, clusters):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"
    if clusters <= 1:
        create_and_updatelog("400")
        return "Max can not be less or equal to 1"

    try:
        img = kaggle_kmeans_elbow(region, gender, clusters, preview=False)
        return render_template_string(img)
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)




if __name__ == "__main__":
    os.environ["DEBUG"] = "True"
    app.run(host="127.0.0.1", debug=True)
