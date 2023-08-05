import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from django_simple_api_auth.business_logic.user_create import UserCreate


@pytest.mark.django_db
class TestLogout(APITestCase):
    def setUp(self):
        self.login_url = reverse('api:v1.0:users-login')
        self.logout = reverse('api:v1.0:users-logout')

    def test_logout(self):
        data = {
            "username": "test@test.com",
            "password": "password",
        }
        user = UserCreate(**data).execute()
        self.client.force_login(user)
        response = self.client.post(self.logout, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'csrftoken' not in response.cookies.keys()
        assert not response.cookies.get('sessionid').value
