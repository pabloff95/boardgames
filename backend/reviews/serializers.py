from rest_framework import serializers
from .models import Review


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["user", "game", "created_at", "updated_at", "score", "comment"]
