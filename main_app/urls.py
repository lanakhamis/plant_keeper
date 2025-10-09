from django.urls import path
from . import views

urlpatterns = [
    path('', views.PlantList.as_view(), name='plant_index'),
    path('plants/<int:pk>/', views.PlantDetail.as_view(), name='plant_detail'),
    path('plants/create/', views.PlantCreate.as_view(), name='plant_create'),
    path('plants/<int:pk>/update/', views.PlantUpdate.as_view(), name='plant_update'),
    path('plants/<int:pk>/delete/', views.PlantDelete.as_view(), name='plant_delete'),
]