from django import forms
from .models import Plant, Reminder


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ["name", "species", "last_watered_date", "watering_frequency", "notes"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "species": forms.TextInput(attrs={"class": "form-control"}),
            "last_watered_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "watering_frequency": forms.NumberInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


# ✅ فورم التذكيرات (Reminders)
class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ["reminder_type", "reminder_date", "message"]
        widgets = {
            "plant": forms.Select(attrs={"class": "form-select"}),
            "reminder_type": forms.Select(attrs={"class": "form-select"}),
            "reminder_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "message": forms.TextInput(attrs={"class": "form-control"}),
        }
