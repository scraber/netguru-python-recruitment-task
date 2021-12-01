import os
from typing import NamedTuple

import requests
from requests import api
from rest_framework import status


class ResponseData(NamedTuple):
    error: str
    status: int
    data: list


def call_external_car_api(car_make: str, car_model: str) -> ResponseData:
    api_url = f"https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{car_make}?format=json"

    try:
        req = requests.request("GET", url=api_url)
    except requests.exceptions.RequestException as e:
        return ResponseData(
            error=f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=[]
        )
    if req.status_code != status.HTTP_200_OK:
        return ResponseData(error=req.reason, status=req.status_code, data=[])

    resp = req.json()
    result = [
        car
        for car in resp.get("Results")
        if car.get("Model_Name", "").capitalize() == car_model.capitalize()
    ]
    return ResponseData(error="", status=status.HTTP_200_OK, data=result)
