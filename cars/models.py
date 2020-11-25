from django.db import models


class Car(models.Model):
    make_name = models.CharField(max_length=25)
    model_name = models.CharField(max_length=40)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["make_name", "model_name"], name="unique car name"
            )
        ]

    def __str__(self) -> str:
        return f"{self.make_name} {self.model_name}"
