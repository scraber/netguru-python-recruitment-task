from django.urls import path

from .views import CarAPIView, CarPopularAPIView

urlpatterns = [
    path("cars", CarAPIView.as_view(), name="cars-list"),
    path("popular", CarPopularAPIView.as_view(), name="cars-popular"),
]
