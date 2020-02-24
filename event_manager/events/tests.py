from unittest import mock

import pytz
from django.db.models.functions import datetime
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Registration, Event


class EventModelTest(TestCase):

    def setUp(self):
        Event.objects.create(name="something amazing", location="galaxy",
                             start_time="2020-02-20T06:00:00Z",
                             end_time="2020-02-20T06:00:00Z")

    def test_event_location(self):
        event_galaxy = Event.objects.get(name="something amazing")
        mocked = datetime.datetime(2020, 2, 20, 6, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
            self.assertEqual(event_galaxy.location, "galaxy")
            self.assertEqual(event_galaxy.name, "something amazing")
            self.assertEqual(event_galaxy.start_time, mocked)
            self.assertEqual(event_galaxy.end_time, mocked)

    def test_string_representation(self):
        event_galaxy = Event.objects.get(name="something amazing")
        self.assertEqual((str(event_galaxy)), event_galaxy.name)


class RegistrationModelTest(TestCase):

    def setUp(self):
        Event.objects.create(name="something amazing", location="galaxy", id=21)
        Registration.objects.create(name="user1", email="gu@ga.com", event_id=21)

    def test_registration_name(self):
        new_registration = Registration.objects.get(name="user1")
        self.assertEqual(new_registration.name, "user1")

    def test_registered_event_name(self):
        new_registration = Registration.objects.get(name="user1")
        self.assertEqual(new_registration.event.name, "something amazing")

    def test_string_representation(self):
        new_registration = Registration.objects.get(name="user1")
        self.assertEqual((str(new_registration)), new_registration.name)


class RegistrationTestCase(APITestCase):
    fixtures = ['testdata.json']

    def test_good_registration_one_mailId_one_event(self):
        data = {"name": "testuser1", "email": "test11@gua.com", "event": 14}
        response = self.client.post("/signUpEvent/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_registration_same_mailId_one_event(self):
        data = {"name": "testuser1", "email": "test123@gu.com", "event": 14}
        response = self.client.post("/signUpEvent/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post("/signUpEvent/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_multiple_registration_same_mailId_diff_events(self):
        data1 = {"name": "testuser1", "email": "test12@gu.com", "event": 14}
        response = self.client.post("/signUpEvent/", data1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data2 = {"name": "testuser1", "email": "test13@gu.com", "event": 15}
        response = self.client.post("/signUpEvent/", data2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_multiple_registration_same_event_diff_mailIds(self):
        data1 = {"name": "testuser1", "email": "test14@gu.com", "event": 14}
        response = self.client.post("/signUpEvent/", data1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data2 = {"name": "testuser1", "email": "test15@gu.com", "event": 14}
        response = self.client.post("/signUpEvent/", data2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_non_existing_event(self):
        data = {"name": "testuser1", "email": "test16@gu.com", "event": 99}
        response = self.client.post("/signUpEvent/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_invalid_emailId_event(self):
        data = {"name": "testuser1", "email": "test19@gu", "event": 14}
        response = self.client.post("/signUpEvent/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
