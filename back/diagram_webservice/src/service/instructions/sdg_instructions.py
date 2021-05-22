from .abstract_instructions import AbstractInstruction
from .param import Param


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
                    "region": Param(["Africa", "Europe"], "enum").as_json(),
                    "gender": Param(["male", "female", "both"], "enum").as_json(),
                }
            }
        }
        self.dataset_link = (
            "https://apps.who.int/gho/data/view.sdg.3-4-data-reg?lang=en"
        )
        self.description = "Insert description here"
        super().set_instruction()
