from django.contrib import admin
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_filter = ["name", "url", "extension"]
    search_fields = ["name", "id", "extension"]
    list_display = ["id", "name", "extension", "file_location"]
    readonly_fields = ["type"]
