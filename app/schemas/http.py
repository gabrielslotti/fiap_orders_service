from pydantic import BaseModel
from typing import Any


class DefaultResponse(BaseModel):
    """HTTP Default Response Schema."""

    detail: str | Any
