from .abstract_instructions import AbstractInstruction
from .param import Param


class KaggleInstruction(AbstractInstruction):
    """Instructions for the Kaggle dataset. Implements AbstractInstruction

    :param AbstractInstruction: Instructions for what the frontend must display. Stored with redis
    :type AbstractInstruction: ABC
    """

    def __init__(self):
        self.dataset_name = "kaggle"
        self.models = {
            "linear_regression": {
                "params": {
                    "regions": Param(["Africa", "Europe"], "enum").as_json(),
                    "gender": Param(["male", "female", "both"], "enum").as_json(),
                    "date_range": Param([2000, 2019], "range").as_json(),
                }
            }
        }
        self.dataset_link = (
            "https://apps.who.int/gho/data/view.sdg.3-4-data-reg?lang=en"
        )
        self.description = "Insert description here"
        super().set_instruction()
