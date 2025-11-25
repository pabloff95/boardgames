from .models import Game, GameRules
from rest_framework import viewsets
from .serializers import GameSerializer, GameRulesSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GameFilter, GameRulesFilter
from rest_framework.permissions import AllowAny
from rest_framework.filters import OrderingFilter
from django.db.models import Avg, Count, FloatField
from django.db.models.functions import Coalesce
from .utils.game_sorts import get_games_of_the_week
from rest_framework.decorators import action


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = GameFilter

    ordering_fields = ["average_score", "name", "saved_by_count"]
    ordering = ["name"]

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        ordering = self.request.query_params.get("ordering", "")
        if "average_score" in ordering:
            queryset = queryset.exclude(average_score=None)

        return queryset

    def get_permissions(self):
        if self.action in ["retrieve", "list"]:
            return [AllowAny()]

        return super().get_permissions()

    def get_queryset(self):
        return Game.objects.all().annotate(
            average_score=Coalesce(
                Avg("review__score"), None, output_field=FloatField()
            ),
            saved_by_count=Count("saved_by", distinct=True),
        )

    @action(detail=False, methods=["get"])
    def games_of_the_week(self, request):
        return get_games_of_the_week(self)


class GameRulesViewSet(viewsets.ModelViewSet):
    queryset = GameRules.objects.all()
    serializer_class = GameRulesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GameRulesFilter

    def get_permissions(self):
        if self.action in ["retrieve", "list"]:
            return [AllowAny()]

        return super().get_permissions()
