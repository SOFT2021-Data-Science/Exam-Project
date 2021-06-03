from .abstract_instructions import AbstractInstruction
from .param import Param
from .model import Model
from logic.sdg import sdg_get_list_of_all_values_in_row_by_column_name
from pprint import pprint
import json

regions = sdg_get_list_of_all_values_in_row_by_column_name("WHO region")
genders = [
    gender.lower() for gender in sdg_get_list_of_all_values_in_row_by_column_name("sex")
]


class SDGInstruction(AbstractInstruction):
    """Instructions for the SDG dataset. Implements AbstractInstruction

    :param AbstractInstruction: Instructions for what the frontend must display. Stored with redis
    :type AbstractInstruction: ABC
    """

    def __init__(self):
        linear_regression_params = {
            "region": Param(regions, "enum").as_json(),
            "gender": Param(genders, "enum").as_json(),
        }

        kmeans_clustering_params = {
            "region": Param(regions, "enum").as_json(),
            "gender": Param(genders, "enum").as_json(),
            "clusters": Param([1,2,3,4,5,6,7,8,9,10], "range").as_json(),
        }

        kmeans_elbow_params = {
            "region": Param(regions, "enum").as_json(),
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

        self.dataset_name = "sdg"
        self.models = [
            linear_regression_model,
            kmeans_clustering_model,
            kmeans_elbow_model,
        ]
        self.dataset_link = (
            "https://apps.who.int/gho/data/view.sdg.3-4-data-reg?lang=en"
        )
        self.description = "The SDG dataset is compiled by the WHO organization"
        super().set_instruction()
