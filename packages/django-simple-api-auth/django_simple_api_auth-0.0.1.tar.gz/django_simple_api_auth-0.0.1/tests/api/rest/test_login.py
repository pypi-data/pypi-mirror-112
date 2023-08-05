import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from django_simple_api_auth.business_logic.user_create import UserCreate


@pytest.mark.django_db
class TestLogin(APITestCase):
    def setUp(self):
        self.url = reverse('api:v1.0:users-login')

    def test_login(self):
        data = {
            "username": "test@test.com",
            "password": "password",
        }
        UserCreate(**data).execute()
        response = self.client.post(self.url, data=data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'csrftoken' in response.cookies.keys()
        assert 'sessionid' in response.cookies.keys()
