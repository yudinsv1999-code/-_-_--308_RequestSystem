class AppError(Exception):
    """Базовое исключение приложения."""

class NotFoundError(AppError):
    """Объект не найден."""

class ForbiddenError(AppError):
    """Недостаточно прав."""

class ConflictError(AppError):
    """Конфликт состояния (повторное назначение, недопустимый переход)."""

class InvalidTransitionError(ConflictError):
    """Недопустимый переход статуса."""

class ValidationError(AppError):
    """Некорректные входные данные."""