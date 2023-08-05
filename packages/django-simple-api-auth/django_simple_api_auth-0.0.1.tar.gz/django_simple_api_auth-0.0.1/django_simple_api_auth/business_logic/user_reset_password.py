from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.exceptions import ValidationError

from django_simple_api_auth.errors import UserResetPasswordErrors


class UserResetPassword:

    def __init__(self, id: str, token: str, password: str):
        self.password = password
        self.token = token
        self.id = id

    def execute(self):
        token_error = ValidationError(UserResetPasswordErrors.INVALID_OR_EXPIRED_TOKEN.value)
        try:
            user = PasswordResetConfirmView().get_user(self.id)
            if not PasswordResetTokenGenerator().check_token(user, self.token):
                raise token_error
            user.set_password(self.password)
            user.save()
        except Exception:
            raise token_error
