from pathlib import Path

import yaml
from dotenv import load_dotenv

from app.models.config import Config


load_dotenv()


CONFIG_PATH = (
    Path(__file__)
    .parent
    / "config.yaml"
)


def load_config() -> Config:

    with open(CONFIG_PATH, "r", encoding="utf-8") as file:

        data = yaml.safe_load(file)

    return Config(**data)