from math import ceil


def pagination_metadata(
    *,
    page: int,
    limit: int,
    total: int,
) -> dict:
    """
    Build pagination metadata.
    """

    total_pages = ceil(total / limit) if total else 1

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
    }