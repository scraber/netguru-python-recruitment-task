from django.shortcuts import get_object_or_404
from requests import api
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RateSerializer


class RateCarAPIView(APIView):
    def post(self, request):
        serializer = RateSerializer(data=request.data)
        if serializer.is_valid():
            car = serializer.validated_data.get("car")
            rating = serializer.validated_data.get("rating")
            serializer.save()
            return Response(
                data=f"Add: rating: {rating} for car: {car}",
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data=f"{serializer.errors}",
            status=status.HTTP_400_BAD_REQUEST,
        )
