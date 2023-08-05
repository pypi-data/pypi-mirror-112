from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from django_simple_api_auth.errors import UserCreateErrors

User = get_user_model()


class UserCreate:

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def execute(self) -> User:
        try:
            User.objects.get_by_natural_key(self.username)
            raise ValidationError(UserCreateErrors.USER_ALREADY_EXISTS.value)
        except User.DoesNotExist as exc:
            return User.objects.create_user(username=self.username, password=self.password, email=self.username)
