from tests.base import AuthenticatedAPITestCase
from rest_framework import status
from game.models import Game
from reviews.models import Review
from users.models import User
import os


class GameAPITestCase(AuthenticatedAPITestCase):
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
            name="Game 2",
            description="Dummy description text",
            min_length=30,
            max_length=60,
            created_at="2025-10-05T14:30:00Z",
            updated_at="2025-10-05T17:54:30.084920Z",
        )

        # Create users
        self.user1 = User.objects.create(
            username="user1", email="user1@example.com", password="password"
        )
        self.user2 = User.objects.create(
            username="user2", email="user2@example.com", password="password"
        )
        self.user3 = User.objects.create(
            username="user3", email="user3@example.com", password="password"
        )

        # Create review objects
        self.review1 = Review.objects.create(game=self.game1, score=2, user=self.user1)
        self.review2 = Review.objects.create(game=self.game1, score=4, user=self.user2)
        self.review3 = Review.objects.create(game=self.game1, score=3, user=self.user3)

    def test_get_games(self):
        response = self.client.get(f"/{os.getenv("API_NAMESPACE")}games/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 2)

    def test_games_default_order_is_by_name(self):
        self.game3 = Game.objects.create(
            name="ZZ Game 3",
            description="Dummy description text",
            min_length=30,
            max_length=60,
            created_at="2025-10-05T14:30:00Z",
            updated_at="2025-10-05T17:54:30.084920Z",
        )
        self.game4 = Game.objects.create(
            name="AA Game 3",
            description="Dummy description text",
            min_length=30,
            max_length=60,
            created_at="2025-10-05T14:30:00Z",
            updated_at="2025-10-05T17:54:30.084920Z",
        )

        response = self.client.get(f"/{os.getenv("API_NAMESPACE")}games/")
        game1, game2, game3, game4 = response.data

        self.assertEqual(len(response.data), 4)
        self.assertEqual(game1["id"], self.game4.id)
        self.assertEqual(game2["id"], self.game1.id)
        self.assertEqual(game3["id"], self.game2.id)
        self.assertEqual(game4["id"], self.game3.id)

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
        self.assertEqual(response.data[0]["name"], self.game2.name)

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

    def test_open_endpoints(self):
        self.client.logout()

        # Allowed requests
        response_list = self.client.get(f"/{os.getenv("API_NAMESPACE")}games/")
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)

        response_retrieve = self.client.get(
            f"/{os.getenv("API_NAMESPACE")}games/{self.game1.id}/"
        )
        self.assertEqual(response_retrieve.status_code, status.HTTP_200_OK)

        # Forbidden requests
        response_post = self.client.post(
            f"/{os.getenv("API_NAMESPACE")}games/",
            {
                "name": "Monopoly",
                "description": "Dummy description text",
                "min_length": 60,
                "max_length": 180,
            },
            format="json",
        )
        self.assertEqual(response_post.status_code, status.HTTP_401_UNAUTHORIZED)

        response_patch = self.client.patch(
            f"/{os.getenv("API_NAMESPACE")}games/{self.game1.id}/",
            {"description": "Updated description"},
            format="json",
        )
        self.assertEqual(response_patch.status_code, status.HTTP_401_UNAUTHORIZED)

        response_put = self.client.put(
            f"/{os.getenv("API_NAMESPACE")}games/{self.game1.id}/",
            {
                "name": "Updated name",
                "description": "Updated description",
                "min_length": 100,
                "max_length": 200,
            },
            format="json",
        )
        self.assertEqual(response_put.status_code, status.HTTP_401_UNAUTHORIZED)

        response_delete = self.client.delete(
            f"/{os.getenv("API_NAMESPACE")}games/{self.game2.id}/"
        )
        self.assertEqual(response_delete.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_games_average_score(self):
        response = self.client.get(f"/{os.getenv("API_NAMESPACE")}games/")

        game1_response, game2_response = response.data
        self.assertEqual(game1_response["id"], self.game1.id)
        self.assertEqual(game1_response["average_score"], 3)

        self.assertEqual(game2_response["id"], self.game2.id)
        self.assertEqual(game2_response["average_score"], None)

    def test_games_ordered_by_average_score(self):
        self.game3 = Game.objects.create(
            name="Game 3",
            description="Dummy description text",
            min_length=30,
            max_length=60,
            created_at="2025-10-05T14:30:00Z",
            updated_at="2025-10-05T17:54:30.084920Z",
        )
        self.review4 = Review.objects.create(game=self.game3, score=1, user=self.user1)

        response_desc = self.client.get(
            f"/{os.getenv("API_NAMESPACE")}games/?ordering=-average_score/"
        )

        game1_response_desc, game2_response_desc = response_desc.data

        self.assertEqual(
            len(response_desc.data), 2
        )  # Games with "average_score" == None are filtered out (self.game2)
        self.assertEqual(game1_response_desc["id"], self.game1.id)
        self.assertEqual(game2_response_desc["id"], self.game3.id)

        response_asc = self.client.get(
            f"/{os.getenv("API_NAMESPACE")}games/?ordering=average_score"
        )

        game1_response_asc, game2_response_asc = response_asc.data

        self.assertEqual(len(response_asc.data), 2)
        self.assertEqual(game1_response_asc["id"], self.game3.id)
        self.assertEqual(game2_response_asc["id"], self.game1.id)
