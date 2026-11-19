from fastapi import Request
from fastapi.responses import JSONResponse
from src.services.exceptions import (
    AppError, NotFoundError, ForbiddenError, ValidationError,
    ConflictError, InvalidTransitionError
)

def register_error_handlers(app):
    @app.exception_handler(NotFoundError)
    def not_found(request: Request, exc: NotFoundError):
        return JSONResponse(status_code=404, content={"error": "not_found", "detail": str(exc)})

    @app.exception_handler(ForbiddenError)
    def forbidden(request: Request, exc: ForbiddenError):
        return JSONResponse(status_code=403, content={"error": "forbidden", "detail": str(exc)})

    @app.exception_handler(ValidationError)
    def validation(request: Request, exc: ValidationError):
        return JSONResponse(status_code=400, content={"error": "validation", "detail": str(exc)})

    @app.exception_handler(InvalidTransitionError)
    def invalid_transition(request: Request, exc: InvalidTransitionError):
        return JSONResponse(status_code=409, content={"error": "invalid_transition", "detail": str(exc)})

    @app.exception_handler(ConflictError)
    def conflict(request: Request, exc: ConflictError):
        return JSONResponse(status_code=409, content={"error": "conflict", "detail": str(exc)})

    @app.exception_handler(AppError)
    def app_error(request: Request, exc: AppError):
        return JSONResponse(status_code=400, content={"error": "app_error", "detail": str(exc)})
