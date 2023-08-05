from django.contrib.auth import get_user_model
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from django_simple_api_auth.api.rest.v1_0.mixins import UserCompleteViewSet
from django_simple_api_auth.api.rest.v1_0.serializers import UserCreateSerializer, UserLoginSerializer, \
    UserReadSerializer, UserSocialLoginSerializer
from django_simple_api_auth.utils.rest.viewsets.views import MultiConfApiViewMixin

User = get_user_model()


class UserApiViewSet(UserCompleteViewSet, MultiConfApiViewMixin):
    queryset = User.objects.all()
    serializer_classes_dict = {
        'create': UserCreateSerializer,
        'login': UserLoginSerializer,
        'me': UserReadSerializer,
        'social-login': UserSocialLoginSerializer
    }
    authentication_classes = [SessionAuthentication]
    permission_classes_dict = {
        'create': [AllowAny],
        'login': [AllowAny],
        'me': [IsAuthenticated],
        'social-login': [AllowAny],
        'password-recovery': [AllowAny],
        'logout': [IsAuthenticated],
        'reset-password': [AllowAny],
    }
