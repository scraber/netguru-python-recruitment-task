from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RateSerializer


class RateCarAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = RateSerializer(data=request.data)
        if serializer.is_valid():
            car = serializer.validated_data.get("car")
            rating = serializer.validated_data.get("rating")
            serializer.save()
            return Response(
                data={"result ": f"Added rating: {rating} for car: {car}"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data={"error": f"{serializer.errors}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
