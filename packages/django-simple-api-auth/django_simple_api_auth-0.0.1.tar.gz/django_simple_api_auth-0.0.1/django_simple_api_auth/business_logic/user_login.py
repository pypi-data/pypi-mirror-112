from django.contrib.auth import authenticate, login, get_user_model
from django.core.exceptions import ValidationError
from rest_framework.request import Request

from django_simple_api_auth.errors import UserLoginErrors

# ModelBackend

User = get_user_model()


class UserLogin:

    def __init__(self, username: str, password: str, request: Request):
        self.username = username
        self.password = password
        self.request = request

    def execute(self):
        try:
            data = {
                "password": self.password,
                User.USERNAME_FIELD: self.username,
            }
            user = authenticate(**data)
            if user is None:
                raise ValidationError(UserLoginErrors.LOGIN_FAILED.value)
            login(request=self.request, user=user)
        except Exception as exc:
            raise ValidationError(UserLoginErrors.LOGIN_FAILED.value)
