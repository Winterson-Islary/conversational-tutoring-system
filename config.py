from pathlib import Path

import yaml


def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


config = load_config("config.yaml")
