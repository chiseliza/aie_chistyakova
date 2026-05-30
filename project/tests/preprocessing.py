import pytest
import pandas as pd
import numpy as np
from src.data.preprocessing import DataPreprocessor


@pytest.fixture
def sample_data():
    """Фикстура с тестовыми данными."""
    return pd.DataFrame(
        {
            "Price": [10000000, 15000000, 8000000, 20000000, np.nan],
            "Area": [50, 75, 30, 100, 60],
            "Region": ["Moscow", "Moscow", "Region", "Moscow", "Region"],
            "Minutes_to_metro": [5, 10, 15, np.nan, 8],
            "Number_of_rooms": [1, 2, 1, 3, 2],
        }
    )


def test_preprocessor_handles_missing_values(sample_data):
    """Тест обработки пропущенных значений."""
    config = {"handle_missing": "drop"}
    preprocessor = DataPreprocessor(config)

    result = preprocessor.fit_transform(sample_data.copy())

    # Проверяем, что строки с пропусками в target удалены
    assert result["Price"].isnull().sum() == 0
    assert len(result) < len(sample_data)


def test_preprocessor_removes_outliers_iqr(sample_data):
    """Тест удаления выбросов методом IQR."""
    # Добавляем явный выброс
    sample_data.loc[len(sample_data)] = {
        "Price": 1000000000,  # Очень высокая цена
        "Area": 50,
        "Region": "Moscow",
        "Minutes_to_metro": 5,
        "Number_of_rooms": 1,
    }

    config = {
        "handle_missing": "drop",
        "outlier_method": "iqr",
        "outlier_threshold": 1.5,
    }
    preprocessor = DataPreprocessor(config)

    result = preprocessor.fit_transform(sample_data.copy())

    # Выброс должен быть удалён
    assert result["Price"].max() < 1000000000


def test_preprocessor_preserves_columns(sample_data):
    """Тест сохранения структуры колонок."""
    config = {"handle_missing": "drop"}
    preprocessor = DataPreprocessor(config)

    result = preprocessor.fit_transform(sample_data.copy())

    expected_cols = set(sample_data.columns)
    actual_cols = set(result.columns)

    assert expected_cols == actual_cols
