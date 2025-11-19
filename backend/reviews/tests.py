from tests.base import AuthenticatedAPITestCase
from rest_framework import status
from .models import Review
from users.models import User
from game.models import Game
import os


class ReviewAPITestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()

        self.user1 = User.objects.create_user(
            username="testuser_1", password="password123"
        )

        self.game1 = Game.objects.create(
            name="Game 1",
            description="Dummy description",
            min_length=10,
            max_length=20,
        )
        self.game2 = Game.objects.create(
            name="Game 2",
            description="Dummy description",
            min_length=30,
            max_length=60,
        )

        self.review1 = Review.objects.create(
            user=self.user1, game=self.game1, score=1, comment="bad review"
        )
        self.review2 = Review.objects.create(
            user=self.user1, game=self.game2, score=5, comment="good review"
        )

    def test_get_reviews(self):
        response = self.client.get(f"/{os.getenv('API_NAMESPACE')}reviews/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_review_by_id(self):
        response = self.client.get(
            f"/{os.getenv('API_NAMESPACE')}reviews/{self.review1.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.review1.id)
        self.assertEqual(response.data["user"], self.review1.user.id)
        self.assertEqual(response.data["game"], self.review1.game.id)
        self.assertEqual(response.data["score"], self.review1.score)
        self.assertEqual(response.data["comment"], self.review1.comment)

    def test_get_reviews_filtered_by_score(self):
        response = self.client.get(
            f"/{os.getenv('API_NAMESPACE')}reviews/", {"score": self.review1.score}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.review1.id)

    def test_get_reviews_filtered_by_user(self):
        response = self.client.get(
            f"/{os.getenv('API_NAMESPACE')}reviews/", {"user": self.user1.id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["id"], self.review1.id)
        self.assertEqual(response.data[1]["id"], self.review2.id)

    def test_get_reviews_filtered_by_game(self):
        response = self.client.get(
            f"/{os.getenv('API_NAMESPACE')}reviews/", {"game": self.game1.id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.review1.id)

    def test_post_review(self):
        data = {
            "user": self.user.id,
            "game": self.game1.id,
            "score": 4,
            "comment": "nice",
        }
        response = self.client.post(
            f"/{os.getenv('API_NAMESPACE')}reviews/", data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 3)

    def test_patch_review_description(self):
        data = {"comment": "Updated comment"}
        response = self.client.patch(
            f"/{os.getenv('API_NAMESPACE')}reviews/{self.review1.id}/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review1.refresh_from_db()
        self.assertEqual(self.review1.comment, data["comment"])

    def test_update_review_fields(self):
        data = {
            "user": self.user.id,
            "game": self.game2.id,
            "score": 3,
            "comment": "Updated",
        }
        response = self.client.put(
            f"/{os.getenv('API_NAMESPACE')}reviews/{self.review2.id}/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review2.refresh_from_db()
        self.assertEqual(self.review2.user.id, data["user"])
        self.assertEqual(self.review2.game.id, data["game"])
        self.assertEqual(self.review2.score, data["score"])
        self.assertEqual(self.review2.comment, data["comment"])

    def test_delete_review(self):
        response = self.client.delete(
            f"/{os.getenv('API_NAMESPACE')}reviews/{self.review2.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 1)

    def test_get_good_reviews(self):
        response = self.client.get(
            f"/{os.getenv('API_NAMESPACE')}reviews/good_reviews/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue(all(r["score"] >= 4 for r in response.data))

    def test_get_bad_reviews(self):
        response = self.client.get(f"/{os.getenv('API_NAMESPACE')}reviews/bad_reviews/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue(all(r["score"] <= 2 for r in response.data))
