from django.contrib import admin
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_filter = ["name", "type"]
    search_fields = ["name", "id"]
    list_display = ["id", "name", "type"]
    readonly_fields = ["type", "file_location", "created_at", "updated_at"]
