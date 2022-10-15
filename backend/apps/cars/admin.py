from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.cars import models

admin.site.register(models.CarDocument)
