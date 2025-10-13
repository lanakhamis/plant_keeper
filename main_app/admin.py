from django.contrib import admin
from .models import User, Plant, CareLog, Reminder
# Register your models here.

# admin.site.register(User)
admin.site.register(Plant)
admin.site.register(CareLog)
admin.site.register(Reminder)