from enum import Enum


class UserCreateErrors(Enum):
    USER_ALREADY_EXISTS = 'USER_ALREADY_EXISTS'


class UserLoginErrors(Enum):
    LOGIN_FAILED = 'LOGIN_FAILED'


class UserLogoutErrors(Enum):
    LOGOUT_FAILED = 'LOGOUT_FAILED'


class UserSocialLoginErrors(Enum):
    PROVIDER_NOT_FOUND = 'PROVIDER_NOT_FOUND'
    INVALID_TOKEN = 'INVALID_TOKEN'
    AUTH_ERROR = 'AUTH_ERROR'


class UserResetPasswordErrors(Enum):
    INVALID_OR_EXPIRED_TOKEN = 'INVALID_OR_EXPIRED_TOKEN'
