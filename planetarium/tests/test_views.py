from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from planetarium.models import PlanetariumDome, AstronomyShow, ShowSession, Ticket, Reservation, ShowTheme
from django.urls import reverse
from datetime import datetime, timedelta
import pytz

User = get_user_model()

class ShowSessionViewSetTests(APITestCase):
    def setUp(self):
        self.dome = PlanetariumDome.objects.create(name="Main Dome", rows=5, seats_in_row=5)
        self.show = AstronomyShow.objects.create(title="Stars", description="Star show")
        self.session = ShowSession.objects.create(
            astronomy_show=self.show,
            planetarium_dome=self.dome,
            show_time=datetime.now(pytz.UTC) + timedelta(days=1)
        )
        self.url = reverse("showsession-list")
        self.client = APIClient()

    def test_list_sessions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_available_seats(self):
        url = reverse("showsession-available-seats", kwargs={"pk": self.session.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("available_seats", response.data)


class TicketViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.dome = PlanetariumDome.objects.create(name="Main Dome", rows=10, seats_in_row=10)
        self.theme = ShowTheme.objects.create(name="Galaxies")
        self.show = AstronomyShow.objects.create(title="Black Holes")
        self.theme.shows.add(self.show)

        self.session = ShowSession.objects.create(
            astronomy_show=self.show,
            planetarium_dome=self.dome,
            show_time=timezone.now() + timezone.timedelta(days=1)
        )

        self.reservation = Reservation.objects.create(user=self.user)
        self.url = reverse("ticket-list")

    def test_create_ticket_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "row": 3,
            "seat": 7,
            "show_session": self.session.id,
            "reservation": self.reservation.id
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_ticket_unauthenticated(self):
        data = {
            "row": 3,
            "seat": 7,
            "show_session": self.session.id,
            "reservation": self.reservation.id
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReservationViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.url = reverse("reservation-list")  # basename='reservation'

    def test_create_reservation_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"], self.user.id)

    def test_create_reservation_unauthenticated(self):
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ShowThemeViewSetTests(APITestCase):
    def setUp(self):
        self.url = reverse("showtheme-list")

    def test_create_show_theme(self):
        data = {"name": "Cosmos", "shows": []}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ShowTheme.objects.filter(name="Cosmos").exists())

    def test_list_show_themes(self):
        ShowTheme.objects.create(name="Black Holes")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], "Black Holes")


class PlanetariumDomeViewSetTests(APITestCase):
    def setUp(self):
        self.url = reverse("planetariumdome-list")

    def test_create_planetarium_dome(self):
        data = {
            "name": "Main Dome",
            "rows": 5,
            "seats_in_row": 10,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PlanetariumDome.objects.count(), 1)

    def test_list_planetarium_domes(self):
        PlanetariumDome.objects.create(name="Small Dome", rows=3, seats_in_row=5)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], "Small Dome")
