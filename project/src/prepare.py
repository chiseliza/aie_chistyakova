from src.data.download import download_csv

from src.data.preprocess import data_preprocess
from src.utils.configs import load_configs
from src.utils.logging import logs
from pathlib import Path
import pandas as pd
import logging

logger = logs()

config = load_configs()


def load_data() -> None:
    data_url = config["data"]["url"]
    processed_data_path = config["data"]["processed_path"]
    raw_path = config["data"]["raw_path"]
    download_csv(url=data_url, path_to=raw_path)
    data_preprocess(raw_path, processed_data_path)


if __name__ == "__main__":
    load_data()
    logger.info("Загрузка и подготовка данных окончены")
