from rest_framework import serializers
from .models import Game, GameRules
from reviews.models import Review
from functools import reduce


class GameRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRules
        fields = ["id", "game", "version", "content", "created_at", "updated_at"]


class GameSerializer(serializers.ModelSerializer):
    rules = GameRulesSerializer(many=True, read_only=True)
    saved_by_count = serializers.SerializerMethodField()
    average_score = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            "id",
            "name",
            "description",
            "min_length",
            "max_length",
            "created_at",
            "updated_at",
            "rules",
            "saved_by_count",
            "average_score",
        ]

    def get_saved_by_count(self, obj):
        return obj.saved_by.count()

    def get_average_score(self, obj):
        game_reviews = Review.objects.filter(game=obj.id)

        number_of_reviews = len(game_reviews)
        if number_of_reviews == 0:
            return None

        return (
            reduce(
                lambda score, acc_score: score + acc_score,
                [review.score for review in game_reviews],
                0,
            )
            / number_of_reviews
        )
