import re

from pydantic import BaseModel, constr, field_validator


class RegisterUserRequest(BaseModel):
    username: constr(min_length=3, max_length=64)
    password: constr(min_length=8, max_length=64)

    @field_validator("username")
    def username_must_not_contain_special_characters(cls, v):
        if re.search(r"[^a-zA-Z0-9]", v):
            raise ValueError("Username must not contain special characters")
        return v
