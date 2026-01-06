"""Global exception handlers for the API."""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.api.schemas.error import (
    ErrorBody,
    ErrorDetail,
    ErrorResponse,
    internal_error,
)


class NotFoundError(Exception):
    """Resource not found exception."""

    def __init__(self, resource: str = "Resource"):
        self.resource = resource
        super().__init__(f"{resource} not found")


class UnauthorizedError(Exception):
    """Unauthorized access exception."""

    def __init__(self, message: str = "Authentication required"):
        self.message = message
        super().__init__(message)


class ConflictError(Exception):
    """Resource conflict exception."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ValidationError(Exception):
    """Custom validation exception."""

    def __init__(self, message: str, details: list[ErrorDetail] | None = None):
        self.message = message
        self.details = details
        super().__init__(message)


def setup_exception_handlers(app: FastAPI) -> None:
    """Configure global exception handlers for the application."""

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Handle Pydantic validation errors."""
        details = []
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
            details.append(ErrorDetail(field=field or "body", message=error["msg"]))

        response = ErrorResponse(
            error=ErrorBody(
                code="VALIDATION_ERROR",
                message="Invalid request data",
                details=details,
            )
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response.model_dump(),
        )

    @app.exception_handler(NotFoundError)
    async def not_found_exception_handler(
        request: Request, exc: NotFoundError
    ) -> JSONResponse:
        """Handle not found errors."""
        response = ErrorResponse(
            error=ErrorBody(
                code="NOT_FOUND",
                message=f"{exc.resource} not found",
            )
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response.model_dump(),
        )

    @app.exception_handler(UnauthorizedError)
    async def unauthorized_exception_handler(
        request: Request, exc: UnauthorizedError
    ) -> JSONResponse:
        """Handle unauthorized errors."""
        response = ErrorResponse(
            error=ErrorBody(
                code="UNAUTHORIZED",
                message=exc.message,
            )
        )
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=response.model_dump(),
        )

    @app.exception_handler(ConflictError)
    async def conflict_exception_handler(
        request: Request, exc: ConflictError
    ) -> JSONResponse:
        """Handle conflict errors."""
        response = ErrorResponse(
            error=ErrorBody(
                code="CONFLICT",
                message=exc.message,
            )
        )
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=response.model_dump(),
        )

    @app.exception_handler(ValidationError)
    async def custom_validation_exception_handler(
        request: Request, exc: ValidationError
    ) -> JSONResponse:
        """Handle custom validation errors."""
        response = ErrorResponse(
            error=ErrorBody(
                code="VALIDATION_ERROR",
                message=exc.message,
                details=exc.details,
            )
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response.model_dump(),
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle unexpected errors."""
        # Log the actual error for debugging
        import traceback
        print(f"ERROR: {exc}")
        traceback.print_exc()
        response = internal_error()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response.model_dump(),
        )
