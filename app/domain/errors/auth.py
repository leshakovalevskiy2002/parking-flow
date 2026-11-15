from app.domain.errors.base import DomainError


class AuthError(DomainError):
    """Authentication flow error"""


class InvalidCredentialsError(AuthError):
    code = "INVALID_CREDENTIALS"

    def __init__(self, message: str = "Incorrect email or password") -> None:
        super().__init__(message)


class InactiveUserError(AuthError):
    code = "INACTIVE_USER"

    def __init__(self, message: str = "Inactive user") -> None:
        super().__init__(message)


class TokenValidationError(AuthError):
    code = "INVALID_TOKEN"

    def __init__(self, message: str = "Invalid token") -> None:
        super().__init__(message)


class ExpiredTokenError(AuthError):
    code = "EXPIRED_TOKEN"

    def __init__(self, message: str = "Token is expired") -> None:
        super().__init__(message)
