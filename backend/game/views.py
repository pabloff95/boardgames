from django.http import JsonResponse
from .models import Game


def index(request):
    games = Game.objects.all().values(
        "id", "name", "description", "min_length", "max_length"
    )

    games_list = list(games)
    return JsonResponse(games_list, safe=False)
