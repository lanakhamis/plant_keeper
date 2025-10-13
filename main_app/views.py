from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import date, timedelta
from django.shortcuts import redirect, get_object_or_404, render
from .forms import PlantForm
from .forms import ReminderForm
from django.views.generic import DetailView
from .models import Plant, Reminder
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout


class PlantList(LoginRequiredMixin, ListView):
    model = Plant
    template_name = "plants/index.html"
    context_object_name = "plants"

    def get_queryset(self):
        # فقط النباتات الخاصة بالمستخدم الحالي
        return Plant.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        next_week = today + timedelta(days=7)

        # 🔹 جلب التذكيرات القادمة خلال 7 أيام
        context["reminders_today"] = Reminder.objects.filter(
            reminder_date__range=(today, next_week),
            is_completed=False,
            plant__user=self.request.user,
        )

        # 🔹 عدد النباتات التي تحتاج سقي
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
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        else:
            form.instance.user_id = 1

        messages.success(self.request, "🌿 Plant added successfully!")
        return super().form_valid(form)


class PlantDetail(LoginRequiredMixin, DetailView):
    model = Plant
    template_name = "plants/detail.html"
    context_object_name = "plant"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plant = self.get_object()
        # التذكيرات القادمة للنبتة
        context["reminders"] = Reminder.objects.filter(
            plant=plant, is_completed=False, reminder_date__gte=date.today()
        ).order_by("reminder_date")
        # تذكيرات اليوم فقط للbadge
        context["today_reminders"] = Reminder.objects.filter(
            plant=plant, is_completed=False, reminder_date=date.today()
        )
        return context


class PlantUpdate(LoginRequiredMixin, UpdateView):
    model = Plant
    form_class = PlantForm
    template_name = "plants/form.html"
    success_url = reverse_lazy("plant_list")


# 🗑️ حذف النبتة
class PlantDelete(LoginRequiredMixin, DeleteView):
    model = Plant
    template_name = "plants/confirm_delete.html"
    success_url = reverse_lazy("plant_list")


class ReminderList(ListView):
    model = Reminder
    template_name = "reminders/index.html"
    context_object_name = "reminders"

    def form_valid(self, form):
        # ربط النبات بالمستخدم الحالي تلقائياً
        form.instance.user = self.request.user
        return super().form_valid(form)


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
    return redirect("login")  # أو أي صفحة تريدينها
