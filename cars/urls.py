from django.urls import path
from . views import CarAPIView, CarPopularAPIView

urlpatterns = [
    path('cars', CarAPIView.as_view()),
    path('popular', CarPopularAPIView.as_view())
]
