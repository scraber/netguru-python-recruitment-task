from unittest import mock

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Car
from .utils import ResponseData


class CarAPITests(APITestCase):
    def setUp(self) -> None:
        """
        Auxiliary test objects and functions
        """
        self.test_car = Car.objects.create(make_name="test", model_name="car")
        self.url = reverse("cars-list")
        test_user = User.objects.create_user(username="foo")  # Used for bearer auth
        self.client.force_authenticate(user=test_user)

    def test_car_get(self):
        """
        Get all fields of Car object according to serializer plus one extra for keeping track of average_rate
        """
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        # Since we have only one Car object we can grab first dict
        self.assertDictEqual(
            {
                "id": self.test_car.id,
                "make_name": self.test_car.make_name,
                "model_name": self.test_car.model_name,
                "average_rate": 0,  # 0 because we don't have any rate for this car
            },
            data[0],
        )

    def test_car_get_fail_auth(self):
        """
        Negative test case
        Methods without bearer token should result in 401_UNAUTHORIZED error
        """

        # turn off force auth for this test
        self.client.force_authenticate(user=None)

        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @mock.patch("cars.views.call_external_car_api")
    def test_car_post_success(self, api_call_mock):
        """
        Positive test case
        With car make_name and model_name existing in external api
        we should be able to create Car object with given names
        """
        car_data = {"make_name": "Tesla", "model_name": "Roadster"}
        count_before_post = Car.objects.count()

        api_call_mock.return_value = ResponseData(
            error="",
            status=status.HTTP_200_OK,
            data=[
                {
                    "Make_ID": 441,
                    "Make_Name": "Tesla",
                    "Model_ID": 2071,
                    "Model_Name": "Roadster",
                }
            ],
        )
        response = self.client.post(self.url, car_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), count_before_post + 1)

        # get() throws DoesNotExist if it can't find object
        Car.objects.get(
            make_name=car_data["make_name"], model_name=car_data["model_name"]
        )

    @mock.patch("cars.views.call_external_car_api")
    def test_car_post_non_existing_names(self, api_call_mock):
        """
        Negative test case
        Testing api with made-up names for make and model
        """
        car_data = {"make_name": "xyz123", "model_name": "Roadster"}

        api_call_mock.return_value = ResponseData(
            error="", status=status.HTTP_200_OK, data=[]
        )

        response = self.client.post(self.url, car_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        car_data = {"make_name": "Tesla", "model_name": "abc456"}
        response = self.client.post(self.url, car_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @mock.patch("cars.views.call_external_car_api")
    def test_car_post_already_exists(self, api_call_mock):
        """
        Negative test case
        Try adding same car twice, should result in first response status of 201_CREATED
        and second post's response of status 409_CONFLICT which signals duplicate
        """
        car_data = {"make_name": "Tesla", "model_name": "Roadster"}

        api_call_mock.return_value = ResponseData(
            error="",
            status=status.HTTP_200_OK,
            data=[
                {
                    "Make_ID": 441,
                    "Make_Name": "Tesla",
                    "Model_ID": 2071,
                    "Model_Name": "Roadster",
                }
            ],
        )

        response = self.client.post(self.url, car_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.url, car_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_car_post_invalid_params(self):
        """
        Negative test case
        Sending request with invalid keys should result in 400_BAD_REQUEST
        """
        car_data = {"abc_name": "Tesla", "model_name": "Roadster"}

        response = self.client.post(self.url, car_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        car_data = {"make_name": "Tesla", "abc_name": "Roadster"}
        response = self.client.post(self.url, car_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch("cars.views.call_external_car_api")
    def test_car_post_server_error(self, api_call_mock):
        """
        Negative test case
        Try adding car, external api unavailable
        """
        car_data = {"make_name": "Tesla", "model_name": "Roadster"}

        api_call_mock.return_value = ResponseData(
            error="Server Error",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data=[],
        )

        response = self.client.post(self.url, car_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class CarPopularAPITests(APITestCase):
    def setUp(self) -> None:
        """
        Auxiliary test objects and functions
        """
        self.test_car = Car.objects.create(make_name="test", model_name="car")
        self.url = reverse("cars-popular")
        test_user = User.objects.create_user(username="foo")  # Used for bearer auth
        self.client.force_authenticate(user=test_user)

    def test_car_popular_get(self):
        """
        Get all fields of Car object according to serializer plus one extra for keeping track of total ratings for this car
        """
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        # Since we have only one Car object we can grab first dict
        self.assertDictEqual(
            {
                "id": self.test_car.id,
                "make_name": self.test_car.make_name,
                "model_name": self.test_car.model_name,
                "rating_qty": 0,  # 0 because we don't have any rate for this car
            },
            data[0],
        )

    def test_car_popular_get_fail_auth(self):
        """
        Negative test case
        Post with valid data without bearer token should result in 401_UNAUTHORIZED error
        """

        # turn off force auth for this test
        self.client.force_authenticate(user=None)

        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
