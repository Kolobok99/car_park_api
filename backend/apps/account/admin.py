from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.account import models

admin.site.register(models.UserModel)
admin.site.register(models.Profile)
admin.site.register(models.UserDocument)