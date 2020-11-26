from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cars.models import Car

from .models import Rate


class RateAPITests(APITestCase):
    def setUp(self) -> None:
        """
        Auxiliary test objects and functions
        """
        self.test_car = Car.objects.create(make_name="test", model_name="car")
        self.url = reverse("rate-car")
        test_user = User.objects.create_user(username="foo")  # Used for bearer auth
        self.client.force_authenticate(user=test_user)

    def test_rate_post_success(self):
        """
        Positive test case
        With existing car.id and rating between 1-5
        we should be able to create rating object for specific car
        """
        data = {"car": self.test_car.id, "rating": 5}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rate.objects.count(), 1)
        self.assertEqual(Rate.objects.get().car, self.test_car)
        self.assertEqual(Rate.objects.get().rating, 5)

    def test_rate_post_invalid_car_id(self):
        """
        Negative test case
        Non existing car.id was given
        """
        data = {"car": self.test_car.id + 1, "rating": 5}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Rate.objects.count(), 0)

    def test_rate_post_rating_not_in_min_max(self):
        """
        Negative test case
        Non rating value is not in range 1-5
        """
        data = {"car": self.test_car.id, "rating": 0}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Rate.objects.count(), 0)

        data = {"car": self.test_car.id, "rating": 6}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Rate.objects.count(), 0)

    def test_rate_post_invalid_car_id(self):
        """
        Negative test case
        Invalid parameter's keys
        """
        data = {"abc": self.test_car.id, "rating": 5}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Rate.objects.count(), 0)

        data = {"car": self.test_car.id, "abc": 5}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Rate.objects.count(), 0)

    def test_rate_post_fail_auth(self):
        """
        Negative test case
        Post with valid data without bearer token should result in 401_UNAUTHORIZED error
        """

        # turn off force auth for this test
        self.client.force_authenticate(user=None)
        data = {"car": self.test_car.id, "rating": 5}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
