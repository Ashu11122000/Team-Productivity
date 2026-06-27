from datetime import datetime, timedelta, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class RefreshToken(Base):
    """
    Refresh Token Model.

    Stores hashed refresh tokens for secure session management.

    Supports:
    - Refresh Token Rotation
    - Logout
    - Logout from All Devices
    - Session Revocation
    - Future Device Tracking
    """

    __tablename__ = "refresh_tokens"

    __table_args__ = (
        Index("idx_refresh_token_user", "user_id"),
        Index("idx_refresh_token_expires", "expires_at"),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    token_hash = Column(
        String(255),
        unique=True,
        nullable=False,
    )

    is_revoked = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    expires_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(days=7),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    revoked_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    user = relationship(
        "User",
        lazy="joined",
    )

    def __repr__(self) -> str:
        return (
            f"RefreshToken("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"revoked={self.is_revoked}"
            f")"
        )