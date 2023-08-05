import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status

from django_simple_api_auth.business_logic.user_create import UserCreate
from tests.api.graphql.common import BaseGraphQLTestCase


@pytest.mark.django_db
class TestResetPassword(BaseGraphQLTestCase):

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
        mutation = '''
            mutation userResetPassword($input: UserResetPasswordMutationInput!){
                userResetPassword(input: $input){
                    ok,
                }
            }
        '''
        operation_name = 'userResetPassword'
        response = self.query(mutation, operation_name=operation_name, input_data=data)
        assert response.status_code == status.HTTP_200_OK
        assert get_user_model().objects.get(id=user.id).check_password(new_password)
