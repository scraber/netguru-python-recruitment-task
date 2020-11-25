import json

import requests
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Car
from .serializers import CarSerializer


class CarAPIView(APIView):
    def get(self, request):
        cars = Car.objects.annotate(average_rate=Avg("rate__rating")).order_by(
            "-average_rate"
        )
        return Response(cars.values())

    def post(self, request):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            car_make = serializer.validated_data.get("make_name")
            car_model = serializer.validated_data.get("model_name")

            # car = Car.objects.filter(make_name=car_make, model_name=car_model).first()
            # if car:
            #     return Response(
            #         data=f"Car {car_make} {car_model} already exists in DB", status=status.HTTP_409_CONFLICT
            #     )

            api_url = f"https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{car_make}?format=json"
            try:
                req = requests.request("GET", url=api_url)
            except requests.exceptions.RequestException as e:
                return Response(
                    data=f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            if req.status_code != status.HTTP_200_OK:
                return Response(req.reason, status=req.status_code)
            resp = req.json()
            result = [
                car
                for car in resp.get("Results")
                if car.get("Model_Name").capitalize() == car_model.capitalize()
            ]
            if result:
                serializer.save()
                return Response(
                    data=f"Add {car_make} {car_model} to database",
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    data=f"No matching result in external api for {car_make} {car_model}",
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                data=f"Invalid Parameters",
                status=status.HTTP_400_BAD_REQUEST,
            )
