import json
import joblib
import sys
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error,
    r2_score,
)
from xgboost import XGBRegressor

from src.utils.logging import logs
from src.utils.configs import load_configs

logger = logs()
config = load_configs()
data_path = config["data"]["processed_path"]
features = config["features"]
target = config["data"]["target_column"]


def split_features_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    X = df[features]
    y = df[target]
    return X, y


def score(y_test, y_pred, y_prob=None):
    metrics = {
        "MAE": round(mean_absolute_error(y_test, y_pred), 4),
        "MSE": round(mean_squared_error(y_test, y_pred), 4),
        "RMSE": round(root_mean_squared_error(y_test, y_pred), 4),
        "R2": round(r2_score(y_test, y_pred), 4),
    }

    return metrics


def train_model(data_path: Path) -> None:
    df = pd.read_csv(data_path)
    X, y = split_features_target(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=config["data"]["test_size"],
        random_state=config["data"]["random_state"],
    )

    xg_conf = config["models"]["xgboost"]

    xgb_reg = XGBRegressor(
        n_estimators=xg_conf["n_estimators"],
        max_depth=xg_conf["max_depth"],
        learning_rate=xg_conf["learning_rate"],
        random_state=xg_conf["random_state"],
    )
    xgb_reg.fit(X_train, y_train)
    xgb_reg_pred = xgb_reg.predict(X_test)
    xgb_reg_metrics = score(y_test, xgb_reg_pred)

    logger.info(f"metrics: {xgb_reg_metrics}")

    joblib.dump(xgb_reg, config["artifacts"]["models"]["best_model"])
    logger.info("модель сохранена")
    with open(
        config["artifacts"]["metrics"]["best_model_metrics"], "w", encoding="utf-8"
    ) as f:
        json.dump(xgb_reg_metrics, f, indent=4)
