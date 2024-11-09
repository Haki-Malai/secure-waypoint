from pydantic import Field

from .base import BaseResponse


class UserResponse(BaseResponse):
    username: str = Field(..., description="The username of the user")

    class Config:
        from_attributes = True
