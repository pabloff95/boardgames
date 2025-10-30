from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from game.models import Game
from users.models import User


class Review(models.Model):
    user = models.ForeignKey(
        User,
        blank=False,
        on_delete=models.CASCADE,
    )
    game = models.ForeignKey(
        Game,
        blank=False,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ("user", "game")

    def __str__(self):
        return f"{self.user} - {self.game} ({self.score})"
