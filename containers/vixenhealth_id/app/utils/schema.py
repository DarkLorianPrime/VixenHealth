from json import JSONDecodeError
from typing import Any, Dict

from pydantic import BaseModel
from starlette.datastructures import FormData
from starlette.requests import Request


class CustomModel(BaseModel):
    @classmethod
    async def as_form(cls, request: Request) -> "CustomModel":
        data: Dict[str, Any] | FormData
        data = await request.form()

        if not data:
            try:
                data = await request.json()
            except JSONDecodeError:
                data = {}

        return cls(**data)
