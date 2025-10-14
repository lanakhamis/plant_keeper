from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, timedelta
from .models import Plant, Reminder


class PlantModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="leen", password="12345")
        self.plant = Plant.objects.create(
            name="Rose",
            species="Flower",
            user=self.user,
            last_watered_date=date.today() - timedelta(days=8),
            watering_frequency=7,
        )

    def test_next_watering_date(self):
        expected_date = self.plant.last_watered_date + timedelta(days=7)
        self.assertEqual(self.plant.next_watering_date(), expected_date)

    def test_needs_watering_true(self):
        self.assertTrue(self.plant.needs_watering)

    def test_needs_watering_false(self):
        self.plant.last_watered_date = date.today()
        self.plant.save()
        self.assertFalse(self.plant.needs_watering)


class ReminderModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="leen", password="12345")
        self.plant = Plant.objects.create(
            name="Aloe Vera", species="Succulent", user=self.user
        )
        self.reminder = Reminder.objects.create(
            plant=self.plant,
            reminder_type="Water",
            reminder_date=date.today() - timedelta(days=1),
        )

    def test_is_due_true(self):
        self.assertTrue(self.reminder.is_due())

    def test_is_due_false(self):
        self.reminder.reminder_date = date.today() + timedelta(days=3)
        self.reminder.save()
        self.assertFalse(self.reminder.is_due())

    def test_mark_completed(self):
        self.reminder.mark_completed()
        self.reminder.refresh_from_db()
        self.assertTrue(self.reminder.is_completed)
