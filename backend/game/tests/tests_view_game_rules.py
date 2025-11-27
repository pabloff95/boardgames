from tests.base import AuthenticatedAPITestCase
from rest_framework import status
from game.models import Game, GameRules
import os


class GameRulesAPITestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()

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

    def test_update_game_rule(self):
        data = {"game": self.game2.id, "version": "v2", "content": "Updated content"}
        response = self.client.put(
            f"/{os.getenv("API_NAMESPACE")}game_rules/{self.rules1.id}/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.rules1.refresh_from_db()

        self.assertEqual(self.rules1.game.id, data["game"])
        self.assertEqual(self.rules1.version, data["version"])
        self.assertEqual(self.rules1.content, data["content"])

    def test_delete_game_rule(self):
        response = self.client.delete(
            f"/{os.getenv("API_NAMESPACE")}game_rules/{self.rules2.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(GameRules.objects.count(), 1)

    def test_open_endpoints(self):
        self.client.logout()

        # Allowed requests
        response_list = self.client.get(f"/{os.getenv("API_NAMESPACE")}game_rules/")
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)

        response_retrieve = self.client.get(
            f"/{os.getenv("API_NAMESPACE")}game_rules/{self.rules1.id}/"
        )
        self.assertEqual(response_retrieve.status_code, status.HTTP_200_OK)

        # Forbidden requests
        response_post = self.client.post(
            f"/{os.getenv("API_NAMESPACE")}game_rules/",
            {
                "game": self.game1.id,
                "version": "v1.1",
                "content": "Additional rules",
            },
            format="json",
        )
        self.assertEqual(response_post.status_code, status.HTTP_401_UNAUTHORIZED)

        response_patch = self.client.patch(
            f"/{os.getenv("API_NAMESPACE")}game_rules/{self.rules1.id}/",
            {"content": "Updated rules content"},
            format="json",
        )
        self.assertEqual(response_patch.status_code, status.HTTP_401_UNAUTHORIZED)

        response_put = self.client.put(
            f"/{os.getenv("API_NAMESPACE")}game_rules/{self.rules1.id}/",
            {"game": self.game2.id, "version": "v2", "content": "Updated content"},
            t="json",
        )
        self.assertEqual(response_put.status_code, status.HTTP_401_UNAUTHORIZED)

        response_delete = self.client.delete(
            f"/{os.getenv("API_NAMESPACE")}game_rules/{self.rules2.id}/"
        )
        self.assertEqual(response_delete.status_code, status.HTTP_401_UNAUTHORIZED)
