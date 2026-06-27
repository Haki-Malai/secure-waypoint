import re
from datetime import date
from typing import Annotated

from pydantic import StringConstraints, field_validator

from app.models import Role
from app.schemas.requests.base import Base

Username = Annotated[str, StringConstraints(min_length=3, max_length=64)]
Password = Annotated[str, StringConstraints(min_length=8, max_length=64)]


class BaseUserRequest(Base):
    username: Username

    @field_validator("username")
    @classmethod
    def username_must_not_contain_special_characters(
        cls, value: str | None
    ) -> str | None:
        if value is not None and re.search(r"[^a-zA-Z0-9]", value):
            raise ValueError("Username must not contain special characters")
        return value


class RegisterUserRequest(BaseUserRequest):
    password: Password


class UpdateUserRequest(BaseUserRequest):
    username: Username | None = None
    role: Role | None = None
    password: Password | None = None


class UpdateSelfRequest(BaseUserRequest):
    username: Username | None = None
    password: Password | None = None


class UserPagination(Base):
    skip: int = 0
    limit: int = 10
    creation_year: int | None = None

    @field_validator("creation_year")
    @classmethod
    def validate_year(cls, value: int | None) -> int | None:
        current_year = date.today().year
        if value is not None and (value > current_year or value < 1900):
            raise ValueError("Invalid year")
        return value
