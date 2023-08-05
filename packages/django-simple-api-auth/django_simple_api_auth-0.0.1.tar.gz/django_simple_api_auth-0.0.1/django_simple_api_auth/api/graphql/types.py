from django.conf import settings
from django.contrib.auth import get_user_model
from graphene import relay
from graphene_django import DjangoObjectType

User = get_user_model()


class AuthUserType(DjangoObjectType):
    class Meta:
        name = 'AuthUserType'
        model = User
        interfaces = (relay.Node,)
        fields = getattr(settings, 'ME_FIELDS', ("id",))
