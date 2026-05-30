import joblib
import pandas as pd
from pathlib import Path

from src.utils.logging import logs
from src.utils.configs import load_configs

logger = logs()
config = load_configs()

features = config["features"]
_model = None


def _load_model():
    global _model
    model_path = config["artifacts"]["models"]["best_model"]
    if not Path(model_path).exists():
        raise FileNotFoundError("модель не найдена")
    _model = joblib.load(model_path)
    logger.info("модель загружена")


def predict(data) -> dict:
    _load_model()
    if isinstance(data, dict):
        df = pd.DataFrame([data])
    else:
        df = data.copy()
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
        errors="ignore",
    )
    all_possible_columns = [
        "stops",
        "class",
        "duration",
        "days_left",
        "airline_Air_India",
        "airline_GO_FIRST",
        "airline_Indigo",
        "airline_SpiceJet",
        "airline_Vistara",
        "airline_AirAsia",
        "source_city_Chennai",
        "source_city_Delhi",
        "source_city_Hyderabad",
        "source_city_Kolkata",
        "source_city_Mumbai",
        "source_city_Bangalore",
        "destination_city_Chennai",
        "destination_city_Delhi",
        "destination_city_Hyderabad",
        "destination_city_Kolkata",
        "destination_city_Mumbai",
        "destination_city_Bangalore",
        "departure_time_Early_Morning",
        "departure_time_Evening",
        "departure_time_Late_Night",
        "departure_time_Morning",
        "departure_time_Night",
        "departure_time_Afternoon",
        "arrival_time_Early_Morning",
        "arrival_time_Evening",
        "arrival_time_Late_Night",
        "arrival_time_Morning",
        "arrival_time_Night",
        "arrival_time_Afternoon",
    ]

    for col in all_possible_columns:
        if col not in df.columns:
            df[col] = 0

    if hasattr(_model, "feature_names_in_"):
        expected_features = list(_model.feature_names_in_)
    else:
        expected_features = all_possible_columns

    missing_features = set(expected_features) - set(df.columns)
    if missing_features:
        logger.warning(f"Отсутствуют колонки: {missing_features}")
        for col in missing_features:
            df[col] = 0

    df = df[expected_features]

    X = df[features]
    price = int(_model.predict(X)[0])
    logger.info(f"предсказание: {price}")
    return {"pred_price": price}
