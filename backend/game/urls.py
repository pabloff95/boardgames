from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameViewSet, GameRulesViewSet, GameImageViewSet

router = DefaultRouter()
router.register(r"games", GameViewSet, basename="game")
router.register(r"game_rules", GameRulesViewSet, basename="game_rules")
router.register(r"game_images", GameImageViewSet, basename="game_images")

urlpatterns = [
    path("", include(router.urls)),
]
