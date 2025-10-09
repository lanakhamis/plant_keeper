from django.db import models
from django.urls import reverse
from datetime import timedelta, date
# Create your models here.
# -----------------------------------------------------------
# 👤 USER MODEL
# -----------------------------------------------------------
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.id})


# -----------------------------------------------------------
# 🌿 PLANT MODEL
# -----------------------------------------------------------
class Plant(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)
    last_watered_date = models.DateField(blank=True, null=True)
    watering_frequency = models.IntegerField(default=7, help_text="How often to water (in days)")
    notes = models.TextField(blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.species})"

    def get_absolute_url(self):
        return reverse('plant_detail', kwargs={'pk': self.id})

    def next_watering_date(self):
        """Calculate the next watering date."""
        if self.last_watered_date:
            return self.last_watered_date + timedelta(days=self.watering_frequency)
        return None

    def needs_watering(self):
        """Check if the plant needs to be watered today."""
        if not self.last_watered_date:
            return True
        days_passed = (date.today() - self.last_watered_date).days
        return days_passed >= self.watering_frequency


# -----------------------------------------------------------
# 🪴 CARE LOG MODEL
# -----------------------------------------------------------
class CareLog(models.Model):
    ACTIONS = [
        ('Watered', 'Watered'),
        ('Fertilized', 'Fertilized'),
        ('Pruned', 'Pruned'),
        ('Repotted', 'Repotted'),
    ]

    action_type = models.CharField(max_length=50, choices=ACTIONS)
    date = models.DateField(auto_now_add=True)
    note = models.TextField(blank=True)
    plant_id = models.ForeignKey(Plant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.action_type} – {self.plant.name} ({self.date})"

    def get_absolute_url(self):
        return reverse('carelog_detail', kwargs={'pk': self.id})


# -----------------------------------------------------------
# ⏰ REMINDER MODEL
# -----------------------------------------------------------
class Reminder(models.Model):
    REMINDER_TYPES = [
        ('Water', 'Water'),
        ('Fertilizer', 'Fertilizer'),
        ('Check Soil', 'Check Soil'),
    ]

    reminder_type = models.CharField(max_length=50, choices=REMINDER_TYPES)
    reminder_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    plant_id = models.ForeignKey(Plant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.reminder_type} for {self.plant.name} on {self.reminder_date}"

    def get_absolute_url(self):
        return reverse('reminder_detail', kwargs={'pk': self.id})

    def mark_completed(self):
        """Mark the reminder as done."""
        self.is_completed = True
        self.save()