from django.db import models
from .enums import MediaType, Extension


class Media(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    url = models.URLField(max_length=500, null=False, blank=False)
    type = models.CharField(
        choices=MediaType.choices, max_length=20, null=False, blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Image(Media):
    file_key = models.CharField(max_length=255, null=False, blank=False)
    bucket_name = models.CharField(max_length=255, null=False, blank=False)
    extension = models.CharField(
        choices=Extension.choices, max_length=10, null=False, blank=False
    )
    type = models.CharField(
        max_length=20,
        choices=MediaType.choices,
        default=MediaType.IMAGE,
        editable=False,
    )
