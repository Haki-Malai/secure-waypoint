from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="The unique identifier for this record")
    created_at: datetime = Field(
        ..., description="The date and time this record was created"
    )
    updated_at: datetime = Field(
        ..., description="The date and time this record was last updated"
    )
