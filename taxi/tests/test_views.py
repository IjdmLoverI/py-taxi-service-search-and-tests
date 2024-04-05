from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Driver.objects.create_user(
            username="testuser",
            password="12345"
        )
        self.client.force_login(self.user)

    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_toggle_assign_to_car(self):
        car_id = 1
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": car_id})
        )
        self.assertEqual(response.status_code, 404)


class CarListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.login(username="testuser", password="password")
        self.manufacturer1 = Manufacturer.objects.create(name="Toyota")
        self.car1 = Car.objects.create(
            model="Toyota Camry", manufacturer=self.manufacturer1
        )

    def test_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"search": "Toyota"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota Camry")


class ManufacturerListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.login(username="testuser", password="password")
        self.manufacturer1 = Manufacturer.objects.create(name="Toyota")

    def test_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"search": "Toyota"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
