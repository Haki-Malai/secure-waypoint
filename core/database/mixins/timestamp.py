from datetime import UTC, datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr


def utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=utc_now, nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime,
            default=utc_now,
            onupdate=utc_now,
            nullable=False,
        )
