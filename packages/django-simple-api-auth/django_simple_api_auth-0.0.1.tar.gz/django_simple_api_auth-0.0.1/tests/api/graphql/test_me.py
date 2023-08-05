import json

import pytest
from graphql_relay import from_global_id
from rest_framework import status

from django_simple_api_auth.business_logic.user_create import UserCreate
from tests.api.graphql.common import BaseGraphQLTestCase


@pytest.mark.django_db
class TestMe(BaseGraphQLTestCase):

    def test_me(self):
        data = {
            "username": "test@test.com",
            "password": "password",
        }
        user = UserCreate(**data).execute()
        self.client.force_login(user)
        query = '''
            query getMe{
                getMe{
                    id,
                }
            }
        '''
        operation_name = 'getMe'
        response = self.query(query, operation_name=operation_name)
        assert response.status_code == status.HTTP_200_OK
        content = json.loads(response.content)
        assert 'errors' not in content
        relay_id = content['data'][operation_name]['id']
        assert int(from_global_id(relay_id).id) == user.id
