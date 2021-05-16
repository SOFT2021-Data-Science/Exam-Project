import os

# This file is for specifying paths and environment variables

# Dynamic retrieval of resource path
# Split over several calls for readability

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(ROOT_DIR)

RESOURCES_DIR = os.path.dirname(ROOT_DIR)
RESOURCES_DIR = os.path.dirname(RESOURCES_DIR)
RESOURCES_DIR = os.path.dirname(RESOURCES_DIR) + "/resources"

LOGGING_DIR = os.path.dirname(ROOT_DIR) + "/log"
_DATASET_DIR = RESOURCES_DIR + "/datasets"
OUT_DIR = RESOURCES_DIR + "/out"

ENV_DEVELOPMENT_PATH = os.path.dirname(ROOT_DIR) + "/.env.development"

if not os.path.isdir(OUT_DIR):
    os.mkdir(OUT_DIR)

DATASETS = {"sdg": f"{_DATASET_DIR}/SDGSUICIDE,SDG_SH_STA_SCIDEN.csv"}
