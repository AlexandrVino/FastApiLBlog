class InvalidCredentialsError(Exception):
    def __init__(self, field: str = None):
        default = "Invalid credentials were provide"
        message = field and f"Invalid credentials were provide at field={field}"
        super().__init__(message or default)
