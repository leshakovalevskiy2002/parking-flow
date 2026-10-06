class AuthServiceError(Exception):
    pass


class InvalidCredentialsError(AuthServiceError):
    code = "INVALID_CREDENTIALS"

    def __init__(self, message: str = "Incorrect email or password") -> None:
        super().__init__(message)


class TokenValidationError(AuthServiceError):
    code = "INVALID_TOKEN"

    def __init__(self, message: str = "Invalid token") -> None:
        super().__init__(message)


class ExpiredTokenError(AuthServiceError):
    code = "EXPIRED_TOKEN"

    def __init__(self, message: str = "Token is expired") -> None:
        super().__init__(message)


class InactiveUserError(AuthServiceError):
    code = "INACTIVE_USER"

    def __init__(self, message: str = "Inactive user"):
        super().__init__(message)
