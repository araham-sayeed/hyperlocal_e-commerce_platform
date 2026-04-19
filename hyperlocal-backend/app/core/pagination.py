from math import ceil
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    limit: int
    offset: int
    page: int
    pages: int

    @classmethod
    def build(cls, items: list[T], total: int, limit: int, offset: int):
        page = (offset // limit) + 1 if limit else 1
        pages = ceil(total / limit) if limit else 1
        return cls(items=items, total=total, limit=limit, offset=offset, page=page, pages=pages)
