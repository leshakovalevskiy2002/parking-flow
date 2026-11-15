from app.domain.errors.base import DomainError


class UserError(DomainError):
    """User flow error"""


class UserAlreadyExistsError(UserError):
    code = "USER_ALREADY_EXISTS"

    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(f"User with email=`{email}` already exists")
