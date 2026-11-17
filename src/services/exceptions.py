class AppError(Exception):
    """Базовое исключение приложения."""

class NotFoundError(AppError):
    """Объект не найден."""

class ForbiddenError(AppError):
    """Недостаточно прав."""

class InvalidTransitionError(AppError):
    """Недопустимый переход статуса."""

class ValidationError(AppError):
    """Некорректные входные данные."""
