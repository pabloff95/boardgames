from rest_framework import status
from .models import Review
from users.models import User
from game.models import Game
import os
import pytest


@pytest.fixture
def user1():
    return User.objects.create_user(username="testuser_1", password="password123")


@pytest.fixture
def game1():
    return Game.objects.create(
        name="Game 1",
        description="Dummy description",
        min_length=10,
        max_length=20,
    )


@pytest.fixture
def game2():
    return Game.objects.create(
        name="Game 2",
        description="Dummy description",
        min_length=30,
        max_length=60,
    )


@pytest.fixture
def review1(user1, game1):
    return Review.objects.create(user=user1, game=game1, score=1, comment="bad review")


@pytest.fixture
def review2(user1, game2):
    return Review.objects.create(user=user1, game=game2, score=5, comment="good review")


@pytest.mark.django_db
class TestReviewAPITestCase:
    def test_get_reviews(self, auth_client, review1, review2):
        response = auth_client.get(f"/{os.getenv('API_NAMESPACE')}reviews/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_get_review_by_id(self, auth_client, review1):
        response = auth_client.get(
            f"/{os.getenv('API_NAMESPACE')}reviews/{review1.id}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == review1.id
        assert response.data["user"] == review1.user.id
        assert response.data["game"] == review1.game.id
        assert response.data["score"] == review1.score
        assert response.data["comment"] == review1.comment

    def test_get_reviews_filtered_by_score(self, auth_client, review1):
        response = auth_client.get(
            f"/{os.getenv('API_NAMESPACE')}reviews/", {"score": review1.score}
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["id"] == review1.id

    def test_get_reviews_filtered_by_user(self, auth_client, user1, review1, review2):
        response = auth_client.get(
            f"/{os.getenv('API_NAMESPACE')}reviews/", {"user": user1.id}
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]["id"] == review1.id
        assert response.data[1]["id"] == review2.id

    def test_get_reviews_filtered_by_game(self, auth_client, game1, review1):
        response = auth_client.get(
            f"/{os.getenv('API_NAMESPACE')}reviews/", {"game": game1.id}
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["id"] == review1.id

    def test_post_review(self, auth_client, game1):
        data = {
            "user": auth_client.user.id,
            "game": game1.id,
            "score": 4,
            "comment": "nice",
        }
        response = auth_client.post(
            f"/{os.getenv('API_NAMESPACE')}reviews/", data, format="json"
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Review.objects.count() == 1

    def test_patch_review_description(self, auth_client, review1):
        data = {"comment": "Updated comment"}
        response = auth_client.patch(
            f"/{os.getenv('API_NAMESPACE')}reviews/{review1.id}/",
            data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        review1.refresh_from_db()
        assert review1.comment == data["comment"]

    def test_update_review_fields(self, auth_client, game2, review2):
        data = {
            "user": auth_client.user.id,
            "game": game2.id,
            "score": 3,
            "comment": "Updated",
        }
        response = auth_client.put(
            f"/{os.getenv('API_NAMESPACE')}reviews/{review2.id}/",
            data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        review2.refresh_from_db()
        assert review2.user.id == data["user"]
        assert review2.game.id == data["game"]
        assert review2.score == data["score"]
        assert review2.comment == data["comment"]

    def test_delete_review(self, auth_client, review2):
        response = auth_client.delete(
            f"/{os.getenv('API_NAMESPACE')}reviews/{review2.id}/"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Review.objects.count() == 0

    def test_get_good_reviews(self, auth_client, review1, review2):
        response = auth_client.get(
            f"/{os.getenv('API_NAMESPACE')}reviews/good_reviews/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert all(r["score"] >= 4 for r in response.data)

    def test_get_bad_reviews(self, auth_client, review1, review2):
        response = auth_client.get(f"/{os.getenv('API_NAMESPACE')}reviews/bad_reviews/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert all(r["score"] <= 2 for r in response.data)

    def test_open_endpoints(self, auth_client, user1, game1, game2, review1, review2):
        auth_client.logout()

        # Allowed requests
        response_list = auth_client.get(f"/{os.getenv('API_NAMESPACE')}reviews/")
        assert response_list.status_code == status.HTTP_200_OK

        response_list_by_game = auth_client.get(
            f"/{os.getenv('API_NAMESPACE')}reviews/", {"game": game1.id}
        )
        assert response_list_by_game.status_code == status.HTTP_200_OK

        response_retrieve = auth_client.get(
            f"/{os.getenv('API_NAMESPACE')}reviews/{review1.id}/"
        )
        assert response_retrieve.status_code == status.HTTP_200_OK

        # Forbidden requests
        response_list_by_user = auth_client.get(
            f"/{os.getenv('API_NAMESPACE')}reviews/", {"user": user1.id}
        )
        assert response_list_by_user.status_code == status.HTTP_401_UNAUTHORIZED

        response_post = auth_client.post(
            f"/{os.getenv('API_NAMESPACE')}reviews/",
            {
                "user": auth_client.user.id,
                "game": game1.id,
                "score": 4,
                "comment": "nice",
            },
            format="json",
        )
        assert response_post.status_code == status.HTTP_401_UNAUTHORIZED

        response_patch = auth_client.patch(
            f"/{os.getenv('API_NAMESPACE')}reviews/{review1.id}/",
            {"comment": "Updated comment"},
            format="json",
        )
        assert response_patch.status_code == status.HTTP_401_UNAUTHORIZED

        response_put = auth_client.put(
            f"/{os.getenv('API_NAMESPACE')}reviews/{review2.id}/",
            {
                "user": auth_client.user.id,
                "game": game2.id,
                "score": 3,
                "comment": "Updated",
            },
            format="json",
        )
        assert response_put.status_code == status.HTTP_401_UNAUTHORIZED

        response_delete = auth_client.delete(
            f"/{os.getenv('API_NAMESPACE')}reviews/{review2.id}/"
        )
        assert response_delete.status_code == status.HTTP_401_UNAUTHORIZED
