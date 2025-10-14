from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, timedelta
from .models import Plant, Reminder


class PlantViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="leen", password="12345")
        self.plant = Plant.objects.create(
            name="Rose",
            species="Flower",
            user=self.user,
            last_watered_date=date.today() - timedelta(days=8),
            watering_frequency=7,
        )
        self.reminder = Reminder.objects.create(
            plant=self.plant,
            reminder_type="Water",
            reminder_date=date.today() + timedelta(days=1),
        )

    def test_plant_list_view_requires_login(self):
        response = self.client.get(reverse("plant_list"))
        self.assertNotEqual(response.status_code, 200)
        self.client.login(username="leen", password="12345")
        response = self.client.get(reverse("plant_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "plants/index.html")

    def test_plant_detail_view(self):
        self.client.login(username="leen", password="12345")
        response = self.client.get(
            reverse("plant_detail", kwargs={"pk": self.plant.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "plants/detail.html")
        self.assertContains(response, self.plant.name)

    def test_plant_create_view(self):
        self.client.login(username="leen", password="12345")
        response = self.client.post(
            reverse("plant_create"),
            {
                "name": "Tulip",
                "species": "Flower",
                "watering_frequency": 5,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Plant.objects.filter(name="Tulip").exists())

    def test_plant_update_view(self):
        self.client.login(username="leen", password="12345")
        response = self.client.post(
            reverse("plant_edit", kwargs={"pk": self.plant.pk}),
            {
                "name": "Rose Updated",
                "species": "Flower",
                "watering_frequency": 10,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.plant.refresh_from_db()
        self.assertEqual(self.plant.name, "Rose Updated")

    def test_plant_delete_view(self):
        self.client.login(username="leen", password="12345")
        response = self.client.post(
            reverse("plant_delete", kwargs={"pk": self.plant.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Plant.objects.filter(pk=self.plant.pk).exists())

    def test_reminder_create_view(self):
        self.client.login(username="leen", password="12345")
        response = self.client.post(
            reverse("reminder_add") + f"?plant_id={self.plant.pk}",
            {
                "reminder_type": "Water",
                "reminder_date": date.today() + timedelta(days=2),
                "message": "Test reminder",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Reminder.objects.filter(message="Test reminder").exists())

    def test_profile_view_get(self):
        self.client.login(username="leen", password="12345")
        response = self.client.get(reverse("my_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/profile.html")

    def test_remove_profile_image(self):
        self.client.login(username="leen", password="12345")
        response = self.client.post(reverse("remove_profile_image"))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "success"})
