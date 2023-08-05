from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = getattr(settings, 'ME_FIELDS', ("id",))
        read_only_fields = fields


class RecoveryPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class UserResetPasswordSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserSocialLoginSerializer(serializers.Serializer):
    provider = serializers.CharField(required=True)
    access_token = serializers.CharField(required=True)
