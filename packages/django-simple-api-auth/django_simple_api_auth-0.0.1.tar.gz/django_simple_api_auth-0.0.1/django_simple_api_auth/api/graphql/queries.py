from graphene import ObjectType, Field
from graphql_extensions.decorators import login_required

from django_simple_api_auth.api.graphql.types import AuthUserType


class UserQuery(ObjectType):
    get_me = Field(AuthUserType)

    @login_required
    def resolve_get_me(self, info, **kwargs):
        return info.context.user
