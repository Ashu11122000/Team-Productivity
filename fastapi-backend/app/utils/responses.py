from typing import Any


def success_response(
    *,
    message: str,
    data: Any = None,
) -> dict[str, Any]:
    """
    Standard success response.
    """

    return {
        "success": True,
        "message": message,
        "data": data,
        "errors": [], 
    }


def error_response(
    *,
    message: str,
    errors: list[Any] | None = None,
) -> dict[str, Any]:
    """
    Standard error response.
    """

    return {
        "success": False,
        "message": message,
        "data": None,
        "errors": errors or [], 
    }


def paginated_response(
    *,
    message: str,
    data: Any,
    pagination: dict[str, Any],
) -> dict[str, Any]:
    """
    Standard paginated response.
    """
    return {
        "success": True,
        "message": message,
        "data": data,
        "errors": [],
        "pagination": pagination, 
    }