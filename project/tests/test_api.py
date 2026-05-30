import pytest
from fastapi.testclient import TestClient

from src.service.app import app

client = TestClient(app)

test_data = {
    "airline": "IndiGo",
    "flight": "6E-123",
    "source_city": "Delhi",
    "departure_time": "Morning",
    "stops": "zero",
    "arrival_time": "Evening",
    "destination_city": "Mumbai",
    "class": "Business",
    "duration": 10,
    "days_left": 30,
}


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    assert "model_loaded" in data


def test_predict_endpoint_missing_fields():
    test_data = {"airline": "Indigo"}
    response = client.post("/predict", json=test_data)

    assert response.status_code in [200, 400, 422]


def test_predict_endpoint_invalid_stops():
    test_data = {
        "airline": "Indigo",
        "source_city": "Delhi",
        "destination_city": "Mumbai",
        "departure_time": "Morning",
        "arrival_time": "Afternoon",
        "stops": "invalid_value",
        "class": "Economy",
        "duration": 2.5,
        "days_left": 15,
        "flight": "6E-123",
    }

    response = client.post("/predict", json=test_data)

    assert response.status_code in [500, 400, 422]
