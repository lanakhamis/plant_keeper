from datetime import timedelta, date
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


#  PLANT MODEL
class Plant(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)
    last_watered_date = models.DateField(blank=True, null=True)
    watering_frequency = models.IntegerField(
        default=7, help_text="Days between watering"
    )
    notes = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.species})"

    def get_absolute_url(self):
        return reverse("plant_detail", kwargs={"pk": self.id})

    def next_watering_date(self):
        """Return the next watering date based on the last watered date."""
        if self.last_watered_date:
            return self.last_watered_date + timedelta(days=self.watering_frequency)
        return None

    @property
    def needs_watering(self):
        """Check if the plant needs watering today."""
        if not self.last_watered_date:
            return True
        days_passed = (date.today() - self.last_watered_date).days
        return days_passed >= self.watering_frequency


# CARE LOG MODEL
class CareLog(models.Model):
    ACTIONS = [
        ("Watered", "Watered"),
        ("Fertilized", "Fertilized"),
        ("Pruned", "Pruned"),
        ("Repotted", "Repotted"),
    ]

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ACTIONS)
    date = models.DateField(auto_now_add=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.action} – {self.plant.name} ({self.date})"

    def get_absolute_url(self):
        return reverse("carelog_detail", kwargs={"pk": self.id})


#  REMINDER MODEL
class Reminder(models.Model):
    REMINDER_TYPES = [
        ("Water", "Water"),
        ("Fertilizer", "Fertilizer"),
        ("Check Soil", "Check Soil"),
    ]

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    reminder_type = models.CharField(
        max_length=50, choices=REMINDER_TYPES, default="Water"
    )
    reminder_date = models.DateField()
    message = models.CharField(
        max_length=255, default="Time to take care of your plant! 💧"
    )
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reminder_type} for {self.plant.name} on {self.reminder_date}"

    def get_absolute_url(self):
        return reverse("reminder_detail", kwargs={"pk": self.id})

    def mark_completed(self):
        """Mark this reminder as completed."""
        self.is_completed = True
        self.save()

    def is_due(self):
        """Check if the reminder is due today or past."""
        return date.today() >= self.reminder_date


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default="profile_pics/default.jpg",
        upload_to="profile_pics",
        verbose_name="Your profile picture",
    )
    bio = models.TextField(max_length=500, blank=True, verbose_name="Bio")

    def __str__(self):
        return f"{self.user.username} Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a Profile whenever a new User is created."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the user's profile whenever the User object is saved."""
    instance.profile.save()
