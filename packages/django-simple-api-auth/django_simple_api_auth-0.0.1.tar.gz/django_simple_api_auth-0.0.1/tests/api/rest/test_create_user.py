import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


@pytest.mark.django_db
class TestCreateUser(APITestCase):
    def setUp(self):
        self.url = reverse('api:v1.0:users-list')

    def test_create_user(self):
        data = {
            "username": "test@test.com",
            "password": "password",
        }
        response = self.client.post(self.url, data=data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert get_user_model().objects.count() == 1
