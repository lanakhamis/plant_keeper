from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Plant
from django.urls import reverse_lazy

class PlantList(ListView):
    model = Plant
    template_name = 'main_app/plant_list.html'

class PlantDetail(DetailView):
    model = Plant
    template_name = 'main_app/plant_detail.html'

class PlantCreate(CreateView):
    model = Plant
    fields = ['name', 'species', 'watering_frequency', 'last_watered_date', 'notes']
    template_name = 'main_app/plant_form.html'

class PlantUpdate(UpdateView):
    model = Plant
    fields = ['name', 'species', 'watering_frequency', 'last_watered_date', 'notes']
    template_name = 'main_app/plant_form.html'

class PlantDelete(DeleteView):
    model = Plant
    success_url = reverse_lazy('plant_index')
    template_name = 'main_app/plant_confirm_delete.html'