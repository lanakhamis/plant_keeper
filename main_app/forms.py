from django import forms
from .models import Plant, Reminder , CareLog
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


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

# /////add (Lujain)////////////////////
class CareLogForm(forms.ModelForm):
    class Meta:
        model = CareLog
        fields = ['action', 'note']  
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add any notes...'}),
            'action': forms.Select(attrs={'class': 'form-select'}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        # 'placeholder': 'Enter your email'
    }))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField() 
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']
        labels = {
            'image': '', 
        }