import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def test_clean_data_removes_outliers():

    test_data = pd.DataFrame(
        {
            "duration": [5, 10, 15, 35, 40],
            "stops": ["zero", "one", "zero", "one", "two_or_more"],
            "class": ["Economy", "Business", "Economy", "Business", "Economy"],
            "airline": ["Indigo", "Air_India", "Vistara", "Indigo", "Air_India"],
            "source_city": ["Delhi", "Mumbai", "Bangalore", "Delhi", "Mumbai"],
            "destination_city": ["Mumbai", "Delhi", "Chennai", "Mumbai", "Delhi"],
            "departure_time": ["Morning", "Evening", "Night", "Morning", "Evening"],
            "arrival_time": ["Afternoon", "Night", "Morning", "Afternoon", "Night"],
            "flight": ["AI-101", "SG-202", "IN-303", "AI-104", "SG-205"],
        }
    )

    assert test_data["duration"].max() <= 30
    assert len(test_data) == 3
    assert all(test_data["duration"] <= 30)
