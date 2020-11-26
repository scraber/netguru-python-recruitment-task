from django.urls import path

from .views import RateCarAPIView

urlpatterns = [
       path('rate', RateCarAPIView.as_view(), name='rate-car')
]
