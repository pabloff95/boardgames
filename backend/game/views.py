from .models import Game, GameRules
from rest_framework import viewsets
from .serializers import GameSerializer, GameRulesSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GameFilter, GameRulesFilter
from rest_framework.permissions import AllowAny


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GameFilter

    def get_permissions(self):
        if self.action in ["retrieve", "list"]:
            return [AllowAny()]

        return super().get_permissions()


class GameRulesViewSet(viewsets.ModelViewSet):
    queryset = GameRules.objects.all()
    serializer_class = GameRulesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GameRulesFilter

    def get_permissions(self):
        if self.action in ["retrieve", "list"]:
            return [AllowAny()]

        return super().get_permissions()
