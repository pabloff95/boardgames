import django_filters
from .models import Game, GameRules, GameImage


class GameFilter(django_filters.FilterSet):
    min_length = django_filters.NumberFilter(field_name="min_length", lookup_expr="gte")
    max_length = django_filters.NumberFilter(field_name="max_length", lookup_expr="lte")
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    description = django_filters.CharFilter(
        field_name="description", lookup_expr="icontains"
    )

    class Meta:
        model = Game
        fields = [
            "name",
            "description",
            "min_length",
            "max_length",
            "created_at",
            "updated_at",
        ]


class GameRulesFilter(django_filters.FilterSet):
    version = django_filters.CharFilter(field_name="version", lookup_expr="icontains")

    class Meta:
        model = GameRules
        fields = ["game", "version", "content", "created_at", "updated_at"]


class GameImageFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = GameImage
        fields = ["id", "name"]
