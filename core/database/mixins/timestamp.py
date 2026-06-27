from datetime import UTC, datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr


def utc_now() -> datetime:
    """Return the current UTC timestamp as a naive datetime.

    SQLAlchemy stores the timestamp columns without timezone information, so
    this helper normalizes the UTC value before persistence.

    :return: A naive datetime representing the current UTC time.
    """
    return datetime.now(UTC).replace(tzinfo=None)


class TimestampMixin:
    @declared_attr
    def created_at(cls):
        """Declare the model creation timestamp column.

        :return: A non-nullable SQLAlchemy datetime column populated on insert.
        """
        return Column(DateTime, default=utc_now, nullable=False)

    @declared_attr
    def updated_at(cls):
        """Declare the model update timestamp column.

        :return: A non-nullable SQLAlchemy datetime column updated on changes.
        """
        return Column(
            DateTime,
            default=utc_now,
            onupdate=utc_now,
            nullable=False,
        )
