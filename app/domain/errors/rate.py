from app.domain.errors.base import DomainError


class RateError(DomainError):
    """Rate flow error"""


class RateAlreadyExistsError(RateError):
    code = "RATE_ALREADY_EXISTS"

    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Rate with name `{name}` already exists")


class RateNotExistsError(RateError):
    code = "RATE_NOT_EXISTS"

    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Rate with name `{name}` does not exist")


class RateInUseError(RateError):
    code = "RATE_IN_USE"

    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Rate with name `{name}` is used")
