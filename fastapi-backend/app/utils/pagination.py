from math import ceil
from typing import Any


def pagination_metadata(
    *,
    page: int,
    limit: int,
    total: int,
) -> dict[str, Any]:
    """
    Build pagination metadata.
    """
    if page < 1:
        raise ValueError("Page number must be greater than or equal to 1.")

    if limit < 1:
        raise ValueError("Limit must be greater than or equal to 1.")

    if total < 0:
        raise ValueError("Total cannot be negative.")
    
    total_pages = max(1, ceil(total / limit))

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
        "next_page": page + 1 if page < total_pages else None,
        "previous_page": page - 1 if page > 1 else None,
        "is_first_page": page == 1,
        "is_last_page": page >= total_pages,  
    }
    
__all__ = [
    "pagination_metadata",
]