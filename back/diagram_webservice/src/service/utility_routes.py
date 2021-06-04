import json

from utils.aliases import DATASETS
# Routes are defined through the DATASETS constant in aliases.

KEYS_STR = ""
KEYS = list(DATASETS.keys())
for char in str(KEYS):
    if char == "'":
        KEYS_STR += "\""
    else:
        KEYS_STR += char


def available_datasets_route():
    """A route for retrieving current available datasets

    :return: Dictionary with keys
    :rtype: Dict
    """
    return KEYS_STR
