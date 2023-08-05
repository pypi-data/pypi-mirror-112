import json

import pytest
from rest_framework import status

from django_simple_api_auth.business_logic.user_create import UserCreate
from tests.api.graphql.common import BaseGraphQLTestCase


@pytest.mark.django_db
class TestLogin(BaseGraphQLTestCase):
    def test_login(self):
        data = {
            "username": "test@test.com",
            "password": "password",
        }
        UserCreate(**data).execute()
        mutation = '''
            mutation userLogin($input: UserLoginMutationInput!){
                userLogin(input: $input){
                    ok,
                    errors,
                }
            }
        '''
        operation_name = 'userLogin'
        response = self.query(mutation, operation_name=operation_name, input_data=data)
        assert response.status_code == status.HTTP_200_OK
        content = json.loads(response.content)
        assert 'errors' not in content
        assert 'csrftoken' in response.cookies.keys()
        assert 'sessionid' in response.cookies.keys()
