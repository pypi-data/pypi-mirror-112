# -*- coding: utf-8 -*-
# Python imports

# Django imports

# 3rd Party imports
import graphene

# App imports
from django_simple_api_auth.api.graphql.mutations import UsersMutation
from django_simple_api_auth.api.graphql.queries import UserQuery


class Query(UserQuery, graphene.ObjectType):
    pass



class Mutation(UsersMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
