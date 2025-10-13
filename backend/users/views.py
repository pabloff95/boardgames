from .models import User
from rest_framework import viewsets, status
from .serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from game.models import Game


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

        if not isinstance(new_saved_games, list) or len(new_saved_games) == 0:
            return Response(
                {"error": '"saved_games" is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_saved_games_ids = set(user.saved_games.values_list("id", flat=True))
        try:
            new_user_saved_games_ids = set(map(int, new_saved_games))
        except (ValueError, TypeError):
            return Response(
                {"error": '"saved_games" must contain only numeric IDs.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(new_user_saved_games_ids) != len(new_saved_games):
            return Response(
                {
                    "error": f'Duplicated game id in received "saved_games": {new_saved_games}'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        duplicate_ids = new_user_saved_games_ids & user_saved_games_ids
        if duplicate_ids:
            return Response(
                {"error": f"Games already saved: {list(duplicate_ids)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_games = list(Game.objects.filter(pk__in=new_user_saved_games_ids))
        if len(new_games) != len(new_user_saved_games_ids):
            missing = new_user_saved_games_ids - {game.id for game in new_games}
            return Response(
                {"error": f"Invalid game IDs: {list(missing)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

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

        if not isinstance(games_to_remove, list) or len(games_to_remove) == 0:
            return Response(
                {"error": '"saved_games" is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_saved_games_ids = set(user.saved_games.values_list("id", flat=True))
        try:
            games_to_remove_ids = set(map(int, games_to_remove))
        except (ValueError, TypeError):
            return Response(
                {"error": '"saved_games" must contain only numeric IDs.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(games_to_remove_ids) != len(games_to_remove):
            return Response(
                {
                    "error": f'Duplicated game id in received "saved_games": {games_to_remove}'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        different_ids = games_to_remove_ids - user_saved_games_ids
        if different_ids:
            return Response(
                {
                    "error": f"Games do not exist in the user saved games: {list(different_ids)}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        games = list(Game.objects.filter(pk__in=games_to_remove_ids))
        if len(games) != len(games_to_remove_ids):
            missing = games_to_remove_ids - {game.id for game in games}
            return Response(
                {"error": f"Invalid game IDs: {list(missing)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.saved_games.remove(*games)

        serializer = self.get_serializer(user)
        return Response(serializer.data)
