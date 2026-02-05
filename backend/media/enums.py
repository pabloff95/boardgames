from django.db import models


class MediaType(models.TextChoices):
    IMAGE = "image", "image"


class ImageLocations(models.TextChoices):
    GAMES_IMG = "games_img", "games_img"
