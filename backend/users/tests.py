from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User
from game.models import Game
import os


class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

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

        self.assertEqual(len(response.data), 2)

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

        self.assertEqual(User.objects.count(), 3)

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
        response = self.client.delete(
            f"/{os.getenv('API_NAMESPACE')}users/{self.user2.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(User.objects.count(), 1)

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
