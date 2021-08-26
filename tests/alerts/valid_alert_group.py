import json
import os
from copy import deepcopy
from pathlib import Path

JSON_DIR = os.path.join(Path(__file__).resolve().parent)


def get_valid_alertgroup():
    with open(os.path.join(JSON_DIR, "valid_alert_group.json")) as json_file:
        data = json.load(json_file)
        return deepcopy(data)
