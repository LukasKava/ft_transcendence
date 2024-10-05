# user_conf_files/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    list_filter = ['is_staff', 'is_active']  
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('display_name',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
