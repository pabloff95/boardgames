from .models import Game, GameRules
from rest_framework import viewsets
from .serializers import GameSerializer, GameRulesSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GameFilter, GameRulesFilter


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GameFilter


class GameRulesViewSet(viewsets.ModelViewSet):
    queryset = GameRules.objects.all()
    serializer_class = GameRulesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GameRulesFilter
