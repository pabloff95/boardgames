from django.db import models


class MediaType(models.TextChoices):
    IMAGE = "image", "Image"


class Extension(models.TextChoices):
    PNG = "png", "PNG"
    JPG = "jpg", "JPG"
    JPEG = "jpeg", "JPEG"
