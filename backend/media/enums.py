from django.db import models


class MediaType(models.TextChoices):
    IMAGE = "image", "Image"


class Extension(models.TextChoices):
    PNG = "png", "PNG"
    JPG = "jpg", "JPG"
    JPEG = "jpeg", "JPEG"


class ImageLocations(models.TextChoices):
    GAMES_IMG = "games_img", "GAMES_IMG"
