import json

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

from tests.api.graphql.common import BaseGraphQLTestCase


@pytest.mark.django_db
class TestCreateUser(BaseGraphQLTestCase):

    def test_create_user(self):
        mutation = '''
            mutation userCreate($input: UserCreateMutationInput!){
                userCreate(input: $input){
                    ok,
                    errors,
                }
            }
        '''
        operation_name = 'userCreate'
        data = {
            "username": "test@test.com",
            "password": "password",
        }
        response = self.query(mutation, operation_name=operation_name, input_data=data)
        assert response.status_code == status.HTTP_200_OK
        content = json.loads(response.content)
        assert 'errors' not in content
        assert get_user_model().objects.count() == 1
