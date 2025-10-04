from django.forms.models import model_to_dict
from django.http import JsonResponse
from .models import Game


def index(request):
    games = Game.objects.all().values(
        "id", "name", "description", "min_length", "max_length"
    )

    games_list = list(games)
    return JsonResponse(games_list, safe=False)


def game(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return JsonResponse({"error": "Game not found"}, status=404)

    return JsonResponse(model_to_dict(game))
