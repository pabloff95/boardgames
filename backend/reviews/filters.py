import django_filters
from .models import Review


class ReviewFilter(django_filters.FilterSet):
    score = django_filters.NumberFilter(field_name="score", lookup_expr="eq")

    game = django_filters.NumberFilter(field_name="game__id", lookup_expr="exact")
    user = django_filters.NumberFilter(field_name="user__id", lookup_expr="exact")

    class Meta:
        model = Review
        fields = [
            "score",
            "game",
            "user",
        ]
