import graphene
from django.core.exceptions import ValidationError
from graphene import ClientIDMutation

from django_simple_api_auth.business_logic.user_create import UserCreate
from django_simple_api_auth.business_logic.user_login import UserLogin
from django_simple_api_auth.business_logic.user_logout import UserLogout
from django_simple_api_auth.business_logic.user_password_recovery import UserPasswordRecovery
from django_simple_api_auth.business_logic.user_reset_password import UserResetPassword
from django_simple_api_auth.business_logic.user_social_login import UserSocialLogin
from django_simple_api_auth.errors import UserCreateErrors, UserLoginErrors, UserLogoutErrors, UserSocialLoginErrors, \
    UserResetPasswordErrors


class UserCreateMutation(ClientIDMutation):
    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.Enum.from_enum(UserCreateErrors))

    @classmethod
    def mutate_and_get_payload(cls, root, info, *args, **kwargs):
        try:
            UserCreate(**kwargs).execute()
            return cls(ok=True)
        except ValidationError as exc:
            return cls(ok=False, errors=exc.messages)


class UserLoginMutation(ClientIDMutation):
    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.Enum.from_enum(UserLoginErrors))

    @classmethod
    def mutate_and_get_payload(cls, root, info, *args, **kwargs):
        try:
            UserLogin(request=info.context, **kwargs).execute()
            return cls(ok=True)
        except ValidationError as exc:
            return cls(ok=False, errors=exc.messages)


class UserLogoutMutation(ClientIDMutation):
    ok = graphene.Boolean()
    errors = graphene.List(graphene.Enum.from_enum(UserLogoutErrors))

    @classmethod
    def mutate_and_get_payload(cls, root, info, *args, **kwargs):
        try:
            UserLogout(request=info.context).execute()
            return cls(ok=True)
        except ValidationError as exc:
            return cls(ok=False, errors=exc.messages)


class UserPasswordRecoveryMutation(ClientIDMutation):
    class Input:
        email = graphene.String(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, email):
        UserPasswordRecovery(info.context, email).execute()
        return cls(ok=True)


class UserSocialLoginMutation(ClientIDMutation):
    class Input:
        provider = graphene.String(required=True)
        access_token = graphene.String(required=True)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.Enum.from_enum(UserSocialLoginErrors))

    @classmethod
    def mutate_and_get_payload(cls, root, info, *args, **kwargs):
        try:
            UserSocialLogin(request=info.context, **kwargs).execute()
            return cls(ok=True)
        except ValidationError as exc:
            return cls(ok=False, errors=exc.messages)


class UserResetPasswordMutation(ClientIDMutation):
    class Input:
        id = graphene.String(required=True)
        token = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.Enum.from_enum(UserResetPasswordErrors))

    @classmethod
    def mutate_and_get_payload(cls, root, info, *args, **kwargs):
        try:
            UserResetPassword(**kwargs).execute()
            return cls(ok=True)
        except ValidationError as exc:
            return cls(ok=False, errors=exc.messages)


class UsersMutation(graphene.ObjectType):
    user_create = UserCreateMutation.Field()
    user_login = UserLoginMutation.Field()
    user_social_login = UserSocialLoginMutation.Field()
    user_logout = UserLogoutMutation.Field()
    user_password_recovery = UserPasswordRecoveryMutation.Field()
    user_reset_password = UserResetPasswordMutation.Field()
