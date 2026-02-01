from django.db import models


class MediaType(models.TextChoices):
    IMAGE = "image", "image"


class Extension(models.TextChoices):
    PNG = "png", "png"
    JPG = "jpg", "jpg"
    JPEG = "jpeg", "jpeg"


class ImageLocations(models.TextChoices):
    GAMES_IMG = "games_img", "games_img"
