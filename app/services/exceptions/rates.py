class RateServiceError(Exception):
    pass


class RateAlreadyExistsError(RateServiceError):
    code = "RATE_ALREADY_EXISTS"

    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Rate with name `{name}` already exists")


class RateNotExistsError(RateServiceError):
    code = "RATE_NOT_EXISTS"

    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Rate with name `{name}` does not exist")


class RateInUseError(RateServiceError):
    code = "RATE_IN_USE"

    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Rate with name `{name}` is used")
