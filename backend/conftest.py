import pytest
from rest_framework.test import APIClient
from users.models import User


@pytest.fixture
def api_client():
    """Provides an unauthenticated API client"""
    return APIClient()


@pytest.fixture
def test_user():
    """Creates the default test user"""
    return User.objects.create_user(username="testuser", password="password2025")


@pytest.fixture
def auth_client(api_client, test_user):
    """Provides an authenticated API client with test_user"""
    api_client.force_authenticate(test_user)
    api_client.user = test_user
    return api_client
