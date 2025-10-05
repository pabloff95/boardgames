from .models import Game
from rest_framework import viewsets
from .serializers import GameSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GameFilter


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GameFilter
