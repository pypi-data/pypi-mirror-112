from django.core.exceptions import ValidationError
from django.http import HttpRequest
from social_core.exceptions import MissingBackend, AuthForbidden
from social_django.utils import load_strategy, load_backend
from social_django.views import _do_login

from django_simple_api_auth.errors import UserSocialLoginErrors


class UserSocialLogin:

    def __init__(self, request: HttpRequest, provider: str, access_token: str):
        self.provider = provider
        self.request = request
        self.access_token = access_token

    def execute(self):
        strategy = load_strategy(self.request)
        backend = self.get_backend(strategy)
        authenticated_user = self.get_authenticated_user()
        user = self.do_user_auth(authenticated_user, backend)
        self.check_auth_errors(strategy, user)
        _do_login(backend, user, user.social_user)

    def check_auth_errors(self, strategy, user):
        user_model = strategy.storage.user.user_model()
        if not isinstance(user, user_model):
            raise ValidationError(UserSocialLoginErrors.AUTH_ERROR.value)

    def do_user_auth(self, authenticated_user, backend):
        try:
            user = backend.do_auth(self.access_token, user=authenticated_user)
        except AuthForbidden:
            raise ValidationError(UserSocialLoginErrors.INVALID_TOKEN.value)
        if user is None:
            raise ValidationError(UserSocialLoginErrors.INVALID_TOKEN.value)
        return user

    def get_authenticated_user(self):
        if self.request.user.is_authenticated:
            authenticated_user = self.request.user
        else:
            authenticated_user = None
        return authenticated_user

    def get_backend(self, strategy):
        try:
            backend = load_backend(strategy, self.provider, redirect_uri=None)
        except MissingBackend:
            raise ValidationError(UserSocialLoginErrors.PROVIDER_NOT_FOUND.value)
        return backend