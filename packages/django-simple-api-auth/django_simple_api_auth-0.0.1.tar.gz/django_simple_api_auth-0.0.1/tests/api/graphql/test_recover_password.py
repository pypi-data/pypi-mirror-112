import json

import pytest
from rest_framework import status

from django_simple_api_auth.business_logic.user_create import UserCreate
from tests.api.graphql.common import BaseGraphQLTestCase


@pytest.mark.django_db
class TestRecoverPassword(BaseGraphQLTestCase):

    def test_recover_password(self):
        username = "test@test.com"
        data = {
            "email": username
        }
        create_data = {
            "username": username,
            "password": "password",
        }
        UserCreate(**create_data).execute()
        mutation = '''
            mutation userPasswordRecovery($input: UserPasswordRecoveryMutationInput!){
                userPasswordRecovery(input: $input){
                    ok,
                }
            }
        '''
        operation_name = 'userPasswordRecovery'
        response = self.query(mutation, operation_name=operation_name, input_data=data)
        assert response.status_code == status.HTTP_200_OK
        content = json.loads(response.content)
        assert 'errors' not in content
