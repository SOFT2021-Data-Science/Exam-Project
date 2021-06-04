from re import sub
from flask import Flask, render_template_string, send_file
from flask import Flask, json, render_template_string, send_file, jsonify
from flask_cors import CORS, cross_origin
import os

from utils.aliases import OUT_DIR
from utils.misc import check_debug
from utils.logging import create_and_updatelog
from utils.file_handling import generate_file_name, IMAGE_FORMAT, file_name_exists
from logic.sdg import sdg_linear_regression
from service.instructions.abstract_instructions import AbstractInstruction
from service.utility_routes import *

from logic.sdg import sdg_kmeans_cluster, sdg_kmeans_elbow, sdg_get_list_of_all_values_in_row_by_column_name, sdg_polynomial_regression, sdg_compare_male_female_from_region, sdg_compare_suicide_rates_for_gender_between_two_regions

from logic.kaggle import kaggle_linear_regression, kaggle_kmeans_cluster, kaggle_kmeans_elbow, kaggle_get_list_of_all_values_in_row_by_column_name, kaggle_polynomial_regression, kaggle_compare_male_female_from_country, kaggle_compare_suicide_rates_for_gender_between_two_countries

from utils.logging import create_and_updatelog


app = Flask(__name__)
CORS(app)
app.config["CORS_HEADERS"] = "*"

INSTRUCTIONS_BASE_PATH = "/instructions"


for subclass in AbstractInstruction.__subclasses__():
    subclass = subclass()
    url = f"{INSTRUCTIONS_BASE_PATH}/{subclass.dataset_name}"
    app.add_url_rule(url, f"{subclass.dataset_name}", subclass.get_instruction)

app.add_url_rule(
    f"{INSTRUCTIONS_BASE_PATH}/available_datasets",
    "available_datasets",
    available_datasets_route,
)

# Should contain swagger like structure
# E.g.http://localhost:5000/
@cross_origin()
@app.route("/")
def index():
    return "This is the backend for the dsc suicide project"


# E.g. http://localhost:5000/sdg/row_values=who%20region
@app.route("/sdg/row_values=<string:row_values>")
def sdg_row_values(row_values):
    return jsonify(sdg_get_list_of_all_values_in_row_by_column_name(row_values))




# E.g. http://localhost:5000/sdg/linear_regression/preview/region=Africa&gender=male
@cross_origin()
@app.route("/sdg/linear_regression/preview/region=<string:region>&gender=<string:gender>")
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


# E.g. http://localhost:5000/sdg/linear_regression/template/region=Africa&gender=male
@cross_origin()
@app.route("/sdg/linear_regression/template/region=<string:region>&gender=<string:gender>")
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


# E.g. http://localhost:5000/sdg/kmeans/elbow/template/region=Africa&gender=male&clusters=5
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

# E.g . http://localhost:5000/sdg/polynomial_regression/preview/region=Europe&gender=male&degrees=2&future_years=5
@cross_origin()
@app.route("/sdg/polynomial_regression/preview/region=<string:region>&gender=<string:gender>&degrees=<int:degrees>&future_years=<int:future_years>")
def sdg_polynomial_regression_preview(region, gender, degrees, future_years):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"

        # File name is false if a file with the same name already exists.
    file_name = generate_file_name("sdg_polynomial_regression", region, gender, degrees, future_years)
    if not file_name_exists(file_name):
        sdg_polynomial_regression(region, gender, degrees, future_years, preview=True, file_name=file_name)
    try:
        return send_file(f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}")
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)

# E.g. http://localhost:5000/sdg/polynomial_regression/template/region=Europe&gender=male&degrees=2&future_years=5
@cross_origin()
@app.route("/sdg/polynomial_regression/template/region=<string:region>&gender=<string:gender>&degrees=<int:degrees>&future_years=<int:future_years>")
def sdg_polynomial_regression_template(region, gender, degrees, future_years):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"

    try:
        img = sdg_polynomial_regression(region, gender, degrees, future_years, preview=False)
        return render_template_string(img)
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)

# E.g. http://localhost:5000/sdg/compare/region_comparison_genders/preview/region=Europe
@cross_origin()
@app.route("/sdg/compare/region_comparison_genders/preview/region=<string:region>")
def sdg_compare_region_male_female_preview(region):
    # File name is false if a file with the same name already exists.
    file_name = generate_file_name("sdg_compare_region_male_female", region)
    if not file_name_exists(file_name):
        sdg_compare_male_female_from_region(region, preview=True, file_name=file_name)
    try:
        return send_file(f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}")
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)

# E.g. http://localhost:5000/sdg/compare/region_comparison_genders/template/region=Europe
@cross_origin()
@app.route("/sdg/compare/region_comparison_genders/template/region=<string:region>")
def sdg_compare_region_male_female_template(region):
    try:
        img = sdg_compare_male_female_from_region(region, preview=False)
        return render_template_string(img)
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)

# E.g.  http://localhost:5000/sdg/compare/regions_comparison/preview/region_1=Europe&region_2=Africa&gender=male
@cross_origin()
@app.route("/sdg/compare/regions_comparison/preview/region_1=<string:region_1>&region_2=<string:region_2>&gender=<string:gender>")
def sdg_compare_suicide_rates_for_gender_between_two_regions_preview(region_1, region_2, gender):
    # File name is false if a file with the same name already exists.
    file_name = generate_file_name("sdg_compare_suicide_rates_for_gender_between_two_regions", region_1, region_2, gender)
    if not file_name_exists(file_name):
        sdg_compare_suicide_rates_for_gender_between_two_regions(region_1, region_2, gender, preview=True, file_name=file_name)
    try:
        return send_file(f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}")
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)

# E.g. http://localhost:5000/sdg/compare/regions_comparison/template/region_1=Europe&region_2=Africa&gender=male
@cross_origin()
@app.route("/sdg/compare/regions_comparison/template/region_1=<string:region_1>&region_2=<string:region_2>&gender=<string:gender>")
def sdg_compare_suicide_rates_for_gender_between_two_regions_template(region_1, region_2, gender):
    try:
        img = sdg_compare_suicide_rates_for_gender_between_two_regions(region_1, region_2, gender, preview=False)
        return render_template_string(img)
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)



# ---- Kaggle ----- #

# E.g. http://localhost:5000/kaggle/row_values=country
@app.route("/kaggle/row_values=<string:row_values>")
def kaggle_row_values(row_values):
    return jsonify(kaggle_get_list_of_all_values_in_row_by_column_name(row_values))


# E.g. http://localhost:5000/kaggle/linear_regression/preview/country=United_States&gender=male
@cross_origin()
@app.route("/kaggle/linear_regression/preview/country=<string:country>&gender=<string:gender>")
def kaggle_linear_regression_preview(country, gender):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"

        # File name is false if a file with the same name already exists.
    file_name = generate_file_name("kaggle_linear_regression", country, gender)
    if not file_name_exists(file_name):
        kaggle_linear_regression(country, gender, preview=True, file_name=file_name)
    try:
        return send_file(f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}")
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)


# E.g. http://localhost:5000/kaggle/linear_regression/template/country=United_States&gender=male
@cross_origin()
@app.route("/kaggle/linear_regression/template/country=<string:country>&gender=<string:gender>")
def kaggle_linear_regression_template(country, gender):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"

    try:
        img = kaggle_linear_regression(country, gender, preview=False)
        return render_template_string(img)
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)

# E.g. http://localhost:5000/kaggle/polynomial_regression/preview/country=United_States&gender=male&degrees=2&future_years=5
@cross_origin()
@app.route("/kaggle/polynomial_regression/preview/country=<string:country>&gender=<string:gender>&degrees=<int:degrees>&future_years=<int:future_years>")
def kaggle_polynomial_regression_preview(country, gender, degrees, future_years):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"

        # File name is false if a file with the same name already exists.
    file_name = generate_file_name("kaggle_polynomial_regression", country, gender, degrees, future_years)
    if not file_name_exists(file_name):
        kaggle_polynomial_regression(country, gender, degrees, future_years, preview=True, file_name=file_name)
    try:
        return send_file(f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}")
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)

# E.g. http://localhost:5000/kaggle/polynomial_regression/template/country=United_States&gender=male&degrees=2&future_years=5
@cross_origin()
@app.route("/kaggle/polynomial_regression/template/country=<string:country>&gender=<string:gender>&degrees=<int:degrees>&future_years=<int:future_years>")
def kaggle_polynomial_regression_template(country, gender, degrees, future_years):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"

    try:
        img = kaggle_polynomial_regression(country, gender, degrees, future_years, preview=False)
        return render_template_string(img)
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)


# E.g. http://localhost:5000/kaggle/kmeans/clustering/preview/country=United_States&gender=male&clusters=2
@cross_origin()
@app.route("/kaggle/kmeans/clustering/preview/country=<string:country>&gender=<string:gender>&clusters=<int:clusters>")
def kaggle_kmeans_clustering_preview(country, gender, clusters):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"

        # File name is false if a file with the same name already exists.
    file_name = generate_file_name("kaggle_kmeans_clustering", country, gender, clusters)
    if not file_name_exists(file_name):
        kaggle_kmeans_cluster(country, gender, clusters, preview=True, file_name=file_name)
    try:
        return send_file(f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}")
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)


# E.g. http://localhost:5000/kaggle/kmeans/clustering/template/country=United_States&gender=male&clusters=2
@cross_origin()
@app.route("/kaggle/kmeans/clustering/template/country=<string:country>&gender=<string:gender>&clusters=<int:clusters>")
def kaggle_kmeans_clustering_template(country, gender, clusters):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"

    try:
        img = kaggle_kmeans_cluster(country, gender, clusters, preview=False)
        return render_template_string(img)
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)


# E.g. http://localhost:5000/kaggle/kmeans/elbow/preview/country=United_States&gender=male&clusters=5
@cross_origin()
@app.route("/kaggle/kmeans/elbow/preview/country=<string:country>&gender=<string:gender>&clusters=<int:clusters>")
def kaggle_kmeans_elbow_preview(country, gender, clusters):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"
    if clusters <= 1:
        create_and_updatelog("400")
        return "Max can not be less or equal to 1"

    # File name is false if a file with the same name already exists.
    file_name = generate_file_name("kaggle_kmeans_elbow", country, gender, clusters)
    if not file_name_exists(file_name):
        kaggle_kmeans_elbow(country, gender, clusters, preview=True, file_name=file_name)
    try:
        return send_file(f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}")
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)


# E.g. http://localhost:5000/kaggle/kmeans/elbow/template/country=United_States&gender=male&clusters=5
@cross_origin()
@app.route("/kaggle/kmeans/elbow/template/country=<string:country>&gender=<string:gender>&clusters=<int:clusters>")
def kaggle_kmeans_elbow_template(country, gender, clusters):
    if gender not in ["both", "male", "female"]:
        create_and_updatelog("400")
        return "400"
    if clusters <= 1:
        create_and_updatelog("400")
        return "Max can not be less or equal to 1"

    try:
        img = kaggle_kmeans_elbow(country, gender, clusters, preview=False)
        return render_template_string(img)
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)

# E.g. http://localhost:5000/kaggle/compare/country_comparison_genders/preview/country=Denmark
@cross_origin()
@app.route("/kaggle/compare/country_comparison_genders/preview/country=<string:country>")
def kaggle_compare_country_male_female_preview(country):
    # File name is false if a file with the same name already exists.
    file_name = generate_file_name("kaggle_compare_country_male_female", country)
    if not file_name_exists(file_name):
        kaggle_compare_male_female_from_country(country, preview=True, file_name=file_name)
    try:
        return send_file(f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}")
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)

# E.g. http://localhost:5000/kaggle/compare/country_comparison_genders/template/country=Denmark
@cross_origin()
@app.route("/kaggle/compare/country_comparison_genders/template/country=<string:country>")
def kaggle_compare_country_male_female_template(country):
    try:
        img = kaggle_compare_male_female_from_country(country, preview=False)
        return render_template_string(img)
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)

# E.g. http://localhost:5000/kaggle/compare/countries_comparison/preview/country_1=Denmark&country_2=Sweden&gender=male
@cross_origin()
@app.route("/kaggle/compare/countries_comparison/preview/country_1=<string:country_1>&country_2=<string:country_2>&gender=<string:gender>")
def kaggle_compare_suicide_rates_for_gender_between_two_countries_preview(country_1, country_2, gender):
    # File name is false if a file with the same name already exists.
    file_name = generate_file_name("kaggle_compare_suicide_rates_for_gender_between_two_countries", country_1, country_2, gender)
    if not file_name_exists(file_name):
        kaggle_compare_suicide_rates_for_gender_between_two_countries(country_1, country_2, gender, preview=True, file_name=file_name)
    try:
        return send_file(f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}")
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)

# E.g. http://localhost:5000/kaggle/compare/countries_comparison/template/country_1=Denmark&country_2=Sweden&gender=male
@cross_origin()
@app.route("/kaggle/compare/countries_comparison/template/country_1=<string:country_1>&country_2=<string:country_2>&gender=<string:gender>")
def kaggle_compare_suicide_rates_for_gender_between_two_countries_template(country_1, country_2, gender):
    try:
        img = kaggle_compare_suicide_rates_for_gender_between_two_countries(country_1, country_2, gender, preview=False)
        return render_template_string(img)
    except Exception as e:
        check_debug(e)
        create_and_updatelog(e)



if __name__ == "__main__":
    os.environ["DEBUG"] = "True"
    app.run(host="127.0.0.1", debug=True)
