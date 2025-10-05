from django.contrib import admin
from .models import Game, GameRules


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_filter = ["min_length", "max_length", "created_at", "updated_at"]
    search_fields = ["name", "id"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = [
        (
            "Game",
            {"fields": ["name", "description", "min_length", "max_length"]},
        ),
        (
            "Timestamps",
            {
                "fields": ["created_at", "updated_at"],
            },
        ),
    ]


@admin.register(GameRules)
class GameRulesAdmin(admin.ModelAdmin):
    list_filter = ["game", "created_at", "updated_at"]
    search_fields = ["game__name", "id"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = [
        ("Rules", {"fields": ["game", "version", "content"]}),
        (
            "Timestamps",
            {
                "fields": ["created_at", "updated_at"],
            },
        ),
    ]
