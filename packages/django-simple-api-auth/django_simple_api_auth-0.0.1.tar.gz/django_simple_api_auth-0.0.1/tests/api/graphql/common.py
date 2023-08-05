import pytest
from graphene_django.utils.testing import graphql_query, GraphQLTestCase


@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=client)

    return func


class BaseGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_URL = '/s/graphqls/'
