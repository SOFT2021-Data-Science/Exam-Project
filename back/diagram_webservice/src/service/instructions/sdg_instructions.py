from .abstract_instructions import AbstractInstruction
from .param import Param
from logic.sdg import sdg_get_list_of_all_values_in_row_by_column_name

regions = sdg_get_list_of_all_values_in_row_by_column_name("WHO region")
genders = sdg_get_list_of_all_values_in_row_by_column_name("sex")

class SDGInstruction(AbstractInstruction):
    """Instructions for the SDG dataset. Implements AbstractInstruction

    :param AbstractInstruction: Instructions for what the frontend must display. Stored with redis
    :type AbstractInstruction: ABC
    """

    def __init__(self):
        self.dataset_name = "sdg"
        self.models = {
            "linear_regression": {
                "params": {
                    "regions": Param(regions, "enum").as_json(),
                    "gender": Param(genders, "enum").as_json(),
                    "date_range": Param([2000, 2019], "range").as_json(),
                }
            },
            "kmeans/clustering":{
                "params": {
                    "regions": Param(regions, "enum").as_json(),
                    "gender": Param(genders, "enum").as_json(),
                    "clusters": Param([1, 10], "range").as_json(),
                }
            },
            "kmeans/elbow":{
                "params": {
                    "regions": Param(regions, "enum").as_json(),
                    "gender": Param(genders, "enum").as_json(),
                    "clusters": Param([1, 10], "range").as_json(),
                }
            }
        }
        self.dataset_link = (
            "https://apps.who.int/gho/data/view.sdg.3-4-data-reg?lang=en"
        )
        self.description = "Insert description here"
        super().set_instruction()
