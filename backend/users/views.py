from .models import User
from rest_framework import viewsets, status
from .serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from game.models import Game
from game.utils.validations import get_game_ids, get_games
from rest_framework.exceptions import ValidationError


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]

    @action(detail=True, methods=["post"])
    def add_saved_games(self, request, pk=None):
        """
        Endpoint: POST /users/{id}/add_saved_games/
        Example body: { "saved_games": [1,2] }
        """
        user = self.get_object()
        new_saved_games = request.data.get("saved_games")

        user_saved_games_ids = set(user.saved_games.values_list("id", flat=True))
        new_user_saved_games_ids = get_game_ids(new_saved_games)

        duplicate_ids = new_user_saved_games_ids & user_saved_games_ids
        if duplicate_ids:
            raise ValidationError(
                {"saved_games": [f"Games already saved: {list(duplicate_ids)}"]}
            )

        new_games = get_games(new_user_saved_games_ids)

        user.saved_games.add(*new_games)

        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def remove_saved_games(self, request, pk=None):
        """
        Endpoint: POST /users/{id}/remove_saved_games/
        Example body: { "saved_games": [1,2] }
        """
        user = self.get_object()
        games_to_remove = request.data.get("saved_games")

        user_saved_games_ids = set(user.saved_games.values_list("id", flat=True))
        games_to_remove_ids = get_game_ids(games_to_remove)

        different_ids = games_to_remove_ids - user_saved_games_ids
        if different_ids:
            raise ValidationError(
                {
                    "saved_games": [
                        f"Games do not exist in the user saved games: {list(different_ids)}"
                    ]
                }
            )

        games = get_games(games_to_remove_ids)

        user.saved_games.remove(*games)

        serializer = self.get_serializer(user)
        return Response(serializer.data)
