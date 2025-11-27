from reviews.models import Review
from game.models import Game
import datetime
from functools import reduce
from rest_framework.response import Response
from django.db.models import Avg, Q


def get_top_scoring_games_in_days_range(
    self,
    days_range: int,
    games_limit: int,
) -> Response:
    today = datetime.datetime.today()
    one_week_ago = (today - datetime.timedelta(days=days_range)).date()

    week_filter = Q(
        review__created_at__date__range=(
            one_week_ago.strftime("%Y-%m-%d"),
            today.strftime("%Y-%m-%d"),
        )
    )
    games = (
        Game.objects.annotate(
            average_score=Avg("review__score", filter=week_filter),
        )
        .exclude(average_score__isnull=True)
        .order_by("-average_score")[:games_limit]
    )

    return Response(self.get_serializer(games, many=True).data)
