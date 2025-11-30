from rest_framework import status
from game.models import Game
from reviews.models import Review
from users.models import User
import os
import pytest


@pytest.fixture
def game1():
    return Game.objects.create(
        name="Game 1",
        description="Dummy description text",
        min_length=5,
        max_length=15,
        created_at="2025-10-05T14:30:00Z",
        updated_at="2025-10-05T17:54:30.084920Z",
    )


@pytest.fixture
def game2():
    return Game.objects.create(
        name="Game 2",
        description="Dummy description text",
        min_length=30,
        max_length=60,
        created_at="2025-10-05T14:30:00Z",
        updated_at="2025-10-05T17:54:30.084920Z",
    )


@pytest.fixture
def game3():
    return Game.objects.create(
        name="ZZ Game 3",
        description="Dummy description text",
        min_length=30,
        max_length=60,
        created_at="2025-10-05T14:30:00Z",
        updated_at="2025-10-05T17:54:30.084920Z",
    )


@pytest.fixture
def game4():
    return Game.objects.create(
        name="AA Game 3",
        description="Dummy description text",
        min_length=30,
        max_length=60,
        created_at="2025-10-05T14:30:00Z",
        updated_at="2025-10-05T17:54:30.084920Z",
    )


@pytest.fixture
def user1():
    return User.objects.create(
        username="user1", email="user1@example.com", password="password"
    )


@pytest.fixture
def user2():
    return User.objects.create(
        username="user2", email="user2@example.com", password="password"
    )


@pytest.fixture
def user3():
    return User.objects.create(
        username="user3", email="user3@example.com", password="password"
    )


@pytest.fixture
def review1(game1, user1):
    return Review.objects.create(game=game1, score=2, user=user1)


@pytest.fixture
def review2(game1, user2):
    return Review.objects.create(game=game1, score=4, user=user2)


@pytest.fixture
def review3(game1, user3):
    return Review.objects.create(game=game1, score=3, user=user3)


@pytest.fixture
def review4(game3, user1):
    return Review.objects.create(game=game3, score=1, user=user1)


@pytest.mark.django_db
class TestGameAPITestCase:
    def test_get_games(self, auth_client, game1, game2):
        response = auth_client.get(f"/{os.getenv("API_NAMESPACE")}games/")

        assert response.status_code == status.HTTP_200_OK

        assert len(response.data) == 2

    def test_games_default_order_is_by_name(
        self, auth_client, game1, game2, game3, game4
    ):
        response = auth_client.get(f"/{os.getenv("API_NAMESPACE")}games/")

        assert len(response.data) == 4
        assert response.data[0]["id"] == game4.id
        assert response.data[1]["id"] == game1.id
        assert response.data[2]["id"] == game2.id
        assert response.data[3]["id"] == game3.id

    def test_get_game_by_id(self, auth_client, game1):
        response = auth_client.get(f"/{os.getenv("API_NAMESPACE")}games/{game1.id}/")

        assert response.status_code == status.HTTP_200_OK

        assert response.data["id"] == game1.id
        assert response.data["name"] == game1.name
        assert response.data["description"] == game1.description
        assert response.data["min_length"] == game1.min_length
        assert response.data["max_length"] == game1.max_length

    def test_get_game_filter_min_length(self, auth_client, game2):
        response = auth_client.get(
            f"/{os.getenv("API_NAMESPACE")}games/", {"min_length": 10}
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == game2.name

    def test_post_game(self, auth_client):
        data = {
            "name": "Monopoly",
            "description": "Dummy description text",
            "min_length": 60,
            "max_length": 180,
        }
        response = auth_client.post(
            f"/{os.getenv("API_NAMESPACE")}games/", data, format="json"
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert Game.objects.count() == 1

    def test_patch_game_description(self, auth_client, game1):
        data = {"description": "Updated description"}
        response = auth_client.patch(
            f"/{os.getenv("API_NAMESPACE")}games/{game1.id}/", data, format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        game1.refresh_from_db()

        assert game1.description == data["description"]

    def test_update_game(self, auth_client, game1):
        data = {
            "name": "Updated name",
            "description": "Updated description",
            "min_length": 100,
            "max_length": 200,
        }
        response = auth_client.put(
            f"/{os.getenv("API_NAMESPACE")}games/{game1.id}/", data, format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        game1.refresh_from_db()

        assert game1.name == data["name"]
        assert game1.description == data["description"]
        assert game1.min_length == data["min_length"]
        assert game1.max_length == data["max_length"]

    def test_delete_game(self, auth_client, game1):
        response = auth_client.delete(f"/{os.getenv("API_NAMESPACE")}games/{game1.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert Game.objects.count() == 0

    def test_open_endpoints(self, auth_client, game1, game2):
        auth_client.logout()

        # Allowed requests
        response_list = auth_client.get(f"/{os.getenv("API_NAMESPACE")}games/")
        assert response_list.status_code == status.HTTP_200_OK

        response_retrieve = auth_client.get(
            f"/{os.getenv("API_NAMESPACE")}games/{game1.id}/"
        )
        assert response_retrieve.status_code == status.HTTP_200_OK

        # Forbidden requests
        response_post = auth_client.post(
            f"/{os.getenv("API_NAMESPACE")}games/",
            {
                "name": "Monopoly",
                "description": "Dummy description text",
                "min_length": 60,
                "max_length": 180,
            },
            format="json",
        )
        assert response_post.status_code == status.HTTP_401_UNAUTHORIZED

        response_patch = auth_client.patch(
            f"/{os.getenv("API_NAMESPACE")}games/{game1.id}/",
            {"description": "Updated description"},
            format="json",
        )
        assert response_patch.status_code == status.HTTP_401_UNAUTHORIZED

        response_put = auth_client.put(
            f"/{os.getenv("API_NAMESPACE")}games/{game1.id}/",
            {
                "name": "Updated name",
                "description": "Updated description",
                "min_length": 100,
                "max_length": 200,
            },
            format="json",
        )
        assert response_put.status_code == status.HTTP_401_UNAUTHORIZED

        response_delete = auth_client.delete(
            f"/{os.getenv("API_NAMESPACE")}games/{game2.id}/"
        )
        assert response_delete.status_code == status.HTTP_401_UNAUTHORIZED

    def test_games_average_score(
        self, auth_client, game1, game2, review1, review2, review3
    ):
        response = auth_client.get(f"/{os.getenv("API_NAMESPACE")}games/")

        game1_response, game2_response = response.data
        assert game1_response["id"] == game1.id
        assert game1_response["average_score"] == 3

        assert game2_response["id"] == game2.id
        assert game2_response["average_score"] == None

    def test_games_ordered_by_average_score(
        self,
        auth_client,
        game1,
        game2,
        game3,
        user1,
        review1,
        review2,
        review3,
        review4,
    ):
        response_desc = auth_client.get(
            f"/{os.getenv("API_NAMESPACE")}games/?ordering=-average_score/"
        )

        game1_response_desc, game2_response_desc = response_desc.data

        assert (
            len(response_desc.data) == 2
        )  # Games with "average_score" == None are filtered out (self, auth_client.game2)
        assert game1_response_desc["id"] == game1.id
        assert game2_response_desc["id"] == game3.id

        response_asc = auth_client.get(
            f"/{os.getenv("API_NAMESPACE")}games/?ordering=average_score"
        )

        game1_response_asc, game2_response_asc = response_asc.data

        assert len(response_asc.data) == 2
        assert game1_response_asc["id"] == game3.id
        assert game2_response_asc["id"] == game1.id
