from django.contrib import admin
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_filter = ["name", "url", "bucket_name", "extension"]
    search_fields = ["name", "id", "bucket_name", "extension"]
    list_display = ["id", "name", "extension", "bucket_name", "file_key"]
    readonly_fields = ["type"]
