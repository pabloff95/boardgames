from rest_framework.exceptions import ValidationError
from game.models import Game


def get_game_ids(games):
    if not isinstance(games, list) or len(games) == 0:
        raise ValidationError({"saved_games": ['"saved_games" is required.']})

    try:
        games_set = set(map(int, games))
    except (ValueError, TypeError):
        raise ValidationError(
            {"saved_games": ['"saved_games" must contain only numeric IDs.']}
        )

    if len(games_set) != len(games):
        raise ValidationError(
            {"saved_games": [f'Duplicated game id in received "saved_games": {games}']}
        )

    return games_set


def get_games(games_ids):
    games = list(Game.objects.filter(pk__in=games_ids))

    if len(games) != len(games_ids):
        missing = games_ids - {game.id for game in games}
        raise ValidationError({"saved_games": [f"Invalid game IDs: {list(missing)}"]})

    return games
