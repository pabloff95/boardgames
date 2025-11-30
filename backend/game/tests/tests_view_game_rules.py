from rest_framework import status
from game.models import Game, GameRules
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
        name="Chess",
        description="Dummy description text",
        min_length=30,
        max_length=60,
        created_at="2025-10-05T14:30:00Z",
        updated_at="2025-10-05T17:54:30.084920Z",
    )


@pytest.fixture
def rules1(game1):
    return GameRules.objects.create(
        game=game1,
        version="v1",
        content="Rules for Game 1 v1",
    )


@pytest.fixture
def rules2(game2):
    return GameRules.objects.create(
        game=game2,
        version="v2",
        content="Rules for Chess v2",
    )


@pytest.mark.django_db
class TestGameRulesAPITestCase:
    def test_get_game_rules(self, auth_client, rules1, rules2):
        response = auth_client.get(f"/{os.getenv("API_NAMESPACE")}game_rules/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_get_game_rule_by_id(self, auth_client, game1, rules1):
        response = auth_client.get(
            f"/{os.getenv("API_NAMESPACE")}game_rules/{rules1.id}/"
        )

        assert response.status_code == status.HTTP_200_OK

        assert response.data["id"] == rules1.id
        assert response.data["game"] == game1.id
        assert response.data["version"] == rules1.version
        assert response.data["content"] == rules1.content

    def test_get_game_rules_filter_version(self, auth_client, rules1, rules2):
        response = auth_client.get(
            f"/{os.getenv("API_NAMESPACE")}game_rules/", {"version": "v2"}
        )

        assert response.status_code == status.HTTP_200_OK

        assert len(response.data) == 1
        assert response.data[0]["version"] == "v2"

    def test_post_game_rule(self, auth_client, game1):
        data = {
            "game": game1.id,
            "version": "v1.1",
            "content": "Additional rules",
        }
        response = auth_client.post(
            f"/{os.getenv("API_NAMESPACE")}game_rules/", data, format="json"
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert GameRules.objects.count() == 1

    def test_patch_game_rule_content(self, auth_client, rules1):
        data = {"content": "Updated rules content"}
        response = auth_client.patch(
            f"/{os.getenv("API_NAMESPACE")}game_rules/{rules1.id}/",
            data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        rules1.refresh_from_db()

        assert rules1.content == data["content"]

    def test_update_game_rule(self, auth_client, game2, rules1):
        data = {"game": game2.id, "version": "v2", "content": "Updated content"}
        response = auth_client.put(
            f"/{os.getenv("API_NAMESPACE")}game_rules/{rules1.id}/",
            data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        rules1.refresh_from_db()

        assert rules1.game.id == data["game"]
        assert rules1.version == data["version"]
        assert rules1.content == data["content"]

    def test_delete_game_rule(self, auth_client, rules1, rules2):
        response = auth_client.delete(
            f"/{os.getenv("API_NAMESPACE")}game_rules/{rules2.id}/"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert GameRules.objects.count() == 1

    def test_open_endpoints(self, auth_client, game1, game2, rules1, rules2):
        auth_client.logout()

        # Allowed requests
        response_list = auth_client.get(f"/{os.getenv("API_NAMESPACE")}game_rules/")
        assert response_list.status_code == status.HTTP_200_OK

        response_retrieve = auth_client.get(
            f"/{os.getenv("API_NAMESPACE")}game_rules/{rules1.id}/"
        )
        assert response_retrieve.status_code == status.HTTP_200_OK

        # Forbidden requests
        response_post = auth_client.post(
            f"/{os.getenv("API_NAMESPACE")}game_rules/",
            {
                "game": game1.id,
                "version": "v1.1",
                "content": "Additional rules",
            },
            format="json",
        )
        assert response_post.status_code == status.HTTP_401_UNAUTHORIZED

        response_patch = auth_client.patch(
            f"/{os.getenv("API_NAMESPACE")}game_rules/{rules1.id}/",
            {"content": "Updated rules content"},
            format="json",
        )
        assert response_patch.status_code == status.HTTP_401_UNAUTHORIZED

        response_put = auth_client.put(
            f"/{os.getenv("API_NAMESPACE")}game_rules/{rules1.id}/",
            {"game": game2.id, "version": "v2", "content": "Updated content"},
            t="json",
        )
        assert response_put.status_code == status.HTTP_401_UNAUTHORIZED

        response_delete = auth_client.delete(
            f"/{os.getenv("API_NAMESPACE")}game_rules/{rules2.id}/"
        )
        assert response_delete.status_code == status.HTTP_401_UNAUTHORIZED
