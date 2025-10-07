from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Game, GameRules
import os


class GameAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create sample games
        self.game1 = Game.objects.create(
            name="Game 1",
            description="Dummy description text",
            min_length=5,
            max_length=15,
            created_at="2025-10-05T14:30:00Z",
            updated_at="2025-10-05T17:54:30.084920Z",
        )
        self.game2 = Game.objects.create(
            name="Chess",
            description="Dummy description text",
            min_length=30,
            max_length=60,
            created_at="2025-10-05T14:30:00Z",
            updated_at="2025-10-05T17:54:30.084920Z",
        )

    def test_get_games(self):
        response = self.client.get(f"/{os.getenv("API_NAMESPACE")}games/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 2)

    def test_get_game_by_id(self):
        response = self.client.get(
            f"/{os.getenv("API_NAMESPACE")}games/{self.game1.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["id"], self.game1.id)
        self.assertEqual(response.data["name"], self.game1.name)
        self.assertEqual(response.data["description"], self.game1.description)
        self.assertEqual(response.data["min_length"], self.game1.min_length)
        self.assertEqual(response.data["max_length"], self.game1.max_length)

    def test_get_game_filter_min_length(self):
        response = self.client.get(
            f"/{os.getenv("API_NAMESPACE")}games/", {"min_length": 10}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Chess")

    def test_post_game(self):
        data = {
            "name": "Monopoly",
            "description": "Dummy description text",
            "min_length": 60,
            "max_length": 180,
        }
        response = self.client.post(
            f"/{os.getenv("API_NAMESPACE")}games/", data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Game.objects.count(), 3)

    def test_patch_game_description(self):
        data = {"description": "Updated description"}
        response = self.client.patch(
            f"/{os.getenv("API_NAMESPACE")}games/{self.game1.id}/", data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.game1.refresh_from_db()

        self.assertEqual(self.game1.description, data["description"])

    def test_update_game(self):
        data = {
            "name": "Updated name",
            "description": "Updated description",
            "min_length": 100,
            "max_length": 200,
        }
        response = self.client.put(
            f"/{os.getenv("API_NAMESPACE")}games/{self.game1.id}/", data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.game1.refresh_from_db()

        self.assertEqual(self.game1.name, data["name"])
        self.assertEqual(self.game1.description, data["description"])
        self.assertEqual(self.game1.min_length, data["min_length"])
        self.assertEqual(self.game1.max_length, data["max_length"])

    def test_delete_game(self):
        response = self.client.delete(
            f"/{os.getenv("API_NAMESPACE")}games/{self.game2.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Game.objects.count(), 1)


class GameRulesAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create sample games
        self.game1 = Game.objects.create(
            name="Game 1",
            description="Dummy description text",
            min_length=5,
            max_length=15,
            created_at="2025-10-05T14:30:00Z",
            updated_at="2025-10-05T17:54:30.084920Z",
        )
        self.game2 = Game.objects.create(
            name="Chess",
            description="Dummy description text",
            min_length=30,
            max_length=60,
            created_at="2025-10-05T14:30:00Z",
            updated_at="2025-10-05T17:54:30.084920Z",
        )

        # Create sample rules
        self.rules1 = GameRules.objects.create(
            game=self.game1,
            version="v1",
            content="Rules for Game 1 v1",
        )
        self.rules2 = GameRules.objects.create(
            game=self.game2,
            version="v2",
            content="Rules for Chess v2",
        )

    def test_get_game_rules(self):
        response = self.client.get(f"/{os.getenv("API_NAMESPACE")}game_rules/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_game_rule_by_id(self):
        response = self.client.get(
            f"/{os.getenv("API_NAMESPACE")}game_rules/{self.rules1.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["id"], self.rules1.id)
        self.assertEqual(response.data["game"], self.game1.id)
        self.assertEqual(response.data["version"], self.rules1.version)
        self.assertEqual(response.data["content"], self.rules1.content)

    def test_get_game_rules_filter_version(self):
        response = self.client.get(
            f"/{os.getenv("API_NAMESPACE")}game_rules/", {"version": "v2"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["version"], "v2")

    def test_post_game_rule(self):
        data = {
            "game": self.game1.id,
            "version": "v1.1",
            "content": "Additional rules",
        }
        response = self.client.post(
            f"/{os.getenv("API_NAMESPACE")}game_rules/", data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(GameRules.objects.count(), 3)

    def test_patch_game_rule_content(self):
        data = {"content": "Updated rules content"}
        response = self.client.patch(
            f"/{os.getenv("API_NAMESPACE")}game_rules/{self.rules1.id}/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.rules1.refresh_from_db()

        self.assertEqual(self.rules1.content, data["content"])

    def test_delete_game_rule(self):
        response = self.client.delete(
            f"/{os.getenv("API_NAMESPACE")}game_rules/{self.rules2.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(GameRules.objects.count(), 1)
