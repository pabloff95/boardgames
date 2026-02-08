from .models import Game, GameRules, GameImage
from rest_framework import viewsets
from .serializers import (
    GameSerializer,
    GameRulesSerializer,
    GamesOfTheWeekQuerySerializer,
    GameImageSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GameFilter, GameRulesFilter, GameImageFilter
from rest_framework.permissions import AllowAny
from rest_framework.filters import OrderingFilter
from django.db.models import Avg, Count, FloatField
from django.db.models.functions import Coalesce
from .utils.game_sorts import get_top_scoring_games_in_days_range
from rest_framework.decorators import action
from rest_framework.response import Response


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
        serializer = GamesOfTheWeekQuerySerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        days_range = serializer.validated_data["days_range"]
        games_limit = serializer.validated_data["games_limit"]

        return get_top_scoring_games_in_days_range(
            self,
            days_range,
            games_limit,
        )


class GameRulesViewSet(viewsets.ModelViewSet):
    queryset = GameRules.objects.all()
    serializer_class = GameRulesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GameRulesFilter

    def get_permissions(self):
        if self.action in ["retrieve", "list"]:
            return [AllowAny()]

        return super().get_permissions()


class GameImageViewSet(viewsets.ModelViewSet):
    queryset = GameImage.objects.all()
    serializer_class = GameImageSerializer
    filterset_class = GameImageFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)
