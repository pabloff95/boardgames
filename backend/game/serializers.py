from rest_framework import serializers
from .models import Game, GameRules


class GameRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRules
        fields = ["game", "version", "content", "created_at", "updated_at"]


class GameSerializer(serializers.ModelSerializer):
    rules = GameRulesSerializer(many=True, read_only=True)

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
        ]
