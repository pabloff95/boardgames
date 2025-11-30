from rest_framework import status
from .models import User
from game.models import Game
import os
import pytest


@pytest.fixture
def user1():
    return User.objects.create_user(
        username="user1", email="user1@example.com", password="password"
    )


@pytest.fixture
def user2():
    return User.objects.create_user(
        username="user2", email="user2@example.com", password="password"
    )


@pytest.fixture
def game1():
    return Game.objects.create(
        name="Saved Game",
        description="desc",
        min_length=10,
        max_length=20,
    )


@pytest.fixture
def game2():
    return Game.objects.create(
        name="AddOne",
        description="desc",
        min_length=5,
        max_length=15,
    )


@pytest.mark.django_db
class TestUserAPITestCase:
    def test_get_users(self, auth_client, user1, user2):
        response = auth_client.get(f"/{os.getenv('API_NAMESPACE')}users/")

        assert response.status_code == status.HTTP_200_OK

        assert len(response.data) == 3  # 2 + the logged user

    def test_get_user_by_id(self, auth_client, user1):
        response = auth_client.get(f"/{os.getenv('API_NAMESPACE')}users/{user1.id}/")

        assert response.status_code == status.HTTP_200_OK

        assert response.data["id"] == user1.id
        assert response.data["username"] == user1.username
        assert response.data["email"] == user1.email

    def test_post_user(self, auth_client, user1, user2):
        data = {"username": "newuser", "email": "new@example.com"}
        response = auth_client.post(
            f"/{os.getenv('API_NAMESPACE')}users/", data, format="json"
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert User.objects.count() == 4  # 3 + the logged user

    def test_patch_user_email(self, auth_client, user1):
        data = {"email": "updated@example.com"}
        response = auth_client.patch(
            f"/{os.getenv('API_NAMESPACE')}users/{user1.id}/", data, format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        user1.refresh_from_db()

        assert user1.email == data["email"]

    def test_update_user(self, auth_client, user1):
        data = {
            "username": "updatedname",
            "email": "updated2@example.com",
            "saved_games": [],
        }
        response = auth_client.put(
            f"/{os.getenv('API_NAMESPACE')}users/{user1.id}/", data, format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        user1.refresh_from_db()

        assert user1.username == data["username"]
        assert user1.email == data["email"]

    def test_delete_user(self, auth_client, user1, user2):
        users = auth_client.get(f"/{os.getenv('API_NAMESPACE')}users/")

        response = auth_client.delete(f"/{os.getenv('API_NAMESPACE')}users/{user2.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert User.objects.count() == len(users.data) - 1

    def test_patch_saved_games(self, auth_client, user1, game1):
        data = {"saved_games": [game1.id]}
        response = auth_client.patch(
            f"/{os.getenv('API_NAMESPACE')}users/{user1.id}/", data, format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        user1.refresh_from_db()
        assert game1 in user1.saved_games.all()

    def test_add_saved_games_success_single(self, auth_client, user1, game2):
        data = {"saved_games": [game2.id]}
        response = auth_client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{user1.id}/add_saved_games/",
            data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        user1.refresh_from_db()
        assert game2 in user1.saved_games.all()

    def test_add_saved_games_success_multiple(self, auth_client, user1, game1, game2):
        data = {"saved_games": [game1.id, game2.id]}
        response = auth_client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{user1.id}/add_saved_games/",
            data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        user1.refresh_from_db()

        assert game1 in user1.saved_games.all()
        assert game2 in user1.saved_games.all()

    def test_add_saved_games_missing_field(self, auth_client, user1):
        response = auth_client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{user1.id}/add_saved_games/",
            {},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert '"saved_games" is required.' in response.data["saved_games"][0]

    def test_add_saved_games_not_a_list(self, auth_client, user1):
        response = auth_client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{user1.id}/add_saved_games/",
            {"saved_games": "notalist"},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert '"saved_games" is required.' in response.data["saved_games"][0]

    def test_add_saved_games_empty_list(self, auth_client, user1):
        response = auth_client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{user1.id}/add_saved_games/",
            {"saved_games": []},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert '"saved_games" is required.' in response.data["saved_games"][0]

    def test_add_saved_games_non_numeric_ids(self, auth_client, user1):
        response = auth_client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{user1.id}/add_saved_games/",
            {"saved_games": ["abc"]},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            '"saved_games" must contain only numeric IDs.'
            in response.data["saved_games"][0]
        )

    def tes(self, auth_client, user1, game1):
        user1.saved_games.add(game1)
        game_ids = [game1.id, game1.id]

        data = {"saved_games": game_ids}
        response = auth_client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{user1.id}/add_saved_games/",
            data,
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            f'Duplicated game id in received "saved_games": {game_ids}'
            in response.data["saved_games"][0]
        )

    def test_add_saved_games_already_saved(self, auth_client, game1, user1):
        user1.saved_games.add(game1)

        data = {"saved_games": [game1.id]}
        response = auth_client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{user1.id}/add_saved_games/",
            data,
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(game1.id) in response.data["saved_games"][0]
        assert "Games already saved" in response.data["saved_games"][0]

    def test_add_saved_games_invalid_game_ids(self, auth_client, user1):
        missing_id = 999999
        data = {"saved_games": [missing_id]}
        response = auth_client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{user1.id}/add_saved_games/",
            data,
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(missing_id) in response.data["saved_games"][0]
        assert "Invalid game IDs" in response.data["saved_games"][0]

    def test_remove_saved_games_success_single(self, auth_client, user1, game1):
        user1.saved_games.add(game1)

        data = {"saved_games": [game1.id]}
        response = auth_client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{user1.id}/remove_saved_games/",
            data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        user1.refresh_from_db()
        assert game1 not in user1.saved_games.all()

    def test_remove_saved_games_success_multiple(
        self, auth_client, user1, game1, game2
    ):
        user1.saved_games.add(game1, game2)

        data = {"saved_games": [game1.id, game2.id]}
        response = auth_client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{user1.id}/remove_saved_games/",
            data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        user1.refresh_from_db()
        assert game1 not in user1.saved_games.all()
        assert game2 not in user1.saved_games.all()

    def test_remove_saved_games_missing_field(self, auth_client, user1):
        response = auth_client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{user1.id}/remove_saved_games/",
            {},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert '"saved_games" is required.' in response.data["saved_games"][0]

    def test_remove_saved_games_not_a_list(self, auth_client, user1):
        response = auth_client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{user1.id}/remove_saved_games/",
            {"saved_games": "notalist"},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert '"saved_games" is required.' in response.data["saved_games"][0]

    def test_remove_saved_games_empty_list(self, auth_client, user1):
        response = auth_client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{user1.id}/remove_saved_games/",
            {"saved_games": []},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert '"saved_games" is required.' in response.data["saved_games"][0]

    def test_remove_saved_games_non_numeric_ids(self, auth_client, user1):
        response = auth_client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{user1.id}/remove_saved_games/",
            {"saved_games": ["abc"]},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            '"saved_games" must contain only numeric IDs.'
            in response.data["saved_games"][0]
        )

    def test_remove_saved_games_duplicated_ids_in_request(
        self, auth_client, user1, game1
    ):
        user1.saved_games.add(game1)
        game_ids = [game1.id, game1.id]

        data = {"saved_games": game_ids}
        response = auth_client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{user1.id}/remove_saved_games/",
            data,
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            f'Duplicated game id in received "saved_games": {game_ids}'
            in response.data["saved_games"][0]
        )

    def test_remove_saved_games_not_existing_in_saved_games(
        self, auth_client, user1, game1
    ):
        data = {"saved_games": [game1.id]}
        response = auth_client.post(
            f"/{os.getenv('API_NAMESPACE')}users/{user1.id}/remove_saved_games/",
            data,
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(game1.id) in response.data["saved_games"][0]
        assert (
            "Games do not exist in the user saved games"
            in response.data["saved_games"][0]
        )
