from .abstract_instructions import AbstractInstruction
from .param import Param
from .model import Model
from logic.kaggle import kaggle_get_list_of_all_values_in_row_by_column_name

genders = [
    gender.lower()
    for gender in kaggle_get_list_of_all_values_in_row_by_column_name("sex")
]
country = kaggle_get_list_of_all_values_in_row_by_column_name("country")


class KaggleInstruction(AbstractInstruction):
    """Instructions for the Kaggle dataset. Implements AbstractInstruction

    :param AbstractInstruction: Instructions for what the frontend must display. Stored with redis
    :type AbstractInstruction: ABC
    """



    def __init__(self):
        linear_regression_params = {
            "country": Param(country, "enum").as_json(),
            "gender": Param(genders, "enum").as_json(),
        }
        kmeans_clustering_params = {
            "country": Param(country, "enum").as_json(),
            "gender": Param(genders, "enum").as_json(),
            "clusters": Param([1,2,3,4,5,6,7,8,9,10], "range").as_json(),
        }
        kmeans_elbow_params = {
            "country": Param(country, "enum").as_json(),
            "gender": Param(genders, "enum").as_json(),
            "clusters": Param([1,2,3,4,5,6,7,8,9,10], "range").as_json(),
        }

        linear_regression_model = Model(
            "linear_regression", linear_regression_params
        ).as_json()
        kmeans_clustering_model = Model(
            "kmeans/clustering", kmeans_clustering_params
        ).as_json()
        kmeans_elbow_model = Model("kmeans/elbow", kmeans_elbow_params).as_json()
        self.dataset_name = "kaggle"
        self.models = [linear_regression_model, kmeans_clustering_model, kmeans_elbow_model]
        self.dataset_link = (
            "https://apps.who.int/gho/data/view.sdg.3-4-data-reg?lang=en"
        )
        self.description = "Insert description here"
        super().set_instruction()
