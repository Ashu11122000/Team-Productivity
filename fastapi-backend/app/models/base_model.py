from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime


class BaseModelMixin:
    """
    Base mixin providing common audit fields.

    This mixin should be inherited alongside SQLAlchemy's Base:

        class Example(Base, BaseModelMixin):
            ...

    Shared Fields:
    - created_at
    - updated_at
    - deleted_at
    - is_active
    """

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )