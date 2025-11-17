from tests.base import AuthenticatedAPITestCase
from rest_framework import status
from .models import User
from game.models import Game
import os


class UserAPITestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()

        # Create sample users
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password"
        )

    def test_get_users(self):
        response = self.client.get(f"/{os.getenv('API_NAMESPACE')}users/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 3)  # 2 + the logged user

    def test_get_user_by_id(self):
        response = self.client.get(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user1.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["id"], self.user1.id)
        self.assertEqual(response.data["username"], self.user1.username)
        self.assertEqual(response.data["email"], self.user1.email)

    def test_post_user(self):
        data = {"username": "newuser", "email": "new@example.com"}
        response = self.client.post(
            f"/{os.getenv('API_NAMESPACE')}users/", data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(User.objects.count(), 4)  # 3 + the logged user

    def test_patch_user_email(self):
        data = {"email": "updated@example.com"}
        response = self.client.patch(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user1.id}/", data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()

        self.assertEqual(self.user1.email, data["email"])

    def test_update_user(self):
        data = {
            "username": "updatedname",
            "email": "updated2@example.com",
            "saved_games": [],
        }
        response = self.client.put(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user1.id}/", data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()

        self.assertEqual(self.user1.username, data["username"])
        self.assertEqual(self.user1.email, data["email"])

    def test_delete_user(self):
        users = self.client.get(f"/{os.getenv('API_NAMESPACE')}users/")

        response = self.client.delete(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user2.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(User.objects.count(), len(users.data) - 1)

    def test_patch_saved_games(self):
        game = Game.objects.create(
            name="Saved Game",
            description="desc",
            min_length=10,
            max_length=20,
        )

        data = {"saved_games": [game.id]}
        response = self.client.patch(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user1.id}/", data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user1.refresh_from_db()
        self.assertIn(game, self.user1.saved_games.all())

    def test_add_saved_games_success_single(self):
        game = Game.objects.create(
            name="AddOne",
            description="desc",
            min_length=5,
            max_length=15,
        )

        data = {"saved_games": [game.id]}
        response = self.client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user1.id}/add_saved_games/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertIn(game, self.user1.saved_games.all())

    def test_add_saved_games_success_multiple(self):
        g1 = Game.objects.create(
            name="G1", description="d", min_length=5, max_length=10
        )
        g2 = Game.objects.create(
            name="G2", description="d", min_length=5, max_length=10
        )

        data = {"saved_games": [g1.id, g2.id]}
        response = self.client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user1.id}/add_saved_games/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()

        self.assertIn(g1, self.user1.saved_games.all())
        self.assertIn(g2, self.user1.saved_games.all())

    def test_add_saved_games_missing_field(self):
        response = self.client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user1.id}/add_saved_games/",
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('"saved_games" is required.', response.data["saved_games"][0])

    def test_add_saved_games_not_a_list(self):
        response = self.client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user1.id}/add_saved_games/",
            {"saved_games": "notalist"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('"saved_games" is required.', response.data["saved_games"][0])

    def test_add_saved_games_empty_list(self):
        response = self.client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user1.id}/add_saved_games/",
            {"saved_games": []},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('"saved_games" is required.', response.data["saved_games"][0])

    def test_add_saved_games_non_numeric_ids(self):
        response = self.client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user1.id}/add_saved_games/",
            {"saved_games": ["abc"]},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            '"saved_games" must contain only numeric IDs.',
            response.data["saved_games"][0],
        )

    def test_add_saved_games_duplicated_ids_in_request(self):
        game = Game.objects.create(
            name="DupTest", description="d", min_length=5, max_length=10
        )
        game_ids = [game.id, game.id]

        data = {"saved_games": game_ids}
        response = self.client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user1.id}/add_saved_games/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            f'Duplicated game id in received "saved_games": {game_ids}',
            response.data["saved_games"][0],
        )

    def test_add_saved_games_already_saved(self):
        game = Game.objects.create(
            name="Already", description="d", min_length=5, max_length=10
        )
        self.user1.saved_games.add(game)

        data = {"saved_games": [game.id]}
        response = self.client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user1.id}/add_saved_games/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(str(game.id), response.data["saved_games"][0])
        self.assertIn("Games already saved", response.data["saved_games"][0])

    def test_add_saved_games_invalid_game_ids(self):
        missing_id = 999999
        data = {"saved_games": [missing_id]}
        response = self.client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user1.id}/add_saved_games/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(str(missing_id), response.data["saved_games"][0])
        self.assertIn("Invalid game IDs", response.data["saved_games"][0])

    def test_remove_saved_games_success_single(self):
        game = Game.objects.create(
            name="RemoveOne",
            description="desc",
            min_length=5,
            max_length=15,
        )

        self.user1.saved_games.add(game)

        data = {"saved_games": [game.id]}
        response = self.client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user1.id}/remove_saved_games/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertNotIn(game, self.user1.saved_games.all())

    def test_remove_saved_games_success_multiple(self):
        g1 = Game.objects.create(
            name="R1", description="d", min_length=5, max_length=10
        )
        g2 = Game.objects.create(
            name="R2", description="d", min_length=5, max_length=10
        )

        self.user1.saved_games.add(g1, g2)

        data = {"saved_games": [g1.id, g2.id]}
        response = self.client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user1.id}/remove_saved_games/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertNotIn(g1, self.user1.saved_games.all())
        self.assertNotIn(g2, self.user1.saved_games.all())

    def test_remove_saved_games_missing_field(self):
        response = self.client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user1.id}/remove_saved_games/",
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('"saved_games" is required.', response.data["saved_games"][0])

    def test_remove_saved_games_not_a_list(self):
        response = self.client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user1.id}/remove_saved_games/",
            {"saved_games": "notalist"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('"saved_games" is required.', response.data["saved_games"][0])

    def test_remove_saved_games_empty_list(self):
        response = self.client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user1.id}/remove_saved_games/",
            {"saved_games": []},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('"saved_games" is required.', response.data["saved_games"][0])

    def test_remove_saved_games_non_numeric_ids(self):
        response = self.client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user1.id}/remove_saved_games/",
            {"saved_games": ["abc"]},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            '"saved_games" must contain only numeric IDs.',
            response.data["saved_games"][0],
        )

    def test_remove_saved_games_duplicated_ids_in_request(self):
        game = Game.objects.create(
            name="DupRem", description="d", min_length=5, max_length=10
        )

        self.user1.saved_games.add(game)
        game_ids = [game.id, game.id]

        data = {"saved_games": game_ids}
        response = self.client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user1.id}/remove_saved_games/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            f'Duplicated game id in received "saved_games": {game_ids}',
            response.data["saved_games"][0],
        )

    def test_remove_saved_games_not_existing_in_saved_games(self):
        game = Game.objects.create(
            name="NotSaved", description="d", min_length=5, max_length=10
        )

        data = {"saved_games": [game.id]}
        response = self.client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user1.id}/remove_saved_games/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(str(game.id), response.data["saved_games"][0])
        self.assertIn(
            "Games do not exist in the user saved games",
            response.data["saved_games"][0],
        )
