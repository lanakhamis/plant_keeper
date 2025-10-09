from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import User, Plant, CareLog, Reminder
admin.site.register(User)
admin.site.register(Plant)
admin.site.register(CareLog)
admin.site.register(Reminder)