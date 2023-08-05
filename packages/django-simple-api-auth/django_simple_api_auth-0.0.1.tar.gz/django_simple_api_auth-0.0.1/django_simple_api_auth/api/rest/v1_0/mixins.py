from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from django_simple_api_auth.api.rest.v1_0.serializers import UserLoginSerializer, \
    RecoveryPasswordSerializer, UserResetPasswordSerializer
from django_simple_api_auth.business_logic.user_create import UserCreate
from django_simple_api_auth.business_logic.user_login import UserLogin
from django_simple_api_auth.business_logic.user_logout import UserLogout
from django_simple_api_auth.business_logic.user_password_recovery import UserPasswordRecovery
from django_simple_api_auth.business_logic.user_reset_password import UserResetPassword
from django_simple_api_auth.business_logic.user_social_login import UserSocialLogin


class UserCreateMixin:

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserCreate(**serializer.validated_data).execute()
        return Response(status=status.HTTP_201_CREATED)


class UserLoginMixin:

    @action(detail=False, methods=['POST'], url_path='login', serializer_class=UserLoginSerializer)
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        UserLogin(**validated_data, request=request).execute()
        return Response(status=status.HTTP_200_OK)


class UserLogoutMixin:

    @action(detail=False, methods=['POST'], url_path='logout')
    def logout(self, request, *args, **kwargs):
        UserLogout(request).execute()
        return Response(status=status.HTTP_200_OK)


class UserMeMixin:

    @action(detail=False, url_path='me', methods=['GET'])
    def me(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserPasswordRecoveryMixin:
    @action(detail=False, methods=['POST'], url_path='password-recovery')
    def password_recovery(self, request, *args, **kwargs):
        serializer = RecoveryPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserPasswordRecovery(request, request.data.get('email')).execute()
        return Response(status=200)


class UserResetPasswordMixin:
    @action(detail=False, methods=['POST'], url_path='reset-password')
    def reset_password(self, request, *args, **kwargs):
        serializer = UserResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserResetPassword(
            serializer.validated_data.get('id'),
            serializer.validated_data.get('token'),
            serializer.validated_data.get('password'),
        ).execute()
        return Response(status=200)


class UserSocialLoginMixin:

    @action(detail=False, methods=['POST'], url_path='social-login')
    def social_login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        UserSocialLogin(**validated_data, request=request).execute()
        return Response(status=status.HTTP_200_OK)


class UserCompleteViewSet(UserCreateMixin, UserLoginMixin, UserMeMixin, UserPasswordRecoveryMixin, UserLogoutMixin,
                          UserSocialLoginMixin, UserResetPasswordMixin):
    pass
