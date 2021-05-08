import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(ROOT_DIR)

RESOURCES_DIR = os.path.dirname(ROOT_DIR)
RESOURCES_DIR = os.path.dirname(RESOURCES_DIR)
RESOURCES_DIR = os.path.dirname(RESOURCES_DIR) + "/resources"
_DATASET_DIR = RESOURCES_DIR + "/datasets"
OUT_DIR = RESOURCES_DIR + "/out"

if not os.path.isdir(OUT_DIR):
    os.mkdir(OUT_DIR)


DATASETS = {"sdg": f"{_DATASET_DIR}/SDGSUICIDE,SDG_SH_STA_SCIDEN.csv"}
