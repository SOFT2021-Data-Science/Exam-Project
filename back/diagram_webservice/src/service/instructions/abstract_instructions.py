import json
from abc import ABC


class AbstractInstruction(ABC):
    """Instructions for what the frontend must display. Stored with redis"""

    dataset_name = ""
    models = ""
    headers = ""
    dataset_link = ""
    description = ""
    dataset_format = {}
    json_obj = None

    def set_instruction(self):
        """Converts object variables into json format and stores it on redis database"""
        self.dataset_format["models"] = self.models
        self.dataset_format["dataset_link"] = self.dataset_link
        self.dataset_format["description"] = self.description

        self.json_obj = json.dumps(self.dataset_format)
        

    def get_instruction(self):
        """Retrieves instruction from redis. Uses the object's dataset name

        :return: Bytes containing the json string
        :rtype: Bytes
        """
        
        return self.json_obj
