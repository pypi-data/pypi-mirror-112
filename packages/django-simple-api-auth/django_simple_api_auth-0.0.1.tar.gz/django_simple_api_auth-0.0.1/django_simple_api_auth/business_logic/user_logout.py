from django.contrib.auth import logout
from django.core.exceptions import ValidationError
from django.http import HttpRequest

from django_simple_api_auth.errors import UserLogoutErrors


class UserLogout:

    def __init__(self, request: HttpRequest):
        self.request = request

    def execute(self):
        try:
            logout(self.request)
        except Exception as exc:
            raise ValidationError(UserLogoutErrors.LOGOUT_FAILED.value)
