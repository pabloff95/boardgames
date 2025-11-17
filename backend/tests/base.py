from rest_framework.test import APITestCase
from users.models import User


class AuthenticatedAPITestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="testuser", password="password2025"
        )
        self.client.force_authenticate(self.user)
