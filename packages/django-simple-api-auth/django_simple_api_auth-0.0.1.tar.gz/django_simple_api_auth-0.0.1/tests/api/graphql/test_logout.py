import json

import pytest
from rest_framework import status

from django_simple_api_auth.business_logic.user_create import UserCreate
from tests.api.graphql.common import BaseGraphQLTestCase


@pytest.mark.django_db
class TestLogout(BaseGraphQLTestCase):

    def test_logout(self):
        data = {
            "username": "test@test.com",
            "password": "password",
        }
        user = UserCreate(**data).execute()
        self.client.force_login(user)

        mutation = '''
            mutation userLogout($input: UserLogoutMutationInput!){
                userLogout(input: $input){
                    ok,
                    errors,
                }
            }
        '''
        operation_name = 'userLogout'
        data = {
            "clientMutationId": "id",
        }
        response = self.query(mutation, operation_name=operation_name, input_data=data)
        assert response.status_code == status.HTTP_200_OK
        content = json.loads(response.content)
        assert 'errors' not in content
        assert not response.cookies.get('sessionid').value
