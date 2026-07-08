#!/usr/bin/env python
# coding: utf-8

# import statements
from fastapi import FastAPI, HTTPException
from sklearn.preprocessing import PolynomialFeatures
import json
import numpy as np
import pickle
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODELS = ROOT / "models"

app = FastAPI(title="Airport Delay Prediction API")

# Import the airport encodings file
f = open(MODELS / "airport_encodings.json")

# returns JSON object as a dictionary
airports = json.load(f)


def create_airport_encoding(airport: str, airports: dict) -> np.array:
    """
    create_airport_encoding is a function that creates an array the length of all arrival airports from the chosen
    departure airport. The array consists of all zeros except for the specified arrival airport, which is a 1.
    """
    temp = np.zeros(len(airports))
    if airport in airports:
        temp[airports.get(airport)] = 1
        temp = temp.T
        return temp
    else:
        return None


# Load the finalized model from Task 2
with open(MODELS / "finalized_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)


def time_to_seconds(time_string: str) -> int:
    """
    Convert a time string in HH:MM format to seconds since midnight.
    """
    time_object = datetime.datetime.strptime(time_string, "%H:%M")

    seconds = (
        time_object.hour * 3600
        + time_object.minute * 60
        + time_object.second
    )

    return seconds


def predict_delay(arrival_airport: str,
                  departure_time: str,
                  arrival_time: str) -> float:
    """
    Predict the average departure delay using the trained model.
    """
    encoded_airport = create_airport_encoding(arrival_airport, airports)

    if encoded_airport is None:
        raise ValueError("Arrival airport not found in airport_encodings.json.")

    departure_seconds = time_to_seconds(departure_time)
    arrival_seconds = time_to_seconds(arrival_time)

    model_input = np.concatenate((
        encoded_airport,
        np.array([departure_seconds, arrival_seconds])
    ))

    model_input = model_input.reshape(1, -1)

    polynomial_order = 1
    poly = PolynomialFeatures(degree=polynomial_order)
    model_input = poly.fit_transform(model_input)

    prediction = model.predict(model_input)

    return float(prediction[0])


@app.get("/")
def read_root():
    return {"message": "API is functional"}


@app.get("/predict/delays")
def get_delay_prediction(
    departure_airport: str,
    arrival_airport: str,
    departure_time: str,
    arrival_time: str
):
    try:
        departure_airport = departure_airport.upper().strip()
        arrival_airport = arrival_airport.upper().strip()
        departure_time = departure_time.strip()
        arrival_time = arrival_time.strip()

        if departure_airport != "DFW":
            raise HTTPException(
                status_code=400,
                detail="This model only supports DFW as the departure airport."
            )

        prediction = predict_delay(
            arrival_airport=arrival_airport,
            departure_time=departure_time,
            arrival_time=arrival_time
        )

        return {
            "departure_airport": departure_airport,
            "arrival_airport": arrival_airport,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
            "average_departure_delay_minutes": round(prediction, 2)
        }

    except HTTPException:
        raise

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))