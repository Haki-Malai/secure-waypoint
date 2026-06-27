import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


def convert_datetime_to_realworld(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.UTC).isoformat().replace("+00:00", "Z")


def convert_field_to_camel_case(string: str) -> str:
    return "".join(
        word if index == 0 else word.capitalize()
        for index, word in enumerate(string.split("_"))
    )


class Base(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={datetime.datetime: convert_datetime_to_realworld},
        alias_generator=convert_field_to_camel_case,
    )

    def to_create_attributes(self) -> dict[str, Any]:
        return self.model_dump()

    def to_update_attributes(self) -> dict[str, Any]:
        return self.model_dump(exclude_unset=True)
