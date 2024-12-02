from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.

class Admin(UserAdmin):
    model = models.User
    list_display = ['email', 'username', 'is_staff', 'is_active']
    search_fields = ['email', 'username']
    ordering = ['email']

admin.site.register(models.User, Admin)    
admin.site.register(models.Category)
admin.site.register(models.Post)
admin.site.register(models.Comment)