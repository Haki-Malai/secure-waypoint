import re

from pydantic import BaseModel, constr, field_validator

from app.models import Role


class BaseUserRequest(BaseModel):
    username: str

    @field_validator("username")
    def username_must_not_contain_special_characters(cls, v):
        if v is not None and re.search(r"[^a-zA-Z0-9]", v):
            raise ValueError("Username must not contain special characters")
        return v


class RegisterUserRequest(BaseUserRequest):
    password: constr(min_length=8, max_length=64)


class UpdateUserRequest(BaseUserRequest):
    username: constr(min_length=3, max_length=64) | None = None
    role: Role | None = None
    password: constr(min_length=8, max_length=64) | None = None
