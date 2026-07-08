from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


# Test the root endpoint
def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "API is functional"}


# Test a valid prediction request
def test_valid_prediction():
    response = client.get(
        "/predict/delays",
        params={
            "departure_airport": "DFW",
            "arrival_airport": "LAX",
            "departure_time": "08:00",
            "arrival_time": "10:30",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "average_departure_delay_minutes" in data
    assert isinstance(data["average_departure_delay_minutes"], float)


# Test an invalid departure airport
def test_invalid_departure_airport():
    response = client.get(
        "/predict/delays",
        params={
            "departure_airport": "ATL",
            "arrival_airport": "LAX",
            "departure_time": "08:00",
            "arrival_time": "10:30",
        },
    )

    assert response.status_code == 400

    data = response.json()
    expected_message = "This model only supports DFW as the departure airport."

    assert data["detail"] == expected_message