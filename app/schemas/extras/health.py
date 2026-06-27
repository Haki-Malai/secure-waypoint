from pydantic import BaseModel, Field


class Health(BaseModel):
    version: str = Field(..., json_schema_extra={"example": "0.0.1"})
    status: str = Field(..., json_schema_extra={"example": "OK"})
