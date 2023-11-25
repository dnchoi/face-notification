import json
from libs.logger import Logger
import os

logger = Logger(
    class_name=os.path.basename(__file__).split(".")[0],
    file_path="logs",
).logger

def read_config(config):
    cfg = None
    try:
        with open(config, "r") as f:
            cfg = json.load(f)

        return cfg
    except Exception as e:
        logger.error(f"Error in function {__name__}: {str(e)}")
