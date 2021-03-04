from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from users import models

admin.site.register(models.CustomUser, UserAdmin)
