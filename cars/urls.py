from django.urls import path
from . views import CarAPIView

urlpatterns = [
    path('cars/', CarAPIView.as_view())
]
