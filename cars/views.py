import requests
from django.db import IntegrityError
from django.db.models import Avg, Count
from django.db.models.functions import Coalesce
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Car
from .serializers import CarSerializer
from .utils import call_external_car_api


class CarAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        cars = Car.objects.annotate(
            average_rate=Coalesce(Avg("rate__rating"), 0)
        ).order_by("-average_rate")
        return Response(cars.values())

    def post(self, request):
        serializer = CarSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={"error": f"Invalid Parameters"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        car_make = serializer.validated_data.get("make_name")
        car_model = serializer.validated_data.get("model_name")

        req = call_external_car_api(car_make, car_model)

        if req.error:
            return Response(data={"error": f"{req.error}"}, status=req.status)

        if req.data:
            try:
                serializer.save()
            except IntegrityError:
                return Response(
                    data={"error": f"Car {car_make} {car_model} already exists!"},
                    status=status.HTTP_409_CONFLICT,
                )
            return Response(
                data={"result": f"Added {car_make} {car_model} to database"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                data={
                    "error": f"No matching result in external api for {car_make} {car_model}"
                },
                status=status.HTTP_404_NOT_FOUND,
            )


class CarPopularAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        cars = Car.objects.annotate(rating_qty=Count("rate__rating")).order_by(
            "-rating_qty"
        )
        return Response(cars.values())
