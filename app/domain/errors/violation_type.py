from app.domain.errors.base import DomainError


class ViolationTypeError(DomainError):
    """Violation type flow error"""


class ViolationTypeNotFoundError(ViolationTypeError):
    code = "VIOLATION_TYPE_NOT_FOUND"

    def __init__(self, identifier: str) -> None:
        self.identifier = identifier
        super().__init__(f"Violation type '{identifier}' not found")
