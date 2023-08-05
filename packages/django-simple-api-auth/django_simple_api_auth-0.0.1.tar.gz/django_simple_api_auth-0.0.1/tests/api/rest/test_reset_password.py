import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from django_simple_api_auth.business_logic.user_create import UserCreate


@pytest.mark.django_db
class TestResetPassword(APITestCase):
    def setUp(self):
        self.url = reverse('api:v1.0:users-reset-password')

    def test_reset_password(self):
        username = "test@test.com"
        password = "password"
        create_data = {
            "username": username,
            "password": password,
        }
        user = UserCreate(**create_data).execute()
        assert user.check_password(password)
        id = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        new_password = "new_password"
        data = {
            "id": id,
            "token": token,
            "password": new_password
        }
        response = self.client.post(self.url, data=data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert get_user_model().objects.get(id=user.id).check_password(new_password)
