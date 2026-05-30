import pandas as pd
import logging
from pathlib import Path
from typing import Optional, Union
import urllib.request

from src.utils.logging import logs

logger = logs()


def download_csv(url: str, path_to: Path) -> None:
    path = Path(path_to)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        logger.info("Файл уже существует", path)
        return

    try:
        urllib.request.urlretrieve(url, path)
        logger.info("Скачивание успешно")
    except urllib.error.URLError:
        logger.exception("Не удалось скачать датасет")
        raise
