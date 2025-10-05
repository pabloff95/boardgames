from django.forms.models import model_to_dict
from django.http import JsonResponse
from .models import Game


def index(request):
    filters = {}

    min_length = request.GET.get("min_length")
    max_length = request.GET.get("max_length")

    if min_length is not None:
        try:
            filters["min_length__gte"] = int(min_length)
        except ValueError:
            return JsonResponse(
                {"Error": '"min_length" must be a valid number'}, status=400
            )

    if max_length is not None:
        try:
            filters["max_length__lte"] = int(max_length)
        except ValueError:
            return JsonResponse(
                {"Error": '"max_length" must be a valid number'}, status=400
            )

    games = Game.objects.filter(**filters).values()
    games_list = list(games)
    return JsonResponse(games_list, safe=False)


def game(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return JsonResponse({"Error": "Game not found"}, status=404)

    return JsonResponse(model_to_dict(game))
