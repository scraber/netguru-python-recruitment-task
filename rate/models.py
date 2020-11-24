from django.db import models
from cars.models import Car


class Rate(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.car}: {self.rating} stars"
