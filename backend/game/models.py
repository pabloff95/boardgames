from django.db import models
from django.core.validators import MinValueValidator


class Game(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    min_length = models.IntegerField(validators=[MinValueValidator(0)])
    max_length = models.IntegerField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    def has_rules(self):
        return self.rules.exists()


class GameRules(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="rules")
    version = models.CharField(max_length=50, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.game.name} ({self.version})"
