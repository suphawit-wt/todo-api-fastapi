from dataclasses import dataclass


@dataclass
class AppException(Exception):
    code: str
    status_code: int
    message: str


def BadRequestError(message: str) -> AppException:
    return AppException(code="BAD_REQUEST", status_code=400, message=message)


def UnauthorizedError(message: str) -> AppException:
    return AppException(code="UNAUTHORIZED", status_code=401, message=message)


def ForbiddenError(message: str) -> AppException:
    return AppException(code="FORBIDDEN", status_code=403, message=message)


def NotFoundError(message: str) -> AppException:
    return AppException(code="NOT_FOUND", status_code=404, message=message)


def ConflictError(message: str) -> AppException:
    return AppException(code="CONFLICT", status_code=409, message=message)


def DatabaseError(message: str) -> AppException:
    return AppException(code="DATABASE_ERROR", status_code=500, message=message)


def UnexpectedError() -> AppException:
    return AppException(code="UNEXPECTED", status_code=500, message="Unexpected error")
