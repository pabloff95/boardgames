from rest_framework import serializers
from .models import Game, GameRules, GameImage


class GameRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRules
        fields = ["id", "game", "version", "content", "created_at", "updated_at"]


class GameImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameImage
        fields = ["id", "name", "type", "file"]


class GameSerializer(serializers.ModelSerializer):
    rules = GameRulesSerializer(many=True, read_only=True)
    images = GameImageSerializer(many=True, read_only=True)
    saved_by_count = serializers.IntegerField(read_only=True)
    average_score = serializers.FloatField(read_only=True)

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
            "images",
        ]


class GamesOfTheWeekQuerySerializer(serializers.Serializer):
    days_range = serializers.IntegerField(default=7, min_value=1)
    games_limit = serializers.IntegerField(default=5, min_value=1)
