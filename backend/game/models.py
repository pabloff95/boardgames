from django.db import models
from django.core.validators import MinValueValidator


class Game(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    min_length = models.IntegerField(validators=[MinValueValidator(0)])
    max_length = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.name}"
