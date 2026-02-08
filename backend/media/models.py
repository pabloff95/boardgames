from django.db import models
from .enums import MediaType, ImageLocations
from backend.storage_backends import PrivateMediaStorage
from django.core.validators import FileExtensionValidator


class Media(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    type = models.CharField(
        choices=MediaType.choices, max_length=20, null=False, blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def file_upload_to_path(instance, filename):
    return f"{instance.file_location}/{filename}"


class Image(Media):
    file_location = models.CharField(
        choices=ImageLocations.choices,
        max_length=255,
        null=False,
        blank=False,
        editable=False,
    )
    type = models.CharField(
        max_length=20,
        choices=MediaType.choices,
        default=MediaType.IMAGE,
        editable=False,
    )
    file = models.ImageField(
        storage=PrivateMediaStorage(),
        upload_to=file_upload_to_path,
        null=False,
        blank=False,
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpeg", "jpg"])],
    )

    class Meta:
        abstract = True
