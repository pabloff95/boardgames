from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ["saved_games"]}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ["saved_games"]}),)
    search_fields = ["username", "email", "id"]
    ordering = ["id"]
