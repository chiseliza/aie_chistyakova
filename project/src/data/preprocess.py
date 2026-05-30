import pandas as pd
import numpy as np
from pathlib import Path

from src.utils.logging import logs
from src.utils.configs import load_configs

logger = logs()
configs = load_configs()

features = configs["features"]
target = configs["data"]["target_column"]


def data_preprocess(raw_path: Path, proc_path: Path) -> None:
    df = pd.read_csv(raw_path)
    df = df[df["duration"] <= 30]
    logger.info("Успешное удаление выбросов")

    df["stops"] = (
        df["stops"].replace({"zero": 0, "one": 1, "two_or_more": 2}).astype(int)
    )
    df["class"] = df["class"].replace({"Economy": 0, "Business": 1}).astype(int)

    dummies_variables = [
        "airline",
        "source_city",
        "destination_city",
        "departure_time",
        "arrival_time",
    ]
    dummies = pd.get_dummies(df[dummies_variables], drop_first=False)
    df = pd.concat([df, dummies], axis=1)

    df = df.drop(
        [
            "Unnamed: 0",
            "flight",
            "airline",
            "source_city",
            "destination_city",
            "departure_time",
            "arrival_time",
        ],
        axis=1,
    )

    logger.info(f"Успешно изменены признаки")

    out = Path(proc_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    logger.info("Предобработанный датасет сохранен")
