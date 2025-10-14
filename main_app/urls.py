from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import CareLogCreate

urlpatterns = [
    path("", views.PlantList.as_view(), name="plant_list"),
    path("plants/create/", views.PlantCreate.as_view(), name="plant_create"),
    path("plants/<int:pk>/", views.PlantDetail.as_view(), name="plant_detail"),
    path("plants/<int:pk>/edit/", views.PlantUpdate.as_view(), name="plant_edit"),
    path("plants/<int:pk>/delete/", views.PlantDelete.as_view(), name="plant_delete"),
    # path("reminders/", views.ReminderList.as_view(), name="reminder_list"),
    # path("reminders/add/", views.ReminderCreate.as_view(), name="reminder_add"),
    path("reminders/", views.ReminderList.as_view(), name="reminder_list"),
    path("reminders/add/", views.ReminderCreate.as_view(), name="reminder_add"),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='plants/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.profile_view, name='my_profile'),
    path('profile/remove-image/', views.remove_profile_image, name='remove_profile_image'),
    path('carelog/add/', CareLogCreate.as_view(), name='carelog_add'),
]


    