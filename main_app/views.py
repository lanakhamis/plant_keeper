from datetime import date, timedelta
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Plant, Reminder
from .forms import PlantForm, ReminderForm, UserUpdateForm, ProfileUpdateForm


class PlantList(LoginRequiredMixin, ListView):
    model = Plant
    template_name = "plants/index.html"
    context_object_name = "plants"

    def get_queryset(self):
        return Plant.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        next_week = today + timedelta(days=7)

        context["reminders_today"] = Reminder.objects.filter(
            reminder_date__range=(today, next_week),
            is_completed=False,
            plant__user=self.request.user,
        )

        needs_watering_plants = [
            plant for plant in context["plants"] if plant.needs_watering
        ]
        context["needs_watering_count"] = len(needs_watering_plants)
        return context


class PlantCreate(LoginRequiredMixin, CreateView):
    model = Plant
    form_class = PlantForm
    template_name = "plants/form.html"
    success_url = reverse_lazy("plant_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "🌿 Plant added successfully!")
        return super().form_valid(form)


class PlantDetail(LoginRequiredMixin, DetailView):
    model = Plant
    template_name = "plants/detail.html"
    context_object_name = "plant"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plant = self.get_object()

        context["reminders"] = Reminder.objects.filter(
            plant=plant, is_completed=False, reminder_date__gte=date.today()
        ).order_by("reminder_date")

        context["today_reminders"] = Reminder.objects.filter(
            plant=plant, is_completed=False, reminder_date=date.today()
        )
        return context


class PlantUpdate(LoginRequiredMixin, UpdateView):
    model = Plant
    form_class = PlantForm
    template_name = "plants/form.html"
    success_url = reverse_lazy("plant_list")


class PlantDelete(LoginRequiredMixin, DeleteView):
    model = Plant
    template_name = "plants/confirm_delete.html"
    success_url = reverse_lazy("plant_list")


class ReminderList(LoginRequiredMixin, ListView):
    model = Reminder
    template_name = "reminders/index.html"
    context_object_name = "reminders"

    def get_queryset(self):
        return Reminder.objects.filter(plant__user=self.request.user)


class ReminderCreate(LoginRequiredMixin, CreateView):
    model = Reminder
    form_class = ReminderForm
    template_name = "reminders/form.html"

    def form_valid(self, form):
        plant_id = self.request.GET.get("plant_id")
        if plant_id:
            plant = get_object_or_404(Plant, pk=plant_id)
            form.instance.plant = plant
        reminder = form.save()
        return redirect("plant_detail", pk=reminder.plant.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plant_id = self.request.GET.get("plant_id")
        if plant_id:
            context["plant"] = get_object_or_404(Plant, pk=plant_id)
        return context


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "plants/signup.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def profile_view(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("my_profile")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "profiles/profile.html", context)


@login_required
@csrf_exempt
def remove_profile_image(request):
    if request.method == "POST":
        profile = request.user.profile
        if profile.image and profile.image.name != "default.jpg":
            profile.image.delete(save=False)
            profile.image = "default.jpg"
            profile.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"}, status=400)
