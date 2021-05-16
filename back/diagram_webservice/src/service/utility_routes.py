import json

from utils.aliases import DATASETS
from connection.redis_connection import make_redis_pool

# Routes are defined through the DATASETS constant in aliases.

make_redis_pool().set("datasets", json.dumps(list(DATASETS.keys())))


def available_datasets_route():
    """A route for retrieving current available datasets

    :return: Bytes object extracted from redis database
    :rtype: Bytes
    """
    return make_redis_pool().get("datasets")
