from .abstract_instructions import AbstractInstruction


class SDGInstruction(AbstractInstruction):
    """Instructions for the SDG dataset. Implements AbstractInstruction

    :param AbstractInstruction: Instructions for what the frontend must display. Stored with redis
    :type AbstractInstruction: ABC
    """

    def __init__(self):
        self.dataset_name = "sdg"
        self.models = {"linear_regression": {"params": ["region", "gender"]}}
        self.header_enums = {
            "gender_enums": ["male", "female", "both"],
            "region_enums": ["Africa", "Europe"],
            "date_range": [2000, 2019],
        }
        self.dataset_link = (
            "https://apps.who.int/gho/data/view.sdg.3-4-data-reg?lang=en"
        )
        super().set_instruction()