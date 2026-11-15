class DomainError(Exception):
    """Base domain exception"""

    code: str = "BASE_DOMAIN_ERROR"
