from django.contrib.auth.models import AbstractUser
from django.db import models
from game.models import Game


class User(AbstractUser):
    saved_games = models.ManyToManyField(Game, blank=True, related_name="saved_by")

    def __str__(self):
        return self.username
