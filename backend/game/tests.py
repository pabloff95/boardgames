from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Game


class GameAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create sample games
        self.game1 = Game.objects.create(
            name="Game 1",
            description="Dummy description text",
            min_length=5,
            max_length=15,
        )
        self.game2 = Game.objects.create(
            name="Chess",
            description="Dummy description text",
            min_length=30,
            max_length=60,
        )

    def test_get_games(self):
        response = self.client.get("/api/v1/games/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 2)

    def test_get_game_by_id(self):
        response = self.client.get(f"/api/v1/games/{self.game1.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["id"], self.game1.id)
        self.assertEqual(response.data["name"], self.game1.name)
        self.assertEqual(response.data["description"], self.game1.description)
        self.assertEqual(response.data["min_length"], self.game1.min_length)
        self.assertEqual(response.data["max_length"], self.game1.max_length)

    def test_get_game_filter_min_length(self):
        response = self.client.get("/api/v1/games/", {"min_length": 10})

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
        response = self.client.post("/api/v1/games/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Game.objects.count(), 3)

    def test_patch_game_description(self):
        data = {"description": "Updated description"}
        response = self.client.patch(
            f"/api/v1/games/{self.game1.id}/", data, format="json"
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
            f"/api/v1/games/{self.game1.id}/", data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.game1.refresh_from_db()

        self.assertEqual(self.game1.name, data["name"])
        self.assertEqual(self.game1.description, data["description"])
        self.assertEqual(self.game1.min_length, data["min_length"])
        self.assertEqual(self.game1.max_length, data["max_length"])

    def test_delete_game(self):
        response = self.client.delete(f"/api/v1/games/{self.game2.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Game.objects.count(), 1)
