import json
from abc import ABC

from connection.redis_connection import make_redis_pool


class AbstractInstruction(ABC):
    """Instructions for what the frontend must display. Stored with redis"""

    dataset_name = ""
    models = ""
    headers = ""
    dataset_link = ""

    def set_instruction(self):
        """Converts object variables into json format and stores it on redis database"""
        dataset_format = {}
        dataset_format["models"] = self.models
        dataset_format["header_enums"] = self.header_enums
        dataset_format["dataset_link"] = self.dataset_link

        JSON = json.dumps(dataset_format)
        make_redis_pool().set(self.dataset_name, JSON)

    def get_instruction(self):
        """Retrieves instruction from redis. Uses the object's dataset name

        :return: Bytes containing the json string
        :rtype: Bytes
        """        
        return make_redis_pool().get(self.dataset_name)
