from typing import Any


def success_response(
    *,
    message: str,
    data: Any = None,
) -> dict:
    """
    Standard success response.
    """

    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_response(
    *,
    message: str,
    errors: list | None = None,
) -> dict:
    """
    Standard error response.
    """

    return {
        "success": False,
        "message": message,
        "errors": errors or [],
    }


def paginated_response(
    *,
    message: str,
    data: Any,
    pagination: dict,
) -> dict:
    """
    Standard paginated response.
    """

    return {
        "success": True,
        "message": message,
        "data": data,
        "pagination": pagination,
    }