from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APIClient
from rute_api.models import User, DriveRequest, Car, Route
from datetime import datetime

from rute_api.queries import get_drive_request_by_user


class DriveRequestViewTest(TestCase):

    def setUp(self):
        self.driver = User.objects.create(
            email="test@teste.com",
            password="testtesttest",
            rating=0.0,
            is_active=True
        )
        self.passenger = User.objects.create(
            email="test@tese.com",
            password="testtesttest",
            rating=0.0
        )
        self.car = Car.objects.create(
            maker="test",
            color="test",
            license_plate="test",
            owner=self.driver
        )
        self.route = Route.objects.create(
            starting_location="test",
            end_location="test",
            starting_time=datetime.now(),
            available_seats=2,
            car=self.car
        )
        self.drive_request1 = DriveRequest.objects.create(
            user=self.passenger,
            route=self.route
        )
        self.drive_request2 = DriveRequest.objects.create(
            user=self.passenger,
            route=self.route,
            deleted=True
        )
        self.drive_request3 = DriveRequest.objects.create(
            user=self.passenger,
            route=self.route,
            is_canceled=True
        )
        self.drive_request4 = DriveRequest.objects.create(
            user=self.passenger,
            route=self.route,
            is_accepted=True
        )

    def test_get_drive_request_by_user(self):
        response = get_drive_request_by_user(self.driver.uuid)
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0], self.drive_request1)

    def test_put_drive_request(self):
        token = Token.objects.get_or_create(user=self.driver)[0]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

        data2 = {
            "is_accepted": True
        }

        data3 = {
            "is_accepted": "test"
        }

        response_2 = client.put(reverse('drive_requests', kwargs={'uuid': self.drive_request2}), data=data2)
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)

        response_3 = client.put(reverse('drive_requests', kwargs={'uuid': self.drive_request2}), data=data3)
        self.assertEqual(response_3.status_code, status.HTTP_400_BAD_REQUEST)


class RouteViewTest(TestCase):

    def setUp(self):
        self.driver = User.objects.create(
            email="test@teste.com",
            password="testtesttest",
            rating=0.0,
            is_active=True
        )
        self.passenger = User.objects.create(
            email="test@tese.com",
            password="testtesttest",
            rating=0.0
        )
        self.car = Car.objects.create(
            maker="test",
            color="test",
            license_plate="test",
            owner=self.driver
        )

    def test_post_route(self):
        token = Token.objects.get_or_create(user=self.driver)[0]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

        data = {
            "starting_location": "nancy",
            "end_location": "metz",
            "starting_time": "2015-10-22T18:17:51Z",
            "contribution": 0.0,
            "available_seats": 4,
            "car": self.car.uuid,
            "passenger": [
                self.passenger.uuid
            ]
        }

        response_1 = self.client.post(reverse('routes'), data)
        self.assertEqual(response_1.status_code, status.HTTP_401_UNAUTHORIZED)

        response_2 = client.post(reverse('routes'), data=data)
        self.assertEqual(response_2.status_code, status.HTTP_201_CREATED)
