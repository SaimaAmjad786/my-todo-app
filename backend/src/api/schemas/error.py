"""Error response schemas per OpenAPI spec."""

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Individual field error detail."""

    field: str
    message: str


class ErrorBody(BaseModel):
    """Error body structure."""

    code: str
    message: str
    details: list[ErrorDetail] | None = None


class ErrorResponse(BaseModel):
    """Standard error response wrapper."""

    error: ErrorBody


# Pre-defined error responses
def validation_error(message: str, details: list[ErrorDetail] | None = None) -> ErrorResponse:
    """Create a validation error response."""
    return ErrorResponse(
        error=ErrorBody(
            code="VALIDATION_ERROR",
            message=message,
            details=details,
        )
    )


def unauthorized_error(message: str = "Authentication required") -> ErrorResponse:
    """Create an unauthorized error response."""
    return ErrorResponse(
        error=ErrorBody(
            code="UNAUTHORIZED",
            message=message,
        )
    )


def not_found_error(resource: str = "Resource") -> ErrorResponse:
    """Create a not found error response."""
    return ErrorResponse(
        error=ErrorBody(
            code="NOT_FOUND",
            message=f"{resource} not found",
        )
    )


def conflict_error(message: str) -> ErrorResponse:
    """Create a conflict error response."""
    return ErrorResponse(
        error=ErrorBody(
            code="CONFLICT",
            message=message,
        )
    )


def internal_error(message: str = "Internal server error") -> ErrorResponse:
    """Create an internal server error response."""
    return ErrorResponse(
        error=ErrorBody(
            code="INTERNAL_ERROR",
            message=message,
        )
    )
